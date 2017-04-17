PLATFORM=linux-x86_64
CWD=$(shell pwd)

# Sources
PROTO_PATH=protos
PROTOS=$(wildcard $(PROTO_PATH)/*.proto)

# Protobuf compiler
PROTOC_VERSION=3.2.0
PROTOC_ARCHIVE=protoc-$(PROTOC_VERSION)-$(PLATFORM).zip
PROTOC_INSTALL_PATH=$(CWD)/vendor/protoc3
PROTOC=~/.local/bin/protoc


.PHONY: protos protoc deps clean

## Dependencies
deps: protoc

# Install protoc v3
protoc: /tmp/$(PROTOC_ARCHIVE)
	-rm -rf $(PROTOC_INSTALL_PATH)
	mkdir -p $(PROTOC_INSTALL_PATH)
	unzip /tmp/$(PROTOC_ARCHIVE) -d $(PROTOC_INSTALL_PATH)
	-rm $(PROTOC)
	ln -s $(PROTOC_INSTALL_PATH)/bin/protoc $(PROTOC)
	chmod +x $(PROTOC_INSTALL_PATH)/bin/protoc

/tmp/$(PROTOC_ARCHIVE):
	curl -OL https://github.com/google/protobuf/releases/download/v$(PROTOC_VERSION)/$(PROTOC_ARCHIVE)
	mv $(PROTOC_ARCHIVE) /tmp/$(PROTOC_ARCHIVE)


## Tasks
protos:
	$(PROTOC) --proto_path=$(PROTO_PATH) --python_out=pakalolo $(PROTOS)

clean:
	rm /tmp/$(PROTOC_ARCHIVE)

