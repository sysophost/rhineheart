import requests


def construct_connection(url: str, headers: str, timeout: int):
    s = requests.Session()
    s.url = url
    s.headers = headers
    s.timeout = timeout
    return s

def test_connection(session: requests.sessions.Session):
    try:
        resp = session.post(session.url)
        resp.raise_for_status()
    except Exception as err:
        raise err
    else:
        return True

def query_neo(session: requests.sessions.Session, json: str):
    neo_response = session.post(session.url, json=json)
    return neo_response
