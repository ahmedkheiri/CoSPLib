# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:19:00 2023

@author: pylya
"""

from Problem import *
from Solution import *
from ExactModels import *
import numpy as np
from csv import writer

class Optimisation():
    def __init__(self, problem, solution):
        self.__solution = solution
        self.__problem = problem
        
    def getProblem(self) -> Problem:
        return self.__problem
    
    def getSolution(self) -> Solution:
        return self.__solution
    
    def setRLscores(self, operators):
        self.__RL_scores = [round(np.random.random(), 2) for x in range(operators)]
    
    def getRLscores(self) -> list:
        return self.__RL_scores
         
    def getBestRLscore(self):
        best = max(self.getRLscores())
        select = self.getRLscores().index(best)
        return select
    
    def updateRLscore(self, index, value):
        self.getRLscores()[index] += value
        
    def resetRLscores(self, operators):
        self.__RL_scores = [round(np.random.random(), 2) for x in range(operators)]

    #Indirect solution method
    def SwapTrack(self):
        session = np.random.randint(self.getProblem().getNumberOfSessions(), size = 2)
        room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        while (session[0] == session[1] and room[0] == room[1]) or self.getSolution().getSolTracks()[session[0]][room[0]] + self.getSolution().getSolTracks()[session[1]][room[1]] == -2:
            session = np.random.randint(self.getProblem().getNumberOfSessions(), size = 2)
            room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        self.getSolution().getSolTracks()[session[0]][room[0]], self.getSolution().getSolTracks()[session[1]][room[1]] = self.getSolution().getSolTracks()[session[1]][room[1]], self.getSolution().getSolTracks()[session[0]][room[0]]

    def InsertTrack(self):
        session = np.random.randint(self.getProblem().getNumberOfSessions())
        room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        temp = self.getSolution().getSolTracks()[session][room[0]]
        del self.getSolution().getSolTracks()[session][room[0]]
        self.getSolution().getSolTracks()[session].insert(room[1], temp)
        
    def SwapSubmission(self):
        track = np.random.randint(len(self.getSolution().getIndSolSubmissions()))
        submissions = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        while (submissions[0] == submissions[1]) or (len(self.getSolution().getIndSolSubmissions()[track])) < 2:
            track = np.random.randint(len(self.getSolution().getIndSolSubmissions()))
            submissions = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        self.getSolution().getIndSolSubmissions()[track][submissions[0]], self.getSolution().getIndSolSubmissions()[track][submissions[1]] = self.getSolution().getIndSolSubmissions()[track][submissions[1]], self.getSolution().getIndSolSubmissions()[track][submissions[0]]
        
    def SwapSubmission2(self):
        track = np.random.randint(len(self.getSolution().getIndSolSubmissions()))
        submissions = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        while (submissions[0] == submissions[1]) or (len(self.getSolution().getIndSolSubmissions()[track])) < 2:
            track = np.random.randint(len(self.getSolution().getIndSolSubmissions()))
            submissions = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        if self.getSolution().getIndSolSubmissions()[track][submissions[0]] != -1:
            ts0 = self.getProblem().getSubmission(self.getSolution().getIndSolSubmissions()[track][submissions[0]]).getRequiredTimeSlots()
        else:
            ts0 = 0
        if self.getSolution().getIndSolSubmissions()[track][submissions[1]] != -1:
            ts1 = self.getProblem().getSubmission(self.getSolution().getIndSolSubmissions()[track][submissions[1]]).getRequiredTimeSlots()
        else:
            ts1 = 0
        if ts0 + ts1 <= 2:
            self.getSolution().getIndSolSubmissions()[track][submissions[0]], self.getSolution().getIndSolSubmissions()[track][submissions[1]] = self.getSolution().getIndSolSubmissions()[track][submissions[1]], self.getSolution().getIndSolSubmissions()[track][submissions[0]]
    
    def InsertSubmission(self):
        track = np.random.randint(len(self.getSolution().getIndSolSubmissions()))
        while len(self.getSolution().getIndSolSubmissions()[track]) < 2:
            track = np.random.randint(len(self.getSolution().getIndSolSubmissions()))
        submissions = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        while submissions[0] == submissions[1]:
            submissions = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        temp = self.getSolution().getIndSolSubmissions()[track][submissions[0]]
        del self.getSolution().getIndSolSubmissions()[track][submissions[0]]
        self.getSolution().getIndSolSubmissions()[track].insert(submissions[1], temp)
        
    def InsertSubmission2(self):
        track = np.random.randint(len(self.getSolution().getIndSolSubmissions()))
        while len(self.getSolution().getIndSolSubmissions()[track]) < 2:
            track = np.random.randint(len(self.getSolution().getIndSolSubmissions()))
        submissions = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        while submissions[0] == submissions[1]:
            submissions = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        if self.getSolution().getIndSolSubmissions()[track][submissions[0]] != -1:
            ts0 = self.getProblem().getSubmission(self.getSolution().getIndSolSubmissions()[track][submissions[0]]).getRequiredTimeSlots()
        else:
            ts0 = 0
        if self.getSolution().getIndSolSubmissions()[track][submissions[1]] != -1:
            ts1 = self.getProblem().getSubmission(self.getSolution().getIndSolSubmissions()[track][submissions[1]]).getRequiredTimeSlots()
        else:
            ts1 = 0
        if ts0 + ts1 <= 2:
            temp = self.getSolution().getIndSolSubmissions()[track][submissions[0]]
            del self.getSolution().getIndSolSubmissions()[track][submissions[0]]
            self.getSolution().getIndSolSubmissions()[track].insert(submissions[1], temp)
        elif ts0 > 1:
            temp = self.getSolution().getIndSolSubmissions()[track][submissions[0]]
            while temp in self.getSolution().getIndSolSubmissions()[track]:
                self.getSolution().getIndSolSubmissions()[track].remove(temp)
            for i in range(self.getProblem().getSubmission(temp).getRequiredTimeSlots()):
                self.getSolution().getIndSolSubmissions()[track].insert(submissions[1], temp)
        elif ts1 > 1:
            temp = self.getSolution().getIndSolSubmissions()[track][submissions[1]]
            while temp in self.getSolution().getIndSolSubmissions()[track]:
                self.getSolution().getIndSolSubmissions()[track].remove(temp)
            for i in range(self.getProblem().getSubmission(temp).getRequiredTimeSlots()):
                self.getSolution().getIndSolSubmissions()[track].insert(submissions[0], temp)
        else:
            temp0 = self.getSolution().getIndSolSubmissions()[track][submissions[0]]
            temp1 = self.getSolution().getIndSolSubmissions()[track][submissions[1]]
            while temp0 in self.getSolution().getIndSolSubmissions()[track]:
                self.getSolution().getIndSolSubmissions()[track].remove(temp0)
            while temp1 in self.getSolution().getIndSolSubmissions()[track]:
                self.getSolution().getIndSolSubmissions()[track].remove(temp1)
            for i in range(self.getProblem().getSubmission(temp0).getRequiredTimeSlots()):
                self.getSolution().getIndSolSubmissions()[track].insert(submissions[1], temp0)
            for i in range(self.getProblem().getSubmission(temp1).getRequiredTimeSlots()):
                self.getSolution().getIndSolSubmissions()[track].insert(submissions[0], temp1)
    
    def K_Swap(self):
        k = np.random.randint(2,5)
        for i in range(k):
            self.SwapTrack()
            
    def ConvertSolFirstTime(self):
        subs_ts = {str(sub): 0 for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getRequiredTimeSlots() == 1}
        index = {str(track): 0 for track in range(self.getProblem().getNumberOfTracks())}
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            if (self.getProblem().getSubmission(sub).getRequiredTimeSlots() != 1) and (sub in self.getSolution().getIndSolSubmissions()[self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getTrack().getName())]):
                self.getSolution().getIndSolSubmissions()[self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getTrack().getName())].remove(sub)
        for session in range(len(self.getSolution().getSolTracks())):
            for room in range(len(self.getSolution().getSolTracks()[session])):
                if self.getSolution().getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolution().getSolSubmissions()[session][room])):
                        if (index[str(self.getSolution().getSolTracks()[session][room])] <= len(self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[session][room]]) - 1) and (self.getSolution().getSolSubmissions()[session][room][ts] == -1):
                            self.getSolution().getSolSubmissions()[session][room][ts] = self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[session][room]][index[str(self.getSolution().getSolTracks()[session][room])]]
                            subs_ts[str(self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[session][room]][index[str(self.getSolution().getSolTracks()[session][room])]])] += 1
                            if self.getProblem().getSubmission(self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[session][room]][index[str(self.getSolution().getSolTracks()[session][room])]]).getRequiredTimeSlots() == subs_ts[str(self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[session][room]][index[str(self.getSolution().getSolTracks()[session][room])]])]:
                                index[str(self.getSolution().getSolTracks()[session][room])] += 1
        #Creating Ind sol
        temp = [[] for i in range(self.getProblem().getNumberOfTracks())]
        for i in range(len(self.getSolution().getSolTracks())):
            for j in range(len(self.getSolution().getSolTracks()[i])):
                if self.getSolution().getSolTracks()[i][j] != -1:
                    for x in range(len(self.getSolution().getSolSubmissions()[i][j])):
                        temp[self.getSolution().getSolTracks()[i][j]].append(self.getSolution().getSolSubmissions()[i][j][x])
        self.getSolution().setIndSolSubmissions(temp)
    
    def ConvertSol(self):
        subs_ts = {str(sub): 0 for sub in range(self.getProblem().getNumberOfSubmissions())}
        index = {str(track): 0 for track in range(self.getProblem().getNumberOfTracks())}
        for session in range(len(self.getSolution().getSolTracks())):
            for room in range(len(self.getSolution().getSolTracks()[session])):
                if self.getSolution().getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolution().getSolSubmissions()[session][room])):
                        if index[str(self.getSolution().getSolTracks()[session][room])] <= len(self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[session][room]]) - 1:
                            self.getSolution().getSolSubmissions()[session][room][ts] = self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[session][room]][index[str(self.getSolution().getSolTracks()[session][room])]]
                            subs_ts[str(self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[session][room]][index[str(self.getSolution().getSolTracks()[session][room])]])] += 1
                            if self.getProblem().getSubmission(self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[session][room]][index[str(self.getSolution().getSolTracks()[session][room])]]).getRequiredTimeSlots() == subs_ts[str(self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[session][room]][index[str(self.getSolution().getSolTracks()[session][room])]])]:
                                index[str(self.getSolution().getSolTracks()[session][room])] += 1

    def ConvertSol2(self):
        index = {str(track): 0 for track in range(self.getProblem().getNumberOfTracks())}
        for i in range(len(self.getSolution().getSolTracks())):
            for j in range(len(self.getSolution().getSolTracks()[i])):
                if self.getSolution().getSolTracks()[i][j] != -1:
                    for x in range(len(self.getSolution().getSolSubmissions()[i][j])):
                        if index[str(self.getSolution().getSolTracks()[i][j])] <= len(self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[i][j]]) - 1:
                            self.getSolution().getSolSubmissions()[i][j][x] = self.getSolution().getIndSolSubmissions()[self.getSolution().getSolTracks()[i][j]][index[str(self.getSolution().getSolTracks()[i][j])]]
                            index[str(self.getSolution().getSolTracks()[i][j])] += 1

    def copyWholeSolution(self):
        copy_solTracks = []
        copy_solSubmissions = []
        for i in range(len(self.getSolution().getSolTracks())):
            temp = []
            temp3 = []
            for j in range(len(self.getSolution().getSolTracks()[i])):
                temp.append(self.getSolution().getSolTracks()[i][j])
                temp2 = []
                for z in range(len(self.getSolution().getSolSubmissions()[i][j])):
                    temp2.append(self.getSolution().getSolSubmissions()[i][j][z])
                temp3.append(temp2)
            copy_solTracks.append(temp)
            copy_solSubmissions.append(temp3)
        copy_indsol = []
        for i in range(len(self.getSolution().getIndSolSubmissions())):
            temp = []
            for j in range(len(self.getSolution().getIndSolSubmissions()[i])):
                temp.append(self.getSolution().getIndSolSubmissions()[i][j])
            copy_indsol.append(temp)
        return copy_solTracks, copy_solSubmissions, copy_indsol
    
    #Direct Method
    def LLH_SwapTrack(self):
        session = np.random.randint(self.getProblem().getNumberOfSessions(), size = 2)
        room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        while (session[0] == session[1] and room[0] == room[1]) or (self.getSolution().getSolTracks()[session[0]][room[0]] + self.getSolution().getSolTracks()[session[1]][room[1]] == -2):
            session = np.random.randint(self.getProblem().getNumberOfSessions(), size = 2)
            room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        if self.getProblem().getSession(session[0]).getMaxTimeSlots() == self.getProblem().getSession(session[1]).getMaxTimeSlots():
            self.getSolution().getSolTracks()[session[0]][room[0]], self.getSolution().getSolTracks()[session[1]][room[1]] = self.getSolution().getSolTracks()[session[1]][room[1]], self.getSolution().getSolTracks()[session[0]][room[0]]
            self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]] = self.getSolution().getSolSubmissions()[session[1]][room[1]], self.getSolution().getSolSubmissions()[session[0]][room[0]]
        elif (len(self.getSolution().getSolSubmissions()[session[0]][room[0]]) - self.getSolution().getSolSubmissions()[session[0]][room[0]].count(-1) <= self.getProblem().getSession(session[1]).getMaxTimeSlots()) and (len(self.getSolution().getSolSubmissions()[session[1]][room[1]]) - self.getSolution().getSolSubmissions()[session[1]][room[1]].count(-1) <= self.getProblem().getSession(session[0]).getMaxTimeSlots()):
            self.getSolution().getSolTracks()[session[0]][room[0]], self.getSolution().getSolTracks()[session[1]][room[1]] = self.getSolution().getSolTracks()[session[1]][room[1]], self.getSolution().getSolTracks()[session[0]][room[0]]
            self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]] = self.getSolution().getSolSubmissions()[session[1]][room[1]], self.getSolution().getSolSubmissions()[session[0]][room[0]]
            temp = [self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]]]
            for i in range(len(temp)):
                while len(temp[i]) != self.getProblem().getSession(session[i]).getMaxTimeSlots():
                    if len(temp[i]) < self.getProblem().getSession(session[i]).getMaxTimeSlots():
                        temp[i].insert(len(temp[i]), -1)
                    else:
                        temp[i].remove(-1)
                        
    def LLH_LSwapTrack(self, indexes):
        s1 = indexes[0]
        r1 = indexes[1]
        s2 = np.random.randint(self.getProblem().getNumberOfSessions())
        r2 = np.random.randint(self.getProblem().getNumberOfRooms())
        while (s1 == s2 and r1 == r2):
            s2 = np.random.randint(self.getProblem().getNumberOfSessions())
            r2 = np.random.randint(self.getProblem().getNumberOfRooms())
        session = [s1, s2]
        room = [r1, r2]
        if self.getProblem().getSession(session[0]).getMaxTimeSlots() == self.getProblem().getSession(session[1]).getMaxTimeSlots():
            self.getSolution().getSolTracks()[session[0]][room[0]], self.getSolution().getSolTracks()[session[1]][room[1]] = self.getSolution().getSolTracks()[session[1]][room[1]], self.getSolution().getSolTracks()[session[0]][room[0]]
            self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]] = self.getSolution().getSolSubmissions()[session[1]][room[1]], self.getSolution().getSolSubmissions()[session[0]][room[0]]
        elif (len(self.getSolution().getSolSubmissions()[session[0]][room[0]]) - self.getSolution().getSolSubmissions()[session[0]][room[0]].count(-1) <= self.getProblem().getSession(session[1]).getMaxTimeSlots()) and (len(self.getSolution().getSolSubmissions()[session[1]][room[1]]) - self.getSolution().getSolSubmissions()[session[1]][room[1]].count(-1) <= self.getProblem().getSession(session[0]).getMaxTimeSlots()):
            self.getSolution().getSolTracks()[session[0]][room[0]], self.getSolution().getSolTracks()[session[1]][room[1]] = self.getSolution().getSolTracks()[session[1]][room[1]], self.getSolution().getSolTracks()[session[0]][room[0]]
            self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]] = self.getSolution().getSolSubmissions()[session[1]][room[1]], self.getSolution().getSolSubmissions()[session[0]][room[0]]
            temp = [self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]]]
            for i in range(len(temp)):
                while len(temp[i]) != self.getProblem().getSession(session[i]).getMaxTimeSlots():
                    if len(temp[i]) < self.getProblem().getSession(session[i]).getMaxTimeSlots():
                        temp[i].insert(len(temp[i]), -1)
                    else:
                        temp[i].remove(-1)
                        
    def LLH_LSwapTrack2(self, indexes):
        s1 = indexes[0]
        r1 = indexes[1]
        s2 = 0
        r2 = 0
        if self.getProblem().getTrack(self.getSolution().getSolTracks()[s1][r1]).getRequiredTimeSlots() > self.getProblem().getLargestSession():
            l = [[i, self.getSolution().getSolTracks()[i].index(self.getSolution().getSolTracks()[s1][r1])] for i in range(len(self.getSolution().getSolTracks())) if self.getSolution().getSolTracks()[s1][r1] in self.getSolution().getSolTracks()[i]]
            np.random.shuffle(l)
            for i in l:
                if [s1,r1] != i:
                    s2 = i[0]
                    r2 = i[1]
                    break
        else:
            l = [[i, self.getSolution().getSolTracks()[i].index(-1)] for i in range(len(self.getSolution().getSolTracks())) if -1 in self.getSolution().getSolTracks()[i]]
            np.random.shuffle(l)
            for i in l:
                if i[0] != s1:
                    s2 = i[0]
                    r2 = i[1]
                    break
            #Split the track
            session = [s1, s2]
            room = [r1, r2]
            rn = np.random.rand()
            if rn > 0.5:
                track = self.getSolution().getSolTracks()[s1][r1]
                self.getSolution().getSolTracks()[s2][r2] = track
                sub1 = self.getSolution().getSolSubmissions()[s1][r1][len(self.getSolution().getSolSubmissions()[s1][r1])-1]
                sub2 = self.getSolution().getSolSubmissions()[s1][r1][len(self.getSolution().getSolSubmissions()[s1][r1])-2]
                self.getSolution().getSolSubmissions()[s2][r2][0] = sub1
                self.getSolution().getSolSubmissions()[s2][r2][1] = sub2
                self.getSolution().getSolSubmissions()[s1][r1][len(self.getSolution().getSolSubmissions()[s1][r1])-1] = -1
                self.getSolution().getSolSubmissions()[s1][r1][len(self.getSolution().getSolSubmissions()[s1][r1])-2] = -1
                return
        session = [s1, s2]
        room = [r1, r2]
        if self.getProblem().getSession(session[0]).getMaxTimeSlots() == self.getProblem().getSession(session[1]).getMaxTimeSlots():
            self.getSolution().getSolTracks()[session[0]][room[0]], self.getSolution().getSolTracks()[session[1]][room[1]] = self.getSolution().getSolTracks()[session[1]][room[1]], self.getSolution().getSolTracks()[session[0]][room[0]]
            self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]] = self.getSolution().getSolSubmissions()[session[1]][room[1]], self.getSolution().getSolSubmissions()[session[0]][room[0]]
        elif (len(self.getSolution().getSolSubmissions()[session[0]][room[0]]) - self.getSolution().getSolSubmissions()[session[0]][room[0]].count(-1) <= self.getProblem().getSession(session[1]).getMaxTimeSlots()) and (len(self.getSolution().getSolSubmissions()[session[1]][room[1]]) - self.getSolution().getSolSubmissions()[session[1]][room[1]].count(-1) <= self.getProblem().getSession(session[0]).getMaxTimeSlots()):
            self.getSolution().getSolTracks()[session[0]][room[0]], self.getSolution().getSolTracks()[session[1]][room[1]] = self.getSolution().getSolTracks()[session[1]][room[1]], self.getSolution().getSolTracks()[session[0]][room[0]]
            self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]] = self.getSolution().getSolSubmissions()[session[1]][room[1]], self.getSolution().getSolSubmissions()[session[0]][room[0]]
            temp = [self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]]]
            for i in range(len(temp)):
                while len(temp[i]) != self.getProblem().getSession(session[i]).getMaxTimeSlots():
                    if len(temp[i]) < self.getProblem().getSession(session[i]).getMaxTimeSlots():
                        temp[i].insert(len(temp[i]), -1)
                    else:
                        temp[i].remove(-1)
                        
    def LLH_SwapTrackSameSession(self):
        session = np.random.randint(self.getProblem().getNumberOfSessions())
        room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        while (room[0] == room[1]) or (self.getSolution().getSolTracks()[session][room[0]] + self.getSolution().getSolTracks()[session][room[1]] == -2):
            session = np.random.randint(self.getProblem().getNumberOfSessions())
            room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        self.getSolution().getSolTracks()[session][room[0]], self.getSolution().getSolTracks()[session][room[1]] = self.getSolution().getSolTracks()[session][room[1]], self.getSolution().getSolTracks()[session][room[0]]
        self.getSolution().getSolSubmissions()[session][room[0]], self.getSolution().getSolSubmissions()[session][room[1]] = self.getSolution().getSolSubmissions()[session][room[1]], self.getSolution().getSolSubmissions()[session][room[0]]
        
    def LLH_LSwapTrackSameSession(self, indexes):
        session = indexes[0]
        r1 = np.random.randint(self.getProblem().getNumberOfRooms())
        r2 = indexes[1]
        while (r1 == r2):
            r1 = np.random.randint(self.getProblem().getNumberOfRooms())
        room = [r1, r2]
        self.getSolution().getSolTracks()[session][room[0]], self.getSolution().getSolTracks()[session][room[1]] = self.getSolution().getSolTracks()[session][room[1]], self.getSolution().getSolTracks()[session][room[0]]
        self.getSolution().getSolSubmissions()[session][room[0]], self.getSolution().getSolSubmissions()[session][room[1]] = self.getSolution().getSolSubmissions()[session][room[1]], self.getSolution().getSolSubmissions()[session][room[0]]
            
    def LLH_SwapSubmission(self):
        session = np.random.randint(self.getProblem().getNumberOfSessions())
        room = np.random.randint(self.getProblem().getNumberOfRooms())
        position = np.random.randint(len(self.getSolution().getSolSubmissions()[session][room]), size = 2)
        while (position[0] == position[1]) or (self.getSolution().getSolSubmissions()[session][room].count(-1) == len(self.getSolution().getSolSubmissions()[session][room])):
            session = np.random.randint(self.getProblem().getNumberOfSessions())
            room = np.random.randint(self.getProblem().getNumberOfRooms())
            position = np.random.randint(len(self.getSolution().getSolSubmissions()[session][room]), size = 2)
        self.getSolution().getSolSubmissions()[session][room][position[0]], self.getSolution().getSolSubmissions()[session][room][position[1]] = self.getSolution().getSolSubmissions()[session][room][position[1]], self.getSolution().getSolSubmissions()[session][room][position[0]]
                      
    def LLH_LSwapSubmission(self, indexes):
        session = indexes[0]
        room = indexes[1]
        ts1 = np.random.randint(len(self.getSolution().getSolSubmissions()[session][room]))
        ts2 = indexes[2]
        while (ts1 == ts2):
            ts1 = np.random.randint(len(self.getSolution().getSolSubmissions()[session][room]))
        position = [ts1, ts2]
        self.getSolution().getSolSubmissions()[session][room][position[0]], self.getSolution().getSolSubmissions()[session][room][position[1]] = self.getSolution().getSolSubmissions()[session][room][position[1]], self.getSolution().getSolSubmissions()[session][room][position[0]]
    
    def LLH_SwapSubmissionSession(self):
        track = np.random.randint(self.getProblem().getNumberOfTracks())
        while self.getProblem().getTrack(track).getRequiredTimeSlots() <= self.getProblem().getLargestSession():
            track = np.random.randint(self.getProblem().getNumberOfTracks())
        sessions = []
        for session in range(len(self.getSolution().getSolTracks())):
            if track in self.getSolution().getSolTracks()[session]:
                sessions.append(session)
        if len(sessions) > 1:
            np.random.shuffle(sessions)
            room0 = self.getSolution().getSolTracks()[sessions[0]].index(track)
            room1 = self.getSolution().getSolTracks()[sessions[1]].index(track)
            position0 = np.random.randint(len(self.getSolution().getSolSubmissions()[sessions[0]][room0]))
            position1 = np.random.randint(len(self.getSolution().getSolSubmissions()[sessions[1]][room1]))
            if self.getSolution().getSolSubmissions()[sessions[0]][room0][position0] != -1:
                ts0 = self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[sessions[0]][room0][position0]).getRequiredTimeSlots()
            else:
                ts0 = 0
            if self.getSolution().getSolSubmissions()[sessions[1]][room1][position1] != -1:
                ts1 = self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[sessions[1]][room1][position1]).getRequiredTimeSlots()
            else:
                ts1 = 0
            if ts0 + ts1 <= 2:
                self.getSolution().getSolSubmissions()[sessions[0]][room0][position0], self.getSolution().getSolSubmissions()[sessions[1]][room1][position1] = self.getSolution().getSolSubmissions()[sessions[1]][room1][position1], self.getSolution().getSolSubmissions()[sessions[0]][room0][position0]
                if self.getSolution().getSolSubmissions()[sessions[0]][room0][position0] == -1:
                    del self.getSolution().getSolSubmissions()[sessions[0]][room0][position0]
                    self.getSolution().getSolSubmissions()[sessions[0]][room0].insert(len(self.getSolution().getSolSubmissions()[sessions[0]][room0]), -1)
                elif self.getSolution().getSolSubmissions()[sessions[1]][room1][position1] == -1:
                    del self.getSolution().getSolSubmissions()[sessions[1]][room1][position1]
                    self.getSolution().getSolSubmissions()[sessions[1]][room1].insert(len(self.getSolution().getSolSubmissions()[sessions[1]][room1]), -1)
            elif (len(self.getSolution().getSolSubmissions()[sessions[0]][room0]) == len(self.getSolution().getSolSubmissions()[sessions[1]][room1])):
                self.getSolution().getSolSubmissions()[sessions[0]][room0], self.getSolution().getSolSubmissions()[sessions[1]][room1] = self.getSolution().getSolSubmissions()[sessions[1]][room1], self.getSolution().getSolSubmissions()[sessions[0]][room0]
                
    def LLH_LSwapSubmissionSession(self, indexes):
        index = indexes
        track = self.getSolution().getSolTracks()[index[0]][index[1]]
        if self.getProblem().getTrack(track).getRequiredTimeSlots() <= self.getProblem().getLargestSession():
            return
        sessions = []
        for session in range(len(self.getSolution().getSolTracks())):
            if track in self.getSolution().getSolTracks()[session]:
                sessions.append(session)
        if len(sessions) > 1:
            np.random.shuffle(sessions)
            sessions[0] = index[0]
            room0 = index[1]
            room1 = self.getSolution().getSolTracks()[sessions[1]].index(track)
            position0 = index[2]
            position1 = np.random.randint(len(self.getSolution().getSolSubmissions()[sessions[1]][room1]))
            if self.getSolution().getSolSubmissions()[sessions[0]][room0][position0] != -1:
                ts0 = self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[sessions[0]][room0][position0]).getRequiredTimeSlots()
            else:
                ts0 = 0
            if self.getSolution().getSolSubmissions()[sessions[1]][room1][position1] != -1:
                ts1 = self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[sessions[1]][room1][position1]).getRequiredTimeSlots()
            else:
                ts1 = 0
            if ts0 + ts1 <= 2:
                self.getSolution().getSolSubmissions()[sessions[0]][room0][position0], self.getSolution().getSolSubmissions()[sessions[1]][room1][position1] = self.getSolution().getSolSubmissions()[sessions[1]][room1][position1], self.getSolution().getSolSubmissions()[sessions[0]][room0][position0]
                if self.getSolution().getSolSubmissions()[sessions[0]][room0][position0] == -1:
                    del self.getSolution().getSolSubmissions()[sessions[0]][room0][position0]
                    self.getSolution().getSolSubmissions()[sessions[0]][room0].insert(len(self.getSolution().getSolSubmissions()[sessions[0]][room0]), -1)
                elif self.getSolution().getSolSubmissions()[sessions[1]][room1][position1] == -1:
                    del self.getSolution().getSolSubmissions()[sessions[1]][room1][position1]
                    self.getSolution().getSolSubmissions()[sessions[1]][room1].insert(len(self.getSolution().getSolSubmissions()[sessions[1]][room1]), -1)
            else:
                temp0 = self.getSolution().getSolSubmissions()[sessions[0]][room0][position0]
                temp1 = self.getSolution().getSolSubmissions()[sessions[1]][room1][position1]
                for i in range(len(self.getSolution().getSolSubmissions()[sessions[0]][room0])):
                    if self.getSolution().getSolSubmissions()[sessions[0]][room0][i] == temp0:
                        self.getSolution().getSolSubmissions()[sessions[0]][room0][i] = -1
                for i in range(len(self.getSolution().getSolSubmissions()[sessions[1]][room1])):
                    if self.getSolution().getSolSubmissions()[sessions[1]][room1][i] == temp1:
                        self.getSolution().getSolSubmissions()[sessions[1]][room1][i] = -1
                if (self.getProblem().getSubmission(temp1).getRequiredTimeSlots() <= self.getSolution().getSolSubmissions()[sessions[0]][room0].count(-1)) and (self.getProblem().getSubmission(temp0).getRequiredTimeSlots() <= self.getSolution().getSolSubmissions()[sessions[1]][room1].count(-1)):
                    for i in range(len(self.getSolution().getSolSubmissions()[sessions[0]][room0])):
                        if self.getSolution().getSolSubmissions()[sessions[0]][room0][i] == -1:
                            self.getSolution().getSolSubmissions()[sessions[0]][room0][i] = temp1
                            if self.getSolution().getSolSubmissions()[sessions[0]][room0].count(temp1) == self.getProblem().getSubmission(temp1).getRequiredTimeSlots():
                                break
                    for i in range(len(self.getSolution().getSolSubmissions()[sessions[1]][room1])):
                        if self.getSolution().getSolSubmissions()[sessions[1]][room1][i] == -1:
                            self.getSolution().getSolSubmissions()[sessions[1]][room1][i] = temp0
                            if self.getSolution().getSolSubmissions()[sessions[1]][room1].count(temp0) == self.getProblem().getSubmission(temp0).getRequiredTimeSlots():
                                break
      
    def LLH_KSwap(self):
        k = np.random.randint(2,5)
        for i in range(k):
            self.LLH_SwapTrack()
             
    #Random Hyper-Heuristic
    def RHH(self, start_time, run_time):
        print('-------- RHH initiated --------')
        LLHS = [lambda: self.LLH_SwapTrack(), lambda: self.LLH_SwapTrackSameSession(), lambda: self.LLH_SwapSubmission(), lambda: self.LLH_SwapSubmissionSession(), lambda: self.LLH_KSwap()]
        obj = self.getSolution().EvaluateSolution()
        i = 0
        calls = [0,0,0,0,0]
        successes = [0,0,0,0,0]
        data = []
        while time() - start_time < run_time:
            i += 1
            select = np.random.randint(len(LLHS))
            calls[select] += 1
            sol_copy = self.copyWholeSolution()
            LLHS[select]()
            obj_new = self.getSolution().QEvaluateSolution(obj)
            if obj_new < obj:
                successes[select] += 1
            if obj_new <= obj:
                obj = obj_new
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
        print('Number of iterations:', i)
        print('LLH_SwapTrack: ', successes[0], '//', calls[0])
        print('LLH_SwapTrackSameSession: ', successes[1], '//', calls[1])
        print('LLH_SwapSubmission: ', successes[2], '//', calls[2])
        print('LLH_SwapSubmissionSession: ', successes[3], '//', calls[3])
        print('LLH_KSwap: ', successes[4], '//', calls[4])
        for i in range(len(calls)):
            data.append(successes[i])
            data.append(calls[i])
        self.RecordLLHs(data)
        print('-------- RHH completed --------')
        
    def LRHH(self, start_time, run_time):
        LLHS = [lambda: self.LLH_SwapTrack(), lambda: self.LLH_SwapTrackSameSession(), lambda: self.LLH_SwapSubmission(), lambda: self.LLH_SwapSubmissionSession(), lambda: self.LLH_KSwap()]
        LLLHS = [lambda: self.LLH_LSwapTrack(indexes), lambda: self.LLH_LSwapTrackSameSession(indexes), lambda: self.LLH_LSwapSubmission(indexes), lambda: self.LLH_LSwapSubmissionSession(indexes), lambda: self.LLH_LSwapTrack2(indexes)]
        obj = self.getSolution().EvaluateSolution()
        i = 0
        l = 0
        while time() - start_time < run_time:
            i += 1
            select = np.random.randint(len(LLHS))
            sol_copy = self.copyWholeSolution()
            LLHS[select]()
            obj_new = self.getSolution().QEvaluateSolution(obj)
            if obj_new >= obj:
                l += 1
            if obj_new <= obj:
                obj = obj_new
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
            if l > 500:
                for j in range(100):
                    i += 1
                    violations = self.getSolution().LEvaluateSolution()
                    s = np.random.randint(len(violations))
                    feed = self.getSolution().getLEvaluation(violations[s])()
                    if (len(feed) < 2) or (len(feed[0]) == 0):
                        next
                    else:
                        indexes = feed[0][0]
                        selectLLLH = feed[1]
                        select = np.random.randint(len(selectLLLH))
                        sol_copy = self.copyWholeSolution()
                        LLLHS[selectLLLH[select]]()
                        obj_new = self.getSolution().QEvaluateSolution(obj)
                        if obj_new <= obj:
                            obj = obj_new
                        else:
                            self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
                l = 0   
        print('Number of iterations:', i)
    
    #Reinforcement Learning Hyper-Heuristic            
    def RLHH(self, start_time, run_time):
        LLHS = [lambda: self.LLH_SwapTrack(), lambda: self.LLH_SwapTrackSameSession(), lambda: self.LLH_SwapSubmission(), lambda: self.LLH_SwapSubmissionSession(), lambda: self.LLH_KSwap()]
        obj_best = self.getSolution().EvaluateSolution()
        obj = obj_best
        best_Sol = self.copyWholeSolution()
        self.setRLscores(len(LLHS))
        tolerance = len(LLHS) * 250
        fails = 0
        i = 0
        while time() - start_time < run_time:
            i += 1                
            select = self.getBestRLscore()
            sol_copy = self.copyWholeSolution()
            LLHS[select]()
            obj_new = self.getSolution().QEvaluateSolution(obj)
            if obj_new < obj:
                print(obj_new)
                obj = obj_new
                fails = 0
                reward = 5*i #2*i
                self.updateRLscore(select, reward)
                if obj_new < obj_best:
                    obj_best = obj_new
                    best_Sol = self.copyWholeSolution()
            elif fails > tolerance and obj_new < obj * 100:
                obj = obj_new
                self.resetRLscores(len(LLHS))
                fails = 0
            else:
               self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
               fails += 1
               penalty = -i #-i/2
               self.updateRLscore(select, penalty)
        self.getSolution().setBestSolution(best_Sol[0], best_Sol[1])
        print('Number of iterations:', i)
                
    def PureLRHH(self, start_time, run_time):
        LLLHS = [lambda: self.LLH_LSwapTrack(indexes), lambda: self.LLH_LSwapTrackSameSession(indexes), lambda: self.LLH_LSwapSubmission(indexes), lambda: self.LLH_LSwapSubmissionSession(indexes), lambda: self.LLH_LSwapTrack2(indexes)]
        obj = self.getSolution().EvaluateSolution()
        i = 0
        while time() - start_time < run_time:
            i += 1
            violations = self.getSolution().LEvaluateSolution()
            s = np.random.randint(len(violations))
            feed = self.getSolution().getLEvaluation(violations[s])()
            if (len(feed) < 2) or (len(feed[0]) == 0):
                pass
            else:
                indexes = feed[0][0]
                selectLLLH = feed[1]
                select = np.random.randint(len(selectLLLH))
                sol_copy = self.copyWholeSolution()
                LLLHS[selectLLLH[select]]()
                obj_new = self.getSolution().QEvaluateSolution(obj)
                if obj_new <= obj:
                    obj = obj_new
                    print(obj)
                else:
                    self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
                
        print('Number of iterations:', i)
    
    #Random Hyper-Heuristic
    def iRHH(self, start_time, run_time):
        print('-------- iRHH initiated --------')
        LLHS = [lambda: self.K_Swap(), lambda: self.SwapTrack(), lambda: self.InsertTrack(),lambda: self.SwapSubmission2(), lambda: self.InsertSubmission2()]
        obj = self.getSolution().EvaluateSolution()
        i = 0
        while time() - start_time < run_time:
            i += 1
            select = np.random.randint(len(LLHS))
            sol_copy = self.copyWholeSolution()
            LLHS[select]()
            self.getSolution().resetSolSubmissions()
            self.ConvertSol2()
            if self.getSolution().EvaluateAllSubmissionsScheduled() == True:
                obj_new = self.getSolution().QEvaluateSolution(obj)
                if obj_new <= obj:
                    obj = obj_new
                else:
                    self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
        print('Number of iterations:', i)
        print('-------- RHH completed --------')
        
    def iLRHH(self, start_time, run_time):
        print('-------- iRHH initiated --------')
        LLHS = [lambda: self.K_Swap(), lambda: self.SwapTrack(), lambda: self.InsertTrack(),lambda: self.SwapSubmission2(), lambda: self.InsertSubmission2()]
        LLLHS = [lambda: self.LLH_LSwapTrack(indexes), lambda: self.LLH_LSwapTrackSameSession(indexes), lambda: self.LLH_LSwapSubmission(indexes), lambda: self.LLH_LSwapSubmissionSession(indexes), lambda: self.LLH_LSwapTrack2(indexes)]
        obj = self.getSolution().EvaluateSolution()
        i = 0
        l = 0
        while time() - start_time < run_time:
            i += 1
            l += 1
            select = np.random.randint(len(LLHS))
            sol_copy = self.copyWholeSolution()
            LLHS[select]()
            self.getSolution().resetSolSubmissions()
            self.ConvertSol2()
            if self.getSolution().EvaluateAllSubmissionsScheduled() == True:
                obj_new = self.getSolution().QEvaluateSolution(obj)
                if obj_new <= obj:
                    obj = obj_new
                else:
                    self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
            if l > 1000:
                for j in range(100):
                    i += 1
                    violations = self.getSolution().LEvaluateSolution()
                    s = np.random.randint(len(violations))
                    feed = self.getSolution().getLEvaluation(violations[s])()
                    if (len(feed) < 2) or (len(feed[0]) == 0):
                        pass
                    else:
                        indexes = feed[0][0]
                        selectLLLH = feed[1]
                        select = np.random.randint(len(selectLLLH))
                        sol_copy = self.copyWholeSolution()
                        LLLHS[selectLLLH[select]]()
                        obj_new = self.getSolution().QEvaluateSolution(obj)
                        if obj_new <= obj:
                            obj = obj_new
                        else:
                            self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
                l = 0
        print('Number of iterations:', i)
        print('-------- RHH completed --------')
    
    #Reinforcement Learning Hyper-Heuristic           
    def iRLHH(self, start_time, run_time):
        LLHS = [lambda: self.SwapTrack(), lambda: self.InsertTrack(),lambda: self.SwapSubmission(), lambda: self.InsertSubmission()]
        self.setRLscores(len(LLHS))
        obj_best = self.getSolution().EvaluateSolution()
        best_Sol = self.copyWholeSolution()
        tolerance = 5000
        fails = 0
        i = 0
        obj = obj_best
        while time() - start_time < run_time:
            i += 1
            select = self.getBestRLscore()
            sol_copy = self.copyWholeSolution()
            LLHS[select]()
            self.getSolution().resetSolSubmissions()
            self.ConvertSol()
            if self.getSolution().EvaluateAllSubmissionsScheduled() == True:
                if fails > tolerance:
                    obj_new = self.getSolution().EvaluateSolution()
                else:
                    obj_new = self.getSolution().QEvaluateSolution(obj)
                if obj_new < obj_best:
                    best_Sol = self.copyWholeSolution()
                    obj_best = obj_new
                if (obj_new < obj) or ((fails > tolerance) and (obj_new < obj * 2.5) and (obj_new != obj)):
                    print(obj_new)
                    if (fails > tolerance) and ((obj_new < obj * 2.5) and (obj_new != obj)):
                        self.resetRLscores(len(LLHS))
                        tolerance += 1000
                    obj = obj_new
                    fails = 0
                    reward = 5*i
                    self.updateRLscore(select, reward)
                else:
                   self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
                   fails += 1
                   penalty = -i/2
                   self.updateRLscore(select, penalty)
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
        self.getSolution().setBestSolution(best_Sol[0], best_Sol[1])
        print('Number of iterations:', i)
        
    def test(self, start_time, run_time):
        LLHS = [lambda: self.K_Swap(), lambda: self.SwapTrack(), lambda: self.InsertTrack(),lambda: self.SwapSubmission(), lambda: self.InsertSubmission()]
        self.setRLscores(len(LLHS))
        obj_best = self.getSolution().EvaluateSolution()
        best_Sol = self.copyWholeSolution()
        tolerance = 500
        fails = 0
        i = 0
        util = [0,0,0,0,0]
        calls = [0,0,0,0,0]
        obj = obj_best
        while time() - start_time < run_time:
            i += 1
            select = self.getBestRLscore()
            calls[select] += 1
            sol_copy = self.copyWholeSolution()
            LLHS[select]()
            self.getSolution().resetSolSubmissions()
            self.ConvertSol()
            if self.getSolution().EvaluateAllSubmissionsScheduled() == True:
                obj_new = self.getSolution().QEvaluateSolution(obj)
                if obj_new < obj_best:
                    best_Sol = self.copyWholeSolution()
                    obj_best = obj_new
                if obj_new < obj or (fails > tolerance and obj_new < obj * 1.2):
                    if fails > tolerance and obj_new < obj * 1.2:
                        self.resetRLscores(len(LLHS))
                        tolerance += 100
                    obj = obj_new
                    fails = 0
                    reward = 5*i
                    self.updateRLscore(select, reward)
                    util[select] += 1
                else:
                   self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
                   fails += 1
                   penalty = -i/2
                   self.updateRLscore(select, penalty)
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
                penalty = -i/4
                self.updateRLscore(select, penalty)
        self.getSolution().setBestSolution(best_Sol[0], best_Sol[1])
        '''
        print('Number of iterations:', i)
        print('K-Swap: ', round((util[0]/calls[0])*100, 2), '% ', util[0], '/', calls[0])
        print('SwapTrack: ', round((util[1]/calls[1])*100, 2), '% ', util[1], '/', calls[1])
        print('InsertTrack: ', round((util[2]/calls[2])*100, 2), '% ', util[2], '/', calls[2])
        print('SwapSub: ', round((util[3]/calls[3])*100, 2), '% ', util[3], '/', calls[3])
        print('InsertSub: ', round((util[4]/calls[4])*100, 2), '% ', util[4], '/', calls[4])
        '''
    
    #Sequential Random Hyper-Heuristic
    def iseqRHH(self, start_time, run_time):
        LLHS = [lambda: self.SwapTrack(), lambda: self.InsertTrack(),lambda: self.SwapSubmission(), lambda: self.InsertSubmission()]
        obj = self.getSolution().EvaluateSolution()
        select = np.random.randint(2)
        i = 0
        while time() - start_time < run_time:
            i += 1
            sol_copy = self.copyWholeSolution()
            LLHS[select]()
            self.getSolution().resetSolSubmissions()
            self.ConvertSol()
            if self.getSolution().EvaluateAllSubmissionsScheduled() == True:
                obj_new = self.getSolution().QEvaluateSolution(obj)
                if obj_new <= obj:
                    obj = obj_new
                else:
                    self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
            if select < 2:
                select = np.random.randint(2,4)
            else:
                select = np.random.randint(2)
        print('Number of iterations:', i)
    
    #Experimentation stage
    def iRLHHexp(self, start_time, run_time):
        LLHS = [lambda: self.SwapTrack(), lambda: self.InsertTrack(),lambda: self.SwapSubmission(), lambda: self.InsertSubmission()]
        self.setRLscores(len(LLHS))
        obj_best = self.getSolution().EvaluateSolution()
        best_Sol = self.copyWholeSolution()
        obj = obj_best
        tolerance = len(LLHS) * 25
        fails = 0
        i = 0
        stuck = 0
        gap = 1.2
        obj_history = [obj, obj]
        while time() - start_time < run_time:
            i += 1
            select = self.getBestRLscore()
            sol_copy = self.copyWholeSolution()
            LLHS[select]()
            self.getSolution().resetSolSubmissions()
            self.ConvertSol()
            if self.getSolution().EvaluateAllSubmissionsScheduled() == True:
                obj_new = self.getSolution().QEvaluateSolution(obj)
                if obj_new < obj_best:
                    best_Sol = self.copyWholeSolution()
                    obj_best = obj_new
                    obj_history[0] = obj_best
                if obj_new < obj or (fails > tolerance and obj_new < obj * gap):
                    if fails > tolerance and obj_new < obj * gap:
                        self.resetRLscores(len(LLHS))
                        tolerance += 100
                        obj_history[1] = obj_best
                        print('Current best obj:', obj_best)
                        if obj_history[0] == obj_history[1]:
                            stuck += 1
                            if stuck == 2:
                                tolerance -= 100
                                gap += 1
                                stuck = 0
                                print('Unstuck function activated')
                    obj = obj_new
                    fails = 0
                    reward = 5*i
                    self.updateRLscore(select, reward)
                else:
                   self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
                   fails += 1
                   penalty = -i/2
                   self.updateRLscore(select, penalty)
                   gap -= 0.001
                   if gap <= 1.01 or gap >= 2.5:
                       gap = 1.2
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
        self.getSolution().setBestSolution(best_Sol[0], best_Sol[1])
        print('Number of iterations:', i)
          
    def ImproveFeasibility(self):
        LLHS = [lambda: self.SwapSubmission(), lambda: self.InsertSubmission()]
        obj = self.getSolution().EvaluateConsecutiveSubmissions()
        done = False
        while done == False:
            select = np.random.randint(len(LLHS))
            sol_copy = self.copyWholeSolution()
            LLHS[select]()
            self.getSolution().resetSolSubmissions()
            self.ConvertSol()
            if self.getSolution().EvaluateAllSubmissionsScheduled() == True:
                obj_new = self.getSolution().EvaluateConsecutiveSubmissions()
                if obj_new <= obj:
                    obj = obj_new
                    print(obj)
                else:
                    self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
            if obj == 0 and self.getSolution().EvaluateAllSubmissionsScheduled() == True:
                done = True
    
    #Constructive Heuristics [Only compatible with indirect solution method]
    #Guided low level heuristics
    def SwapSession(self, track):
        s = []
        r = []
        for session in range(len(self.getSolution().getSolTracks())):
            if track in self.getSolution().getSolTracks()[session]:
                s.append(session)
                r.append(self.getSolution().getSolTracks()[session].index(track))
        select = np.random.randint(len(s))
        session = np.random.randint(self.getProblem().getNumberOfSessions())
        if len(s) != self.getProblem().getNumberOfSessions():
            while session == s[select]:
                session = np.random.randint(self.getProblem().getNumberOfSessions())
        temp = self.getSolution().getSolTracks()[s[select]][r[select]]
        self.getSolution().getSolTracks()[s[select]][r[select]] = self.getSolution().getSolTracks()[session][r[select]]
        self.getSolution().getSolTracks()[session][r[select]] = temp
        
    def SwapRoom(self, track):
        s = []
        r = []
        for session in range(len(self.getSolution().getSolTracks())):
            if track in self.getSolution().getSolTracks()[session]:
                s.append(session)
                r.append(self.getSolution().getSolTracks()[session].index(track))
        select = np.random.randint(len(s))
        room = np.random.randint(self.getProblem().getNumberOfRooms())
        while room == r[select]:
            room = np.random.randint(self.getProblem().getNumberOfRooms())
        temp = self.getSolution().getSolTracks()[s[select]][r[select]]
        self.getSolution().getSolTracks()[s[select]][r[select]] = self.getSolution().getSolTracks()[s[select]][room]
        self.getSolution().getSolTracks()[s[select]][room] = temp
        
    def SwapSessionRoom(self, track):
        s = []
        r = []
        for session in range(len(self.getSolution().getSolTracks())):
            if track in self.getSolution().getSolTracks()[session]:
                s.append(session)
                r.append(self.getSolution().getSolTracks()[session].index(track))
        select = np.random.randint(len(s))
        session = np.random.randint(self.getProblem().getNumberOfSessions())
        room = np.random.randint(self.getProblem().getNumberOfRooms())
        if len(s) != self.getProblem().getNumberOfSessions():
            while session == s[select]:
                session = np.random.randint(self.getProblem().getNumberOfSessions())
        while room == r[select]:
            room = np.random.randint(self.getProblem().getNumberOfRooms())
        temp = self.getSolution().getSolTracks()[s[select]][r[select]]
        self.getSolution().getSolTracks()[s[select]][r[select]] = self.getSolution().getSolTracks()[session][room]
        self.getSolution().getSolTracks()[session][room] = temp
                           
    #RandomSolTracks() generates a random initial tracks solution
    def RandomSolTracks(self):
        unscheduled_tracks = []
        sessions = []
        for track in range(self.getProblem().getNumberOfTracks()):
            unscheduled_tracks.append(track)
        for session in range(self.getProblem().getNumberOfSessions()):
            sessions.append(session)
        i = 0
        restart = False
        while len(unscheduled_tracks) > 0:
            if restart == True:
                unscheduled_tracks = self.ResetSolTracks()
                restart = False
                i = 0
            i += 1
            np.random.shuffle(unscheduled_tracks)
            np.random.shuffle(sessions)
            track = unscheduled_tracks[0]
            for s in sessions:
                if -1 in self.getSolution().getSolTracks()[s]:
                    session = s
                    break
            for r in range(len(self.getSolution().getSolTracks()[session])):
                if self.getSolution().getSolTracks()[session][r] == -1:
                    room = r
                    break
            if self.getSolution().getSolTracks()[session][room] == -1:
                self.getSolution().getSolTracks()[session][room] = track
                self.getProblem().getTrack(track).subtractTimeSlots(self.getProblem().getSession(session).getMaxTimeSlots())
                if self.getProblem().getTrack(track).getDeltaTimeSlots() == 0:
                    unscheduled_tracks.remove(track)
                    i = 0
            if i > 2 * len(self.getSolution().getSolTracks()) * len(self.getSolution().getSolTracks()[0]):
                restart = True
    
    def ResetSolTracks(self):
        unscheduled_tracks = []
        for track in range(self.getProblem().getNumberOfTracks()):
            unscheduled_tracks.append(track)
            self.getProblem().getTrack(track).resetDeltaTimeSlots()
        self.getSolution().resetSolTracks()
        return unscheduled_tracks
    
    def RandomSol(self):
        temp = [sub for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getRequiredTimeSlots() > 1]
        temp2 = [sub for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getRequiredTimeSlots() == 1]
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
                        if (self.getProblem().getSubmission(sub).getRequiredTimeSlots() <= self.getSolution().getSolSubmissions()[session][room].count(-1) and self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getTrack().getName()) == self.getSolution().getSolTracks()[session][room]) or (self.getProblem().getSubmission(sub).getRequiredTimeSlots() <= self.getSolution().getSolSubmissions()[session][room].count(-1) and self.getSolution().getSolTracks()[session][room] == -1):
                            for ts in range(self.getProblem().getSubmission(sub).getRequiredTimeSlots()):
                                i = self.getSolution().getSolSubmissions()[session][room].index(-1)
                                self.getSolution().getSolSubmissions()[session][room][i] = sub
                            stop = True
                            self.getSolution().getSolTracks()[session][room] = self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getTrack().getName())
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
                        if (self.getProblem().getSubmission(sub).getRequiredTimeSlots() <= self.getSolution().getSolSubmissions()[session][room].count(-1) and self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getTrack().getName()) == self.getSolution().getSolTracks()[session][room]) or (self.getProblem().getSubmission(sub).getRequiredTimeSlots() <= self.getSolution().getSolSubmissions()[session][room].count(-1) and self.getSolution().getSolTracks()[session][room] == -1):
                            i = self.getSolution().getSolSubmissions()[session][room].index(-1)
                            self.getSolution().getSolSubmissions()[session][room][i] = sub
                            stop = True
                            self.getSolution().getSolTracks()[session][room] = self.getProblem().getTrackIndex(self.getProblem().getSubmission(sub).getTrack().getName())
                            
            if self.getSolution().EvaluateAllSubmissionsScheduled() == True:
                done = True
            else:
                self.getSolution().resetSolTracks()
                self.getSolution().resetSolSubmissions()
        
        #Creating Ind sol
        temp = [[] for i in range(self.getProblem().getNumberOfTracks())]
        for i in range(len(self.getSolution().getSolTracks())):
            for j in range(len(self.getSolution().getSolTracks()[i])):
                for x in range(len(self.getSolution().getSolSubmissions()[i][j])):
                    if self.getSolution().getSolSubmissions()[i][j][x] != -1 and self.getSolution().getSolSubmissions()[i][j][x] not in temp[self.getSolution().getSolTracks()[i][j]]:
                        temp[self.getSolution().getSolTracks()[i][j]].append(self.getSolution().getSolSubmissions()[i][j][x])
        self.getSolution().setIndSolSubmissions(temp)
    
    def RecordObjective(self, t1, t2):
        obj = [str(self.getSolution().EvaluateSolution()), str(t1), str(t2)]
        with open('record.csv', 'a', newline = "") as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(obj)
            f_object.close()
            
    def RecordLLHs(self, data):
        with open('record.csv', 'a', newline = "") as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data)
            f_object.close()
    
    def Solve(self, problem, solution, method, run_time = 15):
        if method == 'BasicModel':
            insol = InitialSolution(problem, solution)
            insol.BasicModel()
        elif method == 'AdvancedModel':
            insol = InitialSolution(problem, solution)
            insol.AdvancedModel()
        elif method == 'ApproximationModel':
            insol = InitialSolution(problem, solution)
            insol.ApproximationModel()
        elif method == 'RelaxedModel':
            insol = InitialSolution(problem, solution)
            insol.RelaxedModel()
        elif method == 'iRHH':
            insol = InitialSolution(problem, solution)
            self.RandomSolTracks()
            self.ConvertSol()
            start_time = time()
            self.iRHH(start_time, run_time)
        elif method == 'iRLHH':
            insol = InitialSolution(problem, solution)
            self.RandomSolTracks()
            self.ConvertSol()
            start_time = time()
            self.iRLHH(start_time, run_time)
        elif method == 'iseqRHH':
            insol = InitialSolution(problem, solution)
            self.RandomSolTracks()
            self.ConvertSol()
            start_time = time()
            self.iseqRHH(start_time, run_time)
        elif method == 'test':
            insol = InitialSolution(problem, solution)
            self.getSolution().ReadSolution(file_name = 'N2ORSolution.xlsx')
            #insol.tBIP()
            #self.ConvertSol()
            #self.RandomSol()
            #self.RandomSolTracks()
            #self.ConvertSol()
            #start_time = time()
            #self.iRHH(start_time, run_time)
        elif method == 'MH':
            insol = InitialSolution(problem, solution)
            t = insol.tBIP()
            self.ConvertSolFirstTime()
            start_time = time()
            self.LRHH(start_time, run_time - t) #if using iRHH, then in iRHH use ConvertSol2()
            end_time = round(time() - start_time, 2)
            self.RecordObjective(t, end_time - t)
        else:
            sys.exit(print('Method [', method, '] not found!\nAvailable methods are: BasicModel, AdvancedModel, ApproximationModel, MH, iRHH, RHH'))