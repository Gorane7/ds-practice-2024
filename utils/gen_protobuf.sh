#!/usr/bin/bash
cd pb

for f in *; do
	cd $f
	python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./$f.proto
	cd ..
done
