def is_true(value: str) -> bool:
    """
    Check if the string provided matches one of the words that can be used for
    a true expression, eg. "true", "yes".
    """
    return str(value).lower() in ["true", "t", "1", "on", "yes", "y"]


def is_false(value: str) -> bool:
    """
    Check if the string provided matches one of the words that can be used for
    a false expression, eg. "false", "no".
    """
    return str(value).lower() in ["false", "f", "0", "off", "no", "n"]
