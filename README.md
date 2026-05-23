# CloudGuardian

CloudGuardian is an experimental DevStack/OpenStack plugin for cloud security monitoring and resource optimization.

## Features

- VM resource monitoring simulation
- Security risk analysis
- Automatic alert generation
- Optimization recommendations
- DevStack plugin integration

## Endpoints

- `/` service status
- `/metrics` simulated VM metrics
- `/analyze` anomaly analysis
- `/alerts` generated alerts

## DevStack integration

Add this line to your `local.conf`:

```ini
enable_plugin cloudguardian https://github.com/TUO_USERNAME/cloudguardian.git main
