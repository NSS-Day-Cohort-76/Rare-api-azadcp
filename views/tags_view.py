import sqlite3
import json


def list_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                t.id,
                t.label,
                
                
            FROM Tags t
            
            """
        )
        query_results = db_cursor.fetchall()
        tags = [dict(row) for row in query_results]
        serialized_tags = json.dumps(tags)
    return serialized_tags

def retrieve_tags(pk, url=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                t.id,
                t.label,
                
            FROM Tags t
            WHERE t.id = ?
            """, (pk,)
        )
        query_results = db_cursor.fetchone()
        dictionary_version = dict(query_results)
        serial_t = json.dumps(dictionary_version)
    return serial_t