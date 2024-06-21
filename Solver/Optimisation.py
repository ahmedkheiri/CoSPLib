# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

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
    
    def TracksExactModel(self, timelimit): 
        model = LpProblem('model', LpMinimize)
        names = []
        sub_x_map = {self.getProblem().getSubmission(sub).getSubmissionName(): [] for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() > 1}
        track_session_room_x_map = {self.getProblem().getTrack(track).getTrackName()+self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName(): [] for track in range(self.getProblem().getNumberOfTracks()) for session in range(self.getProblem().getNumberOfSessions()) for room in range(self.getProblem().getNumberOfRooms())}
        add_names = []
        track_z_map = {self.getProblem().getTrack(track).getTrackName(): [] for track in range(self.getProblem().getNumberOfTracks())}
        session_room_z_map = {}
        room_track_z_map = {self.getProblem().getRoom(room).getRoomName()+self.getProblem().getTrack(track).getTrackName(): [] for room in range(self.getProblem().getNumberOfRooms()) for track in range(self.getProblem().getNumberOfTracks())}
        track_session_room_z_map = {}
        session_track_z_map = {self.getProblem().getSession(session).getSessionName()+self.getProblem().getTrack(track).getTrackName(): [] for session in range(self.getProblem().getNumberOfSessions()) for track in range(self.getProblem().getNumberOfTracks())}
        add2_names = []
        track_room_y_map = {}
        track_y_map = {}
        product_names = []
        coefficients = {}
        timeslots = {}
        n = {}
        mts_subs = [sub for sub in range(self.getProblem().getNumberOfSubmissions()) if self.getProblem().getSubmission(sub).getSubmissionRequiredTimeSlots() > 1]
        
        #Creating decision variables Zs
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                temp = []
                for z in range(self.getProblem().getNumberOfTracks()):
                    add_names.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                    timeslots['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()] = self.getProblem().getSession(i).getSessionMaxTimeSlots()
                    coefficients['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()] = 1 + self.getProblem().getParameters().getTracksSessionsPenaltyWeight() * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getTrackName(), self.getProblem().getSession(i).getSessionName()) + self.getProblem().getParameters().getTracksRoomsPenaltyWeight() * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(z).getTrackName(), self.getProblem().getRoom(j).getRoomName()) + self.getProblem().getParameters().getSessionsRoomsPenaltyWeight() * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getSessionName(), self.getProblem().getRoom(j).getRoomName())
                    temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                    room_track_z_map[self.getProblem().getRoom(j).getRoomName()+self.getProblem().getTrack(z).getTrackName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                    track_z_map[self.getProblem().getTrack(z).getTrackName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                    track_session_room_z_map[self.getProblem().getTrack(z).getTrackName()+self.getProblem().getSession(i).getSessionName()+self.getProblem().getRoom(j).getRoomName()] = '|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()
                    session_track_z_map[self.getProblem().getSession(i).getSessionName()+self.getProblem().getTrack(z).getTrackName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                session_room_z_map[self.getProblem().getSession(i).getSessionName()+self.getProblem().getRoom(j).getRoomName()] = temp
        
        #Creating decision variables Xs
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                for x in mts_subs:
                    if self.getProblem().getSubmission(x).getSubmissionRequiredTimeSlots() <= self.getProblem().getSession(i).getSessionMaxTimeSlots():
                        names.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getSubmission(x).getSubmissionTrack().getTrackName()+'|'+self.getProblem().getSubmission(x).getSubmissionName())
                        coefficients['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getSubmission(x).getSubmissionTrack().getTrackName()+'|'+self.getProblem().getSubmission(x).getSubmissionName()] = 1
                        n['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getSubmission(x).getSubmissionTrack().getTrackName()+'|'+self.getProblem().getSubmission(x).getSubmissionName()] = self.getProblem().getSubmission(x).getSubmissionRequiredTimeSlots()
                        sub_x_map[self.getProblem().getSubmission(x).getSubmissionName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getSubmission(x).getSubmissionTrack().getTrackName()+'|'+self.getProblem().getSubmission(x).getSubmissionName())
                        track_session_room_x_map[self.getProblem().getSubmission(x).getSubmissionTrack().getTrackName()+self.getProblem().getSession(i).getSessionName()+self.getProblem().getRoom(j).getRoomName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getSubmission(x).getSubmissionTrack().getTrackName()+'|'+self.getProblem().getSubmission(x).getSubmissionName())

        #Additional variables to minimise tracks per room Ys
        for i in range(self.getProblem().getNumberOfTracks()):
            temp = []
            for j in range(self.getProblem().getNumberOfRooms()):
                add2_names.append('|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName())
                coefficients['|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName()] = 1
                temp.append('|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName())
                track_room_y_map[self.getProblem().getTrack(i).getTrackName()+self.getProblem().getRoom(j).getRoomName()] = '|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName()
            track_y_map[self.getProblem().getTrack(i).getTrackName()] = temp

        pen = []
        #Creating penalties for similar tracks
        for i in range(self.getProblem().getNumberOfTracks()):
            temp = [i]
            for j in range(i, self.getProblem().getNumberOfTracks()):
                if i != j:
                    if self.getProblem().getTracksTracksPenaltybyIndex(i, j) != 0:
                        temp.append(j)
                if len(temp) > 1:
                    for session in range(self.getProblem().getNumberOfSessions()):
                        pen.append('ptt_|' + self.getProblem().getTrack(i).getTrackName() + self.getProblem().getTrack(j).getTrackName() + self.getProblem().getSession(session).getSessionName())
                        coefficients['ptt_|' + self.getProblem().getTrack(i).getTrackName() + self.getProblem().getTrack(j).getTrackName() + self.getProblem().getSession(session).getSessionName()] = self.getProblem().getParameters().getSimilarTracksPenaltyWeight() * self.getProblem().getTracksTracksPenaltybyIndex(i, j)
                    temp = [i]
                    
        #Creating penalties for min number of rooms per track
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getTrackName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            pen.append('pmrt_|' + self.getProblem().getTrack(track).getTrackName())
            coefficients['pmrt_|' + self.getProblem().getTrack(track).getTrackName()] = self.getProblem().getParameters().getNumOfRoomsPerTrackWeight()
        
        #Creating penalties for parallel tracks
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getSessionName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getTrackName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and track_name == name.split('|')[3]:
                        temp.append(name)
                pen.append('ppt_|' + self.getProblem().getSession(session).getSessionName() + self.getProblem().getTrack(track).getTrackName())
                coefficients['ppt_|' + self.getProblem().getSession(session).getSessionName() + self.getProblem().getTrack(track).getTrackName()] = self.getProblem().getParameters().getParallelTracksWeight()
        
        #Creating objective function and binary IP formulation
        variables = LpVariable.dicts('Variables', names, cat = 'Binary')
        add_variables = LpVariable.dicts('AddVariables', add_names, cat = 'Binary')
        add2_variables = LpVariable.dicts('Add2Variables', add2_names, cat = 'Binary')
        product_variables = LpVariable.dicts('ProdVariables', product_names, cat = 'Binary')
        penalties = LpVariable.dicts('Penalties', pen, lowBound = 0, cat = 'Integer')
        obj_function = [add_variables, penalties]
        all_names = [add_names, pen]
        model += lpSum([coefficients[i] * obj_function[x][i] for x in range(len(obj_function)) for i in all_names[x]])
              
        #Assign subs with multiple ts
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            for session in range(self.getProblem().getNumberOfSessions()):
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp = track_session_room_x_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]
                    if len(temp) != 0:
                        all_constraints.append(lpSum([n[x] * variables[x] for x in temp]) - self.getProblem().getSession(session).getSessionMaxTimeSlots() * add_variables[track_session_room_z_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]])
                        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        #Creating Constraints: All submissions must be scheduled
        all_constraints = []
        for submission in mts_subs:
            temp = sub_x_map[self.getProblem().getSubmission(submission).getSubmissionName()]
            all_constraints.append(lpSum([variables[x] for x in temp]))
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        #Creating constraints: Assign tracks with respect to available time slots
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = track_z_map[self.getProblem().getTrack(track).getTrackName()]
            model += lpSum([timeslots[x] * add_variables[x] for x in temp]) >= self.getProblem().getTrack(track).getTrackRequiredTimeSlots()
        
        #Creating constraints: Consider organiser conflicts
        all_constraints = []
        temp2 = []
        for z in range(self.getProblem().getNumberOfTracks()):
            if len(self.getProblem().getTrack(z).getTrackChairConflictsList()) != 0:
                for i in range(self.getProblem().getNumberOfSessions()):
                    temp = []
                    for j in range(self.getProblem().getNumberOfRooms()):        
                        temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                        for x in self.getProblem().getTrack(z).getTrackChairConflictsList():
                            temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+x.getTrackName())
                    if sorted(temp) not in temp2:
                        temp2.append(sorted(temp))
        for i in range(len(temp2)):
            all_constraints.append(lpSum([add_variables[x] for x in temp2[i]]))
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints for similar tracks
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
                        all_constraints.append(lpSum([add_variables[x] for x in temp2]) - penalties['ptt_|' + self.getProblem().getTrack(i).getTrackName() + self.getProblem().getTrack(j).getTrackName() + self.getProblem().getSession(session).getSessionName()] - penalties['ppt_|' + self.getProblem().getSession(session).getSessionName() + self.getProblem().getTrack(i).getTrackName()] - penalties['ppt_|' + self.getProblem().getSession(session).getSessionName() + self.getProblem().getTrack(j).getTrackName()])
                    temp = [i]
                        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
            
        #Creating constraints: Do not assign same track into same session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            for track in range(self.getProblem().getNumberOfTracks()):
                temp = session_track_z_map[self.getProblem().getSession(session).getSessionName()+self.getProblem().getTrack(track).getTrackName()]
                all_constraints.append(lpSum([add_variables[x] for x in temp]) - penalties['ppt_|' + self.getProblem().getSession(session).getSessionName() + self.getProblem().getTrack(track).getTrackName()])
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints: Min number of Rooms per Track
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = track_y_map[self.getProblem().getTrack(track).getTrackName()]
            all_constraints.append(lpSum([add2_variables[x] for x in temp]) - penalties['pmrt_|' + self.getProblem().getTrack(track).getTrackName()])
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        all_constraints = []
        for room in range(self.getProblem().getNumberOfRooms()):
            for track in range(self.getProblem().getNumberOfTracks()):
                temp = room_track_z_map[self.getProblem().getRoom(room).getRoomName()+self.getProblem().getTrack(track).getTrackName()]
                all_constraints.append(lpSum([add_variables[x] for x in temp]) - self.getProblem().getNumberOfSessions() * add2_variables[track_room_y_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getRoom(room).getRoomName()]])
                   
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        #Creating constraints: Assign only 1 track into one room and session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            for room in range(self.getProblem().getNumberOfRooms()):
                temp = session_room_z_map[self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1

        #Solving
        print('-------- Solving mathematical model --------')
        stime = time()
        model.solve(GUROBI(msg = 0, timeLimit = timelimit)) #StartNodeLimit / TuneTimeLimit / timeLimit / threads
        print('-------- Mathematical model solved --------')
        t = round(time() - stime, 2)
        print('Solving time:', round((time() - stime), 2))
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
        
        if len(solution2) > 0:
            df = pd.DataFrame(solution2)
            df.replace(to_replace = '_', value = ' ', regex = True, inplace = True)
            df = df.applymap(lambda x: x.split('|'))
            solution2 = df.iloc[:,0].to_list()
        
        for i in range(len(solution)):
            self.getSolution().getSolTracks()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])] = self.getProblem().getTrackIndex(solution[i][3])
                 
        if len(solution2) > 0:
            for i in range(len(solution2)):
                for j in range(self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(solution2[i][4])).getSubmissionRequiredTimeSlots()):
                    ts = self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution2[i][1])][self.getProblem().getRoomIndex(solution2[i][2])].index(-1)
                    self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution2[i][1])][self.getProblem().getRoomIndex(solution2[i][2])][ts] = self.getProblem().getSubmissionIndex(solution2[i][4])
        return t
    
    def SwapTrack(self):
        if self.getProblem().getNumberOfTracks() == 1:
            return
        session = np.random.randint(self.getProblem().getNumberOfSessions(), size = 2)
        room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        while (session[0] == session[1] and room[0] == room[1]) or (self.getSolution().getSolTracks()[session[0]][room[0]] + self.getSolution().getSolTracks()[session[1]][room[1]] == -2) or (self.getSolution().getSolTracks()[session[0]][room[0]] == self.getSolution().getSolTracks()[session[1]][room[1]]):
            session = np.random.randint(self.getProblem().getNumberOfSessions(), size = 2)
            room = np.random.randint(self.getProblem().getNumberOfRooms(), size = 2)
        self.getSolution().getSolTracks()[session[0]][room[0]], self.getSolution().getSolTracks()[session[1]][room[1]] = self.getSolution().getSolTracks()[session[1]][room[1]], self.getSolution().getSolTracks()[session[0]][room[0]]
            
    def SwapSubmission(self):
        track = np.random.randint(self.getProblem().getNumberOfTracks())
        subs = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        while (subs[0] == subs[1]) or (len(self.getSolution().getIndSolSubmissions()[track]) == 1):
            track = np.random.randint(self.getProblem().getNumberOfTracks())
            subs = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        self.getSolution().getIndSolSubmissions()[track][subs[0]], self.getSolution().getIndSolSubmissions()[track][subs[1]] = self.getSolution().getIndSolSubmissions()[track][subs[1]], self.getSolution().getIndSolSubmissions()[track][subs[0]]
    
    def ReverseSubmission(self):
        track = np.random.randint(self.getProblem().getNumberOfTracks())
        locs = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        while (locs[0] == locs[1]) or (len(self.getSolution().getIndSolSubmissions()[track]) == 1):
            track = np.random.randint(self.getProblem().getNumberOfTracks())
            locs = np.random.randint(len(self.getSolution().getIndSolSubmissions()[track]), size = 2)
        loc = sorted(locs)
        temp = self.getSolution().getIndSolSubmissions()[track][loc[0]:loc[1]]
        temp.reverse()
        self.getSolution().getIndSolSubmissions()[track][loc[0]:loc[1]] = temp
          
