FROM osrf/ros:humble-desktop-full as base

# Labels
LABEL maintainer="Juan S. Cely"
LABEL contact="juanscelyg@gmail.com"
LABEL description="Drainy Docker"

ARG ROS_VERSION="humble"
ARG ROS_DOMAIN_ID="73"

# ==
# Disable dialog frontend
# ==
ARG DEBIAN_FRONTEND=noninteractive

# ==
# Select shell
# ==
SHELL ["/bin/bash", "-c"]

FROM base as dev

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y wget curl gnupg lsb-release git build-essential nano \
    && apt install -y ros-humble-ament-cmake* \
                        ros-humble-rclcpp \
                        ros-humble-ouster*

RUN mkdir -p /root/drainy_ws/src/ThirdParty/robots/drone \
    && mkdir -p /root/drainy_ws/src/ThirdParty/worlds \
    && source /opt/ros/humble/setup.bash \
    && source "/root/.bashrc" \
    && apt update && apt upgrade -y

RUN cd /root/drainy_ws/src && git clone -b humble https://github.com/EasyNavigation/EasyNavigation.git \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/EasyNavigation/NavMap.git \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/EasyNavigation/easynav_plugins.git \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/fmrico/yaets.git \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/micro-ROS/micro-ROS-Agent.git \
    && cd /root/drainy_ws/src && git clone -b release/1.16 https://github.com/PX4/px4_msgs.git \ 
    && cd /root/drainy_ws/src && git clone https://github.com/drainy-project/genz-icp.git \
    && cd /root/drainy_ws/src/ThirdParty/robots && git clone -b humble https://github.com/juanscelyg/roboligo.git

RUN cd /root/drainy_ws && rosdep install --from-paths src --ignore-src -y -r 

RUN source /opt/ros/humble/setup.bash && cd /root/drainy_ws && colcon build --symlink-install

RUN rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source /root/drainy_ws/install/setup.bash " >> ~/.bashrc
RUN echo "export ROS_DOMAIN_ID=${ROS_DOMAIN_ID}" >> ~/.bashrc

RUN cd /root/drainy_ws

ENV DEBIAN_FRONTEND=dialog

FROM dev as sim

ENV DEBIAN_FRONTEND=noninteractive

RUN source "/root/.bashrc"

RUN cd /root/drainy_ws/src/ThirdParty/robots/drone && git clone -b easynav --recursive https://github.com/drainy-project/PX4-Autopilot.git \
    && cd /root/drainy_ws/src/ThirdParty/worlds && git clone -b easynav --recursive https://github.com/drainy-project/PX4-gazebo-models.git 

RUN cd /root/drainy_ws && sh -c src/ThirdParty/robots/drone/PX4-Autopilot/Tools/setup/ubuntu.sh --no-nuttx

RUN cd /root/drainy_ws && rosdep install --from-paths src --ignore-src -y -r 

RUN source /opt/ros/humble/setup.bash && cd /root/drainy_ws && colcon build --symlink-install

RUN rm -rf /var/lib/apt/lists/*

RUN source /root/drainy_ws/install/setup.bash

RUN cd /root/drainy_ws

ENV DEBIAN_FRONTEND=dialog