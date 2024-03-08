# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:25:15 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)

"""

import Submission
class Track:
    def __init__(self, name, chairs, chairs_conflicts, submissions):
        self.__name = name
        self.__chairs = chairs
        self.__chairs_conflicts = chairs_conflicts
        self.__submissions = submissions
    def getTrackName(self) -> str:
        return self.__name
    def setTrackName(self, name):
        self.__name = name
    def getNumberOfTrackChairs(self) -> int:
        return len(self.__chairs)
    def getTrackChairs(self, chair_index):
        return self.__chairs[chair_index]
    def getTrackChairsList(self) -> list:
        return self.__chairs
    def setTrackChairs(self, chair):
        self.__chairs.append(chair)
    def setTrackChairsList(self, chairs_list):
        self.__chairs = chairs_list
    def getNumberOfTrackChairConflicts(self) -> int:
        return len(self.__chairs_conflicts)
    def getTrackChairConflicts(self, chair_conflict_index) -> 'Track':
        return self.__chairs_conflicts[chair_conflict_index]
    def getTrackChairConflictsList(self) -> list:
        return self.__chairs_conflicts
    def setTrackChairConflicts(self, track):
        if track not in self.__chairs_conflicts:
            self.__chairs_conflicts.append(track)
    def getNumberOfTrackSubmissions(self) -> int:
        return len(self.__submissions)
    def getTrackSubmissions(self, track_submissions_index) -> Submission:
        return self.__submissions[track_submissions_index]
    def getTrackSubmissionsList(self) -> list:
        return self.__submissions
    def setTrackSubmissions(self, submission):
        self.__submissions.append(submission)
    def getTrackRequiredTimeSlots(self):
        return self.__required_timeslots
    def setTrackRequiredTimeSlots(self, required_timeslots):
        self.__required_timeslots = required_timeslots     
    def __str__(self):
        return "Track("+self.__name+")"