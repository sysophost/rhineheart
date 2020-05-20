from datetime import datetime


def epoch_convert(rows: list, col: int, date_format: str):
    try:
        for row in rows:
            if any(row):
                epochtime = float(row[col])
                row[col] = datetime.fromtimestamp(epochtime).strftime(date_format)

        return rows
    except Exception as err:
        raise err
