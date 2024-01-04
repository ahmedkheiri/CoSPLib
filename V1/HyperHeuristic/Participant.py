# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:27:57 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)

"""

class Participant:
    def __init__(self, ref, first_name, middle_name, last_name, email, affiliation, country, time_zone, in_person_status):
        self.__ref = ref
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__last_name = last_name
        self.__email = email
        self.__affiliation = affiliation
        self.__country = country
        self.__time_zone = time_zone
        self.__status = in_person_status
    def getParticipantID(self) -> str:
        return self.__ref
    def setParticipantID(self, ref):
        self.__ref = ref
    def getParticipantFirstName(self) -> str:
        return self.__first_name
    def setParticipantFirstName(self, first_name):
        self.__first_name = first_name
    def getParticipantMiddleName(self) -> str:
        return self.__middle_name
    def setParticipantMiddleName(self, middle_name):
        self.__middle_name = middle_name
    def getParticipantLastName(self) -> str:
        return self.__last_name
    def setParticipantLastName(self, last_name):
        self.__last_name = last_name
    def getParticipantEmail(self) -> str:
        return self.__email
    def setParticipantEmail(self, email):
        self.__email = email
    def getParticipantAffiliation(self) -> str:
        return self.__affiliation
    def setParticipantAffiliation(self, affiliation):
        self.__affiliation = affiliation
    def getParticipantCountry(self) -> str:
        return self.__country
    def setParticipantCountry(self, country):
        self.__country = country
    def getParticipantTimeZone(self) -> str:
        return self.__time_zone
    def setParticipantTimeZone(self, time_zone):
        self.__time_zone = time_zone
    def getParticipantInPersonStatus(self) -> bool:
        return self.__status
    def setParticipantInPersonStatus(self, in_person_status):
        self.__status = in_person_status
        
    def __str__(self):
        return "Participant("+self.__ref+")"
    
if __name__ == '__main__':
    par = Participant('P1', 'Yaro', '', 'Pyl', 'pyl@pyl.com', 'LU', 'UK', 'GMT+3', False)
    print(par.getParticipantTimeZone())
    par.setParticipantTimeZone('GMT+2')
    print(par.getParticipantTimeZone())
    print(par)