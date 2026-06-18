from pyngrok import ngrok
import sys

# Open a HTTP tunnel on port 8000
public_url = ngrok.connect(8000)
print(f"Backend public URL: {public_url}")
print(f"API URL (for Vercel): {public_url}/api/v1")
print("\nKeep this running! Press Ctrl+C to stop.")
sys.stdout.flush()

try:
    ngrok_process = ngrok.get_ngrok_process()
    ngrok_process.proc.wait()
except KeyboardInterrupt:
    print("Shutting down...")
    ngrok.kill()