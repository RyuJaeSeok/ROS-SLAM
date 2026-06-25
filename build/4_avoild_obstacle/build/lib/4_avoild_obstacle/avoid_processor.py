import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import TwistStamped

class AvoidProcessor(Node):
    def __init__(self):
        super().__init__('avoid_processor')
        
        self.front_distance = None
        self.left_distance = None
        self.right_distance = None
        self.mode = 'FORWARD'
        self.turn_direction = 0.0
        self.obstacle_distance = 0.2
        self.clear_distance = 0.7
        self.create_subscription(Float32,'/front_distance',self.process_front_callback,10)
        self.create_subscription(Float32,'/left_distance',self.process_left_callback,10)
        self.create_subscription(Float32,'/right_distance',self.process_right_callback,10)
        self.cmd_vel_pub = self.create_publisher(TwistStamped,'/cmd_vel',10)

    def process_front_callback(self,msg):
        self.front_distance = msg.data
        self.process_avoidance()

    def process_left_callback(self,msg):
        self.left_distance = msg.data
        self.process_avoidance()

    def process_right_callback(self,msg):
        self.right_distance = msg.data
        self.process_avoidance()

    def process_avoidance(self):
        if None in (self.front_distance, self.left_distance, self.right_distance):
            return

        control = TwistStamped()
        control.header.stamp = self.get_clock().now().to_msg()
        control.header.frame_id = 'base_link'

        if self.mode == 'FORWARD':
            if self.front_distance < self.obstacle_distance:
                self.mode = 'TURN'
                control.twist.linear.x = 0.0

                if self.left_distance > self.right_distance:
                    self.turn_direction = 0.5
                    self.get_logger().info(
                        f'Detect Obstacle then Turn Left: front={self.front_distance:.2f} m, '
                        f'left={self.left_distance:.2f} m, right={self.right_distance:.2f} m'
                    )
                else:
                    self.turn_direction = -0.5
                    self.get_logger().info(
                        f'Detect Obstacle then Turn Right: front={self.front_distance:.2f} m, '
                        f'left={self.left_distance:.2f} m, right={self.right_distance:.2f} m'
                    )

                control.twist.angular.z = self.turn_direction
            else:
                control.twist.linear.x = 0.15
                control.twist.angular.z = 0.0
                self.get_logger().info(f'Go Forward: {self.front_distance:.2f} m')

        elif self.mode == 'TURN':
            if self.front_distance > self.clear_distance:
                self.mode = 'FORWARD'
                self.turn_direction = 0.0
                control.twist.linear.x = 0.15
                control.twist.angular.z = 0.0
                self.get_logger().info(f'Path Clear then Go Forward: {self.front_distance:.2f} m')
            else:
                control.twist.linear.x = 0.0
                control.twist.angular.z = self.turn_direction
                self.get_logger().info(
                    f'Keep Turning: front={self.front_distance:.2f} m, '
                    f'turn={self.turn_direction:.2f}'
                )

        self.cmd_vel_pub.publish(control)

def main(args=None):
    rclpy.init(args=args)
    node = AvoidProcessor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
