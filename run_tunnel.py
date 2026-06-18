import subprocess
import re
import sys
import time
import os

# Run localtunnel and pipe "y" to accept the install prompt
proc = subprocess.Popen(
    ["npx", "localtunnel@2.0.2", "--port", "8000"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

# Send "y" to accept the prompt
proc.stdin.write("y\n")
proc.stdin.flush()

url = None
for line in iter(proc.stdout.readline, ''):
    print(line, end='', flush=True)
    if "your url is:" in line:
        url = line.split("your url is:")[-1].strip()
        print(f"\n{'='*60}")
        print(f"PUBLIC BACKEND URL: {url}")
        print(f"API URL: {url}/api/v1")
        print(f"{'='*60}")
        break
    if "already" in line.lower() and "used" in line.lower() and "subdomain" in line.lower():
        continue

if url:
    print("\nTunnel is running! Keep this window open.")
    print("Press Ctrl+C to stop the tunnel.\n")

# Keep running
try:
    for line in iter(proc.stdout.readline, ''):
        print(line, end='', flush=True)
except KeyboardInterrupt:
    proc.terminate()
    print("\nTunnel stopped.")