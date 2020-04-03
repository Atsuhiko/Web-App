from http.server import BaseHTTPRequestHandler, HTTPServer

class MyServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response_only(200)
        self.end_headers()
        self.wfile.write(b'It is from MySercer Handler')
        return

server = HTTPServer(('', 8000), MyServerHandler)
server.serve_forever()