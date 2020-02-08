
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

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_environment:
    def __init__(self, name, nb_POI=6, nb_markets=3, nb_mines=6, nb_links_per_POI=3, POI_dict: dict=None):
        """
        Environment class, used to generate Ingenium environments. A POI dict can be directly provided
        when initialising a new environment, in which case the environment will be built accordingly
        (disregarding other environment specification parameters)

        :param name: Name of environment
        :param nb_POI: nb of POI to be included in environment
        :param nb_markets: nb of markets to be included in environment
        :param nb_mines: nb of mines to be included in environment
        :param POI_dict: (Optional) POI dictionary for a predefined environment layout/content
        """
        # ----- Setup reference properties
        self.name = name
        self.type = "Environment"

        if POI_dict is not None:
            self.POI_dict = POI_dict
            self.graph = nx.Graph()

            for POI in POI_dict.keys():
                self.add_POI(POI_dict[POI])
        else:
            self.gen_random_layout(nb_POI, nb_markets, nb_mines, nb_links_per_POI)

    def __str__(self):
        return self.name + " (Environment)"

    def __repr__(self):
        return self.__str__()

    # =============================================================================== Getters

    def get_POI_links(self, POI: "POI name"):
        return self.graph.edges(POI)

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

    def plot_environment_graph(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True)

        plt.show()
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

    def add_POI_link(self, POI_1: "POI Name", POI_2: "POI Name"):
        self.graph.add_edge(POI_1, POI_2)
        return

    def add_close_POI_links(self, nb_close_links):
        existing_links = []

        # --> Adding edges
        for current_POI in self.POI_dict.keys():
            distance = []
            adjacent_POIs = []

            for POI in self.POI_dict.keys():
                if current_POI == POI:
                    pass
                else:
                    adjacent_POIs.append(self.POI_dict[POI])
                    pos_current = self.POI_dict[current_POI].pos
                    pos = self.POI_dict[POI].pos

                    # --> Compute distance between current POI and other
                    distance.append(((pos_current[0] - pos[0]) ** 2 + (pos_current[1] - pos[1]) ** 2) ** (1 / 2))

                # --> Sort POIs from closest to farthest from current POI
                for j in range(len(distance)):
                    for i in range(len(distance) - 1):
                        if distance[i] > distance[i + 1]:
                            distance[i], distance[i + 1] = distance[i + 1], distance[i]
                            adjacent_POIs[i], adjacent_POIs[i + 1] = adjacent_POIs[i + 1], adjacent_POIs[i]

            # --> Create edge between x closest POI
            for k in range(nb_close_links):
                link = [self.POI_dict[current_POI].name, adjacent_POIs[k].name]
                link.sort()

                if link in existing_links:
                    pass
                else:
                    existing_links.append(link)
                    self.add_POI_link(self.POI_dict[current_POI].name, adjacent_POIs[k].name)
        return

    def add_all_POI_links(self):
        edges = combinations(self.POI_dict.keys(), 2)
        for edge in edges:
            self.add_POI_link(edge[0], edge[1])
        return

    def gen_random_layout(self, nb_POI=6, nb_markets=3, nb_mines=6, nb_links_per_POI=3):
        # --> Seeding generators
        Faker.seed(4323)
        random.seed(4353)
        np.random.seed(4457)

        # --> Reset current environment content
        self.POI_dict = {}
        self.graph = nx.Graph()

        # --> Initiate environment features counter
        mine_count = nb_mines
        market_count = nb_markets

        fake = Faker()

        name_list = []
        pos_list = []

        # --> Adding POI to environment
        for i in range(nb_POI):
            # --> Generate POI name
            name = fake.first_name() + " City"
            while name in name_list:
                name = fake.first_name() + " City"
            name_list.append(name)

            # --> Generate random ed count
            mines = random.randint(0, mine_count)
            mine_count -= mines

            markets = random.randint(0, market_count)
            market_count -= markets

            # --> Generate city position
            pos = (int(np.random.normal(-10, 10, 1)[0]),
                   int(np.random.normal(-10, 10, 1)[0]))
            pos_list.append(pos)

            self.add_POI(gen_POI(name, "City", pos,
                                 mine_count=mines,
                                 market_count=markets))

        self.add_close_POI_links(nb_links_per_POI)

        print("-- Random environment layout generated successfully --")


if __name__ == "__main__":
    from Ingenium_Engine.Environment.POI_gen import gen_POI

    env = gen_environment("Class test env")
