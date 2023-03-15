import os
import sys
import json

import grpc
import action_decider_service_pb2
import action_decider_service_pb2_grpc

import numpy as np

MONITOR_SERVER_INTERFACE = os.environ.get('HOST', 'localhost')
MONITOR_SERVER_PORT = int(os.environ.get('PORT', 8000))

CHANNEL_IP = f"{MONITOR_SERVER_INTERFACE}:{MONITOR_SERVER_PORT}"

def main():
    channel = grpc.insecure_channel(CHANNEL_IP)
    stub = action_decider_service_pb2_grpc.ACServiceStub(channel)
    state = np.random.rand(126)**2
    converted_state = np.array(state, dtype=np.float32).tobytes()
    result = stub.ActionDecider(action_decider_service_pb2.DialogState(state = converted_state))
    print(json.loads(result.action))
    
if __name__ == "__main__":
    main()
    