from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():

    urdf_path = '/home/ubb/Downloads/ros2_ws_final/ros2_ws/src/3dof/urdf/robot.urdf'
    with open(urdf_path,'r') as i:
        robot_desc = i.read()

    pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output='screen',
        parameters=[{
            'robot_description': robot_desc
        }]
    )

    joint = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output='screen'
    )

    rviz = ExecuteProcess(
        cmd=['rviz2', '-d', '/home/ubb/Downloads/ros2_ws_final/ros2_ws/src/3dof/config/config.rviz'],
        output='screen'
    )

    return LaunchDescription([
        pub,
        joint,
        rviz
    ])