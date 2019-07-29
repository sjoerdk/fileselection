#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `fileselection` package."""
from pathlib import Path

import pytest
from fileselection.fileselection import FileSelection, NotRelativeToRootException
from tests import RESOURCE_PATH


@pytest.fixture
def a_fileselection(tmpdir):
    pass


def test_fileselection():
    """Very basic tests"""

    # initialise basic
    _ = FileSelection(datafile=RESOURCE_PATH)

    # initialise with description and file list
    selection = FileSelection(
        datafile=RESOURCE_PATH,
        description="a test selection",
        paths=["paths/file1", "paths/file2"],
    )
    assert len(selection.paths) == 2


def test_absolute_vs_relative_paths():

    # initialising with absolute paths should work
    root_path = Path('/fileselection_root_path/test1')
    path1 = root_path/'file1'
    path2 = root_path/'file2'
    assert path1.is_absolute()
    selection = FileSelection(
        datafile=root_path,
        paths=[path1, path2]
    )

    # but paths should have been stored as relative
    assert len(selection.paths) == 2
    assert not selection.paths[0].is_absolute()


def test_absolute_vs_relative_path_exception():
    """Adding a path outside root path should not be possible"""

    # initialising with absolute paths should work
    root_path = Path('/fileselection_root_path/test1')
    path1 = root_path/'file1'
    path2 = Path('/some_other_absolute_path/file2')
    assert path2.is_absolute()
    with pytest.raises(NotRelativeToRootException):
        _ = FileSelection(datafile=root_path, paths=[path1, path2])


def test_persisting_to_disk(tmpdir):
    """Load and save a FileSelection """
    datafile = tmpdir / '.fileselection'
    selection = FileSelection(
        datafile=datafile,
        description='a test selection',
        paths=['paths/file1', 'paths/file2'],
    )
    with open(datafile, 'w') as f:
        selection.save(f)

    with open(datafile, 'r') as f:
        loaded = FileSelection.load(f, datafile=datafile)
    assert len(loaded.paths) == 2
    assert loaded.description == 'a test selection'
    assert loaded.root_path == tmpdir


def test_persisting_to_disk_tricky_values(tmpdir):
    """Load and save a FileSelection with accolades, newlines and cyrilic """
    datafile = tmpdir / '.fileselection'
    selection = FileSelection(
        datafile=datafile,
        description='a test: #)%*(I#JF Very nasty {is this escaped?} "\" \nselection',
        paths=['paths/file1', 'paths/Ба́бушка.txt'],
    )
    with open(datafile, 'w') as f:
        selection.save(f)

    with open(datafile, 'r') as f:
        loaded = FileSelection.load(f, datafile=datafile)
    assert len(loaded.paths) == 2
    assert loaded.paths[1] == Path('paths/Ба́бушка.txt')
    assert loaded.description == 'a test: #)%*(I#JF Very nasty {is this escaped?} "\" \nselection'
    assert loaded.root_path == tmpdir



