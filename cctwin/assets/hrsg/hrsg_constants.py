class HrsgConstants:
    # Max DB fuel limit in MMBTu/hr
    MAX_FUEL = 720

    # HP pressure limit for STG inlet in psig
    HP_PRESS_LIMIT = 2059

    # HP super-heater temperature limit in °F
    HP_SH_TEMP_LIMIT = 1040

    # Max HP flow output in KPPH. This is used to bias STG output
    # TODO: This needs to be taken out once STG model is fixed.
    HP_HR_MAX_FLOW = 1900
