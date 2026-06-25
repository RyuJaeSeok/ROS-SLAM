import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray

class LocationSubscriber(Node):
    def __init__(self):
        super().__init__('my_loc')
        self.sub = self.create_subscription(Int16MultiArray, '/location', self.callback, 10)

    def callback(self, msg):
        x, y = msg.data
        self.get_logger().info(f'New location: {x}, {y}')

def main():
    rclpy.init()
    node = LocationSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()