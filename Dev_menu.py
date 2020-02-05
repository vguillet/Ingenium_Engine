
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random

# Libs
import matplotlib.pyplot as plt
import pandas as pd

# Own modules
from Ingenium_Engine.Environment.Environment_gen import gen_environment
from Ingenium_Engine.Environment.POI_gen import gen_POI
from Ingenium_Engine.Environment.Tools.POI_tools import POI_tools

from Ingenium_Engine.Bots.Bot_v1 import Bot_v1

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################

random.seed(345)

training_range = 10

# ----- Generating environment
poi_tools = POI_tools()
poi_1 = gen_POI("Paris", "City", pos=(0, 0), ef_dict=poi_tools.gen_ef_dict(pos=(0, 0), market_count=1))
poi_2 = gen_POI("Amsterdam", "City", pos=(1, 1), ef_dict=poi_tools.gen_ef_dict(pos=(1, 1)))
poi_3 = gen_POI("London", "City", pos=(-1, -1), ef_dict=poi_tools.gen_ef_dict(pos=(-1, -1)))
poi_4 = gen_POI("Berlin", "City", pos=(-1, 1), ef_dict=poi_tools.gen_ef_dict(pos=(-1, 1)))
poi_5 = gen_POI("Shefield", "City", pos=(1, -1), ef_dict=poi_tools.gen_ef_dict(pos=(1, -1)))

POI_lst = [poi_1, poi_2, poi_3, poi_4, poi_5]

env = gen_environment("Test 1")
for poi in POI_lst:
    env.add_POI(poi)

env.add_POI_link(poi_1, poi_2)
env.add_POI_link(poi_1, poi_3)
env.add_POI_link(poi_1, poi_4)
env.add_POI_link(poi_1, poi_5)

# env.plot_environment_graph()

# --> Creating trading bots
billy = Bot_v1("Billy", env.POI_dict["Amsterdam"].pos)
katy = Bot_v1("Katy", env.POI_dict["Amsterdam"].pos)

bots_traded = [billy, katy]
# bots_traded = [billy]


# ----- Creating timeline
timeline = pd.DataFrame(index=pd.date_range(start='1/1/2018', end='2/1/2018'), columns=["Katy Expect",
                                                                                        "Katy invent",
                                                                                        "Billy Expect",
                                                                                        "Billy invent",
                                                                                        "Rosegold M. Price"])

print("")
for index, row in timeline.iterrows():
    print("--------------------- New day")

    # --> Supply single market environment
    env.converters_dict["Rosegold Market"].inventory["Resources"]["Iron"] = 1
    bots = bots_traded
    bots_traded = []

    while len(bots) > 0:
        bot = random.choice(bots)
        env.converters_dict["Rosegold Market"].evaluate_transaction(index.strftime('%d/%m/%Y'), bot, "buy", "Resources", "Iron", 1)

        bots_traded.append(bot)
        bots.remove(bot)
        print("")

        row[bot.name + " Expect"] = bot.interests["Resources"]["Iron"]["Expectation"]
        row[bot.name + " invent"] = bot.inventory["Resources"]["Iron"]

    row["Rosegold M. Price"] = env.converters_dict["Rosegold Market"].interests["Resources"]["Iron"]["Expectation"]


print(timeline)

timeline.plot()

plt.show()








