def format_date(in_format: str):
    if in_format == 'short':
        date_format = '%d/%m/%Y'
    elif in_format == 'us':
        date_format = '%H:%M:%S %m/%d/%Y'
    elif in_format == 'usshort':
        date_format = '%m/%d/%Y'
    else:
        date_format = in_format

    return date_format
