import os
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.getenv('PORT', 8080))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def _handle_request(self):
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                template = f.read()
            html = template.format(path=self.path)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
            logging.info(f"Request: {self.path}")
        except FileNotFoundError:
            self.send_error(404, "Template not found")
        except Exception as e:
            logging.error(f"Error: {e}")
            self.send_error(500, "Internal Server Error")

def main():
    server = HTTPServer(('', PORT), Handler)
    logging.info(f"Starting server on port {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info("Server stopped")

if __name__ == '__main__':
    main()