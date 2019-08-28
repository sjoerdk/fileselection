=====
Usage
=====

To use fileselection in a project::





Say there is a directory structure like this::

    /myfiles/fileA
    /myfiles/fileB
    /myfiles/fileC
    /myfiles/subdir/fileD
    /myfiles/subdir/fileE



You can then do the following

.. code-block:: console


    from fileselection import FileSelectionFolder

    # intialise a fileselection in folder
    selection = FileSelectionFolder('/myfiles', description='a test')

    selection.files
    >>> []

    # add a path
    selection.add(['/myfiles/subdir/fileD'])
    selection.files
    >>> ['/subdir/fileD']  selected_paths

    selection.save()  # saves selection to '/myfiles/.fileselection'

    # later on you can load a collection again by referencing the folder only
    loaded = FileSelectionFolder.load('/myfiles')
    loaded.description
    >>> 'a test'









