from datetime import datetime


def validate_time(time_str: str):
    """Validate time string

    Args:
        time_str (str): Time string

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.strptime(time_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
