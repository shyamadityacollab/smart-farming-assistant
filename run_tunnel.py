import http.server
import socketserver
import threading
import subprocess
import time
import os
import re

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Local server serving at http://localhost:{PORT}")
        httpd.serve_forever()

# Start HTTP Server in background thread
t = threading.Thread(target=start_server, daemon=True)
t.start()
time.sleep(1)

# Start SSH Tunnel via Pinggy or Serveo
cmd = ["ssh", "-p", "443", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=30", "-R0:localhost:8080", "a.pinggy.io"]
print("Connecting to live public internet tunnel...")

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

with open(os.path.join(DIRECTORY, "live_url.txt"), "w") as url_file:
    for line in iter(process.stdout.readline, ''):
        print(line, end='')
        match = re.search(r'https?://[a-zA-Z0-9\-\.]+\.pinggy\.link', line)
        if match:
            url = match.group(0)
            url_file.write(url)
            url_file.flush()
            print(f"\n============================================\nSUCCESS! LIVE URL: {url}\n============================================\n")

process.wait()
