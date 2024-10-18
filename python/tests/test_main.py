from py_check.main import VendingMachine, Coin
import pytest


def test_get_pepsi_name():
    machine = VendingMachine()
    assert machine.get_name("pepsi") == "pepsi"

def test_get_dummy_name():
    machine = VendingMachine()
    assert machine.get_name("dummy") == "item not in inventory"


def test_get_coke_name():
    machine = VendingMachine()
    assert machine.get_name("coke") == "coke"

def test_get_tea_name():
    machine = VendingMachine()
    assert machine.get_name("tea") == "tea"

def test_get_pepsi_price():
    machine = VendingMachine()
    assert machine.get_price("pepsi") == 1.50


def test_get_coke_price():
    machine = VendingMachine()
    assert machine.get_price("coke") == 1.60


def test_get_tea_price():
    machine = VendingMachine()
    assert machine.get_price("tea") == 1.25

def test_PurchaseProdect():
    machine = VendingMachine()
    assert machine.get_product("tea") == "invalid"
    for _ in range(5):
        machine.add_coins(Coin.QUARTER)
    assert machine.money == 1.25
    assert machine.get_product("tea") == "Ok"
    assert machine.get_product("tea") == "invalid"


def test_PurchaseProdect():
    machine = VendingMachine()
    assert machine.get_product("tea") == "invalid"
    for _ in range(5):
        machine.add_coins(Coin.QUARTER)
    assert machine.get_product("tea") == "Ok"
    assert machine.Get_Item("tea").quantity == 9


def test_add_coin():
    machine = VendingMachine()
    assert machine.money == 0
    assert machine.money_supply[Coin.QUARTER.name] == 0
    assert machine.add_coins(Coin.QUARTER) == .25
    assert machine.money_supply[Coin.QUARTER.name] == 1
    assert machine.add_coins(Coin.DIME) == .35

    assert machine.money_supply[Coin.DIME.name] == 1


def test_addProduct():
    machine = VendingMachine()
    assert machine.Get_Item("tea").quantity == 10
    assert machine.add_product("pepsi", 5) == 15

def test_getNoChange():
    machine = VendingMachine()
    assert machine.get_change() == []
    assert machine.add_coins(Coin.QUARTER) == .25
    assert machine.get_change() == [Coin.QUARTER]


# def test_checkChangeReturned():
#     machine = VendingMachine()
#     assert machine.get_product("coke") == "invalid"
#     for _ in range(7):
#         machine.add_coins(Coin.QUARTER)
#     assert machine.get_product("tea") == "Ok"



