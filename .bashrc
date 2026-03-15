export QT_QPA_PLATFORM=xcb
export TURTLEBOT3_MODEL=burger
export PATH=$PATH:$HOME/.local/bin
export ROS_IP=$(hostname -I | cut -f1 -d' ')
export ROS_HOSTNAME=$ROS_IP
export ROS_MASTER_URI="http://$ROS_IP:11311"
export GAZEBO_MODEL_PATH=/root/.gazebo/models
export DISABLE_ROS1_EOL_WARNINGS=1
source /opt/ros/noetic/setup.bash
source /root/catkin_ws/devel/setup.bash
if command -v nvidia-smi &>/dev/null && nvidia-smi &>/dev/null; then
    export __GLX_VENDOR_LIBRARY_NAME=nvidia
    export __NV_PRIME_RENDER_OFFLOAD=1
    export __VK_LAYER_NV_optimus=NVIDIA_only
fi
ros_teleop_joy() {
    roslaunch teleop_twist_joy teleop.launch \
        joy_dev:=/dev/input/js0 \
        config_filepath:=/root/catkin_ws/src/teleop_config/config/joy.yaml
}
