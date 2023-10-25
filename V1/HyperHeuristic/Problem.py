# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:12:46 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

import Submission
import Track
import Room
import Session
import Participant
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
        self.__participants = []
        
        self.__rooms_map = {}
        self.__sessions_map = {}
        self.__tracks_map = {}
        self.__submissions_map = {}
        self.__participants_map = {}
        
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
    #Participants
    def getNumberOfParticipants(self) -> int:
        return len(self.__participants)
    def getParticipant(self, participant_index) -> Participant.Participant:
        return self.__participants[participant_index]
    def getParticipantList(self) -> list:
        return self.__participants
    def setParticipant(self, participant_object):
        self.__participants.append(participant_object)
        self.__participants_map[participant_object.getParticipantID()] = len(self.__participants_map)
    def getParticipantIndex(self, participant_id):
        return self.__participants_map[participant_id]
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
    #Conversions
    def convertTracksElementsToObjects(self):
        for i in range(self.getNumberOfTracks()):
            temp = [self.getTrack(self.getTrackIndex(self.getTrack(i).getTrackSameRoomList()[j])) for j in range(len(self.getTrack(i).getTrackSameRoomList())) if self.getTrack(i).getTrackSameRoomList()[j] != '']
            self.getTrack(i).setTrackSameRoomList(temp)
            temp = [self.getTrack(self.getTrackIndex(self.getTrack(i).getTrackSameBuildingList()[j])) for j in range(len(self.getTrack(i).getTrackSameBuildingList())) if self.getTrack(i).getTrackSameBuildingList()[j] != '']
            self.getTrack(i).setTrackSameBuildingList(temp)
            temp = [self.getParticipant(self.getParticipantIndex(self.getTrack(i).getTrackOrganisersList()[j])) for j in range(len(self.getTrack(i).getTrackOrganisersList())) if self.getTrack(i).getTrackOrganisersList()[j] != '']
            self.getTrack(i).setTrackOrganisersList(temp)
    def convertSubmissionsElementsToObjects(self):
        for i in range(self.getNumberOfSubmissions()):
            temp = [self.getSubmission(self.getSubmissionIndex(self.getSubmission(i).getSubmissionSameSessionList()[j])) for j in range(len(self.getSubmission(i).getSubmissionSameSessionList())) if self.getSubmission(i).getSubmissionSameSessionList()[j] != '']
            self.getSubmission(i).setSubmissionSameSessionList(temp)
            temp = [self.getSubmission(self.getSubmissionIndex(self.getSubmission(i).getSubmissionDifferentSessionList()[j])) for j in range(len(self.getSubmission(i).getSubmissionDifferentSessionList())) if self.getSubmission(i).getSubmissionDifferentSessionList()[j] != '']
            self.getSubmission(i).setSubmissionDifferentSessionList(temp)
            temp = [self.getParticipant(self.getParticipantIndex(self.getSubmission(i).getSubmissionSpeakersList()[j])) for j in range(len(self.getSubmission(i).getSubmissionSpeakersList())) if self.getSubmission(i).getSubmissionSpeakersList()[j] != '']
            self.getSubmission(i).setSubmissionSpeakersList(temp)
            temp = [self.getParticipant(self.getParticipantIndex(self.getSubmission(i).getSubmissionAttendeesList()[j])) for j in range(len(self.getSubmission(i).getSubmissionAttendeesList())) if self.getSubmission(i).getSubmissionAttendeesList()[j] != '']
            self.getSubmission(i).setSubmissionAttendeesList(temp)
    def ReadProblemInstance(self):
        #Begin checking All Sheets Exist
        file = pd.read_excel(self.getFileName(), None)
        existing_sheets = file.keys()
        required_sheets = ['parameters', 'submissions', 'tracks', 'participants', 'sessions', 'rooms','tracks_sessions|penalty', 'tracks_rooms|penalty', 'tracks_tracks|penalty', 'sessions_rooms|penalty']
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
        duplicates_check = ['tracks_sessions|penalty', 'tracks_rooms|penalty', 'tracks_tracks|penalty', 'sessions_rooms|penalty']
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
            temp1 = str(file.iloc[i,5]).split(':')
            temp2 = str(file.iloc[i,6]).split(':')
            start_time = dt.datetime(2021, 7, 21, int(temp1[0]), int(temp1[1]))
            end_time = dt.datetime(2021, 7, 21, int(temp2[0]), int(temp2[1]))
            self.setSession(Session.Session(file.iloc[i,0], file.iloc[i,1], file.iloc[i,2], file.iloc[i,3], file.iloc[i,4], start_time, end_time))
        
        #Reading Rooms
        file = pd.read_excel(self.getFileName(), sheet_name = "rooms", keep_default_na = False, na_filter = False)
        for i in range(len(file)):
            self.setRoom(Room.Room(file.iloc[i,0], file.iloc[i,1]))
            
        #Reading Participants
        file = pd.read_excel(self.getFileName(), sheet_name = "participants", keep_default_na = False, na_filter = False)
        timezones_format = {'GMT-12':'Etc/GMT+12', 'GMT-11':'Etc/GMT+11', 'GMT-10':'Etc/GMT+10', 'GMT-9':'Etc/GMT+9', 
                                        'GMT-8':'Etc/GMT+8', 'GMT-7':'Etc/GMT+7', 'GMT-6':'Etc/GMT+6', 'GMT-5':'Etc/GMT+5', 
                                        'GMT-4':'Etc/GMT+4', 'GMT-3':'Etc/GMT+3', 'GMT-2':'Etc/GMT+2', 'GMT-1':'Etc/GMT+1',
                                        'GMT+0':'Etc/GMT+0', 'GMT+12':'Etc/GMT-12', 'GMT+11':'Etc/GMT-11', 'GMT+10':'Etc/GMT-10', 
                                        'GMT+9':'Etc/GMT-9', 'GMT+8':'Etc/GMT-8', 'GMT+7':'Etc/GMT-7', 'GMT+6':'Etc/GMT-6', 
                                        'GMT+5':'Etc/GMT-5', 'GMT+4':'Etc/GMT-4', 'GMT+3':'Etc/GMT-3', 'GMT+2':'Etc/GMT-2', 
                                        'GMT+1':'Etc/GMT-1'}
        file.replace({'Time Zone': timezones_format}, inplace = True)
        for i in range(len(file)):
            self.setParticipant(Participant.Participant(file.iloc[i,0], file.iloc[i,1], file.iloc[i,2], file.iloc[i,3], file.iloc[i,4], file.iloc[i,5], file.iloc[i,6], file.iloc[i,7], file.iloc[i,8]))
        
        #Reading Submissions part 1
        file = pd.read_excel(self.getFileName(), sheet_name = "submissions", keep_default_na = False, na_filter = False)
        columns = list(file.columns)
        df1 = file.iloc[:, :11]
        df2 = file.iloc[:, 11:]
        df2.replace(to_replace = '', value = 0, inplace = True)
        file = df1.join(df2)
        freq = file['Track'].value_counts(sort = False)
        file2 = pd.read_excel(self.getFileName(), sheet_name = "tracks", keep_default_na = False, na_filter = False)

        #Begin checking for Track of zero size
        for i in file2['Track'].values:
            if i not in freq.keys():
                sys.exit(print('Track Error!\n[ Track Name:', i, ']', ' has none submissions!'))
        #End of checking
        
        #Begin checking number of items
        file3 = pd.read_excel(self.getFileName(), None, header = None)
        if (len(file3['tracks_sessions|penalty'].iloc[0,:]) != len(file3['sessions'])) or (len(file3['tracks_sessions|penalty'].iloc[:,0]) != len(file3['tracks'])):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_sessions|penalty.'))
        if (len(file3['tracks_rooms|penalty'].iloc[0,:]) != len(file3['rooms'])) or (len(file3['tracks_rooms|penalty'].iloc[:,0]) != len(file3['tracks'])):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_rooms|penalty.'))
        if (len(file3['tracks_tracks|penalty'].iloc[0,:]) != len(file3['tracks'])) or (len(file3['tracks_tracks|penalty'].iloc[:,0]) != len(file3['tracks'])):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_tracks|penalty.'))
        if (len(file3['sessions_rooms|penalty'].iloc[0,:]) != len(file3['rooms'])) or (len(file3['sessions_rooms|penalty'].iloc[:,0]) != len(file3['sessions'])):
            sys.exit(print('Incorrect Number of Items Error! \nIncorrect number of items in sheet sessions_rooms|penalty.'))
        #End of checking
        
        #Reading Tracks
        for i in range(len(file2)):
            self.setTrack(Track.Track(file2.iloc[i,0], file2.iloc[i,1], file2.iloc[i,2], file2.iloc[i,3], file2.iloc[i,4], list(file2.iloc[i,5].split(", ")), list(file2.iloc[i,6].split(", ")), list(file2.iloc[i,7].split(", ")), [], []))
        self.convertTracksElementsToObjects()
        
        #Begin checking for number of items between submissions and sessions & rooms
        if len(columns[11:]) != self.getNumberOfSessions() + self.getNumberOfRooms():
            sys.exit(print('Incorrect Number of Items Error! \nEnsure that number of sessions and rooms in sheet submissions match with number of itmes in sessions and rooms sheets.'))
        #End of checking
        
        #Begin checking for matching names between submissions and sessions sheets
        for i in range(self.getNumberOfSessions()):
            if self.getSession(i).getSessionName() not in columns[11:11 + self.getNumberOfSessions()]:
                sys.exit(print('Sessions Error!\nSessions names in submissions sheet must match those in sessions sheet.'))
        #End of checking
        
        #Begin checking for matching names between submissions and rooms sheets
        for i in range(self.getNumberOfRooms()):
            if self.getRoom(i).getRoomName() not in columns[11 + self.getNumberOfSessions():11 + self.getNumberOfSessions() + self.getNumberOfRooms()]:
                sys.exit(print('Rooms Error!\nRooms names in submissions sheet must match those in rooms sheet.'))
        #End of checking
        
        #Reading Submissions part 2
        for i in range(len(file)):
            #Begin checking for Unknown Track
            if file.iloc[i,1] not in file2['Track'].values:
                sys.exit(print('Track Error! \nUnknown track for', file.iloc[i,0], '[ Track name:', file.iloc[i,1],'].'))
            #End of checking
            
            self.setSubmission(Submission.Submission(file.iloc[i,0], self.getTrack(self.getTrackIndex(file.iloc[i,1])), file.iloc[i,2], file.iloc[i,3], file.iloc[i,4], file.iloc[i,5], file.iloc[i,6], list(file.iloc[i,7].split(", ")), list(file.iloc[i,8].split(", ")), list(file.iloc[i,9].split(", ")), list(file.iloc[i,10].split(", ")), [], []))
            self.getTrack(self.getTrackIndex(file.iloc[i,1])).setTrackSubmissions(self.getSubmission(self.getSubmissionIndex(file.iloc[i,0])))
            for j in range(11, 11 + self.getNumberOfSessions()):
                self.setSubmissionsSessionsPenalty(self.getSubmission(self.getSubmissionIndex(file.iloc[i,0])).getSubmissionName(), self.getSession(self.getSessionIndex(columns[j])).getSessionName(), file.iloc[i,j])
            for y in range(11 + self.getNumberOfSessions(), 11 + self.getNumberOfSessions() + self.getNumberOfRooms()):
                self.setSubmissionsRoomsPenalty(self.getSubmission(self.getSubmissionIndex(file.iloc[i,0])).getSubmissionName(), self.getRoom(self.getRoomIndex(columns[y])).getRoomName(), file.iloc[i,y])
        self.convertSubmissionsElementsToObjects()
        
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
                if file.iloc[i,0] not in file2['tracks']['Track'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet tracks_sessions|penalty [',file.iloc[i,0],'] is misspelled!'))
                elif columns[j] not in file2['sessions']['Session'].values:
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
                if file.iloc[i,0] not in file2['tracks']['Track'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet tracks_rooms|penalty [',file.iloc[i,0],'] is misspelled!'))
                elif columns[j] not in file2['rooms']['Room'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet tracks_rooms|penalty [',columns[j],'] is misspelled!'))
                #End of checking
                self.setTracksRoomsPenalty(self.getTrack(self.getTrackIndex(file.iloc[i,0])).getTrackName(), self.getRoom(self.getRoomIndex(columns[j])).getRoomName(), file.iloc[i,j+1])
    
        #Reading 'tracks_tracks|penalty' sheet
        file = pd.read_excel(self.getFileName(), sheet_name = "tracks_tracks|penalty", keep_default_na = False, na_filter = False)
        file.replace(to_replace = '', value = 0, inplace = True)
        temp = file.values.tolist()
        for i in range(len(temp)):
            #Begin checking Misspelling (Only for rows, because only rows are used here)
            if temp[i][0] not in file2['tracks']['Track'].values:
                sys.exit(print('Misspelling Error!\nIn sheet tracks_tracks|penalty [',temp[i][0],'] is misspelled!'))
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
                if file.iloc[i,0] not in file2['sessions']['Session'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet sessions_rooms|penalty [',file.iloc[i,0],'] is misspelled!'))
                elif columns[j] not in file2['rooms']['Room'].values:
                    sys.exit(print('Misspelling Error!\nIn sheet sessions_rooms|penalty [',columns[j],'] is misspelled!'))
                #End of checking
                self.setSessionsRoomsPenalty(self.getSession(self.getSessionIndex(file.iloc[i,0])).getSessionName(), self.getRoom(self.getRoomIndex(columns[j])).getRoomName(), file.iloc[i,j+1])
        
        #Reading 'parameters' sheet
        file = pd.read_excel(self.getFileName(), sheet_name = "parameters", keep_default_na = False, na_filter = False)
        file = file.replace({'Unnamed: 1': timezones_format})
        par = Parameters.Parameters(local_time_zone = file.iloc[0,1], 
                              schedule_time_from = file.iloc[2,1], 
                              schedule_time_to = file.iloc[3,1],
                              tracks_sessions_penalty_weight = file.iloc[0,4], 
                              tracks_rooms_penalty_weight = file.iloc[1,4], 
                              sessions_rooms_penalty_weight = file.iloc[2,4], 
                              tracks_tracks_penalty_weight = file.iloc[3,4], 
                              num_rooms_per_track = file.iloc[4,4], 
                              parallel_tracks = file.iloc[5,4], 
                              consecutive_tracks = file.iloc[6,4], 
                              tracks_relative_order = file.iloc[7,4], 
                              tracks_actual_order = file.iloc[8,4], 
                              submissions_timezones_penalty_weight = file.iloc[9,4], 
                              submissions_relative_order = file.iloc[10,4], 
                              submissions_actual_order = file.iloc[11,4], 
                              submissions_sessions_penalty_weight = file.iloc[12,4], 
                              submissions_rooms_penalty_weight = file.iloc[13,4], 
                              speakers_conflicts = file.iloc[14,4], 
                              attendees_conflicts = file.iloc[15,4], 
                              organiser_conflicts = file.iloc[16,4], 
                              track_duration = file.iloc[17,4], 
                              tracks_buildings = file.iloc[18,4], 
                              balance = file.iloc[19,4], 
                              speakers_conflicts_timeslot_level = file.iloc[20,4], 
                              attendees_conflicts_timeslot_level = file.iloc[21,4], 
                              open_session_weight = file.iloc[22,4], 
                              close_session_weight = file.iloc[23,4], 
                              same_session_weight = file.iloc[24,4], 
                              different_session_weight = file.iloc[25,4], 
                              track_max_num_days_weight = file.iloc[26,4], 
                              tracks_same_room_weight = file.iloc[27,4], 
                              tracks_same_building_weight = file.iloc[28,4], 
                              preferred_num_time_slots = file.iloc[29,4], 
                              min_num_time_slots = file.iloc[30,4], 
                              max_num_time_slots = file.iloc[31,4])
        self.setParameters(par)
        '''
        print(par.getTracksSessionsPenaltyWeight())
        print(par.getTracksRoomsPenaltyWeight())
        print(par.getSessionsRoomsPenaltyWeight())
        print(par.getTracksTracksPenaltyWeight())
        print(par.getNumOfRoomsPerTrackWeight())
        print(par.getParallelTracksWeight())
        print(par.getConsecutiveTracksWeight())
        print(par.getTracksRelativeOrderWeight())
        print(par.getTracksActualOrderWeight())
        print(par.getSubmissionsTimezonesWeight())
        print(par.getSubmissionsRelativeOrderWeight())
        print(par.getSubmissionsActualOrderWeight())
        print(par.getSubmissionsSessionsPenaltyWeight())
        print(par.getSubmissionsRoomsPenaltyWeight())
        print(par.getSpeakersConflictsWeight())
        print(par.getAteendeesConflictsWeight())
        print(par.getOrganisersConflictsWeight())
        print(par.getTrackDurationWeight())
        print(par.getTracksBuildingsWeight())
        print(par.getBalanceWeight())
        print(par.getSpeakersConflictsTimeslotLevelWeight())
        print(par.getAttendeesConflictsTimeSlotWeight())
        print(par.getOpenSessionWeight())
        print(par.getCloseSessionWeight())
        print(par.getSameSessionWeight())
        print(par.getDifferentSessionWeight())
        print(par.getTrackMaxNumDaysWeight())
        print(par.getTrackSameRoomWeight())
        print(par.getTracksSameBuildingWeight())
        print(par.getPreferredNumTimeSlotsWeight())
        print(par.getMinNumTimeSlotsWeight())
        print(par.getMaxNumTimeSlotsWeight())
        '''
        
        #Feasibility Checking
        if self.getSumOfAvailableTimeSlots() * self.getNumberOfRooms() < self.getSumOfRequiredTimeSlots():
            sys.exit(print("Infeasible!: Not Enough Time Slots Available!\nConsider to add an extra session or room."))
        
        return par
    
    def FindConflictsNoAttendees(self):
        for i in range(self.getNumberOfSubmissions()):
            for y in range(self.getNumberOfSubmissions()):
                if y != i:
                    for x in range(len(self.getSubmission(i).getSubmissionSpeakersList())):
                        if self.getSubmission(i).getSubmissionSpeakersList()[x] != '':
                            for z in range(len(self.getSubmission(y).getSubmissionSpeakersList())):
                                if self.getSubmission(i).getSubmissionSpeakersList()[x] == self.getSubmission(y).getSubmissionSpeakersList()[z]:
                                    self.getSubmission(i).setSubmissionSpeakerConflicts(self.getSubmission(y))
                                    self.getSubmission(y).setSubmissionSpeakerConflicts(self.getSubmission(i))
                            for z in range(len(self.getSubmission(y).getSubmissionTrack().getTrackOrganisersList())):
                                if (self.getSubmission(i).getSubmissionSpeakersList()[x] == self.getSubmission(y).getSubmissionTrack().getTrackOrganisersList()[z]) and (self.getSubmission(i).getSubmissionTrack() != self.getSubmission(y).getSubmissionTrack()):
                                    self.getSubmission(i).setSubmissionSpeakerConflicts(self.getSubmission(y))
                                    self.getSubmission(y).setSubmissionSpeakerConflicts(self.getSubmission(i))
        for i in range(self.getNumberOfTracks()):
            for y in range(self.getNumberOfTracks()):
                if y != i:
                    for x in range(len(self.getTrack(i).getTrackOrganisersList())):
                        if self.getTrack(i).getTrackOrganisersList()[x] != '':
                            for z in range(len(self.getTrack(y).getTrackOrganisersList())):
                                if self.getTrack(i).getTrackOrganisersList()[x] == self.getTrack(y).getTrackOrganisersList()[z]:
                                    self.getTrack(i).setTrackOrganiserConflicts(self.getTrack(y))
                                    self.getTrack(y).setTrackOrganiserConflicts(self.getTrack(i))

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
                            for z in range(len(self.getSubmission(y).getSubmissionSpeakersList())):
                                if self.getSubmission(i).getSubmissionAttendeesList()[x] == self.getSubmission(y).getSubmissionSpeakersList()[z]:
                                    self.getSubmission(i).setSubmissionAttendeeConflicts(self.getSubmission(y))
                                    self.getSubmission(y).setSubmissionAttendeeConflicts(self.getSubmission(i))
                    for x in range(len(self.getSubmission(i).getSubmissionAttendeesList())):
                        if self.getSubmission(i).getSubmissionAttendeesList()[x] != '':
                            for z in range(len(self.getSubmission(y).getSubmissionTrack().getTrackOrganisersList())):
                                if (self.getSubmission(i).getSubmissionAttendeesList()[x] == self.getSubmission(y).getSubmissionTrack().getTrackOrganisersList()[z]) and (self.getSubmission(i).getSubmissionTrack() != self.getSubmission(y).getSubmissionTrack()):
                                    self.getSubmission(i).setSubmissionAttendeeConflicts(self.getSubmission(y))
                                    self.getSubmission(y).setSubmissionAttendeeConflicts(self.getSubmission(i))
    
    def FindConflicts(self, attendees = True):
        if attendees == True:
            self.FindAllConflicts()
        else:
            self.FindConflictsNoAttendees()
        
    def AssignTimezonesPenalties(self):
        temp_schedule_from = str(self.getParameters().getScheduleTimeFrom()).split(':')
        schedule_from = dt.datetime(2021, 7, 21, int(temp_schedule_from[0]), int(temp_schedule_from[1])).time()
        temp_schedule_to = str(self.getParameters().getScheduleTimeTo()).split(':')
        schedule_to = dt.datetime(2021, 7, 21, int(temp_schedule_to[0]), int(temp_schedule_to[1])).time()
        #Assign local time zone to session time
        for i in range(self.getNumberOfSessions()):
            loc_tz_st = self.getSession(i).getSessionStartTime().replace(tzinfo = pytz.timezone(self.getParameters().getLocalTimeZone()))
            loc_tz_et = self.getSession(i).getSessionEndTime().replace(tzinfo = pytz.timezone(self.getParameters().getLocalTimeZone()))
            #Assign speaker's time zone to submission
            for j in range(self.getNumberOfSubmissions()):
                if len(self.getSubmission(j).getSubmissionSpeakersList()) == 1:
                    speaker_tz = pytz.timezone(self.getSubmission(j).getSubmissionSpeakers(0).getParticipantTimeZone())
                    start_time = loc_tz_st.astimezone(speaker_tz).time()
                    end_time = loc_tz_et.astimezone(speaker_tz).time()
                    if (start_time >= schedule_from) and (end_time <= schedule_to) and (start_time < schedule_to) and (end_time > schedule_from):
                        self.setSubmissionsTimezonesPenalty(self.getSubmission(j).getSubmissionName(), self.getSession(i).getSessionName(), 0)
                    else:
                        temp_start_time = str(start_time).split(':')
                        temp_end_time = str(end_time).split(':')
                        distance = [abs(int(temp_start_time[0]) - int(temp_schedule_from[0])), abs(int(temp_end_time[0]) - int(temp_schedule_to[0]))]
                        violation = min(distance)
                        self.setSubmissionsTimezonesPenalty(self.getSubmission(j).getSubmissionName(), self.getSession(i).getSessionName(), violation)
                #Assign speakers time zones to submission
                else:
                    violation_sum = 0
                    for speaker in range(len(self.getSubmission(j).getSubmissionSpeakersList())):
                        speaker_tz = pytz.timezone(self.getSubmission(j).getSubmissionSpeakers(speaker).getParticipantTimeZone())
                        start_time = loc_tz_st.astimezone(speaker_tz).time()
                        end_time = loc_tz_et.astimezone(speaker_tz).time()
                        if (start_time >= schedule_from) and (end_time <= schedule_to) and (start_time < schedule_to) and (end_time > schedule_from):
                            pass
                        else:
                            temp_start_time = str(start_time).split(':')
                            temp_end_time = str(end_time).split(':')
                            distance = [abs(int(temp_start_time[0]) - int(temp_schedule_from[0])), abs(int(temp_end_time[0]) - int(temp_schedule_to[0]))]
                            violation = min(distance)
                            violation_sum += violation
                    violation_sum = violation_sum * len(self.getSubmission(j).getSubmissionSpeakersList())
                    self.setSubmissionsTimezonesPenalty(self.getSubmission(j).getSubmissionName(), self.getSession(i).getSessionName(), violation_sum)