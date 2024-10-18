from dataclasses import dataclass
from enum import Enum

class Coin(Enum):
    PENNY = .01
    NICKEL = .05
    DIME = .10
    QUARTER = .25

@dataclass
class InventoryItem:
    price: float = 0
    quantity: int = 0

class VendingMachine:


    def __init__(self):
        self.money: float = 0
        self.Inventory = {"pepsi": InventoryItem(1.50, 10), "coke": InventoryItem(1.60, 10), "tea": InventoryItem(1.25, 10)}
        self.money_supply = {Coin.QUARTER.name: 0, Coin.DIME.name: 0, Coin.NICKEL.name: 0, Coin.PENNY.name: 0}


    def get_name(self, name: str) -> str:
        if name in self.Inventory.keys():
            return name
        else:
            return "item not in inventory"

    def get_price(self, name: str) -> str:
        return self.Inventory.get(name, 'does not exist').price


    def Get_Item(self, name: str) -> str:
        return self.Inventory.get(name, 'does not exist')

    def add_coins(self, added: Coin) -> int:
        self.money += added.value
        self.money_supply[added.name] += 1
        return self.money

    def get_product(self, name: str) -> str:
        product = self.Inventory.get(name, 'does not exist')
        if self.money >= product.price:
            self.money -= product.price
            product.quantity -= 1
            return "Ok"
        else:
            return "invalid"

    def add_product(self, name: str, num_to_add: int) -> int:
        product = self.Inventory.get(name, 'does not exist')
        product.quantity += num_to_add
        return product.quantity

    def get_change(self) -> list[Coin]:
        return_val = self.money
        coins: list[Coin] = []
        while return_val > 0:
            if return_val >= .25:
                coins.append(Coin.QUARTER)
                return_val -= .25
            elif return_val >= .10:
                coins.append(Coin.DIME)
                return_val -= .10
            elif return_val >= .05:
                coins.append(Coin.NICKEL)
                return_val -= .05
            else:
                coins.append(Coin.PENNY)
                return_val -= .01
        
        return coins



    if __name__ == "__main__":
        print("\n\nHello World!\n\n")
