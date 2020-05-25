from datetime import datetime


def epoch_convert(rows: list, col: int, date_format: str):
    """
    convert epoch timestamps in a CSV into a human readable format

    Arguments:
        rows {list} -- rows read in from the CSV
        col {int} -- column index within the row that contains the timestamp to convert
        date_format {str} -- date format to convert epoch timestamp to

    Raises:
        err: generic exception if anything goes wrong

    Returns:
        requests.Response -- updated rows with epoch timestamps converted to human readable, using the given date format
    """

    try:
        for row in rows:
            if any(row):
                epochtime = float(row[col])
                row[col] = datetime.fromtimestamp(epochtime).strftime(date_format)

        return rows
    except Exception as err:
        raise err
