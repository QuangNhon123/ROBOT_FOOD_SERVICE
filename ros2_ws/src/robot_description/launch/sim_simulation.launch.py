import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('robot_description')
    
    # File cấu hình RViz2 (Nên chuyển sang thư mục config/rviz_config.rviz)
    rviz_config_file = os.path.join(pkg_share, 'config', 'rviz2_config.rviz')
    #File cau hinh moi truong gazebo 
    world_file = os.path.join(pkg_share, 'worlds', 'gazebo_world.world')
    # 1. Include RSP (Robot State Publisher)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_share, 'launch', 'rsp.launch.py')]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # 2. Include Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={'world': world_file}.items()
    )

    # 3. Spawn Robot vào Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'food_service_robot'],
        output='screen'
    )

    # 4. Include SLAM
    slam = TimerAction(
        period=float(3.0),
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(pkg_share, 'launch', 'slam.launch.py')]),
                launch_arguments={'use_sim_time': 'true'}.items()
            )
        ]
    )
    
    # # 4.1 Include Map Server 
    # map_server = TimerAction(
    #     period=float(8.0),
    #     actions=[
    #         IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(pkg_share, 'launch', 'map_server.launch.py')])
    #         )
    #     ]
    # )
    
    # 5. Node RViz2
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        #arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # static_tf_map_to_odom = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     name='static_tf_map_to_odom',
    #     arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
    #     parameters=[{'use_sim_time': True}]
    # )
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        slam,
        # map_server,
        # static_tf_map_to_odom,
        rviz
    ])