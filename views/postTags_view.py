import sqlite3
import json


def list_postTags(url=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        expands = []
        if url and "query_params" in url and "_expand" in url["query_params"]:
            expands = url["query_params"]["_expand"]

        # Build the base query
        select_fields = [
            "p.id",
            "p.post_id",
            "p.tag_id"
        ]
        join_clause = ""
        if "post" in expands:
            select_fields += [
                "posts.title AS post_title",
                "posts.content AS post_content"
            ]
            join_clause += " LEFT JOIN Posts posts ON p.post_id = posts.id"
        if "tag" in expands:
            select_fields += [
                "tags.label AS tag_label"
            ]
            join_clause += " LEFT JOIN Tags tags ON p.tag_id = tags.id"

        query = f"""
            SELECT {', '.join(select_fields)}
            FROM PostTags p
            {join_clause}
        """

        db_cursor.execute(query)
        query_results = db_cursor.fetchall()
        post_tags = [dict(row) for row in query_results]
        return json.dumps(post_tags)


def retrieve_postTag(pk, url=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                p.id,
                p.post_id,
                p.tag_id
            FROM PostTags p
            WHERE p.id = ?
            """,
            (pk,),
        )
        query_results = db_cursor.fetchone()
        dictionary_version = dict(query_results)
        serial_post_tag = json.dumps(dictionary_version)
    return serial_post_tag
