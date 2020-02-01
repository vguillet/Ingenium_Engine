
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
import networkx as nx
import matplotlib.pyplot as plt

# Own modules


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Environment:
    def __init__(self):
        self.graph = nx.Graph()

    def add_POI(self, POI: "POI Object"):
        self.graph.add_node(POI.name, pos=(POI.x, POI.y))

        return

    def plot_environment_graph(self):

        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True)

        plt.show()
        return


if __name__ == "__main__":
    from faker import Faker

    from Sapientae_Engine.Environment.POI_gen import POI
    from Sapientae_Engine.Environment.Tools.POI_content_tools import POI_tools

    fake = Faker()
    Faker.seed(322)

    poi_tools = POI_tools()
    poi_1 = POI(fake.name().split(" ")[1] + " City", "City", 0, 0, ef_dict=poi_tools.gen_ef_dict())
    poi_2 = POI(fake.name().split(" ")[1] + " City", "City", -2, 2, ef_dict=poi_tools.gen_ef_dict())
    poi_3 = POI(fake.name().split(" ")[1] + " City", "City", 2, 2, ef_dict=poi_tools.gen_ef_dict())
    poi_4 = POI(fake.name().split(" ")[1] + " City", "City", 2, -2, ef_dict=poi_tools.gen_ef_dict())
    poi_5 = POI(fake.name().split(" ")[1] + " City", "City", -2, -2, ef_dict=poi_tools.gen_ef_dict())

    env = Environment()
    env.add_POI(poi_1)
    env.add_POI(poi_2)
    env.add_POI(poi_3)
    env.add_POI(poi_4)
    env.add_POI(poi_5)

    env.plot_environment_graph()
