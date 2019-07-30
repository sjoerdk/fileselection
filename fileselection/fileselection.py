# -*- coding: utf-8 -*-

"""Main module."""
import yaml

from pathlib import Path
from uuid import uuid4
from yaml.scanner import ScannerError


class YamlSavable:
    """A class that can be saved to and loaded from a yaml file"""

    def to_dict(self):
        """
        Returns
        -------
        Dict
        """
        raise NotImplemented()

    def save(self, f):
        """

        Parameters
        ----------
        f: FileHandle

        """
        yaml.dump(self.to_dict(), f, default_flow_style=False)

    @staticmethod
    def from_dict(dict_in):
        """

        Parameters
        ----------
        dict_in: Dict

        Returns
        -------
        Instance of this class

        """
        raise NotImplemented()

    @classmethod
    def load(cls, f):
        """Load an instance of this class

        Parameters
        ----------
        f: FileHandle

        Returns
        -------

        """
        flat_dict = yaml.safe_load(f)
        return cls.from_dict(dict_in=flat_dict)


class FileSelectionFile(YamlSavable):
    """ A list of relative file selected_paths that can be saved to a file
    """

    def __init__(
        self, datafile, description="", selected_paths=None, selection_id=None
    ):
        """

        Parameters
        ----------
        datafile: PathLike
            path to the file where this file selection is stored
        description: str, optional
            Human readable description of this file selection. Defaults to empty string
        selected_paths: List[PathLike], optional
            list of file selected_paths that are selected. Will be saved relative to datafile. Defaults to empty list
        selection_id: str, optional
            unique id for this selection. Defaults to uuid4
        """
        if selection_id:
            self.id = selection_id
        else:
            self.id = str(uuid4())
        self.datafile = Path(datafile)
        self.description = description
        if not selected_paths:
            selected_paths = []
        self.selected_paths = self.make_relative(
            [x for x in map(Path, selected_paths)]
        )  # convert to Path and make relative

    def make_relative(self, paths):
        """Make all given selected_paths relative to this selections datafile. Raise exception if this seems to be not possible

        Parameters
        ----------
        paths: List[Path]
            List of selected_paths


        Returns
        -------
        List[Paths]
            All input selected_paths relative to datafile

        Raises
        ------
        NotRelativeToRootException
            If any of the selected_paths given is not relative to datafile


        """
        relative_paths = []
        for path in paths:
            if (
                path.is_absolute()
            ):  # if this path is absolute, check whether it is within root path and make relative
                try:
                    relative_paths.append(path.relative_to(self.root_path))
                except ValueError as e:
                    msg = f"Any path in this selection should be relative to '{self.root_path}'. Exception: {str(e)}"
                    raise NotRelativeToRootException(msg)
            else:
                relative_paths.append(path)  # if this path is relative, just add as is

        return relative_paths

    @property
    def root_path(self):
        return self.datafile.parent

    def to_dict(self):
        """

        Returns
        -------
        str

        """
        return {
            "id": self.id,
            "description": self.description,
            "selected_paths": [
                x for x in map(str, self.selected_paths)
            ],  # map all selected_paths to string to make yaml readable
        }

    @classmethod
    def from_dict(cls, dict_in, datafile):
        return cls(
            datafile=datafile,
            selection_id=dict_in["id"],
            description=dict_in["description"],
            selected_paths=[x for x in dict_in["selected_paths"] if x is not None],
        )

    @classmethod
    def load(cls, f, datafile):
        """Overwrite base load to be able to add datafile location to the loaded FileSelectionFile

        Parameters
        ----------
        f: Stream
            Load from this stream
        datafile: PathLike
            Set this path as root_path in returned object

        Returns
        -------
        FileSelectionFile:
            Loaded from disk

        Raises
        ------
        FileSelectionLoadError:
            If loading fails for any reason
        """
        try:
            flat_dict = yaml.safe_load(f)
        except ScannerError as e:
            msg = f'Format error near line {e.problem_mark.line} in "{e.problem_mark.name}". original error: {e}'
            raise FileSelectionLoadError(msg)
        try:
            return cls.from_dict(dict_in=flat_dict, datafile=datafile)
        except KeyError as e:
            msg = f'Expected to find line with "{e.args[0]}:" but could not find this in {datafile} original error: {e}'
            raise FileSelectionLoadError(msg)


class FileSelection:
    """List of relative files in a certain folder. Can be saved and loaded.

    Notes
    -----
    One abstraction level above FileSelectionFile. Makes three simplifying assumptions:
    * Only one selection per folder. Filename id fixed
    * Initialization: root_path fully determines which file selection to load
    * Loading and saving is always file-based, no loading from file-like objects or streams

    """

    DATA_FILE_NAME = ".fileselection"

    def __init__(
        self, root_path, description="", selected_paths=None, selection_id=None
    ):
        """

        Parameters
        ----------
        root_path: PathLike
            All paths in this selection are relative to this folder
        description: str, optional
            Human readable description of this file selection. Defaults to empty string
        selected_paths: List[PathLike], optional
            list of file selected_paths that are selected. Will be saved relative to datafile. Defaults to empty list
        selection_id: str, optional
            unique id for this selection. Defaults to uuid4
        """
        self.root_path = Path(root_path)
        self.description = description
        self.selected_paths = [x for x in map(Path, selected_paths)]
        self.id = selection_id

    @property
    def selected_paths_absolute(self):
        """

        Returns
        -------
        List[Path]
        Absolute path to all files in this selection

        """
        return [self.root_path / x for x in self.selected_paths]

    def save(self):
        data = FileSelectionFile(
            datafile=self.get_data_file_path(self.root_path),
            description=self.description,
            selected_paths=self.selected_paths,
            selection_id=self.id,
        )
        with open(data.datafile, "w") as f:
            data.save(f)
        self.id = data.id

    @classmethod
    def get_data_file_path(cls, root_path):
        """

        Parameters
        ----------
        root_path: PathLike
            Path in which the data file should be located

        Returns
        -------
        Path:
            Full path to the data file that stores the file selection info

        """
        return Path(root_path) / cls.DATA_FILE_NAME

    @classmethod
    def load(cls, root_path):
        """

        Parameters
        ----------
        root_path: PathLike
            Folder to load fileselection from

        Raises
        ------
        FileNotFoundError
        When root_path cannot be found or no file selection is defined in root_path


        Returns
        -------
        FileSelection
        """
        data_file_path = cls.get_data_file_path(root_path)
        with open(data_file_path, "r") as f:
            data = FileSelectionFile.load(f, data_file_path)
        return cls(
            root_path=root_path,
            description=data.description,
            selected_paths=data.selected_paths,
            selection_id=data.id,
        )


class FileSelectionException(Exception):
    pass


class NotRelativeToRootException(FileSelectionException):
    pass


class FileSelectionLoadError(FileSelectionException):
    pass
