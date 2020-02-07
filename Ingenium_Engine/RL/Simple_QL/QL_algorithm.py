
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

        # ----- Gen agents
        self.agents = []
        for _ in range(self.settings.agent_settings.nb_agents):
            agent_name = fake.name()
            agent_starting_position = self.starting_env.POI_dict[random.choice(list(self.starting_env.POI_dict.keys()))].pos
            self.agents.append(gen_Agent(agent_name, agent_starting_position))

        # ----- Gen initial Q-table
        # --> List number of position states
        nb
        
        self.q_table = np.random.uniform(size=())

        # ----- Initialise trackers
        self.progress_bar = Progress_bar(max_step=self.settings.rl_behavior_settings.episodes, label="Episode")

        # ======================== PROCESS ==============================================

        # ===============================================================================

        # ======================== RESULTS ==============================================


if __name__ == "__main__":
    sim = QL_optimiser()
