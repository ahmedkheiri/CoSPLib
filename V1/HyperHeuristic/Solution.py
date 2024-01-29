# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from Problem import *
from Parameters import *
import sys
import numpy as np
import pandas as pd

class Solution:
    def __init__(self, problem):    
        self.__problem = problem
        self.__solTracks = [[-1 for x in range(self.getProblem().getNumberOfRooms())] for y in range(self.getProblem().getNumberOfSessions())]
        self.__solSubmissions = [[[-1 for x in range(self.getProblem().getSession(z).getSessionMaxTimeSlots())] for y in range(self.getProblem().getNumberOfRooms())] for z in range(self.getProblem().getNumberOfSessions())]
        self.__indsolSubmissions = [[self.getProblem().getSubmissionIndex(x.getSubmissionName()) for x in self.getProblem().getTrack(y).getTrackSubmissionsList()] for y in range(self.getProblem().getNumberOfTracks())]
        self.generateEvaluations()
        
    def getProblem(self) -> Problem:
        return self.__problem
      
    def getSolTracks(self) -> list:
        return self.__solTracks
    
    def getSolSubmissions(self) -> list:
        return self.__solSubmissions
    
    def getIndSolSubmissions(self) -> list:
        return self.__indsolSubmissions
    
    def setIndSolSubmissions(self, solInd):
        self.__indsolSubmissions = solInd
    
    def setBestSolution(self, solTracks, solSubmissions):
        self.__solTracks = solTracks
        self.__solSubmissions = solSubmissions
        
    def restoreSolution(self, solTracks, solSubmissions, solInd):
        self.__solTracks = solTracks
        self.__solSubmissions = solSubmissions
        self.__indsolSubmissions = solInd
        
    def resetSolTracks(self):
        self.__solTracks = [[-1 for x in range(self.getProblem().getNumberOfRooms())] for y in range(self.getProblem().getNumberOfSessions())]
        
    def resetSolSubmissions(self):
        self.__solSubmissions = [[[-1 for x in range(self.getProblem().getSession(z).getSessionMaxTimeSlots())] for y in range(self.getProblem().getNumberOfRooms())] for z in range(self.getProblem().getNumberOfSessions())]
    
    def generateEvaluations(self):
        self.__evaluations = []
        self.__evaluations_names = {}
        if self.getProblem().getParameters().getTracksSessionsPenaltyWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getTracksSessionsPenaltyWeight() * self.EvaluateTracksSessions(), 'Tracks_Sessions|Penalty:')
        if self.getProblem().getParameters().getTracksRoomsPenaltyWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getTracksRoomsPenaltyWeight() * self.EvaluateTracksRooms(), 'Tracks_Rooms|Penalty:')
        if self.getProblem().getParameters().getSessionsRoomsPenaltyWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getSessionsRoomsPenaltyWeight() * self.EvaluateSessionsRooms(), 'Sessions_Rooms|Penalty')
        if self.getProblem().getParameters().getTracksTracksPenaltyWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getTracksTracksPenaltyWeight() * self.EvaluateTracksTracks(), 'Tracks_Tracks|Penalty:')
        if self.getProblem().getParameters().getNumOfRoomsPerTrackWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getNumOfRoomsPerTrackWeight() * self.EvaluateNumberOfRoomsPerTrack(), 'Number of rooms per track:')
        if self.getProblem().getParameters().getParallelTracksWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getParallelTracksWeight() * self.EvaluateParallelTracks(), 'Parallel tracks:')
        if self.getProblem().getParameters().getConsecutiveTracksWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getConsecutiveTracksWeight() * self.EvaluateConsecutiveTracks(), 'Consecutive tracks:')
        if self.getProblem().getParameters().getTracksRelativeOrderWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getTracksRelativeOrderWeight() * self.EvaluateTracksRelativeOrder(), 'Tracks relative order:')
        if self.getProblem().getParameters().getSubmissionsTimezonesWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getSubmissionsTimezonesWeight() * self.EvaluateSubmissionsTimezones(), 'Submissions timezones:')
        if self.getProblem().getParameters().getSubmissionsRelativeOrderWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getSubmissionsRelativeOrderWeight() * self.EvaluateSubmissionsRelativeOrder(), 'Submissions relative order:')
        if self.getProblem().getParameters().getSubmissionsActualOrderWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getSubmissionsActualOrderWeight() * self.EvaluateSubmissionsActualOrder(), 'Submissions actual order:')
        if self.getProblem().getParameters().getSubmissionsSessionsPenaltyWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getSubmissionsSessionsPenaltyWeight() * self.EvaluateSubmissionsSessions(), 'Submissions_Sessions|Penalty:')
        if self.getProblem().getParameters().getSubmissionsRoomsPenaltyWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getSubmissionsRoomsPenaltyWeight() * self.EvaluateSubmissionsRooms(), 'Submissions_Rooms|Penalty:')
        if self.getProblem().getParameters().getSpeakersConflictsWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getSpeakersConflictsWeight() * self.EvaluateSpeakersConflicts(), 'Speakers conflicts [Session Level]:')
        if self.getProblem().getParameters().getAteendeesConflictsWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getAteendeesConflictsWeight() * self.EvaluateAttendeesConflicts(), 'Attendees conflicts [Session Level]:')
        if self.getProblem().getParameters().getOrganisersConflictsWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getOrganisersConflictsWeight() * self.EvaluateOrganiserConflicts(), 'Organisers conflicts:')
        if self.getProblem().getParameters().getTracksBuildingsWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getTracksBuildingsWeight() * self.EvaluateTracksBuildings(), 'Tracks buildings:')
        if self.getProblem().getParameters().getBalanceWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getBalanceWeight() * self.EvaluateBalance(), 'Balance:')
        if self.getProblem().getParameters().getSpeakersConflictsTimeslotLevelWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getSpeakersConflictsTimeslotLevelWeight() * self.EvaluateSpeakersConflictsTS(), 'Speakers conflicts [Timeslot Level]:')
        if self.getProblem().getParameters().getAttendeesConflictsTimeSlotWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getAttendeesConflictsTimeSlotWeight() * self.EvaluateAttendeesConflictsTS(), 'Attendees conflicts [Timeslot Level]:')
        if self.getProblem().getParameters().getOpenSessionWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getOpenSessionWeight() * self.EvaluateCanSubmissionOpenSession(), 'Submissions open session:')
        if self.getProblem().getParameters().getCloseSessionWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getCloseSessionWeight() * self.EvaluateCanSubmissionCloseSession(), 'Submissions close session:')
        if self.getProblem().getParameters().getSameSessionWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getSameSessionWeight() * self.EvaluateSubmissionsSameSession(), 'Submissions same session:')
        if self.getProblem().getParameters().getDifferentSessionWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getDifferentSessionWeight() * self.EvaluateSubmissionsDifferentSession(), 'Submissions different session:')
        if self.getProblem().getParameters().getTrackMaxNumDaysWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getTrackMaxNumDaysWeight() * self.EvaluateTrackMaxNumberOfDays(), 'Track max number of days:')
        if self.getProblem().getParameters().getTrackSameRoomWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getTrackSameRoomWeight() * self.EvaluateTracksSameRoom(), 'Tracks same room:')
        if self.getProblem().getParameters().getTracksSameBuildingWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getTracksSameBuildingWeight() * self.EvaluateTracksSameBuilding(), 'Tracks same building:')
        if self.getProblem().getParameters().getPreferredNumTimeSlotsWeight() > 0:
            self.setEvaluation(lambda: self.getProblem().getParameters().getPreferredNumTimeSlotsWeight() * self.EvaluatePreferredNumberTS(), 'Preferred number of timeslots:')
        self.setEvaluation(lambda: self.EvaluateExtendedSubmissions(), 'Submissions with multiple timeslots in different sessions:')
        
    def setEvaluation(self, evaluation_function, evaluation_name):
        self.__evaluations.append(evaluation_function)
        self.__evaluations_names[evaluation_function] = evaluation_name
        
    def getEvaluationsList(self) -> list:
        return self.__evaluations
    
    def getEvaluationName(self, evaluation_function) -> str:
        return self.__evaluations_names[evaluation_function]
    
    def EvaluateTracksSessions(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().getTracksSessionsPenaltybyIndex(self.getSolTracks()[i][j], i)
        return pen
    
    def EvaluateTracksRooms(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().getTracksRoomsPenaltybyIndex(self.getSolTracks()[i][j], j)
        return pen
    
    def EvaluateSessionsRooms(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().getSessionsRoomsPenaltybyIndex(i, j)
        return pen
    
    def EvaluateTracksTracks(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(j, len(self.getSolTracks()[i])):
                    if (self.getSolTracks()[i][j] != self.getSolTracks()[i][x]) and (self.getSolTracks()[i][j] != -1) and (self.getSolTracks()[i][x] != -1):
                        pen += self.getProblem().getTracksTracksPenaltybyIndex(self.getSolTracks()[i][j], self.getSolTracks()[i][x])
        return pen
    
    def EvaluateNumberOfRoomsPerTrack(self) -> int:
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (j not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(j)
        for i in di.values():
            if len(i) > 1:
                pen += len(i) - 1
        return pen
    
    def EvaluateParallelTracks(self) -> int:
        pen = 0
        temp = [tuple(self.getSolTracks()[session]) for session in range(len(self.getSolTracks()))]
        for track in range(self.getProblem().getNumberOfTracks()):
            for session in range(len(temp)):
                c = temp[session].count(track)
                if c > 1:
                    pen += c - 1
        return pen
    
    def EvaluateConsecutiveTracks(self) -> int:
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (i not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(i)
        for i in di.values():
            if (len(i) > 1) and (sum(i) != sum(range(i[0], i[len(i) - 1] + 1))):
                pen += 1
        return pen
    
    def EvaluateTracksRelativeOrder(self) -> int:
        info = [(track, self.getProblem().getTrack(track).getTrackRelativeOrder()) for track in range(self.getProblem().getNumberOfTracks()) if self.getProblem().getTrack(track).getTrackRelativeOrder() != 0]
        sorted_info = sorted(info, key = lambda x: x[1])
        di = {}
        for i in sorted_info:
            di[i] = []
        pen = 0
        for track in di.keys():
            for session in range(len(self.getSolTracks())):
                if (track[0] in self.getSolTracks()[session]) and (session not in di[track]):
                    di[track].append(session)
        temp = list(di.values())
        for i in range(len(temp) - 1):
            for j in range(i + 1, len(temp)):
                for ii in temp[i]:
                    for jj in temp[j]:
                        if ii >= jj:
                            pen += 1
        return pen
    
    def EvaluateSubmissionsTimezones(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().getSubmissionsTimezonesPenaltybyIndex(self.getSolSubmissions()[i][j][x], i)
        return pen
    
    def EvaluateSubmissionsRelativeOrder(self) -> int:
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        di2 = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolSubmissions()[session][room])):
                        if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getSolSubmissions()[session][room][ts] not in di[self.getSolTracks()[session][room]]):
                            di[self.getSolTracks()[session][room]].append(self.getSolSubmissions()[session][room][ts])
                        if self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionRelativeOrder() != 0:
                            di2[session].append(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionRelativeOrder())
        for track in range(self.getProblem().getNumberOfTracks()):
            order = 1
            for sub in di[track]:
                if self.getProblem().getSubmission(sub).getSubmissionRelativeOrder() != 0:
                    if self.getProblem().getSubmission(sub).getSubmissionRelativeOrder() != order:
                        pen += 1
                        order += 1
                    else:
                        order += 1
        for session in range(self.getProblem().getNumberOfSessions()):
            if len(di2[session]) > self.getProblem().getSession(session).getSessionMaxTimeSlots():
                pen += len(di2[session]) - self.getProblem().getSession(session).getSessionMaxTimeSlots()
        return pen
    
    def EvaluateSubmissionsActualOrder(self) -> int:
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        di2 = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolSubmissions()[session][room])):
                        if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getSolSubmissions()[session][room][ts] not in di[self.getSolTracks()[session][room]]):
                            di[self.getSolTracks()[session][room]].append(self.getSolSubmissions()[session][room][ts])
                        if self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionActualOrder() != 0:
                            di2[session].append(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionActualOrder())
        for track in range(self.getProblem().getNumberOfTracks()):
            order = 1
            for sub in di[track]:
                if (self.getProblem().getSubmission(sub).getSubmissionActualOrder() != order) and (self.getProblem().getSubmission(sub).getSubmissionActualOrder() != 0):
                    pen += 1
                order += 1
        for session in range(self.getProblem().getNumberOfSessions()):
            if len(di2[session]) > self.getProblem().getSession(session).getSessionMaxTimeSlots():
                pen += len(di2[session]) - self.getProblem().getSession(session).getSessionMaxTimeSlots()
        return pen
    
    def EvaluateSubmissionsSessions(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().getSubmissionsSessionsPenaltybyIndex(self.getSolSubmissions()[i][j][x], i)
        return pen
    
    def EvaluateSubmissionsRooms(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().getSubmissionsRoomsPenaltybyIndex(self.getSolSubmissions()[i][j][x], j)
        return pen
    
    def EvaluateSpeakersConflicts(self) -> int: #Session Level
        pen = 0
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getSubmissionSpeakerConflictsList()) != 0) and ((self.getSolSubmissions()[i][j][x], j) not in di[i]):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getSubmission(di[i][j][0]) in self.getProblem().getSubmission(di[i][z][0]).getSubmissionSpeakerConflictsList()) and (di[i][j][1] != di[i][z][1]):
                            pen += 1
        return pen
    
    def EvaluateAttendeesConflicts(self) -> int: #Session Level
        pen = 0
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getSubmissionAttendeeConflictsList()) != 0) and ((self.getSolSubmissions()[i][j][x], j) not in di[i]):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getSubmission(di[i][j][0]) in self.getProblem().getSubmission(di[i][z][0]).getSubmissionAttendeeConflictsList()) and (di[i][j][1] != di[i][z][1]):
                            pen += 1
        return pen
    
    def EvaluateOrganiserConflicts(self) -> int:
        pen = 0
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (len(self.getProblem().getTrack(self.getSolTracks()[i][j]).getTrackOrganiserConflictsList()) != 0):
                    di[i].append(self.getSolTracks()[i][j])
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getTrack(di[i][j]) in self.getProblem().getTrack(di[i][z]).getTrackOrganiserConflictsList()):
                            pen += 1
        return pen
        
    def EvaluateTracksBuildings(self) -> int:
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] in di.keys()) and (self.getProblem().getRoom(j).getRoomBuilding() not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(self.getProblem().getRoom(j).getRoomBuilding())
        for track in di.values():
            pen += len(track) - 1
        return pen
    
    def EvaluateBalance(self) -> int:
        pen = 0
        for session in range(len(self.getSolSubmissions())):
            s = []
            for room in range(len(self.getSolSubmissions()[session])):
                s.append(self.getProblem().getSession(session).getSessionMaxTimeSlots() - self.getSolSubmissions()[session][room].count(-1))
            for i in s:
                pen += max(s) - i
        return pen
    
    def EvaluateSpeakersConflictsTS(self) -> int: #Time slot Level
        pen = 0
        di = {str(session)+str(ts):[] for session in range(self.getProblem().getNumberOfSessions()) for ts in range(self.getProblem().getSession(session).getSessionMaxTimeSlots())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionSpeakerConflictsList()) != 0) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)+str(ts)]):
                        di[str(session)+str(ts)].append(self.getSolSubmissions()[session][room][ts])
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session)+str(ts)]) > 1:
                    for j in range(len(di[str(session)+str(ts)])-1):
                        for z in range(j+1, len(di[str(session)+str(ts)])):
                            if (self.getProblem().getSubmission(di[str(session)+str(ts)][j]) in self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getSubmissionSpeakerConflictsList()):
                                pen += 1
        return pen
    
    def EvaluateAttendeesConflictsTS(self) -> int: #Time slot level
        pen = 0
        di = {str(session)+str(ts):[] for session in range(self.getProblem().getNumberOfSessions()) for ts in range(self.getProblem().getSession(session).getSessionMaxTimeSlots())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionAttendeeConflictsList()) != 0) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)+str(ts)]):
                        di[str(session)+str(ts)].append(self.getSolSubmissions()[session][room][ts])
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session)+str(ts)]) > 1:
                    for j in range(len(di[str(session)+str(ts)])-1):
                        for z in range(j+1, len(di[str(session)+str(ts)])):
                            if (self.getProblem().getSubmission(di[str(session)+str(ts)][j]) in self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getSubmissionAttendeeConflictsList()):
                                pen += 1
        return pen
    
    def EvaluateCanSubmissionOpenSession(self) -> int:
        pen = 0
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getProblem().getSubmission(self.getSolSubmissions()[session][room][0]).getSubmissionCanOpenSession() == False:
                    pen += 1
        return pen
    
    def EvaluateCanSubmissionCloseSession(self) -> int:
        pen = 0
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getProblem().getSubmission(self.getSolSubmissions()[session][room][len(self.getSolSubmissions()[session][room]) - 1]).getSubmissionCanCloseSession() == False:
                    pen += 1
        return pen
    
    def EvaluateSubmissionsSameSession(self) -> int:
        pen = 0
        di = {str(session): [] for session in range(self.getProblem().getNumberOfSessions())}
        subs = [x for x in range(self.getProblem().getNumberOfSubmissions()) if len(self.getProblem().getSubmission(x).getSubmissionSameSessionList()) > 0]
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)]):
                        di[str(session)].append(self.getSolSubmissions()[session][room][ts])
        for sub in subs:
            for session in range(len(self.getSolTracks())):
                if sub in di[str(session)]:
                    for x in range(len(self.getProblem().getSubmission(sub).getSubmissionSameSessionList())):
                        if self.getProblem().getSubmissionIndex(self.getProblem().getSubmission(sub).getSubmissionSameSession(x).getSubmissionName()) not in di[str(session)]:
                            pen += 1
        return pen
    
    def EvaluateSubmissionsDifferentSession(self) -> int:
        pen = 0
        di = {str(session): [] for session in range(self.getProblem().getNumberOfSessions())}
        subs = [x for x in range(self.getProblem().getNumberOfSubmissions()) if len(self.getProblem().getSubmission(x).getSubmissionDifferentSessionList()) > 0]
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)]):
                        di[str(session)].append(self.getSolSubmissions()[session][room][ts])
        for sub in subs:
            for session in range(len(self.getSolTracks())):
                if sub in di[str(session)]:
                    for x in range(len(self.getProblem().getSubmission(sub).getSubmissionDifferentSessionList())):
                        if self.getProblem().getSubmissionIndex(self.getProblem().getSubmission(sub).getSubmissionDifferentSession(x).getSubmissionName()) in di[str(session)]:
                            pen += 1
        return pen
    
    def EvaluateTrackMaxNumberOfDays(self) -> int:
        pen = 0
        tracks = [x for x in range(self.getProblem().getNumberOfTracks()) if self.getProblem().getTrack(x).getTrackMaxNumOfDays() != 0]
        di = {str(track): [] for track in tracks}
        for session in range(len(self.getSolTracks())):
            for track in tracks:
                if track in self.getSolTracks()[session]:
                    di[str(track)].append(self.getProblem().getSession(session).getSessionDate())
        for track in tracks:
            if max(di[str(track)]).day - min(di[str(track)]).day >= self.getProblem().getTrack(track).getTrackMaxNumOfDays():
                pen += (max(di[str(track)]).day - min(di[str(track)]).day) * self.getProblem().getTrack(track).getTrackCostExtraDay()
        return pen
    
    def EvaluateTracksSameRoom(self) -> int:
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        tracks = [track for track in range(self.getProblem().getNumberOfTracks()) if len(self.getProblem().getTrack(track).getTrackSameRoomList()) > 0]
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] in di.keys()) and (j+1 not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(j+1) #Adding one to j to eliminate room with index 0 issues when summing
        for track in tracks:
            for x in range(len(self.getProblem().getTrack(track).getTrackSameRoomList())):
                if sum(di[track]) != sum(di[self.getProblem().getTrackIndex(self.getProblem().getTrack(track).getTrackSameRoom(x).getTrackName())]):
                    pen += abs(sum(di[track]) - sum(di[self.getProblem().getTrackIndex(self.getProblem().getTrack(track).getTrackSameRoom(x).getTrackName())]))
        return pen
    
    def EvaluateTracksSameBuilding(self) -> int:
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        tracks = [track for track in range(self.getProblem().getNumberOfTracks()) if len(self.getProblem().getTrack(track).getTrackSameBuildingList()) > 0]
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] in di.keys()) and (self.getProblem().getRoom(j).getRoomBuilding() not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(self.getProblem().getRoom(j).getRoomBuilding())
        for track in tracks:
            for x in range(len(self.getProblem().getTrack(track).getTrackSameBuildingList())):
                temp1 = set(di[track])
                temp2 = set(di[self.getProblem().getTrackIndex(self.getProblem().getTrack(track).getTrackSameBuilding(x).getTrackName())])
                result = temp1.symmetric_difference(temp2)
                pen += len(result)
        return pen
    
    def EvaluatePreferredNumberTS(self) -> int:
        pen = 0
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getProblem().getSession(session).getSessionMaxTimeSlots() - self.getSolSubmissions()[session][room].count(-1) > self.getProblem().getSession(session).getSessionPrefNumOfTimeSlots():
                    pen += (self.getProblem().getSession(session).getSessionMaxTimeSlots() - self.getSolSubmissions()[session][room].count(-1)) - self.getProblem().getSession(session).getSessionPrefNumOfTimeSlots()
                if self.getProblem().getSession(session).getSessionMaxTimeSlots() - self.getSolSubmissions()[session][room].count(-1) < self.getProblem().getSession(session).getSessionMinTimeSlots():
                    pen += self.getProblem().getSession(session).getSessionMinTimeSlots() - (self.getProblem().getSession(session).getSessionMaxTimeSlots() - self.getSolSubmissions()[session][room].count(-1))
        return pen
    
    def EvaluateExtendedSubmissions(self) -> int:
        pen = 0
        di = {str(session)+str(room):[] for session in range(self.getProblem().getNumberOfSessions()) for room in range(self.getProblem().getNumberOfRooms())}
        di2 = {sub: [] for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() > 1}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionRequiredTimeSlots() > 1):
                        di[str(session)+str(room)].append(self.getSolSubmissions()[session][room][ts])
                        di2[self.getSolSubmissions()[session][room][ts]].append(ts)
        for i in di.values():
            if (len(i) != 0):
                temp = set(i)
                for j in temp:
                    if self.getProblem().getSubmission(j).getSubmissionRequiredTimeSlots() != i.count(j):
                        pen += 10000000
        for i in di2.values():
            if len(i) == 0:
                pen += 1000000000
                return pen
            if sum(range(i[0], i[len(i)-1] + 1)) != sum(i):
                pen += 1000000000
        return pen
    
    def EvaluateFeasibility(self) -> int:
        pen = 0
        temp = [self.getSolSubmissions()[session][room][ts] for session in range(len(self.getSolTracks())) for room in range(len(self.getSolTracks()[session])) for ts in range(len(self.getSolSubmissions()[session][room])) if self.getSolSubmissions()[session][room][ts] != -1]
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            if (sub not in temp) or (self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() != temp.count(sub)):
                pen += 1
        return pen
        
    
    def EvaluateAllSubmissionsScheduled(self) -> bool:
        temp = [self.getSolSubmissions()[session][room][ts] for session in range(len(self.getSolTracks())) for room in range(len(self.getSolTracks()[session])) for ts in range(len(self.getSolSubmissions()[session][room])) if self.getSolSubmissions()[session][room][ts] != -1]
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            if (sub not in temp) or (self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() != temp.count(sub)):
                return False
        return True
    
    def ValidateSolution(self) -> bool:
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolTracks()[i][j] != -1:
                        if self.getSolSubmissions()[i][j][x] != -1:
                            if self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]) not in self.getProblem().getTrack(self.getSolTracks()[i][j]).getTrackSubmissionsList():
                                return False
        return True
    
    def EvaluateSolution(self) -> int:
        obj = [self.getEvaluationsList()[i]() for i in range(len(self.getEvaluationsList()))]
        return sum(obj)
    
    def QuickEvaluateSolution(self, previous_obj) -> int:
        obj = 0
        for i in range(len(self.getEvaluationsList())):
            obj += self.getEvaluationsList()[i]()
            if obj > previous_obj:
                return obj
        return obj
    
    def copyWholeSolution(self):
        copy_solTracks = []
        copy_solSubmissions = []
        for i in range(len(self.getSolTracks())):
            temp = []
            temp3 = []
            for j in range(len(self.getSolTracks()[i])):
                temp.append(self.getSolTracks()[i][j])
                temp2 = []
                for z in range(len(self.getSolSubmissions()[i][j])):
                    temp2.append(self.getSolSubmissions()[i][j][z])
                temp3.append(temp2)
            copy_solTracks.append(temp)
            copy_solSubmissions.append(temp3)
        copy_indsol = []
        for i in range(len(self.getIndSolSubmissions())):
            temp = []
            for j in range(len(self.getIndSolSubmissions()[i])):
                temp.append(self.getIndSolSubmissions()[i][j])
            copy_indsol.append(temp)
        return copy_solTracks, copy_solSubmissions, copy_indsol
    
    def printViolations(self):
        print('----- Violations breakdown -----')
        for i in range(len(self.getEvaluationsList())):
            result = self.getEvaluationsList()[i]()
            if result > 0:
                print(self.getEvaluationName(self.getEvaluationsList()[i]), result)
        print('--------------------------------')
        
    def convertSolFirstTime(self):#Use with direct solution method
        subs_ts = {str(sub): 0 for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() == 1}
        index = {str(track): 0 for track in range(self.getProblem().getNumberOfTracks())}
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            if (self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() != 1) and (sub in self.getIndSolSubmissions()[self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName())]):
                self.getIndSolSubmissions()[self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName())].remove(sub)
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolSubmissions()[session][room])):
                        if (index[str(self.getSolTracks()[session][room])] <= len(self.getIndSolSubmissions()[self.getSolTracks()[session][room]]) - 1) and (self.getSolSubmissions()[session][room][ts] == -1):
                            self.getSolSubmissions()[session][room][ts] = self.getIndSolSubmissions()[self.getSolTracks()[session][room]][index[str(self.getSolTracks()[session][room])]]
                            subs_ts[str(self.getIndSolSubmissions()[self.getSolTracks()[session][room]][index[str(self.getSolTracks()[session][room])]])] += 1
                            if self.getProblem().getSubmission(self.getIndSolSubmissions()[self.getSolTracks()[session][room]][index[str(self.getSolTracks()[session][room])]]).getSubmissionRequiredTimeSlots() == subs_ts[str(self.getIndSolSubmissions()[self.getSolTracks()[session][room]][index[str(self.getSolTracks()[session][room])]])]:
                                index[str(self.getSolTracks()[session][room])] += 1
        '''
        #Creating Ind sol
        temp = [[] for i in range(self.getProblem().getNumberOfTracks())]
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    for x in range(len(self.getSolSubmissions()[i][j])):
                        temp[self.getSolTracks()[i][j]].append(self.getSolSubmissions()[i][j][x])
        self.setIndSolSubmissions(temp)
        '''
    def convertSol(self):#Use with indirect solution method
        temp = [self.getIndSolSubmissions()[track][sub] for track in range(len(self.getIndSolSubmissions())) for sub in range(len(self.getIndSolSubmissions()[track]))]
        for sub in temp:
            if self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() > 1:
                stop = False
                for session in range(self.getProblem().getNumberOfSessions()):
                    if stop == True:
                        break
                    for room in range(self.getProblem().getNumberOfRooms()):
                        if stop == True:
                            break
                        if (self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() <= self.getSolSubmissions()[session][room].count(-1)) and (self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName()) == self.getSolTracks()[session][room]):
                            for ts in range(self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots()):
                                i = self.getSolSubmissions()[session][room].index(-1)
                                self.getSolSubmissions()[session][room][i] = sub
                            stop = True
            else:
                stop = False
                for session in range(self.getProblem().getNumberOfSessions()):
                    if stop == True:
                        break
                    for room in range(self.getProblem().getNumberOfRooms()):
                        if stop == True:
                            break
                        if (self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() <= self.getSolSubmissions()[session][room].count(-1)) and (self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName()) == self.getSolTracks()[session][room]):
                            i = self.getSolSubmissions()[session][room].index(-1)
                            self.getSolSubmissions()[session][room][i] = sub
                            stop = True
        for session in range(self.getProblem().getNumberOfSessions()):
            for room in range(self.getProblem().getNumberOfRooms()):
                if self.getSolSubmissions()[session][room].count(-1) == len(self.getSolSubmissions()[session][room]):
                    self.getSolTracks()[session][room] = -1
    
    def toExcel(self, file_name = 'Solution.xlsx'):
        #Preparing sol tracks
        df = pd.DataFrame(self.getSolTracks(), 
                          index = [self.getProblem().getSession(s).getSessionName() for s in range(self.getProblem().getNumberOfSessions())],
                          columns = [self.getProblem().getRoom(r).getRoomName() for r in range(self.getProblem().getNumberOfRooms())])
        df = df.applymap(lambda x: self.getProblem().getTrack(x).getTrackName() if x != -1 else '')
        
        #Preparing sol submissions
        temp2 = []
        for session in range(self.getProblem().getNumberOfSessions()):
            for t in range(self.getProblem().getSession(session).getSessionMaxTimeSlots()):
                temp = []
                for room in range(self.getProblem().getNumberOfRooms()):
                    if self.getSolSubmissions()[session][room][t] != -1:
                        temp.append(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][t]).getSubmissionName())
                    else:
                        temp.append('')
                temp2.append(temp)
        df2 = pd.DataFrame(temp2, index = [self.getProblem().getSession(s).getSessionName() for s in range(self.getProblem().getNumberOfSessions()) for t in range(self.getProblem().getSession(s).getSessionMaxTimeSlots())])
        
        #Preparing objective
        obj = self.EvaluateSolution()
        obj_list = ['Obj', 'Final Objective = ' + str(obj)]
        df3 = pd.DataFrame(obj_list)
        
        #Preparing Tracks|Sessions penalty
        p1_list = ['Evaluate Tracks|Sessions']
        p1_pen = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    if self.getProblem().getTracksSessionsPenaltybyIndex(self.getSolTracks()[i][j], i) != 0:
                        p1_list.append(self.getProblem().getTrack(self.getSolTracks()[i][j]).getTrackName() + ' - ' + self.getProblem().getSession(i).getSessionName())
                        p1_pen.append(self.getProblem().getParameters().getTracksSessionsPenaltyWeight() * self.getProblem().getTracksSessionsPenaltybyIndex(self.getSolTracks()[i][j], i))
        p1_list.append('Total')
        p1_pen.append(sum(p1_pen))
        p1_pen.insert(0, '')
        df4 = pd.DataFrame(p1_list)
        df5 = pd.DataFrame(p1_pen)
        
        #Preparing Tracks|Rooms penalty
        p2_list = ['Evaluate Tracks|Rooms']
        p2_pen = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    if self.getProblem().getTracksRoomsPenaltybyIndex(self.getSolTracks()[i][j], j) != 0:
                        p2_list.append(self.getProblem().getTrack(self.getSolTracks()[i][j]).getTrackName() + ' - ' + self.getProblem().getRoom(j).getRoomName())
                        p2_pen.append(self.getProblem().getParameters().getTracksRoomsPenaltyWeight() * self.getProblem().getTracksRoomsPenaltybyIndex(self.getSolTracks()[i][j], j))
        p2_list.append('Total')
        p2_pen.append(sum(p2_pen))
        p2_pen.insert(0, '')
        df6 = pd.DataFrame(p2_list)
        df7 = pd.DataFrame(p2_pen)
        
        #Preparing Sessions|Rooms penalty
        p3_list = ['Evaluate Sessions|Rooms']
        p3_pen = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    if self.getProblem().getSessionsRoomsPenaltybyIndex(i, j) != 0:
                        p3_list.append(self.getProblem().getSession(i).getSessionName() + ' - ' + self.getProblem().getRoom(j).getRoomName())
                        p3_pen.append(self.getProblem().getParameters().getSessionsRoomsPenaltyWeight() * self.getProblem().getSessionsRoomsPenaltybyIndex(i, j))
        p3_list.append('Total')
        p3_pen.append(sum(p3_pen))
        p3_pen.insert(0, '')
        df8 = pd.DataFrame(p3_list)
        df9 = pd.DataFrame(p3_pen)
        
        #Preparing Tracks|Tracks penalty
        p4_list = ['Evaluate Tracks|Tracks']
        p4_pen = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(j, len(self.getSolTracks()[i])):
                    if (self.getSolTracks()[i][j] != self.getSolTracks()[i][x]) and (self.getSolTracks()[i][j] != -1) and (self.getSolTracks()[i][x] != -1):
                        if self.getProblem().getTracksTracksPenaltybyIndex(self.getSolTracks()[i][j], self.getSolTracks()[i][x]) != 0:
                            p4_list.append(self.getProblem().getTrack(self.getSolTracks()[i][j]).getTrackName() + ' - ' + self.getProblem().getTrack(self.getSolTracks()[i][x]).getTrackName() + ' - ' + self.getProblem().getSession(i).getSessionName())
                            p4_pen.append(self.getProblem().getParameters().getTracksTracksPenaltyWeight() * self.getProblem().getTracksTracksPenaltybyIndex(self.getSolTracks()[i][j], self.getSolTracks()[i][x]))
        p4_list.append('Total')
        p4_pen.append(sum(p4_pen))
        p4_pen.insert(0, '')
        df10 = pd.DataFrame(p4_list)
        df11 = pd.DataFrame(p4_pen)
        
        #Preparing Number of rooms per track
        p5_list = ['Evaluate NumberOfRoomsPerTrack']
        p5_pen = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (j not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(j)
        t = -1
        for i in di.values():
            t += 1
            if len(i) > 1:
                p5_list.append(self.getProblem().getTrack(t).getTrackName())
                p5_pen.append(self.getProblem().getParameters().getNumOfRoomsPerTrackWeight() * (len(i) - 1))
        p5_list.append('Total')
        p5_pen.append(sum(p5_pen))
        p5_pen.insert(0, '')
        df12 = pd.DataFrame(p5_list)
        df13 = pd.DataFrame(p5_pen)
        
        #Preparing Parallel tracks
        p6_list = ['Evaluate Parallel Tracks']
        p6_pen = []
        temp = [tuple(self.getSolTracks()[session]) for session in range(len(self.getSolTracks()))]
        for track in range(self.getProblem().getNumberOfTracks()):
            for session in range(len(temp)):
                c = temp[session].count(track)
                if c > 1:
                    p6_list.append(self.getProblem().getTrack(track).getTrackName() + ' - ' + self.getProblem().getSession(session).getSessionName())
                    p6_pen.append(self.getProblem().getParameters().getParallelTracksWeight() * (c - 1))
        p6_list.append('Total')
        p6_pen.append(sum(p6_pen))
        p6_pen.insert(0, '')
        df14 = pd.DataFrame(p6_list)
        df15 = pd.DataFrame(p6_pen)
        
        #Preparing Consecutive Tracks
        p7_list = ['Evaluate Consecutive Tracks']
        p7_pen = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (i not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(i)
        t = -1
        for i in di.values():
            t += 1
            if (len(i) > 1) and (sum(i) != sum(range(i[0], i[len(i) - 1] + 1))):
                p7_list.append(self.getProblem().getTrack(t).getTrackName())
                p7_pen.append(self.getProblem().getParameters().getConsecutiveTracksWeight())
        p7_list.append('Total')
        p7_pen.append(sum(p7_pen))
        p7_pen.insert(0, '')
        df16 = pd.DataFrame(p7_list)
        df17 = pd.DataFrame(p7_pen)
        
        #Preparing Tracks Order
        p8_list = ['Evaluate Tracks Relative Order']
        p8_pen = []
        info = [(track, self.getProblem().getTrack(track).getTrackRelativeOrder()) for track in range(self.getProblem().getNumberOfTracks()) if self.getProblem().getTrack(track).getTrackRelativeOrder() != 0]
        sorted_info = sorted(info, key = lambda x: x[1])
        di = {}
        for i in sorted_info:
            di[i] = []
        for track in di.keys():
            for session in range(len(self.getSolTracks())):
                if (track[0] in self.getSolTracks()[session]) and (session not in di[track]):
                    di[track].append(session)
        temp = list(di.values())
        t = -1
        for i in range(len(temp) - 1):
            t += 1
            for j in range(i + 1, len(temp)):
                for ii in temp[i]:
                    for jj in temp[j]:
                        if ii >= jj:
                            p8_list.append(self.getProblem().getTrack(sorted_info[t][0]).getTrackName())
                            p8_pen.append(self.getProblem().getParameters().getTracksRelativeOrderWeight())
        p8_list.append('Total')
        p8_pen.append(sum(p8_pen))
        p8_pen.insert(0, '')
        df18 = pd.DataFrame(p8_list)
        df19 = pd.DataFrame(p8_pen)
        
        #Preparing Submissions|Timezones penalty
        p9_list = ['Evaluate Submissions|Timezones']
        p9_pen = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        if self.getProblem().getSubmissionsTimezonesPenaltybyIndex(self.getSolSubmissions()[i][j][x], i) != 0:
                            p9_list.append(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getSubmissionName() + ' - ' + self.getProblem().getSession(i).getSessionName())
                            p9_pen.append(self.getProblem().getParameters().getSubmissionsTimezonesWeight() * self.getProblem().getSubmissionsTimezonesPenaltybyIndex(self.getSolSubmissions()[i][j][x], i))
        p9_list.append('Total')
        p9_pen.append(sum(p9_pen))
        p9_pen.insert(0, '')
        df20 = pd.DataFrame(p9_list)
        df21 = pd.DataFrame(p9_pen)
        
        #Preparing Submissions Relative Order
        p10_list = ['Evaluate Submissions Relative Order']
        p10_pen = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        di2 = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolSubmissions()[session][room])):
                        if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getSolSubmissions()[session][room][ts] not in di[self.getSolTracks()[session][room]]):
                            di[self.getSolTracks()[session][room]].append(self.getSolSubmissions()[session][room][ts])
                        if self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionRelativeOrder() != 0:
                            di2[session].append(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionRelativeOrder())
        for track in range(self.getProblem().getNumberOfTracks()):
            order = 1
            for sub in di[track]:
                if self.getProblem().getSubmission(sub).getSubmissionRelativeOrder() != 0:
                    if self.getProblem().getSubmission(sub).getSubmissionRelativeOrder() != order:
                        p10_list.append(self.getProblem().getSubmission(sub).getSubmissionName())
                        p10_pen.append(self.getProblem().getParameters().getSubmissionsRelativeOrderWeight())
                        order += 1
                    else:
                        order += 1
        for session in range(self.getProblem().getNumberOfSessions()):
            if len(di2[session]) > self.getProblem().getSession(session).getSessionMaxTimeSlots():
                p10_list.append('Parallel submissions in session ' + self.getProblem().getSession(session).getSessionName())
                p10_pen.append(self.getProblem().getParameters().getSubmissionsRelativeOrderWeight() * (len(di2[session]) - self.getProblem().getSession(session).getSessionMaxTimeSlots()))
        p10_list.append('Total')
        p10_pen.append(sum(p10_pen))
        p10_pen.insert(0, '')
        df22 = pd.DataFrame(p10_list)
        df23 = pd.DataFrame(p10_pen)
        
        #Preparing Submissions Actual Order
        p11_list = ['Evaluate Submissions Actual Order']
        p11_pen = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        di2 = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolSubmissions()[session][room])):
                        if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getSolSubmissions()[session][room][ts] not in di[self.getSolTracks()[session][room]]):
                            di[self.getSolTracks()[session][room]].append(self.getSolSubmissions()[session][room][ts])
                        if self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionActualOrder() != 0:
                            di2[session].append(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionActualOrder())
        for track in range(self.getProblem().getNumberOfTracks()):
            order = 1
            for sub in di[track]:
                if (self.getProblem().getSubmission(sub).getSubmissionActualOrder() != order) and (self.getProblem().getSubmission(sub).getSubmissionActualOrder() != 0):
                    p11_list.append(self.getProblem().getSubmission(sub).getSubmissionName())
                    p11_pen.append(self.getProblem().getParameters().getSubmissionsActualOrderWeight())
                order += 1
        for session in range(self.getProblem().getNumberOfSessions()):
            if len(di2[session]) > self.getProblem().getSession(session).getSessionMaxTimeSlots():
                p11_list.append('Parallel submissions in session ' + self.getProblem().getSession(session).getSessionName())
                p11_pen.append(self.getProblem().getParameters().getSubmissionsActualOrderWeight() * (len(di2[session]) - self.getProblem().getSession(session).getSessionMaxTimeSlots()))
        p11_list.append('Total')
        p11_pen.append(sum(p11_pen))
        p11_pen.insert(0, '')
        df24 = pd.DataFrame(p11_list)
        df25 = pd.DataFrame(p11_pen)
        
        #Preparing Submissions|Sessions penalty
        p12_list = ['Evaluate Submissions|Sessions']
        p12_pen = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        if self.getProblem().getSubmissionsSessionsPenaltybyIndex(self.getSolSubmissions()[i][j][x], i) != 0:
                            p12_list.append(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getSubmissionName() + ' - ' + self.getProblem().getSession(i).getSessionName())
                            p12_pen.append(self.getProblem().getParameters().getSubmissionsSessionsPenaltyWeight() * self.getProblem().getSubmissionsSessionsPenaltybyIndex(self.getSolSubmissions()[i][j][x], i))
        p12_list.append('Total')
        p12_pen.append(sum(p12_pen))
        p12_pen.insert(0, '')
        df26 = pd.DataFrame(p12_list)
        df27 = pd.DataFrame(p12_pen)
        
        #Preparing Submissions|Rooms penalty
        p13_list = ['Evaluate Submissions|Rooms']
        p13_pen = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        if self.getProblem().getSubmissionsRoomsPenaltybyIndex(self.getSolSubmissions()[i][j][x], j) != 0:
                            p13_list.append(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getSubmissionName() + ' - ' + self.getProblem().getRoom(j).getRoomName())
                            p13_pen.append(self.getProblem().getParameters().getSubmissionsRoomsPenaltyWeight() * self.getProblem().getSubmissionsRoomsPenaltybyIndex(self.getSolSubmissions()[i][j][x], j))
        p13_list.append('Total')
        p13_pen.append(sum(p13_pen))
        p13_pen.insert(0, '')
        df28 = pd.DataFrame(p13_list)
        df29 = pd.DataFrame(p13_pen)
        
        #Preparing Speakers Conflicts [S]
        p14_list = ['Evaluate Speakers Conflicts [S]']
        p14_pen = []
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getSubmissionSpeakerConflictsList()) != 0) and ((self.getSolSubmissions()[i][j][x], j) not in di[i]):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getSubmission(di[i][j][0]) in self.getProblem().getSubmission(di[i][z][0]).getSubmissionSpeakerConflictsList()) and (di[i][j][1] != di[i][z][1]):
                            p14_list.append(str(self.getProblem().getSubmission(di[i][j][0]).getSubmissionName()) + ' - ' + str(self.getProblem().getSubmission(di[i][z][0]).getSubmissionName()))
                            p14_pen.append(self.getProblem().getParameters().getSpeakersConflictsWeight())
        p14_list.append('Total')
        p14_pen.append(sum(p14_pen))
        p14_pen.insert(0, '')
        df30 = pd.DataFrame(p14_list)
        df31 = pd.DataFrame(p14_pen)
        
        #Preparing Attendees Conflicts [S]
        p15_list = ['Evaluate Attendees Conflicts [S]']
        p15_pen = []
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getSubmissionAttendeeConflictsList()) != 0) and ((self.getSolSubmissions()[i][j][x], j) not in di[i]):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getSubmission(di[i][j][0]) in self.getProblem().getSubmission(di[i][z][0]).getSubmissionAttendeeConflictsList()) and (di[i][j][1] != di[i][z][1]):
                            p15_list.append(self.getProblem().getSubmission(di[i][j][0]).getSubmissionName() + ' - ' + self.getProblem().getSubmission(di[i][z][0]).getSubmissionName())
                            p15_pen.append(self.getProblem().getParameters().getAteendeesConflictsWeight())
        p15_list.append('Total')
        p15_pen.append(sum(p15_pen))
        p15_pen.insert(0, '')
        df32 = pd.DataFrame(p15_list)
        df33 = pd.DataFrame(p15_pen)
        
        #Preparing Organisers Conflicts
        p16_list = ['Evaluate Organisers Conflicts']
        p16_pen = []
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (len(self.getProblem().getTrack(self.getSolTracks()[i][j]).getTrackOrganiserConflictsList()) != 0):
                    di[i].append(self.getSolTracks()[i][j])
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getTrack(di[i][j]) in self.getProblem().getTrack(di[i][z]).getTrackOrganiserConflictsList()):
                            p16_list.append(self.getProblem().getTrack(di[i][j]).getTrackName() + ' - ' + self.getProblem().getTrack(di[i][z]).getTrackName())
                            p16_pen.append(self.getProblem().getParameters().getOrganisersConflictsWeight())
        p16_list.append('Total')
        p16_pen.append(sum(p16_pen))
        p16_pen.insert(0, '')
        df34 = pd.DataFrame(p16_list)
        df35 = pd.DataFrame(p16_pen)
        '''
        #Preparing Tracks Buildings
        p17_list = ['Evaluate Tracks Buildings']
        p17_pen = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] in di.keys()) and (self.getProblem().getRoom(j).getRoomBuilding() not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(self.getProblem().getRoom(j).getRoomBuilding())
        for track in di.values():
            pen += len(track) - 1
        p17_list.append('Total')
        p17_pen.append(sum(p17_pen))
        p17_pen.insert(0, '')
        df36 = pd.DataFrame(p17_list)
        df37 = pd.DataFrame(p17_pen)
        '''
        #Preparing Balance
        p18_list = ['Evaluate Balance']
        p18_pen = []
        for session in range(len(self.getSolSubmissions())):
            s = []
            pen = 0
            for room in range(len(self.getSolSubmissions()[session])):
                s.append(self.getProblem().getSession(session).getSessionMaxTimeSlots() - self.getSolSubmissions()[session][room].count(-1))
            for i in s:
                pen += self.getProblem().getParameters().getBalanceWeight() * (max(s) - i)
            if pen != 0:
                p18_list.append(self.getProblem().getSession(session).getSessionName())
                p18_pen.append(pen)
        p18_list.append('Total')
        p18_pen.append(sum(p18_pen))
        p18_pen.insert(0, '')
        df38 = pd.DataFrame(p18_list)
        df39 = pd.DataFrame(p18_pen)
        
        #Preparing Speakers Conflicts [TS]
        p19_list = ['Evaluate Speakers Conflicts [TS]']
        p19_pen = []
        di = {str(session)+str(ts):[] for session in range(self.getProblem().getNumberOfSessions()) for ts in range(self.getProblem().getSession(session).getSessionMaxTimeSlots())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionSpeakerConflictsList()) != 0) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)+str(ts)]):
                        di[str(session)+str(ts)].append(self.getSolSubmissions()[session][room][ts])
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session)+str(ts)]) > 1:
                    for j in range(len(di[str(session)+str(ts)])-1):
                        for z in range(j+1, len(di[str(session)+str(ts)])):
                            if (self.getProblem().getSubmission(di[str(session)+str(ts)][j]) in self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getSubmissionSpeakerConflictsList()):
                                p19_list.append(str(self.getProblem().getSubmission(di[str(session)+str(ts)][j]).getSubmissionName()) + ' - ' + str(self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getSubmissionName()))
                                p19_pen.append(self.getProblem().getParameters().getSpeakersConflictsTimeslotLevelWeight())
        p19_list.append('Total')
        p19_pen.append(sum(p19_pen))
        p19_pen.insert(0, '')
        df40 = pd.DataFrame(p19_list)
        df41 = pd.DataFrame(p19_pen)
        
        #Preparing Attendees Conflicts[TS]
        p20_list = ['Evaluate Attendees Conflicts [TS]']
        p20_pen = []
        di = {str(session)+str(ts):[] for session in range(self.getProblem().getNumberOfSessions()) for ts in range(self.getProblem().getSession(session).getSessionMaxTimeSlots())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSubmissionAttendeeConflictsList()) != 0) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)+str(ts)]):
                        di[str(session)+str(ts)].append(self.getSolSubmissions()[session][room][ts])
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session)+str(ts)]) > 1:
                    for j in range(len(di[str(session)+str(ts)])-1):
                        for z in range(j+1, len(di[str(session)+str(ts)])):
                            if (self.getProblem().getSubmission(di[str(session)+str(ts)][j]) in self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getSubmissionAttendeeConflictsList()):
                                p20_list.append(self.getProblem().getSubmission(di[str(session)+str(ts)][j]).getSubmissionName() + ' - ' + self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getSubmissionName())
                                p20_pen.append(self.getProblem().getParameters().getAttendeesConflictsTimeSlotWeight())
        p20_list.append('Total')
        p20_pen.append(sum(p20_pen))
        p20_pen.insert(0, '')
        df42 = pd.DataFrame(p20_list)
        df43 = pd.DataFrame(p20_pen)
        
        #Preparing Submission Can Open Session
        p21_list = ['Evaluate Submission Can Open Session']
        p21_pen = []
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getProblem().getSubmission(self.getSolSubmissions()[session][room][0]).getSubmissionCanOpenSession() == False:
                    p21_list.append(self.getProblem().getSession(session).getSessionName() + ' - ' + self.getProblem().getSubmission(self.getSolSubmissions()[session][room][0]).getSubmissionName())
                    p21_pen.append(self.getProblem().getParameters().getOpenSessionWeight())
        p21_list.append('Total')
        p21_pen.append(sum(p21_pen))
        p21_pen.insert(0, '')
        df44 = pd.DataFrame(p21_list)
        df45 = pd.DataFrame(p21_pen)
        
        #Preparing Submission Can Close Session
        p22_list = ['Evaluate Submission Can Close Session']
        p22_pen = []
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getProblem().getSubmission(self.getSolSubmissions()[session][room][len(self.getSolSubmissions()[session][room]) - 1]).getSubmissionCanCloseSession() == False:
                    p22_list.append(self.getProblem().getSession(session).getSessionName() + ' - ' + self.getProblem().getSubmission(self.getSolSubmissions()[session][room][len(self.getSolSubmissions()[session][room]) - 1]).getSubmissionName())
                    p22_pen.append(self.getProblem().getParameters().getCloseSessionWeight())
        p22_list.append('Total')
        p22_pen.append(sum(p22_pen))
        p22_pen.insert(0, '')
        df46 = pd.DataFrame(p22_list)
        df47 = pd.DataFrame(p22_pen)
        
        #Preparing Submissions Same Session
        p23_list = ['Evaluate Submissions Same Session']
        p23_pen = []
        di = {str(session): [] for session in range(self.getProblem().getNumberOfSessions())}
        subs = [x for x in range(self.getProblem().getNumberOfSubmissions()) if len(self.getProblem().getSubmission(x).getSubmissionSameSessionList()) > 0]
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)]):
                        di[str(session)].append(self.getSolSubmissions()[session][room][ts])
        for sub in subs:
            for session in range(len(self.getSolTracks())):
                if sub in di[str(session)]:
                    for x in range(len(self.getProblem().getSubmission(sub).getSubmissionSameSessionList())):
                        if self.getProblem().getSubmissionIndex(self.getProblem().getSubmission(sub).getSubmissionSameSession(x).getSubmissionName()) not in di[str(session)]:
                            p23_list.append(self.getProblem().getSubmission(sub).getSubmissionName() + ' - ' + self.getProblem().getSubmission(sub).getSubmissionSameSession(x).getSubmissionName())
                            p23_pen.append(self.getProblem().getParameters().getSameSessionWeight())
        p23_list.append('Total')
        p23_pen.append(sum(p23_pen))
        p23_pen.insert(0, '')
        df48 = pd.DataFrame(p23_list)
        df49 = pd.DataFrame(p23_pen)
        
        #Preparing Submissions Different Session
        p24_list = ['Evaluate Submissions Different Session']
        p24_pen = []
        di = {str(session): [] for session in range(self.getProblem().getNumberOfSessions())}
        subs = [x for x in range(self.getProblem().getNumberOfSubmissions()) if len(self.getProblem().getSubmission(x).getSubmissionDifferentSessionList()) > 0]
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)]):
                        di[str(session)].append(self.getSolSubmissions()[session][room][ts])
        for sub in subs:
            for session in range(len(self.getSolTracks())):
                if sub in di[str(session)]:
                    for x in range(len(self.getProblem().getSubmission(sub).getSubmissionDifferentSessionList())):
                        if self.getProblem().getSubmissionIndex(self.getProblem().getSubmission(sub).getSubmissionDifferentSession(x).getSubmissionName()) in di[str(session)]:
                            p24_list.append(self.getProblem().getSubmission(sub).getSubmissionName() + ' - ' + self.getProblem().getSubmission(sub).getSubmissionDifferentSession(x).getSubmissionName())
                            p24_pen.append(self.getProblem().getParameters().getDifferentSessionWeight())
        p24_list.append('Total')
        p24_pen.append(sum(p24_pen))
        p24_pen.insert(0, '')
        df50 = pd.DataFrame(p24_list)
        df51 = pd.DataFrame(p24_pen)
        
        #Preparing Track Max Number Of Days
        p25_list = ['Evaluate Track Max Number Of Days']
        p25_pen = []
        tracks = [x for x in range(self.getProblem().getNumberOfTracks()) if self.getProblem().getTrack(x).getTrackMaxNumOfDays() != 0]
        di = {str(track): [] for track in tracks}
        for session in range(len(self.getSolTracks())):
            for track in tracks:
                if track in self.getSolTracks()[session]:
                    di[str(track)].append(self.getProblem().getSession(session).getSessionDate())
        for track in tracks:
            if max(di[str(track)]).day - min(di[str(track)]).day >= self.getProblem().getTrack(track).getTrackMaxNumOfDays():
                p25_list.append(self.getProblem().getTrack(track).getTrackName())
                p25_pen.append(self.getProblem().getParameters().getTrackMaxNumDaysWeight() * ((max(di[str(track)]).day - min(di[str(track)]).day) * self.getProblem().getTrack(track).getTrackCostExtraDay()))
        p25_list.append('Total')
        p25_pen.append(sum(p25_pen))
        p25_pen.insert(0, '')
        df52 = pd.DataFrame(p25_list)
        df53 = pd.DataFrame(p25_pen)
        
        #Preparing Tracks Same Room
        p26_list = ['Evaluate Tracks Same Room']
        p26_pen = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        tracks = [track for track in range(self.getProblem().getNumberOfTracks()) if len(self.getProblem().getTrack(track).getTrackSameRoomList()) > 0]
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] in di.keys()) and (j+1 not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(j+1) #Adding one to j to eliminate room with index 0 issues when summing
        for track in tracks:
            for x in range(len(self.getProblem().getTrack(track).getTrackSameRoomList())):
                if sum(di[track]) != sum(di[self.getProblem().getTrackIndex(self.getProblem().getTrack(track).getTrackSameRoom(x).getTrackName())]):
                    p26_list.append(self.getProblem().getTrack(track).getTrackName() + ' - ' + self.getProblem().getTrack(track).getTrackSameRoom(x).getTrackName())
                    p26_pen.append(self.getProblem().getParameters().getTrackSameRoomWeight() * abs(sum(di[track]) - sum(di[self.getProblem().getTrackIndex(self.getProblem().getTrack(track).getTrackSameRoom(x).getTrackName())])))
        p26_list.append('Total')
        p26_pen.append(sum(p26_pen))
        p26_pen.insert(0, '')
        df54 = pd.DataFrame(p26_list)
        df55 = pd.DataFrame(p26_pen)
        '''
        #Preparing Tracks Same Building
        p27_list = ['Evaluate Tracks Same Building']
        p27_pen = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        tracks = [track for track in range(self.getProblem().getNumberOfTracks()) if len(self.getProblem().getTrack(track).getTrackSameBuildingList()) > 0]
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] in di.keys()) and (self.getProblem().getRoom(j).getRoomBuilding() not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(self.getProblem().getRoom(j).getRoomBuilding())
        for track in tracks:
            for x in range(len(self.getProblem().getTrack(track).getTrackSameBuildingList())):
                temp1 = set(di[track])
                temp2 = set(di[self.getProblem().getTrackIndex(self.getProblem().getTrack(track).getTrackSameBuilding(x).getTrackName())])
                result = temp1.symmetric_difference(temp2)
                pen += len(result)
        p27_list.append('Total')
        p27_pen.append(sum(p27_pen))
        p27_pen.insert(0, '')
        df56 = pd.DataFrame(p27_list)
        df57 = pd.DataFrame(p27_pen)
        '''
        #Preparing Preferred Number of Timeslots
        p28_list = ['Evaluate Preferred Number of Timeslots']
        p28_pen = []
        for session in range(len(self.getSolTracks())):
            pen = 0
            for room in range(len(self.getSolTracks()[session])):
                if self.getProblem().getSession(session).getSessionMaxTimeSlots() - self.getSolSubmissions()[session][room].count(-1) > self.getProblem().getSession(session).getSessionPrefNumOfTimeSlots():
                    pen += self.getProblem().getParameters().getPreferredNumTimeSlotsWeight() * ((self.getProblem().getSession(session).getSessionMaxTimeSlots() - self.getSolSubmissions()[session][room].count(-1)) - self.getProblem().getSession(session).getSessionPrefNumOfTimeSlots())
                if self.getProblem().getSession(session).getSessionMaxTimeSlots() - self.getSolSubmissions()[session][room].count(-1) < self.getProblem().getSession(session).getSessionMinTimeSlots():
                    pen += self.getProblem().getParameters().getPreferredNumTimeSlotsWeight() * (self.getProblem().getSession(session).getSessionMinTimeSlots() - (self.getProblem().getSession(session).getSessionMaxTimeSlots() - self.getSolSubmissions()[session][room].count(-1)))
            if pen != 0:
                p28_list.append(self.getProblem().getSession(session).getSessionName())
                p28_pen.append(pen)
        p28_list.append('Total')
        p28_pen.append(sum(p28_pen))
        p28_pen.insert(0, '')
        df58 = pd.DataFrame(p28_list)
        df59 = pd.DataFrame(p28_pen)
             
        #Writing to excel file
        with pd.ExcelWriter(file_name) as writer:
            #Sol tracks
            df.to_excel(writer, sheet_name = 'sol')
            #Sol submissions
            df2.to_excel(writer, sheet_name = 'sol', startrow = self.getProblem().getNumberOfSessions() + 2, header = False)
            #Objective
            df3.to_excel(writer, sheet_name = 'violations', index = False, header = False)
            #Tracks|Sessions
            df4.to_excel(writer, sheet_name = 'violations', startcol = 1,index = False, header = False)
            df5.to_excel(writer, sheet_name = 'violations', startcol = 2,index = False, header = False)
            #Tracks|Rooms
            df6.to_excel(writer, sheet_name = 'violations', startcol = 3,index = False, header = False)
            df7.to_excel(writer, sheet_name = 'violations', startcol = 4,index = False, header = False)
            #Sessions|Rooms
            df8.to_excel(writer, sheet_name = 'violations', startcol = 5,index = False, header = False)
            df9.to_excel(writer, sheet_name = 'violations', startcol = 6,index = False, header = False)
            #Tracks|Tracks
            df10.to_excel(writer, sheet_name = 'violations', startcol = 7,index = False, header = False)
            df11.to_excel(writer, sheet_name = 'violations', startcol = 8,index = False, header = False)
            #NumberOfRoomsPerTrack
            df12.to_excel(writer, sheet_name = 'violations', startcol = 9,index = False, header = False)
            df13.to_excel(writer, sheet_name = 'violations', startcol = 10,index = False, header = False)
            #Parallel Tracks
            df14.to_excel(writer, sheet_name = 'violations', startcol = 11,index = False, header = False)
            df15.to_excel(writer, sheet_name = 'violations', startcol = 12,index = False, header = False)
            #Consecutive Tracks
            df16.to_excel(writer, sheet_name = 'violations', startcol = 13,index = False, header = False)
            df17.to_excel(writer, sheet_name = 'violations', startcol = 14,index = False, header = False)
            #Tracks Relative Order
            df18.to_excel(writer, sheet_name = 'violations', startcol = 15,index = False, header = False)
            df19.to_excel(writer, sheet_name = 'violations', startcol = 16,index = False, header = False)
            #Submissions|Timezones
            df20.to_excel(writer, sheet_name = 'violations', startcol = 17,index = False, header = False)
            df21.to_excel(writer, sheet_name = 'violations', startcol = 18,index = False, header = False)
            #Submissions Relative Order
            df22.to_excel(writer, sheet_name = 'violations', startcol = 19,index = False, header = False)
            df23.to_excel(writer, sheet_name = 'violations', startcol = 20,index = False, header = False)
            #Submissions Actual Order
            df24.to_excel(writer, sheet_name = 'violations', startcol = 21,index = False, header = False)
            df25.to_excel(writer, sheet_name = 'violations', startcol = 22,index = False, header = False)
            #Submissions|Sessions
            df26.to_excel(writer, sheet_name = 'violations', startcol = 23,index = False, header = False)
            df27.to_excel(writer, sheet_name = 'violations', startcol = 24,index = False, header = False)
            #Submissions|Rooms
            df28.to_excel(writer, sheet_name = 'violations', startcol = 25,index = False, header = False)
            df29.to_excel(writer, sheet_name = 'violations', startcol = 26,index = False, header = False)
            #Speakers Conflicts [S]
            df30.to_excel(writer, sheet_name = 'violations', startcol = 27,index = False, header = False)
            df31.to_excel(writer, sheet_name = 'violations', startcol = 28,index = False, header = False)
            #Attendees Conflicts [S]
            df32.to_excel(writer, sheet_name = 'violations', startcol = 29,index = False, header = False)
            df33.to_excel(writer, sheet_name = 'violations', startcol = 30,index = False, header = False)
            #Organisers Conflicts
            df34.to_excel(writer, sheet_name = 'violations', startcol = 31,index = False, header = False)
            df35.to_excel(writer, sheet_name = 'violations', startcol = 32,index = False, header = False)
            #Tracks Buildings
            #df36.to_excel(writer, sheet_name = 'violations', startcol = 33,index = False, header = False)
            #df37.to_excel(writer, sheet_name = 'violations', startcol = 34,index = False, header = False)
            #Balance
            df38.to_excel(writer, sheet_name = 'violations', startcol = 35,index = False, header = False)
            df39.to_excel(writer, sheet_name = 'violations', startcol = 36,index = False, header = False)
            #Speakers Conflicts [TS]
            df40.to_excel(writer, sheet_name = 'violations', startcol = 37,index = False, header = False)
            df41.to_excel(writer, sheet_name = 'violations', startcol = 38,index = False, header = False)
            #Attendees Conflicts [TS]
            df42.to_excel(writer, sheet_name = 'violations', startcol = 39,index = False, header = False)
            df43.to_excel(writer, sheet_name = 'violations', startcol = 40,index = False, header = False)
            #Open Session
            df44.to_excel(writer, sheet_name = 'violations', startcol = 41,index = False, header = False)
            df45.to_excel(writer, sheet_name = 'violations', startcol = 42,index = False, header = False)
            #Close Session
            df46.to_excel(writer, sheet_name = 'violations', startcol = 43,index = False, header = False)
            df47.to_excel(writer, sheet_name = 'violations', startcol = 44,index = False, header = False)
            #Same Session
            df48.to_excel(writer, sheet_name = 'violations', startcol = 45,index = False, header = False)
            df49.to_excel(writer, sheet_name = 'violations', startcol = 46,index = False, header = False)
            #Different Session
            df50.to_excel(writer, sheet_name = 'violations', startcol = 47,index = False, header = False)
            df51.to_excel(writer, sheet_name = 'violations', startcol = 48,index = False, header = False)
            #Track Max Number of Days
            df52.to_excel(writer, sheet_name = 'violations', startcol = 49,index = False, header = False)
            df53.to_excel(writer, sheet_name = 'violations', startcol = 50,index = False, header = False)
            #Tracks Same Room
            df54.to_excel(writer, sheet_name = 'violations', startcol = 51,index = False, header = False)
            df55.to_excel(writer, sheet_name = 'violations', startcol = 52,index = False, header = False)
            #Tracks Same Building
            #df56.to_excel(writer, sheet_name = 'violations', startcol = 53,index = False, header = False)
            #df57.to_excel(writer, sheet_name = 'violations', startcol = 54,index = False, header = False)
            #Preferred Number of Timeslots
            df58.to_excel(writer, sheet_name = 'violations', startcol = 55,index = False, header = False)
            df59.to_excel(writer, sheet_name = 'violations', startcol = 56,index = False, header = False)
    '''
    ReadSolution
    '''
    
class InitialSolution(Solution):
    def __init__(self, problem):
        Solution.__init__(self, problem)
    
class Random(InitialSolution):
    def __init__(self, problem):
        InitialSolution.__init__(self, problem)
        temp = [sub for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() > 1]
        temp2 = [sub for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() == 1]
        sessions = [session for session in range(self.getProblem().getNumberOfSessions())]
        rooms = [room for room in range(self.getProblem().getNumberOfRooms())]
        np.random.shuffle(sessions)
        np.random.shuffle(rooms)
        done = False
        while done == False:
            np.random.shuffle(temp)
            for sub in temp:
                stop = False
                for session in sessions:
                    if stop == True:
                        break
                    for room in rooms:
                        if stop == True:
                            break
                        if ((self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() <= self.getSolSubmissions()[session][room].count(-1)) and (self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName()) == self.getSolTracks()[session][room])) or ((self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() <= self.getSolSubmissions()[session][room].count(-1)) and (self.getSolTracks()[session][room] == -1)):
                            for ts in range(self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots()):
                                i = self.getSolSubmissions()[session][room].index(-1)
                                self.getSolSubmissions()[session][room][i] = sub
                            stop = True
                            self.getSolTracks()[session][room] = self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName())
            np.random.shuffle(sessions)
            np.random.shuffle(rooms)
            np.random.shuffle(temp2)
            for sub in temp2:
                stop = False
                for session in sessions:
                    if stop == True:
                        break
                    for room in rooms:
                        if stop == True:
                            break
                        if ((self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() <= self.getSolSubmissions()[session][room].count(-1)) and (self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName()) == self.getSolTracks()[session][room])) or ((self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() <= self.getSolSubmissions()[session][room].count(-1)) and (self.getSolTracks()[session][room] == -1)):
                            i = self.getSolSubmissions()[session][room].index(-1)
                            self.getSolSubmissions()[session][room][i] = sub
                            stop = True
                            self.getSolTracks()[session][room] = self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName())
                            
            if self.EvaluateAllSubmissionsScheduled() == True:
                done = True
            else:
                self.resetSolTracks()
                self.resetSolSubmissions()
        for session in range(self.getProblem().getNumberOfSessions()):
            for room in range(self.getProblem().getNumberOfRooms()):
                if self.getSolSubmissions()[session][room].count(-1) == len(self.getSolSubmissions()[session][room]):
                    self.getSolTracks()[session][room] = -1
                
