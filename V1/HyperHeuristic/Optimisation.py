# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 14:35:59 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from Problem import *
from Solution import *
from pulp import *
import pandas as pd
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
            
    def TracksExactModel(self): 
        model = LpProblem('model', LpMinimize)
        names = []
        add_names = []
        add2_names = []
        product_names = []
        coefficients = {}
        timeslots = {}
        n = {}
        mts_subs = []
        
        #Creating decision variables Ys and Zs
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                for z in range(self.getProblem().getNumberOfTracks()):
                    add_names.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                    timeslots['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()] = self.getProblem().getSession(i).getSessionMaxTimeSlots()
                    coefficients['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()] = 1 + self.getProblem().getParameters().getTracksSessionsPenaltyWeight() * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getTrackName(), self.getProblem().getSession(i).getSessionName()) + self.getProblem().getParameters().getSessionsRoomsPenaltyWeight() * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getSessionName(), self.getProblem().getRoom(j).getRoomName())
            
        #Filter submissions with multiple ts
        for x in range(self.getProblem().getNumberOfSubmissions()):
            if self.getProblem().getSubmission(x).getSubmissionRequiredTimeSlots() > 1:
                mts_subs.append(x)
        
        #Creating decision variables Xs
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                for x in mts_subs:
                    if self.getProblem().getSubmission(x).getSubmissionRequiredTimeSlots() <= self.getProblem().getSession(i).getSessionMaxTimeSlots():
                        names.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getSubmission(x).getSubmissionTrack().getTrackName()+'|'+self.getProblem().getSubmission(x).getSubmissionName())
                        coefficients['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getSubmission(x).getSubmissionTrack().getTrackName()+'|'+self.getProblem().getSubmission(x).getSubmissionName()] = 1
                        n['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getSubmission(x).getSubmissionTrack().getTrackName()+'|'+self.getProblem().getSubmission(x).getSubmissionName()] = self.getProblem().getSubmission(x).getSubmissionRequiredTimeSlots()
        
        #Additional variables to minimise tracks per room [Y Variable]
        for i in range(self.getProblem().getNumberOfTracks()):
            for j in range(self.getProblem().getNumberOfRooms()):
                add2_names.append('|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName())
                coefficients['|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName()] = self.getProblem().getParameters().getTracksRoomsPenaltyWeight() * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(i).getTrackName(), self.getProblem().getRoom(j).getRoomName())
        
        #Creating products of variables for consecutive tracks
        for i in range(self.getProblem().getNumberOfRooms() * self.getProblem().getNumberOfTracks()):
            temp = []
            temp.append(add_names[i])
            for j in range(len(add_names)):
                if add_names[i].split('|')[1] != add_names[j].split('|')[1] and add_names[i].split('|')[2] == add_names[j].split('|')[2] and add_names[i].split('|')[3] == add_names[j].split('|')[3]:
                    temp.append(add_names[j])
            for z in range(len(temp)-1):
                temp2 = temp[z] + temp[z+1]
                product_names.append(temp2)
                coefficients[temp2] = -10
        
        pen = []
        #Creating penalties for tracktrack penalty
        for i in range(self.getProblem().getNumberOfTracks()):
            temp = [i]
            for j in range(i, self.getProblem().getNumberOfTracks()):
                if i != j:
                    if self.getProblem().getTracksTracksPenaltybyIndex(i, j) != 0:
                        temp.append(j)
                if len(temp) > 1:
                    for session in range(self.getProblem().getNumberOfSessions()):
                        pen.append('ptt_|' + str(i) + str(j) + str(session))
                        coefficients['ptt_|' + str(i) + str(j) + str(session)] = 1000 * self.getProblem().getTracksTracksPenaltybyIndex(i, j)
                    temp = [i]
                
        #Creating penalties for min number of rooms per track
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getTrackName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            pen.append('pmrt_|' + str(track))
            coefficients['pmrt_|' + str(track)] = 50
        
        #Creating penalties for parallel tracks
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getSessionName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getTrackName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and track_name == name.split('|')[3]:
                        temp.append(name)
                pen.append('ppt_|' + str(session) + str(track))
                coefficients['ppt_|' + str(session) + str(track)] = 10000
        
        #Creating objective function and binary IP formulation
        variables = LpVariable.dicts('Variables', names, cat = 'Binary')
        add_variables = LpVariable.dicts('AddVariables', add_names, cat = 'Binary')
        add2_variables = LpVariable.dicts('Add2Variables', add2_names, cat = 'Binary')
        product_variables = LpVariable.dicts('ProdVariables', product_names, cat = 'Binary')
        penalties = LpVariable.dicts('Penalties', pen, lowBound = 0, cat = 'Integer')
        obj_function = [add_variables, add2_variables, product_variables, penalties]
        all_names = [add_names, add2_names, product_names, pen]
        model += lpSum([coefficients[i] * obj_function[x][i] for x in range(len(obj_function)) for i in all_names[x]])
        
        #Assign subs with multiple ts
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getTrackName()
            for name in range(len(names)):
                if track_name == names[name].split('|')[3]:
                    temp.append(names[name])
            for session in range(self.getProblem().getNumberOfSessions()):
                session_name = self.getProblem().getSession(session).getSessionName()
                session_max_ts = self.getProblem().getSession(session).getSessionMaxTimeSlots()
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp2 = []
                    room_name = self.getProblem().getRoom(room).getRoomName()
                    for name in temp:
                        if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                            temp2.append(name)
                    for add_name in add_names:
                        if track_name == add_name.split('|')[3] and session_name == add_name.split('|')[1] and room_name == add_name.split('|')[2]:
                            add_var = add_name
                    if len(temp2) != 0:
                        all_constraints.append(lpSum([n[x] * variables[x] for x in temp2]) - session_max_ts * add_variables[add_var])
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0

        #Creating Constraints: All submissions must be scheduled
        all_constraints = []
        for submission in range(len(mts_subs)):
            temp = []
            sub_name = self.getProblem().getSubmission(mts_subs[submission]).getSubmissionName()
            for name in range(len(names)):
                if names[name].split('|')[4] == sub_name:
                    temp.append(names[name])
            all_constraints.append(lpSum([variables[x] for x in temp]))
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
            
        #Creating constraints: Assign tracks with respect to available time slots
        for track in range(self.getProblem().getNumberOfTracks()):
            track_name = self.getProblem().getTrack(track).getTrackName()
            temp = []
            for name in add_names:
                if track_name == name.split('|')[3]:
                    temp.append(name)
            model += lpSum([timeslots[x] * add_variables[x] for x in temp]) >= self.getProblem().getTrack(track).getTrackRequiredTimeSlots()
            
        #Creating constraints: Consider organiser conflicts
        all_constraints = []
        temp2 = []
        for z in range(self.getProblem().getNumberOfTracks()):
            if len(self.getProblem().getTrack(z).getTrackOrganiserConflictsList()) != 0:
                for i in range(self.getProblem().getNumberOfSessions()):
                    temp = []
                    for j in range(self.getProblem().getNumberOfRooms()):        
                        temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                        for x in self.getProblem().getTrack(z).getTrackOrganiserConflictsList():
                            temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+x.getTrackName())
                    if sorted(temp) not in temp2:
                        temp2.append(sorted(temp))
        for i in range(len(temp2)):
            all_constraints.append(lpSum([add_variables[x] for x in temp2[i]]))
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints for tracktrack penalty
        all_constraints = []
        for i in range(self.getProblem().getNumberOfTracks()):
            temp = [i]
            for j in range(i, self.getProblem().getNumberOfTracks()):
                if i != j:
                    if self.getProblem().getTracksTracksPenaltybyIndex(i, j) != 0:
                        temp.append(j)
                if len(temp) > 1:
                    for session in range(self.getProblem().getNumberOfSessions()):
                        session_name = self.getProblem().getSession(session).getSessionName()
                        temp2 = []
                        for name in range(len(add_names)):
                            for z in range(len(temp)):
                                if add_names[name].split('|')[1] == session_name and add_names[name].split('|')[3] == self.getProblem().getTrack(temp[z]).getTrackName():
                                    temp2.append(add_names[name])
                        all_constraints.append(lpSum([add_variables[x] for x in temp2]) - penalties['ptt_|' + str(i) + str(j) + str(session)])
                        #all_constraints.append(lpSum([add_variables[x] for x in temp2]))
                    temp = [i]
                        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints: Do not assign same track into same session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getSessionName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getTrackName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and track_name == name.split('|')[3]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[x] for x in temp]) - penalties['ppt_|' + str(session) + str(track)])
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints: Min number of Rooms per Track
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getTrackName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            all_constraints.append(lpSum([add2_variables[x] for x in temp]) - penalties['pmrt_|' + str(track)])
            #all_constraints.append(lpSum([add2_variables[x] for x in temp]))
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        all_constraints = []
        for room in range(self.getProblem().getNumberOfRooms()):
            room_name = self.getProblem().getRoom(room).getRoomName()
            for track in range(self.getProblem().getNumberOfTracks()):
                temp = []
                track_name = self.getProblem().getTrack(track).getTrackName()
                for name in add_names:
                    if room_name == name.split('|')[2] and track_name == name.split('|')[3]:
                        temp.append(name)
                for name in add2_names:
                    if room_name == name.split('|')[1] and track_name == name.split('|')[2]:
                        temp.append(name)
                #all_constraints.append(lpSum([add_variables[temp[x]] for x in range(len(temp) - 1)]) - required_sessions[str(track)] * add2_variables[temp[len(temp) - 1]])
                all_constraints.append(lpSum([add_variables[temp[x]] for x in range(len(temp) - 1)]) - self.getProblem().getNumberOfSessions() * add2_variables[temp[len(temp) - 1]])
                    
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        #Creating constraints: Assign only 1 track into one room and session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getSessionName()
            for room in range(self.getProblem().getNumberOfRooms()):
                room_name = self.getProblem().getRoom(room).getRoomName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
            
        #Creating constraints: Consecutive Tracks
        all_constraints1 = []
        all_constraints2 = []
        for i in range(self.getProblem().getNumberOfRooms() * self.getProblem().getNumberOfTracks()):
            temp = []
            temp.append(add_names[i])
            for j in range(len(add_names)):
                if add_names[i].split('|')[1] != add_names[j].split('|')[1] and add_names[i].split('|')[2] == add_names[j].split('|')[2] and add_names[i].split('|')[3] == add_names[j].split('|')[3]:
                    temp.append(add_names[j])
            for z in range(len(temp)-1):
                temp2 = temp[z] + temp[z+1]
                all_constraints1.append(product_variables[temp2] - add_variables[temp[z]] - add_variables[temp[z+1]])
                all_constraints2.append(product_variables[temp2] - add_variables[temp[z]])
                all_constraints2.append(product_variables[temp2] - add_variables[temp[z+1]])
                    
        for c in range(len(all_constraints1)):
            model += all_constraints1[c] >= -1
            
        for c in range(len(all_constraints2)):
            model += all_constraints2[c] <= 0
        
        #Solving
        print('-------- Solving mathematical model --------')
        stime = time()
        model.solve(GUROBI(msg = 0, timeLimit = 90)) #StartNodeLimit / TuneTimeLimit / timeLimit / threads
        print('-------- Mathematical model solved --------')
        t = round(time() - stime, 2)
        print('BIP Solving time:', round((time() - stime), 2))
        #model.solve(CPLEX_PY(msg = 1, timeLimit = 900))
        print(model.objective.value())
        print("Model Status:", LpStatus[model.status])
        solution = []
        solution2 = []
        to_remove = []
        gur_vars = model.solverModel.getVars()
        for i in gur_vars:
            if i.X > 0:
                solution.append(i.varName)
        for i in range(len(solution)):
            if solution[i].split('|')[0] != 'AddVariables_':
                to_remove.append(solution[i])
            if solution[i].split('|')[0] == 'Variables_':
                solution2.append(solution[i])
        for i in to_remove:
            if i in solution:
                solution.remove(i)
        
        df = pd.DataFrame(solution)
        df.replace(to_replace = '_', value = ' ', regex = True, inplace = True)
        df = df.applymap(lambda x: x.split('|'))
        solution = df.iloc[:,0].to_list()
        
        df = pd.DataFrame(solution2)
        df.replace(to_replace = '_', value = ' ', regex = True, inplace = True)
        df = df.applymap(lambda x: x.split('|'))
        solution2 = df.iloc[:,0].to_list()
        
        for i in range(len(solution)):
            self.getSolution().getSolTracks()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])] = self.getProblem().getTrackIndex(solution[i][3])
                 
        for i in range(len(solution2)):
            for j in range(self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(solution2[i][4])).getSubmissionRequiredTimeSlots()):
                ts = self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution2[i][1])][self.getProblem().getRoomIndex(solution2[i][2])].index(-1)
                self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution2[i][1])][self.getProblem().getRoomIndex(solution2[i][2])][ts] = self.getProblem().getSubmissionIndex(solution2[i][4])
        return t
    
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
        
class Matheuristic(Optimisation):
    def __init__(self, problem, solution):
        Optimisation.__init__(self, problem, solution)
        
    def solve(self, start_time, run_time):
        self.TracksExactModel()
        self.getSolution().convertSolFirstTime()
        solver = HyperHeuristic(self.getProblem(), self.getSolution())
        solver.solve(start_time, run_time)
        