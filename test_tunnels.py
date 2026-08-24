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
        httpd.serve_forever()

t = threading.Thread(target=start_server, daemon=True)
t.start()
time.sleep(1)

# Connect with serveo.net
cmd = ["ssh", "-T", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=30", "-R", "80:localhost:8080", "serveo.net"]

print("Starting public internet tunnel via Serveo...")
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

for line in iter(proc.stdout.readline, ''):
    print(line, end='', flush=True)
    match = re.search(r'https?://[a-zA-Z0-9\-\.]+\.serveo\.net', line)
    if match:
        url = match.group(0)
        with open(os.path.join(DIRECTORY, "public_url.txt"), "w") as f:
            f.write(url)
        print(f"\n=======================================================")
        print(f"🎉 WEBSITE IS LIVE ON THE PUBLIC INTERNET!")
        print(f"🌐 PUBLIC URL: {url}")
        print(f"=======================================================\n", flush=True)

proc.wait()
