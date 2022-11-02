import json
import math
from copy import deepcopy
from typing import Union

from otree.api import *
from .modules.csv_reader import read_all_csvs_from_folder, sort_participant_data
import itertools
import random

c = Currency
CSV_PATH = "_static/aa_experiment_part_2/"
# CSV_PATH = "aa_experiment_part_2/tests_modules/data/valid_csvs/"  # Necessary for tests

doc = """
AA experiment
"""
TREATMENTS = ["control", "caste", "ews"]
OCCUPATION_CHOICES = [[1, 'cultivation own land'],
                      [2, 'cultivation leased land'],
                      [3, 'agricultural labour'],
                      [4, 'animal husbandry'],
                      [5, 'rental income'],
                      [6, 'self-employment'],
                      [7, 'skilled labour (electrician, plumber, tailor, carpenter, mason)'],
                      [8, 'unskilled labour (construction worker, helper, stone cutter, NREGA '
                          'work etc)'],
                      [9, 'non farm petty business (kirana store, tailoring shop, carpentry '
                          'shop, handicrafts business, fishing etc)'],
                      [10, 'Salaried in private firm'],
                      [11, 'Salaried in govt enterprise'],
                      [12, 'Household work'],
                      [13, 'Consultant/freelance'],
                      [14, 'Gig worker (Ola, Uber, Zomato, Swiggy '
                           'etc.)'],
                      [-1, 'Others, specify']]

CORRECT_CRT_SOLUTIONS = {
    "crt_1": 2,
    "crt_2": 23,
    "crt_3": 4,
    "crt_4": 29,
    "crt_5": 4
}

GRADE_RANGES = {
    "A": (75, 100),
    "B": (50, 74),
    "C": (25, 49),
    "D": (0, 24)
}

LATIN_NR = {
    1: "I",
    2: "II",
    3: "III"
}


def get_grade_for_percentage_correct(percentage_correct: Union[float, int]) -> str:
    """
    Get the grade for a participant who answered 'percentage_correct' % of all questions
    correctly

    :param percentage_correct: The percentage of questions correctly answered
    :return: Grade, i.e. 'A', 'B', 'C', or 'D'
    """
    if percentage_correct > 100 or percentage_correct < 0:
        raise ValueError("'percentage_correct' needs to be in the range from 0 to 100")
    if percentage_correct >= 75:
        return "A"
    if percentage_correct >= 50:
        return "B"
    if percentage_correct >= 25:
        return "C"
    return "D"


class Constants(BaseConstants):
    name_in_url = 'aa_experiment_part_2'
    players_per_group = None
    num_rounds = 1
    print("Reading CSV")
    participant_data, csv_names = read_all_csvs_from_folder(CSV_PATH)
    print("CSV read order:", csv_names)
    participant_data_for_treatment = dict()
    # participant_data_for_treatment[TREATMENTS[0]] = sort_participant_data(participant_data)
    # participant_data_for_treatment[TREATMENTS[1]] = sort_participant_data(participant_data,
    #                                                                       "AA caste")
    # participant_data_for_treatment[TREATMENTS[2]] = sort_participant_data(participant_data,
    #                                                               "AA income")

    # with open("sorted_participant_data.json", "w") as fw:
    #     json.dump(participant_data_for_treatment, fw)
        # json.dump(participant_data, fw)
    
    with open("unsorted_part_data.json", "w") as fx:
        json.dump(participant_data, fx)


