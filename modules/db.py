import base64

from requests import sessions


def db_init(dbhost: str, dbport: int, username: str, password: str, timeout: int):
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
        print(f'[i] Testing database connection to {neo_url}')
        test_connection(conn)
        print(f'[i] Database connection to {neo_url} appears to be working')
        return conn
    except Exception as err:
        raise err


def construct_connection(url: str, headers: str, timeout: int):
    s = sessions.Session()
    s.url = url
    s.headers = headers
    s.timeout = timeout
    return s


def test_connection(session: sessions.Session):
    try:
        resp = session.post(session.url)
        resp.raise_for_status()
        return True
    except Exception as err:
        raise err


def query_neo(session: sessions.Session, json: str):
    try:
        neo_response = session.post(session.url, json=json)
        return neo_response
    except Exception as err:
        raise err
