import math
from typing import Union

from otree.api import *
import itertools
import random

c = Currency

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
    jati = models.StringField(label="What is your Jati? (do not change if you prefer not to "
                                    "answer)", initial="prefer not to answer")

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
                                                "Andhra Pradesh",
                                                "Arunāchal Pradesh",
                                                "Assam",
                                                "Bihār",
                                                "Chhattīsgarh",
                                                "Goa",
                                                "Gujarāt",
                                                "Haryāna",
                                                "Himāchal Pradesh",
                                                "Jhārkhand",
                                                "Karnātaka",
                                                "Kerala",
                                                "Madhya Pradesh",
                                                "Mahārāshtra",
                                                "Manipur",
                                                "Meghālaya",
                                                "Mizoram",
                                                "Nāgāland",
                                                "Odisha",
                                                "Punjab",
                                                "Rājasthān",
                                                "Sikkim",
                                                "Tamil Nādu",
                                                "Telangāna",
                                                "Tripura",
                                                "Uttarākhand",
                                                "Uttar Pradesh",
                                                "West Bengal",
                                                "Andaman and Nicobar Islands",
                                                "Chandigarh",
                                                "Dādra and Nagar Haveli and Damān and Diu",
                                                "Delhi",
                                                "Jammu and Kashmīr",
                                                "Ladākh",
                                                "Lakshadweep",
                                                "Puducherry"
                                            ])

    living_area = models.StringField(label="Do you live in an urban or rural area?", choices=[
        "Metro urban",
        "Other urban",
        "Rural"
    ])
    percentage_correct = models.IntegerField(initial=random.randint(0, 100))
    comprehension_check_answer_grade = models.StringField(label="", choices=[
                                                              "A", "B", "C", "D"
                                                          ])


class Consent(Page):
    form_model = "player"
    form_fields = ["consent_given"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        treatment_assigned = False
        i = 0
        while not treatment_assigned and i < len(TREATMENTS):
            i += 1
            treatment = next(player.session.treatment_iterator)
            if player.session.nr_participants_in_treatments[treatment] < \
                    math.ceil(player.session.num_participants / len(TREATMENTS)):
                player.treatment = treatment
                treatment_assigned = True


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


class ComprehensionCheck(Page):
    form_model = "player"
    form_fields = ["comprehension_check_answer_grade"]

    @staticmethod
    def vars_for_template(player):
        return dict(
            treatment=player.treatment,
            bonus=player.session.config['possible_bonus_for_each_score_report'],
            percentage=player.percentage_correct
        )

    @staticmethod
    def error_message(player, values):
        if values["comprehension_check_answer_grade"] != \
                get_grade_for_percentage_correct(player.percentage_correct):
            return "Wrong grade selected"


class Results(Page):
    pass


page_sequence = [Consent,
                 # Demographics,
                 Introduction,
                 ComprehensionCheck,
                 Results]
