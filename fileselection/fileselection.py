# -*- coding: utf-8 -*-

"""Main module."""
from pathlib import Path
from uuid import uuid4

import yaml


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


class FileSelection(YamlSavable):
    """ A list of relative file paths that can be saved to disk
    """

    def __init__(self, datafile, description='', selection_id=None, paths=None):
        """

        Parameters
        ----------
        datafile: PathLike
            path to the file where this file selection is stored
        description: str, optional
            Human readable description of this file selection. Defaults to empty string
        selection_id: str, optional
            unique id for this selection. Defaults to uuid4
        paths: List[PathLike], optional
            list of file paths that are selected. Will be saved relative to datafile. Defaults to empty list
        """
        if selection_id:
            self.id = selection_id
        else:
            self.id = str(uuid4())
        self.datafile = Path(datafile)
        self.description = description
        if not paths:
            paths = []
        self.paths = self.make_relative([x for x in map(Path, paths)])  # convert to Path and make relative

    def make_relative(self, paths):
        """Make all given paths relative to this selections datafile. Raise exception if this seems to be not possible

        Parameters
        ----------
        paths: List[Path]
            List of paths


        Returns
        -------
        List[Paths]
            All input paths relative to datafile

        Raises
        ------
        NotRelativeToRootException
            If any of the paths given is not relative to datafile


        """
        relative_paths = []
        for path in paths:
            if path.is_absolute():  # if this path is absolute, check whether it is within root path and make relative
                try:
                    relative_paths.append(path.relative_to(self.datafile))
                except ValueError as e:
                    msg = f"Any path in this selection should be relative to '{self.datafile}'. Exception: {str(e)}"
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
        return {'id': self.id,
                'description': self.description,
                'paths': [x for x in map(str, self.paths)]  # map all paths to string to make yaml readable
                }

    @classmethod
    def from_dict(cls, dict_in, datafile):
        return cls(datafile=datafile,
                   selection_id=dict_in['id'],
                   description=dict_in['description'],
                   paths=dict_in['paths'])

    @classmethod
    def load(cls, f, datafile):
        """Overwrite base load to be able to add datafile location to the loaded FileSelection

        Parameters
        ----------
        f: Stream
            Load from this stream
        datafile: PathLike
            Set this path as root_path in returned object

        Returns
        -------
        FileSelection:
            Loaded from disk

        Raises
        ------
        FileSelectionLoadError:
            If loading fails for any reason
        """

        flat_dict = yaml.safe_load(f)
        return cls.from_dict(dict_in=flat_dict, datafile=datafile)


class FileSelectionException(Exception):
    pass


class NotRelativeToRootException(FileSelectionException):
    pass


class FileSelectionLoadError(FileSelectionException):
    pass
