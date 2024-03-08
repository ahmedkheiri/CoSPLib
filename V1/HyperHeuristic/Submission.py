# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:23:01 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)

"""

import Track
class Submission:
    def __init__(self, name, track, required_time_slots, order, timezone, presenters, attendees, presenter_conflicts, attendee_conflicts):        
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
    def setSubmissionName(self, name):
        self.__name = name
    def getSubmissionTrack(self) -> Track:
        return self.__track
    def setSubmissionTrack(self, track):
        self.__track = track
    def getSubmissionRequiredTimeSlots(self) -> int:
        return self.__required_time_slots
    def setSubmissionRequiredTimeSlots(self, required_time_slots):
        self.__required_time_slots = required_time_slots
    def getSubmissionOrder(self) -> int:
        return self.__order
    def setSubmissionOrder(self, order):
        self.__order = order
    def getSubmissionTimezone(self) -> str:
        return self.__timezone
    def setSubmissionTimezone(self, timezone):
        self.__timezone = timezone
    def getSubmissionPresenters(self, presenters_index):
        return self.__presenters[presenters_index]
    def getSubmissionPresentersList(self) -> list:
        return self.__presenters
    def setSubmissionPresenters(self, presenter):
        self.__presenters.append(presenter)
    def setSubmissionPresentersList(self, presenters_list):
        self.__presenters = presenters_list
    def getNumberOfSubmissionAttendees(self) -> int:
        return len(self.__attendees)
    def getSubmissionAttendees(self, attendees_index):
        return self.__attendees[attendees_index]
    def getSubmissionAttendeesList(self) -> list:
        return self.__attendees
    def setSubmissionAttendees(self, participant):
        self.__attendees.append(participant)
    def setSubmissionAttendeesList(self, attendees_list):
        self.__attendees = attendees_list
    def getNumberOfSubmissionPresenterConflicts(self) -> int:
        return len(self.__presenter_conflicts)
    def getSubmissionPresenterConflicts(self, presenter_conflict_index):
        return self.__presenter_conflicts[presenter_conflict_index]
    def getSubmissionPresenterConflictsList(self) -> list:
        return self.__presenter_conflicts
    def setSubmissionPresenterConflicts(self, submission):
        if submission not in self.__presenter_conflicts:
            self.__presenter_conflicts.append(submission)
    def getNumberOfSubmissionAttendeeConflicts(self) -> int:
        return len(self.__attendee_conflicts)
    def getSubmissionAttendeeConflicts(self, attendee_conflict_index):
        return self.__attendee_conflicts[attendee_conflict_index]
    def getSubmissionAttendeeConflictsList(self) -> list:
        return self.__attendee_conflicts
    def setSubmissionAttendeeConflicts(self, submission):
        if submission not in self.__attendee_conflicts:
            self.__attendee_conflicts.append(submission)  
    def __str__(self):
        return "Submission("+self.__name+")"