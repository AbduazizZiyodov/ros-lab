full-setup: get-gazebo-models ros-image-build ros-up

ros-up:
	echo "Starting workspace container"
	xhost +local:docker
	rocker --privileged \
		--devices /dev/input/js0 \
		--network host \
		--nocleanup \
		--persist-image \
		--name ros_noetic \
		--volume `pwd`/src:/root/catkin_ws/src \
		--volume `pwd`/gazebo_models:/root/.gazebo/models \
		--nvidia --x11 ros_noetic_custom

ros-shell:
	docker start ros_noetic && docker exec -it ros_noetic bash -c "tmux new-session -A -s main"

ros-stop:
	echo "Stopping & removing ros noetic container"
	@docker stop ros_noetic && docker rm -f ros_noetic

ros-image-build:
	echo "Building custom ros noetic docker image for workspace"
	@docker build -t ros_noetic_custom .

get-gazebo-models:
	echo "Getting gazebo simulation models"
	@git -C gazebo_models pull || git clone https://github.com/osrf/gazebo_models