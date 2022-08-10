import json
import os

import pytest

from ..modules.csv_reader import csv_to_dicts, sort_participant_data


def test_valid_csv():
    participants = csv_to_dicts("aa_experiment_part_2/tests_modules/data/valid_data.csv")
    assert participants[0]["Participant ID"] == "ID1"
    assert participants[3]["Participant ID"] == "ID4"
    assert participants[0]["Grade"] == "A"
    assert participants[3]["Grade"] == "D"
    assert participants[0]["Caste"] == "SC"
    assert participants[3]["Caste"] == "SC"
    assert participants[0]["Income less than 1 Lakh"] == "Yes"
    assert participants[3]["Income less than 1 Lakh"] == "No"
    assert participants[0]["Score"] == "10"
    assert participants[3]["Score"] == "0"


def test_invalid_csv():
    with pytest.raises(ValueError):
        csv_to_dicts("aa_experiment_part_2/tests_modules/data/invalid_data_no_rank.csv")
    with pytest.raises(ValueError):
        csv_to_dicts("aa_experiment_part_2/tests_modules/data/invalid_data_no_score.csv")
    with pytest.raises(ValueError):
        csv_to_dicts("aa_experiment_part_2/tests_modules/data/invalid_data_wrong_delimiter.csv")
    with pytest.raises(ValueError):
        csv_to_dicts("aa_experiment_part_2/tests_modules/data/invalid_data_rank_duplicates.csv")


with open("aa_experiment_part_2/tests_modules/data/dummy_participant_data.json", encoding="utf8") as fr:
    DUMMY_PARTICIPANT_DATA = json.load(fr)

with open("aa_experiment_part_2/tests_modules/data/dummy_participant_data_too_few_aa.json", encoding="utf8") as fr:
    DUMMY_PARTICIPANT_DATA_TOO_FEW_AA = json.load(fr)


def test_sorting_control():
    sorted_part_data = sort_participant_data(DUMMY_PARTICIPANT_DATA)
    assert sorted_part_data[0][0]["Participant ID"] == "ID2"
    assert sorted_part_data[0][1]["Participant ID"] == "ID4"
    assert sorted_part_data[0][2]["Participant ID"] == "ID3"
    assert sorted_part_data[0][3]["Participant ID"] == "ID5"
    assert sorted_part_data[0][4]["Participant ID"] == "ID1"
    assert sorted_part_data[0][5]["Participant ID"] == "ID6"
    assert sorted_part_data[0][6]["Participant ID"] == "ID8"
    assert sorted_part_data[0][7]["Participant ID"] == "ID7"

    assert sorted_part_data[1][0]["Participant ID"] == "ID1"
    assert sorted_part_data[1][1]["Participant ID"] == "ID2"
    assert sorted_part_data[1][2]["Participant ID"] == "ID3"
    assert sorted_part_data[1][3]["Participant ID"] == "ID4"
    assert sorted_part_data[1][4]["Participant ID"] == "ID5"
    assert sorted_part_data[1][5]["Participant ID"] == "ID6"

    last_two = [sorted_part_data[1][6]["Participant ID"],
                sorted_part_data[1][7]["Participant ID"]]
    assert "ID7" in last_two
    assert "ID8" in last_two


def test_sorting_aa():
    sorted_part_data = sort_participant_data(DUMMY_PARTICIPANT_DATA, "AA income")

    assert sorted_part_data[0][0]["Participant ID"] == "ID4"
    assert sorted_part_data[0][1]["Participant ID"] == "ID3"
    assert sorted_part_data[0][2]["Participant ID"] == "ID2"
    assert sorted_part_data[0][3]["Participant ID"] == "ID5"
    assert sorted_part_data[0][4]["Participant ID"] == "ID1"

    assert sorted_part_data[0][5]["Participant ID"] == "ID6"
    assert sorted_part_data[0][6]["Participant ID"] == "ID8"
    assert sorted_part_data[0][7]["Participant ID"] == "ID7"

    assert sorted_part_data[1][0]["Participant ID"] == "ID3"
    assert sorted_part_data[1][1]["Participant ID"] == "ID4"
    assert sorted_part_data[1][2]["Participant ID"] == "ID1"
    assert sorted_part_data[1][3]["Participant ID"] == "ID2"
    assert sorted_part_data[1][4]["Participant ID"] == "ID5"
    assert sorted_part_data[1][5]["Participant ID"] == "ID6"

    last_two = [sorted_part_data[1][6]["Participant ID"],
                sorted_part_data[1][7]["Participant ID"]]
    assert "ID7" in last_two
    assert "ID8" in last_two


def test_sorting_too_few_aa():
    sorted_part_data = sort_participant_data(DUMMY_PARTICIPANT_DATA_TOO_FEW_AA, "AA caste")
    assert sorted_part_data[0][0]["Participant ID"] == "ID1"
    assert sorted_part_data[0][1]["Participant ID"] == "ID2"
    assert sorted_part_data[0][2]["Participant ID"] == "ID3"
    assert sorted_part_data[0][3]["Participant ID"] == "ID4"
    assert sorted_part_data[0][4]["Participant ID"] == "ID5"

    assert sorted_part_data[0][5]["Participant ID"] == "ID6"

    last_two = [sorted_part_data[0][6]["Participant ID"],
                sorted_part_data[0][7]["Participant ID"]]
    assert "ID7" in last_two
    assert "ID8" in last_two

    assert sorted_part_data[1][0]["Participant ID"] == "ID1"
    assert sorted_part_data[1][1]["Participant ID"] == "ID3"
    assert sorted_part_data[1][2]["Participant ID"] == "ID2"
    assert sorted_part_data[1][3]["Participant ID"] == "ID4"
    assert sorted_part_data[1][4]["Participant ID"] == "ID5"
    assert sorted_part_data[1][5]["Participant ID"] == "ID6"

    last_two = [sorted_part_data[1][6]["Participant ID"],
                sorted_part_data[1][7]["Participant ID"]]
    assert "ID7" in last_two
    assert "ID8" in last_two
