import json
import sqlite3


def list_post(query_params=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # 🔍 Check for special query: countOnly for a user's posts
        if (
            query_params
            and query_params.get("countOnly")
            and query_params.get("userId")
        ):
            user_id = int(query_params["userId"][0])
            db_cursor.execute(
                "SELECT COUNT(*) AS post_count FROM Posts WHERE user_id = ?",
                (user_id,),
            )
            result = db_cursor.fetchone()
            return json.dumps({"count": result["post_count"]})

        # 🔥 Otherwise, get all posts with authors and categories
        sql = """
            SELECT
                p.id,
                p.user_id,
                u.first_name || ' ' || u.last_name AS author_name,
                u.username,
                p.category_id,
                c.label AS category,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
        """

        params = []

        # ✅ Optional: filter by category_id
        if query_params and query_params.get("category_id"):
            sql += " WHERE p.category_id = ?"
            params.append(int(query_params["category_id"][0]))

        db_cursor.execute(sql, params)
        posts_raw = db_cursor.fetchall()

        # Convert to list of dictionaries
        posts = [dict(row) for row in posts_raw]

        # 🔗 Get tags for all posts
        db_cursor.execute(
            """
            SELECT
                pt.post_id,
                t.id,
                t.label
            FROM PostTags pt
            JOIN Tags t ON pt.tag_id = t.id
            """
        )
        tag_rows = db_cursor.fetchall()

        # Map tags to post IDs
        tag_map = {}
        for row in tag_rows:
            tag_map.setdefault(row["post_id"], []).append(
                {"id": row["id"], "label": row["label"]}
            )

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
                u.first_name || ' ' || u.last_name AS author_name,
                u.username,
                p.category_id,
                c.label AS category,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
            WHERE p.id = ?
            """,
            (pk,),
        )

        data = db_cursor.fetchone()

        if data is None:
            return json.dumps({"error": "Post not found"})

        # 🔥 Build the dictionary manually
        post = {
            "id": data["id"],
            "user_id": data["user_id"],
            "author_name": data["author_name"],
            "username": data["username"],
            "category_id": data["category_id"],
            "category": data["category"],
            "title": data["title"],
            "publication_date": data["publication_date"],
            "image_url": data["image_url"],
            "content": data["content"],
            "approved": data["approved"],
        }

        # 🔗 Now fetch tags for this one post
        db_cursor.execute(
            """
            SELECT t.id, t.label
            FROM PostTags pt
            JOIN Tags t ON pt.tag_id = t.id
            WHERE pt.post_id = ?
            """,
            (pk,),
        )
        tag_rows = db_cursor.fetchall()
        post["tags"] = [{"id": row["id"], "label": row["label"]} for row in tag_rows]

    return json.dumps(post)


def create_post(post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
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
            "category_id": post_data["category_id"],
            "title": post_data["title"],
            "publication_date": post_data["publication_date"],
            "image_url": post_data["image_url"],
            "content": post_data["content"],
            "approved": post_data["approved"],
        }

        return json.dumps(new_post)


def delete_post(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        DELETE FROM Posts WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
