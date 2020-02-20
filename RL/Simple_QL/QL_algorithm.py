
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
import copy
import sys
import time

# Libs
from faker import Faker
import numpy as np
import matplotlib.pyplot as plt

# Own modules
from Settings.SETTINGS import SETTINGS
from Ingenium_Engine.Tools.Progress_bar_tool import Progress_bar
from RL.Simple_QL.QL_Agent_gen import gen_Agent
from Ingenium_Engine.Visualizer.Visualizer_gen import gen_visualizer

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class QL_optimiser:
    def __init__(self, environment: "Environment object", ):
        # ======================== INITIALISATION =======================================

        # ----- Setup reference properties
        self.starting_env = environment

        # ----- Initialise settings
        self.settings = SETTINGS()
        self.settings.rl_behavior_settings.gen_simple_ql_settings()
        self.settings.agent_settings.gen_agent_settings()
        self.settings.print_plot_settings.gen_rl_print_plot_settings()
        self.settings.cache_settings()

        # ----- Initialise tools
        fake = Faker()

        # --> Seeding generators
        # random.seed(345)
        Faker.seed(346)

        # ----- Gen agents and initial Q tables
        self.agents = {}
        for _ in range(self.settings.agent_settings.nb_agents):
            agent_name = fake.name()
            agent_starting_position = self.starting_env.POI_dict[random.choice(list(self.starting_env.POI_dict.keys()))].pos

            self.agents[agent_name] = gen_Agent(self.starting_env, agent_name, agent_starting_position)

        # ----- Initialise trackers
        progress_bar = Progress_bar(max_step=self.settings.rl_behavior_settings.episodes, label="Episode")

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
            else:
                render = False

            step = 0

            # ----- Run training until goal is achieved by each bot
            while len(agents_done) != len(self.agents):
                step += 1

                # --> Cycle between agents working
                for _ in range(len(agents_working)):
                    agent = random.choice(agents_working)

                    if agent not in agents_done:
                        # time.sleep(0.5)
                        if step == 1:
                            # --> Gen initial state
                            state = self.agents[agent].get_observations(environment)
                            discrete_state = self.get_discrete_state(state,
                                                                     self.agents[agent].os_low,
                                                                     self.agents[agent].discrete_os_win_size)

                        else:
                            action_lst, available_action_lst = self.agents[agent].get_action_lst(environment)

                            # --> Get best action
                            if np.random.randint(0, 100) > self.settings.rl_behavior_settings.epsilon:
                                action_value_lst = self.agents[agent].q_table[discrete_state].copy()
                                action = np.argmax(action_value_lst)

                                # --> Cycle through options until action picked is valid
                                while bool(available_action_lst[action]) is False:

                                    action_value_lst[action] = -100000
                                    action = np.argmax(action_value_lst)

                            # --> Get random action
                            else:
                                action = np.random.randint(0, self.agents[agent].nb_actions)

                                # --> Cycle through options until action picked is valid
                                while bool(available_action_lst[action]) is False:
                                    action = np.random.randint(0, self.agents[agent].nb_actions)

                            # --> Perform step
                            new_state, reward, done = self.agents[agent].step(step, environment, action)

                            # --> Discretise step
                            new_discrete_state = self.get_discrete_state(new_state,
                                                                         self.agents[agent].os_low,
                                                                         self.agents[agent].discrete_os_win_size)

                            if done:    # --> Stop agent if done
                                self.agents[agent].q_table[discrete_state + (action,)] = \
                                    self.agents[agent].reward_history[-1] / self.agents[agent].characteristics["Age"]

                                agents_done.append(agent)
                                agents_working.remove(agent)

                            else:       # --> Update agent Q-table

                                # --> Get maximum possible Q value in next step (for new state)
                                max_future_q = np.max(self.agents[agent].q_table[new_discrete_state])

                                # --> Get current Q value (for current state and performed action)
                                current_q = self.agents[agent].q_table[discrete_state + (action,)]

                                # --> Compute new Q value for current state and action
                                new_q = (1 - self.settings.rl_behavior_settings.learning_rate) * current_q \
                                        + self.settings.rl_behavior_settings.learning_rate * \
                                        (reward + self.settings.rl_behavior_settings.discount * max_future_q)

                                # Update Q table with new Q value
                                self.agents[agent].q_table[discrete_state + (action,)] = new_q

                            discrete_state = new_discrete_state

        # ======================== Render episode =======================================
            if episode % 100 == 0:
                progress_bar.update_progress(current=episode)

            if render and episode != 0:
                gen_visualizer("Episode " + str(episode), environment, self.agents)

                for agent in self.agents.keys():
                    plt.plot(self.agents[agent].reward_timeline[-self.settings.rl_behavior_settings.show_every:])
                    plt.show()

                    iron_quantity = []
                    gold_quantity = []
                    diamond_quantity = []
                    S_tool_quantity = []

                    for step in range(len(self.agents[agent].inventory_history)):
                        iron_quantity.append(self.agents[agent].inventory_history[step]["Resources"]["Iron"])
                        gold_quantity.append(self.agents[agent].inventory_history[step]["Resources"]["Gold"])
                        diamond_quantity.append(self.agents[agent].inventory_history[step]["Resources"]["Diamond"])
                        S_tool_quantity.append(self.agents[agent].inventory_history[step]["Items"]["S_Tool"])

                    plt.plot(self.agents[agent].cargo_history, label="Cargo")
                    # plt.plot(iron_quantity, label="Iron")
                    # plt.plot(gold_quantity, label="Gold")
                    # plt.plot(diamond_quantity, label="Diamond")
                    plt.plot(S_tool_quantity, label="S tool")

                    plt.legend()
                    plt.grid()
                    plt.show()

        # ======================== RESULTS ==============================================

    @staticmethod
    def get_discrete_state(state, os_low, discrete_os_win_size):
        discrete_state = (np.array(state) - np.array(os_low)) / discrete_os_win_size
        return tuple(discrete_state.astype(np.int))  # Tuple to look up the Q values for the available actions in the q-table
