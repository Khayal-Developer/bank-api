"""
Money class for representing monetary amounts with currency.
Uses Decimal for exact arithmetic - never float.
"""
from decimal import Decimal
from typing import Union

ALLOWED_CURRENCIES = frozenset({"USD", "EUR", "AZN", "TRY", "GBP"})

"""
What is frozenset?
A regular set is mutable — you can add or remove items. 
frozenset is immutable — it can never be changed after creation.
Perfect for a fixed list of currencies that should never be modified at runtime.
"""

"""
What is Union[str, int, Decimal]?
It means "this parameter can be a string, int, or Decimal."
We'll use it in __init__. It comes from Python's typing module.
"""

class CurrencyMismatchError(Exception):
    """Raised when operating on Money objects with different currencies."""
    pass

class InvalidCurrencyError(Exception):
    """Raised when an unknown currency is used."""
    pass

"""
These are custom exceptions.
Python has built-in exceptions like ValueError, TypeError.
But in a banking system you want specific, meaningful errors.

When someone tries to add USD + EUR — that's not a ValueError.
That's a CurrencyMismatchError. Much clearer.

class CurrencyMismatchError(Exception) means:
"create a new exception type that inherits from Python's built-in Exception."
The pass means the class has no extra logic — just the name is enough.

In the interview if they ask "did you use custom exceptions?" — you say yes and point here.
"""

class Money:
    """
    Represents a monetary amount in a specific currency.
    Operations return new Money objects - original is never modified.
    """

    def __init__(self, amount: Union[str, int, Decimal], currency: str):
        if currency not in ALLOWED_CURRENCIES:
            raise InvalidCurrencyError(
                f"Currency: '{currency}' is not supported. "
                f"Allowed: {ALLOWED_CURRENCIES}"   
            )
        
        self.amount = Decimal(str(amount))
        self.currency = currency
    
    """
    What's happening here:
    if currency not in ALLOWED_CURRENCIES — before storing anything,
    we check if the currency is valid.
    If someone passes "XYZ" we raise InvalidCurrencyError immediately.

    Decimal(str(amount)) — we convert amount to string first, then to Decimal.
    This handles all three cases safely:
        - If someone passes "100.50" (string) → Decimal("100.50")
        - If someone passes 100 (int) → str(100) → "100" → Decimal("100")
        - If someone passes Decimal("100.50") → str(Decimal("100.50")) → "100.50" → Decimal("100.50")
    """

    def __str__(self):
        return f"{self.currency} {self.amount:.2f}"
    
    """
    What :.2f means: It formats the number to always show 2 decimal places.
    Decimal("100") → "100.00"
    Decimal("99.5") → "99.50"

    For money you always want two decimal places. 100 should display as 100.00, not 100.
    __str__ output: USD 100.00 — clean, human readable.
    """
    
    def __repr__(self):
        return f"Money(amount=Decimal('{self.amount}'), currency='{self.currency}')"

    """
    __repr__ output: Money(amount=Decimal('100.00'), currency='USD') —
    looks like code that could recreate the object. Developer readable.
    """
    
    def __eq__(self, other):
        if not isinstance(other, Money):
            return False
        
        return self.amount == other.amount and self.currency == other.currency

    """
    __eq__ returns False when types don't match — because asking
    "is this Money equal to 42?" is always just false, not an error.
    """
    
    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Cannot compare {self.currency} and {other.currency}"
            )
        
        return self.amount < other.amount
    
    """
    __lt__ raises CurrencyMismatchError when currencies differ —
    because asking "is USD 100 less than EUR 100?" is meaningless without
    an exchange rate. We refuse to guess.

    This is exactly the kind of defensive thinking interviewers look for.
    You're not just writing code that works — 
    you're writing code that fails loudly and clearly when something is wrong.
    """

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Cannot add {self.currency} and {other.currency}"
            )
        
        return Money(self.amount + other.amount, self.currency)
    
    def __sub__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Cannot subtract {self.amount} - {other.amount}"
            )
        
        return Money(self.amount - other.amount, self.currency)
    
    """
    The reason why we used Money() at the end of __sub__ method for two reasons:
        Reason 1 — self.other doesn't exist:
            other is just a parameter name in the method.
            It's not stored on the object.
            So self.other would crash.
            You'd have to write self.amount - other.amount — 
            but that gives you just a Decimal number, not a Money object.

        Reason 2 — You need a Money object back, not a number
            Think about what you want to do after subtracting:
                result = m1 - m2
                print(result)           # should print "USD 50.00"
                result2 = result + m3   # should be able to add again
    
    If __sub__ returned just Decimal("50"), you'd lose the currency.
    You couldn't print it nicely, you couldn't add it to another Money object,
    you couldn't use any of the magic methods you built.

    By returning Money(self.amount - other.amount, self.currency) you get back
    a full Money object with all its methods intact.

    Simple rule:
        When a math operation on a Money object should produce money — return Money.
        When it should produce a yes/no answer — return True/False.
        When it should produce a number — return a number.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, excval, exc_tb):
        pass

    """
    Why does Money need a context manager?
        In a real banking system you'd use Money inside transactions:
            with Money("100.00", "USD") as m:
            # do operations
            # if anything crashes, __exit__ handles cleanup
        
        Right now __exit__ just passes — no cleanup needed for a simple Money object.
        But the structure is there. In a real system __exit__ might log the transaction,
        release a database lock, or roll back changes if an error occurred.

        This shows the interviewer you understand context managers and applied
        them correctly — even when the implementation is simple.
    """