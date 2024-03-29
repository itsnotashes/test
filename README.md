# AA-experiment
oTree app consisting of the following parts:
* Data including the results of participants in a 
[raven test](https://en.wikipedia.org/w/index.php?title=Raven%27s_Progressive_Matrices&oldid=1066390473) and other 
information about the participants (stored under [aa-experiment-part2/_static/aa_experiment_part_2/raven_data.csv](aa-experiment-part2/_static/aa_experiment_part_2/raven_data.csv)) are loaded with the [CSV reader](aa-experiment-part2/aa_experiment_part_2/modules/csv_reader.py)
* Participants in this experiment are supposed to estimate the score of the raven test takers based on the given data
about them and an introduction depending on the treatment
* They answer demographic questions and take part in a CRTest as well

## Important notes
* As participants are sorted randomly within grade per session, the complete participant data in the order presented to
the study participants is stored in a file `sorted_participant_data.json`.
* To set the payoff mode for the ScoreGuessing boni, change the value of `score_guessing_payoff_mode` in the session
  config:
  * 1: One task is randomly determined to be payoff-relevant
  * 2: Two tasks are randomly determined to be payoff-relevant
  * 3: All tasks are payoff-relevant