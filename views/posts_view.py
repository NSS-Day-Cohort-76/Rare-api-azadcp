import json
import sqlite3


def list_post():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # First: fetch posts with author name and category label
        db_cursor.execute(
            """
            SELECT
                p.id,
                p.user_id,
                u.first_name || ' ' || u.last_name AS author_name,
                p.category_id,
                c.label AS category,
                p.title,
                p.publication_date,
                p.image_url,
                p.content
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
            """
        )
        posts_raw = db_cursor.fetchall()
        posts = [dict(row) for row in posts_raw]

        # Then: fetch all post-tag relationships
        db_cursor.execute(
            """
            SELECT
                pt.post_id,
                t.label AS tag
            FROM PostTags pt
            JOIN Tags t ON pt.tag_id = t.id
            """
        )
        tag_rows = db_cursor.fetchall()

        # Build a dictionary of post_id to tags
        tag_map = {}
        for row in tag_rows:
            tag_map.setdefault(row["post_id"], []).append(row["tag"])

        # Attach tags to each post
        for post in posts:
            post["tags"] = tag_map.get(post["id"], [])

        return json.dumps(posts)


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







# def retrieve_post(pk):
#     with sqlite3.connect("./db.sqlite3") as conn:
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()

#         db_cursor.execute(
#             """
#         SELECT 
#             p.id,
#             p.user_id,
#             p.category_id,
#             p.title,
#             p.publication_date,
#             p.image_url,
#             p.content,
#             p.approved,
#             u.first_name || ' ' || u.last_name AS author_name,
#             u.username
#         FROM "Posts" p
#         JOIN Users u ON p.user_id = u.id
#         WHERE p.id = ? 
#         """,
#             (pk,),
#         )
#         query_results = db_cursor.fetchone()
#         if query_results is None:
#             return json.dumps({"error": "Post not found"})
#         dictionary_version_as_obj = dict(query_results)
#         serialized_post = json.dumps(dictionary_version_as_obj)

#     return serialized_post

# print(f"contents of ${retrieve_post(2)}")
