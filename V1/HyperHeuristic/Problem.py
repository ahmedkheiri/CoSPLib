# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:12:46 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

import Submission
import Track
import Room
import Session
import Parameters
import pandas as pd
import datetime as dt
import pytz
import sys

class Problem():
    def __init__(self, file_name = "N2OR.xlsx"):
        self.__file_name = file_name
        
        self.__rooms = []
        self.__sessions = []
        self.__tracks = []
        self.__submissions = []
        
        self.__rooms_map = {}
        self.__sessions_map = {}
        self.__tracks_map = {}
        self.__submissions_map = {}
        
        self.__submissions_sessions_penalty_map = {}
        self.__submissions_timezones_penalty_map = {}
        self.__submissions_rooms_penalty_map = {}
        self.__tracks_sessions_penalty_map = {}
        self.__tracks_rooms_penalty_map = {}
        self.__tracks_tracks_penalty_map = {}
        self.__sessions_rooms_penalty_map = {}
    
    def getFileName(self) -> str:
        return self.__file_name
    def setFileName(self, file_name):
        self.__file_name = file_name
    #Rooms    
    def getNumberOfRooms(self) -> int:
        return len(self.__rooms)
    def getRoom(self, room_index) -> Room.Room:
        return self.__rooms[room_index]
    def getRoomList(self) -> list:
        return self.__rooms
    def setRoom(self, room_object):
        self.__rooms.append(room_object)
        self.__rooms_map[room_object.getRoomName()] = len(self.__rooms_map)
    def getRoomIndex(self, room_name) -> int:
        return self.__rooms_map[room_name]
    #Sessions
    def getNumberOfSessions(self) -> int:
        return len(self.__sessions)
    def getSession(self, session_index) -> Session.Session:
        return self.__sessions[session_index]
    def getSessionList(self) -> list:
        return self.__sessions
    def setSession(self, session_object):
        self.__sessions.append(session_object)
        self.__sessions_map[session_object.getSessionName()] = len(self.__sessions_map)
    def getSessionIndex(self, session_name) -> int:
        return self.__sessions_map[session_name]
    def getSumOfAvailableTimeSlots(self) -> int:
        self.__sum_of_time_slots = 0
        for i in range(len(self.__sessions)):
            self.__sum_of_time_slots += self.__sessions[i].getSessionMaxTimeSlots()
        return self.__sum_of_time_slots
    def getLargestSessionTimeSlots(self):
        temp = []
        for i in range(len(self.__sessions)):
            temp.append(self.getSession(i).getSessionMaxTimeSlots())
        return max(temp)
    #Tracks
    def getNumberOfTracks(self) -> int:
        return len(self.__tracks)
    def getTrack(self, track_index) -> Track.Track:
        return self.__tracks[track_index]
    def getTrackList(self) -> list:
        return self.__tracks
    def setTrack(self, track_object):
        self.__tracks.append(track_object)
        self.__tracks_map[track_object.getTrackName()] = len(self.__tracks_map)
    def getTrackIndex(self, track_name) -> int:
        return self.__tracks_map[track_name]
    #Submissions
    def getNumberOfSubmissions(self) -> int:
        return len(self.__submissions)
    def getSubmission(self, submission_index) -> Submission.Submission:
        return self.__submissions[submission_index]
    def getSubmissionList(self) -> list:
        return self.__submissions
    def setSubmission(self, submission_object):
        self.__submissions.append(submission_object)
        self.__submissions_map[submission_object.getSubmissionName()] = len(self.__submissions_map)
    def getSubmissionIndex(self, submission_name) -> int:
        return self.__submissions_map[submission_name]  
    def getSumOfRequiredTimeSlots(self):
        self.__total_required_time_slots = 0
        for i in range(len(self.__submissions)):
            self.__total_required_time_slots += self.__submissions[i].getSubmissionRequiredTimeSlots()
        return self.__total_required_time_slots
    #Parameters
    def setParameters(self, parameters_object):
        self.__parameters = parameters_object
    def getParameters(self) -> Parameters:
        return self.__parameters
    #Submissions_sessions|penalty
    def setSubmissionsSessionsPenalty(self, submission_name, session_name, penalty):
        self.__submissions_sessions_penalty_map[submission_name + session_name] = penalty
    def getSubmissionsSessionsPenalty(self, submission_name, session_name):
        return self.__submissions_sessions_penalty_map[submission_name + session_name]
    def getSubmissionsSessionsPenaltybyIndex(self, submission_index, session_index):
        return self.__submissions_sessions_penalty_map[self.getSubmission(submission_index).getSubmissionName() + self.getSession(session_index).getSessionName()]
    #Submissions_Timezones|penalty
    def setSubmissionsTimezonesPenalty(self, submission_name, session_name, penalty):
        self.__submissions_timezones_penalty_map[submission_name + session_name] = penalty
    def getSubmissionsTimezonesPenalty(self, submission_name, session_name):
        return self.__submissions_timezones_penalty_map[submission_name + session_name]
    def getSubmissionsTimezonesPenaltybyIndex(self, submission_index, session_index):
        return self.__submissions_timezones_penalty_map[self.getSubmission(submission_index).getSubmissionName() + self.getSession(session_index).getSessionName()]
    #Submissions_rooms|penalty
    def setSubmissionsRoomsPenalty(self, submission_name, room_name, penalty):
        self.__submissions_rooms_penalty_map[submission_name + room_name] = penalty
    def getSubmissionsRoomsPenalty(self, submission_name, room_name):
        return self.__submissions_rooms_penalty_map[submission_name + room_name]
    def getSubmissionsRoomsPenaltybyIndex(self, submission_index, room_index):
        return self.__submissions_rooms_penalty_map[self.getSubmission(submission_index).getSubmissionName() + self.getRoom(room_index).getRoomName()]
    #Tracks_sessions|penalty
    def setTracksSessionsPenalty(self, track_name, session_name, penalty):
        self.__tracks_sessions_penalty_map[track_name + session_name] = penalty
    def getTracksSessionsPenalty(self, track_name, session_name):
        return self.__tracks_sessions_penalty_map[track_name + session_name]
    def getTracksSessionsPenaltybyIndex(self, track_index, session_index):
        return self.__tracks_sessions_penalty_map[self.getTrack(track_index).getTrackName() + self.getSession(session_index).getSessionName()]
    #Tracks_rooms|penalty
    def setTracksRoomsPenalty(self, track_name, room_name, penalty):
        self.__tracks_rooms_penalty_map[track_name + room_name] = penalty
    def getTracksRoomsPenalty(self, track_name, room_name):
        return self.__tracks_rooms_penalty_map[track_name + room_name]
    def getTracksRoomsPenaltybyIndex(self, track_index, room_index):
        return self.__tracks_rooms_penalty_map[self.getTrack(track_index).getTrackName() + self.getRoom(room_index).getRoomName()]
    #Tracks_tracks|penalty
    def setTracksTracksPenalty(self, track_name1, track_name2, penalty):
        self.__tracks_tracks_penalty_map[track_name1 + track_name2] = penalty
    def getTracksTracksPenalty(self, track1_name, track2_name):
        return self.__tracks_tracks_penalty_map[track1_name + track2_name]
    def getTracksTracksPenaltybyIndex(self, track1_index, track2_index):
        return self.__tracks_tracks_penalty_map[self.getTrack(track1_index).getTrackName() + self.getTrack(track2_index).getTrackName()]
    #Sessions_rooms|penalty
    def setSessionsRoomsPenalty(self, session_name, room_name, penalty):
        self.__sessions_rooms_penalty_map[session_name + room_name] = penalty
    def getSessionsRoomsPenalty(self, session_name, room_name):
        return self.__sessions_rooms_penalty_map[session_name + room_name]
    def getSessionsRoomsPenaltybyIndex(self, session_index, room_index):
        return self.__sessions_rooms_penalty_map[self.getSession(session_index).getSessionName() + self.getRoom(room_index).getRoomName()]
    def ReadProblemInstance(self):
        #Begin checking All Sheets Exist
        file = pd.read_excel(self.getFileName(), None)
        existing_sheets = file.keys()
        required_sheets = ['parameters', 'submissions', 'tracks', 'sessions', 'rooms','tracks_sessions|penalty', 'tracks_rooms|penalty', 'similar tracks', 'sessions_rooms|penalty']
        for i in required_sheets:
            if i not in existing_sheets:
                sys.exit(print('Missing Sheet Error! \nMissing Sheet:', i))
        #End of checking
        
        #Begin checking for Duplicates
        cols = list(pd.read_excel(self.getFileName(), sheet_name = "submissions", header = None, nrows = 1).values[0])
        if len(cols) != len(set(cols)):
            sys.exit(print('Duplicates Error! \nColumn names duplicate in sheet submissions!'))
        duplicates_check = ['submissions', 'tracks', 'sessions', 'rooms']
        for i in duplicates_check:
            duplicates = file[i].duplicated(subset = file[i].columns[0])
            if duplicates.any() == True:
                duplicate_indexes = duplicates[duplicates].index
                sys.exit(print('Duplicates Error! \nThe following duplicates were found in sheet', i,':\n', file[i][file[i].columns[0]][duplicate_indexes]))
        #End of checking
        
        #Begin checking for Duplicates in penalty sheets
        duplicates_check = ['tracks_sessions|penalty', 'tracks_rooms|penalty', 'similar tracks', 'sessions_rooms|penalty']
        for i in duplicates_check:
            cols = list(pd.read_excel(self.getFileName(), sheet_name = i, header = None, nrows = 1).values[0])
            if len(cols) != len(set(cols)):
                sys.exit(print('Duplicates Error! \nColumn names duplicate in sheet', i, '!'))
            duplicate_row = file[i].iloc[:,0].duplicated()
            if duplicate_row.any() == True:
                duplicate_indexes = duplicate_row[duplicate_row].index
                sys.exit(print('Duplicates Error! \nThe following duplicates were found in sheet', i,':\n', file[i][file[i].columns[0]][duplicate_indexes]))
        #End of checking
        
        #Reading Sessions
        file = pd.read_excel(self.getFileName(), sheet_name = "sessions", keep_default_na = False, na_filter = False)
        for i in range(len(file)):
            temp1 = str(file.iloc[i,3]).split(':')
            temp2 = str(file.iloc[i,4]).split(':')
            start_time = dt.datetime(2021, 7, 21, int(temp1[0]), int(temp1[1]))
            end_time = dt.datetime(2021, 7, 21, int(temp2[0]), int(temp2[1]))
            self.setSession(Session.Session(file.iloc[i,0], file.iloc[i,1], file.iloc[i,2], start_time, end_time))

        #Reading Rooms
        file = pd.read_excel(self.getFileName(), sheet_name = "rooms", keep_default_na = False, na_filter = False)
        for i in range(len(file)):
            self.setRoom(Room.Room(file.iloc[i,0]))
                    
        #Reading Submissions part 1
        file = pd.read_excel(self.getFileName(), sheet_name = "submissions", keep_default_na = False, na_filter = False)
        columns = list(file.columns)
        timezones_format = {'GMT-12':'Etc/GMT+12', 'GMT-11':'Etc/GMT+11', 'GMT-10':'Etc/GMT+10', 'GMT-9':'Etc/GMT+9', 
                                        'GMT-8':'Etc/GMT+8', 'GMT-7':'Etc/GMT+7', 'GMT-6':'Etc/GMT+6', 'GMT-5':'Etc/GMT+5', 
                                        'GMT-4':'Etc/GMT+4', 'GMT-3':'Etc/GMT+3', 'GMT-2':'Etc/GMT+2', 'GMT-1':'Etc/GMT+1',
                                        'GMT+0':'Etc/GMT+0', 'GMT+12':'Etc/GMT-12', 'GMT+11':'Etc/GMT-11', 'GMT+10':'Etc/GMT-10', 
                                        'GMT+9':'Etc/GMT-9', 'GMT+8':'Etc/GMT-8', 'GMT+7':'Etc/GMT-7', 'GMT+6':'Etc/GMT-6', 
                                        'GMT+5':'Etc/GMT-5', 'GMT+4':'Etc/GMT-4', 'GMT+3':'Etc/GMT-3', 'GMT+2':'Etc/GMT-2', 
                                        'GMT+1':'Etc/GMT-1'}
        df1 = file.iloc[:, :7]
        df1 = df1.replace({'Time Zone': timezones_format})
        df2 = file.iloc[:, 7:]
        df2.replace(to_replace = '', value = 0, inplace = True)
        file = df1.join(df2)
        freq = file['Track'].value_counts(sort = False)
        file2 = pd.read_excel(self.getFileName(), sheet_name = "tracks", keep_default_na = False, na_filter = False)

        #Begin checking for Track of zero size
        for i in file2['Tracks'].values:
            if i not in freq.keys():
                sys.exit(print('Track Error!\n[ Track Name:', i, ']', ' has none submissions!'))
        #End of checking
        
        #Begin checking number of items
        file3 = pd.read_excel(self.getFileName(), None, header = None)
        if (len(file3['tracks_sessions|penalty'].iloc[0,:]) != len(file3['sessions'])) or (len(file3['tracks_sessions|penalty'].iloc[:,0]) != len(file3['tracks'])):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_sessions|penalty.'))
        if (len(file3['tracks_rooms|penalty'].iloc[0,:]) != len(file3['rooms'])) or (len(file3['tracks_rooms|penalty'].iloc[:,0]) != len(file3['tracks'])):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_rooms|penalty.'))
        if (len(file3['similar tracks'].iloc[0,:]) != len(file3['tracks'])) or (len(file3['similar tracks'].iloc[:,0]) != len(file3['tracks'])):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_tracks|penalty.'))
        if (len(file3['sessions_rooms|penalty'].iloc[0,:]) != len(file3['rooms'])) or (len(file3['sessions_rooms|penalty'].iloc[:,0]) != len(file3['sessions'])):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet sessions_rooms|penalty.'))
        #End of checking
        
        #Reading Tracks
        for i in range(len(file2)):
            self.setTrack(Track.Track(file2.iloc[i,0], list(file2.iloc[i,1].split(", ")), [], []))
        
        #Begin checking for number of items between submissions and sessions & rooms
        if len(columns[7:]) != self.getNumberOfSessions() + self.getNumberOfRooms():
            sys.exit(print('Incorrect Number of Items Error! \nEnsure that number of sessions and rooms in sheet submissions match with number of itmes in sessions and rooms sheets.'))
        #End of checking
        
        #Begin checking for matching names between submissions and sessions sheets
        for i in range(self.getNumberOfSessions()):
            if self.getSession(i).getSessionName() not in columns[7:7 + self.getNumberOfSessions()]:
                sys.exit(print('Sessions Error!\nSessions names in submissions sheet must match those in sessions sheet.'))
        #End of checking
        
        #Begin checking for matching names between submissions and rooms sheets
        for i in range(self.getNumberOfRooms()):
            if self.getRoom(i).getRoomName() not in columns[7 + self.getNumberOfSessions():7 + self.getNumberOfSessions() + self.getNumberOfRooms()]:
                sys.exit(print('Rooms Error!\nRooms names in submissions sheet must match those in rooms sheet.'))
        #End of checking
        
        #Reading Submissions part 2
        for i in range(len(file)):
            #Begin checking for Unknown Track
            if file.iloc[i,1] not in file2['Tracks'].values:
                sys.exit(print('Track Error! \nUnknown track for', file.iloc[i,0], '[ Track name:', file.iloc[i,1],'].'))
            #End of checking
            
            self.setSubmission(Submission.Submission(file.iloc[i,0], self.getTrack(self.getTrackIndex(file.iloc[i,1])), file.iloc[i,2], file.iloc[i,3], file.iloc[i,4], list(file.iloc[i,5].split(", ")), list(file.iloc[i,6].split(", ")), [], []))
            self.getTrack(self.getTrackIndex(file.iloc[i,1])).setTrackSubmissions(self.getSubmission(self.getSubmissionIndex(file.iloc[i,0])))
            for j in range(7, 7 + self.getNumberOfSessions()):
                self.setSubmissionsSessionsPenalty(self.getSubmission(self.getSubmissionIndex(file.iloc[i,0])).getSubmissionName(), self.getSession(self.getSessionIndex(columns[j])).getSessionName(), file.iloc[i,j])
            for y in range(7 + self.getNumberOfSessions(), 7 + self.getNumberOfSessions() + self.getNumberOfRooms()):
                self.setSubmissionsRoomsPenalty(self.getSubmission(self.getSubmissionIndex(file.iloc[i,0])).getSubmissionName(), self.getRoom(self.getRoomIndex(columns[y])).getRoomName(), file.iloc[i,y])

        for track in range(self.getNumberOfTracks()):
            track_ts = []
            for sub in self.getTrack(track).getTrackSubmissionsList():
                track_ts.append(sub.getSubmissionRequiredTimeSlots())
            self.getTrack(track).setTrackRequiredTimeSlots(sum(track_ts))
        
        #Reading 'tracks_sessions|penalty' sheet
        file = pd.read_excel(self.getFileName(), sheet_name = "tracks_sessions|penalty", keep_default_na = False, na_filter = False)
        file.replace(to_replace = '', value = 0, inplace = True)
        columns = list(file.columns)
        columns.remove('Unnamed: 0')
        file2 = pd.read_excel(self.getFileName(), None)
        for i in range(len(file)):
            for j in range(len(columns)):
                #Begin checking Misspelling
                if file.iloc[i,0] not in file2['tracks']['Tracks'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet tracks_sessions|penalty [',file.iloc[i,0],'] is misspelled!'))
                elif columns[j] not in file2['sessions']['Sessions'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet tracks_sessions|penalty [',columns[j],'] is misspelled!'))
                #End of checking
                self.setTracksSessionsPenalty(self.getTrack(self.getTrackIndex(file.iloc[i,0])).getTrackName(), self.getSession(self.getSessionIndex(columns[j])).getSessionName(), file.iloc[i,j+1])
        
        #Reading 'tracks_rooms|penalty' sheet
        file = pd.read_excel(self.getFileName(), sheet_name = "tracks_rooms|penalty", keep_default_na = False, na_filter = False)
        file.replace(to_replace = '', value = 0, inplace = True)
        columns = list(file.columns)
        columns.remove('Unnamed: 0')
        for i in range(len(file)):
            for j in range(len(columns)):
                #Begin checking Misspelling
                if file.iloc[i,0] not in file2['tracks']['Tracks'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet tracks_rooms|penalty [',file.iloc[i,0],'] is misspelled!'))
                elif columns[j] not in file2['rooms']['Rooms'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet tracks_rooms|penalty [',columns[j],'] is misspelled!'))
                #End of checking
                self.setTracksRoomsPenalty(self.getTrack(self.getTrackIndex(file.iloc[i,0])).getTrackName(), self.getRoom(self.getRoomIndex(columns[j])).getRoomName(), file.iloc[i,j+1])
    
        #Reading 'similar tracks' sheet
        file = pd.read_excel(self.getFileName(), sheet_name = "similar tracks", keep_default_na = False, na_filter = False)
        file.replace(to_replace = '', value = 0, inplace = True)
        temp = file.values.tolist()
        for i in range(len(temp)):
            #Begin checking Misspelling (Only for rows, because only rows are used here)
            if temp[i][0] not in file2['tracks']['Tracks'].values:
                sys.exit(print('Misspelling Error!\nIn sheet similar tracks [',temp[i][0],'] is misspelled!'))
            #End of checking
            for y in range(len(temp)):
                if y != i:
                    self.setTracksTracksPenalty(self.getTrack(self.getTrackIndex(temp[i][0])).getTrackName(), self.getTrack(self.getTrackIndex(temp[y][0])).getTrackName(), temp[y][i+1])
                    self.setTracksTracksPenalty(self.getTrack(self.getTrackIndex(temp[y][0])).getTrackName(), self.getTrack(self.getTrackIndex(temp[i][0])).getTrackName(), temp[y][i+1])
        
        #Reading 'sessions_rooms|penalty' sheet
        file = pd.read_excel(self.getFileName(), sheet_name = "sessions_rooms|penalty", keep_default_na = False, na_filter = False)
        file.replace(to_replace = '', value = 0, inplace = True)
        columns = list(file.columns)
        columns.remove('Unnamed: 0')
        for i in range(len(file)):
            for j in range(len(columns)):
                #Begin checking Misspelling
                if file.iloc[i,0] not in file2['sessions']['Sessions'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet sessions_rooms|penalty [',file.iloc[i,0],'] is misspelled!'))
                elif columns[j] not in file2['rooms']['Rooms'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet sessions_rooms|penalty [',columns[j],'] is misspelled!'))
                #End of checking
                self.setSessionsRoomsPenalty(self.getSession(self.getSessionIndex(file.iloc[i,0])).getSessionName(), self.getRoom(self.getRoomIndex(columns[j])).getRoomName(), file.iloc[i,j+1])
        
        
        #Reading 'parameters' sheet
        file = pd.read_excel(self.getFileName(), sheet_name = "parameters", keep_default_na = False, na_filter = False)
        file = file.replace({'Unnamed: 1': timezones_format})
        file = file.applymap(lambda x: str(x).split(':'))
        par = Parameters.Parameters(local_time_zone = file.iloc[0,1][0], 
                              suitable_schedule_time_from = file.iloc[2,1], 
                              suitable_schedule_time_to = file.iloc[3,1],
                              less_suitable_schedule_time_from = file.iloc[5,1],
                              less_suitable_schedule_time_to = file.iloc[6,1],
                              tracks_sessions_penalty_weight = int(file.iloc[0,4][0]), 
                              tracks_rooms_penalty_weight = int(file.iloc[1,4][0]), 
                              sessions_rooms_penalty_weight = int(file.iloc[2,4][0]), 
                              similar_tracks_penalty_weight = int(file.iloc[3,4][0]), 
                              num_rooms_per_track = int(file.iloc[4,4][0]), 
                              parallel_tracks = int(file.iloc[5,4][0]), 
                              consecutive_tracks = int(file.iloc[6,4][0]), 
                              submissions_timezones_penalty_weight = int(file.iloc[7,4][0]), 
                              submissions_order = int(file.iloc[8,4][0]), 
                              submissions_sessions_penalty_weight = int(file.iloc[9,4][0]), 
                              submissions_rooms_penalty_weight = int(file.iloc[10,4][0]), 
                              presenters_conflicts = int(file.iloc[11,4][0]), 
                              attendees_conflicts = int(file.iloc[12,4][0]), 
                              chairs_conflicts = int(file.iloc[13,4][0]),
                              presenters_conflicts_timeslot_level = int(file.iloc[14,4][0]), 
                              attendees_conflicts_timeslot_level = int(file.iloc[15,4][0]),
                              small_tz_penalty = int(file.iloc[7,1][0]),
                              big_tz_penalty = int(file.iloc[9,1][0]))
        self.setParameters(par)
        
        #Feasibility Checking
        if self.getSumOfAvailableTimeSlots() * self.getNumberOfRooms() < self.getSumOfRequiredTimeSlots():
            sys.exit(print("Infeasible!: Not Enough Time Slots Available!\nConsider to add an extra session or room."))
        
        return par
    
    def FindConflictsNoAttendees(self):
        for i in range(self.getNumberOfSubmissions()):
            for y in range(self.getNumberOfSubmissions()):
                if y != i:
                    for x in range(len(self.getSubmission(i).getSubmissionPresentersList())):
                        if self.getSubmission(i).getSubmissionPresentersList()[x] != '':
                            for z in range(len(self.getSubmission(y).getSubmissionPresentersList())):
                                if self.getSubmission(i).getSubmissionPresentersList()[x] == self.getSubmission(y).getSubmissionPresentersList()[z]:
                                    self.getSubmission(i).setSubmissionPresenterConflicts(self.getSubmission(y))
                                    self.getSubmission(y).setSubmissionPresenterConflicts(self.getSubmission(i))
                            for z in range(len(self.getSubmission(y).getSubmissionTrack().getTrackChairsList())):
                                if (self.getSubmission(i).getSubmissionPresentersList()[x] == self.getSubmission(y).getSubmissionTrack().getTrackChairsList()[z]) and (self.getSubmission(i).getSubmissionTrack() != self.getSubmission(y).getSubmissionTrack()):
                                    self.getSubmission(i).setSubmissionPresenterConflicts(self.getSubmission(y))
                                    self.getSubmission(y).setSubmissionPresenterConflicts(self.getSubmission(i))
        for i in range(self.getNumberOfTracks()):
            for y in range(self.getNumberOfTracks()):
                if y != i:
                    for x in range(len(self.getTrack(i).getTrackChairsList())):
                        if self.getTrack(i).getTrackChairsList()[x] != '':
                            for z in range(len(self.getTrack(y).getTrackChairsList())):
                                if self.getTrack(i).getTrackChairsList()[x] == self.getTrack(y).getTrackChairsList()[z]:
                                    self.getTrack(i).setTrackChairConflicts(self.getTrack(y))
                                    self.getTrack(y).setTrackChairConflicts(self.getTrack(i))

    def FindAllConflicts(self):
        self.FindConflictsNoAttendees()
        for i in range(self.getNumberOfSubmissions()):
            for y in range(self.getNumberOfSubmissions()):
                if y != i:
                    for x in range(len(self.getSubmission(i).getSubmissionAttendeesList())):
                        if self.getSubmission(i).getSubmissionAttendeesList()[x] != '':
                            for z in range(len(self.getSubmission(y).getSubmissionAttendeesList())):
                                if self.getSubmission(i).getSubmissionAttendeesList()[x] == self.getSubmission(y).getSubmissionAttendeesList()[z]:
                                    self.getSubmission(i).setSubmissionAttendeeConflicts(self.getSubmission(y))
                                    self.getSubmission(y).setSubmissionAttendeeConflicts(self.getSubmission(i))
                    for x in range(len(self.getSubmission(i).getSubmissionAttendeesList())):
                        if self.getSubmission(i).getSubmissionAttendeesList()[x] != '':
                            for z in range(len(self.getSubmission(y).getSubmissionPresentersList())):
                                if self.getSubmission(i).getSubmissionAttendeesList()[x] == self.getSubmission(y).getSubmissionPresentersList()[z]:
                                    self.getSubmission(i).setSubmissionAttendeeConflicts(self.getSubmission(y))
                                    self.getSubmission(y).setSubmissionAttendeeConflicts(self.getSubmission(i))
                    for x in range(len(self.getSubmission(i).getSubmissionAttendeesList())):
                        if self.getSubmission(i).getSubmissionAttendeesList()[x] != '':
                            for z in range(len(self.getSubmission(y).getSubmissionTrack().getTrackChairsList())):
                                if (self.getSubmission(i).getSubmissionAttendeesList()[x] == self.getSubmission(y).getSubmissionTrack().getTrackChairsList()[z]) and (self.getSubmission(i).getSubmissionTrack() != self.getSubmission(y).getSubmissionTrack()):
                                    self.getSubmission(i).setSubmissionAttendeeConflicts(self.getSubmission(y))
                                    self.getSubmission(y).setSubmissionAttendeeConflicts(self.getSubmission(i))
    
    def FindConflicts(self, attendees = True):
        if attendees == True:
            self.FindAllConflicts()
        else:
            self.FindConflictsNoAttendees()
        
    def AssignTimezonesPenalties(self, parameters):
        suitable_from = dt.datetime(2021, 7, 21, int(parameters.getSuitableScheduleTimeFrom()[0]), int(parameters.getSuitableScheduleTimeFrom()[1])).time()
        suitable_to = dt.datetime(2021, 7, 21, int(parameters.getSuitableScheduleTimeTo()[0]), int(parameters.getSuitableScheduleTimeTo()[1])).time()
        less_suitable_from = dt.datetime(2021, 7, 21, int(parameters.getLessSuitableScheduleTimeFrom()[0]), int(parameters.getLessSuitableScheduleTimeFrom()[1])).time()
        less_suitable_to = dt.datetime(2021, 7, 21, int(parameters.getLessSuitableScheduleTimeTo()[0]), int(parameters.getLessSuitableScheduleTimeTo()[1])).time()
        for i in range(self.getNumberOfSessions()):
            #Defining session's local time zone
            loc_tz_st = self.getSession(i).getSessionStartTime().replace(tzinfo = pytz.timezone(parameters.getLocalTimeZone()))
            loc_tz_et = self.getSession(i).getSessionEndTime().replace(tzinfo = pytz.timezone(parameters.getLocalTimeZone()))
            for j in range(self.getNumberOfSubmissions()):
                #Defining submission's time zone
                submission_tz = pytz.timezone(self.getSubmission(j).getSubmissionTimezone())
                #Removing dates
                start_time = loc_tz_st.astimezone(submission_tz).time()
                end_time = loc_tz_et.astimezone(submission_tz).time()
                #Assigning submissionstimezones|penalty
                if start_time < less_suitable_from or end_time > less_suitable_to or end_time < less_suitable_from:
                    self.setSubmissionsTimezonesPenalty(self.getSubmission(j).getSubmissionName(), self.getSession(i).getSessionName(), parameters.getBigTimeZonePenalty())
                elif (start_time >= less_suitable_from and start_time < suitable_from) or (end_time > suitable_to and end_time <= less_suitable_to):
                    self.setSubmissionsTimezonesPenalty(self.getSubmission(j).getSubmissionName(), self.getSession(i).getSessionName(), parameters.getSmallTimeZonePenalty())
                else:
                    self.setSubmissionsTimezonesPenalty(self.getSubmission(j).getSubmissionName(), self.getSession(i).getSessionName(), 0)