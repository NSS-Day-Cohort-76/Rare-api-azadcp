from http.server import HTTPServer
from nss_handler import HandleRequests, status
import json
from views.user import login_user, create_user


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
            import sqlite3

            with sqlite3.connect("./db.sqlite3") as conn:
                conn.row_factory = sqlite3.Row
                db_cursor = conn.cursor()

                db_cursor.execute("SELECT id, username, email FROM Users")

                users = db_cursor.fetchall()
                user_list = [dict(u) for u in users]

            return self.response(json.dumps(user_list), status.HTTP_200_SUCCESS.value)

        return self.response(
            json.dumps({"message": "Not Implemented"}),
            status.HTTP_501_SERVER_ERROR.value,
        )


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
