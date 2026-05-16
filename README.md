# Booster RPC

Python client for controlling Booster K1 humanoid robots via gRPC and WebSocket.

## Installation

```bash
pip install booster-rpc
```

## Usage

```python
from booster_rpc import BoosterConnection

k1 = BoosterConnection()
k1_status = k1.get_status()
print(f"Current mode: {k1_status.mode.name}")
print(f"Current model: {k1_status.robot_info.model}")
```
