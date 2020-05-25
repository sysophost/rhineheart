from requests import sessions

from modules import db, queries


def find_old(conn: sessions.Session, days: int, field: str):
    """
    Search for objects with either lastlogontimestamp or pwdlastchange older than the defined day offset

    Arguments:
        conn {sessions.Session} -- handle to the DB connection
        days {int} -- day offset
        field {str} -- field to perform search filter on

    Raises:
        err: generic exception for anything that goes wrong

    Returns:
        requests.Response -- http response from neo4j
    """

    try:
        query = queries.construct_find_date_query(field, days)
        resp = db.query_neo(conn, query)
        return resp
    except Exception as err:
        raise err
