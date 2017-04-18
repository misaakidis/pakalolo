PLATFORM=linux-x86_64
CWD=$(shell pwd)

# Sources
PROTO_PATH=protos
PROTOS=$(wildcard $(PROTO_PATH)/*.proto)

# Vendor
VENDOR_PATH=$(CWD)/vendor
VENDOR_BIN=$(VENDOR_PATH)/bin
VENDOR_LIB=$(VENDOR_PATH)/lib

# Protobuf compiler
PROTOC_VERSION=3.2.0
PROTOC_ARCHIVE=protoc-$(PROTOC_VERSION)-$(PLATFORM).zip


.PHONY: protos protoc vendor deps clean

## Dependencies
deps: vendor protoc python

vendor:
	mkdir -p $(VENDOR_BIN)
	mkdir -p $(VENDOR_LIB)

python:
	virtualenv $(CWD)/venv --python=python3
	. $(CWD)/venv/bin/activate
	$(CWD)/venv/bin/pip install -r requirements.txt

# Install protoc v3
protoc: /tmp/$(PROTOC_ARCHIVE)
	unzip /tmp/$(PROTOC_ARCHIVE) -d $(VENDOR_LIB)/protoc3
	ln -s $(VENDOR_LIB)/protoc3/bin/protoc $(VENDOR_BIN)/protoc
	chmod a+r+x $(VENDOR_LIB)/protoc3 -R

/tmp/$(PROTOC_ARCHIVE):
	curl -OL https://github.com/google/protobuf/releases/download/v$(PROTOC_VERSION)/$(PROTOC_ARCHIVE)
	mv $(PROTOC_ARCHIVE) /tmp/$(PROTOC_ARCHIVE)


## Tasks
protos:
	$(VENDOR_BIN)/protoc --proto_path=$(PROTO_PATH) --python_out=pakalolo $(PROTOS)

clean:
	-rm /tmp/$(PROTOC_ARCHIVE)
	-rm -rf $(VENDOR_PATH)
	-rm -rf venv
