# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:17:25 2023

@author: pylya
"""

from Solution import *
from pulp import *

class InitialSolution():
    def __init__(self, problem, solution):
        self.__solution = solution
        self.__problem = problem
        
    def getProblem(self) -> Problem:
        return self.__problem
    
    def getSolution(self) -> Solution:
        return self.__solution
    
    def RelaxedModel(self):
        model = LpProblem('model', LpMinimize)
        names = []
        add_names = []
        add2_names = []
        product_names = []
        coefficients = {}
        timeslots = {}
        #Creating decision variables
        for i in range(self.getProblem().getNumberOfSessions()):
            for t in range(self.getProblem().getSession(i).getMaxTimeSlots()):
                for j in range(self.getProblem().getNumberOfRooms()):
                    for z in range(self.getProblem().getNumberOfTracks()):
                        for x in range(len(self.getProblem().getTrack(z).getSubmissions())):
                            names.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x]))
                            #coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getSolution().getWeight(0) * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(1) * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getRoom(j).getName()) + self.getSolution().getWeight(2) * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getName(), self.getProblem().getRoom(j).getName()) + self.getSolution().getWeight(8) * self.getProblem().getSubmissionsTimezonesPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(10) * self.getProblem().getSubmissionsSessionsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(11) * self.getProblem().getSubmissionsRoomsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getRoom(j).getName())
                            coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getSolution().getWeight(8) * self.getProblem().getSubmissionsTimezonesPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(10) * self.getProblem().getSubmissionsSessionsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(11) * self.getProblem().getSubmissionsRoomsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getRoom(j).getName())
                            timeslots['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(z).getSubmissions()[x].getName())).getRequiredTimeSlots()
        
        #Additional variables to minimise tracks per room [Y Variable]
        for i in range(self.getProblem().getNumberOfTracks()):
            for j in range(self.getProblem().getNumberOfRooms()):
                add2_names.append('|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName())
                #coefficients['|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName()] = 1
                coefficients['|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName()] = self.getSolution().getWeight(1) * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(i).getName(), self.getProblem().getRoom(j).getName())
        
        #Additional variables for assigning 1 track into one room and session
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                for z in range(self.getProblem().getNumberOfTracks()):
                    add_names.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName())
                    #coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()] = 1
                    coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()] = self.getSolution().getWeight(0) * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(2) * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getName(), self.getProblem().getRoom(j).getName())
        '''
        #Determine MaxS for each track
        sessions_ts = []
        required_sessions = {}
        for session in range(self.getProblem().getNumberOfSessions()):
            sessions_ts.append(self.getProblem().getSession(session).getMaxTimeSlots())
        sorted_sessions_ts = sorted(sessions_ts)
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            i = -1
            while self.getProblem().getTrack(track).getRequiredTimeSlots() > sum(temp):
                i += 1
                temp.append(sorted_sessions_ts[i])
            required_sessions[str(track)] = len(temp)
        '''
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
                        coefficients['ptt_|' + str(i) + str(j) + str(session)] = 25 * self.getProblem().getTracksTracksPenaltybyIndex(i, j)
                    temp = [i]
    
        #Creating penalties for min number of rooms per track
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            pen.append('pmrt_|' + str(track))
            coefficients['pmrt_|' + str(track)] = 15
        
        #Creating penalties for parallel tracks
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and track_name == name.split('|')[3]:
                        temp.append(name)
                pen.append('ppt_|' + str(session) + str(track))
                coefficients['ppt_|' + str(session) + str(track)] = 25
        '''
        #Creating penalties for attendees conflicts [TS Level]
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            if len(self.getProblem().getSubmission(submission).getAttendeeConflicts()) != 0:
                for conflict in self.getProblem().getSubmission(submission).getAttendeeConflicts():
                    for session in range(self.getProblem().getNumberOfSessions()):
                        for t in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                            temp = []
                            for name in range(len(names)):
                                if (names[name].split('|')[5] == self.getProblem().getSubmission(submission).getName() and names[name].split('|')[1] == self.getProblem().getSession(session).getName() and names[name].split('|')[4] == 'Timeslot' + str(t)) or (names[name].split('|')[5] == conflict and names[name].split('|')[1] == self.getProblem().getSession(session).getName() and names[name].split('|')[4] == 'Timeslot' + str(t)):
                                    temp.append(names[name])
                            pen.append('pac_|' + str(session) + str(t))
                            coefficients['pac_|' + str(session) + str(t)] = 10
        '''
        #Creating objective function and binary IP formulation
        variables = LpVariable.dicts('Variables', names, cat = 'Binary')
        add_variables = LpVariable.dicts('AddVariables', add_names, cat = 'Binary')
        add2_variables = LpVariable.dicts('Add2Variables', add2_names, cat = 'Binary')
        product_variables = LpVariable.dicts('ProdVariables', product_names, cat = 'Binary')
        penalties = LpVariable.dicts('Penalties', pen, lowBound = 0, cat = 'Integer')
        obj_function = [variables, add_variables, add2_variables, product_variables, penalties]
        all_names = [names, add_names, add2_names, product_names, pen]
        model += lpSum([coefficients[i] * obj_function[x][i] for x in range(len(obj_function)) for i in all_names[x]])
        print('# Variables:', len(names) + len(add_names) + len(add2_names))
        constraints_count = 0
        
        #Creating Constraints: All submissions must be scheduled
        all_constraints = []
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            temp = []
            sub_name = self.getProblem().getSubmission(submission).getName()
            for name in range(len(names)):
                if names[name].split('|')[5] == sub_name:
                    temp.append(names[name])
            all_constraints.append(lpSum([variables[x] for x in temp]))
            constraints_count += 1
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        #Creating constraints: Assign only 1 track into one room and session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for room in range(self.getProblem().getNumberOfRooms()):
                room_name = self.getProblem().getRoom(room).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
                constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in range(len(names)):
                if track_name == names[name].split('|')[3]:
                    temp.append(names[name])
            for session in range(self.getProblem().getNumberOfSessions()):
                session_name = self.getProblem().getSession(session).getName()
                session_max_ts = self.getProblem().getSession(session).getMaxTimeSlots()
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp2 = []
                    room_name = self.getProblem().getRoom(room).getName()
                    for name in temp:
                        if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                            temp2.append(name)
                    for add_name in add_names:
                        if track_name == add_name.split('|')[3] and session_name == add_name.split('|')[1] and room_name == add_name.split('|')[2]:
                            add_var = add_name
                    all_constraints.append(lpSum([timeslots[x] * variables[x] for x in temp2]) - session_max_ts * add_variables[add_var])
                    constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in range(len(names)):
                if track_name == names[name].split('|')[3]:
                    temp.append(names[name])
            for session in range(self.getProblem().getNumberOfSessions()):
                session_name = self.getProblem().getSession(session).getName()
                session_max_ts = self.getProblem().getSession(session).getMaxTimeSlots()
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp2 = []
                    room_name = self.getProblem().getRoom(room).getName()
                    for name in temp:
                        if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                            temp2.append(name)
                    for add_name in add_names:
                        if track_name == add_name.split('|')[3] and session_name == add_name.split('|')[1] and room_name == add_name.split('|')[2]:
                            add_var = add_name
                    all_constraints.append(lpSum([timeslots[x] * variables[x] for x in temp2]) - add_variables[add_var])
                    constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] >= 0
        
        #Creating constraints: Min number of Rooms per Track
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            all_constraints.append(lpSum([add2_variables[x] for x in temp]) - penalties['pmrt_|' + str(track)])
            #all_constraints.append(lpSum([add2_variables[x] for x in temp]))
            constraints_count += 1
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        all_constraints = []
        for room in range(self.getProblem().getNumberOfRooms()):
            room_name = self.getProblem().getRoom(room).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                temp = []
                track_name = self.getProblem().getTrack(track).getName()
                for name in add_names:
                    if room_name == name.split('|')[2] and track_name == name.split('|')[3]:
                        temp.append(name)
                for name in add2_names:
                    if room_name == name.split('|')[1] and track_name == name.split('|')[2]:
                        temp.append(name)
                #all_constraints.append(lpSum([add_variables[temp[x]] for x in range(len(temp) - 1)]) - required_sessions[str(track)] * add2_variables[temp[len(temp) - 1]])
                all_constraints.append(lpSum([add_variables[temp[x]] for x in range(len(temp) - 1)]) - self.getProblem().getNumberOfSessions() * add2_variables[temp[len(temp) - 1]])
                constraints_count += 1
                    
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        #Creating constraints: Do not assign same track into same session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and track_name == name.split('|')[3]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[x] for x in temp]) - penalties['ppt_|' + str(session) + str(track)])
                #all_constraints.append(lpSum([add_variables[x] for x in temp]))
                constraints_count += 1
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating Constraints: Avoid Speaker Conflicts [Session Level]
        all_constraints = []
        unique_conflicts = []
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            sub_name = self.getProblem().getSubmission(submission).getName()
            sub_name_track = self.getProblem().getSubmission(submission).getTrack()
            if len(self.getProblem().getSubmission(submission).getSpeakerConflicts()) != 0:
                for conflict in self.getProblem().getSubmission(submission).getSpeakerConflicts():
                    conflict_track = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(conflict)).getTrack()
                    if conflict_track != sub_name_track:
                        for session in range(self.getProblem().getNumberOfSessions()):
                            current_conflict = [sub_name, conflict, self.getProblem().getSession(session).getName()]
                            if sorted(current_conflict) not in unique_conflicts:
                                unique_conflicts.append(sorted(current_conflict))
                                temp = []
                                session_name = self.getProblem().getSession(session).getName()
                                for name in range(len(names)):
                                    if (names[name].split('|')[5] == sub_name and names[name].split('|')[1] == session_name) or (names[name].split('|')[5] == conflict and names[name].split('|')[1] == session_name):
                                        temp.append(names[name])
                                all_constraints.append(lpSum([variables[x] for x in temp]))
                                constraints_count += 1
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints: Only 1 submission can be scheduled per timeslot
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for room in range(self.getProblem().getNumberOfRooms()):
                room_name = self.getProblem().getRoom(room).getName()
                for t in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                    temp = []
                    for name in range(len(names)):
                        if session_name == names[name].split('|')[1] and room_name == names[name].split('|')[2] and 'Timeslot'+str(t) == names[name].split('|')[4]:
                            temp.append(names[name])
                    all_constraints.append(lpSum([variables[x] for x in temp]))
                    constraints_count += 1
                    
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        '''
        #Additional constraints
        #Creating Constraints: Avoid Attendee Conflicts [Time slot Level]        
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            if len(self.getProblem().getSubmission(submission).getAttendeeConflicts()) != 0:
                for conflict in self.getProblem().getSubmission(submission).getAttendeeConflicts():
                    for session in range(self.getProblem().getNumberOfSessions()):
                        for t in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                            temp = []
                            for name in range(len(names)):
                                if (names[name].split('|')[5] == self.getProblem().getSubmission(submission).getName() and names[name].split('|')[1] == self.getProblem().getSession(session).getName() and names[name].split('|')[4] == 'Timeslot' + str(t)) or (names[name].split('|')[5] == conflict and names[name].split('|')[1] == self.getProblem().getSession(session).getName() and names[name].split('|')[4] == 'Timeslot' + str(t)):
                                    temp.append(names[name])
                            #model += lpSum([variables[x] for x in temp]) <= 1
                            model += lpSum(variables[x] for x in temp) - penalties['pac_|' + str(session) + str(t)] <= 1
                            constraints_count += 1
        '''           
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
                        session_name = self.getProblem().getSession(session).getName()
                        temp2 = []
                        for name in range(len(add_names)):
                            for z in range(len(temp)):
                                if add_names[name].split('|')[1] == session_name and add_names[name].split('|')[3] == self.getProblem().getTrack(temp[z]).getName():
                                    temp2.append(add_names[name])
                        all_constraints.append(lpSum([add_variables[x] for x in temp2]) - penalties['ptt_|' + str(i) + str(j) + str(session)])
                        #all_constraints.append(lpSum([add_variables[x] for x in temp2]))
                        constraints_count += 1
                    temp = [i]
                        
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
                constraints_count += 3
                    
        for c in range(len(all_constraints1)):
            model += all_constraints1[c] >= -1
            
        for c in range(len(all_constraints2)):
            model += all_constraints2[c] <= 0
        
        print('# Constraints:', constraints_count)
        #Solving
        stime = time()
        model.solve(GUROBI(msg = 1, MIPGap = 0, IntegralityFocus = 1, timeLimit = 3600)) #StartNodeLimit / TuneTimeLimit / timeLimit / threads
        #model.solve(CPLEX_PY(msg = 1, timeLimit = 900))
        #if LpStatus[model.status] == 'Infeasible':
        #    model.solverModel.computeIIS()
        #    sys.exit(model.solverModel.write("Infeasible_Constraints.ilp"))
        print('BIP Solving time:', round((time() - stime) / 60, 2))
        print(model.objective.value())
        print("Model Status:", LpStatus[model.status])
        solution = []
        '''
        for i in model.variables():
            if i.varValue > 0:
                solution.append(i.name)
        '''
        gur_vars = model.solverModel.getVars()
        for i in gur_vars:
            if i.X > 0:
                solution.append(i.varName)
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
            self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])][int(solution[i][4].split('t')[1])] = self.getProblem().getSubmissionIndex(solution[i][5])
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            if self.getProblem().getSubmission(sub).getRequiredTimeSlots() > 1:
                for session in range(len(self.getSolution().getSolSubmissions())):
                    for room in range(len(self.getSolution().getSolSubmissions()[session])):
                        if sub in self.getSolution().getSolSubmissions()[session][room]:
                            info = []
                            for i in range(len(self.getSolution().getSolSubmissions()[session][room])):
                                if self.getSolution().getSolSubmissions()[session][room][i] != -1:
                                    if (self.getSolution().getSolSubmissions()[session][room][i], self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[session][room][i]).getOrder()) not in info:
                                        info.append((self.getSolution().getSolSubmissions()[session][room][i], self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[session][room][i]).getOrder()))
                            sorted_info = sorted(info, key = lambda x: x[1])
                            temp = []
                            for i in range(len(sorted_info)):
                                while temp.count(sorted_info[i][0]) < self.getProblem().getSubmission(sorted_info[i][0]).getRequiredTimeSlots():
                                    temp.append(sorted_info[i][0])
                            while len(temp) < len(self.getSolution().getSolSubmissions()[session][room]):
                                temp.append(-1)
                            self.getSolution().getSolSubmissions()[session][room] = temp

    def BasicModel(self):
        model = LpProblem('model', LpMinimize)
        names = []
        add_names = []
        add2_names = []
        product_names = []
        coefficients = {}
        timeslots = {}
        #Creating decision variables
        for i in range(self.getProblem().getNumberOfSessions()):
            for t in range(self.getProblem().getSession(i).getMaxTimeSlots()):
                for j in range(self.getProblem().getNumberOfRooms()):
                    for z in range(self.getProblem().getNumberOfTracks()):
                        for x in range(len(self.getProblem().getTrack(z).getSubmissions())):
                            names.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x]))
                            #coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getSolution().getWeight(0) * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(1) * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getRoom(j).getName()) + self.getSolution().getWeight(2) * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getName(), self.getProblem().getRoom(j).getName()) + self.getSolution().getWeight(8) * self.getProblem().getSubmissionsTimezonesPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(10) * self.getProblem().getSubmissionsSessionsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(11) * self.getProblem().getSubmissionsRoomsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getRoom(j).getName())
                            coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getSolution().getWeight(8) * self.getProblem().getSubmissionsTimezonesPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(10) * self.getProblem().getSubmissionsSessionsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(11) * self.getProblem().getSubmissionsRoomsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getRoom(j).getName())
                            timeslots['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(z).getSubmissions()[x].getName())).getRequiredTimeSlots()
        
        #Additional variables to minimise tracks per room [Y Variable]
        for i in range(self.getProblem().getNumberOfTracks()):
            for j in range(self.getProblem().getNumberOfRooms()):
                add2_names.append('|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName())
                #coefficients['|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName()] = 1
                coefficients['|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName()] = self.getSolution().getWeight(1) * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(i).getName(), self.getProblem().getRoom(j).getName())
        
        #Additional variables for assigning 1 track into one room and session
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                for z in range(self.getProblem().getNumberOfTracks()):
                    add_names.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName())
                    #coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()] = 1
                    coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()] = self.getSolution().getWeight(0) * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(2) * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getName(), self.getProblem().getRoom(j).getName())
        
        #Determine MaxS for each track
        sessions_ts = []
        required_sessions = {}
        for session in range(self.getProblem().getNumberOfSessions()):
            sessions_ts.append(self.getProblem().getSession(session).getMaxTimeSlots())
        sorted_sessions_ts = sorted(sessions_ts)
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            i = -1
            while self.getProblem().getTrack(track).getRequiredTimeSlots() > sum(temp):
                i += 1
                temp.append(sorted_sessions_ts[i])
            required_sessions[str(track)] = len(temp)
        
        #Creating objective function and binary IP formulation
        variables = LpVariable.dicts('Variables', names, cat = 'Binary')
        add_variables = LpVariable.dicts('AddVariables', add_names, cat = 'Binary')
        add2_variables = LpVariable.dicts('Add2Variables', add2_names, cat = 'Binary')
        obj_function = [variables, add_variables, add2_variables]#[variables, add_variables, add2_variables, slack_variables]
        all_names = [names, add_names, add2_names]#[names, add_names, add2_names, slack_vars]
        model += lpSum([coefficients[i] * obj_function[x][i] for x in range(len(obj_function)) for i in all_names[x]])
        print('# Variables:', len(names) + len(add_names) + len(add2_names))
        constraints_count = 0
        
        #Creating constraints: Assign only 1 track into one room and session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for room in range(self.getProblem().getNumberOfRooms()):
                room_name = self.getProblem().getRoom(room).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
                constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in range(len(names)):
                if track_name == names[name].split('|')[3]:
                    temp.append(names[name])
            for session in range(self.getProblem().getNumberOfSessions()):
                session_name = self.getProblem().getSession(session).getName()
                session_max_ts = self.getProblem().getSession(session).getMaxTimeSlots()
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp2 = []
                    room_name = self.getProblem().getRoom(room).getName()
                    for name in temp:
                        if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                            temp2.append(name)
                    for add_name in add_names:
                        if track_name == add_name.split('|')[3] and session_name == add_name.split('|')[1] and room_name == add_name.split('|')[2]:
                            add_var = add_name
                    all_constraints.append(lpSum([timeslots[x] * variables[x] for x in temp2]) - session_max_ts * add_variables[add_var])
                    constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in range(len(names)):
                if track_name == names[name].split('|')[3]:
                    temp.append(names[name])
            for session in range(self.getProblem().getNumberOfSessions()):
                session_name = self.getProblem().getSession(session).getName()
                session_max_ts = self.getProblem().getSession(session).getMaxTimeSlots()
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp2 = []
                    room_name = self.getProblem().getRoom(room).getName()
                    for name in temp:
                        if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                            temp2.append(name)
                    for add_name in add_names:
                        if track_name == add_name.split('|')[3] and session_name == add_name.split('|')[1] and room_name == add_name.split('|')[2]:
                            add_var = add_name
                    all_constraints.append(lpSum([timeslots[x] * variables[x] for x in temp2]) - add_variables[add_var])
                    constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] >= 0
        
        #Creating constraints: Min number of Rooms per Track
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            all_constraints.append(lpSum([add2_variables[x] for x in temp]))
            constraints_count += 1
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        all_constraints = []
        for room in range(self.getProblem().getNumberOfRooms()):
            room_name = self.getProblem().getRoom(room).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                temp = []
                track_name = self.getProblem().getTrack(track).getName()
                for name in add_names:
                    if room_name == name.split('|')[2] and track_name == name.split('|')[3]:
                        temp.append(name)
                for name in add2_names:
                    if room_name == name.split('|')[1] and track_name == name.split('|')[2]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[temp[x]] for x in range(len(temp) - 1)]) - required_sessions[str(track)] * add2_variables[temp[len(temp) - 1]])
                #all_constraints.append(lpSum([add_variables[temp[x]] for x in range(len(temp) - 1)]) - self.getProblem().getNumberOfSessions() * add2_variables[temp[len(temp) - 1]])
                constraints_count += 1
                    
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        #Creating Constraints: All submissions must be scheduled
        all_constraints = []
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            temp = []
            sub_name = self.getProblem().getSubmission(submission).getName()
            for name in range(len(names)):
                if names[name].split('|')[5] == sub_name:
                    temp.append(names[name])
            all_constraints.append(lpSum([variables[x] for x in temp]))
            constraints_count += 1
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        #Creating constraints: Do not assign same track into same session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and track_name == name.split('|')[3]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
                constraints_count += 1
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating Constraints: Avoid Speaker Conflicts [Session Level]
        all_constraints = []
        unique_conflicts = []
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            sub_name = self.getProblem().getSubmission(submission).getName()
            sub_name_track = self.getProblem().getSubmission(submission).getTrack()
            if len(self.getProblem().getSubmission(submission).getSpeakerConflicts()) != 0:
                for conflict in self.getProblem().getSubmission(submission).getSpeakerConflicts():
                    conflict_track = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(conflict)).getTrack()
                    if conflict_track != sub_name_track:
                        for session in range(self.getProblem().getNumberOfSessions()):
                            current_conflict = [sub_name, conflict, self.getProblem().getSession(session).getName()]
                            if sorted(current_conflict) not in unique_conflicts:
                                unique_conflicts.append(sorted(current_conflict))
                                temp = []
                                session_name = self.getProblem().getSession(session).getName()
                                for name in range(len(names)):
                                    if (names[name].split('|')[5] == sub_name and names[name].split('|')[1] == session_name) or (names[name].split('|')[5] == conflict and names[name].split('|')[1] == session_name):
                                        temp.append(names[name])
                                all_constraints.append(lpSum([variables[x] for x in temp]))
                                constraints_count += 1
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints: Only 1 submission can be scheduled per timeslot
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for room in range(self.getProblem().getNumberOfRooms()):
                room_name = self.getProblem().getRoom(room).getName()
                for t in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                    temp = []
                    for name in range(len(names)):
                        if session_name == names[name].split('|')[1] and room_name == names[name].split('|')[2] and 'Timeslot'+str(t) == names[name].split('|')[4]:
                            temp.append(names[name])
                    all_constraints.append(lpSum([variables[x] for x in temp]))
                    constraints_count += 1
                    
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        '''
        #Additional constraints
        #Creating Constraints: Avoid Attendee Conflicts [Time slot Level]        
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            if len(self.getProblem().getSubmission(submission).getAttendeeConflicts()) != 0:
                for conflict in self.getProblem().getSubmission(submission).getAttendeeConflicts():
                    for session in range(self.getProblem().getNumberOfSessions()):
                        for t in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                            temp = []
                            for name in range(len(names)):
                                if (names[name].split('|')[5] == self.getProblem().getSubmission(submission).getName() and names[name].split('|')[1] == self.getProblem().getSession(session).getName() and names[name].split('|')[4] == 'Timeslot' + str(t)) or (names[name].split('|')[5] == conflict and names[name].split('|')[1] == self.getProblem().getSession(session).getName() and names[name].split('|')[4] == 'Timeslot' + str(t)):
                                    temp.append(names[name])
                            model += lpSum([variables[x] for x in temp]) <= 1
                            #model += lpSum(variables[x] for x in temp) - len(temp) * variables['pac_|' + str(t)] <= 1
                            constraints_count += 1
                            
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
                    session_name = self.getProblem().getSession(session).getName()
                    temp2 = []
                    for name in range(len(add_names)):
                        for z in range(len(temp)):
                            if add_names[name].split('|')[1] == session_name and add_names[name].split('|')[3] == self.getProblem().getTrack(temp[z]).getName():
                                temp2.append(add_names[name])
                    #all_constraints.append(lpSum([add_variables[x] for x in temp2]) - penalties['ptt_|' + str(i) + str(j)])
                    all_constraints.append(lpSum([add_variables[x] for x in temp2]))
                    constraints_count += 1
                        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        '''
        print('# Constraints:', constraints_count)
        #Solving
        stime = time()
        model.solve(GUROBI(msg = 1, MIPGap = 0, timeLimit = 18000)) #StartNodeLimit / TuneTimeLimit / timeLimit / threads
        #model.solve(CPLEX_PY(msg = 1, timeLimit = 900))
        #if LpStatus[model.status] == 'Infeasible':
        #    model.solverModel.computeIIS()
        #    sys.exit(model.solverModel.write("Infeasible_Constraints.ilp"))
        print('BIP Solving time:', round((time() - stime) / 60, 2))
        print(model.objective.value())
        print("Model Status:", LpStatus[model.status])
        solution = []
        '''
        for i in model.variables():
            if i.varValue > 0:
                solution.append(i.name)
        '''
        gur_vars = model.solverModel.getVars()
        for i in gur_vars:
            if i.X > 0:
                solution.append(i.varName)
        to_remove = []
        for i in range(len(solution)):
            if solution[i].split('|')[0] != 'Variables_':
                to_remove.append(solution[i])
        for i in product_names:
            to_remove.append(str(variables[i]))
        for i in to_remove:
            if i in solution:
                solution.remove(i)
        df = pd.DataFrame(solution)
        df.replace(to_replace = '_', value = ' ', regex = True, inplace = True)
        df = df.applymap(lambda x: x.split('|'))
        solution = df.iloc[:,0].to_list()
        for i in range(len(solution)):
            self.getSolution().getSolTracks()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])] = self.getProblem().getTrackIndex(solution[i][3])
            self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])][int(solution[i][4].split('t')[1])] = self.getProblem().getSubmissionIndex(solution[i][5])
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            #if self.getProblem().getSubmission(sub).getRequiredTimeSlots() > 1:
            for session in range(len(self.getSolution().getSolSubmissions())):
                for room in range(len(self.getSolution().getSolSubmissions()[session])):
                    if sub in self.getSolution().getSolSubmissions()[session][room]:
                        info = []
                        for i in range(len(self.getSolution().getSolSubmissions()[session][room])):
                            if self.getSolution().getSolSubmissions()[session][room][i] != -1:
                                if (self.getSolution().getSolSubmissions()[session][room][i], self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[session][room][i]).getOrder()) not in info:
                                    info.append((self.getSolution().getSolSubmissions()[session][room][i], self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[session][room][i]).getOrder()))
                        sorted_info = sorted(info, key = lambda x: x[1])
                        temp = []
                        for i in range(len(sorted_info)):
                            while temp.count(sorted_info[i][0]) < self.getProblem().getSubmission(sorted_info[i][0]).getRequiredTimeSlots():
                                temp.append(sorted_info[i][0])
                        while len(temp) < len(self.getSolution().getSolSubmissions()[session][room]):
                            temp.append(-1)
                        self.getSolution().getSolSubmissions()[session][room] = temp
                              
    def AdvancedModel(self):
        model = LpProblem('model', LpMinimize)
        names = []
        add_names = []
        add2_names = []
        product_names = []
        coefficients = {}
        timeslots = {}
        save_time = 0
        save_time2 = 0
        #Creating decision variables
        for i in range(self.getProblem().getNumberOfSessions()):
            for t in range(self.getProblem().getSession(i).getMaxTimeSlots()):
                for j in range(self.getProblem().getNumberOfRooms()):
                    for z in range(self.getProblem().getNumberOfTracks()):
                        for x in range(len(self.getProblem().getTrack(z).getSubmissions())):
                            names.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x]))
                            #coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getSolution().getWeight(0) * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(1) * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getRoom(j).getName()) + self.getSolution().getWeight(2) * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getName(), self.getProblem().getRoom(j).getName()) + self.getSolution().getWeight(8) * self.getProblem().getSubmissionsTimezonesPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(10) * self.getProblem().getSubmissionsSessionsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(11) * self.getProblem().getSubmissionsRoomsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getRoom(j).getName())
                            coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getSolution().getWeight(8) * self.getProblem().getSubmissionsTimezonesPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(10) * self.getProblem().getSubmissionsSessionsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(11) * self.getProblem().getSubmissionsRoomsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getRoom(j).getName())
                            timeslots['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(z).getSubmissions()[x].getName())).getRequiredTimeSlots()
            
        #Additional variables to minimise tracks per room [Y Variable]
        for i in range(self.getProblem().getNumberOfTracks()):
            for j in range(self.getProblem().getNumberOfRooms()):
                add2_names.append('|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName())
                #coefficients['|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName()] = 1
                coefficients['|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName()] = self.getSolution().getWeight(1) * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(i).getName(), self.getProblem().getRoom(j).getName())
        
        #Additional variables for assigning 1 track into one room and session
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                for z in range(self.getProblem().getNumberOfTracks()):
                    add_names.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName())
                    #coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()] = 1
                    coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()] = self.getSolution().getWeight(0) * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(2) * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getName(), self.getProblem().getRoom(j).getName())
        
        #Determine MaxS for each track
        sessions_ts = []
        required_sessions = {}
        for session in range(self.getProblem().getNumberOfSessions()):
            sessions_ts.append(self.getProblem().getSession(session).getMaxTimeSlots())
        sorted_sessions_ts = sorted(sessions_ts)
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            i = -1
            while self.getProblem().getTrack(track).getRequiredTimeSlots() > sum(temp):
                i += 1
                temp.append(sorted_sessions_ts[i])
            required_sessions[str(track)] = len(temp)
        
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
                                
        #Creating products of variables for submissions scheduling in order
        for i in range(self.getProblem().getNumberOfTracks()):
            temp = []
            for j in range(len(self.getProblem().getTrack(i).getSubmissions())):
                if self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(i).getSubmissions()[j].getName())).getOrder() != 0:
                    temp.append(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(i).getSubmissions()[j].getName()))
                    if self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(i).getSubmissions()[j].getName())).getRequiredTimeSlots() > 1:
                        for t in range(self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(i).getSubmissions()[j].getName())).getRequiredTimeSlots() - 1):
                            temp.append(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(i).getSubmissions()[j].getName()))
            sorted_temp = []
            order = 0
            while len(sorted_temp) != len(temp):
                order += 1
                for x in temp:
                    if self.getProblem().getSubmission(x).getOrder() == order:
                        sorted_temp.append(x)
            for submission in range(len(sorted_temp) - 1):
                tempa = []
                tempb = []
                if sorted_temp[submission] != sorted_temp[submission + 1] and self.getProblem().getSubmission(sorted_temp[submission]).getRequiredTimeSlots() == 1 and self.getProblem().getSubmission(sorted_temp[submission + 1]).getRequiredTimeSlots() == 1:
                    for name in range(len(names)):
                        if self.getProblem().getSubmission(sorted_temp[submission]).getName() == names[name].split('|')[5]:
                            tempa.append(names[name])
                        if self.getProblem().getSubmission(sorted_temp[submission + 1]).getName() == names[name].split('|')[5]:
                            tempb.append(names[name])
                    for s in range(len(tempa) - self.getProblem().getNumberOfRooms()):
                        tempc = tempa[s] + tempb[s + self.getProblem().getNumberOfRooms()]
                        product_names.append(tempc)
                        coefficients[tempc] = -10
        '''
        pen = []
        #Creating penalties for tracktrack penalty
        for i in range(self.getProblem().getNumberOfTracks()):
            temp = [i]
            for j in range(i, self.getProblem().getNumberOfTracks()):
                if i != j:
                    if self.getProblem().getTracksTracksPenaltybyIndex(i, j) != 0:
                        temp.append(j)
            if len(temp) > 1:
                pen.append('ptt_|' + str(i) + str(j))
                coefficients['ptt_|' + str(i) + str(j)] = 100
        
        
        #Creating penalties for min number of rooms per track
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            pen.append('pmrt_|' + str(track))
            coefficients['pmrt_|' + str(track)] = 10000
        
        #Creating penalties for parallel tracks
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and track_name == name.split('|')[3]:
                        temp.append(name)
                pen.append('ppt_|' + str(session) + str(track))
                coefficients['ppt_|' + str(session) + str(track)] = 1000
        
        for i in product_names:
            names.append(i)
        '''  
        #Creating objective function and binary IP formulation
        variables = LpVariable.dicts('Variables', names, cat = 'Binary')
        add_variables = LpVariable.dicts('AddVariables', add_names, cat = 'Binary')
        add2_variables = LpVariable.dicts('Add2Variables', add2_names, cat = 'Binary')
        product_variables = LpVariable.dicts('ProdVariables', product_names, cat = 'Binary')
        #penalties = LpVariable.dicts('Penalties', pen, lowBound = 0, cat = 'Integer')
        obj_function = [variables, add_variables, add2_variables, product_variables]#[variables, add_variables, add2_variables, penalties]
        all_names = [names, add_names, add2_names, product_names]#[names, add_names, add2_names, pen]
        model += lpSum([coefficients[i] * obj_function[x][i] for x in range(len(obj_function)) for i in all_names[x]])
        print('# Variables:', len(names) + len(add_names) + len(add2_names) + len(product_names))
        constraints_count = 0
        
        #for i in product_names:
        #    names.remove(i)
          
        #Creating constraints: Assign only 1 track into one room and session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for room in range(self.getProblem().getNumberOfRooms()):
                room_name = self.getProblem().getRoom(room).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
                constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in range(len(names)):
                if track_name == names[name].split('|')[3]:
                    temp.append(names[name])
            for session in range(self.getProblem().getNumberOfSessions()):
                session_name = self.getProblem().getSession(session).getName()
                session_max_ts = self.getProblem().getSession(session).getMaxTimeSlots()
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp2 = []
                    room_name = self.getProblem().getRoom(room).getName()
                    for name in temp:
                        if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                            temp2.append(name)
                    for add_name in add_names:
                        if track_name == add_name.split('|')[3] and session_name == add_name.split('|')[1] and room_name == add_name.split('|')[2]:
                            add_var = add_name
                    all_constraints.append(lpSum([timeslots[x] * variables[x] for x in temp2]) - session_max_ts * add_variables[add_var])
                    constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in range(len(names)):
                if track_name == names[name].split('|')[3]:
                    temp.append(names[name])
            for session in range(self.getProblem().getNumberOfSessions()):
                session_name = self.getProblem().getSession(session).getName()
                session_max_ts = self.getProblem().getSession(session).getMaxTimeSlots()
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp2 = []
                    room_name = self.getProblem().getRoom(room).getName()
                    for name in temp:
                        if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                            temp2.append(name)
                    for add_name in add_names:
                        if track_name == add_name.split('|')[3] and session_name == add_name.split('|')[1] and room_name == add_name.split('|')[2]:
                            add_var = add_name
                    all_constraints.append(lpSum([timeslots[x] * variables[x] for x in temp2]) - add_variables[add_var])
                    constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] >= 0
        
        #Creating constraints: Min number of Rooms per Track
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            #all_constraints.append(lpSum([add2_variables[x] for x in temp]) - penalties['pmrt_|' + str(track)])
            all_constraints.append(lpSum([add2_variables[x] for x in temp]))
            constraints_count += 1
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        all_constraints = []
        for room in range(self.getProblem().getNumberOfRooms()):
            room_name = self.getProblem().getRoom(room).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                temp = []
                track_name = self.getProblem().getTrack(track).getName()
                for name in add_names:
                    if room_name == name.split('|')[2] and track_name == name.split('|')[3]:
                        temp.append(name)
                for name in add2_names:
                    if room_name == name.split('|')[1] and track_name == name.split('|')[2]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[temp[x]] for x in range(len(temp) - 1)]) - required_sessions[str(track)] * add2_variables[temp[len(temp) - 1]])
                #all_constraints.append(lpSum([add_variables[temp[x]] for x in range(len(temp) - 1)]) - self.getProblem().getNumberOfSessions() * add2_variables[temp[len(temp) - 1]])
                constraints_count += 1
                    
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        #Creating Constraints: All submissions must be scheduled
        all_constraints = []
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            temp = []
            req_ts = 1
            sub_req_ts = self.getProblem().getSubmission(submission).getRequiredTimeSlots()
            sub_name = self.getProblem().getSubmission(submission).getName()
            for name in range(len(names)):
                if names[name].split('|')[5] == sub_name:
                    temp.append(names[name])
            all_constraints.append(lpSum([variables[x] for x in temp]))
            constraints_count += 1
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        #Creating constraints: Do not assign same track into same session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and track_name == name.split('|')[3]:
                        temp.append(name)
                #all_constraints.append(lpSum([add_variables[x] for x in temp]) - penalties['ppt_|' + str(session) + str(track)])
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
                constraints_count += 1
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating Constraints: Avoid Speaker Conflicts [Session Level]
        all_constraints = []
        unique_conflicts = []
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            sub_name = self.getProblem().getSubmission(submission).getName()
            sub_name_track = self.getProblem().getSubmission(submission).getTrack()
            if len(self.getProblem().getSubmission(submission).getSpeakerConflicts()) != 0:
                for conflict in self.getProblem().getSubmission(submission).getSpeakerConflicts():
                    conflict_track = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(conflict)).getTrack()
                    if conflict_track != sub_name_track:
                        for session in range(self.getProblem().getNumberOfSessions()):
                            current_conflict = [sub_name, conflict, self.getProblem().getSession(session).getName()]
                            if sorted(current_conflict) not in unique_conflicts:
                                unique_conflicts.append(sorted(current_conflict))
                                temp = []
                                session_name = self.getProblem().getSession(session).getName()
                                for name in range(len(names)):
                                    if (names[name].split('|')[5] == sub_name and names[name].split('|')[1] == session_name) or (names[name].split('|')[5] == conflict and names[name].split('|')[1] == session_name):
                                        temp.append(names[name])
                                all_constraints.append(lpSum([variables[x] for x in temp]))
                                constraints_count += 1
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints: Only 1 submission can be scheduled per timeslot
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for room in range(self.getProblem().getNumberOfRooms()):
                room_name = self.getProblem().getRoom(room).getName()
                for t in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                    temp = []
                    for name in range(len(names)):
                        if session_name == names[name].split('|')[1] and room_name == names[name].split('|')[2] and 'Timeslot'+str(t) == names[name].split('|')[4]:
                            temp.append(names[name])
                    all_constraints.append(lpSum([variables[x] for x in temp]))
                    constraints_count += 1
                    
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
                    session_name = self.getProblem().getSession(session).getName()
                    temp2 = []
                    for name in range(len(add_names)):
                        for z in range(len(temp)):
                            if add_names[name].split('|')[1] == session_name and add_names[name].split('|')[3] == self.getProblem().getTrack(temp[z]).getName():
                                temp2.append(add_names[name])
                    #all_constraints.append(lpSum([add_variables[x] for x in temp2]) - penalties['ptt_|' + str(i) + str(j)])
                    all_constraints.append(lpSum([add_variables[x] for x in temp2]))
                    constraints_count += 1
                        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints: Consider organizer conflicts
        all_constraints = []
        temp2 = []
        for z in range(self.getProblem().getNumberOfTracks()):
            if len(self.getProblem().getTrack(z).getOrganizerConflicts()) != 0:
                for i in range(self.getProblem().getNumberOfSessions()):
                    temp = []
                    for j in range(self.getProblem().getNumberOfRooms()):        
                        temp.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName())
                        for x in self.getProblem().getTrack(z).getOrganizerConflicts():
                            temp.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+x)
                    if sorted(temp) not in temp2:
                        temp2.append(sorted(temp))
        for i in range(len(temp2)):
            all_constraints.append(lpSum([add_variables[x] for x in temp2[i]]))
            constraints_count += 1
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        '''
        #Creating Constraints: Avoid Attendee Conflicts [Session Level]        
        all_constraints = []
        unique_conflicts = []
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            sub_name = self.getProblem().getSubmission(submission).getName()
            sub_name_track = self.getProblem().getSubmission(submission).getTrack()
            if len(self.getProblem().getSubmission(submission).getAttendeeConflicts()) != 0:
                for conflict in self.getProblem().getSubmission(submission).getAttendeeConflicts():
                    conflict_track = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(conflict)).getTrack()
                    if conflict_track != sub_name_track:
                        for session in range(self.getProblem().getNumberOfSessions()):
                            current_conflict = [sub_name, conflict, self.getProblem().getSession(session).getName()]
                            if sorted(current_conflict) not in unique_conflicts:
                                unique_conflicts.append(sorted(current_conflict))
                                temp = []
                                for name in range(len(names)):
                                    if (names[name].split('|')[5] == self.getProblem().getSubmission(submission).getName() and names[name].split('|')[1] == self.getProblem().getSession(session).getName()) or (names[name].split('|')[5] == conflict and names[name].split('|')[1] == self.getProblem().getSession(session).getName()):
                                        temp.append(names[name])
                                all_constraints.append(lpSum([variables[x] for x in temp]))
                                constraints_count += 1
                            
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        '''
        #Creating Constraints: Avoid Attendee Conflicts [Time slot Level]        
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            if len(self.getProblem().getSubmission(submission).getAttendeeConflicts()) != 0:
                for conflict in self.getProblem().getSubmission(submission).getAttendeeConflicts():
                    for session in range(self.getProblem().getNumberOfSessions()):
                        for t in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                            temp = []
                            for name in range(len(names)):
                                if (names[name].split('|')[5] == self.getProblem().getSubmission(submission).getName() and names[name].split('|')[1] == self.getProblem().getSession(session).getName() and names[name].split('|')[4] == 'Timeslot' + str(t)) or (names[name].split('|')[5] == conflict and names[name].split('|')[1] == self.getProblem().getSession(session).getName() and names[name].split('|')[4] == 'Timeslot' + str(t)):
                                    temp.append(names[name])
                            model += lpSum([variables[x] for x in temp]) <= 1
                            #model += lpSum(variables[x] for x in temp) - len(temp) * variables['pac_|' + str(t)] <= 1
                            constraints_count += 1
        
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
                constraints_count += 3
                    
        for c in range(len(all_constraints1)):
            model += all_constraints1[c] >= -1
            
        for c in range(len(all_constraints2)):
            model += all_constraints2[c] <= 0
        
        #Creating Constraints: Assign submissions in order
        all_constraints1 = []
        all_constraints2 = []
        for i in range(self.getProblem().getNumberOfTracks()):
            temp = []
            for j in range(len(self.getProblem().getTrack(i).getSubmissions())):
                if self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(i).getSubmissions()[j].getName())).getOrder() != 0:
                    temp.append(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(i).getSubmissions()[j].getName()))
                    if self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(i).getSubmissions()[j].getName())).getRequiredTimeSlots() > 1:
                        for t in range(self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(i).getSubmissions()[j].getName())).getRequiredTimeSlots() - 1):
                            temp.append(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(i).getSubmissions()[j].getName()))
            sorted_temp = []
            order = 0
            while len(sorted_temp) != len(temp):
                order += 1
                for x in temp:
                    if self.getProblem().getSubmission(x).getOrder() == order:
                        sorted_temp.append(x)
            for submission in range(len(sorted_temp) - 1):
                tempa = []
                tempb = []
                if sorted_temp[submission] != sorted_temp[submission + 1] and self.getProblem().getSubmission(sorted_temp[submission]).getRequiredTimeSlots() == 1 and self.getProblem().getSubmission(sorted_temp[submission + 1]).getRequiredTimeSlots() == 1:
                    for name in range(len(names)):
                        if self.getProblem().getSubmission(sorted_temp[submission]).getName() == names[name].split('|')[5]:
                            tempa.append(names[name])
                        if self.getProblem().getSubmission(sorted_temp[submission + 1]).getName() == names[name].split('|')[5]:
                            tempb.append(names[name])
                    for s in range(len(tempa) - self.getProblem().getNumberOfRooms()):
                        tempc = tempa[s] + tempb[s + self.getProblem().getNumberOfRooms()]
                        all_constraints2.append(product_variables[tempc] - variables[tempa[s]])
                        all_constraints2.append(product_variables[tempc] - variables[tempb[s + self.getProblem().getNumberOfRooms()]])
                        all_constraints1.append(product_variables[tempc] - variables[tempa[s]] - variables[tempb[s + self.getProblem().getNumberOfRooms()]])
                        constraints_count += 3
                        
        for c in range(len(all_constraints1)):
            model += all_constraints1[c] >= -1
                
        for c in range(len(all_constraints2)):
            model += all_constraints2[c] <= 0
        
        print('# Constraints:', constraints_count)
        
        #Solving
        stime = time()
        model.solve(GUROBI(msg = 1, MIPGap = 0, timeLimit = 18000, IntegralityFocus = 1)) #StartNodeLimit / TuneTimeLimit / timeLimit / threads
        #model.solve(CPLEX_PY(msg = 1, timeLimit = 900))
        print('BIP Solving time:', round((time() - stime) / 60, 2))
        print(model.objective.value())
        print("Model Status:", LpStatus[model.status])
        solution = []
        '''
        for i in model.variables():
            if i.varValue > 0:
                solution.append(i.name)
        '''
        gur_vars = model.solverModel.getVars()
        for i in gur_vars:
            if i.X > 0:
                solution.append(i.varName)
        to_remove = []
        for i in range(len(solution)):
            if solution[i].split('|')[0] != 'Variables_':
                to_remove.append(solution[i])
        #for i in product_names:
            #to_remove.append(str(variables[i]))
        for i in to_remove:
            if i in solution:
                solution.remove(i)
        df = pd.DataFrame(solution)
        df.replace(to_replace = '_', value = ' ', regex = True, inplace = True)
        df = df.applymap(lambda x: x.split('|'))
        solution = df.iloc[:,0].to_list()
        for i in range(len(solution)):
            self.getSolution().getSolTracks()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])] = self.getProblem().getTrackIndex(solution[i][3])
            self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])][int(solution[i][4].split('t')[1])] = self.getProblem().getSubmissionIndex(solution[i][5])
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            #if self.getProblem().getSubmission(sub).getRequiredTimeSlots() > 1:
            for session in range(len(self.getSolution().getSolSubmissions())):
                for room in range(len(self.getSolution().getSolSubmissions()[session])):
                    if sub in self.getSolution().getSolSubmissions()[session][room]:
                        info = []
                        for i in range(len(self.getSolution().getSolSubmissions()[session][room])):
                            if self.getSolution().getSolSubmissions()[session][room][i] != -1:
                                if (self.getSolution().getSolSubmissions()[session][room][i], self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[session][room][i]).getOrder()) not in info:
                                    info.append((self.getSolution().getSolSubmissions()[session][room][i], self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[session][room][i]).getOrder()))
                        sorted_info = sorted(info, key = lambda x: x[1])
                        temp = []
                        for i in range(len(sorted_info)):
                            while temp.count(sorted_info[i][0]) < self.getProblem().getSubmission(sorted_info[i][0]).getRequiredTimeSlots():
                                temp.append(sorted_info[i][0])
                        while len(temp) < len(self.getSolution().getSolSubmissions()[session][room]):
                            temp.append(-1)
                        self.getSolution().getSolSubmissions()[session][room] = temp
    
    def ApproximationModel(self):
        model = LpProblem('model', LpMinimize)
        names = []
        add_names = []
        add2_names = []
        product_names = []
        coefficients = {}
        timeslots = {}
        save_time = 0
        save_time2 = 0
        
        #Determine MaxS for each track
        sessions_ts = []
        required_sessions = {}
        for session in range(self.getProblem().getNumberOfSessions()):
            sessions_ts.append(self.getProblem().getSession(session).getMaxTimeSlots())
        sorted_sessions_ts = sorted(sessions_ts)
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            i = -1
            while self.getProblem().getTrack(track).getRequiredTimeSlots() > sum(temp):
                i += 1
                temp.append(sorted_sessions_ts[i])
            required_sessions[str(track)] = len(temp)
        
        #Creating decision variables
        for i in range(self.getProblem().getNumberOfSessions()):
            for t in range(self.getProblem().getSession(i).getMaxTimeSlots()):
                for j in range(self.getProblem().getNumberOfRooms()):
                    for z in range(self.getProblem().getNumberOfTracks()):
                        for x in range(len(self.getProblem().getTrack(z).getSubmissions())):
                            alpha = self.getSolution().getWeight(0) * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getSession(i).getName())
                            beta = self.getSolution().getWeight(1) * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getRoom(j).getName())
                            gamma = self.getSolution().getWeight(2) * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getName(), self.getProblem().getRoom(j).getName())
                            nx = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(self.getProblem().getTrack(z).getSubmissions()[x].getName())).getRequiredTimeSlots()
                            MaxTS = self.getProblem().getSession(i).getMaxTimeSlots()
                            MaxS = required_sessions[str(z)]
                            #MaxS = self.getProblem().getNumberOfSessions()
                            names.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x]))
                            #coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getSolution().getWeight(0) * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(1) * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getRoom(j).getName()) + self.getSolution().getWeight(2) * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getName(), self.getProblem().getRoom(j).getName()) + self.getSolution().getWeight(8) * self.getProblem().getSubmissionsTimezonesPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(10) * self.getProblem().getSubmissionsSessionsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(11) * self.getProblem().getSubmissionsRoomsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getRoom(j).getName())
                            coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = self.getSolution().getWeight(8) * self.getProblem().getSubmissionsTimezonesPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(10) * self.getProblem().getSubmissionsSessionsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(11) * self.getProblem().getSubmissionsRoomsPenalty(str(self.getProblem().getTrack(z).getSubmissions()[x]), self.getProblem().getRoom(j).getName()) + (nx*(alpha + gamma)/MaxTS) + ((nx*beta)/(MaxTS*MaxS))
                            timeslots['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()+'|'+'Timeslot'+str(t)+'|'+str(self.getProblem().getTrack(z).getSubmissions()[x])] = nx
                
        #Additional variables to minimise tracks per room [Y Variable]
        for i in range(self.getProblem().getNumberOfTracks()):
            for j in range(self.getProblem().getNumberOfRooms()):
                add2_names.append('|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName())
                coefficients['|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName()] = 1
                #coefficients['|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName()] = self.getSolution().getWeight(1) * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(i).getName(), self.getProblem().getRoom(j).getName())
        
        #Additional variables for assigning 1 track into one room and session
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                for z in range(self.getProblem().getNumberOfTracks()):
                    add_names.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName())
                    coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()] = 1
                    #coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()] = self.getSolution().getWeight(0) * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(2) * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getName(), self.getProblem().getRoom(j).getName())
        
        #Creating objective function and binary IP formulation
        variables = LpVariable.dicts('Variables', names, cat = 'Binary')
        add_variables = LpVariable.dicts('AddVariables', add_names, cat = 'Binary')
        add2_variables = LpVariable.dicts('Add2Variables', add2_names, cat = 'Binary')
        obj_function = [variables]#[variables, add_variables, add2_variables, slack_variables]
        all_names = [names]#[names, add_names, add2_names, slack_vars]
        model += lpSum([coefficients[i] * obj_function[x][i] for x in range(len(obj_function)) for i in all_names[x]])
        print('# Variables:', len(names) + len(add_names) + len(add2_names))
        constraints_count = 0
          
        #Creating constraints: Assign only 1 track into one room and session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for room in range(self.getProblem().getNumberOfRooms()):
                room_name = self.getProblem().getRoom(room).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
                constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in range(len(names)):
                if track_name == names[name].split('|')[3]:
                    temp.append(names[name])
            for session in range(self.getProblem().getNumberOfSessions()):
                session_name = self.getProblem().getSession(session).getName()
                session_max_ts = self.getProblem().getSession(session).getMaxTimeSlots()
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp2 = []
                    room_name = self.getProblem().getRoom(room).getName()
                    for name in temp:
                        if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                            temp2.append(name)
                    for add_name in add_names:
                        if track_name == add_name.split('|')[3] and session_name == add_name.split('|')[1] and room_name == add_name.split('|')[2]:
                            add_var = add_name
                    all_constraints.append(lpSum([timeslots[x] * variables[x] for x in temp2]) - session_max_ts * add_variables[add_var])
                    constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in range(len(names)):
                if track_name == names[name].split('|')[3]:
                    temp.append(names[name])
            for session in range(self.getProblem().getNumberOfSessions()):
                session_name = self.getProblem().getSession(session).getName()
                session_max_ts = self.getProblem().getSession(session).getMaxTimeSlots()
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp2 = []
                    room_name = self.getProblem().getRoom(room).getName()
                    for name in temp:
                        if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                            temp2.append(name)
                    for add_name in add_names:
                        if track_name == add_name.split('|')[3] and session_name == add_name.split('|')[1] and room_name == add_name.split('|')[2]:
                            add_var = add_name
                    all_constraints.append(lpSum([timeslots[x] * variables[x] for x in temp2]) - add_variables[add_var])
                    constraints_count += 1
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] >= 0
        
        #Creating constraints: Min number of Rooms per Track
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            all_constraints.append(lpSum([add2_variables[x] for x in temp]))
            constraints_count += 1
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        all_constraints = []
        for room in range(self.getProblem().getNumberOfRooms()):
            room_name = self.getProblem().getRoom(room).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                temp = []
                track_name = self.getProblem().getTrack(track).getName()
                for name in add_names:
                    if room_name == name.split('|')[2] and track_name == name.split('|')[3]:
                        temp.append(name)
                for name in add2_names:
                    if room_name == name.split('|')[1] and track_name == name.split('|')[2]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[temp[x]] for x in range(len(temp) - 1)]) - required_sessions[str(track)] * add2_variables[temp[len(temp) - 1]])
                #all_constraints.append(lpSum([add_variables[temp[x]] for x in range(len(temp) - 1)]) - self.getProblem().getNumberOfSessions() * add2_variables[temp[len(temp) - 1]])
                constraints_count += 1
                    
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
        
        #Creating Constraints: All submissions must be scheduled
        all_constraints = []
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            temp = []
            req_ts = 1
            sub_req_ts = self.getProblem().getSubmission(submission).getRequiredTimeSlots()
            sub_name = self.getProblem().getSubmission(submission).getName()
            for name in range(len(names)):
                if names[name].split('|')[5] == sub_name:
                    temp.append(names[name])
            all_constraints.append(lpSum([variables[x] for x in temp]))
            constraints_count += 1
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        #Creating constraints: Do not assign same track into same session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and track_name == name.split('|')[3]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
                constraints_count += 1
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating Constraints: Avoid Speaker Conflicts [Session Level]
        all_constraints = []
        unique_conflicts = []
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            sub_name = self.getProblem().getSubmission(submission).getName()
            sub_name_track = self.getProblem().getSubmission(submission).getTrack()
            if len(self.getProblem().getSubmission(submission).getSpeakerConflicts()) != 0:
                for conflict in self.getProblem().getSubmission(submission).getSpeakerConflicts():
                    conflict_track = self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(conflict)).getTrack()
                    if conflict_track != sub_name_track:
                        for session in range(self.getProblem().getNumberOfSessions()):
                            current_conflict = [sub_name, conflict, self.getProblem().getSession(session).getName()]
                            if sorted(current_conflict) not in unique_conflicts:
                                unique_conflicts.append(sorted(current_conflict))
                                temp = []
                                session_name = self.getProblem().getSession(session).getName()
                                for name in range(len(names)):
                                    if (names[name].split('|')[5] == sub_name and names[name].split('|')[1] == session_name) or (names[name].split('|')[5] == conflict and names[name].split('|')[1] == session_name):
                                        temp.append(names[name])
                                all_constraints.append(lpSum([variables[x] for x in temp]))
                                constraints_count += 1
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints: Only 1 submission can be scheduled per timeslot
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for room in range(self.getProblem().getNumberOfRooms()):
                room_name = self.getProblem().getRoom(room).getName()
                for t in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                    temp = []
                    for name in range(len(names)):
                        if session_name == names[name].split('|')[1] and room_name == names[name].split('|')[2] and 'Timeslot'+str(t) == names[name].split('|')[4]:
                            temp.append(names[name])
                    all_constraints.append(lpSum([variables[x] for x in temp]))
                    constraints_count += 1
                    
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        '''
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
                    session_name = self.getProblem().getSession(session).getName()
                    temp2 = []
                    for name in range(len(add_names)):
                        for z in range(len(temp)):
                            if add_names[name].split('|')[1] == session_name and add_names[name].split('|')[3] == self.getProblem().getTrack(temp[z]).getName():
                                temp2.append(add_names[name])
                    #all_constraints.append(lpSum([add_variables[x] for x in temp2]) - penalties['ptt_|' + str(i) + str(j)])
                    all_constraints.append(lpSum([add_variables[x] for x in temp2]))
                    constraints_count += 1
                        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
            
        #Creating Constraints: Avoid Attendee Conflicts [Time slot Level]        
        for submission in range(self.getProblem().getNumberOfSubmissions()):
            if len(self.getProblem().getSubmission(submission).getAttendeeConflicts()) != 0:
                for conflict in self.getProblem().getSubmission(submission).getAttendeeConflicts():
                    for session in range(self.getProblem().getNumberOfSessions()):
                        for t in range(self.getProblem().getSession(session).getMaxTimeSlots()):
                            temp = []
                            for name in range(len(names)):
                                if (names[name].split('|')[5] == self.getProblem().getSubmission(submission).getName() and names[name].split('|')[1] == self.getProblem().getSession(session).getName() and names[name].split('|')[4] == 'Timeslot' + str(t)) or (names[name].split('|')[5] == conflict and names[name].split('|')[1] == self.getProblem().getSession(session).getName() and names[name].split('|')[4] == 'Timeslot' + str(t)):
                                    temp.append(names[name])
                            model += lpSum([variables[x] for x in temp]) <= 1
                            constraints_count += 1
        '''
        print('# Constraints:', constraints_count)
        #Solving
        stime = time()
        model.solve(GUROBI(msg = 1, MIPGap = 0, timeLimit = 18000))#, MIPGap = 0, Method = 2, timeLimit = 7200)) #StartNodeLimit / TuneTimeLimit / timeLimit / threads
        #model.solve(CPLEX_PY(msg = 1, timeLimit = 900))
        #if LpStatus[model.status] == 'Infeasible':
        #    model.solverModel.computeIIS()
        #    sys.exit(model.solverModel.write("Infeasible_Constraints.ilp"))
        print('BIP Solving time:', round((time() - stime) / 60, 2))
        print(model.objective.value())
        print("Model Status:", LpStatus[model.status])
        solution = []
        '''
        for i in model.variables():
            if i.varValue > 0:
                solution.append(i.name)
        '''
        gur_vars = model.solverModel.getVars()
        for i in gur_vars:
            if i.X > 0:
                solution.append(i.varName)
        to_remove = []
        for i in range(len(solution)):
            if solution[i].split('|')[0] != 'Variables_':
                to_remove.append(solution[i])
        for i in product_names:
            to_remove.append(str(variables[i]))
        for i in to_remove:
            if i in solution:
                solution.remove(i)
        df = pd.DataFrame(solution)
        df.replace(to_replace = '_', value = ' ', regex = True, inplace = True)
        df = df.applymap(lambda x: x.split('|'))
        solution = df.iloc[:,0].to_list()
        for i in range(len(solution)):
            self.getSolution().getSolTracks()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])] = self.getProblem().getTrackIndex(solution[i][3])
            self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution[i][1])][self.getProblem().getRoomIndex(solution[i][2])][int(solution[i][4].split('t')[1])] = self.getProblem().getSubmissionIndex(solution[i][5])
        for sub in range(self.getProblem().getNumberOfSubmissions()):
            #if self.getProblem().getSubmission(sub).getRequiredTimeSlots() > 1:
            for session in range(len(self.getSolution().getSolSubmissions())):
                for room in range(len(self.getSolution().getSolSubmissions()[session])):
                    if sub in self.getSolution().getSolSubmissions()[session][room]:
                        info = []
                        for i in range(len(self.getSolution().getSolSubmissions()[session][room])):
                            if self.getSolution().getSolSubmissions()[session][room][i] != -1:
                                if (self.getSolution().getSolSubmissions()[session][room][i], self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[session][room][i]).getOrder()) not in info:
                                    info.append((self.getSolution().getSolSubmissions()[session][room][i], self.getProblem().getSubmission(self.getSolution().getSolSubmissions()[session][room][i]).getOrder()))
                        sorted_info = sorted(info, key = lambda x: x[1])
                        temp = []
                        for i in range(len(sorted_info)):
                            while temp.count(sorted_info[i][0]) < self.getProblem().getSubmission(sorted_info[i][0]).getRequiredTimeSlots():
                                temp.append(sorted_info[i][0])
                        while len(temp) < len(self.getSolution().getSolSubmissions()[session][room]):
                            temp.append(-1)
                        self.getSolution().getSolSubmissions()[session][room] = temp
        
    #tBIP() is only for optimising tracks solution
    def tBIP(self): 
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
                    add_names.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName())
                    timeslots['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()] = self.getProblem().getSession(i).getMaxTimeSlots()
                    coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName()] = 1 + self.getSolution().getWeight(0) * self.getProblem().getTracksSessionsPenalty(self.getProblem().getTrack(z).getName(), self.getProblem().getSession(i).getName()) + self.getSolution().getWeight(2) * self.getProblem().getSessionsRoomsPenalty(self.getProblem().getSession(i).getName(), self.getProblem().getRoom(j).getName())
            
        #Filter submissions with multiple ts
        for x in range(self.getProblem().getNumberOfSubmissions()):
            if self.getProblem().getSubmission(x).getRequiredTimeSlots() > 1:
                mts_subs.append(x)
        
        #Creating decision variables Xs
        for i in range(self.getProblem().getNumberOfSessions()):
            for j in range(self.getProblem().getNumberOfRooms()):
                for x in mts_subs:
                    if self.getProblem().getSubmission(x).getRequiredTimeSlots() <= self.getProblem().getSession(i).getMaxTimeSlots():
                        names.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getSubmission(x).getTrack().getName()+'|'+self.getProblem().getSubmission(x).getName())
                        coefficients['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getSubmission(x).getTrack().getName()+'|'+self.getProblem().getSubmission(x).getName()] = 1
                        n['|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getSubmission(x).getTrack().getName()+'|'+self.getProblem().getSubmission(x).getName()] = self.getProblem().getSubmission(x).getRequiredTimeSlots()
        
        #Additional variables to minimise tracks per room [Y Variable]
        for i in range(self.getProblem().getNumberOfTracks()):
            for j in range(self.getProblem().getNumberOfRooms()):
                add2_names.append('|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName())
                coefficients['|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(i).getName()] = self.getSolution().getWeight(1) * self.getProblem().getTracksRoomsPenalty(self.getProblem().getTrack(i).getName(), self.getProblem().getRoom(j).getName())
        
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
            track_name = self.getProblem().getTrack(track).getName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            pen.append('pmrt_|' + str(track))
            coefficients['pmrt_|' + str(track)] = 50
        
        #Creating penalties for parallel tracks
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getName()
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
        penalties = LpVariable.dicts('Penalties', pen, lowBound = 0, cat = 'Integer')
        obj_function = [add_variables, add2_variables, penalties]
        all_names = [add_names, add2_names, pen]
        model += lpSum([coefficients[i] * obj_function[x][i] for x in range(len(obj_function)) for i in all_names[x]])
        
        #Assign subs with multiple ts
        all_constraints = []
        for track in range(self.getProblem().getNumberOfTracks()):
            temp = []
            track_name = self.getProblem().getTrack(track).getName()
            for name in range(len(names)):
                if track_name == names[name].split('|')[3]:
                    temp.append(names[name])
            for session in range(self.getProblem().getNumberOfSessions()):
                session_name = self.getProblem().getSession(session).getName()
                session_max_ts = self.getProblem().getSession(session).getMaxTimeSlots()
                for room in range(self.getProblem().getNumberOfRooms()):
                    temp2 = []
                    room_name = self.getProblem().getRoom(room).getName()
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
            sub_name = self.getProblem().getSubmission(mts_subs[submission]).getName()
            for name in range(len(names)):
                if names[name].split('|')[4] == sub_name:
                    temp.append(names[name])
            all_constraints.append(lpSum([variables[x] for x in temp]))
            
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
            
        #Creating constraints: Assign tracks with respect to available time slots
        for track in range(self.getProblem().getNumberOfTracks()):
            track_name = self.getProblem().getTrack(track).getName()
            temp = []
            for name in add_names:
                if track_name == name.split('|')[3]:
                    temp.append(name)
            model += lpSum([timeslots[x] * add_variables[x] for x in temp]) >= self.getProblem().getTrack(track).getRequiredTimeSlots()
        
        '''
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
                all_constraints1.append(add_variables[temp2] - add_variables[temp[z]] - add_variables[temp[z+1]])
                all_constraints2.append(add_variables[temp2] - add_variables[temp[z]])
                all_constraints2.append(add_variables[temp2] - add_variables[temp[z+1]])
                    
        for c in range(len(all_constraints1)):
            model += all_constraints1[c] >= -1
            
        for c in range(len(all_constraints2)):
            model += all_constraints2[c] <= 0
        '''
        #Creating constraints: Consider organizer conflicts
        all_constraints = []
        temp2 = []
        for z in range(self.getProblem().getNumberOfTracks()):
            if len(self.getProblem().getTrack(z).getOrganizerConflicts()) != 0:
                for i in range(self.getProblem().getNumberOfSessions()):
                    temp = []
                    for j in range(self.getProblem().getNumberOfRooms()):        
                        temp.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+self.getProblem().getTrack(z).getName())
                        for x in self.getProblem().getTrack(z).getOrganizerConflicts():
                            temp.append('|'+self.getProblem().getSession(i).getName()+'|'+self.getProblem().getRoom(j).getName()+'|'+x)
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
                        session_name = self.getProblem().getSession(session).getName()
                        temp2 = []
                        for name in range(len(add_names)):
                            for z in range(len(temp)):
                                if add_names[name].split('|')[1] == session_name and add_names[name].split('|')[3] == self.getProblem().getTrack(temp[z]).getName():
                                    temp2.append(add_names[name])
                        all_constraints.append(lpSum([add_variables[x] for x in temp2]) - penalties['ptt_|' + str(i) + str(j) + str(session)])
                        #all_constraints.append(lpSum([add_variables[x] for x in temp2]))
                    temp = [i]
                        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
        #Creating constraints: Do not assign same track into same session
        all_constraints = []
        for session in range(self.getProblem().getNumberOfSessions()):
            session_name = self.getProblem().getSession(session).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                track_name = self.getProblem().getTrack(track).getName()
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
            track_name = self.getProblem().getTrack(track).getName()
            for name in add2_names:
                if track_name == name.split('|')[2]:
                    temp.append(name)
            all_constraints.append(lpSum([add2_variables[x] for x in temp]) - penalties['pmrt_|' + str(track)])
            #all_constraints.append(lpSum([add2_variables[x] for x in temp]))
                
        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1
        
        all_constraints = []
        for room in range(self.getProblem().getNumberOfRooms()):
            room_name = self.getProblem().getRoom(room).getName()
            for track in range(self.getProblem().getNumberOfTracks()):
                temp = []
                track_name = self.getProblem().getTrack(track).getName()
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
            session_name = self.getProblem().getSession(session).getName()
            for room in range(self.getProblem().getNumberOfRooms()):
                room_name = self.getProblem().getRoom(room).getName()
                temp = []
                for name in add_names:
                    if session_name == name.split('|')[1] and room_name == name.split('|')[2]:
                        temp.append(name)
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
        
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1
        
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
        for i in product_names:
            to_remove.append(str(add_variables[i]))
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
            for j in range(self.getProblem().getSubmission(self.getProblem().getSubmissionIndex(solution2[i][4])).getRequiredTimeSlots()):
                ts = self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution2[i][1])][self.getProblem().getRoomIndex(solution2[i][2])].index(-1)
                self.getSolution().getSolSubmissions()[self.getProblem().getSessionIndex(solution2[i][1])][self.getProblem().getRoomIndex(solution2[i][2])][ts] = self.getProblem().getSubmissionIndex(solution2[i][4])
        return t