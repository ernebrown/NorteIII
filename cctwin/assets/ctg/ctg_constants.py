class CtgConstants:
    MIN_BASE_LOAD_THRESHOLD = 80  # Below this number, inlet-conditioning and peaking abilities
    # of CTG will be turned off. Value cannot be more than 100

    MIN_CTG_AVLBLTY = 40  # Below this availability value, Min-load logic will be executed.
    # Value cannot be more than 100

    MAX_CTG_AVLBLTY = 100  # Above or equal to this availability value, Base-load logic will be executed.

    BASE_CTG_AVLBLTY = 100  # Above or equal to this availability value, Base-load logic will be executed.


    MIN_IGV = 45  # This is used as the starting point for Solver when solving for IGV.
    # Use a number close to typical value when CTGs are running @ Min-load.

    BASE_IGV = 86  # This value doesn't effect the logic.
    # It is only shown in the output when Base-load logic is executed.

    AGC_SETPT = 98  # This value is for setting up AGC setpoint for running base as AGC

    DEFAULT_PAG_AVLBLTY = 0  # Default availability for PAG

    MAX_PAG_AVLBLTY = 100  # Max availability for PAG

    DEFAULT_WC_AVLBLTY = 100  # Default availability for Wet Compression

    MAX_WC_AVLBLTY = 100  # Max availability for Wet Compression

    DEFAULT_PF_AVLBLTY = 0  # Default availability for Peak Firing

    MAX_PF_AVLBLTY = 100  # Max availability for Peak Firing

    MIN_WC_DB=65 # Min Temperature to run Wet Compression