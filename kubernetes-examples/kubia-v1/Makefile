PREFIX ?= rwang5688
IMAGE ?= kubia:1.0
FULL_IMAGE_TAG = "$(PREFIX)/$(IMAGE)"

all: build push

build:
	@echo "Building image $(FULL_IMAGE_TAG)"
	docker build -t $(FULL_IMAGE_TAG) ./

push:
	@echo "Pushing image $(FULL_IMAGE_TAG)"
	docker push $(FULL_IMAGE_TAG)

run:
	@echo "Running image $(FULL_IMAGE_TAG)"
	docker run -dp 8080:8080 --name kubia-v1 $(FULL_IMAGE_TAG)
