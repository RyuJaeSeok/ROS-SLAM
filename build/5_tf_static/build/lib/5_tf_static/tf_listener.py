import rclpy
from rclpy.node import Node
from tf2_geometry_msgs import PointStamped
import tf2_ros
from sensor_msgs.msg import LaserScan
import math

class TFListener(Node):
    def __init__(self):
        super().__init__('tf_listener')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.create_subscription(LaserScan,'/scan',self.scan_callback,10)
        self.timer = self.create_timer(0.5, self.lookup_tf)

    def scan_callback(self, msg):
        self.scan_data = msg
        self.points = []
        for i, r in enumerate(msg.ranges):
            if not math.isfinite(r):
                continue

            point = PointStamped()
            point.header.frame_id = msg.header.frame_id
            point.header.stamp = msg.header.stamp
            angle = msg.angle_min + i * msg.angle_increment
            point.point.x = math.cos(angle) * r
            point.point.y = math.sin(angle) * r
            point.point.z = 0.0
            self.points.append(point)

        #     self.get_logger().info(
        #         f"Laser point[{i}]: x={point.point.x:.2f}, y={point.point.y:.2f}, z={point.point.z:.2f}"
        #     )
        # self.get_logger().info(f"Received LaserScan with {len(msg.ranges)} ranges")

    def lookup_tf(self):
        if not hasattr(self, 'points') or not self.points:
            return

        try:
            for i, point in enumerate(self.points):
                transformed = self.tf_buffer.transform(point, 'hello_laser')

                self.get_logger().info(
                    f"TF point[{i}]: x={transformed.point.x:.2f}, y={transformed.point.y:.2f}, z={transformed.point.z:.2f}"
                )

        except Exception as e:
            self.get_logger().warn(f"TF not ready: {e}")

def main():
    rclpy.init()
    node = TFListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()