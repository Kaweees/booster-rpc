# Booster RPC

Python client for controlling Booster K1 and T1 humanoid robots via gRPC and WebSocket.

## Installation

```bash
pip install booster-rpc
```

## Usage

```python
from booster_rpc import K1Connection

k1 = K1Connection()
k1_status = k1.get_status()
print(f"Current mode: {k1_status.mode.name}")
print(f"Current model: {k1_status.robot_info.model}")
```

```python
from booster_rpc import T1Connection

t1 = T1Connection()
t1_status = t1.get_status()
print(f"Current mode: {t1_status.mode.name}")
print(f"Current model: {t1_status.robot_info.model}")
```
