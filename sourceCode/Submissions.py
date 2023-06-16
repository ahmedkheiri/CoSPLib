# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:23:01 2023

@author: pylya
"""

class Submission():
    def __init__(self, name, track, required_time_slots, order, timezone, speakers, attendees):        
        self.__name = name
        self.__track = track
        self.__required_time_slots = required_time_slots
        self.__order = order
        self.__timezone = timezone
        self.__speakers = speakers
        self.__attendees = attendees
        self.__speaker_conflicts = []
        self.__attendee_conflicts = []
        self.__delta_time_slots = required_time_slots
    def getName(self):
        return self.__name
    def getTrack(self):
        return self.__track
    def getRequiredTimeSlots(self):
        return self.__required_time_slots
    def getOrder(self):
        return self.__order
    def getTimeZone(self):
        return self.__timezone
    def getSpeakers(self):
        return self.__speakers
    def getAttendees(self):
        return self.__attendees
    def setSpeakerConflicts(self, submission_name):
        if submission_name not in self.__speaker_conflicts:
            self.__speaker_conflicts.append(submission_name)
    def setAttendeeConflicts(self, submission_name):
        if submission_name not in self.__attendee_conflicts:
            self.__attendee_conflicts.append(submission_name)
    def getSpeakerConflicts(self):
        return self.__speaker_conflicts
    def getAttendeeConflicts(self):
        return self.__attendee_conflicts
    def subtractTimeSlots(self, number):
        self.__delta_time_slots -= number
        if self.__delta_time_slots < 0:
            self.__delta_time_slots = 0
    def addTimeSlots(self, number):
        self.__delta_time_slots += number
    def getDeltaTimeSlots(self):
        return self.__delta_time_slots
    def resetDeltaTimeSlots(self):
        self.__delta_time_slots = self.__required_time_slots
    def __str__(self):
        return self.__name