def creating_session(subsession):
    subsession.session.treatment_iterator = itertools.cycle(TREATMENTS)
    csv_indizes = []
    for i in range(len(Constants.participant_data)):
        csv_indizes += len(TREATMENTS)*[i]
    subsession.session.csv_index_iterator = itertools.cycle(csv_indizes)
    subsession.session.nr_participants_in_treatments = dict()
    for treatment in TREATMENTS:
        subsession.session.nr_participants_in_treatments[treatment] = 0


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent_given = models.BooleanField(initial=False)
    treatment = models.StringField(initial="not assigned")

    # Index of Constant.participant_data to avoid having the same data twice for one participant
    csv_data_index_task_1 = models.IntegerField(blank=True, initial=0)
    csv_data_index_task_2 = models.IntegerField(blank=True, initial=0)
    csv_data_index_task_3 = models.IntegerField(blank=True, initial=0)

    csv_name_task_1 = models.StringField(blank=True, initial="Not determined yet")
    csv_name_task_2 = models.StringField(blank=True, initial="Not determined yet")
    csv_name_task_3 = models.StringField(blank=True, initial="Not determined yet")

    payoff_relevant_score_guessing_tasks = models.StringField(blank=True, initial="")
    # Record non-attentive score guessers
    gave_impossible_score_not_matching_grade = models.BooleanField(blank=True, initial=False)

    age = models.IntegerField(min=16, max=150, label="What is your age?")
    biological_sex = models.StringField(label="What is your sex assigned at birth?", choices=[
        "Male",
        "Female"
    ])

    gender = models.StringField(label="What is your Gender?", choices=[
        "Male",
        "Female",
        "Other"
    ])

    religion = models.StringField(label="What is your religion?", choices=[
        "Hindu",
        "Muslim",
        "Christian",
        "Sikh",
        "Jaïn",
        "Other",
        "No religion"
    ])
    jati = models.StringField(label="What is your Jati? (leave empty if you prefer not to "
                                    "answer)", blank=True)

    school = models.StringField(label="What type of school did you attend?", choices=[
        "private",
        "government school"
    ])

    caste = models.StringField(label="What is your caste group?", choices=[
        "SC",
        "ST",
        "OBC",
        "General Category"
    ])

    field_of_study = models.StringField(label="What is your field of study?")

    household_size = models.IntegerField(min=0, label="How many people live in your households?")

    years_of_education = models.IntegerField(min=0, label="How many years of education have you "
                                                          "completed?")

    occupation_father = models.IntegerField(label="What is your father's occupation?",
                                            choices=OCCUPATION_CHOICES,
                                            widget=widgets.RadioSelect)
    occupation_father_other = models.StringField(label="If you selected 'Others', please specify "
                                                       "your father's occupation", blank=True)

    occupation_mother = models.IntegerField(label="What is your mother's occupation?",
                                            choices=OCCUPATION_CHOICES,
                                            widget=widgets.RadioSelect)
    occupation_mother_other = models.StringField(label="If you selected 'Others', please specify "
                                                       "your mother's occupation", blank=True)

    fathers_education = models.StringField(label="What is your father’s education?", choices=[
        "NO SCHOOLING",
        "PRE-PRIMARY",
        "PRIMARY",
        "SECONDARY",
        "HIGHER"
    ])

    mothers_education = models.StringField(label="What is your mother’s education?", choices=[
        "NO SCHOOLING",
        "PRE-PRIMARY",
        "PRIMARY",
        "SECONDARY",
        "HIGHER"
    ])

    income_less_than_100_000 = models.BooleanField(label="Is your family income less than "
                                                         "INR 100,000 per year?")

    state_of_residence = models.StringField(label="What is your State of residence?",
                                            choices=[
                                                "I do not live in India",
                                                "Andaman and Nicobar Islands (UT)",
                                                "Andhra Pradesh",
                                                "Arunāchal Pradesh",
                                                "Assam",
                                                "Bihār",
                                                "Chandigarh (UT)",
                                                "Chhattīsgarh",
                                                "Dādra and Nagar Haveli (UT)",
                                                "Daman and Diu (UT)",
                                                "Delhi",
                                                "Goa",
                                                "Gujarāt",
                                                "Haryāna",
                                                "Himāchal Pradesh",
                                                "Jammu and Kashmīr (UT)",
                                                "Jhārkhand",
                                                "Karnātaka",
                                                "Kerala",
                                                "Ladākh (UT)",
                                                "Lakshadweep (UT)",
                                                "Madhya Pradesh",
                                                "Mahārāshtra",
                                                "Manipur",
                                                "Meghālaya",
                                                "Mizoram",
                                                "Nāgāland",
                                                "Orissa",
                                                "Puducherry (UT)",
                                                "Punjab",
                                                "Rājasthān",
                                                "Sikkim",
                                                "Tamil Nādu",
                                                "Telangāna",
                                                "Tripura",
                                                "Uttar Pradesh",
                                                "Uttarākhand",
                                                "West Bengal",
                                            ])

    living_area = models.StringField(label="Do you live in an urban or rural area?", choices=[
        "Metro urban",
        "Other urban",
        "Rural"
    ])

    crt_1 = models.IntegerField(label="1. If it takes 2 nurses 2 minutes to check 2 patients, how "
                                      "many minutes does it take 40 nurses to check 40 patients?")
    crt_2 = models.IntegerField(label="2. On a loaf of bread, there is a patch of mold. Every day, "
                                      "the patch doubles in size. If it takes 24 days for the "
                                      "patch to cover the entire loaf of bread, how many days "
                                      "would it take for the patch to cover half of the loaf of "
                                      "bread?")
    crt_3 = models.IntegerField(label="3. If Anita can drink ten litres of water in 6 days, and "
                                      "Archana can drink ten litres of water in 12 days, how many "
                                      "days would it take for the two of them together to have "
                                      "drunk a total of ten litres of water?")
    crt_4 = models.IntegerField(label="4. Avinash received both the 15th highest and the 15th "
                                      "lowest mark in the class. How many students are in the "
                                      "class?")
    crt_5 = models.IntegerField(label="5. A tortoise starts crawling up a 6-yard-high rock wall "
                                      "in the morning. During each day it crawls 3 yards and "
                                      "during the night it slips back 2 yards. How many days will "
                                      "it take the tortoise to reach the top of the wall?")
    # For ComprehensionCheck:
    # percentage_correct = models.IntegerField(initial=random.randint(0, 100))
    comprehension_check_answer_grade = models.StringField(label="", choices=[
        "A", "B", "C", "D"
    ])
    received_bonus_crt = models.FloatField(blank=True, initial=0)
    received_bonus_score_guessing_1 = models.FloatField(blank=True, initial=0)
    received_bonus_score_guessing_2 = models.FloatField(blank=True, initial=0)
    received_bonus_score_guessing_3 = models.FloatField(blank=True, initial=0)
    payoff_relevant_bonus_score_guessing = models.FloatField(blank=True, initial=0)

    for i in range(1, 3+1):
        for j in range(1, len(Constants.participant_data[0])+1):
            exec(f"task_{i}_guessed_score_ID{j} = "
                 "models.IntegerField(label='', min=0, max=100)")
    del j  # Necessary to avoid otree complaining that this variable is not stored in the db
    del i  # Same reason as with j

    for j in range(1, len(Constants.participant_data[0])+1):
        exec(f"allocation_ID{j} = "
                "models.IntegerField(label='', min=0, max=200)")
    del j  # Necessary to avoid otree complaining that this variable is not stored in the db




