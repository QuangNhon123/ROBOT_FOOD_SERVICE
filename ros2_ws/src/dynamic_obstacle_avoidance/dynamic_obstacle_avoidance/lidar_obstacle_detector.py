
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

from dynamic_obstacle_avoidance.lidar_processor import scan_to_points
from dynamic_obstacle_avoidance.obstacle_clustering import (
    cluster_points,
    calculate_centroid
)


class LidarObstacleDetector(Node):

    def __init__(self):
        super().__init__('lidar_obstacle_detector')

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.scan_count = 0

        self.get_logger().info(
            'Lidar Obstacle Detector started. Waiting for /scan...'
        )

    def scan_callback(self, msg):

        # Buoc 1: Chuyen LaserScan thanh cac diem X, Y
        points = scan_to_points(msg)

        # Buoc 2: Gom cac diem thanh cac cum vat can
        clusters = cluster_points(
            points,
            threshold=0.15,
            min_points=3
        )

        self.scan_count += 1

        # Chi hien thi moi 10 lan quet de tranh Terminal qua tai
        if self.scan_count % 10 != 0:
            return

        self.get_logger().info(
            f'LiDAR points: {len(points)} | '
            f'Obstacles detected: {len(clusters)}'
        )

        # Buoc 3: Tinh toa do tam tung cum
        for i, cluster in enumerate(clusters, start=1):

            center = calculate_centroid(cluster)

            self.get_logger().info(
                f'Obstacle {i}: '
                f'{len(cluster)} points | '
                f'Centroid: '
                f'({center[0]:.2f}, {center[1]:.2f}) m'
            )


def main(args=None):

    rclpy.init(args=args)

    node = LidarObstacleDetector()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
