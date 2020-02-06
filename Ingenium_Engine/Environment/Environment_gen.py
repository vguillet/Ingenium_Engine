
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
    def __init__(self, name):
        # ----- Setup reference properties
        self.name = name
        self.POI_dict = {}
        self.graph = nx.Graph()

    def __str__(self):
        return self.name + " (Environment)"

    def __repr__(self):
        return self.__str__()

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

    def plot_environment_graph(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True)

        plt.show()
        return

    def gen_random_layout(self, number_of_POI=6, number_of_markets=3, number_of_mines=6):
        # --> Seeding generators
        Faker.seed(4323)
        random.seed(4353)
        np.random.seed(4457)

        # --> Reset current environment content
        self.POI_dict = {}
        self.graph = nx.Graph()

        # --> Initiate environment features counter
        mine_count = number_of_mines
        market_count = number_of_markets

        fake = Faker()

        name_list = []
        pos_list = []

        # --> Adding POI to environment
        for _ in range(number_of_POI):
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

        self.add_close_POI_links(3)

        print("-- Random environment layout generated successfully --")


if __name__ == "__main__":
    from Ingenium_Engine.Environment.POI_gen import gen_POI

    env = gen_environment("Class test env")

    env.gen_random_layout(number_of_POI=10)
