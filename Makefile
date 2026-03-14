.PHONY: full-setup ros-start ros-start-cpu ros-shell ros-stop ros-image-build get-gazebo-models

full-setup-base: ros-stop get-gazebo-models ros-image-build
full-setup-nvidia: full-setup-base ros-up-nvidia
full-setup-non-nvidia: full-setup-base ros-up-non-nvidia

ros-up-nvidia:
	@echo "Starting ROS container (NVIDIA)"
	-docker stop ros_noetic
	-docker rm -f ros_noetic
	xhost +local:docker
	rocker --privileged \
		--devices /dev/input \
		--network host \
		--nocleanup \
		--persist-image \
		--name ros_noetic \
		--volume `pwd`/src:/root/catkin_ws/src \
		--volume `pwd`/gazebo_models:/root/.gazebo/models \
		--nvidia --x11 ros_noetic_custom

ros-up-non-nvidia:
	@echo "Starting ROS container (Non-NVIDIA)"
	-docker stop ros_noetic
	-docker rm -f ros_noetic
	xhost +local:docker
	rocker --privileged \
		--devices /dev/input \
		--devices /dev/dri \
		--network host \
		--nocleanup \
		--persist-image \
		--name ros_noetic \
		--volume `pwd`/src:/root/catkin_ws/src \
		--volume `pwd`/gazebo_models:/root/.gazebo/models \
		--x11 ros_noetic_custom

ros-shell:
	docker start ros_noetic && docker exec -it ros_noetic bash -c "tmux new-session -A -s main"

ros-stop:
	@echo "Stopping & removing ros noetic container"
	- docker stop ros_noetic
	- docker rm -f ros_noetic
	docker ps -a

ros-image-build:
	docker build -t ros_noetic_custom .

get-gazebo-models:
	@echo "Getting gazebo simulation models"
	git -C gazebo_models pull || git clone https://github.com/osrf/gazebo_models
