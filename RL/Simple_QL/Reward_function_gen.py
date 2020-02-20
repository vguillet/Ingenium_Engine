
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
import numpy as np

# Own modules
from Ingenium_Engine.Agents.Agent import Agent

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_reward_function:
    def __init__(self, reward_dict=None):
        if reward_dict is None:
            self.reward_dict = self.gen_reward_dict()
        else:
            self.reward_dict = reward_dict
        return

    def get_reward(self, action_type, success):
        return self.reward_dict[action_type][success]

    @staticmethod
    def gen_reward_dict():
        """
        1: success
        0: Neutral
        -1: Mistake
        """

        reward_dict = {"Move": {1: -1,
                                0: -1,
                                -1: -5},

                       "Mine": {1: 1,
                                0: -1,
                                -1: -5},

                       "buy": {1: 0,
                               0: -1,
                               -1: -10},

                       "sell": {1: -1,
                                0: -1,
                                -1: -10},

                       }
        return reward_dict