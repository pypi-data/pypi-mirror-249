import http.server
import socketserver
import threading
import webbrowser
import os
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).resolve().parent

class LocalHost(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stop':
            print("Local host is stopping...")
            threading.Thread(target=self.shutdown).start()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Local host is stopping...')
        else:
            super().do_GET()

    def shutdown(self):
        self.server.shutdown()

    @staticmethod
    def run_server():
        os.chdir(DIRECTORY)
        with socketserver.TCPServer(("", PORT), LocalHost) as httpd:
            print(f"Serving at http://localhost:{PORT}")
            webbrowser.open_new(f'http://localhost:{PORT}/static/html/main.html')
            httpd.serve_forever()
            
