# Copyright 2026 Intelligent Robotics Lab

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():
    # Rviz config and launching
    rviz_config_file = PathJoinSubstitution(
        [get_package_share_directory("drainy"), "config", "drainy.rviz"]
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[{"use_sim_time": True}],
    )


    return LaunchDescription([
        rviz_node
    ])
