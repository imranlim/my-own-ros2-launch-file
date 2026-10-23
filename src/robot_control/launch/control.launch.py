from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():



    ld = LaunchDescription()

    controller_config = PathJoinSubstitution([FindPackageShare('robot_control'), 'config', 'teleop_twist.yaml'])

    joy_config = PathJoinSubstitution([FindPackageShare('robot_control'), 'config', 'joy_config.yaml'])

    keyboard_twist = PathJoinSubstitution([FindPackageShare('robot_control'), 'config', 'keyboard_twist.yaml'])

    twist_mux_path = PathJoinSubstitution([FindPackageShare('robot_control'), 'config', 'twist_mux.yaml'])

#==========================================================================================================================================================================================================
    # launch joy

	# 1. Hardware driver: reads the physical controller and publishes to /joy
    ld.add_action(Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        output='log',
        parameters=[joy_config, {'use_sim_time': True}]
    ))

    # 2. Teleop node: translates /joy to /cmd_vel using your config file
    ld.add_action(Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        output='log',
        parameters=[controller_config, {'use_sim_time': True}],
        remappings=[('/cmd_vel', '/joy/cmd_vel')]
    ))




    ld.add_action(TimerAction(
    period=5.0,
    actions=[
        ExecuteProcess(
            cmd=[
                'bash', '-c',
                'exec ros2 run teleop_twist_keyboard teleop_twist_keyboard '
                '--ros-args '
                '--remap /cmd_vel:=/key/cmd_vel '
                '--params-file "$1" '
                '-p use_sim_time:=true < /dev/tty',
                'keyboard',
                keyboard_twist
            ],
            output='screen',
            emulate_tty=True
        )
    ]
))



    ld.add_action(Node(
            package='twist_mux',
            executable='twist_mux',
            name='twist_mux_node',
            output='log',
            parameters=[twist_mux_path,{'use_sim_time': True},],
            remappings=[('/cmd_vel_out', '/cmd_vel')]

            ))
    



    return ld