# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: pylya
"""

from Problem import *
from Parameters import *
import sys
import numpy as np

class Solution:
    def __init__(self, problem, parameters):        
        self.__problem = problem
        self.__parameters = parameters
        self.__solTracks = [[-1 for x in range(self.getProblem().getNumberOfRooms())] for y in range(self.getProblem().getNumberOfSessions())]
        self.__solSubmissions = [[[-1 for x in range(self.getProblem().getSession(z).getSessionMaxTimeSlots())] for y in range(self.getProblem().getNumberOfRooms())] for z in range(self.getProblem().getNumberOfSessions())]
        self.__indsolSubmissions = [[x for x in self.getProblem().getTrack(y).getTrackSubmissionsList()] for y in range(self.getProblem().getNumberOfTracks())]
        
    def getProblem(self) -> Problem:
        return self.__problem
    
    def getParameters(self) -> Parameters:
        return self.__parameters
    
    def getSolTracks(self) -> list:
        return self.__solTracks
    
    def getSolSubmissions(self) -> list:
        return self.__solSubmissions
    
    def getIndSolSubmissions(self) -> list:
        return self.__indsolSubmissions
    
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
    
    def EvaluateTracksSessions(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().getTracksSessionsPenaltybyIndex(self.getSolTracks()[i][j], i)
        return pen
    
    def EvaluateTracksRooms(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().getTracksRoomsPenaltybyIndex(self.getSolTracks()[i][j], j)
        return pen
    
    def EvaluateSessionsRooms(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().getSessionsRoomsPenaltybyIndex(i, j)
        return pen
    
    def EvaluateTracksTracks(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(j, len(self.getSolTracks()[i])):
                    if (self.getSolTracks()[i][j] != self.getSolTracks()[i][x]) and (self.getSolTracks()[i][j] != -1) and (self.getSolTracks()[i][x] != -1):
                        pen += self.getProblem().getTracksTracksPenaltybyIndex(self.getSolTracks()[i][j], self.getSolTracks()[i][x])
        return pen
    
    def EvaluateNumberOfRoomsPerTrack(self):
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
    
    def EvaluateParallelTracks(self):
        pen = 0
        temp = [tuple(self.getSolTracks()[session]) for session in range(len(self.getSolTracks()))]
        for track in range(self.getProblem().getNumberOfTracks()):
            for session in range(len(temp)):
                c = temp[session].count(track)
                if c > 1:
                    pen += c - 1
        return pen
    
    def EvaluateConsecutiveTracks(self):
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
    
    def EvaluateTracksRelativeOrder(self):
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
    
    '''
    Evaluation for Tracks actual order. However, what does this mean?
    '''
    
    def EvaluateSubmissionsTimezones(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().getSubmissionsTimezonesPenaltybyIndex(self.getSolSubmissions()[i][j][x], i)
        return pen
    
    def EvaluateSubmissionsRelativeOrder(self):
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolSubmissions()[session][room])):
                        if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getSolSubmissions()[session][room][ts] not in di[self.getSolTracks()[session][room]]):
                            di[self.getSolTracks()[session][room]].append(self.getSolSubmissions()[session][room][ts])
        for track in range(self.getProblem().getNumberOfTracks()):
            order = 1
            for sub in di[track]:
                if (self.getProblem().getSubmission(sub).getSubmissionRelativeOrder() != order) and (self.getProblem().getSubmission(sub).getSubmissionRelativeOrder() != 0):
                    pen += 1
                order += 1
        return pen
    
    def EvaluateSubmissionsActualOrder(self):
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolSubmissions()[session][room])):
                        if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getSolSubmissions()[session][room][ts] not in di[self.getSolTracks()[session][room]]):
                            di[self.getSolTracks()[session][room]].append(self.getSolSubmissions()[session][room][ts])
        for track in range(self.getProblem().getNumberOfTracks()):
            order = 1
            for sub in di[track]:
                if (self.getProblem().getSubmission(sub).getSubmissionActualOrder() != order) and (self.getProblem().getSubmission(sub).getSubmissionActualOrder() != 0):
                    pen += 1
                order += 1
        return pen
    
    def EvaluateSubmissionsSessions(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().getSubmissionsSessionsPenaltybyIndex(self.getSolSubmissions()[i][j][x], i)
        return pen
    
    def EvaluateSubmissionsRooms(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().getSubmissionsRoomsPenaltybyIndex(self.getSolSubmissions()[i][j][x], j)
        return pen
    
    def EvaluateSpeakersConflicts(self): #Session Level
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
    
    def EvaluateAttendeesConflicts(self): #Session Level
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
    
    def EvaluateOrganiserConflicts(self):
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
    
    '''
    Evaluate Track duration. Need to discuss.
    '''
    
    def EvaluateTracksBuildings(self):
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] in di.keys()) and (self.getProblem().getRoom(j).getRoomBuilding() not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(self.getProblem().getRoom(j).getRoomBuilding())
        for track in di.values():
            pen += len(track) - 1
        return pen
    
    '''
    Evaluate Balance. Need to discuss.
    '''
    
    def EvaluateSpeakersConflictsTS(self): #Time slot Level
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
    
    def EvaluateAttendeesConflictsTS(self): #Time slot level
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
    
    def EvaluateCanSubmissionOpenSession(self):
        pen = 0
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getProblem().getSubmission(self.getSolSubmissions()[session][room][0]).getSubmissionCanOpenSession() == False:
                    pen += 1
        return pen
    
    def EvaluateCanSubmissionCloseSession(self):
        pen = 0
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getProblem().getSubmission(self.getSolSubmissions()[session][room][len(self.getSolSubmissions()[session][room]) - 1]).getSubmissionCanCloseSession() == False:
                    pen += 1
        return pen
    
    def EvaluateSubmissionsSameSession(self):
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
    
    def EvaluateSubmissionsDifferentSession(self):
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
    
    def EvaluateTrackMaxNumberOfDays(self):
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
    
    def EvaluateTracksSameRoom(self):
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
    
    def EvaluateTracksSameBuilding(self):
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
    
    '''
    Evaluate Session's Preferred number of time slots. Need to discuss.
    '''
    
    '''
    Evaluate Session's Min number of time slots. Need to discuss.
    '''
    
    '''
    Evaluate Session's Max number of time slots. Need to discuss.
    '''
    
    def EvaluateExtendedSubmissions(self):
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
    
    def EvaluateAllSubmissionsScheduled(self):
        temp = [self.getSolSubmissions()[session][room][ts] for session in range(len(self.getSolTracks())) for room in range(len(self.getSolTracks()[session])) for ts in range(len(self.getSolSubmissions()[session][room])) if self.getSolSubmissions()[session][room][ts] != -1]
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            if (sub not in temp) or (self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() != temp.count(sub)):
                return False
        return True
    
    def ValidateSolution(self):
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolTracks()[i][j] != -1:
                        if self.getSolSubmissions()[i][j][x] != -1:
                            if self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]) not in self.getProblem().getTrack(self.getSolTracks()[i][j]).getTrackSubmissionsList():
                                return False
        return True
    
    '''
    Evaluate Solution
    '''
    
    '''
    Print Violations
    '''
    
    '''
    toExcel
    '''
    
    '''
    ReadSolution
    '''
    
class InitialSolution(Solution):
    def __init__(self, problem, parameters):
        Solution.__init__(self, problem, parameters)
    
class Random(InitialSolution):
    def __init__(self, problem, parameters):
        InitialSolution.__init__(self, problem, parameters)
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
            