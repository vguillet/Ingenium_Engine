
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random

# Libs

# Own modules
from Ingenium_Engine.Environment.Sources.Source_gen import Source
from Ingenium_Engine.Tools.Inventory_tools import Inventory_tools
from Ingenium_Engine.Tools.Characteristics_tools import Characteristics_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_mine(Source):
    def __init__(self, name: "Converter name",
                 pos: tuple,
                 inventory: dict = None,
                 characteristics: dict = None):
        # --> Initialising base class (building all ref properties)
        super().__init__(name, pos)
        self.label = "Mine"

        # --> Setup inventory/interests/characteristics dicts
        self.gen_dicts(inventory, characteristics)

        # --> Initialising records
        self.transaction_records = []

    def mine(self, agent, resource):
        mined_quantity = 5

        # --> Checking if mine is not empty
        if self.inventory["Resources"][resource] > 0:

            # --> Checking if agent tool is sufficient to mine resource
            if agent.characteristics["Tool"] >= self.characteristics["RMD"][resource]:

                # --> Adjusting mined quantity if not available
                if self.inventory["Resources"][resource] < mined_quantity:
                    mined_quantity = self.inventory["Resources"][resource]

                # --> Remove resource from mine inventory
                self.inventory["Resources"][resource] -= mined_quantity

                print("Mined " + str(mined_quantity) + " " + resource + " successfully")

                # --> Adjust gathered quantity to available cargo space
                gathered_quantity = Inventory_tools().get_gathered_quantity(agent, mined_quantity)

                # --> Add resource to agent inventory
                if resource in list(agent.inventory["Resources"].keys()):
                    agent.inventory["Resources"][resource] += gathered_quantity
                    return

                else:
                    agent.inventory["Resources"][resource] = gathered_quantity
                    return

            else:
                print("Tool level " + str(agent.characteristics["Tool"]) + " insufficent to mine " + str(resource) + " (req: " +
                      str(self.characteristics["RMD"][resource]) + ")")
                return

        else:
            print("Mine is empty")
            return

    def add_to_inventory(self, resource, resource_quantity):
        # --> Checking if item is already in inventory
        if resource in self.inventory["Resources"].keys():
            self.inventory["Resources"][resource] += resource_quantity

        else:
            self.inventory["Resources"][resource] = resource_quantity

        self.characteristics = Characteristics_tools().gen_mine_characteristics_dict(self.inventory)

    def remove_from_inventory(self, resource, resource_quantity):
        # --> Checking if resource is in inventory
        if resource in self.inventory["Resources"].keys():

            # --> Checking if resource quantity to be removed is in the inventory
            if self.inventory["Resources"][resource] >= resource_quantity:
                self.inventory["Resources"][resource] -= resource_quantity

            else:
                self.inventory["Resources"][resource] = 0

            self.characteristics = Characteristics_tools().gen_mine_characteristics_dict(self.inventory)

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
