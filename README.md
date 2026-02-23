# Booster RPC

Python client for controlling Booster K1 humanoid robots via gRPC and WebSocket.

## Installation

```bash
pip install booster-rpc
```

## Usage

```python
from booster_rpc import BoosterConnection, GetRobotStatusResponse, RpcApiId

conn = BoosterConnection()
resp = conn._call(RpcApiId.GET_ROBOT_STATUS)
status = GetRobotStatusResponse().parse(resp.payload)
print(f"Current mode: {status.mode.name}")
print(f"Current model: {status.robot_info.model}")
```
