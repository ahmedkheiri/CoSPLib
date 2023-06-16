# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:26:06 2023

@author: pylya
"""

class Session():
    def __init__(self, name, max_time_slots, date, start_time, end_time):
        self.__name = name
        self.__max_time_slots = max_time_slots
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time
    def getName(self):
        return str(self.__name)
    def getMaxTimeSlots(self):
        return self.__max_time_slots
    def getDate(self):
        return self.__date
    def getStartTime(self):
        return self.__start_time
    def getEndTime(self):
        return self.__end_time
    def __str__(self):
        return self.__name