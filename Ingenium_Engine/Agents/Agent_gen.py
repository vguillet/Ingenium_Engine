
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Ingenium_Engine.Settings.SETTINGS import SETTINGS
from Ingenium_Engine.Agents.Tools.Traits_tools import Traits_tools
from Ingenium_Engine.Tools.Inventory_tools import Inventory_tools
from Ingenium_Engine.Tools.Interests_tools import Interests_tools
from Ingenium_Engine.Tools.Characteristics_tools import Characteristics_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_Agent:
    def __init__(self,
                 environment: "Environment object",
                 name: "Bot name",
                 pos: tuple,
                 traits: dict = None,
                 inventory: dict = None,
                 interests: dict = None,
                 characteristics: dict = None):
        # ----- Setup reference properties
        self.name = name
        self.pos = pos

        # --> Setup traits/inventory/interests/characteristics dicts
        self.gen_dicts(traits, inventory, interests, characteristics)

        # --> Setup trackers
        self.profit = []

    @property
    def used_cargo(self):
        used_cargo = 0
        for resource in self.inventory["Resources"].keys():
            used_cargo += self.inventory["Resources"][resource]
        return used_cargo

    def step(self, environment: "Environment Object", action):
        """
        Possible actions:   - 1 : Move
                            - 2 : Mine
                            - 3 : Sell
                            - 4 : Buy

        :param environment:
        :param action:
        :return:
        """
        settings = SETTINGS()
        settings.agent_settings.gen_agent_settings()

        prev_money = self.inventory["Money"]

        # --> Perform action


        # --> Record step reward
        net = self.inventory["Money"] - prev_money
        if net > 0:
            self.profit.append(net)
        else:
            self.profit.append(0)

        # --> Increase agent age
        self.characteristics["Age"] += 1

        # --> Return step results
        new_state = self.get_observations(environment)
        reward = self.profit[-1]

        if self.characteristics["Age"] > settings.agent_settings.max_age \
                or self.inventory["Money"] >= settings.agent_settings.max_money:
            done = True
        else:
            done = False

        return new_state, reward, done

    def get_observations(self, environment):
        # ----- Setup State: [x, y, distance_from_other_POI, Tool, used_cargo, Inventory (resources), Money]
        state = list()

        # --> Add position
        state.append(self.pos[0])
        state.append(self.pos[-1])

        # --> Add distance from other POIs
        for POI in environment.POI_dict.keys():
            pos = environment.POI_dict[POI].pos
            state.append(((self.pos[0] - pos[0]) ** 2 + (self.pos[1] - pos[1]) ** 2) ** (1 / 2))

        # --> Add tool characteristic
        state.append(self.characteristics["Tool"])

        # --> Add used cargo
        state.append(self.used_cargo)

        # --> Add inventory
        for resource in self.inventory["Resources"].keys():
            state.append(self.inventory["Resources"][resource])

        # --> Add Money
        state.append(self.inventory["Money"])

        return state

    def get_action_lst(self, environment: "Environment Object"):
        # ----- List actions
        action_lst = []
        available_action_lst = []

        # --> Listing moving actions
        for POI in environment.POI_dict.keys():
            action_lst.append("Move to " + POI)
            available_action_lst.append(1)

        # --> Listing mining actions
        for source in environment.sources_dict.keys():
            # --> List actions
            for resource in environment.sources_dict[source].inventory["Resources"].keys():
                action_lst.append("Mine " + resource + " in " + source)

            # --> Evaluate action
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
                        action_lst.append("Buy " + item + " in " + converter)

            # --> Evaluate action
            if environment.converters_dict[converter].pos == self.pos:
                available_action_lst.append(1)
            else:
                available_action_lst.append(0)

        # --> Adding "Do nothing" action
        action_lst.append("Do nothing")
        available_action_lst.append(1)

        return action_lst, available_action_lst

    def gen_dicts(self,
                  traits: dict,
                  inventory: dict,
                  interests: dict,
                  characteristics: dict):
        # --> Setting up traits
        if traits is not None:
            self.traits = traits
        else:
            self.traits = Traits_tools().gen_traits_dict()

        # --> Setting up inventory
        if inventory is not None:
            self.inventory = inventory
        else:
            self.inventory = Inventory_tools().gen_agent_inventory_dict()

        # --> Setting up interest
        if interests is not None:
            self.interests = interests
        else:
            self.interests = Interests_tools().gen_agent_interests_dict()

        # --> Setting up characteristics
        if characteristics is not None:
            self.characteristics = characteristics
        else:
            self.characteristics = Characteristics_tools().gen_agent_characteristics_dict()

    def __str__(self):
        return self.name + " (Bot)"

    def __repr__(self):
        self.__repr__()
