FROM ubuntu:24.04 as base

# Labels
LABEL maintainer="Juan S. Cely"
LABEL contact="juanscelyg@gmail.com"
LABEL description="Drainy Docker"

ARG ROS_VERSION="jazzy"
ARG ROS_DOMAIN_ID="32"

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

RUN apt update && apt install curl dpkg -y

RUN export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}') \
    && curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb" \
    && dpkg -i /tmp/ros2-apt-source.deb

RUN apt update && apt upgrade -y \
    && apt install -y ros-jazzy-ros-base \
    && apt install -y ros-dev-tools \
    && source /opt/ros/jazzy/setup.bash \
    && source "/root/.bashrc" \
    && rosdep init && rosdep update \
    && apt update && apt upgrade -y

RUN apt update \
    && apt install -y wget curl gnupg lsb-release git build-essential nano \
    && apt install -y ros-jazzy-ament-cmake* \
                        ros-jazzy-rclcpp \
                        ros-jazzy-realsense2* \
                        ros-jazzy-ouster* \
                        ros-jazzy-mavros* \
                        ros-jazzy-micro-ros-msgs \
                        ros-jazzy-vision-msgs \
                        ros-jazzy-rviz* \
                        ros-jazzy-octomap* \
                        ros-jazzy-robot-localization

RUN mkdir -p /root/drainy_ws/src/ThirdParty/robots/drone \
    && mkdir -p /root/drainy_ws/src/ThirdParty/worlds 


RUN cd /root/drainy_ws/src && git clone -b jazzy https://github.com/EasyNavigation/EasyNavigation.git \
    && cd /root/drainy_ws/src && git clone -b jazzy https://github.com/EasyNavigation/NavMap.git \
    && cd /root/drainy_ws/src && git clone -b jazzy https://github.com/EasyNavigation/easynav_plugins.git \
    && cd /root/drainy_ws/src && git clone -b jazzy https://github.com/fmrico/yaets.git \
    #&& cd /root/drainy_ws/src && git clone -b jazzy https://github.com/micro-ROS/micro-ROS-Agent.git \
    && cd /root/drainy_ws/src && git clone -b release/1.16 https://github.com/PX4/px4_msgs.git \ 
    && cd /root/drainy_ws/src && git clone https://github.com/drainy-project/genz-icp.git \
    && cd /root/drainy_ws/src/ThirdParty/robots && git clone -b jazzy https://github.com/juanscelyg/roboligo.git

RUN cd /root/drainy_ws && rosdep install --from-paths src --ignore-src -y -r 

RUN source /opt/ros/jazzy/setup.bash && cd /root/drainy_ws && colcon build --symlink-install

RUN rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
RUN echo "source /root/drainy_ws/install/setup.bash " >> ~/.bashrc
RUN echo "export ROS_DOMAIN_ID=${ROS_DOMAIN_ID}" >> ~/.bashrc

RUN cd /root/drainy_ws

ENV DEBIAN_FRONTEND=dialog

FROM dev as sim

ENV DEBIAN_FRONTEND=noninteractive

RUN source "/root/.bashrc"

RUN apt update \
    && apt install -y ros-jazzy-gz* \
                        ros-jazzy-ros-gz*

RUN cd /root/drainy_ws/src/ThirdParty/robots/drone && git clone -b easynav --recursive https://github.com/drainy-project/PX4-Autopilot.git \
    && cd /root/drainy_ws/src/ThirdParty/worlds && git clone -b easynav --recursive https://github.com/drainy-project/PX4-gazebo-models.git 

RUN cd /root/drainy_ws && sh -c src/ThirdParty/robots/drone/PX4-Autopilot/Tools/setup/ubuntu.sh --no-nuttx

RUN cd /root/drainy_ws && rosdep install --from-paths src --ignore-src -y -r 

RUN source /opt/ros/jazzy/setup.bash && cd /root/drainy_ws && colcon build --symlink-install

RUN rm -rf /var/lib/apt/lists/*

RUN source /root/drainy_ws/install/setup.bash

RUN cd /root/drainy_ws

ENV DEBIAN_FRONTEND=dialog