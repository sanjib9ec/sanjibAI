# vulnerable.py
def get_user_by_name(db_conn, name):
    # BAD: string formatting in SQL -> SQL injection risk
    query = f"SELECT * FROM users WHERE name = '{name}'"
    cursor = db_conn.execute(query)
    return cursor.fetchall()
