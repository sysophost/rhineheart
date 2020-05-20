from requests import sessions

from modules import db, queries


def find_old(conn: sessions.Session, days: int, field: str):
    try:
        query = queries.construct_find_date_query(field, days)
        resp = db.query_neo(conn, query)
        return resp
    except Exception as err:
        raise err
