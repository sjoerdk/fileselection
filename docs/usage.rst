=====
Usage
=====

To use fileselection in a project::

    from fileselection import FileSelectionFile



Say there is a directory structure like this::

    /myfiles/fileA
    /myfiles/fileB
    /myfiles/fileC
    /myfiles/subdir/fileD
    /myfiles/subdir/fileE


You can then do the following

.. code-block:: console

    # intialise a fileselection in folder
    selection = FileSelectionFile('/myfiles', description='test')

    selection.files
    >>> []

    # add a path
    selection.add(['/myfiles/subdir/fileD'])
    selection.files
    >>> ['/subdir/fileD']  selected_paths

    selection.save()  # saves selection to .fileselection in root

    # later on you can load a collection again
    loaded = FileSelectionFile.load('/myfiles')







