# Drainy Project

## Installation

```bash
# Clone third party dependencies
cd <drainy-workspace>
vcs import --recursive src < src/drainy/thirdparty.repos
```

If you are doing simulation, you will need to install PX4 firmware dependencies and build the workspace. Please follow the steps below:

```bash
vcs import --recursive src < src/drainy/thirdparty_sim.repos
cd <drainy-workspace>/src/ThirdParty/robots/drone/PX4-Autopilot
git submodule update --recursive
# Install PX4 firmware additional dependencies. This will also install Gazebo and other Python dependencies, please check the script before running.
cd <drainy-workspace>
./src/ThirdParty/robots/drone/PX4-Autopilot/Tools/setup/ubuntu.sh --no-nuttx
```

To compile the pkg, you will need to install ROS dependencies and build the workspace. Please follow the steps below:

```bash
# Install ROS dependencies and build
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-up-to drainy
source install/setup.bash
```
