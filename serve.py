import http.server
import socketserver
import os

PORT = 8001

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    # Change directory to the script's directory to serve files correctly
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)
    
    handler = CORSHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[Thoughts Matrix v2] Server running at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
