# Copyright 2026 Intelligent Robotics Lab

# Launches only roboligo. MAVROS must already be running.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_path = get_package_share_directory('drainy')

    roboligo_params_file = os.path.join(pkg_path, 'config', 'roboligo.params.yaml')

    roboligo = Node(
        package="roboligo_system",
        executable="roboligo_main",
        output="screen",
        parameters=[
            roboligo_params_file,
        ],
    )

    return LaunchDescription([
        roboligo,
    ])
