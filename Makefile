GRPC_SOURCES = action_decider_service_pb2.py action_decider_service_pb2_grpc.py

all: $(GRPC_SOURCES)

$(GRPC_SOURCES): action_decider_service.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. action_decider_service.proto

clean:
	rm $(GRPC_SOURCES)