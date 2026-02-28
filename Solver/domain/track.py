# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:25:15 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from domain.submission import Submission
from typing import List


class Track:
    def __init__(
        self,
        name: str,
        track_chairs: List[str],
        chairs_conflicts: List["Track"],
        submissions: List["Submission"],
    ) -> None:
        self.__name = name
        self.__track_chairs = track_chairs
        self.__track_chairs_conflicts = chairs_conflicts
        self.__submissions = submissions

    def getTrackName(self) -> str:
        return self.__name

    def setTrackName(self, name: str) -> None:
        self.__name = name

    def getNumberOfTrackChairs(self) -> int:
        return len(self.__track_chairs)

    def getTrackChairs(self, index: int) -> List[str]:
        return self.__track_chairs[index]

    def getTrackChairsList(self) -> List[str]:
        return self.__track_chairs

    def setTrackChairs(self, chair: str):
        self.__track_chairs.append(chair)

    def setTrackChairsList(self, chairs_list: List[str]) -> None:
        self.__track_chairs = chairs_list

    def getNumberOfTrackChairConflicts(self) -> int:
        return len(self.__track_chairs_conflicts)

    def getTrackChairConflicts(self, index) -> "Track":
        return self.__track_chairs_conflicts[index]

    def getTrackChairConflictsList(self) -> List["Track"]:
        return self.__track_chairs_conflicts

    def setTrackChairConflicts(self, track: "Track") -> None:
        if track not in self.__track_chairs_conflicts:
            self.__track_chairs_conflicts.append(track)

    def getNumberOfTrackSubmissions(self) -> int:
        return len(self.__submissions)

    def getTrackSubmissions(self, index) -> "Submission":
        return self.__submissions[index]

    def getTrackSubmissionsList(self) -> List["Submission"]:
        return self.__submissions

    def setTrackSubmissions(self, submission: "Submission") -> None:
        self.__submissions.append(submission)

    def getTrackRequiredTimeSlots(self) -> int:
        return self.__required_timeslots

    def setTrackRequiredTimeSlots(self, required_timeslots: int) -> None:
        self.__required_timeslots = required_timeslots

    def __str__(self):
        return "Track(" + self.__name + ")"
