
PROTO_PATH = protos
PROTOS = $(wildcard $(PROTO_PATH)/*.proto)

.PHONY: protos

protos:
	protoc --proto_path=$(PROTO_PATH) --python_out=pakalolo $(PROTOS)
