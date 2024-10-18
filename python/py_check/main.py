import time
import os
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
from datetime import datetime


class Coin(Enum):
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUARTER = 25

class MoneySupply:
    def __init__(self):
        self.coins = {
            Coin.QUARTER.name: 0,
            Coin.DIME.name: 0,
            Coin.NICKEL.name: 0,
            Coin.PENNY.name: 0
        }

    def AddCoin(self, coin: Coin) -> int:
        self.coins[coin.name] += 1
        return coin.value


    def RemoveCoin(self, coin: Coin) -> int:
        if self.coins[coin.name] > 0:
            self.coins[coin.name] -= 1
            return coin.value
        return 0
    

    def AddCoins(self, added_money) -> int:
        total = 0
        for coin_name, count in added_money.coins.items():
            for _ in range(count):
                total += self.AddCoin(Coin[coin_name])
        return total


    def RemoveCoins(self, removed_money) -> int:
        total = 0
        for coin_name, count in removed_money.coins.items():
            for _ in range(count):
                total += self.RemoveCoin(Coin[coin_name])
        return total


    def __repr__(self):
        return str(self.coins)

@dataclass
class InventoryItem:
    price: int  # Change to int to represent cents
    quantity: int

class VendingMachine:
    def __init__(self):
        self.money: int = 0  # Change to int for cents
        self.inventory = {
            "pepsi": InventoryItem(150, 10),
            "coke": InventoryItem(160, 10),
            "tea": InventoryItem(125, 10)
        }
        self.money_supply = MoneySupply()
        self.purchase_history = defaultdict(list)
        self.password = "PopGoesTheWeasel"
        for coin in Coin:
            self.money_supply.coins[coin.name] = 20

    def GetName(self, name: str) -> str:
        return name if name in self.inventory else "item not in inventory"

    def GetPrice(self, name: str) -> int:  # Change to int for cents
        return self.inventory.get(name, InventoryItem(0, 0)).price

    def GetItem(self, name: str) -> InventoryItem:
        return self.inventory.get(name, InventoryItem(0, 0))

    def AddCoin(self, coin: Coin) -> int:
        self.money += coin.value
        self.money_supply.AddCoin(coin)
        return self.money

    def AddCoins(self, added_money: MoneySupply) -> None:
        self.money += self.money_supply.AddCoins(added_money)
    

    def DispenseProduct(self, name: str) -> None:
        """Track the purchase of a product by adding a timestamp to the history."""
        purchase_time = time.time()
        self.purchase_history[name].append(purchase_time)
        readable_time = datetime.fromtimestamp(purchase_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{name} purchased at {readable_time}")

    
    def GetProduct(self, name: str) -> str:
        product = self.inventory.get(name)
        if product is None:
            return "item not in inventory"

        if self.money >= product.price and product.quantity > 0:
            self.money -= product.price
            product.quantity -= 1
            self.DispenseProduct(name)
            return "Ok"
        return "insufficent funds"


    def GetChange(self) -> MoneySupply:
        return_val = self.money
        change_supply = MoneySupply()

        def update_change(coin: Coin) -> int:
            change_supply.AddCoin(coin)
            self.money_supply.RemoveCoin(coin)
            return coin.value

        while return_val > 0:
            if return_val >= Coin.QUARTER.value and self.money_supply.coins[Coin.QUARTER.name] > 0:
                return_val -= update_change(Coin.QUARTER)
            elif return_val >= Coin.DIME.value and self.money_supply.coins[Coin.DIME.name] > 0:
                return_val -= update_change(Coin.DIME)
            elif return_val >= Coin.NICKEL.value and self.money_supply.coins[Coin.NICKEL.name] > 0:
                return_val -= update_change(Coin.NICKEL)
            elif return_val >= Coin.PENNY.value and self.money_supply.coins[Coin.PENNY.name] > 0:
                return_val -= update_change(Coin.PENNY)

        return change_supply


    #admin features
    def AddCoinsToStock(self, added_money: MoneySupply, password: str) -> None:
        if password == self.password:
            _ = self.money_supply.AddCoins(added_money)
        else:
            print("incorrect Password")

    def RemoveCoinsFromStock(self, added_money: MoneySupply, password: str) -> None:
        if password == self.password:
            _ = self.money_supply.RemoveCoins(added_money)
        else:
            print("incorrect Password")

    
    def AddProduct(self, name: str, num_to_add: int, password: str) -> int:
        if password == self.password:
            if name in self.inventory:
                # If product exists, update the quantity
                product = self.inventory[name]
                product.quantity += num_to_add
            else:
                # If product does not exist, create a new product
                self.inventory[name] = InventoryItem(price=100, quantity=num_to_add)  # Set a default price of 0.0 or another appropriate value
                print("added ", name, " to inventory with a default price of 1.00")
        return self.inventory[name].quantity

    def ChangePrice(self, name: str, price: int, password: str) -> int:
        if password == self.password and name in self.inventory:
            old_price = self.inventory[name].price
            self.inventory[name].price = price
            print("set new price to: ", price, "from: ", old_price)
            return price


    def ChangePass(self, new_pass: str, password: str):
        if password == self.password:
            self.password = new_pass


    def GeneratePurchaseReport(self, filename: str, password: str) -> None:

        if password != self.password:
            return
        """Generates a report of all purchase history in a text file."""
        with open(filename, 'w') as file:
            for product_name, timestamps in self.purchase_history.items():
                file.write(f"Product: {product_name}\n")
                if timestamps:  # Check if there are any timestamps
                    for timestamp in timestamps:
                        readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
                        file.write(f"  Purchased at: {readable_time}\n")
                else:
                    file.write("  No purchases recorded.\n")
                file.write("\n")  # Add an empty line between products

        print(f"Report generated: {filename}")

if __name__ == "__main__":
    machine = VendingMachine()
    print("Using the machine...\n")
