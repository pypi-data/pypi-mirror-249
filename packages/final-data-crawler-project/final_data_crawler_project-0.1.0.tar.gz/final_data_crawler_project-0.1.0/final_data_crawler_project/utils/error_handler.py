def text_value_error_handler(text: str) -> ValueError | str:
    """
    Handles errors related to search text values.

    Parameters:
        - text (str): The input search text.

    Returns:
        - ValueError or str: Raises a ValueError with specific messages for invalid cases,
          or returns the original search text if it passes validation.

    Notes:
        - If the input text is None, an empty string is returned.
        - Raises a ValueError if the input text is not a string.
        - Raises a ValueError if the input text consists only of digits.
    """
    if text == None: return ""
    if type(text) is not str:
        raise ValueError("Search text must be string")
    elif text.isdigit():
        raise ValueError("Search text must not contain only numbers")
    else:
        return text