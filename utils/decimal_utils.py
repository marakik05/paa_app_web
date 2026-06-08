"""Helpers για ακριβή δεκαδική στρογγυλοποίηση (ROUND_HALF_UP)."""
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

CENT = Decimal("0.01")


def to_decimal(text):
    """Μετατροπή κειμένου σε Decimal με ανοχή σε ',' και κενά. None αν άκυρο/κενό."""
    if text is None:
        return None
    s = str(text).strip().replace(",", ".")
    if not s:
        return None
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def q2(value):
    """Στρογγυλοποίηση σε 2 δεκαδικά με ROUND_HALF_UP."""
    if value is None:
        return None
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def fmt2(value):
    """Διαμόρφωση σε string '#.##' με ROUND_HALF_UP. Άδειο string αν None/άκυρο."""
    q = q2(value)
    return "" if q is None else f"{q:f}"
