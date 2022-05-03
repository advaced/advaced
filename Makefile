# Currently only tested on garuda-linux (v1.4)
# python3 build
install:
	python3 ./build
	cython -3 --embed -o ./out/advaced.c ./__main__.py
	gcc -Os -I /usr/include/python3.10 -o /bin/advaced ./out/advaced.c -lpython3.10 -lpthread -lm -lutil -ldl
	rm ./out/advaced.c

	chmod +rwx /bin/advaced
	chmod +rwx /lib/advaced
	chmod 777 /lib/advaced/database
	chmod 777 /lib/advaced/database/db.db

compile:
	cython -3 --embed -o ./out/advaced.c ./__main__.py
	gcc -Os -I /usr/include/python3.10 -o ./out/advaced ./out/advaced.c -lpython3.10 -lpthread -lm -lutil -ldl
	rm ./out/advaced.c

build-protobuf:
	python3 -m grpc_tools.protoc -I./rpc/protos --python_out=./rpc --grpc_python_out=./rpc ./rpc/protos/*.proto
