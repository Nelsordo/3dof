import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    urdf_path = '/home/ubb/Downloads/ros2_ws_final/ros2_ws/src/3dof/urdf/robot.xacro'

    pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            'robot_description': Command(['xacro ', urdf_path])
        }]
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=['-entity', 'robot', '-topic', 'robot_description'],
        output='screen'
    )

    world = '/home/ubb/Downloads/ros2_ws_final/ros2_ws/src/3dof/world/obstacule.world'
    gazebo = ExecuteProcess(cmd=['gazebo', '--verbose', world,'-s', 'libgazebo_ros_factory.so'], output='screen')

    operacion = Node(
            package='3dof',
            executable='operacion',
            name='operacion',
            output='screen'
        )
#)

    controller_manager = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_trajectory_controller'
        ],
    )
    
    joint_broad_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster'
        ],
    )
    return LaunchDescription([
        pub,
        gazebo,
        spawn_entity,
        controller_manager,
        joint_broad_controller,
        #operacion
    ])