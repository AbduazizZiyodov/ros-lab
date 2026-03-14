.PHONY: full-setup-base full-setup-nvidia full-setup-non-nvidia \
	ros-up-nvidia ros-up-non-nvidia \
	ros-shell ros-stop ros-image-build get-gazebo-models

ROCKER_BASE = rocker --privileged \
	--devices /dev/input /dev/dri \
	--network host \
	--nocleanup \
	--persist-image \
	--name ros_noetic \
	--volume $(PWD)/src:/root/catkin_ws/src \
	--volume $(PWD)/gazebo_models:/root/.gazebo/models \
	--x11 ros_noetic_custom

full-setup-base: ros-stop get-gazebo-models ros-image-build
full-setup-nvidia: full-setup-base ros-up-nvidia
full-setup-non-nvidia: full-setup-base ros-up-non-nvidia

ros-up-nvidia: ros-stop
	xhost +local:docker
	$(ROCKER_BASE) --nvidia

ros-up-non-nvidia: ros-stop
	xhost +local:docker
	$(ROCKER_BASE)

ros-shell:
	docker exec -it ros_noetic bash -c "tmux new-session -A -s main"

ros-stop:
	-docker stop ros_noetic
	-docker rm -f ros_noetic

ros-image-build:
	docker build -t ros_noetic_custom .

get-gazebo-models:
	git -C gazebo_models pull || git clone https://github.com/osrf/gazebo_models gazebo_models