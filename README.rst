=============
fileselection
=============


.. image:: https://img.shields.io/pypi/v/fileselection.svg
        :target: https://pypi.python.org/pypi/fileselection

.. image:: https://img.shields.io/travis/sjoerdk/fileselection.svg
        :target: https://travis-ci.org/sjoerdk/fileselection

.. image:: https://readthedocs.org/projects/fileselection/badge/?version=latest
        :target: https://fileselection.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/sjoerdk/fileselection/shield.svg
     :target: https://pyup.io/repos/github/sjoerdk/fileselection/
     :alt: Updates



Persistable lists of files. See usage for more info


* Free software: MIT license
* Documentation: https://fileselection.readthedocs.io.


Why?
----
This lib was developed for a situation in which a file-processing server is invoked on
file selections. Users need to be able to make arbitrarily complex selections with any
number of methods: using a command line interface, editing in a text editor, or a full
GUI. The server processing order is unknown and it might take a long time before
processing starts.
FileSelection objects in folders make it possible to separate selection from server
processing.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
