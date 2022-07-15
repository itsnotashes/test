from os import environ

SESSION_CONFIGS = [
    dict(
        name='aa_experiment',
        app_sequence=['aa_experiment_part_2'],
        num_demo_participants=3,
        show_up_fee=0.75,
        possible_bonus_for_each_score_report=0.44,
        possible_bonus_for_each_crt_item=0.13,
        score_guessing_payoff_mode=1
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="",

    # adjust MTurk settings here
    mturk_hit_settings=dict(
        keywords='bonus, study',
        title='Behavioral Experiment with Bonus Payments (~10 minutes)',
        description='description',
        frame_height=500,
        template='global/mturk_template.html',
        minutes_allotted_per_assignment=30,
        expiration_hours=24,
        grant_qualification_id='3D6XXPFXVQ1U8X2T9CULQUHLVDESXE',
        qualification_requirements=[
            {'QualificationTypeId': "00000000000000000071",
             'Comparator': "EqualTo",
             'LocaleValues': [{'Country': "IN"}]
             },
            {'QualificationTypeId': "000000000000000000L0",
             'Comparator': "GreaterThanOrEqualTo",
             'IntegerValues': [99]
             },
            {'QualificationTypeId': "00000000000000000040",
             'Comparator': "GreaterThanOrEqualTo",
             'IntegerValues': [5000]
             },
            {'QualificationTypeId': "3D6XXPFXVQ1U8X2T9CULQUHLVDESXE",
             'Comparator': "DoesNotExist",
             }

        ]
        # grant_qualification_id='YOUR_QUALIFICATION_ID_HERE', # to prevent retakes
    )
)

SESSION_FIELDS = [
    "treatment_iterator",  # Iterator for balancing the treatment groups
    "nr_participants_in_treatments",  # Dict containing numbers of participants per treatment group
    "csv_index_iterator"  # Iterator for using alternating CSV files for different players
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'alphabet'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'e86hkSNX/SuWFoEUhCqA4mya+obZIzWToorQczBw'

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
