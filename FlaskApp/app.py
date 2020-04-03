from http.server import SimpleHTTPRequestHandler, HTTPServer

server = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
server.serve_forever()