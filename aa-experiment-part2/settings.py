from os import environ

SESSION_CONFIGS = [
    dict(
        name='aa_experiment',
        app_sequence=['aa_experiment_part_2'],
        num_demo_participants=3,
        show_up_fee=100,
        possible_bonus_for_each_score_report=100,
        possible_bonus_for_each_crt_item=200,
        score_guessing_payoff_mode=1
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
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
REAL_WORLD_CURRENCY_CODE = 'INR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9521158370061'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
