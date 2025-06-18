from http.server import HTTPServer
from nss_handler import HandleRequests, status
import json
from views.user import login_user, create_user
from views import list_subscriptions, retrieve_subscription
from views import list_comments, retrieve_comment
from views import list_tags, retrieve_tags
from views import list_categories, retrieve_category
from views import list_postTags, retrieve_postTag
from views import list_postReactions, retrieve_postReaction
from views import list_reactions, retrieve_reaction
from views import list_users, retrieve_user


class JSONServer(HandleRequests):

    def do_POST(self):
        url = self.parse_url(self.path)
        content_length = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_length)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "login":
            response = login_user(request_body)
            return self.response(response, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "register":
            response = create_user(request_body)
            return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)

        return self.response(
            json.dumps({"message": "Not found"}),
            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
        )

    def do_GET(self):
        url = self.parse_url(self.path)

        if url["requested_resource"] == "users":
            if url["pk"] != 0:
                return self.response(
                    retrieve_user(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_users(), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "subscriptions":
            if url["pk"] != 0:
                return self.response(
                    retrieve_subscription(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_subscriptions(), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "posts":
            if url["pk"] != 0:
                return self.response(
                    retrieve_post(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_posts(), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "comments":
            if url["pk"] != 0:
                return self.response(
                    retrieve_comment(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_comments(), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "reactions":
            if url["pk"] != 0:
                return self.response(
                    retrieve_reaction(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_reactions(), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "postReactions":
            if url["pk"] != 0:
                return self.response(
                    retrieve_postReaction(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_postReactions(), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "tags":
            if url["pk"] != 0:
                return self.response(
                    retrieve_tags(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_tags(), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "postTags":
            if url["pk"] != 0:
                return self.response(
                    retrieve_postTag(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_postTags(), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "categories":
            if url["pk"] != 0:
                return self.response(
                    retrieve_category(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_categories(), status.HTTP_200_SUCCESS.value)

        else:
            return self.response(
                json.dumps({"message": "Not Implemented"}),
                status.HTTP_500_SERVER_ERROR.value,
            )


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()


# import sqlite3

#             with sqlite3.connect("./db.sqlite3") as conn:
#                 conn.row_factory = sqlite3.Row
#                 db_cursor = conn.cursor()

#                 db_cursor.execute("SELECT id, username, email FROM Users")

#                 users = db_cursor.fetchall()
#                 user_list = [dict(u) for u in users]

#             return self.response(json.dumps(user_list), status.HTTP_200_SUCCESS.value)

#         return self.response(
#             json.dumps({"message": "Not Implemented"}),
#             status.HTTP_501_SERVER_ERROR.value,
#         )
