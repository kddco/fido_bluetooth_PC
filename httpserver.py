from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/send2UI'):
            # 解析查詢參數
            query_params = parse_qs(self.path[9:])  # 去掉路由部分，只保留參數部分
            name = query_params.get('name', [''])[0]  # 讀取名稱參數，預設為空字串

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            response = f'Hello, {name}! This is the response for /send2UI route.'
            self.wfile.write(response.encode())  # 將回應內容轉為位元組並回傳
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def main():
    host = 'localhost'
    port = 8000

    server = HTTPServer((host, port), RequestHandler)
    print(f'Starting server on {host}:{port}')

    server.serve_forever()

if __name__ == '__main__':
    main()
