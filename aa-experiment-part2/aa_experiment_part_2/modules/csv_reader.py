"""
Functions to read in results from Raven tests and other data to be used in the experiment
"""
import os
import warnings

import pandas as pd
from typing import Dict, List


def csv_to_dicts(csv_path: str) -> List[Dict[str, str]]:
    """
    Read a CSV file and for each row create a dict with the column name as key and the corresponding
    cell content as value

    :param csv_path: Path to the CSV file to be read
    :return: List of dicts containing participant information
    """
    if not os.path.isfile(csv_path):
        raise ValueError(f"ERROR: CSV file under '{csv_path}' could not be read")
    df = pd.read_csv(csv_path)
    column_names = list(df)
    if "Participant rank" not in column_names:
        raise ValueError(f"ERROR: Column 'Participant rank' not found in CSV '{csv_path}', but is "
                         f"necessary to map the estimations from participants in this experiment "
                         f"to the raven test takers.")
    if "Score" not in column_names:
        warnings.warn(f"WARNING: Column 'Score' not found in CSV '{csv_path}', but is necessary if "
                      f"you want to compare the estimations with the true values.")
    nr_of_rows = len(df)
    df.drop_duplicates(subset=["Participant rank"], inplace=True)
    if len(df) != nr_of_rows:
        raise ValueError(f"CSV {csv_path} contains multiple participants with the same value for "
                         f"'Participant rank', but the rank should be unique.")
    participants = []
    for index, row in df.iterrows():
        participant = dict()
        for column in column_names:
            participant[column] = str(row[column])
        participants.append(participant)
    return participants
