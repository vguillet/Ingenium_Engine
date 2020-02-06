
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Ingenium_Engine.Environment.Sources.Source_gen import Source
from Ingenium_Engine.Tools.Inventory_tools import Inventory_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Mine(Source):
    def __init__(self, name: "Converter name", pos: tuple, mined_resources):
        # --> Initialising base class (building all ref properties)
        super().__init__(name, pos)
        self.name = name
        self.label = "Mine"
        self.ef_type = "Source"

        # --> Setup mine inventory
        self.inventory = Inventory_tools().gen_mine_inventory_dict(mined_resources)

        # --> Setup market interests
        self.gen_mine_characteristics()

        # --> Initialising records
        self.transaction_records = []

    def gen_mine_characteristics(self):
        return