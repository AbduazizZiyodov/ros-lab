export QT_QPA_PLATFORM=xcb
export TURTLEBOT3_MODEL=burger
export PATH=$PATH:$HOME/.local/bin
export GAZEBO_MODEL_PATH=/root/.gazebo/models
export HOST_USER="${HOST_USER:-$(whoami)}"
export HOST_HOSTNAME="${HOST_HOSTNAME:-$(hostname)}"
export DISABLE_ROS1_EOL_WARNINGS=1
export ROS_IP=$(hostname -I | cut -f1 -d' ')
export ROS_HOSTNAME=$ROS_IP
export ROS_MASTER_URI=http://$ROS_IP:11311
source /opt/ros/noetic/setup.bash
if [ -f /root/catkin_ws/devel/setup.bash ]; then
    source /root/catkin_ws/devel/setup.bash
fi
if command -v nvidia-smi &>/dev/null && nvidia-smi &>/dev/null; then
    export __GLX_VENDOR_LIBRARY_NAME=nvidia
    export __NV_PRIME_RENDER_OFFLOAD=1
    export __VK_LAYER_NV_optimus=NVIDIA_only
fi
export HISTFILE=/root/.bash_history
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoredups:erasedups
shopt -s histappend
ros_teleop_joy() {
    roslaunch teleop_twist_joy teleop.launch \
        joy_dev:=/dev/input/js0 \
        config_filepath:=/root/catkin_ws/src/teleop_config/config/joy.yaml
}
ros_reload() {
    export ROS_IP=$(hostname -I | cut -f1 -d' ')
    export ROS_HOSTNAME=$ROS_IP
    export ROS_MASTER_URI=http://$ROS_IP:11311
}
PS1='[${HOST_USER}@${HOST_HOSTNAME}:\w] \[\e[32m\]\$\[\e[0m\] '