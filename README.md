# Service Action Decider using gRPC

Download checkpoint at [thesis drive](https://drive.google.com/drive/folders/15QNWIEC5JrjJwS-24TG-myMmWW7VkbjT?usp=sharing). After that, move `checkpoint` forler and `intent_slot_labels` folder into `model` folder. 

## Run server by localhost

1. Create conda env `conda create -n service python=3.9`
2. Install neccessary Python packages `pip install -r requirements.txt`
3. Run server `python server.py`
4. Run client `python client.py`
    
## Run server by Docker (Use CPU)
1. Build Docker image `sudo docker build --no-cache -t action_decider_service .` 
2. Run container from image `sudo docker run --name action_decider -p 8000:5002 action_decider_service` (port 5002 of server has been changed to port 8000)
3. Change port at line 12 in `client.py` to 8000
4. Run client `python client.py`
