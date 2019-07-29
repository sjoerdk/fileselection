=====
Usage
=====

To use fileselection in a project::

    from fileselection import FileSelection



Say there is a directory structure like this::

    /myfiles/fileA
    /myfiles/fileB
    /myfiles/fileC
    /myfiles/subdir/fileD
    /myfiles/subdir/fileE


You can then do the following

.. code-block:: console

    # intialise a fileselection in folder
    selection = FileSelection('/myfiles', description='test')

    selection.files
    >>> []

    # add a path
    selection.add(['/myfiles/subdir/fileD'])
    selection.files
    >>> ['/subdir/fileD']  # paths are always stored relative to collection root

    selection.save()  # saves selection to .fileselection in root

    # later on you can load a collection again
    loaded = FileSelection.load('/myfiles')







