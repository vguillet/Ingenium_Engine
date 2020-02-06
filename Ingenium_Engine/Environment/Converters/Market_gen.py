
################################################################################################################
"""
A converter sub-class specialising in exchanging items for money (both selling and buying)
"""

# Built-in/Generic Imports

# Libs

# Own modules
from Ingenium_Engine.Environment.Converters.Converter_gen import Converter
from Ingenium_Engine.Tools.Transaction_gen import gen_transaction
from Ingenium_Engine.Tools.Inventory_tools import Inventory_tools
from Ingenium_Engine.Tools.Interests_tools import Interests_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_market(Converter):
    def __init__(self, name: "Converter name", pos: tuple, traded_item_types: list):
        # --> Initialising base class (building all ref properties)
        super().__init__(name, pos)

        # --> Setup market inventory
        self.inventory = Inventory_tools().gen_market_inventory_dict(traded_item_types)

        # --> Setup market interests
        self.interests = Interests_tools().gen_market_interests_dict(traded_item_types)

        # --> Initialising records
        self.transaction_records = []

    def __str__(self):
        return self.name + " (Market-type converter)"

    def __repr__(self):
        return self.__str__()

    def evaluate_transaction(self, date, bot: "Bot class instance", transaction_type, item_type, item, item_quantity):
        interests_tools = Interests_tools()

        print("Transaction request recap:")
        print("Bot trading:", bot.name)

        print("(Bot price) " + str(bot.interests[item_type][item]["Expectation"]) + " - " + str(self.interests[item_type][item]["Expectation"]) + " (Market price)")
        print("(Quantity available) "  + str(self.inventory[item_type][item]) + " - " + str(item_quantity) + " (Quantity requested)\n")

        # ----- Performing buy transaction
        if transaction_type == "buy":

            # --> Checking whether requested item type is in the Market's inventory
            if item_type in self.inventory.keys():

                # --> Checking whether requested item is in the Market's inventory
                if item in self.inventory[item_type].keys():

                    # --> Checking whether the requested item count is available
                    if self.inventory[item_type][item] >= item_quantity:

                        # --> Check whether bot expectation/ market expectation interests match:
                        if bot.interests[item_type][item]["Expectation"] >= self.interests[item_type][item]["Expectation"]:

                            # TODO: Setup price_per_item based on traits
                            # --> Computing price per item based on interest (meet in the middle rn)
                            price_per_item = (bot.interests[item_type][item]["Expectation"] - self.interests[item_type][item]["Expectation"])/2 + self.interests[item_type][item]["Expectation"]

                            # --> Perform transaction
                            self.perform_transaction(date, bot, transaction_type, item_type, item, item_quantity, price_per_item)

                            # --> Computing transaction surplus
                            market_surplus = price_per_item - self.interests[item_type][item]["Minimum"]
                            bot_surplus = bot.interests[item_type][item]["Maximum"] - price_per_item

                            # --> Increasing market expectations
                            self.interests[item_type][item] = interests_tools.increase_expectation(
                                self.interests[item_type][item], market_surplus)

                            # --> Decreasing bot expectations
                            bot.interests[item_type][item] = interests_tools.decrease_expectation(
                                bot.interests[item_type][item], bot_surplus)

                            print("Transaction succesfull, " + str(item_quantity) + " units of " + str(item) + " " + str(item_type) + " brought at " + str(price_per_item) + "$ per unit")
                            return

                        else:
                            print("Market expectation too high")

                            # --> Computing transaction shortfall
                            market_shortfall = self.interests[item_type][item]["Expectation"] - bot.interests[item_type][item]["Expectation"]
                            bot_shortfall = bot.interests[item_type][item]["Expectation"] - self.interests[item_type][item]["Expectation"]

                            # --> Decreasing market expectations
                            self.interests[item_type][item] = interests_tools.decrease_expectation(
                                self.interests[item_type][item], market_shortfall)

                            # --> Increasing bot expectations
                            bot.interests[item_type][item] = interests_tools.increase_expectation(
                                bot.interests[item_type][item], bot_shortfall)


                    # --> If item count is not available
                    else:
                        # --> Increasing market expectations
                        self.interests[item_type][item] = interests_tools.increase_expectation(self.interests[item_type][item],
                                                                                                             setting=1)

                        # --> Increasing bot expectations
                        bot.interests[item_type][item] = interests_tools.increase_expectation(bot.interests[item_type][item],
                                                                                                             setting=1)

                        print("Requested " + item + " quantity not available (max available: " + str(self.inventory[item_type][item]) + " )")
                        return

                # --> If item is not available
                else:
                    # --> Increasing market expectations
                    self.interests[item_type][item] = interests_tools.increase_expectation(self.interests[item_type][item],
                                                                                                          setting=1)

                    # --> Increasing bot expectations
                    bot.interests[item_type][item] = interests_tools.increase_expectation(bot.interests[item_type][item],
                                                                                                         setting=1)

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

                # --> Checking whether the requested item count is available
                if bot.inventory[item_type][item] >= item_quantity:

                    # --> Check whether bot expectation/ market expectation interests match:
                    if bot.interests[item_type][item]["Expectation"] <= self.interests[item_type][item]["Expectation"]:

                        # TODO: Setup price_per_item based on traits
                        # --> Computing price per item based on interest (meet in the middle rn)
                        price_per_item = (self.interests[item_type][item]["Expectation"] - bot.interests[item_type][item]["Expectation"]) / 2 + bot.interests[item_type][item]["Expectation"]

                        # --> Checking whether Market's Money quantity is available
                        if self.inventory["Money"] >= price_per_item * item_quantity:

                            # --> Perform transaction
                            self.perform_transaction(date, bot, transaction_type, item_type, item, item_quantity, price_per_item)

                            # --> Computing transaction surplus
                            market_surplus = self.interests[item_type][item]["Maximum"] - price_per_item
                            bot_surplus = price_per_item - bot.interests[item_type][item]["Minimum"]

                            # --> Decreasing market expectations
                            self.interests[item_type][item] = interests_tools.decrease_expectation(
                                self.interests[item_type][item], market_surplus)

                            # --> Increasing bot expectations
                            bot.interests[item_type][item] = interests_tools.increase_expectation(
                                bot.interests[item_type][item], bot_surplus)

                            print("Transaction succesfull, " + str(item_quantity) + " units of " + str(item) + " " + str(item_type) + " sold at " + str(price_per_item) + "$ per unit")
                            return

                        else:
                            print("Market funds insufficient")
                            return

                    else:
                        print("Market expectation too low")

                        # --> Computing transaction shortfall
                        market_shortfall = bot.interests[item_type][item]["Expectation"] - self.interests[item_type][item]["Expectation"]
                        bot_shortfall = self.interests[item_type][item]["Expectation"] - bot.interests[item_type][item]["Expectation"]

                        # --> Increasing market expectations
                        self.interests[item_type][item] = interests_tools.increase_expectation(
                            self.interests[item_type][item], market_surplus)

                        # --> Decreasing bot expectations
                        bot.interests[item_type][item] = interests_tools.decrease_expectation(
                            bot.interests[item_type][item], bot_surplus)

                else:
                    print("Requested " + item + " quantity not available (max available: " + str(bot.inventory[item_type][item]) + " )")

            else:
                print(item_type + " not tradable in this market")
                return

        else:
            print("Invalid transaction type")
            return

    def perform_transaction(self, date, bot, transaction_type, item_type, item, item_quantity, price_per_item):
        self.transaction_records.append(gen_transaction(date, transaction_type, item_type, item, item_quantity, price_per_item))

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
            self.inventory[item_type][item] -= item_quantity

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


if __name__ == "__main__":
    market = gen_market("Rosestones", (0, 0), "")
    print(market)
    market
