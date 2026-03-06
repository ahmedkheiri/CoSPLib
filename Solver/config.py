# Input file
INSTANCE_NAME = "N2OR"
INPUT_PATH = "Dataset/" + INSTANCE_NAME + ".xlsx"
REQUIRED_SHEETS = [
    "parameters",
    "submissions",
    "tracks",
    "sessions",
    "rooms",
    "tracks_sessions|penalty",
    "tracks_rooms|penalty",
    "similar tracks",
    "sessions_rooms|penalty",
]

# Optimisation
HYPER_HEURISTIC = False
MATHEURISTIC = False
EXACT_MILP = False
EXTENDED_MILP = True

# Utils
# Timezone values are inversed intentionally
TIMEZONE_MAPPING = {
    "GMT-12": "Etc/GMT+12",
    "GMT-11": "Etc/GMT+11",
    "GMT-10": "Etc/GMT+10",
    "GMT-9": "Etc/GMT+9",
    "GMT-8": "Etc/GMT+8",
    "GMT-7": "Etc/GMT+7",
    "GMT-6": "Etc/GMT+6",
    "GMT-5": "Etc/GMT+5",
    "GMT-4": "Etc/GMT+4",
    "GMT-3": "Etc/GMT+3",
    "GMT-2": "Etc/GMT+2",
    "GMT-1": "Etc/GMT+1",
    "GMT+0": "Etc/GMT+0",
    "GMT+12": "Etc/GMT-12",
    "GMT+11": "Etc/GMT-11",
    "GMT+10": "Etc/GMT-10",
    "GMT+9": "Etc/GMT-9",
    "GMT+8": "Etc/GMT-8",
    "GMT+7": "Etc/GMT-7",
    "GMT+6": "Etc/GMT-6",
    "GMT+5": "Etc/GMT-5",
    "GMT+4": "Etc/GMT-4",
    "GMT+3": "Etc/GMT-3",
    "GMT+2": "Etc/GMT-2",
    "GMT+1": "Etc/GMT-1",
}
COLUMNS_TO_INCLUDE = 7
