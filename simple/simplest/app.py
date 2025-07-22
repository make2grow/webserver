from http.server import SimpleHTTPRequestHandler, HTTPServer

server_address = ('', 80)  # Serve on all interfaces, port 8000
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print('Serving on port 8000...')
httpd.serve_forever()
