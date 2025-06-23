import sqlite3
import json


def list_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                t.id,
                t.label
            FROM Tags t
            ORDER BY t.label ASC
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
                t.label
            FROM Tags t
            WHERE t.id = ?
            """,
            (pk,),
        )
        query_results = db_cursor.fetchone()
        dictionary_version = dict(query_results)
        serial_t = json.dumps(dictionary_version)
    return serial_t


def create_tag(tag_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Tags ( label)
            VALUES ( ? )
            """,
            (tag_data["label"],),
        )
        new_id = db_cursor.lastrowid

        new_tag = {"id": new_id, "label": tag_data["label"]}
        return json.dumps(new_tag)
    
def update_tag(id, tag_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Tags
                SET
                    label = ?
            WHERE id = ?
            """,
            (tag_data['label'], id)
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False

def delete_tag(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Tags WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
