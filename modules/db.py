import requests

def query_neo(url: str, headers: str, query: str, timeout: int):
    neo_response = requests.post(url=url, headers=headers, json=query, timeout=timeout)

    return neo_response
