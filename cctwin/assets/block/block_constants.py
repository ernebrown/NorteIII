class BlockConstants:
    # This is is the minimum allowed ambient DB temp
    # Units are °F
    MIN_DB = 0

    # This is is the maximum allowed ambient DB temp
    # Units are °F
    MAX_DB = 120

    # This is is the minimum allowed ambient RH (used as percent only in UI but as fraction in code)
    MIN_RH = 0.0

    # This is is the maximum allowed ambient RH (used as percent only in UI but as fraction in code)
    # Value should not be more than 1.0
    MAX_RH = 1.0

    # This is is the minimum allowed ambient barometric press
    # Units are psia
    MIN_BARO = 14.3

    # This is is the maximum allowed ambient barometric press
    # Units are psia
    MAX_BARO = 15.1
