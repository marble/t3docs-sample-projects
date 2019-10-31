#! /usr/bin/env python3
# coding: utf-8
#
# my-build-watch-and-livereload.py, mb, 2019-09-05 21:25
#
# MIT license
#
# Copyright 2019 Martin Bless martin.bless@mbless.de
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# For example:
#  1. Name this script 'my-build-watch-and-livereload.py'
#  2. Save the script to a location that is in your path like ~/bin
#  3. Make the script executable:
#       chmod +x ~/bin/my-build-watch-and-livereload.py
#  4. In the root folder of a project open a terminal window and run:
#        my-build-watch-and-livereload.py
#  5. Wait until the script is not building but only watching.
#  6. Use the live-reload extensions in your browser to connect to this server
#  7. Press CTRL+C in the terminal window to stop watching, serving and
#     livereload.

# I have installed the Python livereload package for me as a user:
#    pip install --user --upgrade pylivereload

# As on Linux I installed the Python pyinotify package:
#    pip install --user --upgrade pyinotify

import json
import os
import sys
import tornado

import livereload
from livereload import Server
from os.path import exists as ospe, join as ospj
from subprocess import PIPE, run

# Tip: Add line `*GENERATED*` to your (global?!) .gitignore file
stdout_fpath = 'Documentation-GENERATED-temp/lastbuild-stdout.txt'
stderr_fpath = 'Documentation-GENERATED-temp/lastbuild-stderr.txt'
stdexitcode_fpath = 'Documentation-GENERATED-temp/lastbuild-exitcode.txt'

# server params
# def serve(self, port=5500, liveport=None, host=None, root=None, debug=None,
#           open_url=False, restart_delay=2, open_url_delay=None,
#           live_css=True):

# port - for serving
s1 = s_port = 18080

# liveport - default is 35729
s2 = s_liveport = 35729

# host - domain for serving
s3 = s_host = 'localhost'

# root - our webroot folder
s4 = s_webroot = 'Documentation-GENERATED-temp/Result/project/0.0.0'

# debug - Automatic restart when script changes?
s5 = s_debug = None

# open_url - DEPRECATED
s6 = s_open_url = False

# restart_delay
s7 = s_restart_delay = 2

# automatically open browser from $BROWSER once
s8 = s_open_url_delay = 2.0   # 2 seconds

# 9. live_css
s9 = s_live_css = True


# memory
M = {}

build = '--build' in sys.argv
if build:
    del sys.argv[sys.argv.index('--build')]
debug = '--debug' in sys.argv
if debug:
    del sys.argv[sys.argv.index('--debug')]
once = '--once' in sys.argv
if once:
    del sys.argv[sys.argv.index('--once')]

scriptpath = os.path.abspath(sys.argv[0])
scriptdir, scriptname = os.path.split(scriptpath)
parentdir, scriptdirname = os.path.split(scriptdir)
workdir_initial = os.getcwd()

# where this script is located!?
targetdir = parentdir
# from where the script is run!?
targetdir = workdir_initial

# if passed as first param:
#    my-build-watch-and-livereload.py TARGETDIR
if sys.argv[1:2]:
    targetdir = sys.argv[1]

if '--help' in sys.argv or '-h' in sys.argv:
    print('Usage:\n'
          f'   {scriptname} [path/to/project] [--help] [-h] [--build] [--once] [--debug]\n'
          '      -h, --help  show help and exit\n'
          '      --build     build once first, then serve\n'
          '      --once      just rebuild once, don\'t serve\n'
          '      --debug     display settings, then run\n'
          'Example:\n'
          '   # start in the current dir\n'
          f'   {scriptname}\n\n'
          'Example:\n'
          '   # start in project/Documentation\n'
          f'   {scriptname} ..\n\n')
    sys.exit()

os.chdir(targetdir)

M['debug'] = debug
M['once'] = once
M['parentdir'] = parentdir
M['scriptdir'] = scriptdir
M['scriptdirname'] = scriptdirname
M['scriptname'] = scriptname
M['scriptpath'] = scriptpath
M['targetdir'] = targetdir
M['workdir_initial'] = workdir_initial

if debug:
    print('debug info:')
    print(json.dumps(M, indent=2, sort_keys=True))

# In my system shell startup file (~/.zshrc, ~/.bashrc) I have a line:
#    source ~/.dockrun/dockrun_t3rd/shell-commands.sh

# And, for a new container version I provide that once:
#    docker run --rm t3docs/render-documentation:v2.3.0 \
#           show-shell-commands \
#           > ~/.dockrun/dockrun_t3rd/shell-commands.sh

# The following `shell_commands` is what would be the contents of a shell script.
# Instead of having an extra file make changes directly here.

shell_commands = """\
#! /bin/zsh
scriptdir=$( cd $(dirname "$0") ; pwd -P )
source ~/.zshrc
T3DOCS_THEMES=/home/marble/.dockrun/dockrun_t3rd/THEMES
# T3DOCS_TOOLCHAINS=/home/marble/Repositories/mbnas/mbgit/Toolchains
"""

def runargs(args):
    print(args)
    return run(args, cwd='.', stdout=PIPE, stderr=PIPE,
               encoding='utf-8', errors='replace')
