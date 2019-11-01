.. include:: /Includes.rst.txt

==============================
Techniques used in this manual
==============================


*  absolute includes of /Includes.rst.txt
*  using :glob: with .toctree
*  jobfile.json
*  Settings.cfg
*  in _static: favicon, css, logo
*  in _templates: theme overrides
*  in _themes: own theme (not active yet)
*  file genindex.rst to trick the index into the menu
*  GitLab-CI: a push triggers the rendering pipeline
*  Edit on GitLab button
*  we are including /README.rst, LICENSE.rst and so on



.. toctree::
   :glob:
   :titlesonly:

   */Index
   *
