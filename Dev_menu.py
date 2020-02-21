
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Settings.SETTINGS import SETTINGS
from RL.Simple_QL.QL_algorithm import QL_optimiser
from Ingenium_Engine.Environment.Environment_gen import gen_environment


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################

# ----- Initialise settings
settings = SETTINGS()
settings.environment_settings.gen_environment_settings()

# ----- Gen training environment
environment_size = 800
environment = gen_environment("Ingenium_1",
                              settings.environment_settings.nb_POI,
                              settings.environment_settings.nb_markets,
                              settings.environment_settings.nb_mines,
                              environment_size=(environment_size, environment_size))

environment.visualise_environment()
environment.plot_environment_graph()

# --> Supplying mines
resources_list = ["Iron", "Gold", "Diamond"]
for mine in environment.sources_dict.keys():
    for resource in resources_list:
        environment.sources_dict[mine].add_to_inventory(resource, 100)

# --> Supplying market
for i, market in enumerate(environment.converters_dict.keys()):
    # environment.converters_dict[market].add_to_inventory("Items", "S_Health", 10, force_add=True)
    # environment.converters_dict[market].add_to_inventory("Items", "M_Health", 5, force_add=True)
    # environment.converters_dict[market].add_to_inventory("Items", "L_Health", 3, force_add=True)
    #
    # environment.converters_dict[market].add_to_inventory("Items", "S_Weapon", 10, force_add=True)
    # environment.converters_dict[market].add_to_inventory("Items", "M_Weapon", 5, force_add=True)
    # environment.converters_dict[market].add_to_inventory("Items", "L Weapon", 3, force_add=True)
    #
    # environment.converters_dict[market].add_to_inventory("Items", "S_Armor", 10, force_add=True)
    # environment.converters_dict[market].add_to_inventory("Items", "M_Armor", 5, force_add=True)
    # environment.converters_dict[market].add_to_inventory("Items", "L_Armor", 3, force_add=True)

    environment.converters_dict[market].add_to_inventory("Items", "S_Tool", 10, force_add=True)
    # environment.converters_dict[market].add_to_inventory("Items", "M_Tool", 5, force_add=True)
    # environment.converters_dict[market].add_to_inventory("Items", "L_Tool", 3, force_add=True)


# sim = QL_optimiser(environment)
