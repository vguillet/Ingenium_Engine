
################################################################################################################
"""
A converter sub-class specialising in exchanging items for money (both selling and buying)
"""

# Built-in/Generic Imports

# Libs

# Own modules
from Sapientae_Engine.Environment.Converters.Converter_gen import Converter
from Sapientae_Engine.Tools.Inventory_tools import Inventory_tools
from Sapientae_Engine.Tools.Interests_tools import Interests_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_market(Converter):
    def __init__(self, name: "Converter name", traded_item_types: list):
        # --> Initialising base class (building all ef properties)
        super().__init__(name, traded_item_types)

    def evaluate_transaction(self, bot: "Bot class instance", transaction_type, item_type, item, item_quantity):
        # ----- Performing buy transaction
        if transaction_type == "buy":

            # --> Checking whether requested item type is in the Market's inventory
            if item_type in self.inventory.keys():

                # --> Checking whether requested item is in the Market's inventory
                if item in self.inventory[item_type].keys():

                    # --> Checking whether the requested item count is available
                    if self.inventory[item_type][item] >= item_quantity:

                        # --> Check whether bot maximum/ market minimum interests match:
                        if bot.interests[item_type][item]["Maximum"] >= self.interests[item_type][item]["Minimum"]:

                            # --> Check whether bot expectation/ market expectation interests match:
                            if bot.interests[item_type][item]["Expectation"] >= self.interests[item_type][item]["Expectation"]:

                                # TODO: Setup price_per_item based on traits
                                # --> Computing price per item based on interest (meet in the middle rn)
                                price_per_item = (bot.interests[item_type][item]["Expectation"] - self.interests[item_type][item]["Expectation"])/2 + self.interests[item_type][item]["Expectation"]

                                # --> Perform transaction
                                self.perform_transaction(bot, transaction_type, item_type, item, item_quantity, price_per_item)

                                # --> Computing transaction surplus
                                market_surplus = price_per_item - self.interests[item_type][item]["Minimum"]
                                bot_surplus = bot.interests[item_type][item]["Maximum"] - price_per_item

                                # --> Increasing expectations
                                bot.interests[item_type][item]["Expectation"], self.interests[item_type][item]["Expectation"] = \
                                    Interests_tools().increase_expectation(bot.interests[item_type][item]["Expectation"], bot_surplus,
                                                                           self.interests[item_type][item]["Expectation"], market_surplus)

                            else:
                                print("Market expectation too high")

                                # --> Computing transaction shortfall
                                market_shortfall = self.interests[item_type][item]["Expectation"] - bot.interests[item_type][item]["Expectation"]
                                bot_shortfall = bot.interests[item_type][item]["Expectation"] - self.interests[item_type][item]["Expectation"]

                                # --> Decreasing expectations
                                bot.interests[item_type][item]["Expectation"], self.interests[item_type][item]["Expectation"] = \
                                    Interests_tools().decrease_expectation(bot.interests[item_type][item]["Expectation"], bot_shortfalls,
                                                                           self.interests[item_type][item]["Expectation"], market_shortfall)

                        else:
                            print("Market price too high")
                            return

                    # --> If item quantity is not available
                    else:
                        print("Requested " + item + " quantity not available (max available: "
                              + self.inventory[item_type][item] + " )")
                        return

                # --> If item is not available
                else:
                    print("Requested " + item + " not available")
                    return

            # --> If item type is not available
            else:
                print(item_type + " not tradable in this market")
                return

        # ----- Performing sell transaction
        elif transaction_type == "sell":

            # --> Checking whether item is tradable in this market
            if item_type in self.inventory.keys():

                # --> Check whether bot/market interests match:
                if bot.interests[item_type][item] <= self.interests[item_type][item]:

                    # --> Check whether bot expectation/ market expectation interests match:
                    if bot.interests[item_type][item]["Expectation"] <= self.interests[item_type][item]["Expectation"]:

                        # TODO: Setup price_per_item based on traits
                        # --> Computing price per item based on interest (meet in the middle rn)
                        price_per_item = (self.interests[item_type][item]["Expectation"] - bot.interests[item_type][item]["Expectation"]) / 2 + bot.interests[item_type][item]["Expectation"]

                        # --> Checking whether Market's Money quantity is available
                        if self.inventory["Money"] >= price_per_item * item_quantity:

                            # --> Perform transaction
                            self.perform_transaction(bot, transaction_type, item_type, item, item_quantity, price_per_item)

                            # --> Computing transaction surplus
                            market_surplus = self.interests[item_type][item]["Maximum"] - price_per_item
                            bot_surplus = price_per_item - bot.interests[item_type][item]["Minimum"]

                            # --> Increasing expectations
                            bot.interests[item_type][item]["Expectation"], self.interests[item_type][item]["Expectation"] = \
                                Interests_tools().increase_expectation(bot.interests[item_type][item]["Expectation"], bot_surplus,
                                                                       self.interests[item_type][item]["Expectation"], market_surplus)

                        else:
                            print("Market funds insufficient")
                            return

                    else:
                        print("Market expectation too low")

                        # --> Computing transaction shortfall
                        market_shortfall = bot.interests[item_type][item]["Expectation"] - self.interests[item_type][item]["Expectation"]
                        bot_shortfall = self.interests[item_type][item]["Expectation"] - bot.interests[item_type][item]["Expectation"]

                        # --> Decreasing expectations
                        bot.interests[item_type][item]["Expectation"], self.interests[item_type][item]["Expectation"] = \
                            Interests_tools().decrease_expectation(bot.interests[item_type][item]["Expectation"],
                                                                   bot_shortfalls,
                                                                   self.interests[item_type][item]["Expectation"],
                                                                   market_shortfall)

                else:
                    print("Market offer too low")
                    return

            else:
                print(item_type + " not tradable in this market")
                return

        else:
            print("Invalid transaction type")
            return

    def perform_transaction(self, bot, transaction_type, item_type, item, item_quantity, price_per_item):
        # ----- Performing buy transaction
        if transaction_type == "buy":

            # ---> Client account update
            # --> Debiting client
            bot.inventory["Money"] -= price_per_item * item_quantity

            # --> Adding item to client's inventory
            bot.inventory[item_type][item] += item_quantity

            # ---> Market account update
            # --> Crediting Market
            self.inventory["Money"] += price_per_item*item_quantity

            # --> Removing item from Market's inventory
            bot.inventory[item_type][item] -= item_quantity

            return

        # ----- Performing sell transaction
        elif transaction_type == "sell":

            # ---> Client account update
            # --> Crediting client
            bot.inventory["Money"] += price_per_item * item_quantity

            # --> removing item to client's inventory
            bot.inventory[item_type][item] -= item_quantity

            # ---> Market account update
            # --> Debiting Market
            self.inventory["Money"] -= price_per_item * item_quantity

            # --> Adding item to Market's inventory
            self.inventory[item_type][item] += item_quantity

        # ----- Clean up inventories
        inventory_tools = Inventory_tools()

        self.inventory = inventory_tools.clean_inventory(self.inventory)
        bot.inventory = inventory_tools.clean_inventory(bot.inventory)

        return

    def supply_inventory(self, item_type, item, item_quantity):
        # --> Checking whether item type is in the Market's inventory
        if item_type in self.inventory.keys():

            # --> Checking if item is already in inventory
            if item in self.inventory[item_type].keys():
                self.inventory[item_type][item] += item_quantity
                return

            else:
                self.inventory[item_type][item] = item_quantity
                return

        else:
            print(item_type + " not tradable in this market")
            return

    def clear_inventory(self, item_type, item, item_quantity):
        # --> Checking if item is in inventory
        if item in self.inventory[item_type].keys():

            # --> Checking if item quantity to be removed is in the inventory
            if self.inventory[item_type][item] >= item_quantity:
                self.inventory[item_type][item] -= item_quantity

            else:
                print("item quantity in inventory lower than quantity to be removed")
                return

        else:
            print("item not in inventory")
            return
