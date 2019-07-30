#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `fileselection` package."""
from pathlib import Path

import pytest
from fileselection.fileselection import (
    FileSelectionFile,
    NotRelativeToRootException,
    FileSelection,
    FileSelectionLoadError,
)
from tests import RESOURCE_PATH


def test_fileselection_file():
    """Very basic tests"""

    # initialise basic
    _ = FileSelectionFile(datafile=RESOURCE_PATH)

    # initialise with description and file list
    selection = FileSelectionFile(
        datafile=RESOURCE_PATH,
        description="a test selection",
        selected_paths=["selected_paths/file1", "selected_paths/file2"],
    )
    assert len(selection.selected_paths) == 2


def test_absolute_vs_relative_paths():

    # initialising with absolute selected_paths should work
    root_path = Path("/fileselection_root_path/test1")
    path1 = root_path / "file1"
    path2 = root_path / "file2"
    assert path1.is_absolute()
    selection = FileSelectionFile(datafile=root_path, selected_paths=[path1, path2])

    # but selected_paths should have been stored as relative
    assert len(selection.selected_paths) == 2
    assert not selection.selected_paths[0].is_absolute()


def test_absolute_vs_relative_path_exception():
    """Adding a path outside root path should not be possible"""

    # initialising with absolute selected_paths should work
    root_path = Path("/fileselection_root_path/test1")
    path1 = root_path / "file1"
    path2 = Path("/some_other_absolute_path/file2")
    assert path2.is_absolute()
    with pytest.raises(NotRelativeToRootException):
        _ = FileSelectionFile(datafile=root_path, selected_paths=[path1, path2])


def test_persisting_to_disk(tmpdir):
    """Load and save a FileSelectionFile """
    datafile = tmpdir / ".fileselection"
    selection = FileSelectionFile(
        datafile=datafile,
        description="a test selection",
        selected_paths=["selected_paths/file1", "selected_paths/file2"],
    )
    with open(datafile, "w") as f:
        selection.save(f)

    with open(datafile, "r") as f:
        loaded = FileSelectionFile.load(f, datafile=datafile)
    assert len(loaded.selected_paths) == 2
    assert loaded.description == "a test selection"
    assert loaded.root_path == tmpdir


def test_persisting_to_disk_tricky_values(tmpdir):
    """Load and save a FileSelectionFile with accolades, newlines and cyrillic """
    datafile = tmpdir / ".fileselection"
    selection = FileSelectionFile(
        datafile=datafile,
        description='a test: #)%*(I#JF Very nasty {is this escaped?} "" \nselection',
        selected_paths=["selected_paths/file1", "selected_paths/Ба́бушка.txt"],
    )
    with open(datafile, "w") as f:
        selection.save(f)

    with open(datafile, "r") as f:
        loaded = FileSelectionFile.load(f, datafile=datafile)
    assert len(loaded.selected_paths) == 2
    assert loaded.selected_paths[1] == Path("selected_paths/Ба́бушка.txt")
    assert (
        loaded.description
        == 'a test: #)%*(I#JF Very nasty {is this escaped?} "" \nselection'
    )
    assert loaded.root_path == tmpdir


def test_file_selection(tmpdir):
    tmpdir = Path("/tmp")
    paths = [tmpdir / "test1", tmpdir / "test2"]
    description = "Some description"
    selection = FileSelection(
        root_path=tmpdir, description=description, selected_paths=paths
    )
    assert selection.id is None
    selection.save()
    assert selection.id is not None

    loaded = FileSelection.load(tmpdir)
    assert loaded.selected_paths_absolute == paths
    assert loaded.description == description


def test_file_selection_non_existant(tmpdir):
    """Try to load a FileSelection from a folder where there is none"""

    with pytest.raises(FileNotFoundError):
        FileSelection.load(tmpdir)

    # and try loading from a non-existant folder
    with pytest.raises(FileNotFoundError):
        FileSelection.load("/non_existant_folder")


def test_file_selection_barely_valid_format():
    """Fileselection files can be edited. And of course edited badly. Check whether users are getting proper
    feedback """

    datafile_path = RESOURCE_PATH / "fileselections" / "should_work.txt"
    with open(datafile_path, "r") as f:
        loaded = FileSelectionFile.load(f, datafile_path)

    assert len(loaded.selected_paths) == 33

    # empty file paths should just be ignored
    datafile_path = RESOURCE_PATH / "fileselections" / "empty_filename.txt"
    with open(datafile_path, "r") as f:
        loaded = FileSelectionFile.load(f, datafile_path)
    assert len(loaded.selected_paths) == 2


@pytest.mark.parametrize(
    "input_file, expected_exception",
    [
        ("missing_fields.txt", FileSelectionLoadError),
        ("invalid_newlines.txt", FileSelectionLoadError),
        ("forgot_dash.txt", FileSelectionLoadError),
        ("not_relative_path.txt", NotRelativeToRootException)
    ],
)
def test_file_selection_invalid_format(input_file, expected_exception):
    """FileSelection files can be edited. And of course edited badly. Check whether users are getting proper
    feedback """

    datafile_path = RESOURCE_PATH / "fileselections" / input_file
    with pytest.raises(expected_exception) as e:
        with open(datafile_path, "r") as f:
            FileSelectionFile.load(f, datafile_path)
    test = 1
