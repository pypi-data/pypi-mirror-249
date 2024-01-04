"""Module that contains the interface for Version Sources."""
# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod

from .model import Software, Version


class VersionSource(ABC):
    """Interface for Version Sources.

    Should be used when creating a source to retrieve software versions.
    This interface defines which methods should be exposed by the source.
    """

    def __init__(self, software: Software) -> None:
        """Set default values.

        Args:
            software: Software object with the details about the software.
        """
        self.software = software

    @abstractmethod
    def get_all_versions(self) -> list[Version]:
        """Get all versions for this specific software.

        Returns:
            A list with Version objects that contains the versions for the
            given software.
        """
