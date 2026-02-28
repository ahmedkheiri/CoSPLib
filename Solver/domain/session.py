# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""


class Session:
    def __init__(
        self, name: str, max_time_slots: int, date: str, start_time: str, end_time: str
    ) -> None:
        self.__name = name
        self.__max_time_slots = max_time_slots
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time

    def getSessionName(self) -> str:
        return self.__name

    def setSessionName(self, name: str) -> None:
        self.__name = name

    def getSessionMaxTimeSlots(self) -> int:
        return self.__max_time_slots

    def setSessionMaxTimeSlots(self, max_time_slots: int) -> None:
        self.__max_time_slots = max_time_slots

    def getSessionDate(self) -> str:
        return self.__date

    def setSessionDate(self, date: str) -> None:
        self.__date = date

    def getSessionStartTime(self) -> str:
        return self.__start_time

    def setSessionStartTime(self, start_time: str) -> None:
        self.__start_time = start_time

    def getSessionEndTime(self) -> str:
        return self.__end_time

    def setSessionEndTime(self, end_time: str) -> None:
        self.__end_time = end_time

    def __str__(self):
        return "Session(" + self.__name + ")"
