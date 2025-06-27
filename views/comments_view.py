import sqlite3
import json


def list_comments():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """ 
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
            """,
            (pk,),
        )
        query_results = db_cursor.fetchone()
        dictionary_version = dict(query_results)
        serial_com = json.dumps(dictionary_version)
    return serial_com

def create_comment(comment_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            INSERT INTO Comments (post_id, author_id, content)
            VALUES (?, ?, ?)
            """,
            (comment_data["post_id"], comment_data["author_id"], comment_data["content"])
        )
        new_id = db_cursor.lastrowid

        new_comment = {
            "id": new_id,
            "post_id": comment_data["post_id"],
            "author_id": comment_data["author_id"],
            "content": comment_data["content"]
                    }
        return json.dumps(new_comment)
    
def update_comment(id, comment_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            UPDATE Comments
                SET
                    content = ?
            WHERE id = ?
            """,
            (comment_data["content"], id)
        )
        rows_affected = db_cursor.rowcount
    return True if rows_affected > 0 else False

def delete_comment(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Comments WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
