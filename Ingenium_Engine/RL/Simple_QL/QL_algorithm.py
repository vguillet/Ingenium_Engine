
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
        environment_size = 800
        self.starting_env = gen_environment("Ingenium_1",
                                            self.settings.environment_settings.nb_POI,
                                            self.settings.environment_settings.nb_markets,
                                            self.settings.environment_settings.nb_mines,
                                            self.settings.environment_settings.nb_link_per_POI,
                                            environment_size=(environment_size, environment_size))

        # self.starting_env.plot_environment_graph()

        # --> Supplying mines
        resources_list = ["Iron", "Gold", "Diamond"]
        for i, mine in enumerate(self.starting_env.sources_dict.keys()):
            self.starting_env.sources_dict[mine].add_to_inventory(resources_list[i], 100)

        # --> Supplying market
        for i, market in enumerate(self.starting_env.converters_dict.keys()):
            self.starting_env.converters_dict[market].add_to_inventory("Items", "S Health", 10, force_add=True)
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
        self.agents = {}
        for _ in range(self.settings.agent_settings.nb_agents):
            agent_name = fake.name()
            agent_starting_position = self.starting_env.POI_dict[random.choice(list(self.starting_env.POI_dict.keys()))].pos
            self.agents[agent_name] = gen_Agent(self.starting_env, agent_name, agent_starting_position)

        # ----- Gen initial Q-tables
        self.gen_q_tables(self.settings.rl_behavior_settings.bucket_sizes)

        # ----- Initialise trackers
        self.progress_bar = Progress_bar(max_step=self.settings.rl_behavior_settings.episodes, label="Episode")

        # ======================== PROCESS ==============================================

        # ===============================================================================

        # ======================== RESULTS ==============================================

    def gen_q_tables(self, nb_buckets=20):
        self.q_tables = {}
        for agent in self.agents.keys():
            nb_actions = len(self.agents[agent].get_action_lst(self.starting_env)[0])
            nb_states = len(self.agents[agent].get_observations(self.starting_env))

            # --> Get environment high/low for bucket computation
            os_high = self.starting_env.high
            os_low = self.starting_env.low

            # --> Add characteristics high/low
            # For tool:
            os_high.append(100)
            os_low.append(0)

            # --> Add Cargo high/low
            os_high.append(5)
            os_low.append(0)

            # --> Add inventory high/low
            for _ in self.agents[agent].inventory["Resources"].keys():
                os_high.append(5)
                os_low.append(0)

            # For money
            os_high.append(self.settings.agent_settings.max_money)
            os_low.append(0)

            # --> Compute discrete observations window size
            discrete_os_size = [nb_buckets] * nb_states
            discrete_os_win_size = (np.array(os_high) - np.array(os_low)) / discrete_os_size
            # --> Initiate Q table
            print(discrete_os_size + [nb_actions])
            self.q_tables[agent] = np.random.uniform(low=-2, high=0, size=(nb_states*nb_buckets,
                                                                           nb_states*nb_buckets,
                                                                           nb_actions))
            print(self.q_tables[agent].shape)
