import http.server,socketserver,os

port = 65000
# Handler = http.server.SimpleHTTPRequestHandler

class ImageHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("html"):
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        elif self.path.endswith(("jpeg","jpg")):
            f = open(self.path[1:], 'rb')
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        elif self.path.endswith("png"):
            f = open(self.path[1:], 'rb')
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        elif self.path.endswith("ico"):
            self.send_response(404)
        elif self.path.endswith(("py","json","css")):
            f = open(self.path[1:], 'rb')
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            dir_list = os.listdir(os.path.join(os.curdir,self.path.split('/')[1]))
            head = "<html><head><title>Directory listing for /</title></head>"
            html = "<body><h1>Directory listing for /</h1><hr><ul>"
            for item in dir_list:
                if os.path.isdir(item):
                    html += f"<li><a href='{self.path}{item}/'>{item}</a></li>"
                else:
                    html += f"<li><a href='{self.path}{item}'>{item}</a></li>"
            self.wfile.write((head+html+"</ul><hr></body></html>").encode())

Handler = ImageHandler

with socketserver.TCPServer(("",port),Handler) as http_server:
    http_server.serve_forever()
