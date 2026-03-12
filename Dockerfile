FROM osrf/ros:noetic-desktop-full

ENV DEBIAN_FRONTEND=noninteractive \
    QT_QPA_PLATFORM=xcb \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=all \
    TURTLEBOT3_MODEL=burger \
    ROS_WS=/root/catkin_ws

RUN apt-get update && apt-get install -y \
    vim nano curl wget git htop tmux \
    net-tools iputils-ping usbutils \
    x11-apps mesa-utils \
    xboxdrv joystick \
    ros-noetic-rqt \
    ros-noetic-rqt-common-plugins \
    ros-noetic-rqt* \
    ros-noetic-rviz \
    ros-noetic-joy \
    ros-noetic-teleop-twist-joy \
    ros-noetic-teleop-twist-keyboard \
    ros-noetic-gazebo-ros \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-gazebo-ros-control \
    ros-noetic-laser-proc \
    ros-noetic-rgbd-launch \
    ros-noetic-rosserial-arduino \
    ros-noetic-rosserial-python \
    ros-noetic-rosserial-client \
    ros-noetic-rosserial-msgs \
    ros-noetic-amcl \
    ros-noetic-map-server \
    ros-noetic-move-base \
    ros-noetic-urdf \
    ros-noetic-xacro \
    ros-noetic-compressed-image-transport \
    ros-noetic-gmapping \
    ros-noetic-navigation \
    ros-noetic-interactive-markers \
    ros-noetic-dynamixel-sdk \
    ros-noetic-turtlebot3-msgs \
    ros-noetic-turtlebot3 \
    ros-noetic-turtlebot3-simulations \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $ROS_WS
COPY src/ src/

RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make"

COPY .bashrc_append /tmp/.bashrc_append
RUN cat /tmp/.bashrc_append >> /root/.bashrc && rm /tmp/.bashrc_append

COPY .tmux.conf /root/.tmux.conf
RUN git clone https://github.com/tmux-plugins/tpm /root/.tmux/plugins/tpm

RUN mkdir -p /root/.gazebo/models
COPY gazebo_models/ /root/.gazebo/models

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && $HOME/.local/bin/uv tool install ruff

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
