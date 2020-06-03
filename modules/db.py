import base64
import logging

from requests import sessions


def db_init(dbhost: str, dbport: int, username: str, password: str, timeout: int) -> sessions.Session:
    """
    Initialise the request session to the neo4j DB

    Arguments:
        dbhost {str} -- Host/IP address to connect to
        dbport {int} -- Neo4j listening port
        username {str} -- Username to authenticate to neo4j
        password {str} -- Password to authentiate to neo4j
        timeout {int} -- HTTP request timeout in seconds

    Raises:
        err: Generic exception if anything goes wrong

    Returns:
        requests.sessions.Session -- If test_connection() is successful, returns a session object with a handle to the current DB
    """

    neo_url = f'http://{dbhost}:{dbport}/db/data/transaction/commit'
    credString = f'{username}:{password}'
    base64auth = base64.b64encode(credString.encode()).decode('ascii')

    headers = {
        'Authorization': f'Basic {base64auth}',
        'Content-Type': 'application/json'
    }

    conn = construct_connection(neo_url, headers, timeout)

    # Test DB Connection
    try:
        logging.info(f'[i] Testing database connection to {neo_url}')
        test_connection(conn)
        logging.info(f'[i] Database connection to {neo_url} appears to be working')
        return conn
    except Exception as err:
        raise err


def construct_connection(url: str, headers: str, timeout: int) -> sessions.Session:
    """
    Creates a requests.session.Session() object with a handle to the neo4j DB

    Arguments:
        url {str} -- Neo4j URL to connect to
        headers {str} -- JSON string containing the necessary authorization header and content type
        timeout {int} -- HTTP request timeout in seconds

    Returns:
        requests.sessions.Session -- requests.sessions.Session() object for the given connection
    """

    s = sessions.Session()
    s.url = url
    s.headers = headers
    s.timeout = timeout
    return s


def test_connection(session: sessions.Session) -> bool:
    """
    Test connection to neo4j

    Arguments:
        session {sessions.Session} -- Handle to the neo4j DB

    Raises:
        err: Generic exception if anything goes wrong

    Returns:
        bool -- True indicates a successful connection to the DB
    """

    try:
        resp = session.post(session.url)
        resp.raise_for_status()
        return True
    except Exception as err:
        raise err


def query_neo(session: sessions.Session, json: str):
    """
    Submit the supplied query to neo4j

    Arguments:
        session {sessions.Session} -- Handle to the neo4j DB
        json {str} -- Query string to submit

    Raises:
        err: Generic exception of anything goes wrong

    Returns:
        requests.Response -- HTTP response from neo4j
    """

    try:
        neo_response = session.post(session.url, json=json)
        return neo_response
    except Exception as err:
        raise err
