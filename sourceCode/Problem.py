# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:12:46 2023

@author: pylya
"""

from Submissions import *
from Tracks import *
from Rooms import *
from Sessions import *
import pandas as pd
import datetime as dt
import pytz
import sys

class Problem():
    def __init__(self, file_name = "N2OR.xlsx"):
        
        self.__file_name = file_name
        self.__max_day = 0
        
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
    
    def getFileName(self):
        return self.__file_name
    def setFileName(self, file_name):
        self.__file_name = file_name
    #Rooms    
    def getNumberOfRooms(self):
        return len(self.__rooms)
    def setRoom(self, room_name):
        self.__rooms.append(room_name)
        self.__rooms_map[room_name.getName()] = len(self.__rooms_map)
    def getRoom(self, room_index) -> Room:
        if room_index < len(self.__rooms) and room_index >= 0:
            return self.__rooms[room_index]
        else:
            sys.exit(print('Room index Error!\nIndex should range from 0 to', len(self.__rooms)-1, 'but index', room_index, 'was passed.'))
    def getRoomIndex(self, room_name):
        return self.__rooms_map[room_name]
    #Sessions
    def getNumberOfSessions(self):
        return len(self.__sessions)
    def setSession(self, session_name):
        self.__sessions.append(session_name)
        self.__sessions_map[session_name.getName()] = len(self.__sessions_map)
    def getSession(self, session_index) -> Session:
        if session_index < len(self.__sessions) and session_index >= 0:
            return self.__sessions[session_index]
        else:
            sys.exit(print('Session index Error!\nIndex should range from 0 to', len(self.__sessions)-1, 'but index', session_index, 'was passed.'))
    def getSessionIndex(self, session_name):
        return self.__sessions_map[session_name]
    def getSumOfTimeSlots(self):
        self.__sum_of_time_slots = 0
        for i in range(len(self.__sessions)):
            self.__sum_of_time_slots += self.__sessions[i].getMaxTimeSlots()
        return self.__sum_of_time_slots
    def getLargestSession(self):
        temp = []
        for i in range(len(self.__sessions)):
            temp.append(self.getSession(i).getMaxTimeSlots())
        return max(temp)
    def setMaxDay(self, value):
        self.__max_day = value
    def getMaxDay(self):
        return self.__max_day
    #Tracks
    def getNumberOfTracks(self):
        return len(self.__tracks)
    def setTrack(self, track_name):
        self.__tracks.append(track_name)
        self.__tracks_map[track_name.getName()] = len(self.__tracks_map)
    def getTrack(self, track_index) -> Track:
        if track_index != -1:
            return self.__tracks[track_index]
        else:
            sys.exit(print('Track index Error!\nIndex should range from 0 to', len(self.__tracks)-1, 'but index', track_index, 'was passed.'))
    def getTrackIndex(self, track_name):
        return self.__tracks_map[track_name]
    #Submissions
    def getNumberOfSubmissions(self):
        return len(self.__submissions)
    def setSubmission(self, submission_name):
        self.__submissions.append(submission_name)
        self.__submissions_map[submission_name.getName()] = len(self.__submissions_map)
    def getSubmission(self, submission_index) -> Submission:
        return self.__submissions[submission_index]
    def getSubmissionIndex(self, submission_name):
        return self.__submissions_map[submission_name]  
    def getTotalRequiredTimeSlots(self):
        self.__total_required_time_slots = 0
        for i in range(len(self.__submissions)):
            self.__total_required_time_slots += self.__submissions[i].getRequiredTimeSlots()
        return self.__total_required_time_slots
    #Submissions_sessions|penalty
    def setSubmissionsSessionsPenalty(self, submission_name, session_name, penalty):
        self.__submissions_sessions_penalty_map[submission_name + session_name] = penalty
    def getSubmissionsSessionsPenalty(self, submission_name, session_name):
        return self.__submissions_sessions_penalty_map[submission_name + session_name]
    def getSubmissionsSessionsPenaltybyIndex(self, submission_index, session_index):
        return self.__submissions_sessions_penalty_map[self.getSubmission(submission_index).getName() + self.getSession(session_index).getName()]
    #Submissions_Timezones|penalty
    def setSubmissionsTimezonesPenalty(self, submission_name, session_name, penalty):
        self.__submissions_timezones_penalty_map[submission_name + session_name] = penalty
    def getSubmissionsTimezonesPenalty(self, submission_name, session_name):
        return self.__submissions_timezones_penalty_map[submission_name + session_name]
    def getSubmissionsTimezonesPenaltybyIndex(self, submission_index, session_index):
        return self.__submissions_timezones_penalty_map[self.getSubmission(submission_index).getName() + self.getSession(session_index).getName()]
    #Submissions_rooms|penalty
    def setSubmissionsRoomsPenalty(self, submission_name, room_name, penalty):
        self.__submissions_rooms_penalty_map[submission_name + room_name] = penalty
    def getSubmissionsRoomsPenalty(self, submission_name, room_name):
        return self.__submissions_rooms_penalty_map[submission_name + room_name]
    def getSubmissionsRoomsPenaltybyIndex(self, submission_index, room_index):
        return self.__submissions_rooms_penalty_map[self.getSubmission(submission_index).getName() + self.getRoom(room_index).getName()]
    #Tracks_sessions|penalty
    def setTracksSessionsPenalty(self, track_name, session_name, penalty):
        self.__tracks_sessions_penalty_map[track_name + session_name] = penalty
    def getTracksSessionsPenalty(self, track_name, session_name):
        return self.__tracks_sessions_penalty_map[track_name + session_name]
    def getTracksSessionsPenaltybyIndex(self, track_index, session_index):
        return self.__tracks_sessions_penalty_map[self.getTrack(track_index).getName() + self.getSession(session_index).getName()]
    #Tracks_rooms|penalty
    def setTracksRoomsPenalty(self, track_name, room_name, penalty):
        self.__tracks_rooms_penalty_map[track_name + room_name] = penalty
    def getTracksRoomsPenalty(self, track_name, room_name):
        return self.__tracks_rooms_penalty_map[track_name + room_name]
    def getTracksRoomsPenaltybyIndex(self, track_index, room_index):
        return self.__tracks_rooms_penalty_map[self.getTrack(track_index).getName() + self.getRoom(room_index).getName()]
    #Tracks_tracks|penalty
    def setTracksTracksPenalty(self, track_name1, track_name2, penalty):
        self.__tracks_tracks_penalty_map[track_name1 + track_name2] = penalty
    def getTracksTracksPenalty(self, track1_name, track2_name):
        return self.__tracks_tracks_penalty_map[track1_name + track2_name]
    def getTracksTracksPenaltybyIndex(self, track1_index, track2_index):
        if track1_index != track2_index:
            return self.__tracks_tracks_penalty_map[self.getTrack(track1_index).getName() + self.getTrack(track2_index).getName()]
        else:
            sys.exit(print('Index Error!\nSame indexes were passed.\nPenalties between tracks require different indexes.'))
    #Sessions_rooms|penalty
    def setSessionsRoomsPenalty(self, session_name, room_name, penalty):
        self.__sessions_rooms_penalty_map[session_name + room_name] = penalty
    def getSessionsRoomsPenalty(self, session_name, room_name):
        return self.__sessions_rooms_penalty_map[session_name + room_name]
    def getSessionsRoomsPenaltybyIndex(self, session_index, room_index):
        return self.__sessions_rooms_penalty_map[self.getSession(session_index).getName() + self.getRoom(room_index).getName()]
    
    def ReadProblemInstance(self):
        #Begin checking All Sheets Exist
        file = pd.read_excel(self.getFileName(), None)
        existing_sheets = file.keys()
        required_sheets = ['submissions', 'tracks', 'sessions', 'rooms', 'parameters','tracks_sessions|penalty', 'tracks_rooms|penalty', 'tracks_tracks|penalty', 'sessions_rooms|penalty']
        for i in required_sheets:
            if i not in existing_sheets:
                sys.exit(print('Missing Sheet Error! \nMissing Sheet:', i))
        #End of checking
        
        #Begin checking for Duplicates
        duplicates_check = ['submissions', 'tracks', 'sessions', 'rooms']
        for i in duplicates_check:
            duplicates = file[i].duplicated(subset = file[i].columns[0])
            if duplicates.any() == True:
                duplicate_indexes = duplicates[duplicates].index
                sys.exit(print('Duplicates Error! \nThe following duplicates were found in sheet', i,':\n', file[i][file[i].columns[0]][duplicate_indexes]))
        #End of checking
        
        #Begin checking number of items
        file = pd.read_excel(self.getFileName(), None, header = None)
        if len(file['tracks_sessions|penalty'].iloc[0,:]) != len(file['sessions']) or len(file['tracks_sessions|penalty'].iloc[:,0]) != len(file['tracks']):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_sessions|penalty.'))
        if len(file['tracks_rooms|penalty'].iloc[0,:]) != len(file['rooms']) or len(file['tracks_rooms|penalty'].iloc[:,0]) != len(file['tracks']):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_rooms|penalty.'))
        if len(file['tracks_tracks|penalty'].iloc[0,:]) != len(file['tracks']) or len(file['tracks_tracks|penalty'].iloc[:,0]) != len(file['tracks']):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_tracks|penalty.'))
        if len(file['sessions_rooms|penalty'].iloc[0,:]) != len(file['rooms']) or len(file['sessions_rooms|penalty'].iloc[:,0]) != len(file['sessions']):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet sessions_rooms|penalty.'))
        #End of checking
        
        #Begin checking for Duplicates in penalty sheets
        duplicates_check = ['tracks_sessions|penalty', 'tracks_rooms|penalty', 'tracks_tracks|penalty', 'sessions_rooms|penalty']
        for i in duplicates_check:
            duplicate_row = file[i].iloc[0,:].duplicated()
            duplicate_column = file[i].iloc[:,0].duplicated()
            if duplicate_row.any() == True:
                duplicate_indexes = duplicate_row[duplicate_row].index
                sys.exit(print('Duplicates Error! \nThe following duplicates were found in sheet', i,':\n', file[i].iloc[0, duplicate_indexes]))
            elif duplicate_column.any() == True:
                duplicate_indexes = duplicate_column[duplicate_column].index
                sys.exit(print('Duplicates Error! \nThe following duplicates were found in sheet', i,':\n', file[i][file[i].columns[0]][duplicate_indexes]))
        #End of checking
        
        #Reading Sessions
        file = pd.read_excel(self.getFileName(), sheet_name = "sessions", keep_default_na = False, na_filter = False)
        for i in range(len(file)):
            temp1 = str(file.iloc[i,3]).split(':')
            temp2 = str(file.iloc[i,4]).split(':')
            start_time = dt.datetime(2021, 7, 21, int(temp1[0]), int(temp1[1]))
            end_time = dt.datetime(2021, 7, 21, int(temp2[0]), int(temp2[1]))
            self.setSession(Session(file.iloc[i,0], file.iloc[i,1], file.iloc[i, 2], start_time, end_time))
        
        #Reading Rooms
        file = pd.read_excel(self.getFileName(), sheet_name = "rooms", keep_default_na = False, na_filter = False)
        for i in range(len(file)):
            self.setRoom(Room(file.iloc[i,0]))
        
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
        
        #Reading Tracks
        for i in range(len(file)):
            if file.iloc[i,2] > 1:
                freq[file.iloc[i,1]] += file.iloc[i,2] - 1
        for i in range(len(file2['Tracks'].values)):
            for y in range(len(freq)):
                if file2.iloc[i,0] == freq.index[y]:
                    self.setTrack(Track(file2.iloc[i,0], freq[y], file2.iloc[i,1], list(file2.iloc[i,2].split(", "))))

        #Begin checking for number of items between submissions and sessions & rooms
        if len(columns[7:]) != self.getNumberOfSessions() + self.getNumberOfRooms():
            sys.exit(print('Incorrect Number of Items Error! \nEnsure that number of sessions and rooms in sheet submissions match with number of itmes in sessions and rooms sheets.'))
        #End of checking
        
        #Begin checking for matching names between submissions and sessions sheets
        for i in range(self.getNumberOfSessions()):
            if self.getSession(i).getName() not in columns[7:7 + self.getNumberOfSessions()]:
                sys.exit(print('Sessions Error!\nSessions names in submissions sheet must match those in sessions sheet.'))
        #End of checking
        
        #Begin checking for matching names between submissions and rooms sheets
        for i in range(self.getNumberOfRooms()):
            if self.getRoom(i).getName() not in columns[7 + self.getNumberOfSessions():7 + self.getNumberOfSessions() + self.getNumberOfRooms()]:
                sys.exit(print('Rooms Error!\nRooms names in submissions sheet must match those in rooms sheet.'))
        #End of checking
        
        #Reading Submissions part 2
        for i in range(len(file)):
            #Begin checking for Unknown Track
            if file.iloc[i,1] not in file2['Tracks'].values:
                sys.exit(print('Track Error! \nUnknown track for', file.iloc[i,0], '[ Track name:', file.iloc[i,1],'].'))
            #End of checking
            self.setSubmission(Submission(file.iloc[i,0], self.getTrack(self.getTrackIndex(file.iloc[i,1])), file.iloc[i,2], file.iloc[i,3], file.iloc[i,4] , list(file.iloc[i,5].split(", ")), list(file.iloc[i,6].split(", "))))
            self.getTrack(self.getTrackIndex(file.iloc[i,1])).setSubmission(self.getSubmission(self.getSubmissionIndex(file.iloc[i,0])))
            for j in range(7, 7 + self.getNumberOfSessions()):
                self.setSubmissionsSessionsPenalty(self.getSubmission(self.getSubmissionIndex(file.iloc[i,0])).getName(), self.getSession(self.getSessionIndex(columns[j])).getName(), file.iloc[i,j])
            for y in range(7 + self.getNumberOfSessions(), 7 + self.getNumberOfSessions() + self.getNumberOfRooms()):
                self.setSubmissionsRoomsPenalty(self.getSubmission(self.getSubmissionIndex(file.iloc[i,0])).getName(), self.getRoom(self.getRoomIndex(columns[y])).getName(), file.iloc[i,y])

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
                self.setTracksSessionsPenalty(self.getTrack(self.getTrackIndex(file.iloc[i,0])).getName(), self.getSession(self.getSessionIndex(columns[j])).getName(), file.iloc[i,j+1])
        
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
                self.setTracksRoomsPenalty(self.getTrack(self.getTrackIndex(file.iloc[i,0])).getName(), self.getRoom(self.getRoomIndex(columns[j])).getName(), file.iloc[i,j+1])
    
        #Reading 'tracks_tracks|penalty' sheet
        file = pd.read_excel(self.getFileName(), sheet_name = "tracks_tracks|penalty", keep_default_na = False, na_filter = False)
        file.replace(to_replace = '', value = 0, inplace = True)
        temp = file.values.tolist()
        for i in range(len(temp)):
            #Begin checking Misspelling (Only for rows, because only rows are used here)
            if temp[i][0] not in file2['tracks']['Tracks'].values:
                sys.exit(print('Misspelling Error!\nIn sheet tracks_tracks|penalty [',temp[i][0],'] is misspelled!'))
            #End of checking
            for y in range(len(temp)):
                if y != i:
                    self.setTracksTracksPenalty(self.getTrack(self.getTrackIndex(temp[i][0])).getName(), self.getTrack(self.getTrackIndex(temp[y][0])).getName(), temp[y][i+1])
                    self.setTracksTracksPenalty(self.getTrack(self.getTrackIndex(temp[y][0])).getName(), self.getTrack(self.getTrackIndex(temp[i][0])).getName(), temp[y][i+1])
        
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
                self.setSessionsRoomsPenalty(self.getSession(self.getSessionIndex(file.iloc[i,0])).getName(), self.getRoom(self.getRoomIndex(columns[j])).getName(), file.iloc[i,j+1])
        
        #Reading 'parameters' sheet
        file = pd.read_excel(self.getFileName(), sheet_name = "parameters", keep_default_na = False, na_filter = False)
        file = file.replace({'Unnamed: 1': timezones_format})
        weights = list(file.iloc[:, 4])
        file = file.applymap(lambda x: str(x).split(':'))
        indexes = [2,3,6,7]
        parameters = [file.iloc[0,1][0]]    
        for i in indexes:
            parameters.append([int(file.iloc[i,1][0]), int(file.iloc[i,1][1])])
        parameters.append([int(file.iloc[4,1][0]), int(file.iloc[8,1][0])])
        parameters.append(weights)
        
        #Feasibility Checking
        if self.getSumOfTimeSlots() * self.getNumberOfRooms() < self.getTotalRequiredTimeSlots():
            sys.exit(print("Error!: Not Enough Time Slots Available!\nConsider to add an extra session or room."))
        
        #Estimating session-day with max timeslots
        dates = []
        for session in range(self.getNumberOfSessions()):
            if self.getSession(session).getDate() not in dates:
                dates.append(self.getSession(session).getDate())
        temp = []
        for date in dates:
            temp2 = 0
            for session in range(self.getNumberOfSessions()):
                if self.getSession(session).getDate() == date:
                    temp2 += self.getSession(session).getMaxTimeSlots()
            temp.append(temp2)
        self.setMaxDay(max(temp))
        
        return parameters
        
    def FindConflictsNoAttendees(self):
        for i in range(self.getNumberOfSubmissions()):
            for y in range(self.getNumberOfSubmissions()):
                if y != i:
                    for x in range(len(self.getSubmission(i).getSpeakers())):
                        if self.getSubmission(i).getSpeakers()[x] != '':
                            for z in range(len(self.getSubmission(y).getSpeakers())):
                                if self.getSubmission(i).getSpeakers()[x] == self.getSubmission(y).getSpeakers()[z]:
                                    self.getSubmission(i).setSpeakerConflicts(self.getSubmission(y).getName())
                                    self.getSubmission(y).setSpeakerConflicts(self.getSubmission(i).getName())
                            for z in range(len(self.getSubmission(y).getTrack().getOrganizers())):
                                if self.getSubmission(i).getSpeakers()[x] == self.getSubmission(y).getTrack().getOrganizers()[z] and self.getSubmission(i).getTrack().getName() != self.getSubmission(y).getTrack().getName():
                                    self.getSubmission(i).setSpeakerConflicts(self.getSubmission(y).getName())
                                    self.getSubmission(y).setSpeakerConflicts(self.getSubmission(i).getName())
        for i in range(self.getNumberOfTracks()):
            for y in range(self.getNumberOfTracks()):
                if y != i:
                    for x in range(len(self.getTrack(i).getOrganizers())):
                        if self.getTrack(i).getOrganizers()[x] != '':
                            for z in range(len(self.getTrack(y).getOrganizers())):
                                if self.getTrack(i).getOrganizers()[x] == self.getTrack(y).getOrganizers()[z]:
                                    self.getTrack(i).setOrganizerConflicts(self.getTrack(y).getName())
                                    self.getTrack(y).setOrganizerConflicts(self.getTrack(i).getName())

    def FindAllConflicts(self):
        self.FindConflictsNoAttendees()
        for i in range(self.getNumberOfSubmissions()):
            for y in range(self.getNumberOfSubmissions()):
                if y != i:
                    for x in range(len(self.getSubmission(i).getAttendees())):
                        if self.getSubmission(i).getAttendees()[x] != '':
                            for z in range(len(self.getSubmission(y).getAttendees())):
                                if self.getSubmission(i).getAttendees()[x] == self.getSubmission(y).getAttendees()[z]:
                                    self.getSubmission(i).setAttendeeConflicts(self.getSubmission(y).getName())
                                    self.getSubmission(y).setAttendeeConflicts(self.getSubmission(i).getName())
                    for x in range(len(self.getSubmission(i).getAttendees())):
                        if self.getSubmission(i).getAttendees()[x] != '':
                            for z in range(len(self.getSubmission(y).getSpeakers())):
                                if self.getSubmission(i).getAttendees()[x] == self.getSubmission(y).getSpeakers()[z]:
                                    self.getSubmission(i).setAttendeeConflicts(self.getSubmission(y).getName())
                                    self.getSubmission(y).setAttendeeConflicts(self.getSubmission(i).getName())
                    for x in range(len(self.getSubmission(i).getAttendees())):
                        if self.getSubmission(i).getAttendees()[x] != '':
                            for z in range(len(self.getSubmission(y).getTrack().getOrganizers())):
                                if self.getSubmission(i).getAttendees()[x] == self.getSubmission(y).getTrack().getOrganizers()[z] and self.getSubmission(i).getTrack().getName() != self.getSubmission(y).getTrack().getName():
                                    self.getSubmission(i).setAttendeeConflicts(self.getSubmission(y).getName())
                                    self.getSubmission(y).setAttendeeConflicts(self.getSubmission(i).getName())
    
    def FindConflicts(self, attendees = True):
        if attendees == True:
            self.FindAllConflicts()
        else:
            self.FindConflictsNoAttendees()
        
    def AssignTimezonesPenalties(self, parameters):
        suitable_from = dt.datetime(2021, 7, 21, parameters[1][0], parameters[1][1]).time()
        suitable_to = dt.datetime(2021, 7, 21, parameters[2][0], parameters[2][1]).time()
        less_suitable_from = dt.datetime(2021, 7, 21, parameters[3][0], parameters[3][1]).time()
        less_suitable_to = dt.datetime(2021, 7, 21, parameters[4][0], parameters[4][1]).time()
        for i in range(self.getNumberOfSessions()):
            #Defining session's local time zone
            loc_tz_st = self.getSession(i).getStartTime().replace(tzinfo = pytz.timezone(parameters[0]))
            loc_tz_et = self.getSession(i).getEndTime().replace(tzinfo = pytz.timezone(parameters[0]))
            for j in range(self.getNumberOfSubmissions()):
                #Defining submission's time zone
                submission_tz = pytz.timezone(self.getSubmission(j).getTimeZone())
                #Removing dates
                start_time = loc_tz_st.astimezone(submission_tz).time()
                end_time = loc_tz_et.astimezone(submission_tz).time()
                #Assigning submissionstimezones|penalty
                if start_time < less_suitable_from or end_time > less_suitable_to or end_time < less_suitable_from:
                    self.setSubmissionsTimezonesPenalty(self.getSubmission(j).getName(), self.getSession(i).getName(), parameters[5][0])
                elif (start_time >= less_suitable_from and start_time < suitable_from) or (end_time > suitable_to and end_time <= less_suitable_to):
                    self.setSubmissionsTimezonesPenalty(self.getSubmission(j).getName(), self.getSession(i).getName(), parameters[5][1])
                else:
                    self.setSubmissionsTimezonesPenalty(self.getSubmission(j).getName(), self.getSession(i).getName(), 0)