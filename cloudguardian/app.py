from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
import time

alerts = []

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_GET(self):
        if self.path == "/":
            self._send_json({
                "service": "CloudGuardian",
                "status": "running",
                "description": "OpenStack security and optimization plugin"
            })

        elif self.path == "/metrics":
            data = {
                "cpu_usage": random.randint(10, 95),
                "ram_usage": random.randint(10, 95),
                "network_risk": random.choice(["low", "medium", "high"])
            }
            self._send_json(data)

        elif self.path == "/analyze":
            cpu = random.randint(10, 95)
            ram = random.randint(10, 95)
            risk = random.choice(["low", "medium", "high"])

            recommendation = "No action required"

            if cpu > 80 or ram > 80 or risk == "high":
                recommendation = "Possible anomaly detected: consider resizing or isolating VM"

            alert = {
                "timestamp": time.time(),
                "cpu_usage": cpu,
                "ram_usage": ram,
                "network_risk": risk,
                "recommendation": recommendation
            }

            alerts.append(alert)
            self._send_json(alert)

        elif self.path == "/alerts":
            self._send_json(alerts)

        else:
            self._send_json({"error": "endpoint not found"}, 404)

server = HTTPServer(("0.0.0.0", 9090), Handler)
print("CloudGuardian running on port 9090")
server.serve_forever()
