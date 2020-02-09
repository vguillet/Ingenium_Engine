
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
import pygame as pg

# Own modules
from Ingenium_Engine.Visualizer.Agent_visu_gen import gen_agent_visu
from Ingenium_Engine.Visualizer.POI_visu_gen import gen_POI_visu

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_visualizer:
    def __init__(self, run_name: str, environment: "Environment object", agents_dict: dict):
        # ======================== INITIALISATION =======================================
        # --> Initialise packages
        pg.init()
        pg.font.init()
        pg.mixer.init()

        # --> Setup visualiser settings
        fps = 30
        margin = 50

        # --> Setup visualizer window
        screen_size = (environment.size[0] + 2*margin, environment.size[-1] + 2*margin)
        screen = pg.display.set_mode(environment.size)          # Window size
        pg.display.set_caption(run_name)                        # Window name

        # --> Setup visualizer clock (to keep track of visualiser run speed)
        clock = pg.time.Clock()

        # --> Create sprite groups and lists
        all_sprites_group = pg.sprite.Group()
        POI_sprite_group = pg.sprite.Group()
        agent_sprite_group = pg.sprite.Group()
        label_list = []

        # --> Create POI sprites
        POI_visu_dict = {}
        font = pg.font.SysFont('Comic Sans MS', 20)

        for POI in environment.POI_dict.keys():
            sprite = gen_POI_visu(environment.POI_dict[POI], margin)

            # --> Add sprite to group
            all_sprites_group.add(sprite)
            POI_sprite_group.add(sprite)
            POI_visu_dict[POI] = {}
            POI_visu_dict[POI]["Sprite"] = sprite
            POI_visu_dict[POI]["Label"] = font.render(POI, False, (0, 0, 0))

        # --> Create agent sprites
        agents_visu_dict = {}
        font = pg.font.SysFont('Comic Sans MS', 15)

        for agent in agents_dict.keys():
            sprite = gen_agent_visu(agents_dict[agent], margin)

            # --> Add sprite to group
            all_sprites_group.add(sprite)
            agent_sprite_group.add(sprite)

            agents_visu_dict[agent] = {}
            agents_visu_dict[agent]["Sprite"] = sprite
            agents_visu_dict[agent]["Label"] = font.render(agent, False, (0, 0, 0))

        # ======================== PROCESS ==============================================
        running = True
        while running:
            # --> Keep loop running at the right speed (to match requested fps count)
            clock.tick(fps)

            # ----- Process input (events)
            for event in pg.event.get():
                # --> Close windows/exit pygame if window is closed
                if event.type == pg.QUIT:
                    running = False

            # ----- Update
            agent_sprite_group.update()

            # ----- Draw/render
            # --> Fill screen with white
            screen.fill((255, 255, 255))

            # --> Draw all sprites
            all_sprites_group.draw(screen)

            # --> Add POI label to image
            for POI in POI_visu_dict.keys():
                screen.blit(POI_visu_dict[POI]["Label"], (POI_visu_dict[POI]["Sprite"].rect[0] - 20,
                                                          POI_visu_dict[POI]["Sprite"].rect[1] + 55))

            # --> Add agents label to image
            for agent in agents_visu_dict.keys():
                screen.blit(agents_visu_dict[agent]["Label"], (agents_visu_dict[agent]["Sprite"].rect[0] + 25,
                                                               agents_visu_dict[agent]["Sprite"].rect[1] - 3))

            # --> Flip display *after* drawing everything
            pg.display.flip()

        pg.quit()


if __name__ == "__main__":
    from Ingenium_Engine.Settings.SETTINGS import SETTINGS
    from Ingenium_Engine.Environment.Environment_gen import gen_environment
    from Ingenium_Engine.Agents.Agent_gen import gen_Agent
    from faker import Faker
    import random

    # ----- Initialise tools
    settings = SETTINGS()
    settings.rl_behavior_settings.gen_simple_ql_settings()
    settings.environment_settings.gen_environment_settings()
    settings.agent_settings.gen_agent_settings()

    fake = Faker()

    # --> Seeding generators
    random.seed(345)
    Faker.seed(345)

    # ----- Gen initial training environment
    starting_env = gen_environment("Ingenium_1",
                                   settings.environment_settings.nb_POI,
                                   settings.environment_settings.nb_markets,
                                   settings.environment_settings.nb_mines,
                                   settings.environment_settings.nb_link_per_POI)

    agents = {}
    for _ in range(3):
        agent_name = fake.name()
        agent_starting_position = starting_env.POI_dict[random.choice(list(starting_env.POI_dict.keys()))].pos
        agents[agent_name] = gen_Agent(starting_env, agent_name, agent_starting_position)

    visualizer = gen_visualizer("Test", starting_env, agents)

