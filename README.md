# Booster RPC

Python client for controlling Booster K1 humanoid robots via gRPC.

## Installation

```bash
pip install booster-rpc
```

## Usage

```python
from booster_rpc import BoosterConnection
from booster_rpc.proto import GetRobotStatusResponse, RobotMode, RpcApiId

conn = BoosterConnection()
resp = conn._call(RpcApiId.GET_ROBOT_STATUS)
status = GetRobotStatusResponse().parse(resp.payload)
print(f"Current mode: {RobotMode(status.mode).name}")
```
