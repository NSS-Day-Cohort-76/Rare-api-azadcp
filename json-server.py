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


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
