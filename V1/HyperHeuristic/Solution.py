# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from Problem import *
from Parameters import *
import sys
import numpy as np

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
    
    def EvaluateSubmissionsActualOrder(self) -> int:
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
        
    def convertSolFirstTime(self):
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
        #Creating Ind sol
        temp = [[] for i in range(self.getProblem().getNumberOfTracks())]
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    for x in range(len(self.getSolSubmissions()[i][j])):
                        temp[self.getSolTracks()[i][j]].append(self.getSolSubmissions()[i][j][x])
        self.setIndSolSubmissions(temp)
    
    '''
    toExcel
    '''
    
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
            