class RandomInd(InitialSolution):
    def __init__(self, problem):
        InitialSolution.__init__(self, problem)
        temp = [sub for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() > 1]
        temp2 = [sub for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() == 1]
        sessions = [session for session in range(self.getProblem().getNumberOfSessions())]
        rooms = [room for room in range(self.getProblem().getNumberOfRooms())]
        np.random.shuffle(sessions)
        np.random.shuffle(rooms)
        done = False
        while done == False:
            np.random.shuffle(temp)
            for sub in temp:
                stop = False
                for session in sessions:
                    if stop == True:
                        break
                    for room in rooms:
                        if stop == True:
                            break
                        if ((self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() <= self.getSolSubmissions()[session][room].count(-1)) and (self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName()) == self.getSolTracks()[session][room])) or ((self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() <= self.getSolSubmissions()[session][room].count(-1)) and (self.getSolTracks()[session][room] == -1)):
                            for ts in range(self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots()):
                                i = self.getSolSubmissions()[session][room].index(-1)
                                self.getSolSubmissions()[session][room][i] = sub
                            stop = True
                            self.getSolTracks()[session][room] = self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName())
            np.random.shuffle(sessions)
            np.random.shuffle(rooms)
            np.random.shuffle(temp2)
            for sub in temp2:
                stop = False
                for session in sessions:
                    if stop == True:
                        break
                    for room in rooms:
                        if stop == True:
                            break
                        if ((self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() <= self.getSolSubmissions()[session][room].count(-1)) and (self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName()) == self.getSolTracks()[session][room])) or ((self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() <= self.getSolSubmissions()[session][room].count(-1)) and (self.getSolTracks()[session][room] == -1)):
                            i = self.getSolSubmissions()[session][room].index(-1)
                            self.getSolSubmissions()[session][room][i] = sub
                            stop = True
                            self.getSolTracks()[session][room] = self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getSubmissionTrack().getTrackName())
                            
            if self.EvaluateAllSubmissionsScheduled() == True:
                for session in range(self.getProblem().getNumberOfSessions()):
                    for room in range(self.getProblem().getNumberOfRooms()):
                        if self.getSolSubmissions()[session][room].count(-1) == len(self.getSolSubmissions()[session][room]):
                            self.getSolTracks()[session][room] = -1
                self.resetSolSubmissions()
                done = True
            else:
                self.resetSolTracks()
                self.resetSolSubmissions()
        