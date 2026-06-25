import math
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
import rclpy
from rclpy.node import Node
from tf_transformations import euler_from_quaternion


class SimpleYawObstacleAvoider(Node):
    def __init__(self):
        super().__init__('simple_yaw_obstacle_avoider')

        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        self.state = "MOVE"

        self.front_threshold = 0.30
        self.caution_distance = 0.60
        self.linear_speed = 0.08
        self.back_speed = 0.04
        self.angular_speed = 0.25
        
        self.current_yaw = 0.0
        self.target_yaw = 0.0
        self.turn_dir = 1
        self.yaw_tolerance = 0.05
        self.rotation_angle = math.pi / 4
        self.back_until = 0.0
        self.back_duration = 0.6

        self.turn_sensitivity = 0.18
        self.max_turn_speed = 0.22
        self.angular_filter = 0.0
        self.angular_deadband = 0.04

    def odom_callback(self, msg: Odometry):
        q = msg.pose.pose.orientation
        quat = [q.x, q.y, q.z, q.w]
        _, _, self.current_yaw = euler_from_quaternion(quat)

    def scan_callback(self, scan: LaserScan):
        left_vals = [r for r in scan.ranges[:20] if math.isfinite(r)]
        left_avg = sum(left_vals) / len(left_vals) if left_vals else 5.0
        left_min = min(left_vals) if left_vals else 5.0

        right_vals = [r for r in scan.ranges[-20:] if math.isfinite(r)]
        right_avg = sum(right_vals) / len(right_vals) if right_vals else 5.0
        right_min = min(right_vals) if right_vals else 5.0

        difference = left_avg - right_avg
        angular_adjustment = difference * self.turn_sensitivity
        angular_adjustment = max(
            -self.max_turn_speed,
            min(self.max_turn_speed, angular_adjustment)
        )
        if abs(angular_adjustment) < self.angular_deadband:
            angular_adjustment = 0.0
        self.angular_filter = 0.8 * self.angular_filter + 0.2 * angular_adjustment

        front_vals = left_vals + right_vals
        front_min = min(front_vals) if front_vals else float('inf')

        twist = TwistStamped()

        if self.state == "BACK":
            if time.monotonic() < self.back_until:
                twist.twist.linear.x = -self.back_speed
                twist.twist.angular.z = 0.0
            else:
                self.target_yaw = self.normalize_angle(
                    self.current_yaw + self.turn_dir * self.rotation_angle
                )
                self.state = "TURN"

        elif self.state == "TURN":
            angle_diff = self.normalize_angle(self.target_yaw - self.current_yaw)
            if abs(angle_diff) > self.yaw_tolerance:
                twist.twist.linear.x = 0.0
                twist.twist.angular.z = self.angular_speed * (1 if angle_diff > 0 else -1)
            
            elif front_min < self.front_threshold:
                self.state = "BACK"
                self.back_until = time.monotonic() + self.back_duration
                twist.twist.linear.x = -self.back_speed
                twist.twist.angular.z = 0.0
                
            else:
                self.state = "MOVE"
        else:
            if front_min > self.front_threshold:
                if front_min < self.caution_distance:
                    twist.twist.linear.x = self.linear_speed * 0.5
                    twist.twist.angular.z = self.angular_filter
                else:
                    twist.twist.linear.x = self.linear_speed
                    twist.twist.angular.z = 0.0
            else:
                self.state = "TURN"

                self.turn_dir = 1 if left_avg > right_avg else -1
                self.target_yaw = self.normalize_angle(
                    self.current_yaw + self.turn_dir * self.rotation_angle
                )

                twist.twist.linear.x = 0.0
                twist.twist.angular.z = self.angular_speed * self.turn_dir

        self.cmd_pub.publish(twist)

    def normalize_angle(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))


def main():
    rclpy.init()
    node = SimpleYawObstacleAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
