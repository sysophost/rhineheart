from requests import sessions

from modules import db, queries


def mark_objects(conn: sessions.Session, input_objects: list, flag: str):
    """
    mark the supplied objects as owned, high value, or both

    Arguments:
        conn {sessions.Session} -- handle to the DB connection
        input_objects {list} -- the list of objects to perform the update on
        flag {str} -- the attribute to set (owned, high value, both)

    Raises:
        err: generic exception for anything that goes wrong

    Returns:
        requests.Response -- http response from neo4j
    """

    try:
        query = queries.construct_update_query(input_objects, flag)
        resp = db.query_neo(conn, query)
        return resp
    except Exception as err:
        raise err
