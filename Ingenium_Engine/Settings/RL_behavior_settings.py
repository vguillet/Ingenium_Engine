
##################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '7/02/2020'

##################################################################################################################


class RL_behavior_settings:
    def gen_simple_ql_settings(self):
        # --> Print settings
        self.show_every = 2000

        # --> Learning settings
        self.nb_bucket = 10
        self.learning_rate = 0.1

        self.discount = 0.95
        self.episodes = 25000

        # --> Exploration settings
        self.epsilon = 1

        # --> Decay settings
        self.decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]

        return
