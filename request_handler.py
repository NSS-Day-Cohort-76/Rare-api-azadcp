from http.server import HTTPServer
from nss_handler import HandleRequests

HOST = ""
PORT = 8000

with HTTPServer((HOST, PORT), HandleRequests) as server:
    print("🟢 Server is running on port 8000...")
    server.serve_forever()
