#!/bin/bash

source /opt/ros/noetic/setup.bash

if [ -f /root/ros_ws/devel/setup.bash ]; then
  source /root/ros_ws/devel/setup.bash
fi

exec "$@"
