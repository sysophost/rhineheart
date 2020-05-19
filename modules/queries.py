def construct_find_date_query(field: str, days: int):
    data = {
        'statements': [{'statement': f'MATCH (u:User) WHERE u.{field} <= (datetime().epochseconds - ({days} * 86400)) and NOT u.{field} IN [-1.0, 0.0] RETURN u ORDER BY u.name ASC'}]
    }

    return data


def construct_find_object_query(input_objects: list):
    data = {
        'statements': [{'statement': f'MATCH (n) WHERE n.name IN {input_objects} RETURN n'}]
    }

    return data


def construct_update_query(input_objects: list, flag: str):
    if flag == 'both':
        query_action = 'n.owned=TRUE, n.highvalue=TRUE'
    elif flag == 'owned':
        query_action = 'n.owned=TRUE'
    elif flag == 'highvalue':
        query_action = 'n.highvalue=TRUE'

    data = {
        'statements': [{'statement': f'MATCH (n) WHERE n.name IN {input_objects} SET {query_action} RETURN n'}]
    }

    return data