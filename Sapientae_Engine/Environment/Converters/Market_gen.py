
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Sapientae_Engine.Environment.Converters.Converter_gen import Converter

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Market(Converter):
    def __init__(self, name: "Converter name", input: "Resource type list", output: "Resource type list"):
        # --> Initialising base class
        super().__init__(name, input, output)

    def perform_trade(self, client_inventory, transaction_type, product_type, product, product_quantity, price_per_resource):

        # ----- Performing buy transaction
        if transaction_type == "buy":

            # TODO: Develop market for other product categories
            # --> Checking whether requested product is in the Market's inventory
            if product in self.inventory[product_type].keys():

                # --> Checking whether the requested product count is available
                if self.inventory[product_type][product] >= product_quantity:

                    # ---> Client account update
                    # --> Debiting client
                    client_inventory["Money"] -= price_per_resource * product_quantity

                    # --> Adding product to client's inventory
                    client_inventory[product_type][product] += product_quantity

                    # ---> Market account update
                    # --> Crediting Market
                    self.inventory["Money"] += price_per_resource*product_quantity

                    # --> Removing product from Market's inventory
                    client_inventory[product_type][product] -= product_quantity

                # --> If product quantity is not available
                else:
                    print("Requested " + product + " quantity not available (max available: "
                          + self.inventory[product_type][product] + " )")
                    return client_inventory

            # --> If product is not available
            else:
                print("Requested " + product + " not available")
                return client_inventory

        # ----- Performing sell transaction
        if transaction_type == "sell":

            # --> Checking whether Market's Money quantity is available
            if self.inventory["Money"] >= price_per_resource * product_quantity:
                # ---> Client account update
                # --> Crediting client
                client_inventory["Money"] += price_per_resource * product_quantity

                # --> removing product to client's inventory
                client_inventory[product_type][product] -= product_quantity

                # ---> Market account update
                # --> Debiting Market
                self.inventory["Money"] -= price_per_resource * product_quantity

                # --> Adding product to Market's inventory
                self.inventory[product_type][product] += product_quantity

            else:
                print("Market funds insufficient")
                return client_inventory

        return client_inventory

