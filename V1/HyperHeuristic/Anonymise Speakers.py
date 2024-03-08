
import pandas as pd

def update_lists(df, col):
    global current_participant
    output_list = []
    for i in range(len(df)):
        if type(df.loc[i][col]) == str:
            temp_list = []
            for j in df.loc[i][col].split(", "):
                if j not in participant:
                    participant[j] = "P" + str(current_participant)
                    current_participant=current_participant+1
                temp_list.append(participant[j])
            output_list.append(temp_list)
        else:
            output_list.append([])
    return output_list
    

def print_new_participant_ids():
    for i in participant:
        print(participant[i]+"\t"+i)

def print_track_organisers():
    for i in track_organisers:
        for j in range(len(i)):
            if j != len(i)-1:
                print(i[j], end=", ")
            else:
                print(i[j])

def print_submission_speakers():
    for i in submission_speakers:
        for j in range(len(i)):
            if j != len(i)-1:
                print(i[j], end=", ")
            else:
                print(i[j])

def print_submission_attendees():
    for i in submission_attendees:
        if len(i) == 0:
            print()
        for j in range(len(i)):
            if j != len(i)-1:
                print(i[j], end=", ")
            else:
                print(i[j])

df_tracks = pd.read_excel("../Dataset/OR60F3.xlsx", sheet_name = "tracks")
df_participants = pd.read_excel("../Dataset/OR60F3.xlsx", sheet_name = "participants")
df_submissions = pd.read_excel("../Dataset/OR60F3.xlsx", sheet_name = "submissions")

participant = {}
submission_speakers = []
submission_attendees = []
current_participant = 0

track_organisers = update_lists(df_tracks, "Organisers")
submission_speakers = update_lists(df_submissions, "Speakers")
submission_attendees = update_lists(df_submissions, "Attendees")

print_new_participant_ids()
print('-------------------')
print_track_organisers()
print('-------------------')
print_submission_speakers()
print('-------------------')
print_submission_attendees()