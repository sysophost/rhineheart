import csv


def write_output(output_path: str, headers: list, output_objects: list, delim: str):
    """
    Generate output file

    Arguments:
        output_path {str} -- output path for file
        headers {list} -- headers row for output CSV
        output_objects {list} -- input data to be written to CSV
        delim {str} -- column delimiter

    Raises:
        err: returns a generic error for all exceptions, such as file write etc.
    """

    try:
        with open(output_path, "w") as output_file:
            csv_writer = csv.writer(output_file, delimiter=delim, quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(headers)

            for row in output_objects:
                if any(row):
                    csv_writer.writerow(row)
    except Exception as err:
        raise err
    finally:
        output_file.close()
