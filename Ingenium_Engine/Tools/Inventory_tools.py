
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
        inventory_dict = {"Money": 100,
                          "Resources": {"Iron": 0,
                                        "Gold": 0
                                        }
                          }

        return inventory_dict

    @staticmethod
    def gen_market_inventory_dict(traded_item_types, bias=None):
        inventory_dict = {"Money": 100}

        for item_type in traded_item_types:
            inventory_dict[item_type] = {}

        return inventory_dict

    @staticmethod
    def clean_inventory(inventory_dict):
        for item_type in inventory_dict:
            if isinstance(inventory_dict[item_type], dict):
                for item in inventory_dict[item_type].keys():
                    if inventory_dict[item_type][item] == 0:
                        del inventory_dict[item_type][item]

        return inventory_dict
