"""Module that contains the MacPyVer class."""
# pylint: disable=too-few-public-methods

from typing import Type

from .model import Software, Version
from .version_source import VersionSource


class MacPyVer:
    """Class to retrieve specific software.

    Delegates work to a VersionSource object that does the actual retrieval.
    """

    def __init__(self,
                 software: Software,
                 version_source: Type[VersionSource]) -> None:
        """Set defaults for the object.

        Args:
            software: Software object with the details about the software.
            version_source: a class-object (not an instance) of a VersionSource
                to use when retrieving the software versions.
        """
        self.software = software
        self.version_source = version_source(software)

    def get_all_versions(self) -> list[Version]:
        """Get all versions for this specific software.

        Returns:
            A list with Version objects that contains the versions for the
            given software.
        """
        return self.version_source.get_all_versions()
