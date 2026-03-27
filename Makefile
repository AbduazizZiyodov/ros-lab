.PHONY: setup shell start stop rebuild destroy destroy-all \
	logs status get-gazebo-models fix-perms \
	_compose _compose-up _detect-gpu _check-deps

NVIDIA_AVAILABLE := $(shell nvidia-smi > /dev/null 2>&1 && echo "yes" || echo "no")
ifeq ($(NVIDIA_AVAILABLE), yes)
  COMPOSE_FILES := -f docker/docker-compose.yml -f docker/docker-compose.nvidia.yml
  GPU_MSG := "NVIDIA GPU detected"
else
  COMPOSE_FILES := -f docker/docker-compose.yml
  GPU_MSG := "No NVIDIA GPU detected"
endif

_compose:
	@echo "=> GPU: $(GPU_MSG)"
	@docker compose $(COMPOSE_FILES) $(COMPOSE_CMD)

setup: _check-deps get-gazebo-models
	@echo "Building Docker image..."
	docker build -f docker/Dockerfile -t ros_noetic_custom .
	@echo "GPU = $(GPU_MSG)"
	@echo "Starting container"
	xhost +local:docker 2>/dev/null || true
	docker compose $(COMPOSE_FILES) up -d
	$(MAKE) fix-perms
	@echo "Run 'make shell'"

shell:
	xhost +local:docker 2>/dev/null || true
	docker exec -it ros_noetic bash -c "tmux new-session -A -s main"

start:
	xhost +local:docker 2>/dev/null || true
	docker compose $(COMPOSE_FILES) start

stop:
	docker compose $(COMPOSE_FILES) stop

rebuild: stop
	docker build -f docker/Dockerfile -t ros_noetic_custom .
	docker compose $(COMPOSE_FILES) up -d --force-recreate
	$(MAKE) fix-perms

destroy: stop
	docker compose $(COMPOSE_FILES) rm -f

destroy-all: stop
	docker compose $(COMPOSE_FILES) rm -f
	docker compose $(COMPOSE_FILES) down -v

logs:
	docker compose $(COMPOSE_FILES) logs -f

fix-perms:
	@echo "Fixing src/ ownership to $(shell id -u):$(shell id -g)..."
	sudo chown -R $(shell id -u):$(shell id -g) ./src
	@echo "Done"

get-gazebo-models:
	git -C gazebo_models pull 2>/dev/null || \
	    git clone https://github.com/osrf/gazebo_models gazebo_models
	@echo "Gazebo models are up to date"

_check-deps:
	command -v docker > /dev/null 2>&1 || \
	    (echo "Docker is not found. Install Docker Engine." && exit 1)
	docker compose version > /dev/null 2>&1 || \
	    (echo "docker compose is not found. Install pls." && exit 1)
	@echo "OK"