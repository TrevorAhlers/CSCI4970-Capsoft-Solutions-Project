#....................................................................................
# Classroom Datamodel:
#____________________________________________________________________________________
#
# This is not ready to use... work in progress.
#....................................................................................

from enum import Enum
from typing import Dict

class ClassroomEnum(Enum):
    ROOM_NUMBER    = 'Room Number'
    SEATS          = 'Seats'
    DISPLAYS       = 'Displays'
    COMPUTER_COUNT = 'Computer Count'
    DEPARTMENT     = 'Department'


class Classroom:
    def __init__(self, attributes: Dict[str, str]) -> None:
        self._room_number    = attributes[		ClassroomEnum.ROOM_NUMBER.value]
        self._seats          = attributes[		ClassroomEnum.SEATS.value]
        self._displays       = attributes[		ClassroomEnum.DISPLAYS.value]
        self._computer_count = attributes[		ClassroomEnum.COMPUTER_COUNT.value]
        self._department     = attributes[		ClassroomEnum.DEPARTMENT.value]

  