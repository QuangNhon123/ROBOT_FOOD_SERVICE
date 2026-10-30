
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # 1. Tim thu muc package da cai dat
    package_dir = get_package_share_directory(
        'dynamic_obstacle_demo'
    )

    # 2. Tim file mo hinh vat can
    model_path = os.path.join(
        package_dir,
        'models',
        'moving_obstacle',
        'model.sdf'
    )

    # 3. Cho phep thay doi vi tri vat can
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')

    # 4. Dua vat can vao Gazebo
    spawn_obstacle = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_moving_obstacle',
        output='screen',
        arguments=[
            '-entity', 'moving_obstacle',
            '-file', model_path,
            '-x', x,
            '-y', y,
            '-z', '0.0'
        ]
    )

    # 5. Khoi chay node dieu khien vat can
    controller = Node(
        package='dynamic_obstacle_demo',
        executable='moving_obstacle',
        name='moving_obstacle_controller',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # 6. Gom cac thanh phan vao launch file
    return LaunchDescription([
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        spawn_obstacle,
        controller
    ])
