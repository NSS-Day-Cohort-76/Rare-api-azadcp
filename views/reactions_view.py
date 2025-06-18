import sqlite3
import json


def list_reactions():
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                r.id,
                r.label,
                r.image_url,
                
            FROM Reactions r
            
            """
        )
        query_results = db_cursor.fetchall()
        reactions = [dict(row) for row in query_results]
        serialized_reactions = json.dumps(reactions)
    return serialized_reactions

def retrieve_reaction(pk, url=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                r.id,
                r.label,
                r.image_url,
                
            FROM Reactions r
            WHERE r.id = ?
            """, (pk,)
        )
        query_results = db_cursor.fetchone()
        dictionary_version = dict(query_results)
        serial_reaction = json.dumps(dictionary_version)
    return serial_reaction