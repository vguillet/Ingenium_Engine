
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
import sys

# Libs
import matplotlib.pyplot as plt
import pandas as pd
from faker import Faker
import networkx as nx

# Own modules
from Ingenium_Engine.Environment.Environment_gen import gen_environment
from Ingenium_Engine.Environment.POI_gen import gen_POI

from Ingenium_Engine.Bots.Bot_gen import gen_Bot

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################

# --> Seeding generators

random.seed(345)

# ----- Generating environment
env = gen_environment("Test 1")

env.gen_random_layout(number_of_POI=12, number_of_mines=8, number_of_markets=3)

# env.add_POI(gen_POI("Paris", "City", (1, 1), mine_count=0, market_count=1))
# env.add_POI(gen_POI("London", "City", (1, -1), mine_count=1, market_count=0))
# env.add_POI(gen_POI("Rome", "City", (-1, -1), mine_count=0, market_count=1))
# env.add_POI(gen_POI("Amsterdam", "City", (-1, 1), mine_count=1, market_count=0))

# env.add_all_POI_links()

# env.plot_environment_graph()

# ----- Creating trading bots
bots_traded = []

fake = Faker()
for i in range(10):
    bots_traded.append(gen_Bot(fake.name(), env.POI_dict[random.choice(list(env.POI_dict.keys()))].pos))

# ----- Creating timeline
column_names = []
# --> Create bot columns
for bot in bots_traded:
    column_names.append(bot.name + " Expect")
    column_names.append(bot.name + " Invent")
    bot.gen_activity_decision(env)

# --> Create market columns
for market in env.converters_dict.keys():
    column_names.append(market)

# --> Create timeline dataframe
timeline = pd.DataFrame(index=pd.date_range(start='1/1/2018', end='2/1/2018'), columns=column_names)

sys.exit()

print("")
for index, row in timeline.iterrows():
    print("--------------------- New day")

    # --> Supply markets environment
    for market in env.converters_dict.keys():
        env.converters_dict[market].add_to_inventory("Resources", "Iron", 1)

    # --> Perform trade day
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








