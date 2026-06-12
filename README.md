# CloudGuardian

CloudGuardian is a DevStack/OpenStack plugin designed for cloud VM monitoring, threat assessment and automatic remediation.

## Features

- OpenStack VM monitoring
- Threat Score calculation
- Security risk classification
- Automatic alert generation
- Auto-remediation for SHUTOFF VMs
- REST API integration
- DevStack plugin integration
- GitHub-based deployment

---

## Architecture

OpenStack → CloudGuardian Plugin → REST API → Threat Analysis → Remediation Engine

The plugin retrieves VM information from OpenStack using the OpenStack CLI and analyzes their operational status.

---

## Threat Score Model

| VM Status | Threat Score | Risk |
|------------|------------|------------|
| ACTIVE | 10 | Low |
| SHUTOFF | 50 | Medium |
| BUILD | 70 | Medium |
| ERROR | 100 | High |

---

## Available Endpoints

### Service Status

```bash
curl http://localhost:9090/
```

### VM Inventory

```bash
curl http://localhost:9090/servers
```

### Threat Analysis

```bash
curl http://localhost:9090/analyze
```

### Alerts History

```bash
curl http://localhost:9090/alerts
```

### Auto Remediation

```bash
curl http://localhost:9090/remediate
```

---

## DevStack Integration

Add the plugin to local.conf:

```ini
enable_plugin cloudguardian https://github.com/prince97av/cloudguardian.git main
```

Then execute:

```bash
./stack.sh
```

---

## Demonstration Scenario

1. Create a VM in OpenStack
2. Analyze the VM using CloudGuardian
3. Shut down the VM
4. Detect the increased threat score
5. Execute auto-remediation
6. Verify VM recovery

---

## Technologies

- OpenStack DevStack
- Python 3
- REST API
- Systemd
- GitHub
- OpenStack CLI

---

## Future Developments

- Machine Learning anomaly detection
- Web Dashboard
- Resource optimization engine
- Predictive risk analysis