class ExactModel(Optimisation):
    def __init__(self, problem, solution):
        Optimisation.__init__(self, problem, solution)
        
    def solve(self, timelimit = 3600):
        t_b = time()
        model = LpProblem('model', LpMinimize)
        names = []
        subs_with_conflicts = [sub for sub in range(self.getProblem().getNumberOfSubmissions()) if len(self.getProblem().getSubmission(sub).getSubmissionPresenterConflictsList()) != 0]
        submission_conflict_x_list = []
        track_session_room_x_map = {}
        track_submission_x_map = {self.getProblem().getTrack(track).getTrackName()+self.getProblem().getTrack(track).getTrackSubmissionsList()[sub].getSubmissionName(): [] for track in range(self.getProblem().getNumberOfTracks()) for sub in range(len(self.getProblem().getTrack(track).getTrackSubmissionsList()))}
        add_names = []
        session_room_z_map = {}
        track_session_room_z_map = {}
        room_track_z_map = {self.getProblem().getRoom(room).getRoomName()+self.getProblem().getTrack(track).getTrackName(): [] for room in range(self.getProblem().getNumberOfRooms()) for track in range(self.getProblem().getNumberOfTracks())}
        add2_names = []
        track_y_map = {}
        track_room_y_map = {}
        coefficients = {}
        timeslots = {}
        
        #Determine MaxS for each track
        sessions_ts = []
        required_sessions = {}
        for session in range(self.getProblem().getNumberOfSessions()):
            sessions_ts.append(self.getProblem().getSession(session).getSessionMaxTimeSlots())
        sorted_sessions_ts = sorted(sessions_ts)
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            i = -1
            while self.getProblem().getTrack(track).getTrackRequiredTimeSlots() > sum(temp):
                i += 1
                temp.append(sorted_sessions_ts[i])
                if i == self.getProblem().getNumberOfSessions() - 1:
                    break
            required_sessions[str(track)] = len(temp)
        
        #Creating decision variables [X Variables]
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                for z in range(self.getProblem().getNumberOfTracks()):
                    temp = []
                    for x in range(len(self.getProblem().getTrack(z).getTrackSubmissionsList())):
                        names.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()))
                        coefficients['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName())] = self.getProblem().getParameters().getSubmissionsTimezonesWeight() * self.getProblem().getSubmissionsTimezonesPenalty(str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()), self.getProblem().getSession(i).getSessionName()) + self.getProblem().getParameters().getSubmissionsSessionsPenaltyWeight() * self.getProblem().getSubmissionsSessionsPenalty(str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()), self.getProblem().getSession(i).getSessionName()) + self.getProblem().getParameters().getSubmissionsRoomsPenaltyWeight() * self.getProblem().getSubmissionsRoomsPenalty(str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()), self.getProblem().getRoom(j).getRoomName())
                        timeslots['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName())] = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName())).getSubmissionRequiredTimeSlots()
                        temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()))
                        track_submission_x_map[self.getProblem().getTrack(z).getTrackName()+self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()))
                        if len(self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName())).getSubmissionPresenterConflictsList()) != 0:
                            submission_conflict_x_list.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()))
                    track_session_room_x_map[self.getProblem().getTrack(z).getTrackName()+self.getProblem().getSession(i).getSessionName()+self.getProblem().getRoom(j).getRoomName()] = temp
        
        #Additional variables to minimise tracks per room [Y Variables]
        for i in range(self.getProblem().getNumberOfTracks()):
            temp = []
            for j in range(self.getProblem().getNumberOfRooms()):
                add2_names.append('|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName())
                temp.append('|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName())
                track_room_y_map[self.getProblem().getTrack(i).getTrackName()+self.getProblem().getRoom(j).getRoomName()] = '|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName()
            track_y_map[self.getProblem().getTrack(i).getTrackName()] = temp
        
        #Additional variables for assigning tracks into sessions and rooms [Z Variables]
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                temp = []
                for z in range(self.getProblem().getNumberOfTracks()):
                    add_names.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                    coefficients['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()] = self.getProblem().getParameters().getTracksSessionsPenaltyWeight() * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getTrackName(), self.getProblem().getSession(i).getSessionName()) + self.getProblem().getParameters().getTracksRoomsPenaltyWeight() * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(z).getTrackName(), self.getProblem().getRoom(j).getRoomName()) + self.getProblem().getParameters().getSessionsRoomsPenaltyWeight() * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getSessionName(), self.getProblem().getRoom(j).getRoomName())
                    temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                    track_session_room_z_map[self.getProblem().getTrack(z).getTrackName()+self.getProblem().getSession(i).getSessionName()+self.getProblem().getRoom(j).getRoomName()] = '|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()
                    room_track_z_map[self.getProblem().getRoom(j).getRoomName()+self.getProblem().getTrack(z).getTrackName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                session_room_z_map[self.getProblem().getSession(i).getSessionName()+self.getProblem().getRoom(j).getRoomName()] = temp
        
        #Creating objective function and binary IP formulation
        variables = LpVariable.dicts('Variables', names, cat = 'Binary')
        add_variables = LpVariable.dicts('AddVariables', add_names, cat = 'Binary')
        add2_variables = LpVariable.dicts('Add2Variables', add2_names, cat = 'Binary')
        obj_function = [variables, add_variables]
        all_names = [names, add_names]
        model += lpSum([coefficients[i] * obj_function[x][i] for x in range(len(obj_function)) for i in all_names[x]])
              
        #Creating Constraints Eq.2
        if len(subs_with_conflicts) != 0:
            unique_conflicts = []
            for submission in range(self.getProblem().getNumberOfSubmissions()):
                sub_name = self.getProblem().getSubmission(submission).getSubmissionName()
                if len(self.getProblem().getSubmission(submission).getSubmissionPresenterConflictsList()) != 0:
                    for conflict in self.getProblem().getSubmission(submission).getSubmissionPresenterConflictsList():
                        for session in range(self.getProblem().getNumberOfSessions()):
                            session_name = self.getProblem().getSession(session).getSessionName()
                            for room in range(self.getProblem().getNumberOfRooms()):
                                room_name = self.getProblem().getRoom(room).getRoomName()
                                current_conflict = [sub_name, conflict.getSubmissionName(), session_name, room_name]
                                M_list = [len(self.getProblem().getSubmission(submission).getSubmissionPresenterConflictsList())+1, self.getProblem().getSession(session).getSessionMaxTimeSlots()]
                                M = min(M_list)
                                if sorted(current_conflict) not in unique_conflicts:
                                    unique_conflicts.append(sorted(current_conflict))
                                    temp = []
                                    temp2 = []
                                    for name in range(len(submission_conflict_x_list)):
                                        if (submission_conflict_x_list[name].split('|')[4] == sub_name and submission_conflict_x_list[name].split('|')[1] == session_name and submission_conflict_x_list[name].split('|')[2] == room_name):
                                            temp.append(submission_conflict_x_list[name])
                                        if (submission_conflict_x_list[name].split('|')[4] == conflict.getSubmissionName() and submission_conflict_x_list[name].split('|')[2] != room_name and submission_conflict_x_list[name].split('|')[1] == session_name):
                                            temp2.append(submission_conflict_x_list[name])
                                    model += lpSum([M * variables[x] for x in temp]) + lpSum([variables[x] for x in temp2]) <= M
   
        #Creating constraints Eq.5
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            for room in range(self.getProblem().getNumberOfRooms()):
                temp = session_room_z_map[self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints Eq.6 & Eq.7
        all_constraints = []
        all_constraints2 = []
        for track in range(self.getProblem().getNumberOfTracks()):
            for session in range(self.getProblem().getNumberOfSessions()):
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp = track_session_room_x_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]
                    all_constraints.append(lpSum([timeslots[x] * variables[x] for x in temp]) - self.getProblem().getSession(session).getSessionMaxTimeSlots() * add_variables[track_session_room_z_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]])
                    all_constraints2.append(lpSum([variables[x] for x in temp]) - add_variables[track_session_room_z_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]])

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
            model += all_constraints2[c] >= 0
            
        #Creating constraints Eq.3
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = track_y_map[self.getProblem().getTrack(track).getTrackName()]
            all_constraints.append(lpSum([add2_variables[x] for x in temp]))
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        #Creating constraints Eq.4
        all_constraints = []
        for room in range(self.getProblem().getNumberOfRooms()):
            for track in range(self.getProblem().getNumberOfTracks()):
                temp = room_track_z_map[self.getProblem().getRoom(room).getRoomName()+self.getProblem().getTrack(track).getTrackName()]
                all_constraints.append(lpSum([add_variables[x] for x in temp]) - required_sessions[str(track)] * add2_variables[track_room_y_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getRoom(room).getRoomName()]])
                   
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        #Creating Constraints Eq.1
        all_constraints = []
        for z in range(self.getProblem().getNumberOfTracks()):
            for x in range(len(self.getProblem().getTrack(z).getTrackSubmissionsList())):
                temp = track_submission_x_map[self.getProblem().getTrack(z).getTrackName()+self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()]
                all_constraints.append(lpSum([variables[x] for x in temp]))
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        t_b = round((time() - t_b), 2)
        #Solving
        t_s = time()
        model.solve(GUROBI(msg = 0, MIPGap = 0, timeLimit = timelimit))
        #model.solve(GLPK_CMD(msg = 0))
        print('Building time:', t_b)
        print('Solving time:', round((time() - t_s), 2))
        print(model.objective.value())
        print("Model Status:", LpStatus[model.status])
        if LpStatus[model.status] == 'Infeasible':
            sys.exit(print('Model is Infeasible.'))
        solution = []
        for i in model.variables():
            if i.varValue > 0:
                solution.append(i.name)
        to_remove = []
        for i in range(len(solution)):
            if solution[i].split('|')[0] != 'Variables_':
                to_remove.append(solution[i])
        for i in to_remove:
            if i in solution:
                solution.remove(i)
        df = pd.DataFrame(solution)
        df.replace(to_replace = '_', value = ' ', regex = True, inplace = True)
        df = df.applymap(lambda x: x.split('|'))
        solution = df.iloc[:,0].to_list()
        for i in range(len(solution)):
            self.getSolution().getSolTracks()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])] = self.getProblem().getTrackIndex(solution[i][3])
            ts = self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])].index(-1)
            self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])][ts] = self.getProblem().getSubmissionIndex(solution[i][4])
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            for session in range(len(self.getSolution().getSolSubmissions())):
                for room in range(len(self.getSolution().getSolSubmissions()[session])):
                    if sub in self.getSolution().getSolSubmissions()[session][room]:
                        info = []
                        for i in range(len(self.getSolution().getSolSubmissions()[session][room])):
                            if self.getSolution().getSolSubmissions()[session][room][i] != -1:
                                if self.getSolution().getSolSubmissions()[session][room][i] not in info:
                                    info.append(self.getSolution().getSolSubmissions()[session][room][i])
                        temp = []
                        for i in range(len(info)):
                            while temp.count(info[i]) < self.getProblem().getSubmission(info[i]).getSubmissionRequiredTimeSlots():
                                temp.append(info[i])
                        while len(temp) < len(self.getSolution().getSolSubmissions()[session][room]):
                            temp.append(-1)
                        self.getSolution().getSolSubmissions()[session][room] = temp
                        
