

def fetchall_as_dict(cursor):
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    result = [dict(zip(column_names, row)) for row in rows]
    return result

def fetchone_as_dict(cursor):
    column_names = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    result = dict(zip(column_names, row)
    ) if row else None
    return result