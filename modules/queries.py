def construct_find_date_query(field: str, days: int) -> str:
    """
    Assembles the find query with a filter for the supplied field (lastlogontimestamp or pwdlastchange) and supplied day offset

    Arguments:
        field {str} -- the field to filter on 
        days {int} -- days offset

    Returns:
        str -- the complete query string
    """

    query = {
        'statements': [{'statement': f'MATCH (u:User) WHERE u.{field} <= (datetime().epochseconds - ({days} * 86400)) and NOT u.{field} IN [-1.0, 0.0] RETURN u ORDER BY u.name ASC'}]
    }

    return query


def construct_find_object_query(input_objects: list) -> str:
    """
    Assembles the find query with a filter for the supplied list of input objects

    Arguments:
        input_objects {list} -- objects to include within the search ilter

    Returns:
        str -- the complete query string, including the supplied objects
    """

    query = {
        'statements': [{'statement': f'MATCH (n) WHERE n.name IN {input_objects} RETURN n'}]
    }

    return query


def construct_update_query(input_objects: list, flag: str) -> str:
    """
    Assembles the update query to mark objects as owned, high value, or both

    Arguments:
        input_objects {list} -- objects to perform the update on
        flag {str} -- the attribute to mark as true

    Returns:
        str -- the complete query string, including the supplied objects and the relevant attribute to mark true
    """

    actions = {
        'both': 'n.owned=TRUE, n.highvalue=TRUE',
        'owned': 'n.owned=TRUE',
        'highvalue': 'n.highvalue=TRUE'
    }

    query = {
        'statements': [{'statement': f'MATCH (n) WHERE n.name IN {input_objects} SET {actions[flag]} RETURN n'}]
    }

    return query
