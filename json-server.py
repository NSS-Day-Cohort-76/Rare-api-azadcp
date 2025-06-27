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
)
from views import (
    list_comments,
    retrieve_comment,
    create_comment,
    update_comment,
    delete_comment,
)
from views import list_tags, retrieve_tags, create_tag, update_tag, delete_tag
from views import (
    list_categories,
    retrieve_category,
    create_category,
    delete_category,
    update_category,
)
from views import list_postTags, retrieve_postTag
from views import list_postReactions, retrieve_postReaction
from views import list_reactions, retrieve_reaction
from views import list_users, retrieve_user
from views import list_post, retrieve_post, create_post, delete_post, update_post
from views import get_subscriber_count


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

        if url["requested_resource"] == "tags":
            response = create_tag(request_body)
            return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)

        if url["requested_resource"] == "posts":
            response = create_post(request_body)
            return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)

        if url["requested_resource"] == "categories":
            response = create_category(request_body)
            return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)

        if url["requested_resource"] == "comments":
            response = create_comment(request_body)
            return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)

        if url["requested_resource"] == "subscriptions":

            follower_id = request_body.get("follower_id")
            author_id = request_body.get("author_id")

            if follower_id and author_id:
                response = create_subscription(follower_id, author_id)
                return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)
            else:
                print(" Missing follower_id or author_id")
                return self.response(
                    json.dumps({"message": "Missing follower_id or author_id"}), 400
                )

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
            if url.get("query_params"):
                follower_id = url["query_params"].get("followerId", [None])[0]
                author_id = url["query_params"].get("authorId", [None])[0]

                if follower_id and author_id:
                    return self.response(
                        check_subscription(follower_id, author_id),
                        status.HTTP_200_SUCCESS.value,
                    )

                if author_id and not follower_id:
                    response = get_subscriber_count(author_id)
                    return self.response(response, status.HTTP_200_SUCCESS.value)

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
            if url.get("query_params"):
                return self.response(
                    list_post(url.get("query_params")), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_post(), status.HTTP_200_SUCCESS.value)

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
            return self.response(list_postTags(url), status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "categories":
            if url["pk"] != 0:
                return self.response(
                    retrieve_category(url["pk"]), status.HTTP_200_SUCCESS.value
                )
            return self.response(list_categories(), status.HTTP_200_SUCCESS.value)

        return self.response(
            json.dumps({"message": "Not Implemented"}),
            status.HTTP_500_SERVER_ERROR.value,
        )

    def do_PUT(self):
        url = self.parse_url(self.path)
        pk = url["pk"]

        if (
            url["requested_resource"] == "subscriptions"
            and self.path.endswith("/end")
            and pk != 0
        ):
            response = end_subscription(pk)
            return self.response(
                response, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
            )

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "tags":
            if pk != 0:
                successfully_updated = update_tag(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                else:
                    return self.response(
                        json.dumps({"message": "Tag not found or not updated"}),
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )

        if url["requested_resource"] == "categories":
            if pk != 0:
                successfully_updated = update_category(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                else:
                    return self.response(
                        json.dumps({"message": "Category not found or not updated"}),
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )

        if url["requested_resource"] == "comments":
            if pk != 0:
                successfully_updated = update_comment(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                else:
                    return self.response(
                        json.dumps({"message": "Comment not found or not updated"}),
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )
        if url["requested_resource"] == "posts":
            if pk != 0:
                successfully_updated = update_post(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                else:
                    return self.response(
                        json.dumps({"message": "Post not found or not updated"}),
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )


        return self.response(
            json.dumps({"message": "Requested resource not found"}),
            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
        )

    def do_DELETE(self):
        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "tags":
            if pk != 0:
                successfully_deleted = delete_tag(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        if url["requested_resource"] == "categories":
            if pk != 0:
                successfully_deleted = delete_category(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        if url["requested_resource"] == "comments":
            if pk != 0:
                successfully_deleted = delete_comment(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        if url["requested_resource"] == "posts":
            if pk != 0:
                successfully_deleted = delete_post(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        return self.response(
            "Requested resource not found",
            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
        )


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
