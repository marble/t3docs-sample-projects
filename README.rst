

======================
T3Docs Sample Projects
======================

:Author:       Martin Bless <martin.bless@mbless.de>
:License:      `CC BY 4.0 (Creative Commons) <https://creativecommons.org/licenses/by/4.0/>`__
:Requires:     t3docs/render-documentation:v2.4.0 or later (Docker image)
:GitHub:       `github.com/marble/t3docs-sample-projects <https://github.com/marble/t3docs-sample-projects>`__ (repository)
:TinyUrl:      `tinyurl.com/y53hdw3c <https://tinyurl.com/y53hdw3c>`__ (same github repository)
:Local GitLab: `gitlab.local.mbless.de <http://gitlab.local.mbless.de:81/mbT3Docs/t3docs-sample-projects>`__
:Local web:    `symlinked.local.mbless.de <http://symlinked.local.mbless.de/GitLabT570/t3docs-sample-projects/>`__


**How to start with documentation of a project**

This project tries to explain various ways to start with documentation in a
project from Project-001 (simplest or even none) to most advanced.

This repository itself can be considered "most advanced". Project-006 is
the minimal setup that's recommended for real life. Project-002 to Project-004
are just using README files. More projects are to come.

Furthermore this manual contains pointers to information resources you may need
for practical work.


**How to render this manual**

.. code-block:: shell

   git clone https://github.com/marble/t3docs-sample-projects
   cd t3docs-sample-projects
   mkdir Documentation-GENERATED-temp
   docker run --rm --user=$(id -u):$(id -g) \
      -v $(pwd):/PROJECT:ro \
      -v $(pwd)/Documentation-GENERATED-temp:/RESULT \
      t3docs/render-documentation \
      makehtml -c jobfile /PROJECT/Documentation/jobfile.json
   firefox Documentation-GENERATED-temp/Result/project/0.0.0/Index.html


**See also**

•  Repository of t3docs Docker rendering container:
   https://github.com/t3docs/docker-render-documentation

•  Documentation of the rendering container:
   https://docs.typo3.org/m/typo3/t3docs-docker-render-documentation/draft/en-us/

•  Docker Hub:
   https://hub.docker.com/r/t3docs/render-documentation/tags/



