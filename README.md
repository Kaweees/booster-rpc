# Booster RPC

Python client for controlling Booster K1 and T1 humanoid robots via gRPC and WebSocket.

## Installation

```bash
pip install booster-rpc
```

## Usage

> [!NOTE]
> The `with` block closes the connection automatically.

### Booster K1

```python
from booster_rpc import K1Connection

with K1Connection() as k1:
    status = k1.get_status()
    print(f"Current mode: {status.mode.name}")
    print(f"Current model: {status.robot_info.model}")
    k1.stand_up()
```

### Booster T1

```python
from booster_rpc import RobotMode, T1Connection

with T1Connection() as t1:
    status = t1.get_status()
    print(f"Current mode: {status.mode.name}")
    print(f"Body control: {status.body_control.name}")
    print(f"Action: {status.action.name}")
    t1.get_up(RobotMode.WALKING)
```
