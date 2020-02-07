
##################################################################################################################
"""
Used to combine all setting classes
"""

# Built-in/Generic Imports

# Libs

# Own modules
from Ingenium_Engine.Settings.RL_behavior_settings import RL_behavior_settings
from Ingenium_Engine.Settings.Environment_settings import Environment_settings
from Ingenium_Engine.Settings.Agent_settings import Agent_settings

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '7/02/2020'

##################################################################################################################


class SETTINGS:
    def __init__(self):
        self.rl_behavior_settings = RL_behavior_settings()
        self.environment_settings = Environment_settings()
        self.agent_settings = Agent_settings()
