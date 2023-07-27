import pytest
from app.calculations import *

# @pytest.mark.parametrize call one test case multiple times with different parameters
@pytest.mark.parametrize("num1, num2, expected", [(3,2,5),(7,5,12),(1,2,3) ])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_substract():
    assert substract(4, 1) == 3

def test_mnultiply():
    assert multiply(4, 1) == 4

def test_divide():
    assert divide(4, 1) == 4

# @pytest.fixture define a funtions that get called before running a test case
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_default_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_bank_default_deposite(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_bank_default_collet_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposite, withdraw, expected", [(200,100,100),(50,10,40),(800,100,700)])
def test_bank_transaction(zero_bank_account, deposite, withdraw, expected):
    zero_bank_account.deposit(deposite)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

# Exception handling
def test_insufficient(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)