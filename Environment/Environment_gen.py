
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
from itertools import combinations

# Libs
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from faker import Faker

# Own modules
from Ingenium_Engine.Environment.POI_gen import gen_POI
from Ingenium_Engine.Visualizer.Visualizer_gen import gen_visualizer


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_environment:
    def __init__(self, name: str, nb_POI: int = 6, nb_markets: int = 3, nb_mines: int = 6, environment_size: tuple = (800, 800)):
        """
        Environment class, used to generate Ingenium environments

        :param name: Name of environment
        :param nb_POI: nb of POI to be included in environment
        :param nb_markets: nb of markets to be included in environment
        :param nb_mines: nb of mines to be included in environment
        :param environment_size: Size of environment to be generated in pixels
        :param POI_dict: (Optional) POI dictionary for a predefined environment layout/content
        """
        # ----- Setup reference properties
        self.name = name
        self.type = "Environment"
        self.size = environment_size

        self.POI_dict = {}
        self.graph = nx.Graph()

        self.gen_random_layout(nb_POI, nb_markets, nb_mines, environment_size)

    # =============================================================================== Getters

    @property
    def converters_dict(self):
        converters_dict = {}
        for POI in self.POI_dict.keys():
            for converter in self.POI_dict[POI].ef_dict["Converters"].keys():
                converters_dict[converter] = self.POI_dict[POI].ef_dict["Converters"][converter]
        return converters_dict

    @property
    def sources_dict(self):
        sources_dict = {}
        for POI in self.POI_dict.keys():
            for source in self.POI_dict[POI].ef_dict["Sources"].keys():
                sources_dict[source] = self.POI_dict[POI].ef_dict["Sources"][source]
        return sources_dict

    @property
    def high(self):
        # --> Max x and y
        high_lst = [self.size[0], self.size[-1]]

        # --> Add max distance for each POI (diagonal of env)
        max_distance = (self.size[0] ** 2 + self.size[-1] ** 2) ** (1 / 2)
        for _ in self.POI_dict.keys():
            high_lst.append(max_distance)
        return high_lst

    @property
    def low(self):
        # --> Max x and y
        low_lst = [0, 0]

        # --> Add max distance for each POI (diagonal of env)
        for _ in self.POI_dict.keys():
            low_lst.append(0)
        return low_lst

    def visualise_environment(self):
        gen_visualizer(self.name, self, press_start=False)
        return

    def plot_environment_graph(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True)

        plt.show()
        return

    def save_environment_graph(self):
        # --> Set plot size
        plt.figure(figsize=(8, 8))

        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True)

        plt.savefig("Ingenium_Engine/Visualizer/Assets/Environments/" + self.name)
        print(self.name + " environment graph saved successfully")
        return

    def get_POI_at_pos(self, pos: tuple):
        for POI in self.POI_dict.keys():
            if self.POI_dict[POI].pos == pos:
                return POI
            else:
                print("!!! No POI at provided pos !!!")
                return

    def get_label_of_name(self, name: str):
        for POI in self.POI_dict.keys():
            if POI == name:
                return self.POI_dict[POI].label
            else:
                for ef in self.POI_dict[POI].ef_dict.keys():
                    if ef == name:
                        return self.POI_dict[POI].ef_dict[ef].label
                    else:
                        pass
        print("!!! Name not found !!!")

    # =============================================================================== Setters

    def add_POI(self, POI: "POI Object"):
        self.POI_dict[POI.name] = POI
        self.graph.add_node(POI.name, pos=POI.pos)
        return

    def remove_POI(self, POI: "POI Object"):
        del self.POI_dict[POI.name]
        self.graph.remove_node(POI.name)
        return

    def gen_random_layout(self, nb_POI=6, nb_markets=3, nb_mines=6, environment_size=(800, 800)):
        # --> Seeding generators
        Faker.seed(4323)
        random.seed(43)

        # --> Initiate environment features counter
        mine_count = nb_mines
        market_count = nb_markets

        fake = Faker()

        name_lst = []
        pos_lst = []

        # --> Adding POI to environment
        for i in range(nb_POI):
            # --> Generate POI name
            name = fake.first_name() + "_City"
            while name in name_lst:
                name = fake.first_name() + "_City"
            name_lst.append(name)

            if i != nb_POI-1:
                # --> Generate random ed count
                # TODO: Fix mine count repartition
                mines = random.randint(0, 2)
                mine_count -= mines

                markets = random.randint(0, market_count)
                market_count -= markets

            else:
                # --> If last POI, add all missing ef:
                mines = mine_count
                markets = market_count

            # --> Generate POI position
            min_distance = 100
            valid_new_pos = False

            while valid_new_pos is not True:
                new_pos = (random.randint(0, environment_size[0]), random.randint(0, environment_size[-1]))

                if len(pos_lst) > 1:
                    # Checking if POI is at a reasonable distance from other POI
                    distance_lst = []

                    for pos in pos_lst:
                        distance_lst.append(((new_pos[0] - pos[0]) ** 2 + (new_pos[1] - pos[1]) ** 2) ** (1 / 2))

                    if min(distance_lst) > min_distance:
                        valid_new_pos = True
                    else:
                        pass
                else:
                    valid_new_pos = True

            pos_lst.append(new_pos)

            self.add_POI(gen_POI(name, "City", new_pos,
                                 mine_count=mines,
                                 market_count=markets))

        print("-- Random environment layout generated successfully --")

    def __str__(self):
        return self.name + " (Environment)"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    from Ingenium_Engine.Environment.POI_gen import gen_POI

    env = gen_environment("Class test env")
