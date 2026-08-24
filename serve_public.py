import http.server
import socketserver
import threading
import subprocess
import time
import os
import re
import socket

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

PORT = get_free_port()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

# Bind explicitly to 127.0.0.1
httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)

print(f"Local server started on 127.0.0.1:{PORT}")
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
time.sleep(1)

# Forward explicitly 127.0.0.1:PORT
cmd = ["ssh", "-T", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=30", "-R", f"80:127.0.0.1:{PORT}", "serveo.net"]
print(f"Opening public HTTPS internet tunnel for 127.0.0.1:{PORT}...")

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

for line in iter(proc.stdout.readline, ''):
    print(line, end='', flush=True)
    match = re.search(r'https?://[a-zA-Z0-9\-\.]+\.serveousercontent\.com', line) or re.search(r'https?://[a-zA-Z0-9\-\.]+\.serveo\.net', line)
    if match:
        url = match.group(0)
        with open(os.path.join(DIRECTORY, "public_url.txt"), "w") as f:
            f.write(url)
        print("\n=======================================================")
        print(f"WEBSITE IS LIVE ON THE PUBLIC INTERNET!")
        print(f"PUBLIC URL: {url}")
        print("=======================================================\n", flush=True)

proc.wait()
