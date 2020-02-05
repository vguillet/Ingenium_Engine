
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
        interests_dict = {"Resources": {"Iron": {"Expectation": 30,
                                                 "Minimum": 20,
                                                 "Maximum": 40},
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
        interests_dict = {"Resources": {"Iron": {"Expectation": 30,
                                                 "Minimum": 20,
                                                 "Maximum": 40},
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
    def increase_expectation(expectation, expectation_p_difference=None, increase_percent=0, setting=1):
        # TODO: Add expectation settings
        if setting == 1:
            return expectation + 1
        if setting == 2:
            return expectation + increase_percent * expectation_p_difference

    @staticmethod
    def decrease_expectation(expectation, expectation_ap_difference, decrease_percent=0, setting=1):
        if setting == 1:
            return expectation - 1
        if setting == 2:
            return expectation - decrease_percent * expectation_ap_difference

