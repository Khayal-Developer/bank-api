"""
Order: 02

Encapsulation (private attributes)
__init__, __str__, __repr__
Using Money inside another class
"""

"""
Customer class representing a bank customer
"""

from typing import List
from money import Money

"""
from typing import List
List lets you say "this is not just any list — 
this is a list of a specific type." For example List[Money]
means "a list that contains only Money objects." 
This makes your code clearer and helps catch mistakes early. 
It comes from Python's built-in typing module.

from money import Money
You already built the Money class in money.py.
A customer's balance is not a plain number — 
it's a Money object with amount and currency. 
This line tells Python: "go find money.py in the same folder
and bring the Money class here so I can use it."
"""

"""
Encapsulation concept + __init__
Encapsulation means protecting data inside a class so
it cannot be changed from outside without going through your rules.

Without encapsulation anyone can do this:
customer.name = ""
customer.balance = -999999

No error, no warning. The data is just broken silently.

Python convention for private attributes — 
put a single underscore before the name:
self._name = balance
self._balance = balance

The underscore means: "this is internal, don't touch it from outside."

To allow reading from outside without allowing writing, you use @property:
@property
def name(self):
    return self._name

Now customer.name works for reading.
But customer.name = "hacker" raises an AttributeError.
Read allowed, write blocked.
"""

class Customer:
    """
    Represents a bank customer.
    Attributes are private - accessed through properties.
    """

    def __init__(self, name: str, balance: Money): # This line just hints that name should be string and balance must be the Money object           
        if not isinstance(balance, Money):                      # Actual check starts here
            raise TypeError("Balance must be a Money object")
        if not name or not name.strip():                        # And checks here
            raise ValueError("name cannot be empty")
        
        """
        Why isinstance(balance, Money)?
        Same reason as in Money.__eq__ — we check the type before using it.
        If someone passes 1000 instead of Money("1000", "USD") we raise a clear
        TypeError immediately.
        

        What is name.strip()?
        strip() removes spaces from both ends of a string.
        So "   ".strip() becomes "" which is empty —
        meaning someone passed only spaces as a name. We reject that.
        """
        
        
        """
        The underscore means: "this is internal. Don't touch it from outside."
        """
        self._name = name           # private — stored with underscore
        self._balance = balance     # private — stored with underscore

    """
    Without Encapsulation, if you use code below, you would just break the object.
    No error, no warning. The data is completely unprotected.
    m = Money("100", "USD")
    m.balance = -999999
    m.currency = "XYZ"

    Encapsulation means hiding data inside the class so it can't be changed
    from outside without going through your rules.

    But then how do you read the value from outside? With a property:
    @property is a decorator — it turns a method into something you
    access like an attribute, not a function call.
    So you write m.name not m.name().
    """
    @property
    def name(self):             # public — read only
        return self._name
    
    @property
    def balance(self):          # public — read only
        return self._balance
    
    """
    Now m.balance works for reading — but m.balance = -999 raises an AttributeError.
    You can read, you can't overwrite.
    """

    def __str__(self):
        return f"Customer: {self._name} | Balance: {self._balance}"
    
    def __repr__(self):
        return f"Customer(name='{self._name}', balance={repr(self._balance)})"
    
    """
    {self._balance} in __str__
    self._balance is a Money object. When you put it inside an f-string,
    Python automatically calls __str__ on it. So it prints USD 100.50 —
    exactly what Money.__str__ returns. One class using another class's
    magic methods automatically.

    repr(self._balance) in __repr__
    Same idea but for __repr__. repr() calls Money.__repr__
    which returns Money(amount=Decimal('100.50'), currency='USD').
    This makes the full output look like real code that could recreate the object.
    """