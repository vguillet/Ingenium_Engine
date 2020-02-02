
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


class gen_environment:
    def __init__(self):
        self.POI_dict = {}
        self.graph = nx.Graph()

    def add_POI(self, POI: "POI Object"):
        self.POI_dict[POI.name] = POI
        self.graph.add_node(POI.name, pos=POI.pos)
        return

    def remove_POI(self, POI: "POI Object"):
        del self.POI_dict[POI.name]
        self.graph.remove_node(POI.name)
        return

    def add_POI_link(self, POI_1: "POI Object", POI_2: "POI Object"):
        self.graph.add_edge(POI_1.name, POI_2.name)
        return

    def plot_environment_graph(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True)

        plt.show()
        return


if __name__ == "__main__":
    from Sapientae_Engine.Environment.POI_gen import gen_POI
    from Sapientae_Engine.Environment.Tools.POI_tools import POI_tools

    poi_tools = POI_tools()
    poi_1 = gen_POI("Paris", "City", pos=(0, 0), ef_dict=poi_tools.gen_ef_dict(market_count=1))
    poi_2 = gen_POI("Amsterdam", "City", pos=(1, 1), ef_dict=poi_tools.gen_ef_dict())
    poi_3 = gen_POI("London", "City", pos=(-1, -1), ef_dict=poi_tools.gen_ef_dict())
    poi_4 = gen_POI("Berlin", "City", pos=(-1, 1), ef_dict=poi_tools.gen_ef_dict())
    poi_5 = gen_POI("Shefield", "City", pos=(1, -1), ef_dict=poi_tools.gen_ef_dict())

    poi_6 = gen_POI("Tokio", "City", pos=(2, -1), ef_dict=poi_tools.gen_ef_dict())

    POI_lst = [poi_1, poi_2, poi_3, poi_4, poi_5, poi_6]

    env = gen_environment()
    for poi in POI_lst:
        env.add_POI(poi)

    env.add_POI_link(poi_1, poi_2)
    env.add_POI_link(poi_1, poi_3)
    env.add_POI_link(poi_1, poi_4)
    env.add_POI_link(poi_1, poi_5)

    env.plot_environment_graph()

    env.remove_POI(poi_6)

    env.plot_environment_graph()
