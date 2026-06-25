import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int16MultiArray
import numpy as np

class LocationProcessor(Node):
    def __init__(self):
        super().__init__('calc_loc')

        self.loc = np.array([0, 0])
        self.dir_map = {
            "w": np.array([0, 1]),
            "s": np.array([0, -1]),
            "a": np.array([-1, 0]),
            "d": np.array([1, 0])
        }

        self.pub = self.create_publisher(Int16MultiArray, '/location', 10)
        self.sub = self.create_subscription(String, '/direction', self.callback, 10)

        self.timer = self.create_timer(0.5, self.publish_location)

    def callback(self, msg):
        self.get_logger().info(f"RECEIVED: {msg.data}")
        d = msg.data.lower()

        if d in self.dir_map:
            self.loc += self.dir_map[d]
            self.get_logger().info(f'Updated loc: {self.loc}')

    def publish_location(self):
        msg = Int16MultiArray()
        msg.data = [int(self.loc[0]), int(self.loc[1])]

        self.pub.publish(msg)

def main():
    rclpy.init()
    node = LocationProcessor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()