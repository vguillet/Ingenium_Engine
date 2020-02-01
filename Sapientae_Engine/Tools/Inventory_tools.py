
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


class Inventory_tools:
    @staticmethod
    def gen_bot_inventory_dict(bias=None):
        inventory_dict = {"Money": 0,
                          "Resources": {"Iron": 10,
                                        "Gold": 10
                                        }
                          }

        return inventory_dict

    @staticmethod
    def gen_market_inventory_dict(bias=None):
        inventory_dict = {"Money": 0,
                          "Resources": {"Iron": 10,
                                        "Gold": 10
                                        }
                          }

        return inventory_dict

    @staticmethod
    def clean_inventory(inventory_dict):
        for items in inventory_dict:
            if isinstance(inventory_dict[items], dict):
                for resource in inventory_dict[items].keys():
                    if inventory_dict[items][resource]["Quantity available"] == 0:
                        del inventory_dict[items][resource]

        return inventory_dict
