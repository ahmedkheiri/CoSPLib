# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""


class Room:
    def __init__(self, name: str):
        self.__name = name

    def get_room_name(self) -> str:
        return self.__name

    def __str__(self):
        return "Room(" + self.__name + ")"
