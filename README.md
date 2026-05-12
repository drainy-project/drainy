# Drainy Project

## Installation

```bash
# Clone third party dependencies
cd <drainy-workspace>
vcs import --recursive src < src/drainy/thirdparty.repos
# Manually update PX4 git submodules (not done by vcs)
cd <drainy-workspace>/src/ThirdParty/robots/drone/PX4-Autopilot
git submodule update --recursive
# Install PX4 firmware additional dependencies. This will also install Gazebo and other Python dependencies, please check the script before running.
cd <drainy-workspace>
.src/ThirdParty/robots/drone/PX4-Autopilot/Tools/setup/ubuntu.sh --no-nuttx
# Install ROS dependencies and build
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install 
```

## Usage

<!-- ```bash
ros2 launch easynav_playground_drone playground_drone.launch.py
``` -->

or

<!-- ```bash
ros2 launch easynav_playground_drone playground_drone.launch.py world:=<path-to-world>
``` -->
