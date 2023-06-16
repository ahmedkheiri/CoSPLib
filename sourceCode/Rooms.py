# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:25:42 2023

@author: pylya
"""

class Room():
    def __init__(self, name):
        self.__name = name
    def getName(self):
        return str(self.__name)
    def __str__(self):
        return self.__name