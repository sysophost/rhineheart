import argparse
import base64
import csv
import sys
from datetime import datetime, timezone

import requests

from modules import db, epochconvert, findold, markobjects, output, queries

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
PARSER.add_argument('--outputfile', '-of', type=str, default='results.csv', help='Path to output file (default: %(default)s)')
PARSER.add_argument('--delim', type=str, default=',', help='Output file delimiter (default: %(default)s)')
PARSER.add_argument('--dateformat', '-df', choices=['short', 'us', 'usshort', 'utc'], default='%H:%M:%S %d/%m/%Y', help='Output date format (default: %(default)s)')

PARSER.add_argument('--timeout', '-t', type=int, default=30, help='HTTP request timeout')
PARSER.add_argument('--verbose', '-v', action='store_true', help='Increase output verbosity')

ARGS = PARSER.parse_args()

if not (ARGS.markobjects or ARGS.epochconvert or ARGS.findold):
    PARSER.error('--markobjects, --epochconvert, or --findold must be specified')

verbose_print = print if ARGS.verbose else lambda *a, **k: None

def db_init(dbhost: str, dbport: int, username: str, password: str):
    neo_url = f'http://{dbhost}:{dbport}/db/data/transaction/commit'
    credString = f'{username}:{password}'
    base64auth = base64.b64encode(credString.encode()).decode('ascii')

    headers = {
        'Authorization': f'Basic {base64auth}',
        'Content-Type': 'application/json'
    }

    conn = db.construct_connection(neo_url, headers, ARGS.timeout)
    
    # Test DB Connection
    try:
        verbose_print(f'[i] Testing database connection to {neo_url}')
        db.test_connection(conn)
    except requests.exceptions.HTTPError as err:
        print(f'[!] {err}')
        sys.exit()
    except requests.exceptions.ConnectionError as err:
        print(f'[!] {err}')
        sys.exit()
    else:
        verbose_print(f'[i] Database connection to {neo_url} appears to be working')    
        return conn


def main():

    # check input file exists        

    if ARGS.markobjects:
        conn = db_init(ARGS.dbhost, ARGS.dbport, ARGS.username, ARGS.password)
        input_objects = ['aaa', 'bbb', 'ADMINVV@DBA.CORP']
       
        print(f'[i] Performing query with {len(input_objects)} object(s)') 
        resp = markobjects.mark_objects(conn, input_objects, ARGS.markobjects)
        matched_objects = resp.json()['results'][0]['data']
        print(f'[i] Updated {len(matched_objects)} object(s)')
        for matched_object in matched_objects:
            verbose_print(f"{matched_object['row'][0]['name']}\r\n\tOwned:{matched_object['row'][0]['owned']}\r\n\tHighvalue:{matched_object['row'][0]['highvalue']}\r\n")

    if ARGS.epochconvert:
        return

    if ARGS.findold:
        conn = db_init(ARGS.dbhost, ARGS.dbport, ARGS.username, ARGS.password)
        resp = findold.find_old(conn, ARGS.days, ARGS.findold)
        matched_objects = resp.json()['results'][0]['data']
        print(f'[i] Query returned {len(matched_objects)} object(s)')

        # with open(ARGS.outfile, "w") as output_csv_file:
        #     CSV_WRITER = csv.writer(output_csv_file)
        #     CSV_WRITER.writerow(['Username', field, 'Delta (Days)'])

        #     for matched_object in matched_objects:
        #         epochtime = matched_object['row'][0][field]
        #         human_time = datetime.fromtimestamp(
        #             epochtime).strftime(date_format)
        #         current_time = datetime.now().strftime(date_format)
        #         delta = (datetime.strptime(current_time, date_format) -
        #                 datetime.strptime(human_time, date_format)).days
        #         name = matched_object['row'][0]['name']
        #         verbose_print(name)

        #         CSV_WRITER.writerow([name, human_time, delta])

        # output_csv_file.close()
        # print(f"[i] Output file written to {ARGS.outfile}")


if __name__ == '__main__':
    main()
