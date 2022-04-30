from util.database.database import Database


def fetch_known_nodes(database=None):
    """
    Fetch all known nodes from the database.

    :param database: The database to use.
    :type database: :py:class:`util.database.database.Database`
    """
    if database:
        response = database.fetchall('SELECT ip_address, port FROM nodes_archive', {})

    else:
        response = Database.fetchall_from_db('SELECT ip_address, port FROM nodes_archive', {})

    if not response:
        return []

    # Check if only one node is returned.
    if type(response) == tuple:
        return [response]

    return response
