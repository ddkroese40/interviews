from py_check.main import VendingMachine, Coin, MoneySupply
import pytest
import os

@pytest.fixture
def machine():
    return VendingMachine()

def test_GetPepsiName(machine):
    assert machine.GetName("pepsi") == "pepsi"


def test_GetDummyName(machine):
    assert machine.GetName("dummy") == "item not in inventory"


def test_GetCokeName(machine):
    assert machine.GetName("coke") == "coke"


def test_GetTeaName(machine):
    assert machine.GetName("tea") == "tea"


def test_GetPepsiPrice(machine):
    assert machine.GetPrice("pepsi") == 150


def test_GetCokePrice(machine):
    assert machine.GetPrice("coke") == 160


def test_GetTeaPrice(machine):
    assert machine.GetPrice("tea") == 125


def test_PurchaseProduct(machine):
    assert machine.GetProduct("tea") == "insufficent funds"
    for _ in range(5):
        machine.AddCoin(Coin.QUARTER)
    assert machine.money == 125
    assert machine.GetProduct("tea") == "Ok"
    assert machine.GetProduct("tea") == "insufficent funds"


def test_ProductQuantityAfterPurchase(machine):
    assert machine.GetProduct("tea") == "insufficent funds"
    for _ in range(5):
        machine.AddCoin(Coin.QUARTER)
    assert machine.GetProduct("tea") == "Ok"
    assert machine.GetItem("tea").quantity == 9


def test_AddCoin(machine):
    assert machine.money == 0
    assert machine.money_supply.coins[Coin.QUARTER.name] == 20
    assert machine.money_supply.coins[Coin.DIME.name] == 20
    assert machine.AddCoin(Coin.QUARTER) == 25
    assert machine.money_supply.coins[Coin.QUARTER.name] == 21
    assert machine.AddCoin(Coin.DIME) == 35
    assert machine.money_supply.coins[Coin.DIME.name] == 21
    assert machine.money_supply.coins[Coin.QUARTER.name] == 21

def test_AddCoins(machine):
    added_money = MoneySupply()
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.DIME)
    
    assert machine.money_supply.coins[Coin.QUARTER.name] == 20
    assert machine.money_supply.coins[Coin.DIME.name] == 20
    assert machine.money == 0

    machine.AddCoins(added_money)

    assert machine.money_supply.coins[Coin.QUARTER.name] == 22
    assert machine.money_supply.coins[Coin.DIME.name] == 21
    assert machine.money == 60


def test_AddCoinsToStockDoesNotEffectMoney(machine):
    added_money = MoneySupply()
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.DIME)
    
    assert machine.money_supply.coins[Coin.QUARTER.name] == 20
    assert machine.money_supply.coins[Coin.DIME.name] == 20
    assert machine.money == 0
    
    #incorrect password
    machine.AddCoinsToStock(added_money, "PopnCaffeineAndSugar")
    assert machine.money_supply.coins[Coin.QUARTER.name] == 20
    assert machine.money_supply.coins[Coin.DIME.name] == 20
    
    #correct pass
    machine.AddCoinsToStock(added_money, "PopGoesTheWeasel")

    assert machine.money_supply.coins[Coin.QUARTER.name] == 22
    assert machine.money_supply.coins[Coin.DIME.name] == 21
    assert machine.money == 0


def test_RemoveCoinsFromStockDoesNotEffectMoney(machine):
    added_money = MoneySupply()
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.DIME)

    machine.money = 100
    
    assert machine.money_supply.coins[Coin.QUARTER.name] == 20
    assert machine.money_supply.coins[Coin.DIME.name] == 20
    assert machine.money == 100

    #incorrect password
    machine.RemoveCoinsFromStock(added_money, "PopnCaffeineAndSugar")
    assert machine.money_supply.coins[Coin.QUARTER.name] == 20
    assert machine.money_supply.coins[Coin.DIME.name] == 20
    
    #correct pass
    machine.RemoveCoinsFromStock(added_money, "PopGoesTheWeasel")

    assert machine.money_supply.coins[Coin.QUARTER.name] == 18
    assert machine.money_supply.coins[Coin.DIME.name] == 19
    assert machine.money == 100


def test_AddProduct(machine):
    assert machine.GetItem("tea").quantity == 10
    assert machine.AddProduct("pepsi", 5, "PopGoesTheWeasel") == 15
    #incorrect Password doesn't add
    assert machine.AddProduct("tea", 5, "PopnCaffeineAndSugar") == 10


def test_AddNewProduct(machine):
    #adding New products creates a new dictionary lookup with that product key
    assert machine.AddProduct("gatorade", 5, "PopGoesTheWeasel") == 5


