import csv

from _io import TextIOWrapper


def is_csv(objects_file: TextIOWrapper, delim: str):
    try:
        csv.Sniffer().sniff(objects_file.read(1024), delimiters=delim)
        return True
    except:
        return False
    finally:
        objects_file.seek(0)  # need this to move back to the beginning of the file after sampling
