import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster

class StaticFramePublisher(Node):
    def __init__(self):
        super().__init__('static_tf_broadcaster')
        self.broadcaster = StaticTransformBroadcaster(self)
        
        t1 = TransformStamped()
        t1.header.stamp = self.get_clock().now().to_msg()
        t1.header.frame_id = 'hello_base_link'
        t1.child_frame_id = 'hello_laser'
        
        t1.transform.translation.x = 0.2
        t1.transform.translation.y = 0.3
        t1.transform.translation.z = 1.0

        t1.transform.rotation.x = 0.0
        t1.transform.rotation.y = 0.0
        t1.transform.rotation.z = 0.0
        t1.transform.rotation.w = 1.0

        self.broadcaster.sendTransform(t1)

        t2 = TransformStamped()
        t2.header.stamp = self.get_clock().now().to_msg()
        t2.header.frame_id = 'hello_base_link'
        t2.child_frame_id = 'hello_imu'
        
        t2.transform.translation.x = 0.0
        t2.transform.translation.y = 0.0
        t2.transform.translation.z = -1.0

        t2.transform.rotation.x = 0.0
        t2.transform.rotation.y = 0.0
        t2.transform.rotation.z = 0.0
        t2.transform.rotation.w = 1.0

        self.broadcaster.sendTransform(t2)

def main():
    rclpy.init()
    node = StaticFramePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()