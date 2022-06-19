from . import *
from otree.api import expect, Bot

NR_PARTICIPANTS_IN_CSV_FILE = 8
read_important_note = False

class PlayerBot(Bot):
    # cases = ["treatment=control", "treatment=caste", "treatment=ews", "invalid input demographics",
    #          "invalid input score guessing", "control all boni", "control no boni",
    #          "does not match grade"]

    cases = ["payoff_mode_1", "payoff_mode_1 not all boni"]
    # cases = ["payoff_mode_2", "payoff_mode_2 not all boni"]




    cases_with_delayed_payoff_calculation = ["payoff_mode_2", "payoff_mode_1"]
    cases_with_control_treatment = ["treatment=control", "control all boni",
                                    "control no boni", "payoff_mode_2", "payoff_mode_1"]
    cases_all_boni = ["control all boni", "payoff_mode_2", "payoff_mode_1"]
    # Note: 'No boni' has still a small probability that all boni are obtained

    def play_round(self):
        global read_important_note
        if not read_important_note:
            input("IMPORTANT: As the session config variables cannot be set in the test without "
                  "being overwritten, you need to set the payoff mode to subsequently 1, 2 and 3"
                  " and activate / deactivate the corresponding test cases to avoid false "
                  "positives and to cover all test cases.\nPress Enter to continue...")
            read_important_note = True
        print(f"{self.case=}")
        print(f"Using payoff mode '{self.player.session.config['score_guessing_payoff_mode']}'")
        yield Submission(Consent, {
            "consent_given": True
        })

        if self.case in self.cases_with_control_treatment:
            self.player.treatment = "control"
        elif self.case == "treatment=caste":
            self.player.treatment = "caste"
        else:
            self.player.treatment = "ews"

        print(self.player.treatment)  # This call is necessary, because otree does not store the
        # updated value otherwise, so do not remove!

        yield Start

        if self.case in self.cases_with_control_treatment:
            expect("We selected the 5 best performers among these 8 people.", "in",
                   self.html)
        elif self.case == "treatment=caste":
            expect("3 of the 5 are the top scorers in the group of 8. The remaining 2 seats are "
                   "reserved for the best performing SC candidates.", "in",
                   self.html)
        else:
            expect("3 of the 5 are the top scorers in the group of 8. The remaining 2 seats are "
                   "reserved for the best performing EWS candidates.", "in",
                   self.html)

        yield Introduction

        html_aa = "<th>Affirmative action status</th>"
        if self.case in self.cases_with_control_treatment:
            expect(html_aa, "not in", self.html)
        else:
            expect(html_aa, "in", self.html)

        for nr_page, page in enumerate([ScoreGuessing, ScoreGuessing2, ScoreGuessing3]):
            if self.case == "invalid input score guessing":
                for i in range(1, NR_PARTICIPANTS_IN_CSV_FILE+1):
                    submit = dict()
                    for j in range(1, NR_PARTICIPANTS_IN_CSV_FILE+1):
                        if j == i:
                            submit[f"task_{nr_page+1}_guessed_score_ID{j}"] = -1  # inv. percentage
                        else:
                            submit[f"task_{nr_page+1}_guessed_score_ID{j}"] = 50
                    yield SubmissionMustFail(page, submit)

                for i in range(1, NR_PARTICIPANTS_IN_CSV_FILE+1):
                    submit = dict()
                    for j in range(1, NR_PARTICIPANTS_IN_CSV_FILE+1):
                        if j == i:
                            submit[f"task_{nr_page+1}_guessed_score_ID{j}"] = 101  # inv. percentage
                        else:
                            submit[f"task_{nr_page+1}_guessed_score_ID{j}"] = 50
                    yield SubmissionMustFail(page, submit)

            if self.case == "does not match grade":
                for i in range(1, NR_PARTICIPANTS_IN_CSV_FILE+1):
                    submit = dict()
                    for j in range(1, NR_PARTICIPANTS_IN_CSV_FILE+1):
                        if j == i:
                            grade = eval("Constants.participant_data["
                                         f"self.player.csv_data_index_task_{nr_page+1}][i-1]"
                                         "['Grade']")
                            score = int(
                                eval("Constants.participant_data["
                                     f"self.player.csv_data_index_task_{nr_page + 1}][i-1]"
                                     "['Score']"))
                            if grade in ["A", "B"]:
                                invalid = score - 30
                            else:
                                invalid = score + 30
                            submit[f"task_{nr_page + 1}_guessed_score_ID{j}"] = invalid
                        else:
                            submit[f"task_{nr_page + 1}_guessed_score_ID{j}"] = score
                    yield SubmissionMustFail(page, submit)
                    expect(self.player.gave_impossible_score_not_matching_grade, True)
                    expect(
                        "Please make sure that the scores you entered fit to the participants' "
                        "grades", "in", self.html)
            else:
                expect(self.player.gave_impossible_score_not_matching_grade, False)

            submit = dict()
            participant_data_for_task = eval("Constants.participant_data["
                                             f"self.player.csv_data_index_task_{nr_page + 1}]")
            print(participant_data_for_task)
            expected_boni = {
                0: len(Constants.participant_data[0]) *
                   self.player.session.config['possible_bonus_for_each_score_report'],
                1: 2 * len(Constants.participant_data[0]) *
                   self.player.session.config['possible_bonus_for_each_score_report'],
                2: 3 * len(Constants.participant_data[0]) *
                   self.player.session.config['possible_bonus_for_each_score_report']
            }
            if self.case in self.cases_all_boni:
                for participant in participant_data_for_task:
                    submit[f"task_{nr_page + 1}_guessed_score_{participant['Participant ID']}"] = \
                        participant["Score"]
                yield Submission(page, submit)
                bonus_for_task = eval(f"self.player.received_bonus_score_guessing_{nr_page+1}")
                for i in range(1, 3 + 1):
                    if eval(f"self.player.received_bonus_score_guessing_{i}") > 0:
                        expect(eval(f"self.player.received_bonus_score_guessing_{i}"),
                               expected_boni[0])
                if self.case in self.cases_with_delayed_payoff_calculation and nr_page < 2:
                    expect(bonus_for_task, expected_boni[0])
                    expect(self.player.payoff, 0)
                elif self.case == "payoff_mode_1":
                    expect(self.player.payoff, expected_boni[0])
                elif self.case == "payoff_mode_2":
                    expect(self.player.payoff, expected_boni[1])
                else:
                    expect(bonus_for_task, expected_boni[0])
                    expect(self.player.payoff, expected_boni[nr_page])
            else:
                for participant in participant_data_for_task:
                    submit[f"task_{nr_page + 1}_guessed_score_{participant['Participant ID']}"] = \
                        int(participant["Score"])+20
                yield Submission(page, submit)
                for i in range(1, 3 + 1):
                    if eval(f"self.player.received_bonus_score_guessing_{i}") > 0:
                        expect(eval(f"self.player.received_bonus_score_guessing_{i}"), "<",
                               expected_boni[0])
                if self.case in self.cases_with_delayed_payoff_calculation and nr_page < 2:
                    expect(self.player.payoff, 0)
                elif self.case == "payoff_mode_1 not all boni":
                    expect(self.player.payoff, "<", expected_boni[0])
                elif self.case == "payoff_mode_2 not all boni":
                    expect(self.player.payoff, "<", expected_boni[1])
                else:
                    expect(self.player.payoff, "<", expected_boni[nr_page])

        if self.case in self.cases_all_boni:
            yield Submission(CRT, {
                "crt_1": CORRECT_CRT_SOLUTIONS["crt_1"],
                "crt_2": CORRECT_CRT_SOLUTIONS["crt_2"],
                "crt_3": CORRECT_CRT_SOLUTIONS["crt_3"],
                "crt_4": CORRECT_CRT_SOLUTIONS["crt_4"],
                "crt_5": CORRECT_CRT_SOLUTIONS["crt_5"]
            })
            if self.case == "control all boni":
                expect(self.player.payoff,
                       5*self.player.session.config['possible_bonus_for_each_crt_item'] +
                       3*len(Constants.participant_data[0]) *
                       self.player.session.config['possible_bonus_for_each_score_report'])
            elif self.case == "payoff_mode_1":
                expect(self.player.payoff,
                       5 * self.player.session.config['possible_bonus_for_each_crt_item'] +
                       1 * len(Constants.participant_data[0]) *
                       self.player.session.config['possible_bonus_for_each_score_report'])
            elif self.case == "payoff_mode_2":
                expect(self.player.payoff,
                       5 * self.player.session.config['possible_bonus_for_each_crt_item'] +
                       2 * len(Constants.participant_data[0]) *
                       self.player.session.config['possible_bonus_for_each_score_report'])
        else:
            yield Submission(CRT, {
                "crt_1": 100,
                "crt_2": 100,
                "crt_3": 100,
                "crt_4": 100,
                "crt_5": 100
            })
            if self.case == "payoff_mode_1 not all boni":
                expect(self.player.payoff, "<", len(Constants.participant_data[0]) *
                       self.player.session.config['possible_bonus_for_each_score_report'])
            elif self.case == "payoff_mode_2 not all boni":
                expect(self.player.payoff, "<", 2 * len(Constants.participant_data[0]) *
                       self.player.session.config['possible_bonus_for_each_score_report'])
            else:
                expect(self.player.payoff, "<", 3*len(Constants.participant_data[0]) *
                       self.player.session.config['possible_bonus_for_each_score_report'])

        if self.case == "invalid input demographics":
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 5,  # Invalid
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,  # biological_sex missing
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",  # gender missing
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "school": "private",  # religion missing
                                         "caste": "SC",
                                         "jati": "some jati",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "caste": "SC",  # school missing
                                         "jati": "some jati",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "household_size": 2,  # caste missing
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": -2,  # invalid
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": -2,  # Invalid
                                         "occupation_father": 1,
                                         "occupation_mother": 1,
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 25,  # Invalid
                                         "occupation_mother": 1,
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 25,  # Invalid
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,  # fathers_education missing
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,  # mothers_education missing
                                         "fathers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,  # income_less_than_100_000 missing
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "state_of_residence": "Bihār",
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 25,
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,  # state_of_residence missing
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "living_area": "Metro urban"
                                     })
            yield SubmissionMustFail(Demographics,
                                     {
                                         "age": 5,  # Invalid
                                         "biological_sex": "Male",
                                         "gender": "Male",
                                         "religion": "Hindu",
                                         "school": "private",
                                         "jati": "some jati",
                                         "caste": "SC",
                                         "household_size": 2,
                                         "years_of_education": 2,
                                         "occupation_father": 1,
                                         "occupation_mother": 1,
                                         "fathers_education": "SECONDARY",
                                         "mothers_education": "SECONDARY",
                                         "income_less_than_100_000": False,
                                         "state_of_residence": "Bihār"  # living_area missing
                                     })
        yield Submission(Demographics,
                         {
                             "age": 25,
                             "biological_sex": "Male",
                             "gender": "Male",
                             "religion": "Hindu",
                             "school": "private",
                             "jati": "some jati",
                             "caste": "SC",
                             "household_size": 2,
                             "years_of_education": 2,
                             "occupation_father": 1,
                             "occupation_mother": 1,
                             "fathers_education": "SECONDARY",
                             "mothers_education": "SECONDARY",
                             "income_less_than_100_000": False,
                             "state_of_residence": "Bihār",
                             "living_area": "Metro urban"
                         })
        if self.case == "control all boni":
            expect(self.player.payoff,
                   5 * self.player.session.config['possible_bonus_for_each_crt_item'] +
                   3*len(Constants.participant_data[0]) *
                   self.player.session.config['possible_bonus_for_each_score_report'] +
                   self.player.session.config['show_up_fee'])
        elif self.case == "payoff_mode_1":
            expect(self.player.payoff,
                   5 * self.player.session.config['possible_bonus_for_each_crt_item'] +
                   len(Constants.participant_data[0]) *
                   self.player.session.config['possible_bonus_for_each_score_report'] +
                   self.player.session.config['show_up_fee'])
        elif self.case == "payoff_mode_2":
            expect(self.player.payoff,
                   5 * self.player.session.config['possible_bonus_for_each_crt_item'] +
                   2*len(Constants.participant_data[0]) *
                   self.player.session.config['possible_bonus_for_each_score_report'] +
                   self.player.session.config['show_up_fee'])
        elif self.case == "payoff_mode_1 not all boni":
            expect(self.player.payoff, "<", len(Constants.participant_data[0]) *
                   self.player.session.config['possible_bonus_for_each_score_report'] +
                   self.player.session.config['show_up_fee'])
            expect(self.player.payoff, ">=", self.player.session.config['show_up_fee'])
        elif self.case == "payoff_mode_2 not all boni":
            expect(self.player.payoff, "<", 2*len(Constants.participant_data[0]) *
                   self.player.session.config['possible_bonus_for_each_score_report'] +
                   self.player.session.config['show_up_fee'])
            expect(self.player.payoff, ">=", self.player.session.config['show_up_fee'])
        else:
            expect(self.player.payoff, "<", 3*len(Constants.participant_data[0]) *
                   self.player.session.config['possible_bonus_for_each_score_report'] +
                   self.player.session.config['show_up_fee'])
            expect(self.player.payoff, ">=",  self.player.session.config['show_up_fee'])
        yield Results
