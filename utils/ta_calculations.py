from utils.excel_loader import (in_norm_set, contains_norm_keyword, 
                                PARAGWGIKA_CAT_NORM, PARAGWGIKA_NORM,AEGEAN_PERIFERIES, LOCK_AMPELI_NORM, 
                                LOCK_TREES_NORM, FMZ_ZWIKI_NORM, FMZ_MELISSES_NORM)


def typiki_apodosi(col_0, col_2, col_3, col_5, col_6, col_7):
    """
    Υπολογισμός ΤΑ ανά αγροτεμάχιο (στήλη 8).
    col_0: category, col_2: TA, col_3: area,
    col_5: trees>=4, col_6: trees<4, col_7: vine>3yr
    """
    if col_2 is None or col_3 is None:
        return None

    if in_norm_set(col_0, LOCK_AMPELI_NORM):
        if col_7 == "Ναι":
            return col_2 * col_3
        elif col_7 == "Όχι":
            return (col_2 / 2) * col_3
        else:  # empty or "--Επιλέξτε"
            return None
    else:
        if (col_5 is None or col_5 == 0) and (col_6 is None or col_6 == 0):
            return col_2 * col_3
        if col_5 is None or col_5 == 0:
            return (col_2 / 2) * col_3
        if col_6 is None or col_6 == 0:
            return col_2 * col_3
        total = col_5 + col_6
        return col_2 * (col_3 * (col_5 / total)) + (col_2 / 2) * (col_3 * (col_6 / total))


def ta_paragwgikwn(col_0, col_2, col_3, col_5, col_6, col_7):
    """
    Υπολογισμός ΤΑ παραγωγικών (μόνο παραγωγικά δένδρα).
    """
    if col_2 is None or col_3 is None:
        return None

    if in_norm_set(col_0, LOCK_AMPELI_NORM):
        if col_7 == "Ναι":
            return col_2 * col_3
        else:
            return None
    else:
        if (col_5 is None or col_5 == 0) and (col_6 is None or col_6 == 0):
            return col_2 * col_3
        if col_5 is None or col_5 == 0:
            return None
        if col_6 is None or col_6 == 0:
            return col_2 * col_3
        total = col_5 + col_6
        return col_2 * (col_3 * (col_5 / total))


def route_fzm(category):
    """
    Determines which TA column a category goes to.
    Returns 12 (φυτική), 13 (ζωική), or 14 (μελίσσια).
    """
    if in_norm_set(category, FMZ_ZWIKI_NORM):
        return 13
    elif in_norm_set(category, FMZ_MELISSES_NORM):
        return 14
    return 12

def paragwgikwn(category, description, output_per_choice, productive_value):
    """Στήλη 11 — ΤΑ Παραγωγικών."""
    if in_norm_set(category, PARAGWGIKA_CAT_NORM) and contains_norm_keyword(description, PARAGWGIKA_NORM):
        return output_per_choice
    return productive_value

def lookup_typical_output(value_mapping, category, description, region):
    """Στήλη 2 — ΤΑ από ta.xlsx, aegean ή default column ανά περιφέρεια."""
    if not region or region == "--Επιλέξτε":
        return None
    entry = value_mapping.get((category, description))
    if entry is None:
        return None
    return entry["aegean"] if region in AEGEAN_PERIFERIES else entry["default"]

def calc_row(value_mapping, region, category, description, quantity, trees_over_4, trees_under_4, vine_over_3):
    """Υπολογίζει στήλες 2, 8, locks, routing για 1 γραμμή."""
    typical_output = lookup_typical_output(value_mapping, category, description, region)
    output_per_choice = typiki_apodosi(category, typical_output, quantity, trees_over_4, trees_under_4, vine_over_3)
    productive = ta_paragwgikwn(category, typical_output, quantity, trees_over_4, trees_under_4, vine_over_3)
    return {
        "typical_output": typical_output,
        "output_per_choice": output_per_choice,
        "productive": paragwgikwn(category, description, output_per_choice, productive),
        "route": route_fzm(category),
        "lock_ampeli": in_norm_set(category, LOCK_AMPELI_NORM),
        "lock_trees": in_norm_set(category, LOCK_TREES_NORM),
    }

def calc_totals(rows_calc):
    """Σύνολα 10-14: Σύνολο ΤΑ, ΤΑ Παραγωγικών, Φυτικής, Ζωικής, Μελισσών."""
    def _sum(values):
        present = [v for v in values if v is not None]
        return sum(present) if present else None

    return {
        "total_output": _sum(r["output_per_choice"] for r in rows_calc),
        "ta_productive": _sum(r["productive"] for r in rows_calc),
        "ta_plant":  _sum(r["output_per_choice"] for r in rows_calc if r["route"] == 12),
        "ta_animal": _sum(r["output_per_choice"] for r in rows_calc if r["route"] == 13),
        "ta_bees":   _sum(r["output_per_choice"] for r in rows_calc if r["route"] == 14),
    }

def to_float(value):
    """Μετατροπή input string ('', None, '1,5', '3') σε float ή None."""
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return None
    
def to_int(value):
    """Μετατροπή input string ('', None, '1,5', '3') σε int ή None."""
    if value in (None, ""):
        return None
    try:
        return int(str(value))
    except (ValueError, TypeError):
        return None