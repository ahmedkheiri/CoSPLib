# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:25:15 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)

"""

import Participant
import Submission
class Track:
    def __init__(self, name, rel_order, act_order, max_num_days, cost_extra_day
                 , track_same_room, track_same_building, organisers, organiser_conflicts, submissions):
        self.__name = name
        self.__rel_order = rel_order
        self.__act_order = act_order
        self.__max_num_days = max_num_days
        self.__cost_extra_day = cost_extra_day
        self.__track_same_room = track_same_room
        self.__track_same_building = track_same_building
        self.__organisers = organisers
        self.__organiser_conflicts = organiser_conflicts
        self.__submissions = submissions
    def getTrackName(self) -> str:
        return self.__name
    def setTrackName(self, name):
        self.__name = name
    def getTrackRelativeOrder(self) -> int:
        return self.__rel_order
    def setTrackRelativeOrder(self, rel_order):
        self.__rel_order = rel_order
    def getTrackActualOrder(self) -> int:
        return self.__act_order
    def setTrackActualOrder(self, act_order):
        self.__act_order = act_order
    def getTrackMaxNumOfDays(self) -> int:
        return self.__max_num_days
    def setTrackMaxNumOfDays(self, max_num_days):
        self.__max_num_days = max_num_days
    def getTrackCostExtraDay(self) -> int:
        return self.__cost_extra_day
    def setTrackCostExtraDay(self, cost_extra_day):
        self.__cost_extra_day = cost_extra_day
    def getNumberOfTrackSameRoom(self) -> int:
        return len(self.__track_same_room)
    def getTrackSameRoom(self, track_same_room_index) -> 'Track':
        return self.__track_same_room[track_same_room_index]
    def getTrackSameRoomList(self) -> list:
        return self.__track_same_room
    def setTrackSameRoom(self, track):
        self.__track_same_room.append(track)
    def setTrackSameRoomList(self, track_same_room_list):
        self.__track_same_room = track_same_room_list
    def getNumberOfTrackSameBuilding(self) -> int:
        return self.__track_same_building
    def getTrackSameBuilding(self, track_same_building_index) -> 'Track':
        return self.__track_same_building[track_same_building_index]
    def getTrackSameBuildingList(self) -> list:
        return self.__track_same_building
    def setTrackSameBuilding(self, track):
        self.__track_same_building.append(track)
    def setTrackSameBuildingList(self, track_same_building_list):
        self.__track_same_building = track_same_building_list
    def getNumberOfTrackOrganisers(self) -> int:
        return len(self.__organisers)
    def getTrackOrganisers(self, organiser_index) -> Participant:
        return self.__organisers[organiser_index]
    def getTrackOrganisersList(self) -> list:
        return self.__organisers
    def setTrackOrganisers(self, participant):
        self.__organisers.append(participant)
    def setTrackOrganisersList(self, organisers_list):
        self.__organisers = organisers_list
    def getNumberOfTrackOrganiserConflicts(self) -> int:
        return len(self.__organiser_conflicts)
    def getTrackOrganiserConflicts(self, organiser_conflict_index) -> 'Track':
        return self.__organiser_conflicts[organiser_conflict_index]
    def getTrackOrganiserConflictsList(self) -> list:
        return self.__organiser_conflicts
    def setTrackOrganiserConflicts(self, track):
        if track not in self.__organiser_conflicts:
            self.__organiser_conflicts.append(track)
    def getNumberOfTrackSubmissions(self) -> int:
        return len(self.__submissions)
    def getTrackSubmissions(self, track_submissions_index) -> Submission:
        return self.__submissions[track_submissions_index]
    def getTrackSubmissionsList(self) -> list:
        return self.__submissions
    def setTrackSubmissions(self, submission):
        self.__submissions.append(submission)
        
    def __str__(self):
        return "Track("+self.__name+")"
    
if __name__ == '__main__':
    track = Track('NewTrack', 0, 0, 0, 0, [], [], [], [], [])
    print(track.getTrackName())
    track.setTrackName('Track_1')
    print(track)