def test_GetChange(machine):
    assert machine.GetChange().coins == {Coin.QUARTER.name: 0, Coin.DIME.name: 0, Coin.NICKEL.name: 0, Coin.PENNY.name: 0}
    
    # Add coins and test correct change is returned
    added_money = MoneySupply()
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.DIME)
    added_money.AddCoin(Coin.NICKEL)
    added_money.AddCoin(Coin.PENNY)
    added_money.AddCoin(Coin.PENNY)
    
    machine.AddCoins(added_money)

    change = machine.GetChange()
    assert change.coins[Coin.QUARTER.name] == 1
    assert change.coins[Coin.DIME.name] == 1
    assert change.coins[Coin.NICKEL.name] == 1
    assert change.coins[Coin.PENNY.name] == 2

    # Check that money supply is reduced accordingly
    assert machine.money_supply.coins[Coin.QUARTER.name] == 20
    assert machine.money_supply.coins[Coin.DIME.name] == 20
    assert machine.money_supply.coins[Coin.NICKEL.name] == 20
    assert machine.money_supply.coins[Coin.PENNY.name] == 20


def test_GetChangeCalcs(machine):
    
    # Add specific coins using AddCoins
    added_money = MoneySupply()
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.DIME)
    added_money.AddCoin(Coin.DIME)
    added_money.AddCoin(Coin.NICKEL)

    machine.AddCoins(added_money)

    # Get change and ensure it returns the correct coins
    change = machine.GetChange()
    
    assert change.coins[Coin.QUARTER.name] == 2
    assert change.coins[Coin.DIME.name] == 0
    assert change.coins[Coin.NICKEL.name] == 0

    # Check that money supply is updated correctly
    assert machine.money_supply.coins[Coin.QUARTER.name] == 19
    assert machine.money_supply.coins[Coin.DIME.name] == 22
    assert machine.money_supply.coins[Coin.NICKEL.name] == 21


def test_DispenseProduct(machine):
    # Purchase a product
    added_money = MoneySupply()
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)

    machine.AddCoins(added_money)
    assert machine.GetProduct("tea") == "Ok"  # Purchase should be valid
    assert len(machine.purchase_history["tea"]) == 1
    assert len(machine.purchase_history["pepsi"]) == 0
    assert len(machine.purchase_history["coke"]) == 0

    # Purchase again
    machine.AddCoins(added_money)
    assert machine.GetProduct("tea") == "Ok"
    assert len(machine.purchase_history["tea"]) == 2
    assert len(machine.purchase_history["pepsi"]) == 0
    assert len(machine.purchase_history["coke"]) == 0

    # Purchase a different product
    machine.AddCoins(added_money)
    assert machine.GetProduct("pepsi") == "insufficent funds"
    machine.AddCoin(Coin.QUARTER)  # Add 25 cents
    assert machine.GetProduct("pepsi") == "Ok"
    assert len(machine.purchase_history["tea"]) == 2
    assert len(machine.purchase_history["pepsi"]) == 1
    assert len(machine.purchase_history["coke"]) == 0


def test_ChangePrice(machine):
    # Initially check the price of an existing product
    original_price = machine.GetPrice("tea")
    
    # Change the price with the correct password
    new_price = 150
    assert machine.GetPrice("tea") != new_price  # Check that the price has been updated
    assert machine.ChangePrice("tea", new_price, "PopGoesTheWeasel") == new_price
    assert machine.GetPrice("tea") == new_price  # Check that the price has been updated

    # Try to change the price with an incorrect password
    incorrect_password = "WrongPassword"
    assert machine.ChangePrice("tea", 200, incorrect_password) is None  # Assuming the method returns None on failure
    assert machine.GetPrice("tea") == new_price  # Price should remain unchanged

    # Change the price of a non-existing product
    assert machine.ChangePrice("food", 300, "PopGoesTheWeasel") is None


def test_ChangePassword(machine):
    #first check price works
    new_price = 200
    old = "PopGoesTheWeasel"
    new = "newPass"
    assert machine.ChangePrice("tea", new_price, old) == new_price
    new_price = 125
    machine.ChangePass(new, old)
    assert machine.ChangePrice("tea", new_price, old) != new_price
    assert machine.ChangePrice("tea", new_price, new) == new_price
    
def test_GeneratePurchaseReport(machine):
    # Adding some purchases to the machine
    added_money = MoneySupply()
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)
    added_money.AddCoin(Coin.QUARTER)
    machine.AddCoins(added_money)
    machine.GetProduct("tea")  # Purchase tea

    machine.AddCoins(added_money)
    machine.GetProduct("tea")  # Purchase tea

    machine.AddCoins(added_money)
    machine.AddCoin(Coin.QUARTER)
    machine.GetProduct("pepsi")  # Purchase tea
    # Generate report
    report_filename = 'test_purchase_history_report.txt'
    machine.GeneratePurchaseReport(report_filename, "PopGoesTheWeasel")

    # Verify report file exists and check its content
    assert os.path.exists(report_filename)

    with open(report_filename, 'r') as file:
        content = file.read()
        assert "Product: tea" in content  # Check that the product is listed
        assert "Product: pepsi" in content  # Check that the product is listed
        assert "Product: coke" not in content  # Check that the product is not listed
        assert "Purchased at:" in content  # Check that purchase time is recorded

    #validate can't generate report with incorrect password
    machine.GeneratePurchaseReport("New_report", "wrongPass")
    assert not os.path.exists("New_report")