class Consent(Page):
    form_model = "player"
    form_fields = ["consent_given"]

    @staticmethod
    def vars_for_template(player):
        return dict(
            show_up=player.session.config['show_up_fee'],
            max_additional_amount=player.session.config['possible_bonus_for_each_crt_item'] * 5 +
                                  1*player.session.config['possible_bonus_for_each_score_report'] *
                                  len(Constants.participant_data[0]),
            min_payoff=player.session.config['show_up_fee'],
            max_payoff=player.session.config['show_up_fee'] +
                       player.session.config['possible_bonus_for_each_crt_item'] * 5 +
                       1*player.session.config['possible_bonus_for_each_score_report'] *
                       len(Constants.participant_data[0])
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        i = 0
        index_1 = next(player.session.csv_index_iterator)
        if index_1+2 < len(Constants.participant_data):
            index_2 = index_1+1
            index_3 = index_1+2
        elif index_1+1 < len(Constants.participant_data):
            index_2 = index_1+1
            index_3 = 0
        else:
            index_2 = 0
            index_3 = 1

        player.csv_data_index_task_1 = index_1
        player.csv_name_task_1 = Constants.csv_names[index_1]
        player.csv_data_index_task_2 = index_2
        player.csv_name_task_2 = Constants.csv_names[index_2]
        player.csv_data_index_task_3 = index_3
        player.csv_name_task_3 = Constants.csv_names[index_3]

        if player.session.config["score_guessing_payoff_mode"] == 3:
            player.payoff_relevant_score_guessing_tasks = "I, II, III"

        treatment = next(player.session.treatment_iterator)
        while i < len(TREATMENTS):
            i += 1
            if player.session.nr_participants_in_treatments[treatment] < \
                    math.ceil(player.session.num_participants / len(TREATMENTS)):
                player.treatment = treatment
                player.session.nr_participants_in_treatments[treatment] += 1
                return
            treatment = next(player.session.treatment_iterator)
        player.treatment = treatment        


class Start(Page):  # Necessary to allow externally assigning treatments in tests
    pass


class Demographics(Page):
    form_model = "player"
    form_fields = ["age", "biological_sex", "gender", "religion", "jati", "school", "caste",
                   "household_size", "years_of_education", "occupation_father",
                   "occupation_father_other", "occupation_mother", "occupation_mother_other",
                   "fathers_education", "mothers_education", "income_less_than_100_000",
                   "state_of_residence", "living_area", "field_of_study"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payoff += player.session.config['show_up_fee']
        print(f"INFO: player earned show_up_fee: '{player.session.config['show_up_fee']}'")
        print(f"INFO: payoff is now: '{player.payoff}'")


class Introduction(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            treatment=player.treatment,
            bonus=player.session.config['possible_bonus_for_each_score_report']
        )


# class ComprehensionCheck(Page):
#     form_model = "player"
#     form_fields = ["comprehension_check_answer_grade"]
#
#     @staticmethod
#     def vars_for_template(player):
#         return dict(
#             treatment=player.treatment,
#             bonus=player.session.config['possible_bonus_for_each_score_report'],
#             percentage=player.percentage_correct
#         )
#
#     @staticmethod
#     def error_message(player, values):
#         if values["comprehension_check_answer_grade"] != \
#                 get_grade_for_percentage_correct(player.percentage_correct):
#             return "Wrong grade selected"


class ScoreGuessing(Page): # task 1 page
    form_model = "player"
    form_fields = [f"task_1_guessed_score_ID{i}" for i in range(
        1, len(Constants.participant_data[0])+1
    )]

    @staticmethod
    def error_message(player: Player, values):
        scores = []
        grades = []
        for form_field in ScoreGuessing.form_fields:
            scores.append(values[form_field])
            # for participant in Constants.participant_data_for_treatment[
            #         player.treatment][player.csv_data_index_task_1]:
            for participant in Constants.participant_data[0]:
                if participant["Participant ID"].split("ID")[-1] == form_field.split("ID")[-1]:
                    grades.append(participant["Grade"])
        for i, value in enumerate(scores):
            if value < GRADE_RANGES[grades[i]][0] or value > GRADE_RANGES[grades[i]][1]:
                player.gave_impossible_score_not_matching_grade = True
                return "Please make sure that the scores you entered fit to the participants' " \
                       "grades. Click 'Show grade table' for more information."

    @staticmethod
    def vars_for_template(player):
        # copy() necessary to avoid otree unnecessarily complaining with 'MustCopyError'
        # participants = deepcopy(Constants.participant_data_for_treatment[
        #                             player.treatment][player.csv_data_index_task_1].copy())
        participants = deepcopy(Constants.participant_data[0].copy())
        # print(participants)
        for i in range(len(participants)):
            participants[i][
                "formfield_name"] = f"task_1_guessed_score_{participants[i]['Participant ID']}"
        print("Grades:", [x['Grade'] for x in participants])
        return dict(
            treatment=player.treatment,
            # keys=Constants.participant_data_for_treatment[player.treatment][
            #     player.csv_data_index_task_1][0].keys(),
            keys=Constants.participant_data[0][0].keys(),
            participant_data=participants
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        answer_solution_pairs = []
        # for participant in Constants.participant_data_for_treatment[player.treatment][
        #         player.csv_data_index_task_1]:
        for participant in Constants.participant_data[0]: 
            answer = eval(f"player.task_1_guessed_score_{participant['Participant ID']}")
            answer_solution_pairs.append((answer, int(participant["Score"])))

        for answer, solution in answer_solution_pairs:
            random_nr = random.randint(0, 625)
            prediction_error = answer - solution
            if prediction_error ** 2 < random_nr:
                if player.session.config["score_guessing_payoff_mode"] == 3:
                    player.payoff += player.session.config['possible_bonus_for_each_score_report']
                    player.payoff_relevant_bonus_score_guessing += player.session.config[
                        'possible_bonus_for_each_score_report']
                    print("INFO: player earned bonus for task 1: "
                          f"'{player.session.config['possible_bonus_for_each_score_report']}'")
                    print(f"INFO: payoff is now: '{player.payoff}'")
                player.received_bonus_score_guessing_1 += \
                    player.session.config['possible_bonus_for_each_score_report']


class ScoreGuessing2(Page):
    form_model = "player"
    form_fields = [f"task_2_guessed_score_ID{i}" for i in range(
        1, len(Constants.participant_data[1])+1
    )]

    @staticmethod
    def error_message(player: Player, values):
        scores = []
        grades = []
        for form_field in ScoreGuessing2.form_fields:
            scores.append(values[form_field])
            # for participant in Constants.participant_data_for_treatment[player.treatment][
            #         player.csv_data_index_task_2]:
            for participant in Constants.participant_data[1]:
                if participant["Participant ID"].split("ID")[-1] == form_field.split("ID")[-1]:
                    grades.append(participant["Grade"])
        for i, value in enumerate(scores):
            if value < GRADE_RANGES[grades[i]][0] or value > GRADE_RANGES[grades[i]][1]:
                player.gave_impossible_score_not_matching_grade = True
                return "Please make sure that the scores you entered fit to the participants' " \
                       "grades. Click 'Show grade table' for more information."

    @staticmethod
    def vars_for_template(player):
        # copy() necessary to avoid otree unnecessarily complaining with 'MustCopyError'
        # participants = deepcopy(Constants.participant_data_for_treatment[player.treatment][
        #                             player.csv_data_index_task_2].copy())
        # for i in range(len(participants)):
        #     participants[i][
        #         "formfield_name"] = f"task_2_guessed_score_{participants[i]['Participant ID']}"
        # return dict(
        #     treatment=player.treatment,
        #     keys=Constants.participant_data_for_treatment[player.treatment][
        #             player.csv_data_index_task_2][0].keys(),
        #     participant_data=participants
        # )
        participants = deepcopy(Constants.participant_data[1].copy())
        # print(participants)
        for i in range(len(participants)):
            participants[i][
                "formfield_name"] = f"task_2_guessed_score_{participants[i]['Participant ID']}"
        print("Grades:", [x['Grade'] for x in participants])
        return dict(
            treatment=player.treatment,
            keys=Constants.participant_data[1][0].keys(),
            participant_data=participants
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        answer_solution_pairs = []
        # for participant in Constants.participant_data_for_treatment[player.treatment][
        #         player.csv_data_index_task_2]:
        for participant in Constants.participant_data[1]:
            answer = eval(f"player.task_2_guessed_score_{participant['Participant ID']}")
            answer_solution_pairs.append((answer, int(participant["Score"])))

        for answer, solution in answer_solution_pairs:
            random_nr = random.randint(0, 625)
            prediction_error = answer - solution
            if prediction_error ** 2 < random_nr:
                if player.session.config["score_guessing_payoff_mode"] == 3:
                    player.payoff += player.session.config['possible_bonus_for_each_score_report']
                    player.payoff_relevant_bonus_score_guessing += player.session.config[
                        'possible_bonus_for_each_score_report']
                    print("INFO: player earned bonus for task 2: "
                          f"'{player.session.config['possible_bonus_for_each_score_report']}'")
                    print(f"INFO: payoff is now: '{player.payoff}'")
                player.received_bonus_score_guessing_2 += \
                    player.session.config['possible_bonus_for_each_score_report']


class ScoreGuessing3(Page):
    form_model = "player"
    form_fields = [f"task_3_guessed_score_ID{i}" for i in range(
        1, len(Constants.participant_data[2])+1
    )]

    @staticmethod
    def error_message(player: Player, values):
        scores = []
        grades = []
        for form_field in ScoreGuessing3.form_fields:
            scores.append(values[form_field])
            # for participant in Constants.participant_data_for_treatment[player.treatment][
            #         player.csv_data_index_task_3]:
            for participant in Constants.participant_data[2]:
                if participant["Participant ID"].split("ID")[-1] == form_field.split("ID")[-1]:
                    grades.append(participant["Grade"])
        for i, value in enumerate(scores):
            if value < GRADE_RANGES[grades[i]][0] or value > GRADE_RANGES[grades[i]][1]:
                player.gave_impossible_score_not_matching_grade = True
                return "Please make sure that the scores you entered fit to the participants' " \
                       "grades. Click 'Show grade table' for more information."

    @staticmethod
    def vars_for_template(player):
        # # copy() necessary to avoid otree unnecessarily complaining with 'MustCopyError'
        # participants = deepcopy(Constants.participant_data_for_treatment[player.treatment][
        #                             player.csv_data_index_task_3].copy())
        # for i in range(len(participants)):
        #     participants[i][
        #         "formfield_name"] = f"task_3_guessed_score_{participants[i]['Participant ID']}"
        # return dict(
        #     treatment=player.treatment,
        #     keys=Constants.participant_data_for_treatment[player.treatment][
        #             player.csv_data_index_task_3][0].keys(),
        #     participant_data=participants
        # )
        participants = deepcopy(Constants.participant_data[2].copy())
        for i in range(len(participants)):
            participants[i][
                "formfield_name"] = f"task_3_guessed_score_{participants[i]['Participant ID']}"
        print("Grades:", [x['Grade'] for x in participants])
        return dict(
            treatment=player.treatment,
            keys=Constants.participant_data[2][0].keys(),
            participant_data=participants
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        answer_solution_pairs = []
        # for participant in Constants.participant_data_for_treatment[player.treatment][
        #         player.csv_data_index_task_3]:
        for participant in Constants.participant_data[2]:
            answer = eval(f"player.task_3_guessed_score_{participant['Participant ID']}")
            answer_solution_pairs.append((answer, int(participant["Score"])))

        for answer, solution in answer_solution_pairs:
            random_nr = random.randint(0, 625)
            prediction_error = answer - solution
            if prediction_error ** 2 < random_nr:
                if player.session.config["score_guessing_payoff_mode"] == 3:
                    player.payoff += player.session.config['possible_bonus_for_each_score_report']
                    player.payoff_relevant_bonus_score_guessing += player.session.config['possible_bonus_for_each_score_report']
                    print("INFO: player earned bonus for task 3: "
                          f"'{player.session.config['possible_bonus_for_each_score_report']}'")
                    print(f"INFO: payoff is now: '{player.payoff}'")
                player.received_bonus_score_guessing_3 += \
                    player.session.config['possible_bonus_for_each_score_report']
        if player.session.config["score_guessing_payoff_mode"] != 3:
            task_indizes = [1, 2, 3]
            random.shuffle(task_indizes)
            for task_nr in task_indizes[:player.session.config["score_guessing_payoff_mode"]]:
                player.payoff += eval(f"player.received_bonus_score_guessing_{task_nr}")
                player.payoff_relevant_bonus_score_guessing += eval(
                    f"player.received_bonus_score_guessing_{task_nr}")
                print(f"INFO: player earned randomly selected bonus for task {task_nr}: "
                      f"'{eval(f'player.received_bonus_score_guessing_{task_nr}')}'")
                print(f"INFO: payoff is now: '{player.payoff}'")
                player.payoff_relevant_score_guessing_tasks += f"{LATIN_NR[task_nr]}, "
            player.payoff_relevant_score_guessing_tasks = \
                player.payoff_relevant_score_guessing_tasks.strip(", ")


class Allocation(Page):
    form_model = "player"
    form_fields = [f"allocation_ID{i}" for i in range(
        1, len(Constants.participant_data[2])+1
    )]

    @staticmethod
    def error_message(player: Player, values):
        scores = []
        grades = []
        sum = 0
        for form_field in Allocation.form_fields:
            sum += values[form_field]
        if sum != 200:
            return "The sum of all allocations must be 200."

    @staticmethod
    def vars_for_template(player):
        # # copy() necessary to avoid otree unnecessarily complaining with 'MustCopyError'
        # participants = deepcopy(Constants.participant_data_for_treatment[player.treatment][
        #                             player.csv_data_index_task_3].copy())
        # for i in range(len(participants)):
        #     participants[i][
        #         "formfield_name"] = f"task_3_guessed_score_{participants[i]['Participant ID']}"
        # return dict(
        #     treatment=player.treatment,
        #     keys=Constants.participant_data_for_treatment[player.treatment][
        #             player.csv_data_index_task_3][0].keys(),
        #     participant_data=participants
        # )
        participants = deepcopy(Constants.participant_data[2].copy())
        for i in range(len(participants)):
            participants[i][
                "formfield_name"] = f"allocation_{participants[i]['Participant ID']}"
        return dict(
            treatment=player.treatment,
            keys=Constants.participant_data[2][0].keys(),
            participant_data=participants
        )

class CRT(Page):
    form_model = "player"
    form_fields = [f"crt_{nr}" for nr in range(1, 5 + 1)]

    @staticmethod
    def vars_for_template(player):
        return dict(
            bonus=player.session.config['possible_bonus_for_each_crt_item']
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        answer_key_pairs = [(player.crt_1, "crt_1"), (player.crt_2, "crt_2"),
                            (player.crt_3, "crt_3"), (player.crt_4, "crt_4"),
                            (player.crt_4, "crt_4")]
        for answer, key in answer_key_pairs:
            if answer == CORRECT_CRT_SOLUTIONS[key]:
                player.payoff += player.session.config['possible_bonus_for_each_crt_item']
                print(f"INFO: player earned CRT bonus: "
                      f"'{player.session.config['possible_bonus_for_each_crt_item']}'")
                print(f"INFO: payoff is now: '{player.payoff}'")
                player.received_bonus_crt += \
                    player.session.config['possible_bonus_for_each_crt_item']


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            show_up_fee=player.session.config['show_up_fee'],
            bonus_crt=player.received_bonus_crt,
            sum=player.payoff,
            relevant_boni=player.payoff_relevant_score_guessing_tasks,
            relevant_boni_amount=player.payoff_relevant_bonus_score_guessing,
        )


page_sequence = [Consent,
                 Start,
                 Introduction,
                 Allocation,
                 # ComprehensionCheck,  # If reactivated, add questions for all treatment groups
                 ScoreGuessing,
                 ScoreGuessing2,
                 ScoreGuessing3,
                 CRT,
                 Demographics,
                 Results]
