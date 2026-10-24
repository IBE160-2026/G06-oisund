"""Bus values for fresh writes only; historical facts stay verbatim."""
# Unicode White_Space, explicitly shared with busValue.ts. FEFF is meaningful.
BUS_WHITESPACE = '\u0009\u000a\u000b\u000c\u000d\u0020\u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000'


def normalize_bus(value):
    return value if value and any(character not in BUS_WHITESPACE for character in value) else None


def validate_bus(value):
    if value is not None and (len(value) > 100 or "\x00" in value):
        raise ValueError("Bussnummer må ha høyst 100 tegn og kan ikke inneholde NUL.")
    return value
