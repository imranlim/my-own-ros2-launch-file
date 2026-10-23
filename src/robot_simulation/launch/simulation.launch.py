from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

def generate_launch_description():

    ld = LaunchDescription()

    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('robot_description'), 'launch', 'display.launch.py']),
    ))


    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('robot_control'), 'launch', 'control.launch.py']),
    ))

    
    ld.add_action(Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager-timeout', '30'],
        output='screen'))


    ld.add_action(Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_drive_base_controller', '--controller-manager-timeout', '30'],
        remappings=[
            ('~/diff_drive_base_controller/cmd_vel_unstamped', '/cmd_vel')],
        output='screen',
    ))

    world_path = PathJoinSubstitution([FindPackageShare('robot_simulation'),'world'])

    

    



    #=========================================================================================================================================================================================================

#                                                                                             GAZEBO

    
   # Spawn robot into Gazebo
# spawn_entity.py creates the physical body: This node actually places the 3D model of your robot into the Gazebo simulator. 
# Without it, Gazebo will just be an empty world.

# spawner creates the nervous system: This node tells ROS 2 how the robot's 
# joints are moving in Gazebo. It reads the joint positions (like wheels turning or arms moving) and 
# publishes them so that other ROS 2 tools (like RViz, navigation, or TF) know the robot's current pose.
    
    ld.add_action(Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='urdf_spawner',
        arguments=[
            '-topic', '/robot_description',
            '-entity', 'robot',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.4',       # Centers your 0.5m box cleanly onto the floor
            '-unpause'
        ],
        output='screen',
    ))







    # Gazebo World load

    
    # ld.add_action(SetEnvironmentVariable(
    #     name='GAZEBO_MODEL_PATH',
    #     value=[world_path, ':', os.environ.get('GAZEBO_MODEL_PATH', '')]
    #     ))



    # Gazebo GUI
    ld.add_action(DeclareLaunchArgument(name='gui',default_value='true'))

    

    ld.add_action(
        IncludeLaunchDescription(PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare('gazebo_ros'),'launch', 'gazebo.launch.py'])]),
            launch_arguments={
                'gui': LaunchConfiguration('gui'),
                'pause': 'false',
                'world': PathJoinSubstitution([FindPackageShare('robot_simulation'), 'world', 'robot_world.world'])
            }.items()
        )
    )



    return ld