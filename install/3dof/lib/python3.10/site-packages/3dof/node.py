import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
import math

class JointController(Node):
    def __init__(self):
        super().__init__('joint_controller')
        self.publisher_ = self.create_publisher(JointTrajectory, '/set_joint_trajectory', 10)
        self.subscription = self.create_subscription(
            JointTrajectory,
            '/set_joint_trajectory',
            self.trajectory_callback,
            10)
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.joint_names = ['joint_1', 'joint_2', 'joint_3']
        self.current_positions = [0.0, 0.0, 0.0]
        self.t = 0.0

    def joint_state_callback(self, msg):
        for i, name in enumerate(self.joint_names):
            if name in msg.name:
                self.current_positions[i] = msg.position[msg.name.index(name)]

    def timer_callback(self):
        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = self.joint_names
        point = JointTrajectoryPoint()
        point.positions = [
            0.5 * math.sin(self.t),
            0.5 * math.sin(self.t + math.pi/2),
            0.5 * math.sin(self.t + math.pi)
        ]
        point.time_from_start.sec = 1
        trajectory_msg.points.append(point)
        self.publisher_.publish(trajectory_msg)
        self.t += 0.1

    def trajectory_callback(self, msg):
        self.get_logger().info('Received trajectory command')
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    joint_controller = JointController()
    rclpy.spin(joint_controller)
    joint_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()