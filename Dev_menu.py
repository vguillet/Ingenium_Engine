
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Sapientae_Engine.Environment.Environment_gen import gen_environment
from Sapientae_Engine.Environment.POI_gen import gen_POI
from Sapientae_Engine.Environment.Tools.POI_tools import POI_tools

from Sapientae_Engine.Bots.Bot_v1 import Bot_v1

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################

training_range = 10

poi_tools = POI_tools()
poi_1 = gen_POI("Paris", "City", pos=(0, 0), ef_dict=poi_tools.gen_ef_dict(market_count=1))
poi_2 = gen_POI("Amsterdam", "City", pos=(1, 1), ef_dict=poi_tools.gen_ef_dict())
poi_3 = gen_POI("London", "City", pos=(-1, -1), ef_dict=poi_tools.gen_ef_dict())
poi_4 = gen_POI("Berlin", "City", pos=(-1, 1), ef_dict=poi_tools.gen_ef_dict())
poi_5 = gen_POI("Shefield", "City", pos=(1, -1), ef_dict=poi_tools.gen_ef_dict())

POI_lst = [poi_1, poi_2, poi_3, poi_4, poi_5]

env = gen_environment()
for poi in POI_lst:
    env.add_POI(poi)

env.add_POI_link(poi_1, poi_2)
env.add_POI_link(poi_1, poi_3)
env.add_POI_link(poi_1, poi_4)
env.add_POI_link(poi_1, poi_5)

env.plot_environment_graph()

env.POI_dict["Paris"].ef_dict["Converters"]["Jason Market"].supply_inventory("Resources", "Iron", 10)

print(env.POI_dict["Paris"].ef_dict["Converters"]["Jason Market"].inventory)

bob = Bot_v1(env.POI_dict["Amsterdam"].pos)


