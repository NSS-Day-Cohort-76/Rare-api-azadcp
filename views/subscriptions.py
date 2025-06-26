import sqlite3
import json
from datetime import datetime

def create_subscription(follower_id, author_id):

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        now = datetime.now().isoformat()

        db_cursor.execute(
            """
            INSERT INTO Subscriptions (follower_id, author_id, created_on)
            VALUES (?, ?, ?)
            """,
            (follower_id, author_id, now),
        )
        conn.commit()

        subscription_id = db_cursor.lastrowid
        return json.dumps({
            "id": subscription_id,
            "follower_id": follower_id,
            "author_id": author_id,
            "created_on": now
        })

def end_subscription(subscription_id):
    """Update the subscription's end datetime to current datetime"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        now = datetime.now().isoformat()

        db_cursor.execute(
            """
            UPDATE Subscriptions
            SET ended_on = ?
            WHERE id = ?
            """,
            (now, subscription_id)
        )
        conn.commit()

        # Optionally return success message or updated subscription
        return json.dumps({"message": "Subscription ended", "subscription_id": subscription_id})

def check_subscription(follower_id, author_id):
    follower_id = int(follower_id)
    author_id = int(author_id)
    print(f"Backend check_subscription called with follower_id={follower_id}, author_id={author_id}")

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Only active subscriptions (where ended_on is NULL)
        db_cursor.execute(
            """
            SELECT *
            FROM Subscriptions
            WHERE follower_id = ? AND author_id = ? AND ended_on IS NULL
            """,
            (follower_id, author_id)
        )
        subscription = db_cursor.fetchone()
        if subscription:
            return json.dumps(dict(subscription))
        else:
            return json.dumps(None)

def list_subscriptions():
    """Return all active subscriptions as JSON list"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT * FROM Subscriptions
            WHERE ended_on IS NULL
        """)

        subscriptions = db_cursor.fetchall()
        return json.dumps([dict(row) for row in subscriptions])

def retrieve_subscription(subscription_id):
    """Return a single subscription by id as JSON"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT * FROM Subscriptions
            WHERE id = ?
        """, (subscription_id,))

        subscription = db_cursor.fetchone()
        if subscription:
            return json.dumps(dict(subscription))
        else:
            return json.dumps(None)

# NEW function to get count of active subscribers for an author
def get_subscriber_count(author_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT COUNT(*) AS subscriber_count
            FROM Subscriptions
            WHERE author_id = ? AND ended_on IS NULL
        """, (author_id,))

        count = db_cursor.fetchone()[0]
        return json.dumps({"subscriber_count": count})
