import argparse
import json
import threading
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
LOG_PATH = ROOT / "device-log.jsonl"
MAX_BODY_BYTES = 256 * 1024
LOG_LOCK = threading.Lock()


class LanLoggerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if urlsplit(self.path).path == "/device-log.jsonl":
            self.send_error(404, "Diagnostic logs are not served over HTTP")
            return
        super().do_GET()

    def do_POST(self):
        if urlsplit(self.path).path != "/log":
            self.send_error(404, "Unknown logging endpoint")
            return

        try:
            body_size = int(self.headers.get("Content-Length", "0"))
            if body_size <= 0 or body_size > MAX_BODY_BYTES:
                raise ValueError("Invalid request size")
            payload = json.loads(self.rfile.read(body_size))
            if not isinstance(payload, dict):
                raise ValueError("Expected a JSON object")
            events = payload.get("events")
            if not isinstance(events, list) or len(events) > 200:
                raise ValueError("Expected up to 200 events")
            if any(not isinstance(event, dict) for event in events):
                raise ValueError("Each event must be an object")
        except (ValueError, json.JSONDecodeError) as error:
            self.send_error(400, str(error))
            return

        device = payload.get("device", {})
        if not isinstance(device, dict):
            device = {}
        session_id = str(payload.get("sessionId", "unknown"))[:80]
        client_ip = self.client_address[0]
        with LOG_LOCK, LOG_PATH.open("a", encoding="utf-8") as log_file:
            for event in events:
                record = {
                    **event,
                    "receivedAt": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
                    "clientIp": client_ip,
                    "sessionId": session_id,
                    "device": device,
                }
                log_file.write(json.dumps(record, ensure_ascii=False) + "\n")
            log_file.flush()

        self.send_response(204)
        self.end_headers()
        self.log_message("wrote %d event(s) to %s", len(events), LOG_PATH.name)


def main():
    parser = argparse.ArgumentParser(description="Serve Pixel Saturation and receive LAN diagnostics")
    parser.add_argument("--host", default="0.0.0.0", help="Interface to bind (default: all interfaces)")
    parser.add_argument("--port", type=int, default=8000, help="HTTP port (default: 8000)")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), LanLoggerHandler)
    print(f"Serving {ROOT} on http://{args.host}:{args.port}/")
    print(f"Device events will be appended to {LOG_PATH}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping LAN logger.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