class ExtendedModel(Optimisation):
    def __init__(self, problem, solution):
        Optimisation.__init__(self, problem, solution)
        
    def solve(self, timelimit = 3600):
        t_b = time()
        model = LpProblem('model', LpMinimize)
        names = []
        submission_conflict_x_list = []
        submission_att_conflict_x_list = []
        track_session_room_x_map = {}
        track_submission_x_map = {self.getProblem().getTrack(track).getTrackName()+self.getProblem().getTrack(track).getTrackSubmissionsList()[sub].getSubmissionName(): [] for track in range(self.getProblem().getNumberOfTracks()) for sub in range(len(self.getProblem().getTrack(track).getTrackSubmissionsList()))}
        add_names = []
        session_room_z_map = {}
        track_session_room_z_map = {}
        room_track_z_map = {self.getProblem().getRoom(room).getRoomName()+self.getProblem().getTrack(track).getTrackName(): [] for room in range(self.getProblem().getNumberOfRooms()) for track in range(self.getProblem().getNumberOfTracks())}
        similar_tracks = {self.getProblem().getSession(session).getSessionName()+self.getProblem().getTrack(track).getTrackName(): [] for session in range(self.getProblem().getNumberOfSessions()) for track in range(self.getProblem().getNumberOfTracks())}
        add2_names = []
        track_y_map = {}
        track_room_y_map = {}
        product_names = []
        coefficients = {}
        timeslots = {}
        
        #Determine MaxS for each track
        sessions_ts = []
        required_sessions = {}
        for session in range(self.getProblem().getNumberOfSessions()):
            sessions_ts.append(self.getProblem().getSession(session).getSessionMaxTimeSlots())
        sorted_sessions_ts = sorted(sessions_ts)
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            i = -1
            while self.getProblem().getTrack(track).getTrackRequiredTimeSlots() > sum(temp):
                i += 1
                temp.append(sorted_sessions_ts[i])
                if i == self.getProblem().getNumberOfSessions() - 1:
                    break
            required_sessions[str(track)] = len(temp)
        
        #Creating decision variables [X Variables]
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                for z in range(self.getProblem().getNumberOfTracks()):
                    temp = []
                    for x in range(len(self.getProblem().getTrack(z).getTrackSubmissionsList())):
                        names.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()))
                        coefficients['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName())] = self.getProblem().getParameters().getSubmissionsTimezonesWeight() * self.getProblem().getSubmissionsTimezonesPenalty(str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()), self.getProblem().getSession(i).getSessionName()) + self.getProblem().getParameters().getSubmissionsSessionsPenaltyWeight() * self.getProblem().getSubmissionsSessionsPenalty(str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()), self.getProblem().getSession(i).getSessionName()) + self.getProblem().getParameters().getSubmissionsRoomsPenaltyWeight() * self.getProblem().getSubmissionsRoomsPenalty(str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()), self.getProblem().getRoom(j).getRoomName())
                        timeslots['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName())] = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName())).getSubmissionRequiredTimeSlots()
                        temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()))
                        track_submission_x_map[self.getProblem().getTrack(z).getTrackName()+self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()))
                        if len(self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName())).getSubmissionPresenterConflictsList()) != 0:
                            submission_conflict_x_list.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()))
                        if len(self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName())).getSubmissionAttendeeConflictsList()) != 0:
                            submission_att_conflict_x_list.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()+'|'+str(self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()))
                    track_session_room_x_map[self.getProblem().getTrack(z).getTrackName()+self.getProblem().getSession(i).getSessionName()+self.getProblem().getRoom(j).getRoomName()] = temp
        
        #Additional variables to minimise tracks per room [Y Variables]
        for i in range(self.getProblem().getNumberOfTracks()):
            temp = []
            for j in range(self.getProblem().getNumberOfRooms()):
                add2_names.append('|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName())
                temp.append('|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName())
                track_room_y_map[self.getProblem().getTrack(i).getTrackName()+self.getProblem().getRoom(j).getRoomName()] = '|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(i).getTrackName()
            track_y_map[self.getProblem().getTrack(i).getTrackName()] = temp
        
        #Additional variables for assigning tracks into sessions and rooms [Z Variables]
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                temp = []
                for z in range(self.getProblem().getNumberOfTracks()):
                    add_names.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                    coefficients['|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()] = self.getProblem().getParameters().getTracksSessionsPenaltyWeight() * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getTrackName(), self.getProblem().getSession(i).getSessionName()) + self.getProblem().getParameters().getTracksRoomsPenaltyWeight() * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(z).getTrackName(), self.getProblem().getRoom(j).getRoomName()) + self.getProblem().getParameters().getSessionsRoomsPenaltyWeight() * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getSessionName(), self.getProblem().getRoom(j).getRoomName())
                    temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                    track_session_room_z_map[self.getProblem().getTrack(z).getTrackName()+self.getProblem().getSession(i).getSessionName()+self.getProblem().getRoom(j).getRoomName()] = '|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName()
                    room_track_z_map[self.getProblem().getRoom(j).getRoomName()+self.getProblem().getTrack(z).getTrackName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                    for x in range(z + 1, self.getProblem().getNumberOfTracks()):
                        if self.getProblem().getTracksTracksPenaltybyIndex(z, x) != 0:
                            if '|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName() not in similar_tracks[self.getProblem().getSession(i).getSessionName()+self.getProblem().getTrack(z).getTrackName()]:
                                similar_tracks[self.getProblem().getSession(i).getSessionName()+self.getProblem().getTrack(z).getTrackName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                            if '|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(x).getTrackName() not in similar_tracks[self.getProblem().getSession(i).getSessionName()+self.getProblem().getTrack(z).getTrackName()]:
                                similar_tracks[self.getProblem().getSession(i).getSessionName()+self.getProblem().getTrack(z).getTrackName()].append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(x).getTrackName())
                session_room_z_map[self.getProblem().getSession(i).getSessionName()+self.getProblem().getRoom(j).getRoomName()] = temp
        
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
                coefficients[temp2] = - self.getProblem().getParameters().getConsecutiveTracksWeight()
             
        #Creating objective function and binary IP formulation
        variables = LpVariable.dicts('Variables', names, cat = 'Binary')
        add_variables = LpVariable.dicts('AddVariables', add_names, cat = 'Binary')
        add2_variables = LpVariable.dicts('Add2Variables', add2_names, cat = 'Binary')
        product_variables = LpVariable.dicts('ProdVariables', product_names, cat = 'Binary')
        obj_function = [variables, add_variables, product_variables]
        all_names = [names, add_names, product_names]
        model += lpSum([coefficients[i] * obj_function[x][i] for x in range(len(obj_function)) for i in all_names[x]])

        #Creating Constraints Eq.2
        if len(submission_conflict_x_list) != 0:
            unique_conflicts = []
            for submission in range(self.getProblem().getNumberOfSubmissions()):
                sub_name = self.getProblem().getSubmission(submission).getSubmissionName()
                if len(self.getProblem().getSubmission(submission).getSubmissionPresenterConflictsList()) != 0:
                    for conflict in self.getProblem().getSubmission(submission).getSubmissionPresenterConflictsList():
                        for session in range(self.getProblem().getNumberOfSessions()):
                            session_name = self.getProblem().getSession(session).getSessionName()
                            for room in range(self.getProblem().getNumberOfRooms()):
                                room_name = self.getProblem().getRoom(room).getRoomName()
                                current_conflict = [sub_name, conflict.getSubmissionName(), session_name, room_name]
                                M_list = [len(self.getProblem().getSubmission(submission).getSubmissionPresenterConflictsList())+1, self.getProblem().getSession(session).getSessionMaxTimeSlots()]
                                M = min(M_list)
                                if sorted(current_conflict) not in unique_conflicts:
                                    unique_conflicts.append(sorted(current_conflict))
                                    temp = []
                                    temp2 = []
                                    for name in range(len(submission_conflict_x_list)):
                                        if (submission_conflict_x_list[name].split('|')[4] == sub_name and submission_conflict_x_list[name].split('|')[1] == session_name and submission_conflict_x_list[name].split('|')[2] == room_name):
                                            temp.append(submission_conflict_x_list[name])
                                        if (submission_conflict_x_list[name].split('|')[4] == conflict.getSubmissionName() and submission_conflict_x_list[name].split('|')[2] != room_name and submission_conflict_x_list[name].split('|')[1] == session_name):
                                            temp2.append(submission_conflict_x_list[name])
                                    model += lpSum([M * variables[x] for x in temp]) + lpSum([variables[x] for x in temp2]) <= M
        
        #Creating constraints Eq.5
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            for room in range(self.getProblem().getNumberOfRooms()):
                temp = session_room_z_map[self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints Eq.6 & Eq.7
        all_constraints = []
        all_constraints2 = []
        for track in range(self.getProblem().getNumberOfTracks()):
            for session in range(self.getProblem().getNumberOfSessions()):
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp = track_session_room_x_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]
                    all_constraints.append(lpSum([timeslots[x] * variables[x] for x in temp]) - self.getProblem().getSession(session).getSessionMaxTimeSlots() * add_variables[track_session_room_z_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]])
                    all_constraints2.append(lpSum([variables[x] for x in temp]) - add_variables[track_session_room_z_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getSession(session).getSessionName()+self.getProblem().getRoom(room).getRoomName()]])

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
            model += all_constraints2[c] >= 0
            
        #Creating constraints Eq.3
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = track_y_map[self.getProblem().getTrack(track).getTrackName()]
            all_constraints.append(lpSum([add2_variables[x] for x in temp]))
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        #Creating constraints Eq.4
        all_constraints = []
        for room in range(self.getProblem().getNumberOfRooms()):
            for track in range(self.getProblem().getNumberOfTracks()):
                temp = room_track_z_map[self.getProblem().getRoom(room).getRoomName()+self.getProblem().getTrack(track).getTrackName()]
                all_constraints.append(lpSum([add_variables[x] for x in temp]) - required_sessions[str(track)] * add2_variables[track_room_y_map[self.getProblem().getTrack(track).getTrackName()+self.getProblem().getRoom(room).getRoomName()]])
                   
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        #Creating Constraints Eq.1
        all_constraints = []
        for z in range(self.getProblem().getNumberOfTracks()):
            for x in range(len(self.getProblem().getTrack(z).getTrackSubmissionsList())):
                temp = track_submission_x_map[self.getProblem().getTrack(z).getTrackName()+self.getProblem().getTrack(z).getTrackSubmissionsList()[x].getSubmissionName()]
                all_constraints.append(lpSum([variables[x] for x in temp]))
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        #Creating Constraints Eq.13
        all_constraints = []
        for i in similar_tracks.values():
            if len(i) != 0:
                temp = i
                all_constraints.append(lpSum([add_variables[x] for x in temp]))

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints Eq.15
        all_constraints = []
        temp2 = []
        for z in range(self.getProblem().getNumberOfTracks()):
            if len(self.getProblem().getTrack(z).getTrackChairConflictsList()) != 0:
                for i in range(self.getProblem().getNumberOfSessions()):
                    temp = []
                    for j in range(self.getProblem().getNumberOfRooms()):        
                        temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+self.getProblem().getTrack(z).getTrackName())
                        for x in self.getProblem().getTrack(z).getTrackChairConflictsList():
                            temp.append('|'+self.getProblem().getSession(i).getSessionName()+'|'+self.getProblem().getRoom(j).getRoomName()+'|'+x.getTrackName())
                    if sorted(temp) not in temp2:
                        temp2.append(sorted(temp))
        for i in range(len(temp2)):
            all_constraints.append(lpSum([add_variables[x] for x in temp2[i]]))
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating Constraints Eq.14
        if len(submission_att_conflict_x_list) != 0:
            unique_conflicts = []
            for submission in range(self.getProblem().getNumberOfSubmissions()):
                sub_name = self.getProblem().getSubmission(submission).getSubmissionName()
                if len(self.getProblem().getSubmission(submission).getSubmissionAttendeeConflictsList()) != 0:
                    for conflict in self.getProblem().getSubmission(submission).getSubmissionAttendeeConflictsList():
                        for session in range(self.getProblem().getNumberOfSessions()):
                            session_name = self.getProblem().getSession(session).getSessionName()
                            for room in range(self.getProblem().getNumberOfRooms()):
                                room_name = self.getProblem().getRoom(room).getRoomName()
                                current_conflict = [sub_name, conflict.getSubmissionName(), session_name, room_name]
                                M_list = [len(self.getProblem().getSubmission(submission).getSubmissionAttendeeConflictsList())+1, self.getProblem().getSession(session).getSessionMaxTimeSlots()]
                                M = min(M_list)
                                if sorted(current_conflict) not in unique_conflicts:
                                    unique_conflicts.append(sorted(current_conflict))
                                    temp = []
                                    temp2 = []
                                    for name in range(len(submission_att_conflict_x_list)):
                                        if (submission_att_conflict_x_list[name].split('|')[4] == sub_name and submission_att_conflict_x_list[name].split('|')[1] == session_name and submission_att_conflict_x_list[name].split('|')[2] == room_name):
                                            temp.append(submission_att_conflict_x_list[name])
                                        if (submission_att_conflict_x_list[name].split('|')[4] == conflict.getSubmissionName() and submission_att_conflict_x_list[name].split('|')[2] != room_name and submission_att_conflict_x_list[name].split('|')[1] == session_name):
                                            temp2.append(submission_att_conflict_x_list[name])
                                    model += lpSum([M * variables[x] for x in temp]) + lpSum([variables[x] for x in temp2]) <= M
        
        #Creating constraints Eq.16 & Eq.17 & Eq.18
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
                
        t_b = round((time() - t_b), 2)
        #Solving
        t_s = time()
        model.solve(GUROBI(msg = 1, MIPGap = 0, timeLimit = timelimit, IntegralityFocus = 1))
        #model.solve(GLPK_CMD(msg = 0))
        print('Building time:', t_b)
        print('Solving time:', round((time() - t_s), 2))
        print(model.objective.value())
        print("Model Status:", LpStatus[model.status])
        if LpStatus[model.status] == 'Infeasible':
            sys.exit(print('Model is Infeasible.'))
        solution = []
        for i in model.variables():
            if i.varValue > 0:
                solution.append(i.name)
        to_remove = []
        for i in range(len(solution)):
            if solution[i].split('|')[0] != 'Variables_':
                to_remove.append(solution[i])
        for i in to_remove:
            if i in solution:
                solution.remove(i)
        df = pd.DataFrame(solution)
        df.replace(to_replace = '_', value = ' ', regex = True, inplace = True)
        df = df.applymap(lambda x: x.split('|'))
        solution = df.iloc[:,0].to_list()
        for i in range(len(solution)):
            self.getSolution().getSolTracks()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])] = self.getProblem().getTrackIndex(solution[i][3])
            ts = self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])].index(-1)
            self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])][ts] = self.getProblem().getSubmissionIndex(solution[i][4])
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            for session in range(len(self.getSolution().getSolSubmissions())):
                for room in range(len(self.getSolution().getSolSubmissions()[session])):
                    if sub in self.getSolution().getSolSubmissions()[session][room]:
                        info = []
                        for i in range(len(self.getSolution().getSolSubmissions()[session][room])):
                            if self.getSolution().getSolSubmissions()[session][room][i] != -1:
                                if self.getSolution().getSolSubmissions()[session][room][i] not in info:
                                    info.append(self.getSolution().getSolSubmissions()[session][room][i])
                        temp = []
                        for i in range(len(info)):
                            while temp.count(info[i]) < self.getProblem().getSubmission(info[i]).getSubmissionRequiredTimeSlots():
                                temp.append(info[i])
                        while len(temp) < len(self.getSolution().getSolSubmissions()[session][room]):
                            temp.append(-1)
                        self.getSolution().getSolSubmissions()[session][room] = temp
                        
