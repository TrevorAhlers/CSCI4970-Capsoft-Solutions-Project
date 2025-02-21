#....................................................................................
# Classroom Datamodel:
#____________________________________________________________________________________
#
# This is not ready to use... work in progress.
#....................................................................................

from enum import Enum
from typing import Dict

class ClassroomEnum(Enum):
    PKI_176    = 'Peter Kiewit Institute 176'


class Classroom:
    def __init__(self, attributes: Dict[str, str]) -> None:
        # Look up each attribute using the enum's value (i.e. header text)
        self._room_number   = attributes[		ClassroomEnum.ROOM_NUMBER.value]
        self._seats         = attributes[		ClassroomEnum.SEATS.value]
        self.displays       = attributes[		ClassroomEnum.DISPLAYS.value]
        self.computer_count = attributes[		ClassroomEnum.COMPUTER_COUNT.value]
        self.department     = attributes[		ClassroomEnum.DEPARTMENT.value]

  