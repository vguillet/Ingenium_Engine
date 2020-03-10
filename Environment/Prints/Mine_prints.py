
################################################################################################################
"""

"""

# Built-in/Generic Imports
from distutils import util

# Libs

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Mine_prints:
    def __init__(self):
        with open("Settings/Settings_cache/Print_settings", "r") as cache:
            for line in cache:
                if line.split()[0] == "Environment_prints":
                    environment_print_setting = bool(util.strtobool(line.split()[-1]))
                    break

        if environment_print_setting is False:
            self.mining_recap = self.__monkey_patch_pass
            self.gathered_resource_recap = self.__monkey_patch_pass
            self.failed_mining_recap = self.__monkey_patch_pass
            self.mine_empty = self.__monkey_patch_pass
            self.print_1 = self.__monkey_patch_pass

    @staticmethod
    def __monkey_patch_pass(*args, **kwargs):
        return

    @staticmethod
    def mining_recap(resource, mined_quantity):
        print("Mined " + str(mined_quantity) + " " + resource + " successfully")

    @staticmethod
    def gathered_resource_recap(resource, gathered_quantity):
        print("Mined " + str(gathered_quantity) + " " + resource + " successfully")

    @staticmethod
    def failed_mining_recap(agent_tool_characteristic, resource, resource_tool_characteristic_req):

        print(
            "Tool level " + str(agent_tool_characteristic) + " insufficient to mine " + str(resource) + " (req: " +
            str(resource_tool_characteristic_req) + ")")

    @staticmethod
    def mine_empty():
        print("Mine is empty")

    @staticmethod
    def print_1():
        print("Resource not in inventory")

