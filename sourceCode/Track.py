# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:25:15 2023

@author: pylya
"""

class Track:
    def __init__(self, name, required_time_slots, rel_order, act_order, max_num_days, cost_extra_day, track_same_room, organisers):
        self.__name = name
        self.__required_time_slots = required_time_slots
        self.__rel_order = rel_order
        self.__act_order = act_order
        self.__max_num_days = max_num_days
        self.__cost_extra_day = cost_extra_day
        self.__track_same_room = track_same_room
        self.__organisers = organisers
        self.__organiser_conflicts = []
        self.__submissions = []
        self.__delta_time_slots = required_time_slots
    def __str__(self):
        return self.__name
    def getTrackName(self):
        return str(self.__name)
    def setTrackName(self, name):
        self.__name = name
    def getTrackRequiredTimeSlots(self):
        return self.__required_time_slots
    def setTrackRequiredTimeSlots(self, required_time_slots):
        self.__required_time_slots = required_time_slots
    def getTrackRelativeOrder(self):
        return self.__rel_order
    def setTrackRelativeOrder(self, rel_order):
        self.__rel_order = rel_order
    def getTrackActualOrder(self):
        return self.__act_order
    def setTrackActualOrder(self, act_order):
        self.__act_order = act_order
    def getTrackMaxNumOfDays(self):
        return self.__max_num_days
    def setTrackMaxNumOfDays(self, max_num_days):
        self.__max_num_days = max_num_days
    def getTrackCostExtraDay(self):
        return self.__cost_extra_day
    def setTrackCostExtraDay(self, cost_extra_day):
        self.__cost_extra_day = cost_extra_day
    def getTrackSameRoom(self):
        return self.__track_same_room
    def setTrackSameRoom(self, track_same_room):
        self.__track_same_room = track_same_room
    def getTrackOrganisers(self):
        return self.__organisers
    def setTrackOrganisers(self, organisers):
        self.__organisers = organisers
    def setTrackOrganiserConflicts(self, submission_name):
        if submission_name not in self.__organiser_conflicts:
            self.__organiser_conflicts.append(submission_name)
    def getTrackOrganiserConflicts(self):
        return self.__organizer_conflicts
    def setTrackSubmission(self, submission_name):
        self.__submissions.append(submission_name)
    def getTrackSubmissions(self):
        return self.__submissions
    def subtractTrackTimeSlots(self, number):
        self.__delta_time_slots -= number
        if self.__delta_time_slots < 0:
            self.__delta_time_slots = 0
    def addTrackTimeSlots(self, number):
        self.__delta_time_slots += number
    def getTrackDeltaTimeSlots(self):
        return self.__delta_time_slots
    def resetTrackDeltaTimeSlots(self):
        self.__delta_time_slots = self.__required_time_slots