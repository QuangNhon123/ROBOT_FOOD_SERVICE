# 🤖 Robot Food Service (ROS 2 Humble + Hardware Integration)

Dự án phát triển hệ thống robot di động tự hành phục vụ thực phẩm (Food Service Robot). Hệ thống hỗ trợ hoàn chỉnh cả **môi trường mô phỏng 3D (Gazebo/RViz2)** lẫn **môi trường phần cứng thực tế (STM32, RPLiDARSensor, Serial/UART Communication, Nav2 Navigation)**.

---

## 📌 1. Giới thiệu, Tính năng & Lệnh chạy nhanh

* **Mô hình hóa Robot (URDF/XACRO):** Cấu trúc robot dạng mô-đun hóa gồm khung gầm, hệ thống động cơ vi sai và cảm biến LiDAR.
  * *Lệnh kiểm tra mô hình robot:*
    ```bash
    ros2 launch robot_description rsp.launch.py
    ```

* **Môi trường mô phỏng (Gazebo World):** Xây dựng thế giới 3D thực tế với không gian di chuyển và vật cản.
  * *Lệnh khởi chạy mô phỏng Gazebo + RViz2 + Spawn Robot:*
    ```bash
    ros2 launch robot_description sim_simulation.launch.py
    ```

* **Xây dựng bản đồ (SLAM)/Hiển thị Map_server:** Tích hợp package `slam_toolbox` để dựng bản đồ 2D từ cảm biến LiDAR (mô phỏng hoặc thật).
  * *Lệnh khởi chạy quét bản đồ SLAM:*
    ```bash
    ros2 launch robot_description slam.launch.py
    ```
  * Thay bằng map_server khi chạy Nav2:
    ```bash
     ros2 launch robot_description map_server.launch.py
    ```

* **Dẫn đường tự hành (Navigation2 / Nav2):** Lập kế hoạch chuyển động, né vật cản động/tĩnh và tự tìm đường đến điểm đích trên bản đồ.
  * *Lệnh khởi chạy Nav2:*
    ```bash
    ros2 launch robot_description navigation.launch.py
    ```

* **Kết nối Phần cứng Thực tế (Real Hardware):** Đọc cảm biến RPLiDAR thật và giao tiếp nối tiếp (Serial/UART) với vi điều khiển STM32 để nhận dữ liệu Odometry và truyền lệnh vận tốc (`cmd_vel`).
  * *Lệnh khởi chạy toàn bộ phần cứng thực:*
    ```bash
    ros2 launch robot_description real_hardware.launch.py
    ```

* **Lưu bản đồ (Map Saver):** Lưu kết quả quét thành định dạng `.yaml` và `.pgm`.
  * *Lệnh lưu bản đồ vào thư mục `map/`:*
    ```bash
    cd ~/robot_food_service/ros2_ws/src/robot_description/map
    ros2 run nav2_map_server map_saver_cli -f my_map
    ```

---

## 📁 2. Cấu trúc thư mục dự án
```text
robot_food_service/
├── README.md                               # Hướng dẫn chi tiết dự án
├── .gitignore                              # Cấu hình bỏ qua file build/log cho Git
└── ros2_ws/                                # ROS 2 Workspace chính
    └── src/
        ├── robot_description/              # Package mô tả robot, launch & cấu hình
        │   ├── package.xml                 # Khai báo phụ thuộc ROS 2
        │   ├── setup.py                    # Cấu hình cài đặt và nạp tài nguyên
        │   ├── config/                     # File cấu hình tham số
        │   │   ├── mapper_params_online_async.yaml  # Cấu hình thuật toán SLAM Toolbox
        │   │   ├── nav2_params.yaml                 # Cấu hình bộ dẫn đường Nav2 (Costmaps, Planner, Controller)
        │   │   └── rviz2_config.rviz                # Cấu hình giao diện hiển thị RViz2
        │   ├── launch/                     # Các file khởi chạy hệ thống
        │   │   ├── navigation.launch.py             # Launch hệ thống tự hành Nav2
        │   │   ├── real_hardware.launch.py          # Launch chạy phần cứng thật (LiDAR + STM32)
        │   │   ├── robot_launch.py                  # Launch khởi tạo tổng thể
        │   │   ├── rsp.launch.py                    # Launch Robot State Publisher (URDF)
        │   │   ├── sim_simulation.launch.py         # Launch mô phỏng Gazebo 3D
        │   │   └── slam.launch.py                  # Launch quét bản đồ SLAM
        │   ├── map/                        # Thư mục lưu bản đồ 2D (pgm, yaml)
        │   ├── resource/
        │   │   └── robot_description       # Marker package file
        │   ├── robot_description/
        │   │   └── __init__.py             # Python module init
        │   ├── urdf/                       # File mô tả hình học & cảm biến (XACRO)
        │   │   ├── gazebo_control.xacro        # Plugin động cơ vi sai cho Gazebo
        │   │   ├── lidar_sensor.xacro          # Mô tả cảm biến LiDAR
        │   │   ├── robot_core.xacro            # Khung gầm, bánh xe drive & castor
        │   │   ├── robot_demo.xacro            # File demo / backup
        │   │   └── robot_master.xacro          # File XACRO tổng hợp chính
        │   └── worlds/                     # Môi trường 3D
        │       └── gazebo_world.world          # Thế giới Gazebo thực tế
        ├── rplidar_ros/                    # Driver ROS 2 cho cảm biến RPLiDAR phần cứng
        ├── script/                         # Các script bổ trợ (Serial bridge, python nodes, v.v.)
        └── stm32/                          # Mã nguồn Firmware & giao tiếp vi điều khiển STM32
```
## 🛠️ 3. Chuẩn bị cho Môi trường Phần cứng Thật (STM32 & RPLiDAR)

