
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class MovingObstacle(Node):

    def __init__(self):
        super().__init__('moving_obstacle_controller')

        # Tao publisher gui van toc cho vat can
        self.publisher = self.create_publisher(
            Twist,
            '/moving_obstacle/cmd_vel',
            10
        )

        # Cau hinh chuyen dong
        self.speed = 0.45
        self.direction = 1
        self.last_switch = self.get_clock().now()

        # Goi ham move_obstacle moi 0.1 giay
        self.timer = self.create_timer(
            0.1,
            self.move_obstacle
        )

        self.get_logger().info(
            'Moving obstacle controller started'
        )

    def move_obstacle(self):
        now = self.get_clock().now()

        elapsed = (
            now - self.last_switch
        ).nanoseconds / 1e9

        # Dao chieu sau moi  giay
        if elapsed >= 10:
            self.direction *= -1
            self.last_switch = now

        # Tao lenh van toc
        msg = Twist()
        msg.linear.y = self.speed * self.direction

        # Gui lenh den Gazebo
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = MovingObstacle()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.publisher.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
