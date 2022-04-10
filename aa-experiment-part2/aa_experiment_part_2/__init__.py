import math
from copy import deepcopy
from typing import Union

from otree.api import *
from .modules.csv_reader import csv_to_dicts
import itertools
import random

c = Currency
CSV_PATH = "_static/aa_experiment_part_2/raven_data.csv"

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
    participant_data = csv_to_dicts(CSV_PATH)


def creating_session(subsession):
    subsession.session.treatment_iterator = itertools.cycle(TREATMENTS)
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

    state_of_residence = models.StringField(label="What is your State of residence?",  # TODO: Change to State / Union territory?
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
                                      "days would it take for the two of  them together to have "
                                      "drunk a total of ten litres of water?")
    crt_4 = models.IntegerField(label="4. Avinash received both the 15th highest and the 15th "
                                      "lowest mark in the class. How many students are in the "
                                      "class?")
    crt_5 = models.IntegerField(label="5. A tortoise starts crawling up a 6-foot-high rock wall "
                                      "in the morning. During each day it crawls 3 yards and "
                                      "during the night it slips back 2 yards. How many days will "
                                      "it take the tortoise to reach the top of the wall?")

    percentage_correct = models.IntegerField(initial=random.randint(0, 100))
    comprehension_check_answer_grade = models.StringField(label="", choices=[
                                                              "A", "B", "C", "D"
                                                          ])

    for participant in Constants.participant_data:
        exec(f"guessed_score_{participant['Participant rank']} = "
             "models.IntegerField(label='', min=0, max=100)")
    del participant  # Necessary to avoid otree complaining that this variable is not stored in the db


class Consent(Page):
    form_model = "player"
    form_fields = ["consent_given"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        i = 0
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
                   "state_of_residence", "living_area"]


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


class ScoreGuessing(Page):
    form_model = "player"
    form_fields = [f"guessed_score_{participant['Participant rank']}" for participant in
                   Constants.participant_data]

    @staticmethod
    def vars_for_template(player):
        # copy() necessary to avoid otree unnecessarily complaining with 'MustCopyError'
        participants = deepcopy(Constants.participant_data.copy())
        for i in range(len(participants)):
            participants[i]["formfield_name"] = f"guessed_score_{participants[i]['Participant rank']}"
        return dict(
            treatment=player.treatment,
            keys=Constants.participant_data[0].keys(),
            participant_data=participants
        )


class CRT(Page):
    form_model = "player"
    form_fields = [f"crt_{nr}" for nr in range(1, 5+1)]


class Results(Page):
    pass


page_sequence = [Consent,
                 Start,
                 Introduction,
                 # ComprehensionCheck,  # If reactivated, add questions for all treatment groups
                 ScoreGuessing,
                 CRT,
                 Demographics,
                 Results]
