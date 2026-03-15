# Unit Tests for Restaurant_System
from idlelib.config_key import AVAILABLE_KEYS

import pytest

from Restaurant_System.domain.custom_error import (
    PaymentNotEnough, OrderNotInMenu, TableAlreadyOccupiedError)
from Restaurant_System.domain.domain_logic import (
    Order, Table, Customer)
from Restaurant_System.domain.value_object import (
    MenuItem, MoneyTHB, TableID, TableName, TableStatus, CustomerID, CustomerName, CustomerPhoneNumber)

@pytest.fixture
def customer():
    return Customer(
        customer_id=CustomerID(customer_id='123'),
        customer_name=CustomerName(first_name='nattapong',
                                   last_name='developer'),
        customer_phone_number=CustomerPhoneNumber(phone_number='0984572874')
    )

@pytest.fixture
def table():
    return Table(
        table_id=TableID(table_id='101'),
        table_name=TableName(table_name='T101'),
    )

@pytest.fixture
def order():
    return Order(
        menu=MenuItem(name='ข้าวผัด'),
        available_menus={'ข้าวผัด': MoneyTHB(amount=50.0)}
    )


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
    menu, change = order.calculate_bill(
        menu_item=MenuItem(name='kaparwkaikidow'),
        payment=MoneyTHB(amount=100)
    )
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


def test_should_raise_error_when_table_status_is_invalid():
    t_id = TableID(table_id='101')
    t_name = TableName(table_name='T101')
    with pytest.raises(ValueError):
        Table(
            table_id=t_id,
            table_name=t_name,
            table_status='table_status'
        )
def test_should_assign_order_to_table_and_change_status_occupied():
    table = Table(
        table_id=TableID(table_id='101'),
        table_name=TableName(table_name='T101'),
        table_status=TableStatus.AVAILABLE
    )
    order = Order(
        menu=MenuItem(name='ข้าวผัด'),
        price=MoneyTHB(amount=50.0),
        available_menus={'ข้าวผัด':MoneyTHB(amount=50.0)}
    )
    new_table = table.assign_order(order)

    assert new_table.table_id == TableID(table_id='101')
    assert new_table.table_status == TableStatus.OCCUPIED
    assert new_table.order == order

def test_should_raise_error_when_table_is_already_occupied():
    table = Table(
        table_id=TableID(table_id='101'),
        table_name=TableName(table_name='T101'),
    )
    order = Order(
        menu=MenuItem(name='ข้าวผัด'),
        price=MoneyTHB(amount=50.0),
        available_menus={'ข้าวผัด':MoneyTHB(amount=50.0)}
    )
    new_table = table.assign_order(order)

    with pytest.raises(TableAlreadyOccupiedError):
        new_table.assign_order(order)

def test_should_clear_order_from_table_and_change_status_available():
    menu_item = MenuItem(name='ข้าวผัด')
    price_item = MoneyTHB(amount=50.0)
    table = Table(
        table_id=TableID(table_id='101'),
        table_name=TableName(table_name='T101'),
    )
    order = Order(
        menu=menu_item,
        price=price_item,
        available_menus={'ข้าวผัด':MoneyTHB(amount=50.0)}
    )
    new_table = table.assign_order(order)
    new_table = new_table.clear_order()

    assert new_table.table_id == TableID(table_id='101')
    assert new_table.table_status == TableStatus.AVAILABLE

def test_should_calculate_bill_from_table_price_50_payment_100_change_50_bath():
    menu_item = MenuItem(name='ข้าวผัด')
    order = Order(
        menu = menu_item,
        price = MoneyTHB(amount=50.0),
        available_menus={'ข้าวผัด':MoneyTHB(amount=50.0)}
    )
    new_table = Table(
        table_id=TableID(table_id='101'),
        table_name=TableName(table_name='T101'),
    )
    new_table = new_table.assign_order(order)

    menu, change = new_table.order.calculate_bill(menu_item=menu_item, payment=MoneyTHB(amount=100))
    assert change == MoneyTHB(amount=50.0)
    assert menu == menu_item
    assert new_table.table_id == TableID(table_id='101')

def test_should_get_price_from_available_menus():
    order = Order(
        menu=MenuItem(name='ข้าวผัด'),
        available_menus={'ข้าวผัด': MoneyTHB(amount=50.0)}
    )
    assert order.price == MoneyTHB(amount=50.0)

def test_should_create_customer_id_with_vo_valid():
    customer_id = CustomerID(customer_id='123')
    assert customer_id.customer_id == '123'

def test_should_create_customer_name_lastname_valid():
    name = 'nattapong'
    last = 'developer'
    customer_name = CustomerName(
        first_name=name,
        last_name=last,)
    assert customer_name.first_name == name
    assert customer_name.last_name == last

def test_should_create_customer_phone_number_valid():
    phone_number = '0981234583'
    customer_phone_number = CustomerPhoneNumber(
        phone_number=phone_number,
    )
    assert customer_phone_number.phone_number == phone_number

def test_should_raise_error_customer_phone_number_invalid():
    phone_number = '094357683i'
    with pytest.raises(ValueError):
        CustomerPhoneNumber(
        phone_number=phone_number,
    )

def test_should_create_customer_valid():
    name = 'nattapong'
    last = 'developer'
    phone_number = '0981234583'
    customer = Customer(
        customer_id=CustomerID(customer_id='123'),
        customer_name=CustomerName(
            first_name=name,
            last_name=last),
        customer_phone_number=CustomerPhoneNumber(
            phone_number=phone_number)
    )
    assert customer.customer_id == CustomerID(customer_id='123')
    assert customer.customer_name == CustomerName(
        first_name=name,
        last_name=last)
    assert customer.customer_phone_number == CustomerPhoneNumber(
        phone_number=phone_number)

def test_should_assign_customer_to_table():
    customer = Customer(
        customer_id=CustomerID(customer_id='123'),
        customer_name=CustomerName(
            first_name='nattapong',
            last_name='developer'),
        customer_phone_number=CustomerPhoneNumber(
            phone_number='0981234583')
    )
    table = Table(
        table_id=TableID(table_id='101'),
        table_name=TableName(table_name='T101'),
    )
    new_table = table.assign_customer(customer)
    assert new_table.customer == customer
    assert new_table.table_status == TableStatus.OCCUPIED
    assert new_table.table_id == TableID(table_id='101')


def test_should_assign_order_after_customer_seated(customer, table, order):
    new_table = table.assign_customer(customer)
    new_table = new_table.assign_order(order)

    assert new_table.customer == customer
    assert new_table.table_status == TableStatus.OCCUPIED
    assert new_table.table_id == TableID(table_id='101')
    assert new_table.order == order
