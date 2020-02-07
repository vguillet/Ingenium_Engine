
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

from Ingenium_Engine.Agents.Agent_gen import gen_Agent

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################

# --> Seeding generators
random.seed(345)

# ----- Generating environment
env = gen_environment("Test 1")

env.gen_random_layout(number_POI=12, number_mines=8, number_markets=3)

# env.add_POI(gen_POI("Paris", "City", (1, 1), mine_count=0, market_count=1))
# env.add_POI(gen_POI("London", "City", (1, -1), mine_count=1, market_count=0))
# env.add_POI(gen_POI("Rome", "City", (-1, -1), mine_count=0, market_count=1))
# env.add_POI(gen_POI("Amsterdam", "City", (-1, 1), mine_count=1, market_count=0))

# env.add_all_POI_links()
# env.plot_environment_graph()

# ----- Creating trading agents
agents_traded = []

fake = Faker()
for i in range(1):
    agents_traded.append(gen_Agent(fake.name(), env.POI_dict[random.choice(list(env.POI_dict.keys()))].pos))

# ----- Creating timeline
column_names = []
# --> Create agent columns
for agent in agents_traded:
    column_names.append(agent.name + " Expect")
    column_names.append(agent.name + " Invent")
    agent.gen_activity_decision(env)

# --> Create market columns
for market in env.converters_dict.keys():
    column_names.append(market)

# --> Create timeline dataframe
timeline = pd.DataFrame(index=pd.date_range(start='1/1/2018', end='2/1/2018'), columns=column_names)

sys.exit()

# --> Initiating QRL


print("")
for index, row in timeline.iterrows():
    print("--------------------- New day")

    # --> Supply markets environment
    for market in env.converters_dict.keys():
        env.converters_dict[market].add_to_inventory("Resources", "Iron", 1)

    # --> Perform trade day
    agents = agents_traded
    agents_traded = []

    while len(agents) > 0:
        agent = random.choice(agents)
        env.converters_dict["Rosegold Market"].evaluate_transaction(index.strftime('%d/%m/%Y'), agent, "buy", "Resources", "Iron", 1)

        agents_traded.append(agent)
        agents.remove(agent)
        print("")

        row[agent.name + " Expect"] = agent.interests["Resources"]["Iron"]["Expectation"]
        row[agent.name + " invent"] = agent.inventory["Resources"]["Iron"]

    row["Rosegold M. Price"] = env.converters_dict["Rosegold Market"].interests["Resources"]["Iron"]["Expectation"]


print(timeline)

timeline.plot()

plt.show()








