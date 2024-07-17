import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from launch_ros.actions import Node

#En este código se inician los nodos necesarios para la simulación en gazebo 

def generate_launch_description():
    urdf_path = '/home/ubb/Downloads/ros2_ws_final/ros2_ws/src/3dof/urdf/robot.xacro'

#Este es el nodo con el diseño del robot
    pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            'robot_description': Command(['xacro ', urdf_path])
        }]
    )
#Este nodo recibe el diseño del robot para simularlo en gazebo
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=['-entity', 'robot', '-topic', 'robot_description'],
        output='screen'
    )
#en estas dos lineas se inicia gazebo en un mundo personalizado
    world = '/home/ubb/Downloads/ros2_ws_final/ros2_ws/src/3dof/world/obstacule.world'
    gazebo = ExecuteProcess(cmd=['gazebo', '--verbose', world,'-s', 'libgazebo_ros_factory.so'], output='screen')

#Este nodo envía una posición constante al topico /joint_trajectory para mover al brazo a una
#posicion designada
    operacion = Node(
            package='3dof',
            executable='operacion',
            name='operacion',
            output='screen'
        )

#Este nodo procesa los datos del robot para simular la posición de las articulaciones
    controller_manager = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_trajectory_controller'
        ],
    )
#Este nodo envia la posición calculada por controller_manager a gazebo para visualizarla en la simulación
    joint_broad_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster'
        ],
    )
#Se ejecutan los procesos para la simulación en gazebo
    return LaunchDescription([
        pub,
        gazebo,
        spawn_entity,
        controller_manager,
        joint_broad_controller,
        #operacion #Esta linea es para enviar una posición de forma permanente, en caso de quere usar otra posición, se comenta esta linea.
    ])