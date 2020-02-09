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
    def __init__(self):
        self.ref_interests_dict = {"Resources": {"Iron": {"Expectation": 30,
                                                          "Minimum": 20,
                                                          "Maximum": 40},

                                                 "Gold": {"Expectation": 50,
                                                          "Minimum": 45,
                                                          "Maximum": 60},

                                                 "Diamond": {"Expectation": 200,
                                                             "Minimum": 185,
                                                             "Maximum": 210}},

                                   "Items": {"S Health": {"Expectation": 30,
                                                          "Minimum": 20,
                                                          "Maximum": 40},

                                             "M Health": {"Expectation": 50,
                                                          "Minimum": 45,
                                                          "Maximum": 60},

                                             "L Health": {"Expectation": 200,
                                                          "Minimum": 185,
                                                          "Maximum": 210},

                                             "S Weapon": {"Expectation": 30,
                                                          "Minimum": 20,
                                                          "Maximum": 40},

                                             "M Weapon": {"Expectation": 50,
                                                          "Minimum": 45,
                                                          "Maximum": 60},

                                             "L Weapon": {"Expectation": 200,
                                                          "Minimum": 185,
                                                          "Maximum": 210},

                                             "S Armor": {"Expectation": 30,
                                                         "Minimum": 20,
                                                         "Maximum": 40},

                                             "M Armor": {"Expectation": 50,
                                                         "Minimum": 45,
                                                         "Maximum": 60},

                                             "L Armor": {"Expectation": 200,
                                                         "Minimum": 185,
                                                         "Maximum": 210},

                                             "S Tool": {"Expectation": 30,
                                                        "Minimum": 20,
                                                        "Maximum": 40},

                                             "M Tool": {"Expectation": 50,
                                                        "Minimum": 45,
                                                        "Maximum": 60},

                                             "L Tool": {"Expectation": 200,
                                                        "Minimum": 185,
                                                        "Maximum": 210}
                                             }
                                   }

    def gen_agent_interests_dict(self):
        return self.ref_interests_dict

    def gen_market_interests_dict(self, traded_item_types):
        # TODO: Rethink market interest dict gen
        return self.ref_interests_dict

    @staticmethod
    def increase_expectation(expectation_dict, surplus=None, increase_percent=0, setting=1):
        # TODO: Add expectation settings
        # --> Fixed value expectation increase
        if setting == 1:
            if expectation_dict["Maximum"] > expectation_dict["Expectation"] + 1:
                expectation_dict["Expectation"] += 1
                return expectation_dict
            else:
                expectation_dict["Expectation"] = expectation_dict["Maximum"]
                return expectation_dict

        # --> Surplus percent based expectation increase
        if setting == 2:
            if expectation_dict["Maximum"] > expectation_dict["Expectation"] + increase_percent * surplus:
                expectation_dict["Expectation"] += increase_percent * surplus
                return expectation_dict
            else:
                expectation_dict["Expectation"] = expectation_dict["Maximum"]
                return expectation_dict

    @staticmethod
    def decrease_expectation(expectation_dict, expectation_difference, decrease_percent=0, setting=1):
        # --> Fixed value expectation decrease
        if setting == 1:
            if expectation_dict["Minimum"] > expectation_dict["Expectation"] - 1:
                expectation_dict["Expectation"] -= 1
                return expectation_dict
            else:
                expectation_dict["Expectation"] = expectation_dict["Minimum"]
                return expectation_dict

        # --> Expectation difference percent based expectation decrease
        if setting == 2:
            if expectation_dict["Minimum"] > expectation_dict["Expectation"] - decrease_percent * expectation_difference:
                expectation_dict["Expectation"] -= decrease_percent * expectation_difference
                return expectation_dict
            else:
                expectation_dict["Expectation"] = expectation_dict["Minimum"]
                return expectation_dict
