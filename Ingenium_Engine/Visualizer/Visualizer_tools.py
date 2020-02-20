
################################################################################################################
"""

"""

# Built-in/Generic Imports
import time

# Libs
import pygame as pg

# Own modules
from Ingenium_Engine.Visualizer.Agent_visu_gen import gen_agent_visu
from Ingenium_Engine.Visualizer.POI_visu_gen import gen_POI_visu
from Ingenium_Engine.Visualizer.Dynamic_label_gen import gen_dynamic_label

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Visualizer_tools:
    @staticmethod
    def update_dynamic_labels(sprite_dictionary, step):
        for sprite in sprite_dictionary.keys():
            for dynamic_label in sprite_dictionary[sprite]["Dynamic_Labels"].keys():
                sprite_dictionary[sprite]["Dynamic_Labels"][dynamic_label].update(step)
    
    @staticmethod
    def blit_all_labels(sprite_dictionary, screen):
        for sprite in sprite_dictionary.keys():
            # --> Blit labels
            for label in sprite_dictionary[sprite]["Labels"].keys():
                screen.blit(sprite_dictionary[sprite]["Labels"][label]["Label"],
                            sprite_dictionary[sprite]["Labels"][label]["Pos"])

            # --> Blit dynamic labels
            for dynamic_label in sprite_dictionary[sprite]["Dynamic_Labels"].keys():
                screen.blit(sprite_dictionary[sprite]["Dynamic_Labels"][dynamic_label].label,
                            sprite_dictionary[sprite]["Dynamic_Labels"][dynamic_label].label_pos)
    
    @staticmethod
    def gen_POI_visu_dict(environment, margin):
        POIs_visu_dict = {}

        for POI in environment.POI_dict.keys():
            POIs_visu_dict[POI] = {}

            # --> Create POI sprite
            sprite = gen_POI_visu(environment.POI_dict[POI], margin)

            # Add POI sprite to dict
            POIs_visu_dict[POI]["Sprite"] = sprite
            
            # --> Create labels
            POIs_visu_dict[POI]["Labels"] = {}

            h_offset = -20
            v_offset = 55

            # Add name label
            name_font = pg.font.SysFont("comicsansms", 20)

            POIs_visu_dict[POI]["Labels"]["Name"] = {}
            POIs_visu_dict[POI]["Labels"]["Name"]["Label"] = name_font.render(POI, False, (0, 0, 0))
            POIs_visu_dict[POI]["Labels"]["Name"]["Pos"] = (POIs_visu_dict[POI]["Sprite"].rect[0] + h_offset,
                                                            POIs_visu_dict[POI]["Sprite"].rect[1] + v_offset)
            h_offset += 15
            v_offset += 25

            # Add converters labels
            converter_font = pg.font.SysFont("comicsansms", 12)

            for converter in environment.POI_dict[POI].ef_dict["Converters"].keys():
                POIs_visu_dict[POI]["Labels"][converter] = {}
                POIs_visu_dict[POI]["Labels"][converter]["Label"] = converter_font.render(converter, False, (0, 0, 0))
                POIs_visu_dict[POI]["Labels"][converter]["Pos"] = (POIs_visu_dict[POI]["Sprite"].rect[0] + h_offset,
                                                                   POIs_visu_dict[POI]["Sprite"].rect[1] + v_offset)
                v_offset += 12

            # Add sources labels
            v_offset += 2
            source_font = pg.font.SysFont("comicsansms", 12)

            for source in environment.POI_dict[POI].ef_dict["Sources"].keys():
                POIs_visu_dict[POI]["Labels"][source] = {}
                POIs_visu_dict[POI]["Labels"][source]["Label"] = source_font.render(source, False, (0, 0, 0))
                POIs_visu_dict[POI]["Labels"][source]["Pos"] = (POIs_visu_dict[POI]["Sprite"].rect[0] + h_offset,
                                                                POIs_visu_dict[POI]["Sprite"].rect[1] + v_offset)
                v_offset += 12

            # --> Create dynamic labels
            POIs_visu_dict[POI]["Dynamic_Labels"] = {}

        return POIs_visu_dict

    @staticmethod
    def gen_agents_visu_dict(agents_dict, margin):
        agents_visu_dict = {}

        for agent in agents_dict.keys():
            agents_visu_dict[agent] = {}

            # --> Create agent sprite
            sprite = gen_agent_visu(agents_dict[agent], margin)

            # Add agent sprite to dict
            agents_visu_dict[agent]["Sprite"] = sprite

            # --> Create labels
            agents_visu_dict[agent]["Labels"] = {}

            # --> Create dynamic labels
            agents_visu_dict[agent]["Dynamic_Labels"] = {}

            # Add name label
            agents_visu_dict[agent]["Dynamic_Labels"]["Name"] = gen_dynamic_label(agent,
                                                                                  agents_dict[agent].pos_history,
                                                                                  15, 25, -12, margin)

            # Add action label
            agents_visu_dict[agent]["Dynamic_Labels"]["Action"] = gen_dynamic_label(agents_dict[agent].action_history,
                                                                                    agents_dict[agent].pos_history,
                                                                                    12, -30, 10, margin)

        return agents_visu_dict
