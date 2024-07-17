import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class TrajectoryPublisher(Node):

    def __init__(self):
        super().__init__('trajectory_publisher')
        self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = JointTrajectory()
        msg.joint_names = ['joint_1', 'joint_2', 'joint_3']
        
        point = JointTrajectoryPoint()
        point.positions = [0.6, 1.423, 1.564]
        point.time_from_start = Duration(sec=5, nanosec=0)

        msg.points.append(point)
        
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
