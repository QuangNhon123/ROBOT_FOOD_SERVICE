import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node
from rclpy.time import Time
from rclpy.duration import Duration
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped

from tf2_ros import Buffer, TransformListener, TransformException
from tf2_geometry_msgs import do_transform_point

from dynamic_obstacle_avoidance.lidar_processor import scan_to_points
from dynamic_obstacle_avoidance.obstacle_clustering import (
    cluster_points,
    calculate_centroid
)
from dynamic_obstacle_avoidance.obstacle_tracker import ObstacleTracker


class TrackedLidarDetector(Node):

    def __init__(self):
        super().__init__('tracked_lidar_detector')

        # Khoi tao TF
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(
            self.tf_buffer,
            self
        )
        self.lidar_callback_group = ReentrantCallbackGroup()
        # Khoi tao bo theo doi vat can
        self.tracker = ObstacleTracker(
            max_match_distance=0.5,
            max_missed_frames=3
        )

        # Nhan du lieu LiDAR
        self.subscription = self.create_subscription(
           LaserScan,
           '/scan',
           self.scan_callback,
           10,
           callback_group=self.lidar_callback_group
)

        self.scan_count = 0

        self.get_logger().info(
            'Tracked LiDAR Detector started. Waiting for /scan...'
        )

    def scan_callback(self, msg):

        # Buoc 1: Chuyen LaserScan thanh cac diem X, Y
        points = scan_to_points(msg)

        # Buoc 2: Gom diem thanh cac cum vat can
        clusters = cluster_points(
            points,
            threshold=0.15,
            min_points=3
        )

        # Thoi gian cua lan quet, su dung dong ho simulation
        timestamp = (
            msg.header.stamp.sec
            + msg.header.stamp.nanosec * 1e-9
        )

        detections = []

        try:
            # Lay phep bien doi tu laser_frame sang odom
            transform = self.tf_buffer.lookup_transform(
    'odom',
    msg.header.frame_id,
    Time.from_msg(msg.header.stamp),
    timeout=Duration(seconds=0.1)
)

            # Buoc 3: Chuyen tam tung cum sang he toa do odom
            for cluster in clusters:

                center = calculate_centroid(cluster)

                point = PointStamped()
                point.header = msg.header

                point.point.x = center[0]
                point.point.y = center[1]
                point.point.z = 0.0

                transformed_point = do_transform_point(
                    point,
                    transform
                )

                detections.append((
                    transformed_point.point.x,
                    transformed_point.point.y
                ))

        except TransformException as ex:
            self.get_logger().warning(
                f'TF transform unavailable: {ex}'
            )
            return

        # Buoc 4: Theo doi vat can trong he odom
        tracked_objects = self.tracker.update(
            detections,
            timestamp
        )

        self.scan_count += 1

        # Chi hien thi moi 10 lan quet
        if self.scan_count % 10 != 0:
            return

        self.get_logger().info(
            f'LiDAR points: {len(points)} | '
            f'Clusters: {len(clusters)} | '
            f'Tracked objects: {len(tracked_objects)}'
        )

        # Buoc 5: Hien thi ID, vi tri va van toc
        for obj in tracked_objects:

            x, y = obj['position']
            vx, vy = obj['velocity']

            self.get_logger().info(
                f"ID: {obj['id']} | "
                f"Position ODOM: ({x:.2f}, {y:.2f}) m | "
                f"Velocity: ({vx:.2f}, {vy:.2f}) m/s | "
                f"Speed: {obj['speed']:.2f} m/s"
            )


def main(args=None):

    rclpy.init(args=args)

    node = TrackedLidarDetector()

    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)

    try:
        executor.spin()

    except KeyboardInterrupt:
        pass

    finally:
        executor.shutdown()
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()