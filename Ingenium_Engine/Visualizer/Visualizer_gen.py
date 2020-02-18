
################################################################################################################
"""

"""

# Built-in/Generic Imports
import time

# Libs
import pygame as pg

# Own modules
from Ingenium_Engine.Visualizer.Visualizer_tools import Visualizer_tools
from Ingenium_Engine.Visualizer.Agent_visu_gen import gen_agent_visu
from Ingenium_Engine.Visualizer.POI_visu_gen import gen_POI_visu
from Ingenium_Engine.Visualizer.Dynamic_label_gen import gen_dynamic_label

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_visualizer:
    def __init__(self, run_name: str, environment: "Environment object", agents_dict: dict):
        # ======================== INITIALISATION =======================================
        # ----- Initialise packages and tools
        pg.init()
        pg.font.init()
        pg.mixer.init()
        
        visualiser_tools = Visualizer_tools()
        
        # --> Setup visualiser settings
        fps = 30
        margin = 100

        # --> Setup visualizer window
        screen_size = (environment.size[0] + 2*margin, environment.size[-1] + 2*margin)
        screen = pg.display.set_mode(screen_size)          # Window size
        pg.display.set_caption(run_name)                        # Window name

        # --> Setup visualizer clock (to keep track of visualiser run speed)
        clock = pg.time.Clock()

        # --> Create sprite groups and lists
        all_sprites_group = pg.sprite.Group()
        POI_sprite_group = pg.sprite.Group()
        agent_sprite_group = pg.sprite.Group()

        # ----- Create POIs
        POIs_visu_dict = visualiser_tools.gen_POI_visu_dict(environment, margin)

        # --> Add sprites to group
        for sprite in POIs_visu_dict.keys():
            all_sprites_group.add(POIs_visu_dict[sprite]["Sprite"])
            POI_sprite_group.add(POIs_visu_dict[sprite]["Sprite"])
                
        # ----- Create agents
        agents_visu_dict = visualiser_tools.gen_agents_visu_dict(agents_dict, margin)

        # --> Add sprites to group
        for sprite in agents_visu_dict.keys():
            all_sprites_group.add(agents_visu_dict[sprite]["Sprite"])
            agent_sprite_group.add(agents_visu_dict[sprite]["Sprite"])

        # ======================== PROCESS ==============================================
        running = True
        step = -1
        while running:
            # --> Keep loop running at the right speed (to match requested fps count)
            # clock.tick(fps)
            time.sleep(0.5)

            # --> Set step
            step += 1

            # ----- Process input (events)
            for event in pg.event.get():
                # --> Close windows/exit pygame if window is closed
                if event.type == pg.QUIT:
                    running = False

            # ----- Update all sprites
            agent_sprite_group.update(step)

            visualiser_tools.update_dynamic_labels(agents_visu_dict, step)

            # ----- Draw/render
            # --> Fill screen with white
            screen.fill((255, 255, 255))

            # --> Draw all sprites
            all_sprites_group.draw(screen)

            # --> Add POI label to image
            visualiser_tools.blit_all_labels(POIs_visu_dict, screen)

            # --> Add agents label to image
            visualiser_tools.blit_all_labels(agents_visu_dict, screen)

            # --> Flip display *after* drawing everything
            pg.display.flip()

        pg.quit()
