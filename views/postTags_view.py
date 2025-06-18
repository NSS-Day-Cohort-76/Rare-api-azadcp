import sqlite3
import json


def list_postTags():
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                p.id,
                p.follower_id,
                p.author_id,
                p.created_on
            FROM PostTags p
            
            """
        )
        query_results = db_cursor.fetchall()
        postTags = [dict(row) for row in query_results]
        serialized_postTags = json.dumps(postTags)
    return serialized_postTags

def retrieve_postTag(pk, url=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                p.id,
                p.follower_id,
                p.author_id,
                p.created_on
            FROM PostTags p
            WHERE p.id = ?
            """, (pk,)
        )
        query_results = db_cursor.fetchone()
        dictionary_version = dict(query_results)
        serial_post_tag = json.dumps(dictionary_version)
    return serial_post_tag