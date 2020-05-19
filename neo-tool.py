import argparse
import base64
import csv
import sys
from datetime import datetime, timezone

import requests

from modules import db, queries

PARSER = argparse.ArgumentParser()

# DB connection args
PARSER.add_argument('--dbhost', '-dh', type=str, default='127.0.0.1', help='IP address or hostname where Neo4J is running (default: %(default)s)')
PARSER.add_argument('--dbport', '-dp', type=str, default='7474', help='Neo4J listen port (default: %(default)s)')
PARSER.add_argument('--username', '-u', type=str, default='neo4j', help='Neo4J username (default: %(default)s)')
PARSER.add_argument('--password', '-p', type=str, default='Pa55w0rd', help='Neo4J password (default: %(default)s)')

# Input/output formatting args
PARSER.add_argument('--inputfile', '-if', type=str, default='file.txt', help='Path to file containing matched_object names (default: %(default)s)')
PARSER.add_argument('--outputfile', '-of', type=str, default='results.csv', help='Path to output file (default: %(default)s)')
PARSER.add_argument('--delim', type=str, default=',', help='Output file delimiter (default: %(default)s)')
PARSER.add_argument('--dateformat', '-df', choices=['short', 'us', 'usshort', 'utc'], default='%H:%M:%S %d/%m/%Y', help='Output date format (default: %(default)s)')

# Workflows
PARSER.add_argument('--markobjects', '-mo', choices=['owned', 'highvalue', 'both'], help='Mark supplied objects as owned, highvalue, or both')
PARSER.add_argument('--epochconvert', '-ec', action='store_true', help='Convert epoch timestamps in input file to human readable date/time')
PARSER.add_argument('--col', '-c', type=int, action='append', required='--epochconvert' in sys.argv or '-ec' in sys.argv, help='Column index with epoch timestamps (can be supplied multiple times)')
PARSER.add_argument('--findold', '-fo', action='store_true', help='Search for users with password last set or last logon older than X days')
PARSER.add_argument('--days', '-d', type=int, required='--findold' in sys.argv or '-fo' in sys.argv, help='Number of days since last logon or password change')

PARSER.add_argument('--verbose', '-v',action='store_true', help='increase output verbosity')

ARGS = PARSER.parse_args()

if not (ARGS.markobjects or ARGS.epochconvert or ARGS.findold):
    PARSER.error('--markobjects, --epochconvert, or --findold must be specified')

REQUEST_TIMEOUT = 30

verbose_print = print if ARGS.verbose else lambda *a, **k: None

def main():

    users = ['a', 'b']
    update_query = queries.construct_update_query(users, ARGS.markobjects)
    
    
    find_query = queries.construct_find_object_query(users)
    print(find_query)



    return

if __name__ == '__main__':
    main()
