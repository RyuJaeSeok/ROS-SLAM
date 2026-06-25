import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import random


class RandomMotion(Node):
    def __init__(self):
        super().__init__('random_motion')
        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.timer = self.create_timer(0.2, self.timer_callback)

    def timer_callback(self):
        mag = TwistStamped()

        mag.twist.linear.x = 0.3
        mag.twist.angular.z = random.uniform(-2.5, 1.8)  # Random angular speed
        self.cmd_pub.publish(mag)


def main():
    rclpy.init()
    node = RandomMotion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()