Dự án thiết kế cấu trúc sẵn sàng để đưa code từ SIM ra ROBOT THẬT mà không cần thay đổi kiến trúc cốt lõi:

1. **Thư mục `stm32/`**:
   * Chứa chương trình chạy trên vi điều khiển STM32.
   * **Nhiệm vụ:** Đọc Encoders bánh xe, chạy thuật toán PID điều khiển động cơ DC, tính toán Odometry và gửi/nhận dữ liệu với máy tính nhúng qua UART/Serial.

2. **Package `rplidar_ros/`**:
   * Driver chính thức tương tác trực tiếp với mắt cảm biến RPLiDAR cắm qua cổng USB.
   * **Nhiệm vụ:** Bắn tia laser quét không gian và xuất dữ liệu ra topic `/scan` thực tế thay cho plugin mô phỏng.

3. **Thư mục `script/`**:
   * Chứa các script cầu nối (Serial Bridge) giữa ROS 2 nodes và bo mạch STM32 để đọc/ghi dữ liệu cổng nối tiếp `/dev/ttyUSB*`.

4. **File `real_hardware.launch.py`**:
   * Gom chung việc khởi chạy Driver RPLiDAR + Node giao tiếp STM32 + `robot_state_publisher` để sẵn sàng chạy SLAM/Nav2 trên robot thật.

---

## 🔗 4. Kiến trúc Cây TF (Transform Tree)

Cây TF quản lý liên kết tọa độ không gian giữa các bộ phận của robot và môi trường xung quanh:
``` text
map (Bản đồ tổng)
 └── odom (Gốc tọa độ xuất phát từ Encoder/STM32)
      └── base_footprint (Hình chiếu robot xuống mặt sàn)
           └── base_link (Tâm trọng thái robot)
                ├── left_wheel / right_wheel (Bánh xe)
                └── laser_frame (Mắt cảm biến RPLiDAR)
```

---

## ⚙️ 5. Yêu cầu môi trường & Phụ thuộc

### 5.1. Cấu hình cơ bản
* **Hệ điều hành:** Ubuntu 22.04 LTS
* **Phiên bản ROS 2:** ROS 2 Humble Hawksbill

### 5.2. Cài đặt các gói phụ thuộc (Dependencies)
Chạy lệnh sau trong Terminal để cài đặt đầy đủ các package cần thiết cho Gazebo, Nav2, SLAM và Teleop:

```bash
sudo apt update
sudo apt install -y ros-humble-gazebo-ros-pkgs \
                    ros-humble-xacro \
                    ros-humble-slam-toolbox \
                    ros-humble-nav2-bringup \
                    ros-humble-navigation2 \
                    ros-humble-nav2-map-server \
                    ros-humble-teleop-twist-keyboard
```


## 🚀 6. Quy trình Vận hành từng bước
### Bước 1: Biên dịch Workspace

Trước khi vận hành, luôn di chuyển về thư mục workspace chính và tiến hành build code:

```bash
    cd ~/robot_food_service/ros2_ws
    colcon build --symlink-install
    source install/setup.bash
```
### Bước 2A: Vận hành trong Môi trường MÔ PHỎNG (Gazebo 3D)
#### 1. Khởi động môi trường, Gazebo, SLAM, Rviz2, Map đã lưu,... tất cả đều chạy bằng file simulation
```bash
    cd ~/robot_food_service/ros2_ws
    source install/setup.bash
    ros2 launch robot_description sim_simulation.launch.py
```
#### 2. Điều khiển Robot di chuyển
```bash
    ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
#### 3. Lưu bản đồ đã quét (Map saver)
```bash
    cd ~/robot_food_service/ros2_ws/src/robot_description/map
    ros2 run nav2_map_server map_saver_cli -f my_map
```
#### 4. Build lại để lưu map để cập nhật sang install/
```bash
    cd ~/robot_food_service/ros2_ws
    colcon build --symlink-install
    source install/setup.bash
```
#### 5. Khởi chạy tự hành Nav2 (Thêm 1 terminal - Khi đã có bản đồ sẵn)
```bash
    cd ~/robot_food_service/ros2_ws
    source install/setup.bash
    ros2 launch robot_description navigation.launch.py
```
## Bước 2B: Vận hành trên PHẦN CỨNG THẬT (Real Robot)
```text
.... (cập nhật sau)
```