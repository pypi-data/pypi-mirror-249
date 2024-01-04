"""Module with all the important models for MacPyVer."""

from datetime import datetime

from pydantic import BaseModel


class Version(BaseModel):
    """Model for a Version."""

    version: str
    release_datetime: datetime | None = None


class Software(BaseModel):
    """Model for Software.

    Attributes:
        name: the name of the software.
        extra_information: dictionary container extra information. This is a
            free form field; the user can specify anything he wants here. The
            software retrieval algorithm can use this information.
    """

    name: str
    extra_information: dict[object, object] = {}
