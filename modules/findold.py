import requests

from modules import db, queries


def find_old(conn: requests.sessions.Session, days: int, field: str):
    query = queries.construct_find_date_query(field, days)
    resp = db.query_neo(conn, query)
    return resp
