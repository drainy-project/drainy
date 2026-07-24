FROM osrf/ros:humble-desktop-full as base

# Labels
LABEL maintainer="Juan S. Cely"
LABEL contact="juanscelyg@gmail.com"
LABEL description="Drainy Docker"

ARG ROS_VERSION="humble"
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

RUN apt update \
    && apt install --no-install-recommends -y curl gnupg lsb-release git build-essential nano 

RUN mkdir -p /root/drainy_ws/src \
    && source /opt/ros/humble/setup.bash \
    && source "/root/.bashrc" \
    && apt-get update \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/EasyNavigation/EasyNavigation.git \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/EasyNavigation/NavMap.git \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/EasyNavigation/easynav_plugins.git \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/fmrico/yaets.git \
    && cd /root/drainy_ws && rosdep install --from-paths src --ignore-src -y -r \
    && cd /root/drainy_ws && colcon build --symlink-install\
    && source /root/drainy_ws/install/setup.bash \
    && rm -rf /var/lib/apt/lists/*


RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
# RUN echo "source /root/env/bin/activate" >> ~/.bashrc

ENV DEBIAN_FRONTEND=dialog

FROM base as sim 

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install --no-install-recommends -y curl gnupg lsb-release git build-essential nano 

RUN mkdir -p /root/drainy_ws/src/ThirdParty/robots/drone \
    && mkdir -p /root/drainy_ws/src/ThirdParty/worlds \
    && source /opt/ros/humble/setup.bash \
    && source "/root/.bashrc" \
    && apt-get update \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/EasyNavigation/EasyNavigation.git \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/EasyNavigation/NavMap.git \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/EasyNavigation/easynav_plugins.git \
    && cd /root/drainy_ws/src && git clone -b humble https://github.com/fmrico/yaets.git \
    && cd /root/drainy_ws/src/ThirdParty/robots && git clone -b jazzy https://github.com/juanscelyg/roboligo.git \
    && cd /root/drainy_ws/src/ThirdParty/robots/drone && git clone -b easynav --recursive https://github.com/drainy-project/PX4-Autopilot.git \
    && cd /root/drainy_ws/src/ThirdParty/worlds && git clone -b easynav --recursive https://github.com/drainy-project/PX4-gazebo-models.git \
    && cd /root/drainy_ws && sh -c src/ThirdParty/robots/drone/PX4-Autopilot/Tools/setup/ubuntu.sh --no-nuttx\
    && cd /root/drainy_ws && rosdep install --from-paths src --ignore-src -y -r \
    && cd /root/drainy_ws && colcon build --symlink-install\
    && source /root/drainy_ws/install/setup.bash \
    && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
# RUN echo "source /root/env/bin/activate" >> ~/.bashrc

ENV DEBIAN_FRONTEND=dialog