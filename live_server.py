import http.server
import socketserver
import threading
import subprocess
import time
import os
import re
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

# Start HTTP Server in background thread
t = threading.Thread(target=start_server, daemon=True)
t.start()
time.sleep(1)

# Start Pinggy SSH tunnel
cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=30", "-p", "443", "-R0:localhost:8080", "a.pinggy.io"]

try:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    
    url_found = False
    for line in iter(proc.stdout.readline, ''):
        print(line, end='', flush=True)
        match = re.search(r'https?://[a-zA-Z0-9\-\.]+\.(?:pinggy\.link|free\.pinggy\.link|pinggy\.io)', line)
        if match and not url_found:
            url = match.group(0)
            url_found = True
            with open(os.path.join(DIRECTORY, "public_url.txt"), "w") as f:
                f.write(url)
            print(f"\n=======================================================")
            print(f"🎉 WEBSITE IS LIVE ON THE PUBLIC INTERNET!")
            print(f"🌐 PUBLIC URL: {url}")
            print(f"=======================================================\n")
    proc.wait()
except Exception as e:
    print(f"Tunnel error: {e}")
