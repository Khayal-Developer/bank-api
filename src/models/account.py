"""
Order: 03 — Third model built

Inheritance — SavingsAccount and CheckingAccount both inherit from a base Account class
This covers: Multiple inheritance, MRO, SOLID principles.
"""

from typing import List
from money import Money
from customer import Customer
from decimal import Decimal 

class Account:
    """
    Base class for all account types
    Contains shared logic for all acounts.
    """

    def __init__(self, account_id: str, owner: Customer, balance: Money):
        if not isinstance(owner, Customer):
            raise TypeError("owner must be a Customer object")
        if not isinstance(balance, Money):
            raise TypeError("balance must be a Money object")
        if not account_id or not account_id.strip():
            raise ValueError("account_id cannot be empty")
        
        self._account_id = account_id
        self._owner = owner
        self._balance = balance
        self._transactions: List[str] = []

    @property
    def account_id(self):
        return self._account_id
        
    @property
    def owner(self):
        return self._owner
        
    @property
    def balance(self):
        return self._balance
        
    @property
    def transactions(self):
        return self._transactions
        

    def deposit(self, amount: Money) -> None:
        if not isinstance (amount, Money):
            raise TypeError("amount must be a Money object")
        if amount.currency != self._balance.currency:
            raise ValueError(
                f"Cannot deposit {amount.currency} into "
                f"{self._balance.currency} account."
            )

        if amount.amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        
        self._balance = self._balance + amount
        self._transactions.append(f"Deposit: {amount}")


    def withdraw(self, amount: Money) -> None:
        if not isinstance(amount, Money):
            raise TypeError ("amount must be a Money object")
        if amount.currency != self._balance.currency:
            raise ValueError(
                f"Cannot withdraw {amount.currency} from "
                f"{self._balance.currency} account."
            )
        
        if amount.amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount.amount > self._balance.amount:
            raise ValueError("Insufficient funds")
        
        self._balance = self._balance - amount
        self._transactions.append(f"Withdrawal: {amount}")

    
    def __str__(self):
        return(
            f"Account ID: {self._account_id} | "
            f"Owner: {self._owner.name} | "
            f"Balance: {self._balance}"
        )
    
    def __repr__(self):
        return(
            f"Account(account_id='{self._account_id}', "
            f"owner={repr(self._owner)}, "
            f"balance={repr(self._balance)}"
        )
    
class SavingsAccount(Account):
    """
    A saving account with an interest rate.
    Inherits all behaviour from Account.
    Adds: interest rate, apply interest method.
    """

    def __init__(self, account_id: str, owner: Customer,
                 balance: Money, interest_rate: float = 0.03):
        super().__init__(account_id, owner, balance)

        self._interest_rate = interest_rate
    

    @property
    def interest_rate(self):
        return self._interest_rate
    

    def apply_interest(self) -> None:
        interest = Money(
            self._balance.amount * Decimal(str(self._interest_rate)),
            self._balance.currency
        )

        self._balance = self._balance + interest
        self._transactions.append(f"Interest applied: {interest}")


    def __str__(self):
        return (
            f"SavingsAccount | {super().__str__()} | "
            f"Interest rate: {self._interest_rate * 100:.1f}%"
        )
    
class CheckingAccount(Account):
    """
    A checking account with an overdraft limit.
    Inherits all behaviour from Account
    Adds: overdraft limit
    """

    def __init__(self, account_id:str, owner:Customer,
                 balance: Money, overdraft_limit: Money):
        super().__init__(account_id, owner, balance)

        if not isinstance(overdraft_limit, Money):
            raise TypeError("overdraft_limit must be Money object")
        
        self._overdraft_limit = overdraft_limit


    @property
    def overdraft_limit(self):
        return self._overdraft_limit
    

    def withdraw(self, amount: Money) -> None:
        if not isinstance(amount, Money):
            raise TypeError("amount must be a Money object")
        if amount.currency != self._balance.currency:
            raise ValueError(
                f"Cannot withdraw {amount.currency} with "
                f"{self._balance.currency} account"
            )
        
        if amount.amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount.amount > self._balance.amount + self._overdraft_limit.amount:
            raise ValueError("Exceeds overdraft limit.")
        
        self._balance = self._balance - amount
        self._transactions.append(f"Withdrawal completed: {amount}")

    
    def __str__(self):
        return(
            f"CheckingAccount | {super().__str__()} | "
            f"Overdraft Limit: {self._overdraft_limit}"
        )
    


        




"""Documentation"""
"""
1. Inheritance concept
    - Before we write code, you need to understand inheritance.
    - The problem without inheritance:
    - Imagine you need two types of accounts:
        a. SavingsAccount — earns interest, limited withdrawals
        b. CheckingAccount — no interest, unlimited withdrawals

    - Both accounts share a lot of the same things:
        - Both have an owner
        - Both have a balance
        - Both have a transaction history
        - Both can deposit money

    - Without inheritance you'd write the same code twice.
    - If you need to fix a bug in deposit — you fix it in two places.
    - If you add a new feature — you add it in two places.
    - This violates DRY — Don't Repeat Yourself.

    - The solution — inheritance:
        - You create one base Account class with everything that is shared.
        - Then SavingsAccount and CheckingAccount inherit from it — they automatically
          get everything the base class has, and only add what makes them different.

    class Account:
        # shared code — deposit, balance, owner, history

    class SavingsAccount(Account):
        # only what's unique to savings — interest rate, withdrawal limit

    class CheckingAccount(Account):
        # only what's unique to checking — overdraft limit

    - SavingsAccount(Account) means: "SavingsAccount inherits from Account."

    - Real world analogy:
        - Account is like a general "vehicle" blueprint. SavingsAccount and CheckingAccount
          are like "car" and "truck" — they're both vehicles, they both have wheels and an
          engine, but each has unique features.


    - self._transactions: List[str] = []
        - This creates an empty list when the account is first created.
          Every deposit and withdrawal will be recorded here as a string.
          List[str] means "a list that contains only strings." 

        - Same encapsulation pattern as Customer — private attributes with
          @property for read-only access.


    - def deposit(self, amount: Money) -> None:
        - It's a return type hint. None means this method returns
          nothing — it just modifies the object. Same as hints on
          parameters — just documentation, not enforced by Python.

        
        - self._balance = self._balance + amount
            - This calls Money.__add__ — which returns a new Money object.
              So the balance gets updated with the new total.
        
        
        - self._transactions.append(f"Deposit: {amount}")
            - append adds a new item to the end of the list.
              So every deposit gets recorded as a string like
              "Deposit: USD 100.00" in the transaction history.
"""