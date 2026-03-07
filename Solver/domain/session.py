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

    def get_session_name(self) -> str:
        return self.__name

    def get_session_max_time_slots(self) -> int:
        return self.__max_time_slots

    def get_session_date(self) -> str:
        return self.__date

    def get_session_start_time(self) -> str:
        return self.__start_time

    def get_session_end_time(self) -> str:
        return self.__end_time

    def __str__(self):
        return "Session(" + self.__name + ")"
