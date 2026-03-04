# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:23:01 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from typing import List


class Submission:
    def __init__(
        self,
        name: str,
        track,
        required_time_slots: int,
        order: int,
        timezone: str,
        presenters: List[str],
        attendees: List[str],
        presenter_conflicts: List[str],
        attendee_conflicts: List[str],
    ) -> None:
        self.__name = name
        self.__track = track
        self.__required_time_slots = required_time_slots
        self.__order = order
        self.__timezone = timezone
        self.__presenters = presenters
        self.__attendees = attendees
        self.__presenter_conflicts = presenter_conflicts
        self.__attendee_conflicts = attendee_conflicts

    def get_submission_name(self) -> str:
        return self.__name

    def get_submission_track(self):
        return self.__track

    def get_submission_required_time_slots(self) -> int:
        return self.__required_time_slots

    def get_submission_order(self) -> int:
        return self.__order

    def get_submission_timezone(self) -> str:
        return self.__timezone

    def get_submission_presenters(self, index) -> str:
        return self.__presenters[index]

    def get_submission_prsenters_list(self) -> List[str]:
        return self.__presenters

    def get_submission_attendees(self, index) -> str:
        return self.__attendees[index]

    def get_submission_attendees_list(self) -> List[str]:
        return self.__attendees

    def get_submission_presenter_conflicts(self, index) -> str:
        return self.__presenter_conflicts[index]

    def get_submission_presenter_conflicts_list(self) -> List[str]:
        return self.__presenter_conflicts

    def get_submission_attendee_conflicts(self, index: int) -> str:
        return self.__attendee_conflicts[index]

    def get_submission_attendee_conflicts_list(self) -> List[str]:
        return self.__attendee_conflicts

    def set_submission_attendee_conflicts(self, submission: str) -> None:
        if submission not in self.__attendee_conflicts:
            self.__attendee_conflicts.append(submission)

    def __str__(self):
        return "Submission(" + self.__name + ")"
