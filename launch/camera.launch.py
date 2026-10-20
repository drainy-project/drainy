# Copyright 2026 Intelligent Robotics Lab

# Launches the RealSense camera with the pointcloud enabled.
# Humble uses 'pointcloud__neon__.enable', Jazzy and newer use 'pointcloud.enable'.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    ros_distro = os.environ.get('ROS_DISTRO', '').lower()

    if ros_distro == 'humble':
        pointcloud_param = 'pointcloud__neon__.enable'
    else:
        pointcloud_param = 'pointcloud.enable'

    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('realsense2_camera'),
                'launch',
                'rs_launch.py'
            )
        ),
        launch_arguments={
            pointcloud_param: 'true',
        }.items(),
    )

    return LaunchDescription([
        LogInfo(msg=f'ROS_DISTRO={ros_distro}: setting {pointcloud_param}:=true'),
        realsense_launch,
    ])
