from http.server import BaseHTTPRequestHandler, HTTPServer

class MyServerHandler(BaseHTTPRequestHandler): # 新しいServerHandlerのクラスを作成
    def do_GET(self):
        self.send_response_only(200)
        self.end_headers()
        self.wfile.write(b'It is from MySercer Handler') # HTML情報を送信
        return

server = HTTPServer(('', 8000), MyServerHandler) # 自分で定義したServerHandleを使用
server.serve_forever()