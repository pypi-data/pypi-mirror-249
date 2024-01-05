"""
Collection of useful utility functions
"""


def map_value(value, from_min, from_max, to_min, out_max):
    """
    Map a value from one range to another.

    Parameters:
    - value (float): The input value to be mapped
    - from_min (float): The minimum value of the range we are mapping from
    - from_max (float): The maximum value of the range we are mapping from
    - to_min (float): The minimum value of the range we are mapping to
    - to_max (float): The maximum value of the range we are mapping to

    Returns:
    float: The mapped value in the output range
    """
    return (value - from_min) * (out_max - to_min) / (from_max - from_min) + to_min
