import random

from timeitpoj.utils import constants


def reformat_units(value: float, start_unit="seconds"):
    """
    Reformat a time value to a more readable format.
    :param value: The time value to reformat.
    :param start_unit: The unit of the time value.

    returns: a list of tuples containing the reformatted time value and the unit.
    """

    units = ['seconds', 'milliseconds', 'microseconds', 'nanoseconds', 'minutes', 'hours']
    unit_factors = [1, 1000, 1000000, 1000000000, 60, 3600]

    # first convert to seconds
    if start_unit != "seconds":
        value = value / unit_factors[units.index(start_unit)]
        start_unit = "seconds"

    # check if we need to convert to minutes or hours
    if value >= 60:
        hours = int(value // 3600)
        minutes = int((value % 3600) // 60)
        seconds = value % 60

        ret = []

        if hours > 0:
            ret.append((hours, "hours"))

        if minutes > 0:
            ret.append((minutes, "minutes"))

        if seconds > 0:
            ret.append((seconds, "seconds"))

        return ret

    nvalue = value
    nunit = start_unit

    while nvalue < 1 and nunit != "nanoseconds":
        nvalue *= 1000
        nunit = units[units.index(nunit) + 1]

    reformatted_values = [(nvalue, nunit)]

    return reformatted_values


def time_to_str(value: float, unit: str = "seconds", time_format=constants.DURATION_FORMAT):
    reformatted = reformat_units(value, unit)
    out = ""

    for i, (nvalue, nunit) in enumerate(reformatted):
        if i != 0:
            out += " "
        out += f"{nvalue:{time_format}} {nunit}"

    return out


def format_percentage(value: float, include_brackets=True):
    percentage = f"{value:{constants.PERCENTAGE_FORMAT}}"
    percentage = f"{percentage:>6}"
    if include_brackets:
        percentage = f"[{percentage}]"
    return percentage


def random_task_name():
    adjectives = ['green', 'blue', 'red', 'yellow', 'orange', 'purple']
    nouns = ['apple', 'pistachio', 'ocean', 'sun', 'moon', 'mountain']

    adjective = random.choice(adjectives)
    noun = random.choice(nouns)

    number = random.randint(0, 100)

    return f"task {adjective} {noun} {number}"
