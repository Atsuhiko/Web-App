from http.server import BaseHTTPRequestHandler, HTTPServer

with open('index2.html', mode='r', encoding='utf-8') as f:
    index = f.read()

class MyServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response_only(200)
        self.end_headers()
        body = index.format(title='Formatted Text', content='整形済みのテキストです')
        self.wfile.write(body.encode('utf-8'))
        return

server = HTTPServer(('', 8000), MyServerHandler)
server.serve_forever()