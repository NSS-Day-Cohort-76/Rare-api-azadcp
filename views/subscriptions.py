import sqlite3
import json


def list_subscriptions():
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                s.id,
                s.follower_id,
                s.author_id,
                s.created_on
            FROM Subscriptions s
            
            """
        )
        query_results = db_cursor.fetchall()
        subscriptions = [dict(row) for row in query_results]
        serialized_subs = json.dumps(subscriptions)
    return serialized_subs

def retrieve_subscription(pk, url=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                s.id,
                s.follower_id,
                s.author_id,
                s.created_on
            FROM Subscriptions s
            WHERE s.id = ?
            """, (pk,)
        )
        query_results = db_cursor.fetchone()
        dictionary_version = dict(query_results)
        serial_sub = json.dumps(dictionary_version)
    return serial_sub