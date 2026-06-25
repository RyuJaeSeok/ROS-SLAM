import math
import rclpy
from rclpy.node import Node
from sensor_msgs import msg
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32, Float32MultiArray


class LidarListener(Node):
    def __init__(self):
        super().__init__('lidar_listener')
        self.create_subscription(LaserScan,'/scan',self.scan_callback,10)
        self.front_distance_pub = self.create_publisher(Float32, '/front_distance', 10)
        self.left_distance_pub = self.create_publisher(Float32, '/left_distance', 10)
        self.right_distance_pub = self.create_publisher(Float32, '/right_distance', 10)
        # self.get_logger().info('listening /scan and publishing /front_distance, /scan_zones')

    def scan_callback(self, msg):

        front_ranges = []
        left_ranges = []
        right_ranges = []

        for i,distances in enumerate(msg.ranges):
            if not math.isfinite(distances):
                continue

            angle_rad = msg.angle_min + i * msg.angle_increment
            angle_deg = math.degrees(angle_rad)

            if angle_deg <= 15 or angle_deg >= 345:
                front_ranges.append((i, distances))
            elif 60 <= angle_deg <= 120:
                left_ranges.append((i, distances))
            elif 240 <= angle_deg <= 300:
                right_ranges.append((i, distances))


        close_front_distance = min(front_ranges, key=lambda x: x[1]) if front_ranges else (0, float('inf'))
        close_left_distance = min(left_ranges, key=lambda x: x[1]) if left_ranges else (0, float('inf'))
        close_right_distance = min(right_ranges, key=lambda x: x[1]) if right_ranges else (0, float('inf'))
        
        self.get_logger().info(f'front distance : {close_front_distance[1]:.2f} m')
        self.get_logger().info(f'left distance : {close_left_distance[1]:.2f} m')
        self.get_logger().info(f'right distance : {close_right_distance[1]:.2f} m')

        self.front_distance_pub.publish(Float32(data=close_front_distance[1]))
        self.left_distance_pub.publish(Float32(data=close_left_distance[1]))
        self.right_distance_pub.publish(Float32(data=close_right_distance[1])) 

def main(args=None):
    rclpy.init(args=args)
    node = LidarListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
