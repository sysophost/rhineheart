import requests

from modules import db, queries


def mark_objects(conn: requests.sessions.Session, input_objects: list, flag: str):
    query = queries.construct_update_query(input_objects, flag)
    resp = db.query_neo(conn, query)
    return resp
