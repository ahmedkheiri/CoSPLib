# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:25:15 2023

@author: pylya
"""

class Track():
    def __init__(self, name, required_time_slots, order, organizers):
        self.__name = name
        self.__required_time_slots = required_time_slots
        self.__order = order
        self.__organizers = organizers
        self.__organizer_conflicts = []
        self.__submissions = []
        self.__delta_time_slots = required_time_slots
    def getName(self):
        return str(self.__name)
    def getRequiredTimeSlots(self):
        return self.__required_time_slots
    def getOrder(self):
        return self.__order
    def getOrganizers(self):
        return self.__organizers
    def setOrganizerConflicts(self, submission_name):
        if submission_name not in self.__organizer_conflicts:
            self.__organizer_conflicts.append(submission_name)
    def getOrganizerConflicts(self):
        return self.__organizer_conflicts
    def setSubmission(self, submission_name):
        self.__submissions.append(submission_name)
    def getSubmissions(self):
        return self.__submissions
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