# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 14:35:59 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from Problem import *
from Solution import *
import numpy as np
from time import time

class Optimisation:
    def __init__(self, problem, solution):
        self.__problem = problem
        self.__solution = solution
        
    def getProblem(self) -> Problem:
        return self.__problem
    
    def getSolution(self) -> Solution:
        return self.__solution
    
    def LLH_SwapTrack(self):
        session = np.random.randint(self.getProblem().getNumberOfSessions(), size = 2)
        room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        while (session[0] == session[1] and room[0] == room[1]) or (self.getSolution().getSolTracks()[session[0]][room[0]] + self.getSolution().getSolTracks()[session[1]][room[1]] == -2):
            session = np.random.randint(self.getProblem().getNumberOfSessions(), size = 2)
            room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        if self.getProblem().getSession(session[0]).getSessionMaxTimeSlots() == self.getProblem().getSession(session[1]).getSessionMaxTimeSlots():
            self.getSolution().getSolTracks()[session[0]][room[0]], self.getSolution().getSolTracks()[session[1]][room[1]] = self.getSolution().getSolTracks()[session[1]][room[1]], self.getSolution().getSolTracks()[session[0]][room[0]]
            self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]] = self.getSolution().getSolSubmissions()[session[1]][room[1]], self.getSolution().getSolSubmissions()[session[0]][room[0]]
        elif (len(self.getSolution().getSolSubmissions()[session[0]][room[0]]) - self.getSolution().getSolSubmissions()[session[0]][room[0]].count(-1) <= self.getProblem().getSession(session[1]).getSessionMaxTimeSlots()) and (len(self.getSolution().getSolSubmissions()[session[1]][room[1]]) - self.getSolution().getSolSubmissions()[session[1]][room[1]].count(-1) <= self.getProblem().getSession(session[0]).getSessionMaxTimeSlots()):
            self.getSolution().getSolTracks()[session[0]][room[0]], self.getSolution().getSolTracks()[session[1]][room[1]] = self.getSolution().getSolTracks()[session[1]][room[1]], self.getSolution().getSolTracks()[session[0]][room[0]]
            self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]] = self.getSolution().getSolSubmissions()[session[1]][room[1]], self.getSolution().getSolSubmissions()[session[0]][room[0]]
            temp = [self.getSolution().getSolSubmissions()[session[0]][room[0]], self.getSolution().getSolSubmissions()[session[1]][room[1]]]
            for i in range(len(temp)):
                while len(temp[i]) != self.getProblem().getSession(session[i]).getSessionMaxTimeSlots():
                    if len(temp[i]) < self.getProblem().getSession(session[i]).getSessionMaxTimeSlots():
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
        
    def LLH_SwapSubmission(self):
        session = np.random.randint(self.getProblem().getNumberOfSessions())
        room = np.random.randint(self.getProblem().getNumberOfRooms())
        position = np.random.randint(len(self.getSolution().getSolSubmissions()[session][room]), size = 2)
        while (position[0] == position[1]) or (self.getSolution().getSolSubmissions()[session][room].count(-1) == len(self.getSolution().getSolSubmissions()[session][room])):
            session = np.random.randint(self.getProblem().getNumberOfSessions())
            room = np.random.randint(self.getProblem().getNumberOfRooms())
            position = np.random.randint(len(self.getSolution().getSolSubmissions()[session][room]), size = 2)
        self.getSolution().getSolSubmissions()[session][room][position[0]], self.getSolution().getSolSubmissions()[session][room][position[1]] = self.getSolution().getSolSubmissions()[session][room][position[1]], self.getSolution().getSolSubmissions()[session][room][position[0]]
        
    def LLH_SwapSubmissionSession(self):
        track = np.random.randint(self.getProblem().getNumberOfTracks())
        while self.getProblem().getTrack(track).getTrackRequiredTimeSlots() <= self.getProblem().getLargestSessionTimeSlots():
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
                ts0 = self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[sessions[0]][room0][position0]).getSubmissionRequiredTimeSlots()
            else:
                ts0 = 0
            if self.getSolution().getSolSubmissions()[sessions[1]][room1][position1] != -1:
                ts1 = self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[sessions[1]][room1][position1]).getSubmissionRequiredTimeSlots()
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
                
    def LLH_KSwap(self):
        k = np.random.randint(2,5)
        for i in range(k):
            self.LLH_SwapTrack()
    
class HyperHeuristic(Optimisation):
    def __init__(self, problem, solution):
        Optimisation.__init__(self, problem, solution)
        
    def solve(self, start_time, run_time):
        LLHS = [lambda: self.LLH_SwapTrack(), lambda: self.LLH_SwapTrackSameSession(), lambda: self.LLH_SwapSubmission(), lambda: self.LLH_SwapSubmissionSession(), lambda: self.LLH_KSwap()]
        obj = self.getSolution().EvaluateSolution()
        i = 0
        while time() - start_time < run_time:
            i += 1
            select = np.random.randint(len(LLHS))
            sol_copy = self.getSolution().copyWholeSolution()
            LLHS[select]()
            obj_new = self.getSolution().QuickEvaluateSolution(obj)
            if obj_new <= obj:
                obj = obj_new
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
        print('Number of iterations:', i)