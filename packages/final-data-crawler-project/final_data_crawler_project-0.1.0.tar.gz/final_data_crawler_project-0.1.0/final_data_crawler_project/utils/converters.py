def convert_to_float(value):
    """
    Converts a string to a float.

    Parameters:
        - value: The input string to be converted.

    Returns:
        - float or None: The converted float value if successful, or None if the conversion fails.

    Notes:
        - If the input value is an empty string, None is returned.
    """
    if value == "":
        return None 
    else:
        try:
            return float(value.strip())
        except ValueError:
            # Handle the case where the conversion fails
            return None

def convert_to_int(value):
    """
    Converts a string to an integer.

    Parameters:
        - value: The input string to be converted.

    Returns:
        - int or None: The converted integer value if successful, or None if the conversion fails.

    Notes:
        - If the input value is an empty string, None is returned.
    """
    if value == "":
        return None 
    else:
        try:
            return int(value.strip())
        except ValueError:
            # Handle the case where the conversion fails
            return None