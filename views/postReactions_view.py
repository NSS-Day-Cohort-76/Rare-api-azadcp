import sqlite3
import json


def list_postReactions():
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                p.id,
                p.user_id,
                p.reaction_id,
                p.post_id
            FROM PostReactions p
            
            """
        )
        query_results = db_cursor.fetchall()
        post_reactions = [dict(row) for row in query_results]
        serialized_post_reactions = json.dumps(post_reactions)
    return serialized_post_reactions

def retrieve_postReaction(pk, url=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                p.id,
                p.user_id,
                p.reaction_id,
                p.post_id
            FROM PostReactions p
            WHERE p.id = ?
            """, (pk,)
        )
        query_results = db_cursor.fetchone()
        dictionary_version = dict(query_results)
        serial_sub = json.dumps(dictionary_version)
    return serial_sub