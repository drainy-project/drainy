# Copyright 2026 Intelligent Robotics Lab

# Launches the EasyNav system with the drainy params.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_path = get_package_share_directory('drainy')

    params_file_arg = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(pkg_path, 'config', 'easynav.params.yaml'),
        description='EasyNav params file',
    )

    easynav = Node(
        package='easynav_system',
        executable='system_main',
        output='screen',
        parameters=[
            LaunchConfiguration('params_file'),
        ],
    )

    return LaunchDescription([
        params_file_arg,
        easynav,
    ])
