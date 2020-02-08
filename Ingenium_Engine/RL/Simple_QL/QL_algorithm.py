
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
import time

# Libs
from faker import Faker
import numpy as np

# Own modules
from Ingenium_Engine.Settings.SETTINGS import SETTINGS
from Ingenium_Engine.Tools.Progress_bar_tool import Progress_bar
from Ingenium_Engine.Environment.Environment_gen import gen_environment
from Ingenium_Engine.Agents.Agent_gen import gen_Agent

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class QL_optimiser:
    def __init__(self):
        # ======================== INITIALISATION =======================================

        # ----- Initialise settings
        self.settings = SETTINGS()
        self.settings.rl_behavior_settings.gen_simple_ql_settings()
        self.settings.environment_settings.gen_environment_settings()
        self.settings.agent_settings.gen_agent_settings()

        # ----- Initialise tools
        fake = Faker()

        # --> Seeding generators
        random.seed(345)
        Faker.seed(345)

        # ----- Gen initial training environment
        self.starting_env = gen_environment("Ingenium_1",
                                            self.settings.environment_settings.nb_POI,
                                            self.settings.environment_settings.nb_markets,
                                            self.settings.environment_settings.nb_mines,
                                            self.settings.environment_settings.nb_link_per_POI,
                                            POI_dict=None)

        self.starting_env.plot_environment_graph()

        # --> Supplying mines
        resources_list = ["Iron", "Gold", "Diamond"]
        for i, mine in enumerate(self.starting_env.sources_dict.keys()):
            self.starting_env.sources_dict[mine].add_to_inventory(resources_list[i], 100)

        # --> Supplying market
        for i, market in enumerate(self.starting_env.converters_dict.keys()):
            self.starting_env.converters_dict[market].add_to_inventory("Items", "S Health", 10, force_add=True)
            print(self.starting_env.converters_dict[market].interests)

            self.starting_env.converters_dict[market].add_to_inventory("Items", "M Health", 5, force_add=True)
            self.starting_env.converters_dict[market].add_to_inventory("Items", "L Health", 3, force_add=True)

            self.starting_env.converters_dict[market].add_to_inventory("Items", "S Weapon", 10, force_add=True)
            self.starting_env.converters_dict[market].add_to_inventory("Items", "M Weapon", 5, force_add=True)
            self.starting_env.converters_dict[market].add_to_inventory("Items", "L Weapon", 3, force_add=True)

            self.starting_env.converters_dict[market].add_to_inventory("Items", "S Armor", 10, force_add=True)
            self.starting_env.converters_dict[market].add_to_inventory("Items", "M Armor", 5, force_add=True)
            self.starting_env.converters_dict[market].add_to_inventory("Items", "L Armor", 3, force_add=True)

            self.starting_env.converters_dict[market].add_to_inventory("Items", "S Tool", 10, force_add=True)
            self.starting_env.converters_dict[market].add_to_inventory("Items", "M Tool", 5, force_add=True)
            self.starting_env.converters_dict[market].add_to_inventory("Items", "L Tool", 3, force_add=True)

        # ----- Gen agents
        self.agents = []
        for _ in range(self.settings.agent_settings.nb_agents):
            agent_name = fake.name()
            agent_starting_position = self.starting_env.POI_dict[random.choice(list(self.starting_env.POI_dict.keys()))].pos
            self.agents.append(gen_Agent(agent_name, agent_starting_position))

        for i, market in enumerate(self.starting_env.converters_dict.keys()):
            self.starting_env.converters_dict[market].evaluate_transaction("",
                                                                           self.agents[-1],
                                                                           "buy",
                                                                           "Items",
                                                                           "L Health",
                                                                           1)


        # ----- Gen initial Q-table
        # --> List number of position states
        nb_position_states = self.settings.environment_settings.nb_POI
        
        self.q_table = np.random.uniform(size=())

        # ----- Initialise trackers
        self.progress_bar = Progress_bar(max_step=self.settings.rl_behavior_settings.episodes, label="Episode")

        # ======================== PROCESS ==============================================

        # ===============================================================================

        # ======================== RESULTS ==============================================


if __name__ == "__main__":
    sim = QL_optimiser()
