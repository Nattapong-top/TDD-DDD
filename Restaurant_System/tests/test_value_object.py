# Unit Tests for Restaurant_System
from idlelib.config_key import AVAILABLE_KEYS

import pytest

from Restaurant_System.domain.custom_error import PaymentNotEnough, OrderNotInMenu
from Restaurant_System.domain.domain_logic import Order, Table
from Restaurant_System.domain.value_object import (
    MenuItem, MoneyTHB, TableID, TableName, TableStatus)

def test_should_create_MenuItem_is_valid():
    menu_item = MenuItem(name='kaparwkaikidow')
    assert menu_item.name == 'kaparwkaikidow'

def test_should_raise_error_when_Menuitem_is_Empty():
    with pytest.raises(ValueError):
        menu_item = MenuItem(name='')

def test_should_raise_error_when_MenuItem_is_name_too_long():
    with pytest.raises(ValueError):
        menu_item = MenuItem(name='kaparwkaikidow'*20)

def test_should_create_MoneyTHB_is_valid():
    money_thb = MoneyTHB(amount=50.0)
    assert money_thb.amount == 50.0

def test_should_raise_error_when_MoneyTHB_is_negative():
    with pytest.raises(ValueError):
        money_thb = MoneyTHB(amount=-1)

def test_should_raise_error_when_MoneyTHB_is_more_than_1000():
    with pytest.raises(ValueError):
        money_thb = MoneyTHB(amount=1001)

def test_should_create_order_with_valid():
    order = Order(
        menu=MenuItem(name='kaparwkaikidow'),
        price=MoneyTHB(amount=50.0),
        available_menus={'kaparwkaikidow': MoneyTHB(amount=50.0)}
    )
    assert order.menu == MenuItem(name='kaparwkaikidow')
    assert order.price == MoneyTHB(amount=50.0)

def test_should_calculate_bill_order_price_50_payment_100_change_50_baht():
    menu_item = MenuItem(name='kaparwkaikidow')
    price_item = MoneyTHB(amount=50.0)
    order = Order(
        menu=menu_item,
        price=price_item,
        available_menus={'kaparwkaikidow':price_item})
    menu, change = order.calculate_bill(menu_item=MenuItem(name='kaparwkaikidow'),
                                        payment=MoneyTHB(amount=100))
    assert menu.name == 'kaparwkaikidow'
    assert change == MoneyTHB(amount=50.0)

def test_should_raise_error_when_buy_price_50_with_payment_Not_enough_10_baht():
    order = Order(
        menu=MenuItem(name='kaparwkaikidow'),
        price=MoneyTHB(amount=50.0),
        available_menus={'kaparwkaikidow':MoneyTHB(amount=50.0)}
    )
    with pytest.raises(PaymentNotEnough):
        order.calculate_bill(menu_item=MenuItem(name='kaparwkaikidow'), payment=MoneyTHB(amount=40))

def test_should_raise_error_when_order_NotInMenu():
    available_menus = {'kaparwkaikidow':70, 'ข้าวผัด':50, 'ผัดคะน้า':60}
    with pytest.raises(OrderNotInMenu):
        menu_item = MenuItem(name='ข้าวมันไก่')
        price_item = MoneyTHB(amount=50.0)
        Order(menu=menu_item, price=price_item, available_menus=available_menus)

def test_should_create_table_with_status_available():
    t_id = TableID(table_id='101')
    t_name = TableName(table_name='T101')
    table = Table(
        table_id=t_id,
        table_name=t_name,
        table_status=TableStatus.AVAILABLE
    )
    assert table.table_id == t_id
    assert table.table_name == t_name
    assert table.table_status == TableStatus.AVAILABLE


