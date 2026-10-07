import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Đường dẫn đến gói của bạn
    pkg_share = get_package_share_directory('robot_description')
    
    # 2. Định nghĩa các file cấu hình
    urdf_file = os.path.join(pkg_share, 'urdf', 'robot_demo.urdf')
    rviz_file = os.path.join(pkg_share, 'urdf', 'robot_demo.rviz')
    slam_config = os.path.join(get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')

    # 3. Khởi chạy Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_file],
        parameters=[{'use_sim_time': True}]
    )

    # 4. Khởi chạy Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # 5. Đưa Robot vào Gazebo (Spawn)
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'food_service_robot'],
        output='screen'
    )

    # 6. Khởi chạy SLAM Toolbox (Tự động đồng bộ thời gian)
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_config),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # 7. Khởi chạy RViz2
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_file],
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        spawn_entity,
        slam,
        rviz
    ])
