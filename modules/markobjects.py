from requests import sessions

from modules import db, queries


def mark_objects(conn: sessions.Session, input_objects: list, flag: str):
    try:
        query = queries.construct_update_query(input_objects, flag)
        resp = db.query_neo(conn, query)
        return resp
    except Exception as err:
        raise err
