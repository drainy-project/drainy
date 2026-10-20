# Copyright 2026 Intelligent Robotics Lab

# Launches GenZ-ICP odometry on the RealSense pointcloud.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    topic_arg = DeclareLaunchArgument(
        'topic',
        default_value='/camera/camera/depth/color/points',
        description='Pointcloud topic used by GenZ-ICP',
    )

    genz_icp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('genz_icp'),
                'launch',
                'odometry.launch.py'
            )
        ),
        launch_arguments={
            'topic': LaunchConfiguration('topic'),
        }.items(),
    )

    return LaunchDescription([
        topic_arg,
        genz_icp_launch,
    ])
