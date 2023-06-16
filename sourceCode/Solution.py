# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: pylya
"""

from Problem import *
import sys
import numpy as np

class Solution():
    def __init__(self, problem, parameters):        
        self.__problem = problem
        self.__allEvaluations = [lambda: self.getWeight(0)*self.EvaluateTracksSessions(), lambda: self.getWeight(1)*self.EvaluateTracksRooms(), lambda: self.getWeight(2)*self.EvaluateSessionsRooms(), lambda: self.getWeight(3)*self.EvaluateTracksTracks(), lambda: self.getWeight(4)*self.EvaluateNumberOfRoomsPerTrack(), lambda: self.getWeight(5)*self.EvaluateParallelTracks(), lambda: self.getWeight(6)*self.EvaluateConsecutiveTracks(), lambda: self.getWeight(7)*self.EvaluateTracksOrder(), lambda: self.getWeight(8)*self.EvaluateSubmissionsTimezones(), lambda: self.getWeight(9)*self.EvaluateSubmissionsOrder(), lambda: self.getWeight(10)*self.EvaluateSubmissionsSessions(), lambda: self.getWeight(11)*self.EvaluateSubmissionsRooms(), lambda: self.getWeight(12)*self.EvaluateSpeakersConflictsSessions(), lambda: self.getWeight(13)*self.EvaluateAttendeesConflicts(), lambda: self.getWeight(14)*self.EvaluateOrganizerConflicts(), lambda: self.getWeight(15)*self.EvaluateTrackDuration()]
        self.__allLEvaluations = [lambda: self.LEvaluateTracksSessions(), lambda: self.LEvaluateTracksRooms(), lambda: self.LEvaluateSessionsRooms(), lambda: self.LEvaluateTracksTracks(), lambda: self.LEvaluateNumberOfRoomsPerTrack(), lambda: self.LEvaluateParallelTracks(), lambda: self.LEvaluateConsecutiveTracks(), lambda: self.LEvaluateTracksOrder(), lambda: self.LEvaluateSubmissionsTimezones(), lambda: self.LEvaluateSubmissionsOrder(), lambda: self.LEvaluateSubmissionsSessions(), lambda: self.LEvaluateSubmissionsRooms(), lambda: self.LEvaluateSpeakersConflictsSessions(), lambda: self.LEvaluateAttendeesConflicts(), lambda: self.LEvaluateOrganizerConflicts(), lambda: self.LEvaluateTrackDuration()]
        self.__weights = parameters[6]
        self.__evaluations = [self.__allEvaluations[i] for i in range(len(self.__allEvaluations)) if self.getWeight(i) != 0]
        self.__evaluationsforl = [self.__allEvaluations[i] for i in range(len(self.__allEvaluations)) if self.getWeight(i) != 0]
        self.__Levaluations = [self.__allLEvaluations[i] for i in range(len(self.__allEvaluations)) if self.getWeight(i) != 0]
        self.__Levaluationsmap = {self.__evaluations[i] : self.__Levaluations[i] for i in range(len(self.__evaluations))}
        temp = self.__evaluations[0]
        self.__evaluations[0] = lambda: self.EvaluateConsecutiveSubmissions()
        self.__evaluations.append(temp)
        #self.__evaluations.append(lambda: self.EvaluateEmptyTS())
        #self.__evaluations.append(lambda: self.EvaluateBalance())
        self.__solTracks = [[-1 for x in range(self.getProblem().getNumberOfRooms())] for y in range(self.getProblem().getNumberOfSessions())]
        self.__solSubmissions = [[[-1 for x in range(self.getProblem().getSession(z).getMaxTimeSlots())] for y in range(self.getProblem().getNumberOfRooms())] for z in range(self.getProblem().getNumberOfSessions())]
        self.__indsolSubmissions = [[self.getProblem().getSubmissionIndex(x.getName()) for x in self.getProblem().getTrack(y).getSubmissions()] for y in range(self.getProblem().getNumberOfTracks())]

    def getProblem(self) -> Problem:
        return self.__problem
    
    def getWeight(self, index):
        return self.__weights[index]
    
    def getWeights(self) -> list:
        return self.__weights
    
    def getEvaluations(self):
        return self.__evaluations
    
    def getEvaluationsForL(self):
        return self.__evaluationsforl
    
    def getLEvaluation(self, key):
        return self.__Levaluationsmap[key]
    
    def getSolTracks(self) -> list:
        return self.__solTracks
    
    def resetSolTracks(self):
        self.__solTracks = [[-1 for x in range(self.getProblem().getNumberOfRooms())] for y in range(self.getProblem().getNumberOfSessions())]
    
    def getSolSubmissions(self) -> list:
        return self.__solSubmissions
    
    def resetSolSubmissions(self):
        self.__solSubmissions = [[[-1 for x in range(self.getProblem().getSession(z).getMaxTimeSlots())] for y in range(self.getProblem().getNumberOfRooms())] for z in range(self.getProblem().getNumberOfSessions())]
    
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
    
    def EvaluateTracksSessions(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().getTracksSessionsPenaltybyIndex(self.getSolTracks()[i][j], i)
        return pen
    
    def LEvaluateTracksSessions(self):
        indexes = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (self.getProblem().getTracksSessionsPenaltybyIndex(self.getSolTracks()[i][j], i) != 0):
                    indexes.append([i,j])
        np.random.shuffle(indexes)
        return [indexes, [0]]
      
    def EvaluateTracksRooms(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().getTracksRoomsPenaltybyIndex(self.getSolTracks()[i][j], j)
        return pen
    
    def LEvaluateTracksRooms(self):
        indexes = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (self.getProblem().getTracksRoomsPenaltybyIndex(self.getSolTracks()[i][j], j) != 0):
                    indexes.append([i,j])
        np.random.shuffle(indexes)
        return [indexes, [0,1]]
       
    def EvaluateSessionsRooms(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().getSessionsRoomsPenaltybyIndex(i, j)
        return pen
    
    def LEvaluateSessionsRooms(self):
        indexes = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (self.getProblem().getSessionsRoomsPenaltybyIndex(i, j) != 0):
                    indexes.append([i,j])
        np.random.shuffle(indexes)
        return [indexes, [0,1]]

    def EvaluateTracksTracks(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(j, len(self.getSolTracks()[i])):
                    if (self.getSolTracks()[i][j] != self.getSolTracks()[i][x]) and (self.getSolTracks()[i][j] != -1) and (self.getSolTracks()[i][x] != -1):
                        pen += self.getProblem().getTracksTracksPenaltybyIndex(self.getSolTracks()[i][j], self.getSolTracks()[i][x])
        return pen
    
    def LEvaluateTracksTracks(self):
        indexes = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(j, len(self.getSolTracks()[i])):
                    if (self.getSolTracks()[i][j] != self.getSolTracks()[i][x]) and (self.getSolTracks()[i][j] != -1) and (self.getSolTracks()[i][x] != -1) and (self.getProblem().getTracksTracksPenaltybyIndex(self.getSolTracks()[i][j], self.getSolTracks()[i][x]) != 0):
                        indexes.append([i,j])
                        indexes.append([i,x])
        np.random.shuffle(indexes)
        return [indexes, [0]]
    
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
    
    def LEvaluateNumberOfRoomsPerTrack(self):
        indexes = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (j not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(j)
                    if len(di[self.getSolTracks()[i][j]]) > 1:
                        indexes.append([i,j])
        np.random.shuffle(indexes)
        return [indexes, [0,1]]
      
    def EvaluateParallelTracks(self):
        pen = 0
        temp = [tuple(self.getSolTracks()[session]) for session in range(len(self.getSolTracks()))]
        for track in range(self.getProblem().getNumberOfTracks()):
            for session in range(len(temp)):
                c = temp[session].count(track)
                if c > 1:
                    pen += c - 1
        return pen
    
    def LEvaluateParallelTracks(self):
        indexes = []
        temp = [tuple(self.getSolTracks()[session]) for session in range(len(self.getSolTracks()))]
        for track in range(self.getProblem().getNumberOfTracks()):
            for session in range(len(temp)):
                c = temp[session].count(track)
                if c > 1:
                    find = self.getSolTracks()[session].index(track)
                    indexes.append([session, find])
        np.random.shuffle(indexes)
        return [indexes, [0]]

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
    
    def LEvaluateConsecutiveTracks(self):
        indexes = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (i not in di[self.getSolTracks()[i][j]]):
                    di[self.getSolTracks()[i][j]].append(i)
                    if (len(di[self.getSolTracks()[i][j]])) and (sum(di[self.getSolTracks()[i][j]]) != sum(range(di[self.getSolTracks()[i][j]][0], di[self.getSolTracks()[i][j]][len(di[self.getSolTracks()[i][j]]) - 1] + 1))):
                        indexes.append([i,j])
        np.random.shuffle(indexes)
        return [indexes, [0]]
       
    def EvaluateTracksOrder(self):
        info = [(track, self.getProblem().getTrack(track).getOrder()) for track in range(self.getProblem().getNumberOfTracks()) if self.getProblem().getTrack(track).getOrder() != 0]
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
    
    def LEvaluateTracksOrder(self):
        info = [(track, self.getProblem().getTrack(track).getOrder()) for track in range(self.getProblem().getNumberOfTracks()) if self.getProblem().getTrack(track).getOrder() != 0]
        sorted_info = sorted(info, key = lambda x: x[1])
        di = {}
        for i in sorted_info:
            di[i] = []
        indexes = []
        for track in di.keys():
            for session in range(len(self.getSolTracks())):
                if (track[0] in self.getSolTracks()[session]) and (session not in di[track]):
                    di[track].append(session)
                    find = self.getSolTracks()[session].index(track[0])
                    indexes.append([session, find])
        np.random.shuffle(indexes)
        return [indexes, [0]]
         
    def EvaluateSubmissionsTimezones(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().getSubmissionsTimezonesPenaltybyIndex(self.getSolSubmissions()[i][j][x], i)
        return pen
    
    def LEvaluateSubmissionsTimezones(self):
        indexes = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (self.getProblem().getSubmissionsTimezonesPenaltybyIndex(self.getSolSubmissions()[i][j][x], i) != 0) :
                        indexes.append([i,j,x])
        np.random.shuffle(indexes)
        return [indexes, [3]]
         
    def EvaluateSubmissionsOrder(self):
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
                if (self.getProblem().getSubmission(sub).getOrder() != order) and (self.getProblem().getSubmission(sub).getOrder() != 0):
                    pen += 1
                order += 1
        return pen
    
    def LEvaluateSubmissionsOrder(self):
        indexes = []
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
                if (self.getProblem().getSubmission(sub).getOrder() != order) and (self.getProblem().getSubmission(sub).getOrder() != 0):
                    for session in range(len(self.getSolTracks())):
                        for room in range(len(self.getSolTracks()[session])):
                            if (track == self.getSolTracks()[session][room]) and (sub in self.getSolSubmissions()[session][room]):
                                find = self.getSolSubmissions()[session][room].index(sub)
                                indexes.append([session, room, find])
                                return indexes
                order += 1
        return [indexes, [2,3]]
    
    def EvaluateSubmissionsSessions(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().getSubmissionsSessionsPenaltybyIndex(self.getSolSubmissions()[i][j][x], i)
        return pen
    
    def LEvaluateSubmissionsSessions(self):
        indexes = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (self.getProblem().getSubmissionsSessionsPenaltybyIndex(self.getSolSubmissions()[i][j][x], i) != 0):
                        indexes.append([i,j,x])
        np.random.shuffle(indexes)
        return [indexes, [3]]
     
    def EvaluateSubmissionsRooms(self):
        pen = 0
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().getSubmissionsRoomsPenaltybyIndex(self.getSolSubmissions()[i][j][x], j)
        return pen
    
    def LEvaluateSubmissionsRooms(self):
        indexes = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (self.getProblem().getSubmissionsRoomsPenaltybyIndex(self.getSolSubmissions()[i][j][x], j) != 0):
                        indexes.append([i,j,x])
        np.random.shuffle(indexes)
        return [indexes, [2,3]]
      
    def EvaluateSpeakersConflicts(self):
        pen = 0
        di = {str(session)+str(ts):[] for session in range(self.getProblem().getNumberOfSessions()) for ts in range(self.getProblem().getSession(session).getMaxTimeSlots())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSpeakerConflicts()) != 0) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)+str(ts)]):
                        di[str(session)+str(ts)].append(self.getSolSubmissions()[session][room][ts])
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session)+str(ts)]) > 1:
                    for j in range(len(di[str(session)+str(ts)])-1):
                        for z in range(j+1, len(di[str(session)+str(ts)])):
                            if (self.getProblem().getSubmission(di[str(session)+str(ts)][j]).getName() in self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getSpeakerConflicts()):
                                pen += 1
        return pen
    
    def LEvaluateSpeakersConflicts(self):
        indexes = []
        di = {str(session)+str(ts):[] for session in range(self.getProblem().getNumberOfSessions()) for ts in range(self.getProblem().getSession(session).getMaxTimeSlots())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSpeakerConflicts()) != 0) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)+str(ts)]):
                        di[str(session)+str(ts)].append(self.getSolSubmissions()[session][room][ts])
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session)+str(ts)]) > 1:
                    for j in range(len(di[str(session)+str(ts)])-1):
                        for z in range(j+1, len(di[str(session)+str(ts)])):
                            if (self.getProblem().getSubmission(di[str(session)+str(ts)][j]).getName() in self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getSpeakerConflicts()):
                                for room in range(len(self.getSolTracks()[session])):
                                    if di[str(session)+str(ts)][j] in self.getSolSubmissions()[session][room]:
                                        indexes.append([session,room,ts])
                                    if di[str(session)+str(ts)][z] in self.getSolSubmissions()[session][room]:
                                        indexes.append([session,room,ts])
        np.random.shuffle(indexes)
        return [indexes, [2,3]]
    
    def EvaluateSpeakersConflictsSessions(self):
        pen = 0
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getSpeakerConflicts()) != 0) and ((self.getSolSubmissions()[i][j][x], j) not in di[i]):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getSubmission(di[i][j][0]).getName() in self.getProblem().getSubmission(di[i][z][0]).getSpeakerConflicts()) and (di[i][j][1] != di[i][z][1]):
                            pen += 1
        return pen
    
    def LEvaluateSpeakersConflictsSessions(self):
        indexes = []
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getSpeakerConflicts()) != 0) and ((self.getSolSubmissions()[i][j][x], j) not in di[i]):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getSubmission(di[i][j][0]).getName() in self.getProblem().getSubmission(di[i][z][0]).getSpeakerConflicts()) and (di[i][j][1] != di[i][z][1]):
                            find1 = self.getSolSubmissions()[i][di[i][j][1]].index(di[i][j][0])
                            find2 = self.getSolSubmissions()[i][di[i][z][1]].index(di[i][z][0])
                            indexes.append([i,di[i][j][1],find1])
                            indexes.append([i,di[i][z][1],find2])
        np.random.shuffle(indexes)
        return [indexes, [3,4]]
     
    def EvaluateOrganizerConflicts(self):
        pen = 0
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (len(self.getProblem().getTrack(self.getSolTracks()[i][j]).getOrganizerConflicts()) != 0):
                    di[i].append(self.getSolTracks()[i][j])
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getTrack(di[i][j]).getName() in self.getProblem().getTrack(di[i][z]).getOrganizerConflicts()):
                            pen += 1
        return pen
    
    def LEvaluateOrganizerConflicts(self):
        indexes = []
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (len(self.getProblem().getTrack(self.getSolTracks()[i][j]).getOrganizerConflicts()) != 0):
                    di[i].append(self.getSolTracks()[i][j])
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getTrack(di[i][j]).getName() in self.getProblem().getTrack(di[i][z]).getOrganizerConflicts()):
                            find1 = self.getSolTracks()[i].index(di[i][j])
                            find2 = self.getSolTracks()[i].index(di[i][z])
                            indexes.append([i,find1])
                            indexes.append([i,find2])
        np.random.shuffle(indexes)
        return [indexes, [0]]
    
    def EvaluateAttendeesConflicts(self):
        pen = 0
        di = {str(session)+str(ts):[] for session in range(self.getProblem().getNumberOfSessions()) for ts in range(self.getProblem().getSession(session).getMaxTimeSlots())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getAttendeeConflicts()) != 0) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)+str(ts)]):
                        di[str(session)+str(ts)].append(self.getSolSubmissions()[session][room][ts])
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session)+str(ts)]) > 1:
                    for j in range(len(di[str(session)+str(ts)])-1):
                        for z in range(j+1, len(di[str(session)+str(ts)])):
                            if (self.getProblem().getSubmission(di[str(session)+str(ts)][j]).getName() in self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getAttendeeConflicts()):
                                pen += 1
        return pen
    
    def LEvaluateAttendeesConflicts(self):
        indexes = []
        di = {str(session)+str(ts):[] for session in range(self.getProblem().getNumberOfSessions()) for ts in range(self.getProblem().getSession(session).getMaxTimeSlots())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getAttendeeConflicts()) != 0) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)+str(ts)]):
                        di[str(session)+str(ts)].append(self.getSolSubmissions()[session][room][ts])
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session)+str(ts)]) > 1:
                    for j in range(len(di[str(session)+str(ts)])-1):
                        for z in range(j+1, len(di[str(session)+str(ts)])):
                            if (self.getProblem().getSubmission(di[str(session)+str(ts)][j]).getName() in self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getAttendeeConflicts()):
                                for room in range(len(self.getSolTracks()[session])):
                                    if di[str(session)+str(ts)][j] in self.getSolSubmissions()[session][room]:
                                        indexes.append([session,room,ts])
                                    if di[str(session)+str(ts)][z] in self.getSolSubmissions()[session][room]:
                                        indexes.append([session,room,ts])
        np.random.shuffle(indexes)
        return [indexes, [2,3]]
    
    def EvaluateAttendeesConflictsSessions(self):
        pen = 0
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getAttendeeConflicts()) != 0) and ((self.getSolSubmissions()[i][j][x], j) not in di[i]):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getSubmission(di[i][j][0]).getName() in self.getProblem().getSubmission(di[i][z][0]).getAttendeeConflicts()) and (di[i][j][1] != di[i][z][1]):
                            pen += 1
        return pen
    
    def LEvaluateAttendeesConflictsSessions(self):
        indexes = []
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getAttendeeConflicts()) != 0) and ((self.getSolSubmissions()[i][j][x], j) not in di[i]):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getSubmission(di[i][j][0]).getName() in self.getProblem().getSubmission(di[i][z][0]).getAttendeeConflicts()) and (di[i][j][1] != di[i][z][1]):
                            find1 = self.getSolSubmissions()[i][di[i][j][1]].index(di[i][j][0])
                            find2 = self.getSolSubmissions()[i][di[i][z][1]].index(di[i][z][0])
                            indexes.append([i,di[i][j][1],find1])
                            indexes.append([i,di[i][z][1],find2])
        np.random.shuffle(indexes)
        return [indexes, [3]]
    
    def EvaluateTrackDuration(self):
        pen = 0
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if (self.getSolTracks()[session][room] != -1) and (session not in di[self.getSolTracks()[session][room]]):
                    di[self.getSolTracks()[session][room]].append(session)
        for track in range(self.getProblem().getNumberOfTracks()):
            if len(di[track]) > 1:
                for j in range(len(di[track])-1):
                    for z in range(j+1, len(di[track])):
                        if (self.getProblem().getSession(di[track][j]).getDate() != self.getProblem().getSession(di[track][z]).getDate()) and (self.getProblem().getTrack(track).getRequiredTimeSlots() <= self.getProblem().getMaxDay()):
                            pen += 1
        return pen
    
    def LEvaluateTrackDuration(self):
        indexes = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if (self.getSolTracks()[session][room] != -1) and (session not in di[self.getSolTracks()[session][room]]):
                    di[self.getSolTracks()[session][room]].append(session)
        for track in range(self.getProblem().getNumberOfTracks()):
            if len(di[track]) > 1:
                for j in range(len(di[track])-1):
                    for z in range(j+1, len(di[track])):
                        if (self.getProblem().getSession(di[track][j]).getDate() != self.getProblem().getSession(di[track][z]).getDate()) and (self.getProblem().getTrack(track).getRequiredTimeSlots() <= self.getProblem().getMaxDay()):
                            find = self.getSolTracks()[di[track][j]].index(track)
                            indexes.append([di[track][j],find])
        np.random.shuffle(indexes)
        return [indexes, [0]]
    '''
    def EvaluateEmptyTS(self):
        pen = 0
        temp = [self.getSolSubmissions()[session][room] for session in range(self.getProblem().getNumberOfSessions()) for room in range(self.getProblem().getNumberOfRooms()) if self.getSolTracks()[session][room] != -1]
        for i in temp:
            pen += i.count(-1)
        return pen
    
    def EvaluateBalance(self):
        pen = 0
        temp = []
        for session in range(self.getProblem().getNumberOfSessions()):
            temp = [self.getSolSubmissions()[session][room] for room in range(self.getProblem().getNumberOfRooms()) if self.getSolTracks()[session][room] != -1]
            temp2 = self.getSolTracks()[session]
            if len(temp2) - temp2.count(-1) != self.getProblem().getNumberOfRooms():
                pen += len(temp2) - temp2.count(-1)
            for i in temp:
                if len(i) - i.count(-1) != self.getProblem().getSession(session).getMaxTimeSlots():
                    pen += len(i) - i.count(-1)
        return pen
    '''
    def EvaluateConsecutiveSubmissions(self):
        pen = 0
        di = {str(session)+str(room):[] for session in range(self.getProblem().getNumberOfSessions()) for room in range(self.getProblem().getNumberOfRooms())}
        di2 = {sub: [] for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getRequiredTimeSlots() > 1}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getRequiredTimeSlots() > 1):
                        di[str(session)+str(room)].append(self.getSolSubmissions()[session][room][ts])
                        di2[self.getSolSubmissions()[session][room][ts]].append(ts)
        for i in di.values():
            if (len(i) != 0):
                temp = set(i)
                for j in temp:
                    if self.getProblem().getSubmission(j).getRequiredTimeSlots() != i.count(j):
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
            if (sub not in temp) or (self.getProblem().getSubmission(sub).getRequiredTimeSlots() != temp.count(sub)):
                return False
        return True
    
    def EvaluateTracksSubmissionsScheduled(self, track):
        result = True
        subs = [self.getProblem().getSubmissionIndex(str(x)) for x in self.getProblem().getTrack(track).getSubmissions()]
        for sub in subs:
            count = 0
            stop = False
            for i in range(len(self.getSolTracks())):
                if stop == True:
                    break
                for j in range(len(self.getSolTracks()[i])):
                    if stop == True:
                        break
                    if self.getProblem().getSubmission(sub).getRequiredTimeSlots() == 1:
                        if sub in self.getSolSubmissions()[i][j]:
                            stop = True
                        elif sub not in self.getSolSubmissions()[i][j] and i == len(self.getSolTracks()) - 1 and j == len(self.getSolTracks()[i]) - 1:
                            result = False
                            return result
                    else:
                        if sub in self.getSolSubmissions()[i][j]:
                            count += self.getSolSubmissions()[i][j].count(sub)
                            if count == self.getProblem().getSubmission(sub).getRequiredTimeSlots():
                                stop = True
                        elif sub not in self.getSolSubmissions()[i][j] and i == len(self.getSolTracks()) - 1 and j == len(self.getSolTracks()[i]) - 1:
                            result = False
                            return result
        return result
    
    def EvaluateSolution(self):
        obj = 0
        evaluations = self.getEvaluations()
        for i in range(len(evaluations)):
            obj += evaluations[i]()
        return obj
    
    #QEvaluateSolution() is only applicable to indirect solution method
    def QEvaluateSolution(self, objective):
        obj = 0
        evaluations = self.getEvaluations()
        for i in range(len(evaluations)):
            obj += evaluations[i]()
            if obj > objective:
                return obj
        return obj
    
    def LEvaluateSolution(self):
        violations = {}
        evaluations = self.getEvaluationsForL()
        for i in range(len(evaluations)):
            violations[evaluations[i]()] = evaluations[i]
        temp = sorted(violations.keys(), reverse = True)[:3]
        top = [violations[i] for i in temp]
        return top
     
    #ValidateSolution() ensures all submissions are scheduled under their corresponding tracks
    def ValidateSolution(self):
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolTracks()[i][j] != -1:
                        if self.getSolSubmissions()[i][j][x] != -1:
                            if self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]) not in self.getProblem().getTrack(self.getSolTracks()[i][j]).getSubmissions():
                                return False
        return True
    
    def PrintSolutionTracks(self):
        for i in range(len(self.getSolTracks())):
            print('<<<', 'Session: ', self.getProblem().getSession(i).getName(), '>>>')
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    print('Room: ', self.getProblem().getRoom(j), '->', 'Track: ', self.getProblem().getTrack(self.getSolTracks()[i][j]))
                else:
                    print('Room: ', self.getProblem().getRoom(j), '->', 'Track: ', '')
            print('\n')
            
    def PrintSolutionSubmissions(self):
        for i in range(len(self.getSolTracks())):
            print('<<<', 'Session: ', self.getProblem().getSession(i).getName(), '>>>')
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    print('Room: ', self.getProblem().getRoom(j), '->', 'Track: ', self.getProblem().getTrack(self.getSolTracks()[i][j]))
                else:
                    print('Room: ', self.getProblem().getRoom(j), '->', 'Track: ', '')
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        print('*', self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getName())
                    else:
                        print('*')
            print('\n')
    
    def PrintViolations(self):
        names = ['TracksSessions:', 'TracksRooms:', 'SessionsRooms:', 'TracksTracks:', 'NumberOfRoomsPerTrack:', 'ParallelTracks:', 'ConsecutiveTracks:', 'TracksOrder:', 'SubmissionsTimezones:', 'SubmissionsOrder:', 'SubmissionsSessions:', 'SubmissionsRooms:', 'SpeakersConflictsSessions:', 'AttendeesConflicts:', 'OrganizerConflicts:', 'TrackDuration:']
        obj = [lambda: self.getWeight(0)*self.EvaluateTracksSessions(), lambda: self.getWeight(1)*self.EvaluateTracksRooms(), lambda: self.getWeight(2)*self.EvaluateSessionsRooms(), lambda: self.getWeight(3)*self.EvaluateTracksTracks(), lambda: self.getWeight(4)*self.EvaluateNumberOfRoomsPerTrack(), lambda: self.getWeight(5)*self.EvaluateParallelTracks(), lambda: self.getWeight(6)*self.EvaluateConsecutiveTracks(), lambda: self.getWeight(7)*self.EvaluateTracksOrder(), lambda: self.getWeight(8)*self.EvaluateSubmissionsTimezones(), lambda: self.getWeight(9)*self.EvaluateSubmissionsOrder(), lambda: self.getWeight(10)*self.EvaluateSubmissionsSessions(), lambda: self.getWeight(11)*self.EvaluateSubmissionsRooms(), lambda: self.getWeight(12)*self.EvaluateSpeakersConflictsSessions(), lambda: self.getWeight(13)*self.EvaluateAttendeesConflicts(), lambda: self.getWeight(14)*self.EvaluateOrganizerConflicts(), lambda: self.getWeight(15)*self.EvaluateTrackDuration()]
        for i in range(len(self.getWeights())):
            if self.getWeight(i) != 0 and obj[i]() != 0:
                print(names[i], obj[i]())
        print('ConsecutiveSubmissions:', self.EvaluateConsecutiveSubmissions())
        #print('EmptyTimeSlots:', self.EvaluateEmptyTS())
        #print('Balance:', self.EvaluateBalance())
                
    def toExcel(self, file_name = 'Solution.xlsx'):
        #Preparing sol tracks
        df = pd.DataFrame(self.getSolTracks(), 
                          index = [self.getProblem().getSession(s).getName() for s in range(self.getProblem().getNumberOfSessions())],
                          columns = [self.getProblem().getRoom(r).getName() for r in range(self.getProblem().getNumberOfRooms())])
        df = df.applymap(lambda x: self.getProblem().getTrack(x).getName() if x != -1 else '')
        
        #Preparing sol submissions
        temp2 = []
        for session in range(self.getProblem().getNumberOfSessions()):
            for t in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                temp = []
                for room in range(self.getProblem().getNumberOfRooms()):
                    if self.getSolSubmissions()[session][room][t] != -1:
                        temp.append(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][t]).getName())
                    else:
                        temp.append('')
                temp2.append(temp)
        df2 = pd.DataFrame(temp2,
                           index = [self.getProblem().getSession(s).getName() for s in range(self.getProblem().getNumberOfSessions()) for t in range(self.getProblem().getSession(s).getMaxTimeSlots())])
        
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
                        p1_list.append(self.getProblem().getTrack(self.getSolTracks()[i][j]).getName() + ' - ' + self.getProblem().getSession(i).getName())
                        p1_pen.append(self.getWeight(0)*self.getProblem().getTracksSessionsPenaltybyIndex(self.getSolTracks()[i][j], i))
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
                        p2_list.append(self.getProblem().getTrack(self.getSolTracks()[i][j]).getName() + ' - ' + self.getProblem().getRoom(j).getName())
                        p2_pen.append(self.getWeight(1)*self.getProblem().getTracksRoomsPenaltybyIndex(self.getSolTracks()[i][j], j))
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
                        p3_list.append(self.getProblem().getSession(i).getName() + ' - ' + self.getProblem().getRoom(j).getName())
                        p3_pen.append(self.getWeight(2)*self.getProblem().getSessionsRoomsPenaltybyIndex(i, j))
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
                            p4_list.append(self.getProblem().getTrack(self.getSolTracks()[i][j]).getName() + ' - ' + self.getProblem().getTrack(self.getSolTracks()[i][x]).getName() + ' - ' + self.getProblem().getSession(i).getName())
                            p4_pen.append(self.getWeight(3)*self.getProblem().getTracksTracksPenaltybyIndex(self.getSolTracks()[i][j], self.getSolTracks()[i][x]))
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
                p5_list.append(self.getProblem().getTrack(t).getName())
                p5_pen.append(self.getWeight(4)*(len(i) - 1))
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
                    p6_list.append(self.getProblem().getTrack(track).getName() + ' - ' + self.getProblem().getSession(session).getName())
                    p6_pen.append(self.getWeight(5)*(c - 1))
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
                p7_list.append(self.getProblem().getTrack(t).getName())
                p7_pen.append(self.getWeight(6)*1)
        p7_list.append('Total')
        p7_pen.append(sum(p7_pen))
        p7_pen.insert(0, '')
        df16 = pd.DataFrame(p7_list)
        df17 = pd.DataFrame(p7_pen)
        
        #Preparing Tracks Order
        p8_list = ['Evaluate Tracks Order']
        p8_pen = []
        info = [(track, self.getProblem().getTrack(track).getOrder()) for track in range(self.getProblem().getNumberOfTracks()) if self.getProblem().getTrack(track).getOrder() != 0]
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
                            p8_list.append(self.getProblem().getTrack(sorted_info[t][0]).getName())
                            p8_pen.append(self.getWeight(7)*1)
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
                            p9_list.append(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getName() + ' - ' + self.getProblem().getSession(i).getName())
                            p9_pen.append(self.getWeight(8)*self.getProblem().getSubmissionsTimezonesPenaltybyIndex(self.getSolSubmissions()[i][j][x], i))
        p9_list.append('Total')
        p9_pen.append(sum(p9_pen))
        p9_pen.insert(0, '')
        df20 = pd.DataFrame(p9_list)
        df21 = pd.DataFrame(p9_pen)
        
        #Preparing Submissions Order
        p10_list = ['Evaluate Submissions Order']
        p10_pen = []
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
                if (self.getProblem().getSubmission(sub).getOrder() != order) and (self.getProblem().getSubmission(sub).getOrder() != 0):
                    p10_list.append(self.getProblem().getSubmission(sub).getName() + ' - ' + self.getProblem().getTrack(track).getName())
                    p10_pen.append(self.getWeight(9)*1)
                order += 1
        p10_list.append('Total')
        p10_pen.append(sum(p10_pen))
        p10_pen.insert(0, '')
        df22 = pd.DataFrame(p10_list)
        df23 = pd.DataFrame(p10_pen)
        
        #Preparing Submissions|Sessions penalty
        p11_list = ['Evaluate Submissions|Sessions']
        p11_pen = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        if self.getProblem().getSubmissionsSessionsPenaltybyIndex(self.getSolSubmissions()[i][j][x], i) != 0:
                            p11_list.append(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getName() + ' - ' + self.getProblem().getSession(i).getName())
                            p11_pen.append(self.getWeight(10)*self.getProblem().getSubmissionsSessionsPenaltybyIndex(self.getSolSubmissions()[i][j][x], i))
        p11_list.append('Total')
        p11_pen.append(sum(p11_pen))
        p11_pen.insert(0, '')
        df24 = pd.DataFrame(p11_list)
        df25 = pd.DataFrame(p11_pen)
        
        #Preparing Submissions|Rooms penalty
        p12_list = ['Evaluate Submissions|Rooms']
        p12_pen = []
        for i in range(len(self.getSolTracks())):        
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        if self.getProblem().getSubmissionsRoomsPenaltybyIndex(self.getSolSubmissions()[i][j][x], j) != 0:
                            p12_list.append(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getName() + ' - ' + self.getProblem().getRoom(j).getName())
                            p12_pen.append(self.getWeight(11)*self.getProblem().getSubmissionsRoomsPenaltybyIndex(self.getSolSubmissions()[i][j][x], j))
        p12_list.append('Total')
        p12_pen.append(sum(p12_pen))
        p12_pen.insert(0, '')
        df26 = pd.DataFrame(p12_list)
        df27 = pd.DataFrame(p12_pen)
        
        #Preparing Speakers Conflicts [S]
        p13_list = ['Evaluate Speakers Conflicts [S]']
        p13_pen = []
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getSpeakerConflicts()) != 0) and ((self.getSolSubmissions()[i][j][x], j) not in di[i]):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getSubmission(di[i][j][0]).getName() in self.getProblem().getSubmission(di[i][z][0]).getSpeakerConflicts()) and (di[i][j][1] != di[i][z][1]):
                            p13_list.append(str(self.getProblem().getSubmission(di[i][j][0]).getName()) + ' - ' + str(self.getProblem().getSubmission(di[i][z][0]).getName()))
                            p13_pen.append(self.getWeight(12)*1)
        p13_list.append('Total')
        p13_pen.append(sum(p13_pen))
        p13_pen.insert(0, '')
        df28 = pd.DataFrame(p13_list)
        df29 = pd.DataFrame(p13_pen)
        
        #Preparing Speakers Conflicts [TS]
        p14_list = ['Evaluate Speakers Conflicts [TS]']
        p14_pen = []
        di = {str(session)+str(ts):[] for session in range(self.getProblem().getNumberOfSessions()) for ts in range(self.getProblem().getSession(session).getMaxTimeSlots())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getSpeakerConflicts()) != 0) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)+str(ts)]):
                        di[str(session)+str(ts)].append(self.getSolSubmissions()[session][room][ts])
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session)+str(ts)]) > 1:
                    for j in range(len(di[str(session)+str(ts)])-1):
                        for z in range(j+1, len(di[str(session)+str(ts)])):
                            if (self.getProblem().getSubmission(di[str(session)+str(ts)][j]).getName() in self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getSpeakerConflicts()):
                                p14_list.append(str(self.getProblem().getSubmission(di[str(session)+str(ts)][j]).getName()) + ' - ' + str(self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getName()))
                                p14_pen.append(self.getWeight(12)*1)
        p14_list.append('Total')
        p14_pen.append(sum(p14_pen))
        p14_pen.insert(0, '')
        df30 = pd.DataFrame(p14_list)
        df31 = pd.DataFrame(p14_pen)
        
        #Preparing Organizers Conflicts
        p15_list = ['Evaluate Organizers Conflicts']
        p15_pen = []
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (len(self.getProblem().getTrack(self.getSolTracks()[i][j]).getOrganizerConflicts()) != 0):
                    di[i].append(self.getSolTracks()[i][j])
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getTrack(di[i][j]).getName() in self.getProblem().getTrack(di[i][z]).getOrganizerConflicts()):
                            p15_list.append(self.getProblem().getTrack(di[i][j]).getName() + ' - ' + self.getProblem().getTrack(di[i][z]).getName())
                            p15_pen.append(self.getWeight(14)*1)
        p15_list.append('Total')
        p15_pen.append(sum(p15_pen))
        p15_pen.insert(0, '')
        df32 = pd.DataFrame(p15_list)
        df33 = pd.DataFrame(p15_pen)
        
        #Preparing Attendees Conflicts [S]
        p16_list = ['Evaluate Attendees Conflicts [S]']
        p16_pen = []
        di = {session:[] for session in range(self.getProblem().getNumberOfSessions())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (self.getSolSubmissions()[i][j][x] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[i][j][x]).getAttendeeConflicts()) != 0) and ((self.getSolSubmissions()[i][j][x], j) not in di[i]):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i])-1):
                    for z in range(j+1, len(di[i])):
                        if (self.getProblem().getSubmission(di[i][j][0]).getName() in self.getProblem().getSubmission(di[i][z][0]).getAttendeeConflicts()) and (di[i][j][1] != di[i][z][1]):
                            p16_list.append(self.getProblem().getSubmission(di[i][j][0]).getName() + ' - ' + self.getProblem().getSubmission(di[i][z][0]).getName())
                            p16_pen.append(self.getWeight(13)*1)
        p16_list.append('Total')
        p16_pen.append(sum(p16_pen))
        p16_pen.insert(0, '')
        df34 = pd.DataFrame(p16_list)
        df35 = pd.DataFrame(p16_pen)
        
        #Preparing Attendees Conflicts[TS]
        p17_list = ['Evaluate Attendees Conflicts [TS]']
        p17_pen = []
        di = {str(session)+str(ts):[] for session in range(self.getProblem().getNumberOfSessions()) for ts in range(self.getProblem().getSession(session).getMaxTimeSlots())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (len(self.getProblem().getSubmission(self.getSolSubmissions()[session][room][ts]).getAttendeeConflicts()) != 0) and (self.getSolSubmissions()[session][room][ts] not in di[str(session)+str(ts)]):
                        di[str(session)+str(ts)].append(self.getSolSubmissions()[session][room][ts])
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session)+str(ts)]) > 1:
                    for j in range(len(di[str(session)+str(ts)])-1):
                        for z in range(j+1, len(di[str(session)+str(ts)])):
                            if (self.getProblem().getSubmission(di[str(session)+str(ts)][j]).getName() in self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getAttendeeConflicts()):
                                p17_list.append(self.getProblem().getSubmission(di[str(session)+str(ts)][j]).getName() + ' - ' + self.getProblem().getSubmission(di[str(session)+str(ts)][z]).getName())
                                p17_pen.append(self.getWeight(13)*1)
        p17_list.append('Total')
        p17_pen.append(sum(p17_pen))
        p17_pen.insert(0, '')
        df36 = pd.DataFrame(p17_list)
        df37 = pd.DataFrame(p17_pen)
        
        #Preparing Track Duration
        p18_list = ['Evaluate Track Duration']
        p18_pen = []
        di = {track:[] for track in range(self.getProblem().getNumberOfTracks())}
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if (self.getSolTracks()[session][room] != -1) and (session not in di[self.getSolTracks()[session][room]]):
                    di[self.getSolTracks()[session][room]].append(session)
        for track in range(self.getProblem().getNumberOfTracks()):
            if len(di[track]) > 1:
                for j in range(len(di[track])-1):
                    for z in range(j+1, len(di[track])):
                        if (self.getProblem().getSession(di[track][j]).getDate() != self.getProblem().getSession(di[track][z]).getDate()) and (self.getProblem().getTrack(track).getRequiredTimeSlots() <= self.getProblem().getMaxDay()):
                            p18_list.append(self.getProblem().getTrack(track).getName())
                            p18_pen.append(self.getWeight(15)*1)
        p18_list.append('Total')
        p18_pen.append(sum(p18_pen))
        p18_pen.insert(0, '')
        df38 = pd.DataFrame(p18_list)
        df39 = pd.DataFrame(p18_pen)
             
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
            #Tracks Order
            df18.to_excel(writer, sheet_name = 'violations', startcol = 15,index = False, header = False)
            df19.to_excel(writer, sheet_name = 'violations', startcol = 16,index = False, header = False)
            #Submissions|Timezones
            df20.to_excel(writer, sheet_name = 'violations', startcol = 17,index = False, header = False)
            df21.to_excel(writer, sheet_name = 'violations', startcol = 18,index = False, header = False)
            #Submissions Order
            df22.to_excel(writer, sheet_name = 'violations', startcol = 19,index = False, header = False)
            df23.to_excel(writer, sheet_name = 'violations', startcol = 20,index = False, header = False)
            #Submissions|Sessions
            df24.to_excel(writer, sheet_name = 'violations', startcol = 21,index = False, header = False)
            df25.to_excel(writer, sheet_name = 'violations', startcol = 22,index = False, header = False)
            #Submissions|Rooms
            df26.to_excel(writer, sheet_name = 'violations', startcol = 23,index = False, header = False)
            df27.to_excel(writer, sheet_name = 'violations', startcol = 24,index = False, header = False)
            #Speakers Conflicts [S]
            df28.to_excel(writer, sheet_name = 'violations', startcol = 25,index = False, header = False)
            df29.to_excel(writer, sheet_name = 'violations', startcol = 26,index = False, header = False)
            #Speakers Conflicts [TS]
            df30.to_excel(writer, sheet_name = 'violations', startcol = 27,index = False, header = False)
            df31.to_excel(writer, sheet_name = 'violations', startcol = 28,index = False, header = False)
            #Organizers Conflicts
            df32.to_excel(writer, sheet_name = 'violations', startcol = 29,index = False, header = False)
            df33.to_excel(writer, sheet_name = 'violations', startcol = 30,index = False, header = False)
            #Attendees Conflicts [S]
            df34.to_excel(writer, sheet_name = 'violations', startcol = 31,index = False, header = False)
            df35.to_excel(writer, sheet_name = 'violations', startcol = 32,index = False, header = False)
            #Attendees Conflicts [TS]
            df36.to_excel(writer, sheet_name = 'violations', startcol = 33,index = False, header = False)
            df37.to_excel(writer, sheet_name = 'violations', startcol = 34,index = False, header = False)
            #Track Duration
            df38.to_excel(writer, sheet_name = 'violations', startcol = 35,index = False, header = False)
            df39.to_excel(writer, sheet_name = 'violations', startcol = 36,index = False, header = False)

    def ReadSolution(self, file_name = None):
        #Creating temporary tracks solution
        file = pd.read_excel(file_name, header = None, keep_default_na = False, na_filter = False)
        temp2 = []
        for session in range(1, self.getProblem().getNumberOfSessions() + 1):
            temp = []
            for room in range(1, len(file.keys())):
                if file.iloc[session][room] != '':
                    temp.append(self.getProblem().getTrackIndex(file.iloc[session][room]))
                else:
                    temp.append(-1)
            temp2.append(temp)
            
        #Converting temporary tracks solution into permanent tracks solution
        for session in range(len(temp2)):
            for room in range(len(temp2[session])):
                self.getSolTracks()[session][room] = temp2[session][room]
                
        #Creating temporary submissions solution
        temp3 = []
        sum_ts = 0
        for session in range(self.getProblem().getNumberOfSessions()):
            index = self.getProblem().getNumberOfSessions() + 1 + sum_ts
            temp2 = []
            for room in range(1, len(file.keys())):
                temp = []
                for ts in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                    index += 1
                    if file.iloc[index][room] != '':
                        temp.append(self.getProblem().getSubmissionIndex(file.iloc[index][room]))
                    else:
                        temp.append(-1)
                index = self.getProblem().getNumberOfSessions() + 1 + sum_ts
                temp2.append(temp)
            temp3.append(temp2)
            sum_ts += self.getProblem().getSession(session).getMaxTimeSlots()
        
        #Converting temporary submissions solution into permanent submissions solution
        for session in range(len(temp3)):
            for room in range(len(temp3[session])):
                for ts in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                    self.getSolSubmissions()[session][room][ts] = temp3[session][room][ts]