from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    ld = LaunchDescription()


    # # kill gazebo yang masih hidup
    # ld.add_action(ExecuteProcess(cmd=['pkill', '-9', '-f', 'gzserver'], output='screen'))
    # ld.add_action(ExecuteProcess(cmd=['pkill', '-9', '-f', 'gzclient'], output='screen'))
    # ld.add_action(ExecuteProcess(cmd=['pkill', '-9', '-f', 'gazebo'], output='screen'))


#===========================================================================================================================================================================================================
	#Define path

    ##define path package
    robot_path = FindPackageShare('robot_description')

	##define path model urdf
    model_path = PathJoinSubstitution(['urdf', 'assy.urdf'])

	##define path setting rviz
    rviz_config = PathJoinSubstitution([robot_path, 'rviz', 'urdf.rviz'])

    urdf_path = PathJoinSubstitution([robot_path, model_path])




#============================================================================================================================================================================================================
    

    robot_description_content = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(package='robot_state_publisher',executable='robot_state_publisher',parameters=[{'robot_description': robot_description_content,'use_sim_time': True,}])

    ld.add_action(robot_state_publisher_node)


#######################################################################################################################################################################################################################



	#untuk buat flag contohnya tulis command ...mapping:=true/false tuje nak bagitahu nak run macam mana atau nak run ke tak
    ld.add_action(DeclareLaunchArgument(name='jsp_gui', default_value='false', choices=['true', 'false'],
                                    description='Flag to enable joint_state_publisher_gui'))
    ld.add_action(DeclareLaunchArgument(name='jsp', default_value='false', choices=['true', 'false'],
                                    description='Flag to enable joint_state_publisher'))
    ld.add_action(DeclareLaunchArgument(name='rviz_config', default_value = rviz_config, description = 'path rviz_config kek mano'))

#===================================================================================================================================================================================================================

 #Depending on gui parameter, either launch joint_state_publisher or joint_state_publisher_gui
    ld.add_action(Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        condition=IfCondition(LaunchConfiguration('jsp_gui'))
    ))

    ld.add_action(Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('jsp_gui'))
    ))

    ld.add_action(Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rviz_config')],
        parameters=[{'use_sim_time': True}],
    ))
    




    return ld
 


