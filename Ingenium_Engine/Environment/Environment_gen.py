
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
    def __init__(self, name):
        # --> Setup reference properties
        self.name = name
        self.POI_dict = {}
        self.graph = nx.Graph()

    def __str__(self):
        return self.name + " (Environment)"

    def __repr__(self):
        return self.__str__()

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

    def add_POI_link(self, POI_1: "POI Object", POI_2: "POI Object"):
        self.graph.add_edge(POI_1.name, POI_2.name)
        return

    def plot_environment_graph(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True)

        plt.show()
        return


if __name__ == "__main__":
    from Ingenium_Engine.Environment.POI_gen import gen_POI
    from Ingenium_Engine.Environment.Tools.POI_tools import POI_tools

    poi_tools = POI_tools()
    poi_1 = gen_POI("Paris", "City", pos=(0, 0), ef_dict=poi_tools.gen_ef_dict(pos=(0, 0), market_count=1))
    poi_2 = gen_POI("Amsterdam", "City", pos=(1, 1), ef_dict=poi_tools.gen_ef_dict(pos=(1, 1)))
    poi_3 = gen_POI("London", "City", pos=(-1, -1), ef_dict=poi_tools.gen_ef_dict(pos=(-1, -1)))
    poi_4 = gen_POI("Berlin", "City", pos=(-1, 1), ef_dict=poi_tools.gen_ef_dict(pos=(-1, 1)))
    poi_5 = gen_POI("Shefield", "City", pos=(1, -1), ef_dict=poi_tools.gen_ef_dict(pos=(1, -1)))

    poi_6 = gen_POI("Tokio", "City", pos=(2, -1), ef_dict=poi_tools.gen_ef_dict(pos=(2, -1)))

    POI_lst = [poi_1, poi_2, poi_3, poi_4, poi_5, poi_6]

    env = gen_environment("Class test env")

    print(env)

    for poi in POI_lst:
        env.add_POI(poi)

    env.add_POI_link(poi_1, poi_2)
    env.add_POI_link(poi_1, poi_3)
    env.add_POI_link(poi_1, poi_4)
    env.add_POI_link(poi_1, poi_5)

    env.plot_environment_graph()

    env.remove_POI(poi_6)

    env.plot_environment_graph()
