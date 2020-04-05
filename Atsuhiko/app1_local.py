from http.server import BaseHTTPRequestHandler, HTTPServer

with open('index1.html', mode='r', encoding='utf-8') as f:
    index = f.read() # self.wfile.write() で引用される変数

class MyServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response_only(200)
        self.end_headers()
        self.wfile.write(index.encode('utf-8')) # 送信する内容をHTMLファイルから引用
        return

server = HTTPServer(('', 8000), MyServerHandler)
server.serve_forever()