class HyperHeuristic(Optimisation):
    def __init__(self, problem, solution):
        Optimisation.__init__(self, problem, solution)
          
    def solve(self, start_time, run_time, rr = 600):
        LLHS = [lambda: self.SwapTrack(), lambda: self.SwapSubmission(), lambda: self.ReverseSubmission()]
        obj_best = self.getSolution().EvaluateSolution()
        obj = obj_best
        best_Sol = self.getSolution().copyWholeSolution()
        i = 0
        t = time()
        tt = rr
        while time() - start_time < run_time:
            i += 1
            select = np.random.randint(len(LLHS))
            sol_copy = self.getSolution().copyWholeSolution()
            LLHS[select]()
            self.getSolution().resetSolSubmissions()
            self.getSolution().convertSol()
            if self.getSolution().EvaluateAllSubmissionsScheduled() == True:
                obj_new = self.getSolution().QuickEvaluateSolution(obj)
                if obj_new <= obj:
                    obj = obj_new
                    if obj_new < obj_best:
                        best_Sol = self.getSolution().copyWholeSolution()
                        obj_best = obj_new
                else:
                    self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
            else:
                self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
            #Ruin & Recreate
            if time() - t > tt:
                s = 0
                while s != 10:
                    sol_copy = self.getSolution().copyWholeSolution()
                    LLHS[0]()
                    self.getSolution().resetSolSubmissions()
                    self.getSolution().convertSol()
                    if self.getSolution().EvaluateAllSubmissionsScheduled() == False:
                        self.getSolution().restoreSolution(sol_copy[0], sol_copy[1], sol_copy[2])
                    else:
                        s += 1
                obj = self.getSolution().EvaluateSolution()
                tt += rr
        self.getSolution().setBestSolution(best_Sol[0], best_Sol[1])
        print('Number of iterations:', i)

class Matheuristic(Optimisation):
    def __init__(self, problem, solution):
        Optimisation.__init__(self, problem, solution)
        
    def solve(self, start_time, run_time, timelimit = 90):
        self.TracksExactModel(timelimit)
        self.getSolution().convertIndSolFirstTime()
        solver = HyperHeuristic(self.getProblem(), self.getSolution())
        solver.solve(start_time, run_time)