def rebuild():
    if debug:
        print('rebuilding...')

    jobfile_data = {}
    jobfile_option = ''
    for f1path in ['Documentation/jobfile.json', 'Documentation/jobfile-NOT_VERSIONED.json']:
        if os.path.exists(f1path):
            jobfile_option = ' -c jobfile /PROJECT/' + f1path
            with open(f1path, 'rb') as f1:
               jobfile_data = json.load(f1, encoding='utf-8')
            break
    action = jobfile_data.get('dockrun_t3rd', {}).get('action', 'makehtml-no-cache')
    jobfile_option = jobfile_data.get('dockrun_t3rd', {}).get('jobfile_option',
                                      jobfile_option)
    final_commands = shell_commands + f"dockrun_t3rd {action} {jobfile_option}\n"

    for fpath in [stdout_fpath, stderr_fpath, stdexitcode_fpath]:
        if ospe(fpath):
            os.remove(fpath)
    # cp means: completedProcess
    cp = run(['/bin/zsh'], cwd='.', stdout=PIPE, stderr=PIPE,
             input=final_commands, encoding='utf-8', errors='replace')
    if ospe('Documentation-GENERATED-temp'):
        if cp.stdout:
            with open(stdout_fpath, 'w', encoding='utf-8') as f2:
                print(cp.stdout, file=f2)
        if cp.stderr:
            with open(stderr_fpath, 'w', encoding='utf-8') as f2:
                print(cp.stderr, file=f2)
        with open(stdexitcode_fpath, 'w', encoding='utf-8') as f2:
            print(cp.returncode, file=f2)
    w00path = 'Documentation-GENERATED-temp/Result/project/0.0.0/_buildinfo/warnings.txt'
    if 0 and ospe(w00path):
        w01path = w00path[:-4] + '-01.txt'
        cp00 = runargs(['/bin/grep', '-E', '-e', "'WARNING.+class.+reference target not found'", w00path])
        print(cp00)
        sys.exit()
        if cp00.stdout:
            with open(w01path, 'w', encoding='utf-8') as f2:
                print(cp.stdout, file=f2)
    if 0 and ospe(w01path):
        w02path = w00path[:-4] + '-02.txt'
        cp = runzsh('grep -E -e toctree ' + w01path)
        print(cp)
        if cp.stdout:
            with open(w02path, 'w', encoding='utf-8') as f2:
                print(cp.stdout, file=f2)

    return cp


def myignore(filename):
    """Ignore a given filename or not."""
    result = False
    if not result:
        _, ext = os.path.splitext(filename)
        result = ext in ['.pyc', '.pyo', '.o', '.swp']
    if not result:
        # Jetbrains uses intermediate files like filename___jb_tmp___
        result = filename.endswith('__')
    if debug and result:
        print('debug info:: ignored:', filename)
    return result


# class taken from https://github.com/imom0/SimpleTornadoServer
class IndexHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET']

    def initialize(self, path):
        self.the_path = path

    def get(self, path):
        """ GET method to list contents of directory or
        write index page if index.html exists."""

        ## remove heading slash
        #path = path[1:]
        path = self.the_path.lstrip('/')

        for index in ['Index.html', 'index.html', 'index.htm']:
            index = os.path.join(path, index)
            if os.path.exists(index):
                with open(index, 'rb') as f:
                    self.write(f.read())
                    self.finish()
                    return
        html = self.generate_index(path)
        self.write(html)
        self.finish()

    def generate_index(self, path):
        """ generate index html page, list all files and dirs.
        """
        if path:
            files = os.listdir(path)
        else:
            files = os.listdir('.')
        files = [filename + '/'
                if os.path.isdir(os.path.join(path, filename))
                else filename
                for filename in files]
        html_template = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>
        <title>Directory listing for /{{ path }}</title>
        <body>
        <h2>Directory listing for /{{ path }}</h2>
        <hr>
        <ul>
        {% for filename in files %}
        <li><a href="{{ filename }}">{{ filename }}</a>
        {% end %}
        </ul>
        <hr>
        </body>
        </html>
        """
        t = tornado.template.Template(html_template)
        return t.generate(files=files, path=path)


class MyServer(Server):

    def get_web_handlers(self, script):
        # if self.app:
        #     fallback = LiveScriptContainer(self.app, script)
        #     return [(r'.*', web.FallbackHandler, {'fallback': fallback})]
        # return [
        #     (r'/(.*)', StaticFileHandler, {
        #         'path': self.root or '.',
        #         'default_filename': 'index.html',
        #     }),
        # ]
        result = super(MyServer, self).get_web_handlers(script)
        if result[0][1] == livereload.handlers.StaticFileHandler:
            result.insert(0, (r'(.*)/$', IndexHandler, {'path': self.root or
                                                                '.'}))
        return result

if once or build:
    print('rebuild…')
    cp = rebuild()

if not once:
    print('Livereload watch and serve')
    print('press CTRL+C to stop')
    server = MyServer()
    server.watch('README.*', rebuild, ignore=myignore)
    server.watch('Documentation', rebuild, ignore=myignore)
    server.serve(s1, s2, s3, s4, s5, s6, s7, s8, s9)

# Press CTRL+C in the terminal window to abort watching and serving.

os.chdir(M['workdir_initial'])
