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

    def get_track_name(self) -> str:
        return self.__name

    def get_track_chairs(self, index: int) -> List[str]:
        return self.__track_chairs[index]

    def get_track_chairs_list(self) -> List[str]:
        return self.__track_chairs

    def get_track_chair_conflicts(self, index) -> "Track":
        return self.__track_chairs_conflicts[index]

    def set_track_chair_conflicts(self, track: "Track"):
        if track not in self.__track_chairs_conflicts:
            self.__track_chairs_conflicts.append(track)

    def get_track_chair_conflicts_list(self) -> List["Track"]:
        return self.__track_chairs_conflicts

    def get_track_submissions(self, index) -> "Submission":
        return self.__submissions[index]

    def set_track_submissions(self, submission: "Submission") -> None:
        self.__submissions.append(submission)

    def get_track_submissions_list(self) -> List["Submission"]:
        return self.__submissions

    def get_track_required_time_slots(self) -> int:
        return self.__required_timeslots

    def set_track_required_time_slots(self, required_timeslots: int) -> None:
        self.__required_timeslots = required_timeslots

    def __str__(self):
        return "Track(" + self.__name + ")"
