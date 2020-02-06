
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Ingenium_Engine.Environment.Sources.Source_gen import Source
from Ingenium_Engine.Tools.Inventory_tools import Inventory_tools
from Ingenium_Engine.Tools.Interests_tools import Interests_tools
from Ingenium_Engine.Tools.Characteristics_tools import Characteristics_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Mine(Source):
    def __init__(self, name: "Converter name",
                 pos: tuple,
                 inventory: dict = None,
                 characteristics: dict = None):
        # --> Initialising base class (building all ref properties)
        super().__init__(name, pos)
        self.name = name
        self.label = "Mine"
        self.ef_type = "Source"

        # --> Setup inventory/interests/characteristics dicts
        self.gen_dicts(inventory, characteristics)

        # --> Initialising records
        self.transaction_records = []

    def add_to_inventory(self, resource, resource_quantity):
        # --> Checking if item is already in inventory
        if resource in self.inventory["Resources"].keys():
            self.inventory["Resources"][resource] += resource_quantity
            return

        else:
            self.inventory["Resources"][resource] = resource_quantity
            return

    def remove_from_inventory(self, resource, resource_quantity):
        # --> Checking if resource is in inventory
        if resource in self.inventory["Resources"].keys():

            # --> Checking if resource quantity to be removed is in the inventory
            if self.inventory["Resources"][resource] >= resource_quantity:
                self.inventory["Resources"][resource] -= resource_quantity

            else:
                self.inventory["Resources"][resource] = 0
                return

        else:
            print("Resource not in inventory")
            return

    def gen_dicts(self,
                  inventory: dict,
                  characteristics: dict):
        # --> Setting up inventory
        if inventory is not None:
            self.inventory = inventory
        else:
            self.inventory = Inventory_tools().gen_mine_inventory_dict()

        # --> Setting up characteristics
        if characteristics is not None:
            self.characteristics = characteristics
        else:
            self.characteristics = Characteristics_tools().gen_mine_characteristics_dict(self.inventory)

    def __str__(self):
        return self.name + " (Mine-type source)"

    def __repr__(self):
        return self.__str__()
