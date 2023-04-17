import os
import logging
import grpc
import argparse

import action_decider_service_pb2
import action_decider_service_pb2_grpc

import numpy as np

from pipeline import ActionDeciderModel
from concurrent import futures

action_decider_interface = os.environ.get('ACTION_DECIDER_SERVER_INTERFACE', '0.0.0.0')
action_decider_port = int(os.environ.get('ACTION_DECIDER_SERVER_PORT', 5003))
action_decider_model_path = os.environ.get('ACTION_DECIDER_MODEL_PATH', 'model')

class ACServiceServicer(action_decider_service_pb2_grpc.ACServiceServicer):
    
    def __init__(self, model_path):
        self.decider = ActionDeciderModel(model_path)
        logging.info(f"Loaded model!")
        
    def ActionDecider(self, request, context):
        state = np.frombuffer(request.state, dtype=np.float32)
        next_action = self.decider(state) 
        return action_decider_service_pb2.ActionResponse(action = next_action)

def serve():
    logging.info("Server starting ...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 32))
    action_decider_service_pb2_grpc.add_ACServiceServicer_to_server(
        ACServiceServicer(model_path = action_decider_model_path),
        server
    )
    server.add_insecure_port('{}:{}'.format(action_decider_interface, action_decider_port))
    server.start()
    logging.info(f"Started server on {action_decider_interface}:{action_decider_port}")
    server.wait_for_termination()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    serve()