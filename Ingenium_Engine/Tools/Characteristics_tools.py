
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


class Characteristics_tools:
    @staticmethod
    def gen_agent_characteristics_dict():
        characteristics_dict = {"Age": 0,
                                "Health": 0,
                                "Attack": 0,
                                "Armor": 0,
                                "Mining": 0,
                                }

        return characteristics_dict

    @staticmethod
    def gen_mine_characteristics_dict(inventory):
        characteristics_dict = {"Reputation": 100,
                                "Infrastructure": 100,
                                "RMD": {}}                      # Resource mining difficulty

        for resource in inventory["Resources"].keys():
            if resource == "Iron":
                characteristics_dict["RMD"][resource] = 85

            elif resource == "Gold":
                characteristics_dict["RMD"][resource] = 50

            elif resource == "Diamond":
                characteristics_dict["RMD"][resource] = 25

        return characteristics_dict

    @staticmethod
    def gen_market_characteristics_dict():
        characteristics_dict = {"Reputation": 100,
                                "Honesty": 100
                                }

        return characteristics_dict

