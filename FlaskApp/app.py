from http.server import SimpleHTTPRequestHandler, HTTPServer

server = HTTPServer(('', 8000), SimpleHTTPRequestHandler) # サーバーを定義
server.serve_forever() # サーバーを常に稼働させる HTTPServer のメソッド