
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
import numpy as np

# Own modules
from Ingenium_Engine.Agents.Agent import Agent

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_Agent(Agent):
    def __init__(self,
                 environment: "Environment object",
                 name: "Bot name",
                 pos: tuple,
                 traits: dict = None,
                 inventory: dict = None,
                 interests: dict = None,
                 characteristics: dict = None):
        super().__init__(name, pos, traits, inventory, interests, characteristics)

        # --> Setup rl settings
        self.settings.rl_behavior_settings.gen_simple_ql_settings()

        # --> Setup Q-table
        self.gen_q_table(environment, self.settings.rl_behavior_settings.nb_bucket)

    def step(self, date, environment: "Environment Object", action: int):
        """
        Possible actions:   - 1 : Move
                            - 2 : Mine
                            - 3 : Sell
                            - 4 : Buy

        :param date: Date of step
        :param environment: Environment object
        :param action: Action reference integer
        :return: new_state, reward, done
        """
        prev_money = self.inventory["Money"]

        # --> Convert action int to matching action str
        action = self.action_lst[action]

        # --> Perform action
        if action.split()[0] == "Move":
            # --> Get target POI
            poi = action.split()[-1]

            # --> Get target POI position
            poi_pos = environment.POI_dict[poi].pos
            if poi_pos == self.pos:
                pass

            else:
                # --> Compute movement
                poi_vector = (self.pos[0] - poi_pos[0], self.pos[1] - poi_pos[1])
                poi_vector_mag = ((poi_vector[0]) ** 2 + (poi_vector[1]) ** 2) ** (1 / 2)
                normalised_poi_vector = (poi_vector[0]/poi_vector_mag, poi_vector[1]/poi_vector_mag)

                movement = (normalised_poi_vector[0]*self.velocity, normalised_poi_vector[1]*self.velocity)
                movement_mag = ((movement[0]) ** 2 + (movement[1]) ** 2) ** (1 / 2)

                # --> Adjust movement if overshooting goal
                if poi_vector_mag < movement_mag:
                    movement = poi_vector
                else:
                    pass

                new_x = self.pos[0] - int(movement[0])
                new_y = self.pos[1] - int(movement[1])

                if new_x < 0:
                    new_x = 0
                elif new_x >= 800:
                    new_x = 800

                if new_y < 0:
                    new_y = 0
                elif new_y >= 800:
                    new_y = 800

                # --> Update position
                self.pos = (new_x, new_y)

        elif action.split()[0] == "Mine":
            # --> Get target mine
            mine = environment.sources_dict[action.split()[-1]]

            # --> Get target resource
            mined_resource = action.split()[1]

            # --> Perform mining action
            mine.mine(self, mined_resource)

        elif action.split()[0] == "buy" or action.split()[0] == "sell":
            # --> Get target market
            market = environment.converters_dict[action.split()[-1]]

            # --> Get target transaction
            transaction = action.split()[0]

            # --> Get target item_type/item
            item_type = action.split()[1]
            item = action.split()[2]

            # --> Perform trade
            market.evaluate_transaction(date, self, transaction, item_type, item, 1)      # TODO: Auto pick quantity

        elif action == "Do nothing":
            pass

        # --> Record step
        if self.characteristics["Age"] >= self.settings.agent_settings.max_age \
                or self.inventory["Money"] >= self.settings.agent_settings.max_money:
            done = True
        else:
            done = False

        # Step reward
        net = (self.inventory["Money"] - prev_money)/self.characteristics["Age"]

        if net > 0:
            self.profit.append(net)
        else:
            self.profit.append(0)

        # Step position
        self.pos_history.append(self.pos)

        # Step action
        self.action_history.append(action)

        # --> Increase agent age
        self.characteristics["Age"] += 1

        # --> Return step results
        new_state = self.get_observations(environment)
        reward = self.profit[-1]

        if done:
            self.profit_history.append(sum(self.profit))

        return new_state, reward, done

    def get_observations(self, environment):
        # ----- Setup State: [x, y, distance_from_other_POI, Tool, used_cargo, Inventory (resources), Money]
        state = list()

        # --> Add position
        state.append(self.pos[0])       # x pos
        state.append(self.pos[-1])      # y pos

        # # --> Add distance from other POIs
        # for POI in environment.POI_dict.keys():
        #     poi_pos = environment.POI_dict[POI].pos
        #     state.append(((self.pos[0] - poi_pos[0]) ** 2 + (self.pos[1] - poi_pos[1]) ** 2) ** (1 / 2))

        # --> Add characteristics high/low
        # Tool
        state.append(self.characteristics["Tool"])

        # --> Add used cargo
        state.append(self.used_cargo)

        # --> Add inventory
        # Resources
        for resource in self.inventory["Resources"].keys():
            state.append(self.inventory["Resources"][resource])

        # Money
        state.append(self.inventory["Money"])

        return state

    def get_action_lst(self, environment: "Environment Object"):
        # ----- List actions
        self.action_lst = []
        available_action_lst = []

        # --> Listing moving actions
        for POI in environment.POI_dict.keys():
            self.action_lst.append("Move to " + POI)
            available_action_lst.append(1)

        # --> Listing mining actions
        for source in environment.sources_dict.keys():
            # --> List actions
            for resource in environment.sources_dict[source].inventory["Resources"].keys():
                self.action_lst.append("Mine " + resource + " in " + source)

                # --> Evaluate action possibility
                if environment.sources_dict[source].pos == self.pos:
                    available_action_lst.append(1)
                else:
                    available_action_lst.append(0)

        # --> Listing trade actions
        for converter in environment.converters_dict.keys():
            # --> List actions
            for item_type in environment.converters_dict[converter].inventory.keys():
                if item_type == "Money":
                    pass
                else:
                    for item in environment.converters_dict[converter].inventory[item_type].keys():
                        self.action_lst.append("buy " + item_type + " " + item + " in " + converter)
                        self.action_lst.append("sell " + item_type + " " + item + " in " + converter)

                    # --> Evaluate action possibility
                    if environment.converters_dict[converter].pos == self.pos:
                        available_action_lst.append(1)
                    else:
                        available_action_lst.append(0)

        # --> Adding "Do nothing" action
        self.action_lst.append("Do nothing")
        available_action_lst.append(1)

        return self.action_lst, available_action_lst

    def gen_q_table(self, environment: "Environment Object", nb_buckets=20):
        # ----- Build os high/low lists
        # --> Add position
        self.os_high = [800, 800]   # x, y pos
        self.os_low = [0, 0]        # x, y pos

        # # --> Add distance from other POIs
        # self.os_high = environment.high
        # self.os_low = environment.low

        # --> Add characteristics high/low
        # Tool
        self.os_high.append(100)
        self.os_low.append(0)

        # --> Add used cargo high/low
        self.os_high.append(5)
        self.os_low.append(0)

        # --> Add inventory high/low
        # Resources
        for _ in self.inventory["Resources"].keys():
            self.os_high.append(5)
            self.os_low.append(0)

        # Money
        self.os_high.append(self.settings.agent_settings.max_money)
        self.os_low.append(0)

        # ----- Compute discrete observation window size and build q table
        self.nb_states = len(self.get_observations(environment))
        self.nb_actions = len(self.get_action_lst(environment)[0])

        # --> Compute discrete observations window size
        discrete_os_size = [nb_buckets] * self.nb_states
        self.discrete_os_win_size = (np.array(self.os_high) + 1 - np.array(self.os_low)) / discrete_os_size

        # --> Initiate Q table
        self.q_table = np.random.uniform(low=-2, high=0, size=(discrete_os_size + [self.nb_actions]))

    def __str__(self):
        return self.name + " (Bot)"

    def __repr__(self):
        self.__repr__()
