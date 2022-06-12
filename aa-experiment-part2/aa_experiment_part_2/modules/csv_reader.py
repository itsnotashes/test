"""
Functions to read in results from Raven tests and other data to be used in the experiment
"""
import os
import random
from copy import deepcopy

import pandas as pd
from typing import Dict, List, Tuple


def csv_to_dicts(csv_path: str) -> List[Dict[str, str]]:
    """
    Read a CSV file and for each row create a dict with the column name as key and the corresponding
    cell content as value

    :param csv_path: Path to the CSV file to be read
    :return: List of dicts containing participant information
    """
    if not os.path.isfile(csv_path):
        raise ValueError(f"ERROR: CSV file under '{csv_path}' could not be read. CWD: "
                         f"'{os.getcwd()}'")
    df = pd.read_csv(csv_path)
    column_names = list(df)
    if "Participant ID" not in column_names:
        raise ValueError(f"Column 'Participant ID' not found in CSV '{csv_path}', but is "
                         f"necessary to map the estimations from participants in this experiment "
                         f"to the raven test takers.")
    if "Score" not in column_names:
        raise ValueError(f"Column 'Score' not found in CSV '{csv_path}', but is necessary if "
                         "you want to compare the estimations with the true values.")
    nr_of_rows = len(df)
    df.drop_duplicates(subset=["Participant ID"], inplace=True)
    if len(df) != nr_of_rows:
        raise ValueError(f"CSV {csv_path} contains multiple participants with the same value for "
                         f"'Participant ID', but the rank should be unique.")
    if nr_of_rows != 8:
        raise ValueError(f"CSV {csv_path} contains {nr_of_rows} rows. 8 rows are expected.")
    if list(df["Participant ID"].values) != [f"ID{i}" for i in range(1, 8+1)]:
        raise ValueError("Participant IDs should be 'ID1', 'ID2', ... 'ID8' for each CSV file.")
    participants = []
    for index, row in df.iterrows():
        participant = dict()
        for column in column_names:
            participant[column] = str(row[column])
        participants.append(participant)
    return participants


def read_all_csvs_from_folder(
        parent_directory_path: str) -> Tuple[List[List[Dict[str, str]]], List[str]]:
    """
    Read all CSV files within a given directory. Per CSV for each row create a dict with the column
    name as key and the corresponding cell content as value

    :param parent_directory_path: Path to the folder in which the CSV files to be read are stored
    :return: List containing for each CSV file a List of dicts containing participant information
             and List containing CSV file names in the same order as their corresponding Lists
    """
    csv_file_names = []
    for file in os.listdir(parent_directory_path):
        if file.endswith(".csv") or file.endswith(".CSV"):
            csv_file_names.append(file)
    if len(csv_file_names) < 3:
        raise ValueError("Not enough CSV files found. At least 3 are required as each participant "
                         "is supposed to complete three score guessing tasks and should not get "
                         "the same data twice.")
    list_of_csv_values = []
    for csv_name in csv_file_names:
        list_of_csv_values.append(csv_to_dicts(parent_directory_path.strip(os.sep)+os.sep+csv_name))
    return list_of_csv_values, csv_file_names


def sort_participant_data(participant_data: List[List[Dict[str, str]]]) \
        -> List[List[Dict[str, str]]]:
    """
    Sort participants dicts in given participant data according to their grade, but randomly within
    a grade. This sorting is performed for all lists, each corresponding to a single CSV file

    :param participant_data: List of lists, each of which contains the participant data from one
                             CSV file
    :return: participant data sorted by grade, and randomly within grade

    >>> part_data = [[{"Grade": "B"}, {"Grade": "A"}], [{"Grade": "C"}, {"Grade": "D"}]]
    >>> sort_participant_data(part_data)
    [[{'Grade': 'A'}, {'Grade': 'B'}], [{'Grade': 'C'}, {'Grade': 'D'}]]
    """
    sorted_participant_data = []
    for part_data in participant_data:
        part_data = deepcopy(part_data)
        sorted_participant_data.append(
            sorted(part_data, key=lambda participant: (participant["Grade"], random.random())))
    return sorted_participant_data
