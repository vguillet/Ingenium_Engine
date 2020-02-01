
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


class POI:
    def __init__(self, name, label, x, y, ef_dict=None):
        # --> Setup POI reference properties
        self.name = name
        self.label = label

        # --> Setup POI position
        self.x = x
        self.y = y

        # --> Setup POI content
        if ef_dict is None:
            self.ef_dict = {"Sources": {},
                            "Converters": {}}
        else:
            self.ef_dict = ef_dict

    def add_to_ef_dict(self, ef):
        self.ef_dict[ef.ef_type][ef.name] = ef
        return
