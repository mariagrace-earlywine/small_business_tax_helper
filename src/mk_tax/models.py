# this file is the projects "data definition" file.  It defines the shape of data/transaction in a clean, consistent object.

from dataclasses import dataclass #dataclass -> gives a clean 'data container' class without writing boilerplate.
from datetime import date # date -> stores dates as real dates objects (not strings)
from decimal import Decimal # safer for money than float (avoids rounding surprises).


@dataclass(frozen=True) #makes the object immutable (helps prevent accidental edits)
class Expense:
    """
    One expense transaction (a single row from the CSV).
    'vendor' = who you paid (vendor/payee) or who it involved (customer/client).
    """
    when: date
    vendor: str
    category: str
    amount: Decimal
    notes: str = ""
    business: str = ""
    payment_method: str = ""
