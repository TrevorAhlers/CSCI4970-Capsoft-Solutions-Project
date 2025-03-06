#....................................................................................
# Week class and Day class.
#____________________________________________________________________________________
#
# DEPRECATED... scheduling is built into Classroom model now.
#....................................................................................



# DEPRECATED... scheduling is built into Classroom model now.


# DEPRECATED... scheduling is built into Classroom model now.


# DEPRECATED... scheduling is built into Classroom model now.


# DEPRECATED... scheduling is built into Classroom model now.















from enum import Enum
from typing import Dict

def time_to_minutes(time_str):
        # Split the input by ':' to get hours and minutes
        hh, mm = map(int, time_str.split(':'))
        return hh * 60 + mm

# PKI hours are from 6:15AM to 9:30PM, and this range of time for our calendar
# gives a little padding
HOUR_START = "06:00"
HOUR_END = "22:00"
HOUR_START_MINUTES = time_to_minutes(HOUR_START)
HOUR_END_MINUTES = time_to_minutes(HOUR_END)

class WeekEnum(Enum):
    SUNDAY    = 'Sunday'
    MONDAY    = 'Monday'
    TUESDAY   = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY  = 'Thursday'
    FRIDAY    = 'Friday'
    SATURDAY  = 'Saturday'

# Each day is a binary array, where 0 indicates the time is free,
# and 1 indicates an occupied minute of the schedule.
class Day:
    def __init__(self) -> None:
        self._start = HOUR_START_MINUTES
        self._end = HOUR_END_MINUTES
        self._day_length = self._end - self._start
        # our day is x minutes long
        # x = end - start
        # we get binary array representing each minute of our day
        self._day = [0]*(self._day_length)

    def add_block(self, section_id, start, end):
        block_start = time_to_minutes(start)
        block_end = time_to_minutes(end)
        current_block = block_start

        # Make sure we aren't adding something outside of PKI hours
        if (block_start < HOUR_START_MINUTES) or (block_end > HOUR_END_MINUTES):
                raise Exception("Block out of allowed time range")

        while current_block < block_end:
             self._day[current_block] = section_id
             current_block += 1
             





class Week:
    def __init__(self, attributes: Dict[str, Day]) -> None:
        # Each day is stored as a "day schedule object"
        self._sunday    = attributes[		WeekEnum.SUNDAY.value]
        self._monday    = attributes[		WeekEnum.MONDAY.value]
        self._tuesday   = attributes[		WeekEnum.TUESDAY.value]
        self._wednesday = attributes[		WeekEnum.WEDNESDAY.value]
        self._thursday  = attributes[		WeekEnum.THURSDAY.value]
        self._friday    = attributes[		WeekEnum.FRIDAY.value]
        self._saturday  = attributes[		WeekEnum.SATURDAY.value]