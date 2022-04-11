from . import *
from otree.api import expect, Bot

NR_PARTICIPANTS_IN_CSV_FILE = 8


class PlayerBot(Bot):
    cases = ["treatment=control", "treatment=caste", "treatment=ews", "invalid input demographics",
             "invalid input score guessing", "control all bonuses", "control no bonuses"]

    def play_round(self):

        yield Submission(Consent, {
            "consent_given": True
        })

        if self.case in ["treatment=control", "control all bonuses", "control no bonuses"]:
            self.player.treatment = "control"
        elif self.case == "treatment=caste":
            self.player.treatment = "caste"
        else:
            self.player.treatment = "ews"

        print(self.player.treatment)  # This call is necessary, because otree does not store the
        # updated value otherwise, so do not remove!

        yield Start

        if self.case in ["treatment=control", "control all bonuses", "control no bonuses"]:
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
        if self.case in ["treatment=control", "control all bonuses", "control no bonuses"]:
            expect(html_aa, "not in", self.html)
        elif self.case == "treatment=caste":
            expect(html_aa, "in", self.html)
        else:
            expect(html_aa, "in", self.html)

        if self.case == "invalid input score guessing":
            for i in range(1, NR_PARTICIPANTS_IN_CSV_FILE+1):
                submit = dict()
                for j in range(1, NR_PARTICIPANTS_IN_CSV_FILE+1):
                    if j == i:
                        submit[f"guessed_score_{j}"] = -1  # invalid percentage
                    else:
                        submit[f"guessed_score_{j}"] = 50
                yield SubmissionMustFail(ScoreGuessing, submit)

            for i in range(1, NR_PARTICIPANTS_IN_CSV_FILE+1):
                submit = dict()
                for j in range(1, NR_PARTICIPANTS_IN_CSV_FILE+1):
                    if j == i:
                        submit[f"guessed_score_{j}"] = 101  # invalid percentage
                    else:
                        submit[f"guessed_score_{j}"] = 50
                yield SubmissionMustFail(ScoreGuessing, submit)

        submit = dict()
        if self.case == "control all bonuses":
            print(f"payoff is before {self.player.payoff}")
            for j in range(1, NR_PARTICIPANTS_IN_CSV_FILE + 1):
                submit[f"guessed_score_{j}"] = Constants.participant_data[j-1]["Score"]
            yield Submission(ScoreGuessing, submit)
            expect(self.player.payoff,
                   len(Constants.participant_data) *
                   self.player.session.config['possible_bonus_for_each_score_report'])
            print(f"payoff is now {self.player.payoff}")
        else:
            print(f"B payoff is before {self.player.payoff}")
            for j in range(1, NR_PARTICIPANTS_IN_CSV_FILE + 1):
                submit[f"guessed_score_{j}"] = int(
                    Constants.participant_data[j-1]["Score"])+1
            yield Submission(ScoreGuessing, submit)
            print(f"B payoff is now {self.player.payoff}")
            expect(self.player.payoff, 0)
        if self.case == "control all bonuses":
            yield Submission(CRT, {
                "crt_1": CORRECT_CRT_SOLUTIONS["crt_1"],
                "crt_2": CORRECT_CRT_SOLUTIONS["crt_2"],
                "crt_3": CORRECT_CRT_SOLUTIONS["crt_3"],
                "crt_4": CORRECT_CRT_SOLUTIONS["crt_4"],
                "crt_5": CORRECT_CRT_SOLUTIONS["crt_5"]
            })
            expect(self.player.payoff,
                   5*self.player.session.config['possible_bonus_for_each_crt_item'] +
                   len(Constants.participant_data) *
                   self.player.session.config['possible_bonus_for_each_score_report'])
        else:
            yield Submission(CRT, {
                "crt_1": 100,
                "crt_2": 100,
                "crt_3": 100,
                "crt_4": 100,
                "crt_5": 100
            })
            expect(self.player.payoff,
                   0)

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

        yield Results
