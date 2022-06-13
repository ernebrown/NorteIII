import math
from typing import Union


def get_db_temp_list(db: Union[int, float]) -> list:
    steps = 5
    min_temp = -20
    max_temp = 120

    sign = int(math.copysign(1, db))
    rounded_db = sign * int(round(abs(db)))

    left_steps = min(abs(min_temp - rounded_db), steps)
    min_db = rounded_db - left_steps

    right_steps = min(max_temp - rounded_db, steps)
    max_db = rounded_db + right_steps

    if left_steps <= right_steps:
        db_temps = list(range(min_db, min_db + 2 * steps + 1))
    else:
        db_temps = list(range(max_db - 2 * steps, max_db + 1))

    db_temps = [db_temp if db_temp != rounded_db else db for db_temp in db_temps]
    return db_temps
