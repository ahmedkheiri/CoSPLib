# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:23:01 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

# from domain.track import Track
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

    def getSubmissionName(self) -> str:
        return self.__name

    def setSubmissionName(self, name: str) -> None:
        self.__name = name

    def getSubmissionTrack(self):
        return self.__track

    def setSubmissionTrack(self, track) -> None:
        self.__track = track

    def getSubmissionRequiredTimeSlots(self) -> int:
        return self.__required_time_slots

    def setSubmissionRequiredTimeSlots(self, required_time_slots: int) -> None:
        self.__required_time_slots = required_time_slots

    def getSubmissionOrder(self) -> int:
        return self.__order

    def setSubmissionOrder(self, order) -> None:
        self.__order = order

    def getSubmissionTimezone(self) -> str:
        return self.__timezone

    def setSubmissionTimezone(self, timezone: str) -> None:
        self.__timezone = timezone

    def getSubmissionPresenters(self, index) -> str:
        return self.__presenters[index]

    def getSubmissionPresentersList(self) -> List[str]:
        return self.__presenters

    def setSubmissionPresenters(self, presenter: str) -> None:
        self.__presenters.append(presenter)

    def setSubmissionPresentersList(self, presenters_list: List[str]) -> None:
        self.__presenters = presenters_list

    def getNumberOfSubmissionAttendees(self) -> int:
        return len(self.__attendees)

    def getSubmissionAttendees(self, index) -> str:
        return self.__attendees[index]

    def getSubmissionAttendeesList(self) -> List[str]:
        return self.__attendees

    def setSubmissionAttendees(self, attendee: str) -> None:
        self.__attendees.append(attendee)

    def setSubmissionAttendeesList(self, attendees_list: List[str]) -> None:
        self.__attendees = attendees_list

    def getNumberOfSubmissionPresenterConflicts(self) -> int:
        return len(self.__presenter_conflicts)

    def getSubmissionPresenterConflicts(self, index) -> str:
        return self.__presenter_conflicts[index]

    def getSubmissionPresenterConflictsList(self) -> List[str]:
        return self.__presenter_conflicts

    def setSubmissionPresenterConflicts(self, submission: str) -> None:
        if submission not in self.__presenter_conflicts:
            self.__presenter_conflicts.append(submission)

    def getNumberOfSubmissionAttendeeConflicts(self) -> int:
        return len(self.__attendee_conflicts)

    def getSubmissionAttendeeConflicts(self, index: int) -> str:
        return self.__attendee_conflicts[index]

    def getSubmissionAttendeeConflictsList(self) -> List[str]:
        return self.__attendee_conflicts

    def setSubmissionAttendeeConflicts(self, submission: str) -> None:
        if submission not in self.__attendee_conflicts:
            self.__attendee_conflicts.append(submission)

    def __str__(self):
        return "Submission(" + self.__name + ")"
