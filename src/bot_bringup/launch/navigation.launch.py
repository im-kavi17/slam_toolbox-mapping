from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_share = get_package_share_directory('bot_bringup')

    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    map_file = LaunchConfiguration('map')
    lidar_port = LaunchConfiguration('lidar_port')
    micro_ros_port = LaunchConfiguration('micro_ros_port')

    rviz_config = os.path.join(
        pkg_share,
        'config',
        'navigation.rviz'
    )

    nav2_params = os.path.join(
        pkg_share,
        'config',
        'nav2_params.yaml'
    )

    amcl_params = os.path.join(
        pkg_share,
        'config',
        'amcl_params.yaml'
    )

    return LaunchDescription([

        # ==================================
        # Arguments
        # ==================================

        DeclareLaunchArgument(
            'map',
            description='Full path to map YAML file'
        ),

        DeclareLaunchArgument(
            'lidar_port',
            default_value='/dev/ttyUSB1'
        ),

        DeclareLaunchArgument(
            'micro_ros_port',
            default_value='/dev/ttyUSB0'
        ),

        # ==================================
        # RPLIDAR A1
        # ==================================

        Node(
            package='rplidar_ros',
            executable='rplidar_node',
            name='rplidar',
            output='screen',
            parameters=[{
                'serial_port': lidar_port,
                'serial_baudrate': 115200,
                'frame_id': 'laser',
                'inverted': False,
                'angle_compensate': True,
            }]
        ),

        # ==================================
        # base_link -> laser
        # ==================================

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='laser_tf',
            arguments=[
                '0.0', '0.0', '0.20',
                '0.0', '0.0', '0.0',
                'base_link',
                'laser'
            ],
            output='screen'
        ),

        # ==================================
        # MAP SERVER + AMCL
        # ==================================

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    nav2_bringup_dir,
                    'launch',
                    'localization_launch.py'
                )
            ),
            launch_arguments={
                'map': map_file,
                'params_file': amcl_params,
                'autostart': 'True'
            }.items()
        ),

        # ==================================
        # NAV2
        # ==================================

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    nav2_bringup_dir,
                    'launch',
                    'navigation_launch.py'
                )
            ),
            launch_arguments={
                'params_file': nav2_params,
                'autostart': 'True'
            }.items()
        ),

        # ==================================
        # micro-ROS Agent
        # ==================================

        Node(
            package='micro_ros_agent',
            executable='micro_ros_agent',
            name='micro_ros_agent',
            output='screen',
            arguments=[
                'serial',
                '--dev',
                micro_ros_port,
                '-b',
                '115200'
            ]
        ),

        # ==================================
        # RVIZ
        # ==================================

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            output='screen'
        ),
    ])
