from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    bot_bringup_share = get_package_share_directory('bot_bringup')

    rviz_config = os.path.join(
        bot_bringup_share,
        'config',
        'mapping.rviz'
    )

    return LaunchDescription([

        # ========================================================
        # ROBOT DESCRIPTION / URDF
        # ========================================================

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    bot_bringup_share,
                    'launch',
                    'description.launch.py'
                )
            )
        ),

        # ========================================================
        # JOINT STATE PUBLISHER
        # Added only for wheel joint TFs in RViz
        # ========================================================

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen'
        ),

        # ========================================================
        # SLAM TOOLBOX
        # ========================================================

        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[{
                'use_sim_time': False,

                'odom_frame': 'odom',
                'map_frame': 'map',
                'base_frame': 'base_link',

                'scan_topic': '/scan',

                'mode': 'mapping',

                'resolution': 0.05,

                'map_update_interval': 2.0,

                'minimum_time_interval': 0.5,

                'throttle_scans': 1,

                'max_laser_range': 12.0,

                'minimum_travel_distance': 0.05,
                'minimum_travel_heading': 0.05,

                'use_scan_matching': True,
                'use_scan_barycenter': True,

                'debug_logging': False,
            }]
        ),

        # ========================================================
        # RVIZ
        # ========================================================

       # Node(
       #     package='rviz2',
       #     executable='rviz2',
        #   arguments=[
         #       '-d',
          #      rviz_config
         #   ],
          #  output='screen'
       # ),
   ])
