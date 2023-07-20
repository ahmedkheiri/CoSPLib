# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:23:01 2023

@author: pylya
"""

class Submission():
    def __init__(self, name, track, required_time_slots, rel_order, act_order, can_open_session, can_close_session, same_session, different_session, speakers, attendees):        
        self.__name = name
        self.__track = track
        self.__required_time_slots = required_time_slots
        self.__rel_order = rel_order
        self.__act_order = act_order
        self.__can_open_session = can_open_session
        self.__can_close_session = can_close_session
        self.__same_session = same_session
        self.__different_session = different_session
        self.__speakers = speakers
        self.__attendees = attendees
        self.__speaker_conflicts = []
        self.__attendee_conflicts = []
        self.__delta_time_slots = required_time_slots
    def __str__(self):
        return self.__name
    def getSubmissionName(self):
        return self.__name
    def setSubmissionName(self, name):
        self.__name = name
    def getSubmissionTrack(self):
        return self.__track
    def setSubmissionTrack(self, track):
        self.__track = track
    def getSubmissionRequiredTimeSlots(self):
        return self.__required_time_slots
    def setSubmissionRequiredTimeSlots(self, required_time_slots):
        self.__required_time_slots = required_time_slots
    def getSubmissionRelativeOrder(self):
        return self.__rel_order
    def setSubmissionRelativeOrder(self, rel_order):
        self.__rel_order = rel_order
    def getSubmissionActualOrder(self):
        return self.__act_order
    def setSubmissionActualOrder(self, act_order):
        self.__act_order = act_order
    def getSubmissionCanOpenSession(self):
        return self.__can_open_session
    def setSubmissionCanOpenSession(self, can_open_session):
        self.__can_open_session = can_open_session
    def getSubmissionCanCloseSession(self):
        return self.__can_close_session
    def setSubmissionCanCloseSession(self, can_close_session):
        self.__can_close_session = can_close_session
    def getSubmissionSameSession(self):
        return self.__same_session
    def setSubmissionSameSession(self, same_session):
        self.__same_session = same_session
    def getSubmissionDifferentSession(self):
        return self.__different_session
    def setSubmissionDifferentSession(self, different_session):
        self.__different_session = different_session
    def getSubmissionSpeakers(self):
        return self.__speakers
    def getSubmissionAttendees(self):
        return self.__attendees
    def getSubmissionSpeakerConflicts(self):
        return self.__speaker_conflicts
    def setSubmissionSpeakerConflicts(self, submission_name):
        if submission_name not in self.__speaker_conflicts:
            self.__speaker_conflicts.append(submission_name)
    def getSubmissionAttendeeConflicts(self):
        return self.__attendee_conflicts
    def setSubmissionAttendeeConflicts(self, submission_name):
        if submission_name not in self.__attendee_conflicts:
            self.__attendee_conflicts.append(submission_name)
    def subtractSubmissionTimeSlots(self, number):
        self.__delta_time_slots -= number
        if self.__delta_time_slots < 0:
            self.__delta_time_slots = 0
    def addSubmissionTimeSlots(self, number):
        self.__delta_time_slots += number
    def getSubmissionDeltaTimeSlots(self):
        return self.__delta_time_slots
    def resetSubmissionDeltaTimeSlots(self):
        self.__delta_time_slots = self.__required_time_slots