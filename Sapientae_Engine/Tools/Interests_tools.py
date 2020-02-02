
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Interests_tools:
    @staticmethod
    def gen_bot_interests_dict(bias=None):
        interests_dict = {"Resources": {"Iron": {"Expectation": 10,
                                                 "Minimum": 5,
                                                 "Maximum": 12},
                                        "Gold": {"Expectation": 50,
                                                 "Minimum": 45,
                                                 "Maximum": 60},
                                        "Diamond": {"Expectation": 200,
                                                    "Minimum": 185,
                                                    "Maximum": 210},
                                        }
                          }

        return interests_dict

    @staticmethod
    def gen_market_interests_dict(item_types):
        interests_dict = {"Resources": {"Iron": {"Expectation": 10,
                                                 "Minimum": 5,
                                                 "Maximum": 12},
                                        "Gold": {"Expectation": 50,
                                                 "Minimum": 45,
                                                 "Maximum": 60},
                                        "Diamond": {"Expectation": 200,
                                                    "Minimum": 185,
                                                    "Maximum": 210},
                                        }
                          }

        return interests_dict

    @staticmethod
    def increase_expectation(bot_expectation, bot_surplus,
                             ef_expectation, ef_surplus):
        # TODO: Dynamically adjusted percents
        increase_percent = 0.2
        new_bot_expectation = bot_expectation + increase_percent * bot_surplus
        new_ef_expectation = ef_expectation + increase_percent * ef_surplus

        return new_bot_expectation, new_ef_expectation

    @staticmethod
    def decrease_expectation(bot_expectation, bot_shortfall,
                             ef_expectation, ef_shortfall):
        # TODO: Dynamically adjusted percents
        decrease_percent = 0.3
        new_bot_expectation = bot_expectation - decrease_percent * bot_shortfall
        new_ef_expectation = ef_expectation - decrease_percent * ef_shortfall

        return new_bot_expectation, new_ef_expectation
