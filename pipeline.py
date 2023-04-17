# -*- coding: utf-8 -*-

import os
import yaml
import torch
import copy
import json

import numpy as np

from architecture import DQNModel
from typing import List, Dict, Union
from azureml.core import Model, Workspace

class ActionDeciderModel:
    def __init__(self, model_path: str, **kwargs):
        self._get_config(model_path)
        self.get_intent_slot_labels()
        self._init_model()
    
    
    def _init_model(self) -> None:
        self.state_size = self.get_state_size()
        self.model = DQNModel(
            self.config['model']['hidden_size'], 
            self.state_size, 
            self.num_actions
        )
        self.device = 'cuda' if self.config['device']['cuda'] else 'cpu'
        try:
            # model_name = 'action_decider_model'
            # path = Model.get_model_path(
            #     model_name=model_name,
            # )
            # print('path ', path)

            self.model.load_state_dict(torch.load(
                os.path.join(self.config['checkpoint']['checkpoint_dir'], 'model.pt'),
                # path,
                map_location=torch.device(self.device)
            ))
        except Exception:
            raise Exception("Checkpoint file might be missing...")
        
        # if self.device == 'cuda':
        #     self.model.to(self.device)
    
    
    def _get_config(self, model_path: str) -> None:
        try:
            with open(os.path.join(model_path, 'config.yaml'), 'r') as yamlfile:
                self.config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        except Exception:
            raise Exception("Can't load config.yaml file!")
    
    
    def get_intent_slot_labels(self) -> None:
        intent_slot_dir = self.config['agent']['intent_slot_dir']
        try:
            # Load all intents
            intents = [intent.strip() for intent in 
                        open(os.path.join(intent_slot_dir, 'intents.txt'))]
            self.num_intents = len(intents)
            # Load all inform slots
            inform_slots = [inform.strip() for inform in 
                            open(os.path.join(intent_slot_dir, 'inform_slots.txt'))]
            self.num_slots = len(inform_slots)
            # Load all request slots
            request_slots = [request.strip() for request in 
                            open(os.path.join(intent_slot_dir, 'request_slots.txt'))]
        except Exception:
            raise Exception("Intent or slot file has some errors")
        
        self.agent_actions = [
            {'intent': 'done', 'inform_slots': {}, 'request_slots': {}}  # Triggers closing of conversation
        ]
        for slot in inform_slots:
            self.agent_actions.append(
                {'intent': 'inform', 'inform_slots': {slot: 'PLACEHOLDER'}, 'request_slots': {}}
            )
        for slot in request_slots:
            self.agent_actions.append(
                {'intent': 'request', 'inform_slots': {}, 'request_slots': {slot: 'UNK'}}
            )
        
        self.num_actions = len(self.agent_actions)
        
        
    def get_state_size(self) -> int:
        return 2 * self.num_intents + 8 * self.num_slots + 4 + self.config['agent']['max_round_num']
    
    
    def convert_state_to_tensor(self, state: np.array) -> torch.Tensor:
        state = torch.tensor(state, dtype=torch.float32)
        return state.to(device = self.device)
    
    
    def _map_index_to_action(self, index: int) -> Dict[str, Union[str, Dict[str, str]]]:
        for (i, action) in enumerate(self.agent_actions):
            if index == i:
                return copy.deepcopy(action)
        raise ValueError('Index: {} not in range of possible actions'.format(index))
    
    
    def __call__(self, state: List) -> str:
        state = self.convert_state_to_tensor(state).reshape(1, self.state_size)
        action_index = torch.argmax(self.model(state).flatten())
        return json.dumps(self._map_index_to_action(action_index))
         
if __name__ == "__main__":
    decider = ActionDeciderModel()
    input = [0]*decider.state_size
    print(decider(input))
    