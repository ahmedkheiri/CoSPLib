# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:26:06 2023

@author: pylya
"""
from datetime import datetime, date

class Session:
    def __init__(self, name, pref_num_time_slots, min_time_slots, max_time_slots, date, start_time, end_time):
        self.__name = name
        self.__pref_num_time_slots = pref_num_time_slots
        self.__min_time_slots = min_time_slots
        self.__max_time_slots = max_time_slots
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time
    
    def __str__(self):
        return "Session("+self.__name+")"
    def getSessionName(self):
        return str(self.__name)
    def setSessionName(self, name):
        self.__name = name
    def getSessionPrefNumOfTimeSlots(self):
        return self.__pref_num_time_slots
    def setSessionPrefNumOfTimeSlots(self, pref_num_time_slots):
        self.__pref_num_time_slots = pref_num_time_slots
    def getSessionMinTimeSlots(self):
        return self.__min_time_slots
    def setSessionMinTimeSlots(self, min_time_slots):
        self.__min_time_slots = min_time_slots
    def getSessionMaxTimeSlots(self):
        return self.__max_time_slots
    def setSessionMaxTimeSlots(self, max_time_slots):
        self.__max_time_slots = max_time_slots
    def getSessionDate(self):
        return self.__date
    def setSessionDate(self, date):
        self.__date = date
    def getSessionStartTime(self):
        return self.__start_time
    def setSessionStartTime(self, start_time):
        self.__start_time = start_time
    def getSessionEndTime(self):
        return self.__end_time
    def setSessionEndTime(self, end_time):
        self.__end_time = end_time
    
if __name__ == '__main__':
    s = Session("Mon1", 2, 0, 2, date(2021,7,28), datetime(2021, 7, 28, 9, 30), datetime(2021, 7, 28, 10, 30))
    print(s.getSessionDate())
    print(s.getSessionEndTime())
    print(s)
    
    