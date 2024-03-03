from django.db import connection


def execute_query(query):
    """Function:
        Executes a query on a database and returns the results as a list of dictionaries.
    Parameters:
        - query (str): SQL query to be executed.
    Returns:
        - data (list): List of dictionaries containing the results of the query.
    Processing Logic:
        - Execute query on database.
        - Get column names from cursor description.
        - Fetch all rows from cursor.
        - Create a dictionary for each row."""
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

    return data


