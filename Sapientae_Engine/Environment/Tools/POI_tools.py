
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
from faker import Faker

# Own modules
from Sapientae_Engine.Environment.Sources.Mine_gen import Mine
from Sapientae_Engine.Environment.Converters.Market_gen import gen_market

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class POI_tools:
    @staticmethod
    def gen_ef_dict(mine_count=0, market_count=0):

        ef_dict = {"Sources": {},
                   "Converters": {}}

        fake = Faker()
        Faker.seed(4321)

        for mine in range(mine_count):
            name = fake.name().split(" ")[0] + " Mine"
            ef_dict["Sources"][name] = Mine(name)

        for market in range(market_count):
            name = fake.name().split(" ")[0] + " Market"
            ef_dict["Converters"][name] = gen_market(name, ["Resources"])

        return ef_dict