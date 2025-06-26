import json
import sqlite3


def list_post(query_params=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Handle query: ?userId=1&countOnly=true
        if (
            query_params
            and query_params.get("countOnly")
            and query_params.get("userId")
        ):
            user_id = int(query_params["userId"][0])
            db_cursor.execute(
                "SELECT COUNT(*) AS post_count FROM Posts WHERE user_id = ?", (user_id,)
            )
            result = db_cursor.fetchone()
            return json.dumps({"count": result["post_count"]})

        #  Otherwise, continue as normal
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

        # Fetch tags
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

        tag_map = {}
        for row in tag_rows:
            tag_map.setdefault(row["post_id"], []).append(row["tag"])

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
                p.image_url,
                p.content,
                p.approved,
                u.first_name || ' ' || u.last_name AS author_name,
                u.username
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            WHERE p.id = ?
            """,
            (pk,),
        )

        data = db_cursor.fetchone()
        if data:
            return dict(data)
        return {}


def create_post(post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Posts ( user_id, category_id, title, publication_date, image_url, content, approved)
            VALUES ( ?, ?, ?, ?, ?, ?, ? )
            """,
            (
                post_data["user_id"],
                post_data["category_id"],
                post_data["title"],
                post_data["publication_date"],
                post_data["image_url"],
                post_data["content"],
                post_data["approved"],
            ),
        )
        new_id = db_cursor.lastrowid

        new_post = {
            "id": new_id,
            "user_id": post_data["user_id"],
            "title": post_data["title"],
            "publication_date": post_data["publication_date"],
            "image_url": post_data["image_url"],
            "content": post_data["content"],
            "approved": post_data["approved"],
        }
        return json.dumps(new_post)
