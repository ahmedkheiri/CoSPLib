# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""
from datetime import datetime, date

class Session:
    def __init__(self, name, max_time_slots, date, start_time, end_time):
        self.__name = name
        self.__max_time_slots = max_time_slots
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time
    def getSessionName(self) -> str:
        return self.__name
    def setSessionName(self, name):
        self.__name = name
    def getSessionMaxTimeSlots(self) -> int:
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
    def __str__(self):
        return "Session("+self.__name+")"   