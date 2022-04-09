# Currently only tested on garuda-linux (v1.4)
install:
	python3 build
	chmod +rwx /bin/advaced
	chmod +rwx /lib/advaced
	chmod 777 /lib/advaced/database
	chmod 777 /lib/advaced/database/db.db

build-protobuf:
	python3 -m grpc_tools.protoc -I./rpc/protos --python_out=./rpc --grpc_python_out=./rpc ./rpc/protos/*.proto
