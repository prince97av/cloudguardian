from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import time

alerts = []

def run_cmd(cmd):
    try:
        result = subprocess.check_output(
            cmd,
            shell=True,
            text=True,
            stderr=subprocess.STDOUT,
            executable="/bin/bash"
        )
        return result.strip()
    except subprocess.CalledProcessError as e:
        return "ERROR: " + e.output.strip()

def openstack_cmd(command):
    return run_cmd(
        f"source /opt/stack/devstack/openrc admin admin && {command}"
    )

def get_servers():
    output = openstack_cmd("openstack server list -f json")

    if output.startswith("ERROR:"):
        return {"error": output}

    try:
        return json.loads(output)
    except Exception:
        return {"error": output}

def calculate_risk(status):
    status = status.upper()

    if status == "ACTIVE":
        return 10, "low", "no action required"

    if status == "SHUTOFF":
        return 50, "medium", "VM is powered off: verify if this is expected or restart it"

    if status == "BUILD":
        return 70, "medium", "VM still in BUILD: verify resources, image and Neutron network"

    if status == "ERROR":
        return 100, "high", "VM in ERROR state: check image, flavor, network or Nova logs"

    return 40, "medium", f"Unknown VM status: {status}"

def analyze_servers():
    servers = get_servers()

    if isinstance(servers, dict) and "error" in servers:
        return {
            "status": "error",
            "message": servers["error"]
        }

    results = []

    for vm in servers:
        name = vm.get("Name", "unknown")
        status = vm.get("Status", "unknown")

        threat_score, risk, recommendation = calculate_risk(status)

        alert = {
            "timestamp": time.strftime("%Y-%m-%d%H:%M:%S"),
            "vm_name": name,
            "status": status,
            "threat_score": threat_score,
            "risk": risk,
            "recommendation": recommendation
        }

        results.append(alert)

        if risk != "low":
            alerts.append(alert)

    return results

def remediate_servers():
    servers = get_servers()

    if isinstance(servers, dict) and "error" in servers:
        return {
            "status": "error",
            "message": servers["error"]
        }

    actions = []

    for vm in servers:
        name = vm.get("Name", "unknown")
        status = vm.get("Status", "unknown").upper()

        if status == "SHUTOFF":
            output = openstack_cmd(f"openstack server start {name}")
            action = {
                "vm_name": name,
                "previous_status": status,
                "action": "server_start",
                "result": output if output else "start command  executed"
            }

        elif status == "ERROR":
            action = {
                "vm_name": name,
                "previous_status": status,
                "action": "manual_check_required",
                "result": "VM is in ERROR state. Automatic remediation skipped for safety."
            }

        else:
            action = {
                "vm_name": name,
                "previous_status": status,
                "action": "none",
                "result": "No remedation required"
            }

        actions.append(action)

    return actions

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
                "description": "OpenStack VM monitoring and anomaly recommendation plugin",
                "endpoints": ["/servers", "/analyze", "/alerts", "/remediate"]
            })

        elif self.path == "/servers":
            self._send_json(get_servers())

        elif self.path == "/analyze":
            self._send_json(analyze_servers())

        elif self.path == "/alerts":
            self._send_json(alerts)

        elif self.path == "/remediate":
            self._send_json(remediate_servers())

        else:
            self._send_json({"error": "endpoint not found"}, 404)

server = HTTPServer(("0.0.0.0", 9090), Handler)
print("CloudGuardian running on port 9090")
server.serve_forever()
