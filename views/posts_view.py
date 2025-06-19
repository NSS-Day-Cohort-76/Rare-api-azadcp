import json
import sqlite3


def list_posts():
    """Get a list of all posts"""
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
                p.content,
                p.approved,
                u.username,
                u.first_name || ' ' || u.last_name AS author_name,
                c.label AS category
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
            ORDER BY p.publication_date DESC
            """
        )

        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            post = dict(row)

            # Get tags for each post
            db_cursor.execute(
                """
                SELECT t.label
                FROM PostTags pt
                JOIN Tags t ON pt.tag_id = t.id
                WHERE pt.post_id = ?
                """,
                (post["id"],),
            )
            tags = db_cursor.fetchall()
            post["tags"] = [t["label"] for t in tags]

            posts.append(post)

        return json.dumps(posts)


def retrieve_post(pk):
    """Get details for a single post"""
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
                p.content,
                p.approved,
                u.first_name || ' ' || u.last_name AS author_name,
                u.username,
                c.label AS category
            FROM "Posts" p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
            WHERE p.id = ?
            """,
            (pk,),
        )

        post_data = db_cursor.fetchone()

        if post_data is None:
            return json.dumps({"error": "Post not found"})

        post = dict(post_data)

        # Add tags
        db_cursor.execute(
            """
            SELECT t.label
            FROM PostTags pt
            JOIN Tags t ON pt.tag_id = t.id
            WHERE pt.post_id = ?
            """,
            (pk,),
        )
        tags = db_cursor.fetchall()
        post["tags"] = [row["label"] for row in tags]

        return json.dumps(post)
