import argparse
import csv
import logging
import sys
from datetime import datetime

from modules import (data, db, epochconvert, findold, formatting, markobjects,
                     output, queries)

PARSER = argparse.ArgumentParser()

# DB connection args
PARSER.add_argument('--dbhost', '-dh', type=str, default='127.0.0.1', help='IP address or hostname where Neo4J is running (default: %(default)s)')
PARSER.add_argument('--dbport', '-dp', type=int, default='7474', help='Neo4J listen port (default: %(default)s)')
PARSER.add_argument('--username', '-u', type=str, default='neo4j', help='Neo4J username (default: %(default)s)')
PARSER.add_argument('--password', '-p', type=str, default='Pa55w0rd', help='Neo4J password (default: %(default)s)')

# Workflows
PARSER.add_argument('--markobjects', '-mo', choices=['owned', 'highvalue', 'both'], help='Mark supplied objects as owned, highvalue, or both')
PARSER.add_argument('--epochconvert', '-ec', action='store_true', help='Convert epoch timestamps in input file to human readable date/time')
PARSER.add_argument('--col', '-c', type=int, action='append', required='--epochconvert' in sys.argv or '-ec' in sys.argv, help='Column index with epoch timestamps (can be supplied multiple times)')
PARSER.add_argument('--findold', '-fo', choices=['logon', 'password'], help='Search for users with password last set or last logon older than X days')
PARSER.add_argument('--days', '-d', type=int, required='--findold' in sys.argv or '-fo' in sys.argv, help='Number of days since last logon or password change')

# Input/output formatting args
PARSER.add_argument('--inputfile', '-if', type=str, required='--markobjects' in sys.argv or '-mo' in sys.argv or '--epochconvert' in sys.argv or '-ec' in sys.argv, help='Path to input file')
PARSER.add_argument('--outputfile', '-of', type=str, help='Path to output file')
PARSER.add_argument('--indelim', '-id', type=str, default=',', help='Output file delimiter (default: %(default)s)')
PARSER.add_argument('--outdelim', '-od', type=str, default=',', help='Output file delimiter (default: %(default)s)')
PARSER.add_argument('--dateformat', '-df', choices=['short', 'us', 'usshort'], default='%H:%M:%S %d/%m/%Y', help='Output date format (default: %(default)s)')

PARSER.add_argument('--noheaders', '-nh', action='store_true', help='Prevent header row from being written to screen')
PARSER.add_argument('--timeout', '-t', type=int, default=30, help='HTTP request timeout')
PARSER.add_argument('--verbose', '-v', action='store_true', help='Increase output verbosity')

ARGS = PARSER.parse_args()

if not (ARGS.markobjects or ARGS.epochconvert or ARGS.findold):
    PARSER.error('--markobjects, --epochconvert, or --findold must be specified')

verbose_print = print if ARGS.verbose else lambda *a, **k: None
logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stderr)


def main():
    date_format = formatting.format_date(ARGS.dateformat)

    if ARGS.inputfile:
        try:
            with open(ARGS.inputfile, 'r') as objects_file:
                if data.is_csv(objects_file, ARGS.indelim):
                    csv_reader = csv.reader(objects_file, delimiter=ARGS.indelim)
                    HEADERS = next(csv_reader)
                    input_objects = list(csv_reader)
                else:
                    input_objects = objects_file.read().splitlines()

                objects_file.close()
                logging.info(f'[i] Found {len(input_objects)} object(s) in {ARGS.inputfile}')

        except (OSError, IOError) as err:
            logging.error(f'[!] {ARGS.inputfile} not found')
            sys.exit(1)

    if ARGS.markobjects:
        try:
            conn = db.db_init(ARGS.dbhost, ARGS.dbport, ARGS.username, ARGS.password, ARGS.timeout)

            logging.info(f'[i] Performing query with {len(input_objects)} object(s)')
            resp = markobjects.mark_objects(conn, input_objects, ARGS.markobjects)
            matched_objects = resp.json()['results'][0]['data']
            logging.info(f'[i] Updated {len(matched_objects)} object(s)')

            output_objects = list()
            headers = ['Name', 'Owned', 'Highvalue']
            if not ARGS.noheaders:
                verbose_print(f'{ARGS.outdelim}'.join(map(str, headers)))
            for matched_object in matched_objects:
                name = matched_object['row'][0]['name']
                owned = matched_object['row'][0]['owned']
                highvalue = matched_object['row'][0]['highvalue']
                output_objects.append([name, owned, highvalue])
                verbose_print(f'{ARGS.outdelim}'.join(map(str, [name, owned, highvalue])))
            if ARGS.outputfile:
                output.write_output(ARGS.outputfile, headers, output_objects, ARGS.outdelim)
                logging.info(f"[i] Output file written to {ARGS.outputfile}")

        except Exception as err:
            logging.error(f'[!] {err}')
            sys.exit(1)

    if ARGS.epochconvert:
        try:
            for col in ARGS.col:
                converted = epochconvert.epoch_convert(input_objects, col, date_format)

        except ValueError as err:
            logging.error(f'[!] Input file is incorrectly formatted - {err}')
        except IndexError as err:
            logging.error(f'[!] Invalid column index specified - {err}')
        else:
            try:
                print(f'{ARGS.outdelim}'.join(map(str, HEADERS)))
                for row in converted:
                    print(f'{ARGS.outdelim}'.join(map(str, row)))

                if ARGS.outputfile:
                    output.write_output(ARGS.outputfile, HEADERS, converted, ARGS.outdelim)
                    logging.info(f"[i] Output file written to {ARGS.outputfile}")

            except Exception as err:
                logging.error(f'[!] {err}')
                sys.exit(1)

    if ARGS.findold:
        try:
            conn = db.db_init(ARGS.dbhost, ARGS.dbport, ARGS.username, ARGS.password, ARGS.timeout)

            if ARGS.findold == 'logon':
                field = 'lastlogontimestamp'
            elif ARGS.findold == 'password':
                field = 'pwdlastset'

            resp = findold.find_old(conn, ARGS.days, field)
            matched_objects = resp.json()['results'][0]['data']
            logging.info(f'[i] Query returned {len(matched_objects)} object(s)')

            output_objects = list()
            headers = ['Name', field, 'Delta (days)']
            if not ARGS.noheaders:
                verbose_print(f'{ARGS.outdelim}'.join(map(str, headers)))
            for matched_object in matched_objects:
                # TODO: resuse epoch convert code here

                epochtime = matched_object['row'][0][field]
                human_time = datetime.fromtimestamp(epochtime).strftime(date_format)
                current_time = datetime.now().strftime(date_format)
                delta = (datetime.strptime(current_time, date_format) - datetime.strptime(human_time, date_format)).days
                name = matched_object['row'][0]['name']

                output_objects.append([name, human_time, delta])
                verbose_print(f'{ARGS.outdelim}'.join(map(str, [name, human_time, delta])))

            if ARGS.outputfile:
                output.write_output(ARGS.outputfile, headers, output_objects, ARGS.outdelim)
                logging.info(f"[i] Output file written to {ARGS.outputfile}")

        except Exception as err:
            logging.error(f'[!] {err}')
            sys.exit(1)


if __name__ == '__main__':
    main()
