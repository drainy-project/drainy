# Copyright 2026 Intelligent Robotics Lab

import os
from ament_index_python.packages import get_package_prefix, get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, DeclareLaunchArgument, OpaqueFunction, RegisterEventHandler, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution, LaunchConfiguration, FindExecutable
from launch.event_handlers import OnProcessStart
import launch_ros.descriptions


def get_world(context, *args, **kwargs):
    world_arg = LaunchConfiguration('world').perform(context)
    x_arg = LaunchConfiguration('x').perform(context)
    y_arg = LaunchConfiguration('y').perform(context)
    z_arg = LaunchConfiguration('z').perform(context)

def generate_launch_description():
    prefix = LaunchConfiguration("prefix", default="")
    pkg_path = get_package_share_directory('drainy')
    install_dir = get_package_prefix('drainy')
    ws_dir = install_dir.split("install")[0]
    sim_path = ws_dir+"src/ThirdParty/worlds/PX4-gazebo-models"
    sitl_path = ws_dir+"src/ThirdParty/robots/drone/PX4-Autopilot"

    world_arg = DeclareLaunchArgument(
        	'world',
			default_value='niosh_11',
			description='World to be launched',
    )

    x_arg = DeclareLaunchArgument(
        	'x',
			default_value='0',
			description='X init position',
    )

    y_arg = DeclareLaunchArgument(
        	'y',
			default_value='0',
			description='Y init position',
    )

    z_arg = DeclareLaunchArgument(
        	'z',
			default_value='0',
			description='Z init position',
    )

    # NOTE: Removed empty child_frame_id which was causing TF errors
    # tf = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     arguments = ['--x', '0', '--y', '0', '--z', '0', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'world', '--child-frame-id', 'base_link']
    # )

    sdf_file = os.path.join(sim_path, 'models', 'drainy', 'model.sdf')

    with open(sdf_file, 'r') as infp:
        robot_desc = infp.read()

    # robot_state_publisher_node = Node(
    #     package='robot_state_publisher',
    #     executable='robot_state_publisher',
    #     name='robot_state_publisher',
    #     #namespace=robot_id,
    #     output='screen',
    #     parameters=[{
    #       'use_sim_time': True,
    #       'robot_description': robot_desc,
    #       'publish_frequency': 100.0,
    #       'frame_prefix': '',
    #     }],
    # )

    gazebo_sim = ExecuteProcess(
        cmd=[
            'python3',
            'simulation-gazebo',
            '--world',
            LaunchConfiguration('world')
        ],
        cwd=sim_path,
        output='screen'
    ) # SIM

    px4_sitl = ExecuteProcess(
        cmd=[
            'make',
            'px4_sitl',
            'gz_drainy'
        ],
        cwd=sitl_path,
        additional_env={
            'PX4_GZ_STANDALONE': '1',
            'PX4_GZ_WORLD': [LaunchConfiguration('world'), '_world'],
            'PX4_GZ_MODEL_POSE': ([LaunchConfiguration('x'),',', LaunchConfiguration('y'),',', LaunchConfiguration('z'),',0,0,0']),
        },
        output='screen'
    ) # SIM

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_ros_gz',
        parameters=[
            {
                'config_file': os.path.join(
                    pkg_path, 'config', 'drone_bridge.yaml'
                ),
                'use_sim_time': True,
            }
        ],
        output='screen',
    )# SIM

    # Image bridge
    gz_image_bridge_node = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=[
            "/depth_camera/image",
        ],
        output="screen",
        parameters=[
            {'use_sim_time': True,
             'camera.image.compressed.jpeg_quality': 75},
        ],
    ) # SIM

    roboligo_params_file = os.path.join(pkg_path, 'config', 'roboligo.params.yaml')
    
    roboligo = Node(
            package="roboligo_system",
            executable="roboligo_main",
            output="screen",
            parameters=[
                roboligo_params_file,
            ],
        )
    
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['--x', '0', '--y', '0', '--z', '0', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'base_link', '--child-frame-id', 'drainy_0'],
        output='screen',
    )

    on_gazebo_init = RegisterEventHandler(
        OnProcessStart(
            target_action=gazebo_sim,
            on_start=[
                px4_sitl
            ],
        )
    )

    on_px4_init = RegisterEventHandler(
        OnProcessStart(
            target_action=px4_sitl,
            on_start=[
                bridge,
                gz_image_bridge_node,
            ],
        )
    )

    on_bridge_init = RegisterEventHandler(
        OnProcessStart(
            target_action=bridge,
            on_start=[
                roboligo
            ],
        )
    )


    return LaunchDescription([
        # tf,
        world_arg,
        x_arg,
        y_arg,
        z_arg,
        OpaqueFunction(function=get_world),
        gazebo_sim,
        # static_tf,
        on_gazebo_init,
        on_px4_init,
        on_bridge_init
        # robot_state_publisher_node,
    ])

