import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('robot_description')

    # 1. Bật Robot State Publisher (use_sim_time:=false)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_share, 'launch', 'rsp.launch.py')]),
        launch_arguments={'use_sim_time': 'false'}.items()
    )

    # 2. Driver LiDAR thật (Ví dụ cho RPLiDAR A1/A2/A3)
    lidar_driver = Node(
        package='rplidar_ros',
        executable='rplidar_node',
        name='rplidar_node',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': 115200,
            'frame_id': 'laser_frame',  # Khớp chính xác với laser_frame trong URDF
            'inverted': False,
            'angle_compensate': True,
        }],
        output='screen'
    )

    # 3. Node giao tiếp Serial/UART giữa Raspberry Pi 5 và STM32 (Nhận cmd_vel -> gửi động cơ, đọc Encoder -> publish /odom)
    stm32_bridge_node = Node(
        package='robot_firmware',  # Package chứa node giao tiếp STM32
        executable='stm32_bridge',
        parameters=[{
            'port': '/dev/ttyAMA0', # Cổng UART trên Pi 5
            'baudrate': 115200
        }],
        output='screen'
    )

    return LaunchDescription([
        rsp,
        lidar_driver,
        stm32_bridge_node
    ])