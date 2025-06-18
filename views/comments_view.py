import sqlite3
import json


def list_comments():
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                c.id,
                c.post_id,
                c.author_id,
                c.content
            FROM Comments c
            
            """
        )
        query_results = db_cursor.fetchall()
        comments = [dict(row) for row in query_results]
        serialized_comments = json.dumps(comments)
    return serialized_comments

def retrieve_comment(pk, url=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                c.id,
                c.post_id,
                c.author_id,
                c.content
            FROM Comments c
            WHERE c.id = ?
            """, (pk,)
        )
        query_results = db_cursor.fetchone()
        dictionary_version = dict(query_results)
        serial_com = json.dumps(dictionary_version)
    return serial_com