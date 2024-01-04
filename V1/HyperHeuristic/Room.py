# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:25:42 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)

"""

class Room:
    def __init__(self, name, building):
        self.__name = name
        self.__building = building
    def getRoomName(self) -> str:
        return self.__name
    def setRoomName(self, name):
        self.__name = name
    def getRoomBuilding(self) -> str:
        return self.__building
    def setRoomBuilding(self, building):
        self.__building = building

    def __str__(self):
        return "Room("+self.__name+")"
    
if __name__ == '__main__':
    r = Room("Room 1", "Floor 1")
    print(r.getRoomName())
    r.setRoomName("Room 2")
    print(r)