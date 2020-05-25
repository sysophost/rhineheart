def format_date(in_format: str) -> str:
    """
    Return the relevant date format string for the given input switch

    Arguments:
        in_format {str} -- date type to return the format string for

    Returns:
        str -- date format string for the passed arg
    """

    if in_format == 'short':
        date_format = '%d/%m/%Y'
    elif in_format == 'us':
        date_format = '%H:%M:%S %m/%d/%Y'
    elif in_format == 'usshort':
        date_format = '%m/%d/%Y'
    else:
        date_format = in_format

    return date_format
