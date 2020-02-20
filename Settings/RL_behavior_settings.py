
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
        # --> Run / Visualiser settings
        self.episodes = 100000
        self.show_every = 1000

        # --> Learning settings
        self.nb_bucket = 3

        self.learning_rate = 0.6        #     learn nothing 0 <-- x --> 1 only consider recent info
        self.discount = 0.75            # short-term reward 0 <-- x --> 1 long-term reward

        # --> Exploration settings
        self.epsilon = 5               # Probability (percent) of taking random action

        # --> Decay settings
        self.decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]

        return
