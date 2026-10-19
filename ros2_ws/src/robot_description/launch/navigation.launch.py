import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg_share = get_package_share_directory('robot_description')
    nav2_share = get_package_share_directory('nav2_bringup')

    map_file = os.path.join(pkg_share, 'map', 'map.yaml')
    params_file = os.path.join(pkg_share, 'config', 'nav2_params.yaml')

    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_share, 'launch', 'localization_launch.py')
        ),
        launch_arguments={
            'map': map_file,
            'use_sim_time': 'True',
            'params_file': params_file,
            'autostart': 'True',
        }.items()
    )

    navigation = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(nav2_share, 'launch', 'navigation_launch.py')
                ),
                launch_arguments={
                    'use_sim_time': 'True',
                    'params_file': params_file,
                    'autostart': 'True',
                }.items()
            )
        ]
    )

    return LaunchDescription([
        localization,
        navigation,
    ])
