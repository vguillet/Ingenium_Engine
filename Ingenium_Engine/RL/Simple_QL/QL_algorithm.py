
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
import time
import copy

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
                                            environment_size=(environment_size, environment_size))

        self.starting_env.plot_environment_graph()

        # --> Supplying mines
        resources_list = ["Iron", "Gold", "Diamond"]
        for i, mine in enumerate(self.starting_env.sources_dict.keys()):
            self.starting_env.sources_dict[mine].add_to_inventory(resources_list[i], 100)

        # --> Supplying market
        for i, market in enumerate(self.starting_env.converters_dict.keys()):
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "S Health", 10, force_add=True)
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "M Health", 5, force_add=True)
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "L Health", 3, force_add=True)
            #
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "S Weapon", 10, force_add=True)
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "M Weapon", 5, force_add=True)
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "L Weapon", 3, force_add=True)
            #
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "S Armor", 10, force_add=True)
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "M Armor", 5, force_add=True)
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "L Armor", 3, force_add=True)

            self.starting_env.converters_dict[market].add_to_inventory("Items", "S Tool", 10, force_add=True)
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "M Tool", 5, force_add=True)
            # self.starting_env.converters_dict[market].add_to_inventory("Items", "L Tool", 3, force_add=True)

        # ----- Gen agents and initial Q-tables
        self.agents = {}
        for _ in range(self.settings.agent_settings.nb_agents):
            agent_name = fake.name()
            agent_starting_position = self.starting_env.POI_dict[random.choice(list(self.starting_env.POI_dict.keys()))].pos

            self.agents[agent_name] = gen_Agent(self.starting_env, agent_name, agent_starting_position)

        # ----- Initialise trackers
        self.progress_bar = Progress_bar(max_step=self.settings.rl_behavior_settings.episodes, label="Episode")

        # ======================== PROCESS ==============================================
        for episode in range(self.settings.rl_behavior_settings.episodes):
            # --> Setup episode variables
            agents_working = []
            agents_done = []

            environment = copy.deepcopy(self.starting_env)

            # --> Reset agents and add to working agent list
            for agent in self.agents.keys():
                agents_working.append(agent)
                self.agents[agent].reset_agent()

            # --> Render if episode matches show every
            if episode % self.settings.rl_behavior_settings.show_every == 0:
                render = True
                print("Episode", episode)
            else:
                render = False

            # --> Run training until goal is achieved by each bot
            while len(agents_done) != len(self.agents):

                # --> Cycle between agents working
                for _ in range(len(agents_working)):
                    agent = random.choice(agents_working)

                    if agent not in agents_done:
                        if episode == 1:
                            # --> Gen initial state
                            state = self.agents[agent].get_observations(environment)
                            discrete_state = self.get_discrete_state(state,
                                                                     self.agents[agent].os_low,
                                                                     self.agents[agent].discrete_os_win_size)

                        else:
                            # --> Get action from Q table
                            if np.random.random() > self.settings.rl_behavior_settings.epsilon:
                                action = np.argmax(self.agents[agent].q_table[discrete_state])

                            # --> Get random action
                            else:
                                action = np.random.randint(0, self.agents[agent].nb_actions)

                            new_state, reward, done, _ = self.agents[agent].step(environment, action)

                            new_discrete_state = self.get_discrete_state(new_state,
                                                                         self.agents[agent].os_low,
                                                                         self.agents[agent].discrete_os_win_size)

                            # TODO: Add render

                            if done:    # --> Stop agent if done
                                self.agents[agent].q_table[discrete_state + (action,)] = self.agents[agent].profit

                                agents_done.append(agent)
                                agents_working.remove(agent)

                            else:       # --> Update agent Q-table

                                # Maximum possible Q value in next step (for new state)
                                max_future_q = np.max(self.agents[agent].q_table[new_discrete_state])

                                # Current Q value (for current state and performed action)
                                current_q = self.agents[agent].q_table[discrete_state + (action,)]

                                # And here's our equation for a new Q value for current state and action
                                new_q = (1 - self.settings.rl_behavior_settings.learning_rate) * current_q \
                                        + self.settings.rl_behavior_settings.learning_rate * \
                                        (reward + self.settings.rl_behavior_settings.discount * max_future_q)

                                # Update Q table with new Q value
                                self.agents[agent].q_table[discrete_state + (action,)] = new_q

                            discrete_state = new_discrete_state

        # ===============================================================================

        # ======================== RESULTS ==============================================

    # def gen_q_tables(self, nb_buckets=20):
    #     self.q_tables = {}
    #     for agent in self.agents.keys():
    #         nb_actions = len(self.agents[agent].get_action_lst(self.starting_env)[0])
    #         nb_states = len(self.agents[agent].get_observations(self.starting_env))
    #
    #         # --> Get environment high/low for bucket computation
    #         # self.os_high = self.starting_env.high
    #         # self.os_low = self.starting_env.low
    #         self.os_high = [800, 800]
    #         self.os_low = [0, 0]
    #
    #         # --> Add characteristics high/low
    #         # For tool:
    #         self.os_high.append(100)
    #         self.os_low.append(0)
    #
    #         # --> Add Cargo high/low
    #         self.os_high.append(5)
    #         self.os_low.append(0)
    #
    #         # --> Add inventory high/low
    #         for _ in self.agents[agent].inventory["Resources"].keys():
    #             self.os_high.append(5)
    #             self.os_low.append(0)
    #
    #         # For money
    #         self.os_high.append(self.settings.agent_settings.max_money)
    #         self.os_low.append(0)
    #
    #         # --> Compute discrete observations window size
    #         discrete_os_size = [nb_buckets] * nb_states
    #         self.discrete_os_win_size = (np.array(self.os_high) - np.array(self.os_low)) / discrete_os_size
    #
    #         # --> Initiate Q table
    #         total = 1
    #         for x in discrete_os_size + [nb_actions]:
    #             total = total * x
    #         print(total)
    #         self.q_tables[agent] = np.random.uniform(low=-2, high=0, size=(discrete_os_size + [nb_actions]))
    #         print(self.q_tables[agent].shape)

    @staticmethod
    def get_discrete_state(state, os_low, discrete_os_win_size):
        discrete_state = (np.array(state) - np.array(os_low)) / discrete_os_win_size
        return tuple(discrete_state.astype(np.int))  # Tuple to look up the Q values for the available actions in the q-table
