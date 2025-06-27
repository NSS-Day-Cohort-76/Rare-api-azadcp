from http.server import HTTPServer
from nss_handler import HandleRequests, status
import json

from views.user import login_user, create_user
from views import (
    list_subscriptions,
    retrieve_subscription,
    end_subscription,
    create_subscription,
    check_subscription,
    list_comments,
    retrieve_comment,
    create_comment,
    update_comment,
    delete_comment,
    list_tags,
    retrieve_tags,
    create_tag,
    update_tag,
    delete_tag,
    list_categories,
    retrieve_category,
    create_category,
    delete_category,
    update_category,
    list_postTags,
    retrieve_postTag,
    list_postReactions,
    retrieve_postReaction,
    list_reactions,
    retrieve_reaction,
    list_users,
    retrieve_user,
    list_post,
    retrieve_post,
    create_post,
    delete_post,
    update_post,
    get_subscriber_count,
)

class JSONServer(HandleRequests):
    def do_POST(self):
        url = self.parse_url(self.path)
        length = int(self.headers.get("content-length", 0))
        body = json.loads(self.rfile.read(length))

        if url["requested_resource"] == "login":
            return self.response(login_user(body), status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "register":
            return self.response(create_user(body), status.HTTP_201_SUCCESS_CREATED.value)

        if url["requested_resource"] == "tags":
            return self.response(create_tag(body), status.HTTP_201_SUCCESS_CREATED.value)

        if url["requested_resource"] == "posts":
            return self.response(create_post(body), status.HTTP_201_SUCCESS_CREATED.value)

        if url["requested_resource"] == "categories":
            return self.response(create_category(body), status.HTTP_201_SUCCESS_CREATED.value)

        if url["requested_resource"] == "comments":
            return self.response(create_comment(body), status.HTTP_201_SUCCESS_CREATED.value)

        if url["requested_resource"] == "subscriptions":
            follower_id = body.get("follower_id")
            author_id   = body.get("author_id")
            if follower_id and author_id:
                return self.response(
                    create_subscription(follower_id, author_id),
                    status.HTTP_201_SUCCESS_CREATED.value
                )
            else:
                return self.response(
                    json.dumps({"message": "Missing follower_id or author_id"}),
                    400
                )

        return self.response(
            json.dumps({"message": "Not found"}),
            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
        )

    def do_GET(self):
        url = self.parse_url(self.path)

        # --- Users ---
        if url["requested_resource"] == "users":
            if url["pk"] != 0:
                return self.response(retrieve_user(url["pk"]), status.HTTP_200_SUCCESS.value)
            return self.response(list_users(), status.HTTP_200_SUCCESS.value)

        # --- Subscriptions ---
        if url["requested_resource"] == "subscriptions":
            qp = url.get("query_params", {})
            follower_id = qp.get("followerId", [None])[0]
            author_id   = qp.get("authorId",   [None])[0]

            if follower_id and author_id:
                return self.response(check_subscription(follower_id, author_id), status.HTTP_200_SUCCESS.value)

            if author_id and not follower_id:
                return self.response(get_subscriber_count(author_id), status.HTTP_200_SUCCESS.value)

            if url["pk"] != 0:
                return self.response(retrieve_subscription(url["pk"]), status.HTTP_200_SUCCESS.value)

            return self.response(list_subscriptions(), status.HTTP_200_SUCCESS.value)

        # --- Posts ---
        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                return self.response(retrieve_post(url["pk"]), status.HTTP_200_SUCCESS.value)

            qp = url.get("query_params")
            # Route through list_post, which now handles countOnly, subscribedTo, category_id, etc.
            return self.response(list_post(qp), status.HTTP_200_SUCCESS.value)

        # --- Comments ---
        if url["requested_resource"] == "comments":
            if url["pk"] != 0:
                return self.response(retrieve_comment(url["pk"]), status.HTTP_200_SUCCESS.value)
            return self.response(list_comments(), status.HTTP_200_SUCCESS.value)

        # --- Reactions ---
        if url["requested_resource"] == "reactions":
            if url["pk"] != 0:
                return self.response(retrieve_reaction(url["pk"]), status.HTTP_200_SUCCESS.value)
            return self.response(list_reactions(), status.HTTP_200_SUCCESS.value)

        # --- PostReactions ---
        if url["requested_resource"] == "postReactions":
            if url["pk"] != 0:
                return self.response(retrieve_postReaction(url["pk"]), status.HTTP_200_SUCCESS.value)
            return self.response(list_postReactions(), status.HTTP_200_SUCCESS.value)

        # --- Tags ---
        if url["requested_resource"] == "tags":
            if url["pk"] != 0:
                return self.response(retrieve_tags(url["pk"]), status.HTTP_200_SUCCESS.value)
            return self.response(list_tags(), status.HTTP_200_SUCCESS.value)

        # --- PostTags ---
        if url["requested_resource"] == "postTags":
            if url["pk"] != 0:
                return self.response(retrieve_postTag(url["pk"]), status.HTTP_200_SUCCESS.value)
            return self.response(list_postTags(), status.HTTP_200_SUCCESS.value)

        # --- Categories ---
        if url["requested_resource"] == "categories":
            if url["pk"] != 0:
                return self.response(retrieve_category(url["pk"]), status.HTTP_200_SUCCESS.value)
            return self.response(list_categories(), status.HTTP_200_SUCCESS.value)

        return self.response(
            json.dumps({"message": "Not Implemented"}),
            status.HTTP_500_SERVER_ERROR.value
        )

    def do_PUT(self):
        url = self.parse_url(self.path)
        pk = url["pk"]
        resource = url["requested_resource"]

        # End a subscription
        if resource == "subscriptions" and self.path.endswith("/end") and pk != 0:
            return self.response(end_subscription(pk), status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        length = int(self.headers.get("content-length", 0))
        body   = json.loads(self.rfile.read(length))

        # --- Tag update ---
        if resource == "tags" and pk != 0:
            if update_tag(pk, body):
                return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
            return self.response(json.dumps({"message": "Tag not found or not updated"}), status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        # --- Category update ---
        if resource == "categories" and pk != 0:
            if update_category(pk, body):
                return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
            return self.response(json.dumps({"message": "Category not found or not updated"}), status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

          # --- Comment update ---
        if resource == "comments" and pk != 0:
            if update_comment(pk, body):
                return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
            return self.response(json.dumps({"message": "Comment not found or not updated"}), status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        if resource == "posts" and pk != 0:
                successfully_updated = update_post(pk, body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                else:
                    return self.response(
                        json.dumps({"message": "Post not found or not updated"}),
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )

        return self.response(json.dumps({"message": "Requested resource not found"}), status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_DELETE(self):
        url = self.parse_url(self.path)
        pk = url["pk"]
        res = url["requested_resource"]

        if res == "tags" and pk != 0:
            if delete_tag(pk):
                return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        if res == "categories" and pk != 0:
            if delete_category(pk):
                return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        if res == "comments" and pk != 0:
            if delete_comment(pk):
                return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        if res == "posts" and pk != 0:
            if delete_post(pk):
                return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()
