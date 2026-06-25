import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


class ActionMove(Node):
    def __init__(self):
        super().__init__('action_move')
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def move_callback(self,msg):
        self.cmd_vel_pub.publish(msg)
        self.get_logger().info(f'Publishing cmd_vel: linear.x={msg.linear.x:.2f}, angular.z={msg.angular.z:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = ActionMove()
    rclpy.spin(node)
    node.destroy_node()

if __name__ == '__main__':
    main()