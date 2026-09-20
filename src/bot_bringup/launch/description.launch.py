from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_share = get_package_share_directory('bot_bringup')

    urdf_file = os.path.join(
        pkg_share,
        'urdf',
        'rover.urdf.xacro'
    )

    robot_description = Command([
        'xacro ',
        urdf_file
    ])

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': False
            }
        ]
    )

    return LaunchDescription([
        robot_state_publisher
    ])
