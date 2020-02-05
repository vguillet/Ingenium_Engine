
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
import networkx as nx
import matplotlib.pyplot as plt

# Own modules


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_POI:
    def __init__(self, name, label, pos: tuple, ef_dict=None):
        # --> Setup reference properties
        self.name = name
        self.label = label

        # --> Setup POI position
        self.pos = pos

        # --> Setup POI content
        if ef_dict is None:
            self.ef_dict = self.gen_ef_dict(pos, mine_count=0, market_count=1)

        else:
            self.ef_dict = ef_dict

    @property
    def POI_money(self):
        POI_money = 0
        for ef_type in self.ef_dict.keys():
            for ef in self.ef_dict[ef_type].keys():
                POI_money += self.ef_dict[ef_type][ef].inventory["Money"]
        return

    def add_to_ef_dict(self, ef):
        self.ef_dict[ef.ef_type][ef.name] = ef
        return

    @staticmethod
    def gen_ef_dict(pos: tuple, mine_count=0, market_count=0):
        from Ingenium_Engine.Environment.Sources.Mine_gen import Mine
        from Ingenium_Engine.Environment.Converters.Market_gen import gen_market

        ef_dict = {"Sources": {},
                   "Converters": {}}

        # fake = Faker()
        # Faker.seed(4321)

        for mine in range(mine_count):
            # name = fake.name().split(" ")[0] + " Mine"
            name = "Strongstone mine"
            ef_dict["Sources"][name] = Mine(name)

        for market in range(market_count):
            # name = fake.name().split(" ")[0] + " Market"
            name = "Rosegold Market"
            ef_dict["Converters"][name] = gen_market(name, pos, ["Resources"])

        return ef_dict