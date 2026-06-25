import math

import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.node import Node


class InitialPosePublisher(Node):
    def __init__(self):
        super().__init__('initial_pose_publisher')
        self.declare_parameter('x', 0.0)
        self.declare_parameter('y', 0.0)
        self.declare_parameter('yaw', 0.0)
        self.declare_parameter('frame_id', 'map')
        self.declare_parameter('publish_count', 10)

        self.publisher = self.create_publisher(PoseWithCovarianceStamped, 'initialpose', 10)
        self.remaining = self.get_parameter('publish_count').value
        self.timer = self.create_timer(0.5, self.publish_initial_pose)

    def publish_initial_pose(self):
        if self.remaining <= 0:
            self.get_logger().info('Initial pose published.')
            rclpy.shutdown()
            return

        x = float(self.get_parameter('x').value)
        y = float(self.get_parameter('y').value)
        yaw = float(self.get_parameter('yaw').value)
        frame_id = self.get_parameter('frame_id').value

        msg = PoseWithCovarianceStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = frame_id
        msg.pose.pose.position.x = x
        msg.pose.pose.position.y = y
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.orientation.z = math.sin(yaw / 2.0)
        msg.pose.pose.orientation.w = math.cos(yaw / 2.0)
        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.06853891945200942

        self.publisher.publish(msg)
        self.remaining -= 1


def main(args=None):
    rclpy.init(args=args)
    node = InitialPosePublisher()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
