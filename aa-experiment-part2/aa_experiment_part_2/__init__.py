from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'aa_experiment_part_2'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField(initial="control")
    age = models.IntegerField(min=16, max=150, label="What is your age?")
    biological_sex = models.IntegerField(label="What is your sex assigned at birth?", choices=[
        "male",
        "female"
    ])
    gender = models.IntegerField(label="What is your Gender?", choices=[
        "male",
        "female",
        "other"
    ])
    religion = models.IntegerField(label="What is your religion?", choices=[
        "Hindu",
        "Muslim",
        "Christian",
        "Sikh",
        "Jaïn",
        "Other",
        "No religion"
    ])

# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
