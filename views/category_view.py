import sqlite3
import json


def list_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                c.id,
                c.label
                
            FROM Categories c
            
            """
        )
        query_results = db_cursor.fetchall()
        categories = [dict(row) for row in query_results]
        serialized_categories = json.dumps(categories)
    return serialized_categories


def retrieve_category(pk, url=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                c.id,
                c.label
                
            FROM Categories c
            WHERE c.id = ?
            """,
            (pk,),
        )
        query_results = db_cursor.fetchone()
        dictionary_version = dict(query_results)
        serial_category = json.dumps(dictionary_version)
    return serial_category

def create_category(request_body):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO Categories (label)
            VALUES (?)
        """, (request_body["label"],))

        category_id = db_cursor.lastrowid

        return json.dumps({
            "id": category_id,
            "label": request_body["label"]
        })

def delete_category(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Categories 
        WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False

# print(f"contents of ${list_categories()}")
