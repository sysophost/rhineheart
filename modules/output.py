import csv


def write_output(output_path: str, headers: list, output_objects: list, delim: str):
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
