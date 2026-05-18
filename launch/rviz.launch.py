# Copyright 2026 Intelligent Robotics Lab

# This file is part of the project Easy Navigation (EasyNav in short)
# licensed under the GNU General Public License v3.0.
# See <http://www.gnu.org/licenses/> for details.

# Easy Navigation program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
