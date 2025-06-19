import json
import sqlite3

def list_post():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content
        FROM "Posts" p
        """
        )
        query_results = db_cursor.fetchall()

        posts= []
        for row in query_results:
            posts.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_posts = json.dumps(posts)

    return serialized_posts

def retrieve_post(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.content
        FROM "Posts" p
        WHERE id = ? 
        """,
            (pk,),
        )
        query_results = db_cursor.fetchone()
        if query_results is None:
            return json.dumps({"error": "Post not found"})
        dictionary_version_as_obj = dict(query_results)
        serialized_post = json.dumps(dictionary_version_as_obj)
    
    return serialized_post
