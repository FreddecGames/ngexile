from django.db import connection


serverId = 'ng0'


def dictFetchAll(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dictFetchOne(cursor):
    results = dictFetchAll(cursor)
    if results: return results[0]
    else: return None


cursor = connection.cursor()

def dbRow(query):
    cursor.execute(query)
    return dictFetchOne(cursor)
    
def dbExecute(query):
    cursor.execute(query)