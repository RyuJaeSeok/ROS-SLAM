import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import math

class DynamicFramePublisher(Node):
    def __init__(self):
        super().__init__('dynamic_tf_broadcaster')
        self.broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.publish_tf)
        self.angle = 0.0

    def publish_tf(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'hello_odom'
        t.child_frame_id = 'hello_base_link'

        t.transform.translation.x = math.cos(self.angle)
        t.transform.translation.y = math.sin(self.angle)
        t.transform.translation.z = 0.0

        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.broadcaster.sendTransform(t)
        self.angle += 0.05

def main():
    rclpy.init()
    node = DynamicFramePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()