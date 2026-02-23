# Booster RPC

Python client for controlling Booster K1 humanoid robots via gRPC.

## Installation

```bash
pip install booster-rpc
```

## Usage

```python
from booster_rpc import BoosterRPCConnection
from booster_rpc.proto import RpcApiId, GetRobotStatusResponse

conn = BoosterRPCConnection()
resp = conn._call(RpcApiId.GET_ROBOT_STATUS)
status = GetRobotStatusResponse().parse(resp.payload)
print(f"Current mode: {status.mode.name}")
```
