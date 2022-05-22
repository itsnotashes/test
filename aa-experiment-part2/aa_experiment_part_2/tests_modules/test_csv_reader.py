import pytest

from ..modules.csv_reader import csv_to_dicts


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
