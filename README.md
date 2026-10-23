# My Own ROS 2 Robot Workspace

A personal ROS 2 robot workspace containing my robot description, Gazebo simulation, robot control, launch files, controller configuration, joystick control, keyboard teleoperation, and RViz visualization.

This README documents **how my code is actually written and connected**.

It is intended as a personal reference so that I can come back later and understand:

- which package does what
- which launch file starts which nodes
- which launch file calls another launch file
- how my URDF is assembled
- how my robot description reaches RViz and Gazebo
- how joystick control works
- how keyboard control works
- how `twist_mux` combines the control inputs
- how Gazebo controllers are started
- how `/cmd_vel` reaches the differential-drive controller
- where each configuration file is used
- what I need to change when modifying the system

This README describes the code **as it currently exists**, including things that are unused, commented out, or could be improved.

---

# 1. Workspace Overview

My workspace is:

```text
ros2_ws/
└── src/
    ├── robot_description/
    ├── robot_simulation/
    └── robot_control/
```

The three packages have different responsibilities.

```text
                    ros2_ws
                       |
                       +------------------------+
                       |                        |
                       v                        v
              robot_description         robot_simulation
                       |                        |
                       |                        |
                       v                        v
                 Robot model              Gazebo world
                 URDF/Xacro               Controllers
                 RViz                     Simulation
                       |
                       |
                       +------------+
                                    |
                                    v
                              robot_control
                                    |
                                    v
                         Joystick / Keyboard
                              /cmd_vel
```

---

# 2. My Three Packages

## `robot_description`

This package contains the physical description of my robot.

It contains:

```text
robot_description/
├── launch/
│   └── display.launch.py
│
├── urdf/
│   ├── assy.urdf
│   ├── body.urdf
│   ├── wheel_left.urdf
│   ├── wheel_right.urdf
│   ├── shaft.urdf
│   └── caster.urdf
│
├── rviz/
│   └── urdf.rviz
│
├── scripts/
│   └── start_node_red.sh
│
├── config/
├── package.xml
└── CMakeLists.txt
```

Its main job is:

```text
URDF files
    |
    v
assy.urdf
    |
    v
robot_description
    |
    +------> robot_state_publisher
    |
    +------> Gazebo
    |
    +------> RViz
```

---

# 3. `robot_simulation`

This package contains my Gazebo simulation.

```text
robot_simulation/
├── launch/
│   └── simulation.launch.py
│
├── config/
│   ├── joints.yaml
│   └── diffdrive.yaml
│
├── world/
│   ├── robot_world.world
│   └── turtlebot3_world/
│       ├── model.sdf
│       ├── model-1_4.sdf
│       ├── model.config
│       └── meshes/
│           ├── wall.dae
│           └── hexagon.dae
│
├── package.xml
└── CMakeLists.txt
```

Its job is to provide:

- Gazebo world
- robot spawning
- controller spawners
- diff-drive configuration
- joint-state configuration

---

# 4. `robot_control`

This package contains my robot control system.

```text
robot_control/
├── launch/
│   └── control.launch.py
│
├── config/
│   ├── joy_config.yaml
│   ├── teleop_twist.yaml
│   ├── twist_mux.yaml
│   └── keyboard_twist.yaml
│
├── package.xml
└── CMakeLists.txt
```

Its control flow is:

```text
Joystick
   |
   v
joy_node
   |
   v
/joy
   |
   v
teleop_twist_joy
   |
   v
/joy/cmd_vel
   |
   |
   +--------------------+
                        |
Keyboard                |
   |                    |
   v                    |
/key/cmd_vel             |
   |                    |
   +---------+----------+
             |
             v
        twist_mux
             |
             v
          /cmd_vel
             |
             v
diff_drive_base_controller
             |
             v
          Wheels
```

This is the main control architecture in my project.

---

# 5. Complete Launch File Structure

There are three important launch files.

```text
robot_description
└── launch/
    └── display.launch.py

robot_control
└── launch/
    └── control.launch.py

robot_simulation
└── launch/
    └── simulation.launch.py
```

The most important relationship is:

```text
simulation.launch.py
        |
        +----------------------------+
        |                            |
        v                            v
display.launch.py             control.launch.py
        |                            |
        v                            v
robot_state_publisher       joy / teleop / keyboard
RViz                        twist_mux
        |
        |
        +--------------------------+
                                   |
                                   v
                              Gazebo simulation
```

---

# 6. Main Launch File: `simulation.launch.py`

Location:

```text
robot_simulation/launch/simulation.launch.py
```

This is effectively my main simulation launch file.

It starts:

1. `display.launch.py`
2. `control.launch.py`
3. `joint_state_broadcaster` spawner
4. `diff_drive_base_controller` spawner
5. Gazebo robot spawner
6. Gazebo itself

---

# 7. Imports in `simulation.launch.py`

My code starts with:

```python
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
```

Not all of these imports are currently used.

## Actually used

My file uses:

```python
LaunchDescription
DeclareLaunchArgument
IncludeLaunchDescription
PathJoinSubstitution
LaunchConfiguration
Node
FindPackageShare
PythonLaunchDescriptionSource
```

## Currently unused

These are imported but not currently used in the active code:

```python
ExecuteProcess
SetEnvironmentVariable
IfCondition
UnlessCondition
ParameterValue
Command
os
```

I should remember this because if I clean up the file later, these imports can be removed unless I start using them again.

---

# 8. Creating the Launch Description

My code does:

```python
def generate_launch_description():

    ld = LaunchDescription()
```

Instead of putting everything directly inside:

```python
return LaunchDescription([
    ...
])
```

I create an `ld` object first.

Then I repeatedly use:

```python
ld.add_action(...)
```

to add each action.

My launch structure is therefore:

```text
generate_launch_description()
        |
        v
ld = LaunchDescription()
        |
        +-- add display launch
        |
        +-- add control launch
        |
        +-- add joint state spawner
        |
        +-- add diff drive spawner
        |
        +-- add Gazebo robot spawner
        |
        +-- add GUI argument
        |
        +-- add Gazebo launch
        |
        v
return ld
```

---

# 9. `simulation.launch.py` Calls `display.launch.py`

My code:

```python
ld.add_action(IncludeLaunchDescription(
    PathJoinSubstitution([
        FindPackageShare('robot_description'),
        'launch',
        'display.launch.py'
    ]),
))
```

This is one of the most important parts of my project.

My simulation launch file does not recreate the RViz and robot-description setup itself.

Instead it says:

```text
Find robot_description package
        |
        v
Find launch/
        |
        v
Find display.launch.py
        |
        v
Include it
```

Therefore:

```text
simulation.launch.py
        |
        v
robot_description/launch/display.launch.py
```

---

# 10. `simulation.launch.py` Calls `control.launch.py`

My code:

```python
ld.add_action(IncludeLaunchDescription(
    PathJoinSubstitution([
        FindPackageShare('robot_control'),
        'launch',
        'control.launch.py'
    ]),
))
```

This means my simulation launch also starts the entire control system.

The relationship is:

```text
simulation.launch.py
        |
        v
robot_control
        |
        v
control.launch.py
```

So I do not need to separately run:

```bash
ros2 launch robot_control control.launch.py
```

if I already run my simulation launch.

---

# 11. My `FindPackageShare`

I use:

```python
FindPackageShare('robot_description')
```

to locate the installed `robot_description` package.

Then I construct:

```text
robot_description
    |
    +-- launch
         |
         +-- display.launch.py
```

Likewise:

```python
FindPackageShare('robot_control')
```

finds:

```text
robot_control
    |
    +-- launch
         |
         +-- control.launch.py
```

This is how my launch files find each other without hardcoding `/home/...` paths.

---

# 12. Joint State Broadcaster Spawner

My simulation launch starts:

```python
ld.add_action(Node(
    package='controller_manager',
    executable='spawner',
    arguments=[
        'joint_state_broadcaster',
        '--controller-manager-timeout',
        '30'
    ],
    output='screen'
))
```

This starts the controller-manager spawner.

It asks the controller manager to start:

```text
joint_state_broadcaster
```

I also specifically give it:

```text
--controller-manager-timeout 30
```

meaning it can wait up to 30 seconds for the controller manager.

---

# 13. Diff Drive Controller Spawner

My code:

```python
ld.add_action(Node(
    package='controller_manager',
    executable='spawner',
    arguments=[
        'diff_drive_base_controller',
        '--controller-manager-timeout',
        '30'
    ],
    remappings=[
        (
            '~/diff_drive_base_controller/cmd_vel_unstamped',
            '/cmd_vel'
        )
    ],
    output='screen',
))
```

This starts:

```text
diff_drive_base_controller
```

The important part is the remapping:

```text
~/diff_drive_base_controller/cmd_vel_unstamped
                    |
                    v
                 /cmd_vel
```

Therefore my final velocity command topic is:

```text
/cmd_vel
```

This matches the output from my `twist_mux`.

---

# 14. My Control Chain

The complete control chain is therefore:

```text
Joystick
    |
    v
/joy
    |
    v
teleop_twist_joy
    |
    v
/joy/cmd_vel
    |
    |
    +-----------------------+
                            |
Keyboard                    |
    |                       |
    v                       |
/key/cmd_vel                |
    |                       |
    +----------+------------+
               |
               v
           twist_mux
               |
               v
            /cmd_vel
               |
               v
diff_drive_base_controller
               |
               v
         left/right wheels
```

This is the most important diagram for understanding my robot control.

---

# 15. `world_path` in `simulation.launch.py`

My code creates:

```python
world_path = PathJoinSubstitution([
    FindPackageShare('robot_simulation'),
    'world'
])
```

So this creates a path pointing to:

```text
robot_simulation/world
```

However, my current code does not actually use `world_path` in an active action.

The code that would use it is commented out:

```python
# ld.add_action(SetEnvironmentVariable(
#     name='GAZEBO_MODEL_PATH',
#     value=[world_path, ':', os.environ.get('GAZEBO_MODEL_PATH', '')]
# ))
```

Therefore, as my code currently stands:

```text
world_path
   |
   X
not actively used
```

---

# 16. Gazebo Robot Spawner

My code:

```python
ld.add_action(Node(
    package='gazebo_ros',
    executable='spawn_entity.py',
    name='urdf_spawner',
    arguments=[
        '-topic', '/robot_description',
        '-entity', 'robot',
        '-x', '0.0',
        '-y', '0.0',
        '-z', '0.4',
        '-unpause'
    ],
    output='screen',
))
```

This is how my robot gets inserted into Gazebo.

The important part is:

```text
-topic /robot_description
```

The spawner gets the robot description from:

```text
/robot_description
```

which is published/generated by my robot description setup.

I name the Gazebo entity:

```text
robot
```

and spawn it at:

```text
x = 0.0
y = 0.0
z = 0.4
```

I also use:

```text
-unpause
```

so the spawned entity is not left in a paused state.

---

# 17. Gazebo GUI Argument

My code declares:

```python
ld.add_action(
    DeclareLaunchArgument(
        name='gui',
        default_value='true'
    )
)
```

Therefore I can control Gazebo GUI with:

```bash
gui:=true
```

or:

```bash
gui:=false
```

The default is:

```text
true
```

---

# 18. Gazebo Launch File

My code includes Gazebo's own launch file:

```python
IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        PathJoinSubstitution([
            FindPackageShare('gazebo_ros'),
            'launch',
            'gazebo.launch.py'
        ])
    ]),
    launch_arguments={
        'gui': LaunchConfiguration('gui'),
        'pause': 'false',
        'world': PathJoinSubstitution([
            FindPackageShare('robot_simulation'),
            'world',
            'robot_world.world'
        ])
    }.items()
)
```

So my code is effectively doing:

```text
Find gazebo_ros
      |
      v
launch/gazebo.launch.py
      |
      +-- gui = my gui argument
      |
      +-- pause = false
      |
      +-- world = robot_world.world
```

---

# 19. My Gazebo World

My world file is:

```text
robot_simulation/world/robot_world.world
```

It contains:

```text
ground_plane
sun
turtlebot3_world
```

It also sets:

```text
shadows = false
```

and defines the Gazebo camera.

---

# 20. My Gazebo Camera

My world contains:

```xml
<camera name='user_camera'>
    <pose>0.0 -25.0 35.0 0 0.9 1.57</pose>
    <view_controller>orbit</view_controller>
    <projection_type>perspective</projection_type>
</camera>
```

So when Gazebo opens, my initial camera is positioned above and behind the arena to give a larger view.

---

# 21. My Gazebo Physics

My world uses:

```xml
<physics type="ode">
```

with:

```text
real_time_update_rate = 1000
max_step_size = 0.001
real_time_factor = 1
```

I also configure the ODE solver.

The important point is that these are my simulation physics settings, not controller settings.

---

# 22. My TurtleBot3 World Model

My world includes:

```xml
<include>
    <uri>model://turtlebot3_world</uri>
    <pose>0 0 0 0 0 0</pose>
</include>
```

My own local model is stored at:

```text
world/turtlebot3_world/
```

with:

```text
model.sdf
model-1_4.sdf
model.config
meshes/
    wall.dae
    hexagon.dae
```

---

# 23. My World Meshes

The model uses:

```text
wall.dae
hexagon.dae
```

The SDF defines these meshes as both:

```text
collision
```

and:

```text
visual
```

This means the same geometry is used for:

- what I see
- what Gazebo uses for collision

---

# 24. Difference Between My Two Model SDF Files

I have:

```text
model.sdf
model-1_4.sdf
```

`model.sdf` scales the meshes by:

```text
15.0 15.0 15.0
```

`model-1_4.sdf` scales them by:

```text
10.0 10.0 10.0
```

This means these are two different scaling versions of the same world model.

The active `model.sdf` uses the 15x scale.

---

# 25. `display.launch.py`

Location:

```text
robot_description/launch/display.launch.py
```

This launch file is responsible for:

```text
robot description
robot_state_publisher
joint state publisher options
RViz
```

It is included by:

```text
simulation.launch.py
```

---

# 26. Imports in `display.launch.py`

My file imports:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
```

The active code mainly uses:

```text
LaunchDescription
DeclareLaunchArgument
LaunchConfiguration
PathJoinSubstitution
IfCondition
Node
FindPackageShare
ParameterValue
Command
```

Some imports are currently unused:

```text
IncludeLaunchDescription
ExecuteProcess
UnlessCondition
PythonLaunchDescriptionSource
```

---

# 27. Creating `ld`

My code:

```python
ld = LaunchDescription()
```

Then I add actions using:

```python
ld.add_action(...)
```

This is the same structure I use in my other launch files.

---

# 28. My Robot Package Path

My code:

```python
robot_path = FindPackageShare('robot_description')
```

This stores the package location.

Conceptually:

```text
robot_path
    |
    v
robot_description package
```

I then reuse this variable when constructing the paths.

---

# 29. My URDF Model Path

My code:

```python
model_path = PathJoinSubstitution([
    'urdf',
    'assy.urdf'
])
```

This creates:

```text
urdf/assy.urdf
```

Then:

```python
urdf_path = PathJoinSubstitution([
    robot_path,
    model_path
])
```

combines the package path and model path.

The final result is effectively:

```text
<robot_description package>/urdf/assy.urdf
```

---

# 30. My RViz Configuration Path

My code:

```python
rviz_config = PathJoinSubstitution([
    robot_path,
    'rviz',
    'urdf.rviz'
])
```

Therefore my RViz configuration is:

```text
robot_description/
└── rviz/
    └── urdf.rviz
```

---

# 31. My Robot Description Generation

This is one of the most important parts of my code:

```python
robot_description_content = ParameterValue(
    Command(['xacro ', urdf_path]),
    value_type=str
)
```

My code does not simply read the URDF file as a plain parameter.

It executes:

```text
xacro
  |
  v
assy.urdf
  |
  v
robot description string
```

Even though my file is named `.urdf`, I am using Xacro processing because `assy.urdf` contains:

```xml
<xacro:include>
```

---

# 32. My Robot State Publisher

I create:

```python
robot_state_publisher_node = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[
        {
            'robot_description': robot_description_content,
            'use_sim_time': True,
        }
    ]
)
```

Therefore:

```text
assy.urdf
   |
   v
xacro Command
   |
   v
robot_description
   |
   v
robot_state_publisher
```

I explicitly set:

```text
use_sim_time = true
```

because my robot is being used with simulation time.

---

# 33. My `jsp_gui` Argument

I declare:

```python
DeclareLaunchArgument(
    name='jsp_gui',
    default_value='false',
    choices=['true', 'false'],
    description='Flag to enable joint_state_publisher_gui'
)
```

So I intended this argument to control whether the GUI version is used.

I can pass:

```bash
jsp_gui:=true
```

or:

```bash
jsp_gui:=false
```

---

# 34. My `jsp` Argument

I also declare:

```python
DeclareLaunchArgument(
    name='jsp',
    default_value='false',
    choices=['true', 'false'],
    description='Flag to enable joint_state_publisher'
)
```

However, in the current code, I never use:

```python
LaunchConfiguration('jsp')
```

for the normal `joint_state_publisher`.

Therefore:

```text
jsp argument
    |
    X
currently not connected to a Node condition
```

This is important to remember when modifying the file.

---

# 35. My `rviz_config` Argument

I declare:

```python
DeclareLaunchArgument(
    name='rviz_config',
    default_value=rviz_config,
    description='path rviz_config kek mano'
)
```

Therefore the default RViz file is:

```text
robot_description/rviz/urdf.rviz
```

But I can override it from the command line.

---

# 36. My Joint State Publisher Conditions

My code currently contains:

```python
Node(
    package='joint_state_publisher',
    executable='joint_state_publisher',
    condition=IfCondition(
        LaunchConfiguration('jsp_gui')
    )
)
```

and:

```python
Node(
    package='joint_state_publisher_gui',
    executable='joint_state_publisher_gui',
    condition=IfCondition(
        LaunchConfiguration('jsp_gui')
    )
)
```

Notice something important:

**Both nodes use `jsp_gui`.**

Therefore the current behavior is:

```text
jsp_gui=false
     |
     +--> joint_state_publisher        NOT STARTED
     |
     +--> joint_state_publisher_gui    NOT STARTED
```

When:

```text
jsp_gui=true
```

the current behavior becomes:

```text
jsp_gui=true
     |
     +--> joint_state_publisher        STARTED
     |
     +--> joint_state_publisher_gui    STARTED
```

So the code currently does **not** implement the comment:

> "either launch joint_state_publisher or joint_state_publisher_gui"

It actually makes both conditions depend on the same flag.

That is worth keeping in this README because this is what the code actually does.

---

# 37. My RViz Node

My code:

```python
Node(
    package='rviz2',
    executable='rviz2',
    output='screen',
    arguments=[
        '-d',
        LaunchConfiguration('rviz_config')
    ],
    parameters=[
        {
            'use_sim_time': True
        }
    ],
)
```

This starts RViz and gives it my selected configuration file.

The important relationship is:

```text
rviz_config argument
        |
        v
LaunchConfiguration('rviz_config')
        |
        v
RViz
        |
        v
urdf.rviz
```

---

# 38. My Robot Assembly: `assy.urdf`

This is the main robot description file.

Location:

```text
robot_description/urdf/assy.urdf
```

It includes:

```text
wheel_right.urdf
wheel_left.urdf
body.urdf
shaft.urdf
caster.urdf
```

Therefore:

```text
assy.urdf
   |
   +-- wheel_right
   +-- wheel_left
   +-- body
   +-- shaft
   +-- caster
```

---

# 39. My Xacro Includes

My code:

```xml
<xacro:include filename="$(find robot_description)/urdf/wheel_right.urdf" />
<xacro:include filename="$(find robot_description)/urdf/wheel_left.urdf" />
<xacro:include filename="$(find robot_description)/urdf/body.urdf" />
<xacro:include filename="$(find robot_description)/urdf/shaft.urdf" />
<xacro:include filename="$(find robot_description)/urdf/caster.urdf" />
```

Therefore `assy.urdf` acts as the assembly file.

It combines my separate robot parts into one robot.

---

# 40. My Robot Links

The resulting robot contains:

```text
base_link
left_wheel_link
right_wheel_link
shaft_link
caster_link
```

The main relationship is:

```text
base_link
├── left_wheel_link
├── right_wheel_link
└── shaft_link
      └── caster_link
```

---

# 41. My Right Wheel Joint

My code:

```xml
<joint name="base_to_right_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel_link"/>
    <origin xyz="-1.3 -1.1 0.0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
</joint>
```

This connects:

```text
base_link
    |
    v
right_wheel_link
```

The joint is:

```text
continuous
```

so the wheel can continuously rotate.

Its rotation axis is:

```text
0 1 0
```

---

# 42. My Left Wheel Joint

My code:

```xml
<joint name="base_to_left_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel_link"/>
    <origin xyz="-1.3 1.1 0.0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
</joint>
```

This connects:

```text
base_link
    |
    v
left_wheel_link
```

The left and right wheels therefore use the same rotation axis but are placed on opposite sides.

---

# 43. My Shaft

My code:

```xml
<joint name="base_to_shaft" type="fixed">
    <parent link="base_link"/>
    <child link="shaft_link"/>
    <origin xyz="1.3 0 -0.35" rpy="0 0 0"/>
</joint>
```

This means:

```text
base_link
    |
    v
shaft_link
```

The shaft cannot rotate relative to the base because I use:

```text
type="fixed"
```

---

# 44. My Caster

My code:

```xml
<joint name="shaft_to_caster" type="fixed">
    <parent link="shaft_link"/>
    <child link="caster_link"/>
    <origin xyz="-0.07 0 -0.15" rpy="0 0 0"/>
</joint>
```

Therefore:

```text
base_link
    |
    v
shaft_link
    |
    v
caster_link
```

Again, the connection is fixed.

---

# 45. My Base Body

`body.urdf` defines:

```xml
<link name="base_link">
```

The body is a box:

```text
size = 4 2 0.5
```

Therefore my robot base is:

```text
length = 4
width  = 2
height = 0.5
```

The mass is:

```text
5.0
```

I also provide inertia values.

The same box geometry is used for:

```text
visual
collision
```

---

# 46. My Wheels

Both wheels use:

```text
cylinder
radius = 0.75
length = 0.2
```

They are rotated using:

```text
rpy = 1.5708 0 0
```

Each wheel has:

```text
visual
inertial
collision
```

---

# 47. Wheel Friction

My wheel files contain:

```xml
<gazebo reference="left_wheel_link">
    <mu1>1.0</mu1>
    <mu2>1.0</mu2>
</gazebo>
```

and similarly for the right wheel.

Therefore I give both wheels:

```text
mu1 = 1.0
mu2 = 1.0
```

This affects their Gazebo contact friction.

---

# 48. My Shaft

`shaft.urdf` creates:

```xml
<link name="shaft_link">
```

with a cylinder:

```text
radius = 0.1
length = 0.25
```

Unlike the body and wheels, I do not define inertial or collision information for this shaft in the current file.

---

# 49. My Caster

The caster is:

```text
radius = 0.15
length = 0.1
mass = 0.5
```

It has:

```text
visual
collision
inertial
```

I also configure very low friction:

```xml
<mu1 value="0.001"/>
<mu2 value="0.001"/>
```

This makes the caster behave much more freely in Gazebo.

---

# 50. My `ros2_control` Configuration

Inside `assy.urdf`, I add:

```xml
<ros2_control name="GazeboSystem" type="system">
```

The hardware plugin is:

```xml
<plugin>gazebo_ros2_control/GazeboSystem</plugin>
```

So my simulated hardware interface is:

```text
Gazebo
   |
   v
gazebo_ros2_control
   |
   v
ros2_control
```

---

# 51. My Wheel Command Interfaces

For each wheel I define:

```xml
<command_interface name="velocity">
```

with:

```text
min = -10
max = 10
```

So my wheel velocity command interface allows:

```text
-10 <= velocity <= 10
```

I also define:

```xml
<state_interface name="position"/>
<state_interface name="velocity"/>
```

Therefore each wheel provides position and velocity states.

---

# 52. My Gazebo ROS 2 Control Plugin

My URDF contains:

```xml
<gazebo>
    <plugin
        filename="libgazebo_ros2_control.so"
        name="gazebo_ros2_control">
```

This connects my Gazebo robot to ROS 2 Control.

I give it:

```xml
<parameters>
    $(find robot_simulation)/config/diffdrive.yaml
</parameters>
```

Therefore the controller configuration comes from:

```text
robot_simulation/config/diffdrive.yaml
```

---

# 53. My Diff Drive Configuration

The important part is:

```yaml
diff_drive_base_controller:
  ros__parameters:
```

My controller uses:

```text
left wheel:
base_to_left_wheel

right wheel:
base_to_right_wheel
```

These names exactly match my URDF joint names.

This is important.

```text
URDF
base_to_left_wheel
       |
       v
diffdrive.yaml
left_wheel_names

URDF
base_to_right_wheel
       |
       v
diffdrive.yaml
right_wheel_names
```

---

# 54. My Wheel Dimensions in `diffdrive.yaml`

I configure:

```yaml
wheel_separation: 2.00
wheel_radius: 0.75
```

The radius matches the wheel geometry:

```text
wheel radius = 0.75
```

---

# 55. My Base Frame

My diff-drive controller uses:

```yaml
base_frame_id: base_link
```

This matches my URDF:

```xml
<link name="base_link">
```

Therefore:

```text
URDF base_link
       |
       v
diff-drive base_frame_id
```

---

# 56. My Velocity Limits

My linear velocity limits are:

```text
maximum = 2.0 m/s
minimum = -2.0 m/s
```

My linear acceleration limit is:

```text
0.5 m/s²
```

Angular velocity:

```text
maximum = 2.0 rad/s
minimum = -2.0 rad/s
```

Angular acceleration:

```text
0.5 rad/s²
```

---

# 57. `robot_control/launch/control.launch.py`

This launch file is responsible for all my manual control inputs.

The main components are:

```text
joy_node
teleop_twist_joy
teleop_twist_keyboard
twist_mux
```

---

# 58. My Control Configuration Paths

I create:

```python
controller_config = PathJoinSubstitution([
    FindPackageShare('robot_control'),
    'config',
    'teleop_twist.yaml'
])
```

This points to:

```text
robot_control/config/teleop_twist.yaml
```

I also create:

```python
joy_config
```

for:

```text
joy_config.yaml
```

and:

```python
keyboard_twist
```

for:

```text
keyboard_twist.yaml
```

and:

```python
twist_mux_path
```

for:

```text
twist_mux.yaml
```

So my launch file collects all the control configuration paths at the beginning.

---

# 59. My Joystick Driver

My code:

```python
Node(
    package='joy',
    executable='joy_node',
    name='joy_node',
    output='log',
    parameters=[
        joy_config,
        {'use_sim_time': True}
    ]
)
```

This starts:

```text
joy_node
```

The purpose is to read the physical joystick/controller.

The control flow starts as:

```text
Physical controller
       |
       v
joy_node
       |
       v
/joy
```

---

# 60. My Joystick Configuration

My `joy_config.yaml` sets:

```yaml
device_id: 0
device_name: ""
deadzone: 0.01
autorepeat_rate: 20.0
sticky_buttons: False
```

Important values:

```text
device ID = 0
deadzone = 0.01
autorepeat = 20 Hz
```

So my joystick has a very small deadzone of 1%.

---

# 61. My Joystick Teleop

My code:

```python
Node(
    package='teleop_twist_joy',
    executable='teleop_node',
    name='teleop_twist_joy_node',
    output='log',
    parameters=[
        controller_config,
        {'use_sim_time': True}
    ],
    remappings=[
        ('/cmd_vel', '/joy/cmd_vel')
    ]
)
```

This converts joystick input into velocity commands.

The important part is my remapping:

```text
teleop_twist_joy output
        |
        v
/joy/cmd_vel
```

Instead of publishing directly to:

```text
/cmd_vel
```

I send it to:

```text
/joy/cmd_vel
```

because I want `twist_mux` to combine it with keyboard control.

---

# 62. My Joystick Button Configuration

My `teleop_twist.yaml` says:

```yaml
enable_button: 4
enable_turbo_button: 5
```

According to my comments:

```text
button 4 = L1
button 5 = R1
```

Normal speed is:

```text
0.5
```

Turbo speed:

```text
1.0
```

Angular turbo scale:

```text
2.0
```

---

# 63. My Joystick Axis Configuration

My linear axis is:

```yaml
axis_linear:
  x: 1
  y: 0
  z: -1
```

My angular axis is:

```yaml
axis_angular:
  yaw: 3
  pitch: 2
  roll: -1
```

So my controller mapping is explicitly defined by these axis numbers.

---

# 64. My Keyboard Teleop

My keyboard control is different from the joystick.

I do not launch it immediately.

I use:

```python
TimerAction(
    period=5.0,
```

Therefore:

```text
control.launch.py starts
        |
        v
wait 5 seconds
        |
        v
keyboard teleop starts
```

This 5-second delay is an intentional part of my current code.

---

# 65. My Keyboard Process

My code uses:

```python
ExecuteProcess(
    cmd=[
        'bash',
        '-c',
        'exec ros2 run teleop_twist_keyboard teleop_twist_keyboard ...'
    ]
)
```

So unlike the joystick node, I launch keyboard teleop through:

```text
ExecuteProcess
    |
    v
bash
    |
    v
ros2 run teleop_twist_keyboard
```

---

# 66. My Keyboard Remapping

My command contains:

```text
--remap /cmd_vel:=/key/cmd_vel
```

Therefore:

```text
keyboard teleop
       |
       v
/key/cmd_vel
```

Again, I intentionally do not send keyboard commands directly to `/cmd_vel`.

---

# 67. My Keyboard Terminal

My command contains:

```text
< /dev/tty
```

and:

```python
emulate_tty=True
```

This is part of how I make the keyboard teleop interact with the terminal input/output when launched through the launch system.

---

# 68. My Keyboard Configuration

My `keyboard_twist.yaml` sets:

```yaml
speed: 0.5
turn: 1.0
speed_step: 0.1
turn_step: 0.1
stamped: false
```

So my keyboard teleoperation starts with:

```text
speed = 0.5 m/s
turn = 1.0 rad/s
```

and uses:

```text
speed step = 0.1
turn step = 0.1
```

---

# 69. My Twist Mux

My launch file starts:

```python
Node(
    package='twist_mux',
    executable='twist_mux',
    name='twist_mux_node',
    output='log',
    parameters=[
        twist_mux_path,
        {'use_sim_time': True},
    ],
    remappings=[
        ('/cmd_vel_out', '/cmd_vel')
    ]
)
```

This is the central point where my manual control inputs are combined.

---

# 70. My Twist Mux Inputs

My `twist_mux.yaml` defines:

```text
joystick
    /joy/cmd_vel
    priority 100

rqt
    /rqt/cmd_vel
    priority 100

keyboard
    /key/cmd_vel
    priority 90
```

So my mux accepts:

```text
/joy/cmd_vel
/rqt/cmd_vel
/key/cmd_vel
```

---

# 71. My Twist Mux Priorities

My current priorities are:

```text
joystick = 100
rqt      = 100
keyboard = 90
```

Therefore joystick and RQT have higher priority than keyboard.

The timeout is:

```text
0.5 seconds
```

for each configured input.

---

# 72. My Twist Mux Output

I remap:

```text
/cmd_vel_out
```

to:

```text
/cmd_vel
```

Therefore:

```text
                    /joy/cmd_vel
                         |
                         v
                    +---------+
/key/cmd_vel ------>|         |
                    |twist_mux|----> /cmd_vel
/rqt/cmd_vel ------>|         |
                    +---------+
```

This `/cmd_vel` is then used by my diff-drive controller.

---

# 73. Complete Control System

My complete actual control system is:

```text
                   JOYSTICK
                      |
                      v
                   joy_node
                      |
                      v
                     /joy
                      |
                      v
               teleop_twist_joy
                      |
                      v
                /joy/cmd_vel
                      |
                      |
                      +------------------+
                                         |
                                         v
KEYBOARD ---> teleop_twist_keyboard --> /key/cmd_vel
                                         |
                                         |
RQT --------------------------------> /rqt/cmd_vel
                                         |
                                         v
                                    twist_mux
                                         |
                                         v
                                      /cmd_vel
                                         |
                                         v
                             diff_drive_base_controller
                                         |
                                         v
                              base_to_left_wheel
                              base_to_right_wheel
```

This is the main diagram to remember.

---

# 74. My `diffdrive.yaml`

The controller manager section:

```yaml
controller_manager:
  ros__parameters:
    update_rate: 100
    use_sim_time: true
```

means my controller manager is configured for:

```text
update rate = 100 Hz
simulation time = true
```

---

# 75. My Joint State Broadcaster Configuration

I define:

```yaml
joint_state_broadcaster:
  type: joint_state_broadcaster/JointStateBroadcaster
```

This is the controller that publishes joint state information.

---

# 76. My Diff Drive Controller

I define:

```yaml
diff_drive_base_controller:
  type: diff_drive_controller/DiffDriveController
```

This is the controller responsible for translating:

```text
/cmd_vel
```

into wheel commands.

---

# 77. My `joints.yaml`

I also have:

```text
robot_simulation/config/joints.yaml
```

It contains:

```yaml
controller_manager:
  ros__parameters:
    update_rate: 100
    use_sim_time: true

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster
```

This is a simpler controller-manager configuration containing only the joint-state broadcaster.

Currently, my active `simulation.launch.py` does not directly load this YAML file.

My active Gazebo plugin uses:

```text
diffdrive.yaml
```

instead.

---

# 78. My `robot_description/CMakeLists.txt`

My package uses:

```cmake
find_package(ament_cmake REQUIRED)
```

Then installs:

```text
launch
urdf
config
rviz
scripts
```

using:

```cmake
install(DIRECTORY
  launch
  urdf
  config
  rviz
  scripts
  DESTINATION share/${PROJECT_NAME}
)
```

This is important because my launch files later use:

```python
FindPackageShare(...)
```

to find these installed files.

---

# 79. My Node-RED Script Installation

My `robot_description` package also installs:

```text
scripts/start_node_red.sh
```

using:

```cmake
install(
  PROGRAMS
    scripts/start_node_red.sh
  DESTINATION lib/${PROJECT_NAME}
)
```

So ROS 2 installs the script as an executable belonging to the package.

---

# 80. My `start_node_red.sh`

The script begins with:

```bash
#!/usr/bin/env bash
```

and:

```bash
set -euo pipefail
```

This makes the script stop on errors, unset variables, and failed pipeline commands.

---

# 81. My Node Version Manager Setup

The script sets:

```bash
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
```

So if `NVM_DIR` is not already defined, it uses:

```text
$HOME/.nvm
```

Then it checks:

```bash
if [[ ! -s "$NVM_DIR/nvm.sh" ]]; then
```

If NVM does not exist, the script stops.

---

# 82. My Node.js Version

The script loads NVM:

```bash
source "$NVM_DIR/nvm.sh"
```

and then selects:

```bash
nvm use 24
```

Therefore this script specifically expects Node.js 24 through NVM.

---

# 83. My Node-RED Configuration

I use:

```bash
USER_DIR="${NODE_RED_USER_DIR:-$HOME/.node-red}"
PORT="${NODE_RED_PORT:-1880}"
```

So my defaults are:

```text
Node-RED user directory:
$HOME/.node-red

Port:
1880
```

These can be overridden through environment variables.

---

# 84. Starting Node-RED

My script finally executes:

```bash
exec node-red \
    --userDir "$USER_DIR" \
    --port "$PORT" \
    "$@"
```

The `exec` means the Node-RED process replaces the shell script process.

---

# 85. My Package Installation Structure

My three packages use CMake.

The common structure is:

```text
find_package(ament_cmake REQUIRED)

install(DIRECTORY
    ...
    DESTINATION share/${PROJECT_NAME}
)

ament_package()
```

---

# 86. `robot_simulation/CMakeLists.txt`

My simulation package installs:

```text
launch
config
world
```

using:

```cmake
install(DIRECTORY
  launch
  config
  world
  DESTINATION share/${PROJECT_NAME}
)
```

Therefore ROS 2 can find:

```text
simulation.launch.py
diffdrive.yaml
joints.yaml
robot_world.world
turtlebot3_world/
```

after installation.

---

# 87. `robot_control/CMakeLists.txt`

My control package installs:

```text
launch
config
```

using:

```cmake
install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)
```

Therefore:

```text
control.launch.py
joy_config.yaml
teleop_twist.yaml
twist_mux.yaml
keyboard_twist.yaml
```

are available from the installed package.

---

# 88. My `package.xml` Situation

My package files currently contain the basic:

```xml
<buildtool_depend>ament_cmake</buildtool_depend>
```

and test dependencies.

They currently do not explicitly list all the runtime ROS packages used by the launch files.

For example, `robot_control` uses:

```text
joy
teleop_twist_joy
teleop_twist_keyboard
twist_mux
```

but these are not currently listed as `<exec_depend>` entries in its `package.xml`.

Likewise, `robot_simulation` uses packages such as:

```text
gazebo_ros
controller_manager
```

through the launch file.

This README records the current state rather than silently changing it.

---

# 89. Build My Workspace

From my workspace:

```bash
cd ~/ros2_ws
```

Build:

```bash
colcon build --symlink-install
```

Then:

```bash
source install/setup.bash
```

---

# 90. Run My Simulation

The main launch command is:

```bash
ros2 launch robot_simulation simulation.launch.py
```

This starts my complete system.

Conceptually:

```text
ros2 launch robot_simulation simulation.launch.py
                    |
                    v
          simulation.launch.py
                    |
          +---------+---------+
          |                   |
          v                   v
 display.launch.py      control.launch.py
          |                   |
          v                   v
 robot description       joystick
 robot state publisher   keyboard
 RViz                    twist_mux
          |                   |
          +---------+---------+
                    |
                    v
                  Gazebo
                    |
                    v
             robot simulation
```

---

# 91. Run My Display Only

My display launch can be run directly:

```bash
ros2 launch robot_description display.launch.py
```

This starts:

```text
robot_state_publisher
RViz
```

and the joint-state publisher nodes according to my current `jsp_gui` condition.

---

# 92. Run My Control Only

My control launch can be run directly:

```bash
ros2 launch robot_control control.launch.py
```

This starts:

```text
joy_node
teleop_twist_joy_node
keyboard teleop after 5 seconds
twist_mux_node
```

---

# 93. My Launch Arguments

For `simulation.launch.py`:

```text
gui
```

Default:

```text
true
```

Example:

```bash
ros2 launch robot_simulation simulation.launch.py gui:=false
```

For `display.launch.py`:

```text
jsp_gui
jsp
rviz_config
```

Example:

```bash
ros2 launch robot_description display.launch.py jsp_gui:=true
```

or:

```bash
ros2 launch robot_description display.launch.py rviz_config:=/path/to/file.rviz
```

---

# 94. My Full Startup Sequence

When I run:

```bash
ros2 launch robot_simulation simulation.launch.py
```

my intended system startup is:

```text
1. simulation.launch.py starts
        |
        v
2. display.launch.py is included
        |
        +--> robot_state_publisher
        +--> joint state publisher conditions
        +--> RViz
        |
        v
3. control.launch.py is included
        |
        +--> joy_node
        +--> teleop_twist_joy
        +--> keyboard teleop after 5 sec
        +--> twist_mux
        |
        v
4. controller spawners start
        |
        +--> joint_state_broadcaster
        +--> diff_drive_base_controller
        |
        v
5. Gazebo launch starts
        |
        v
6. robot_world.world loads
        |
        v
7. Gazebo ROS 2 control plugin provides controller manager
        |
        v
8. robot is spawned from /robot_description
        |
        v
9. /cmd_vel reaches diff_drive_base_controller
        |
        v
10. wheels are controlled
```

Because ROS 2 launch actions are started as part of one launch system, the exact timing between concurrently started actions is not simply the order in the Python file.

This is particularly important for the controller spawners and Gazebo.

---

# 95. Important Timing Detail in My Simulation

My code adds the controller spawners before the Gazebo launch action:

```text
joint_state_broadcaster spawner
diff_drive spawner
spawn_entity
Gazebo launch
```

However, adding them in this order does not mean Gazebo completely starts first and then the spawners automatically wait.

The spawners have:

```text
--controller-manager-timeout 30
```

which is important because the controller manager comes from the Gazebo `gazebo_ros2_control` system.

Therefore my 30-second timeout is relevant to allowing the controller manager time to become available.

---

# 96. My Complete Robot Architecture

```text
                         simulation.launch.py
                                  |
             +--------------------+--------------------+
             |                    |                    |
             v                    v                    v
      display.launch.py    control.launch.py      Gazebo launch
             |                    |                    |
             |                    |                    v
             |                    |              robot_world.world
             |                    |
             |                    +-----------------------------+
             |                                                  |
             v                                                  v
     robot_state_publisher                              Gazebo control
             |                                                  |
             v                                                  v
             TF                                      controller_manager
             |                                                  |
             v                                                  |
            RViz                                      +---------+---------+
                                                       |                   |
                                                       v                   v
                                                joint_state_broadcaster   diff_drive
                                                                           controller
                                                                                |
                                                                                v
                                                                            wheels
```

---

# 97. Complete Control Architecture

```text
                         Controller
                             |
                             v
                          /joy
                             |
                             v
                     teleop_twist_joy
                             |
                             v
                       /joy/cmd_vel
                             |
                             |
                             +----------------------+
                                                    |
Keyboard                                            |
    |                                               |
    v                                               |
teleop_twist_keyboard                               |
    |                                               |
    v                                               |
/key/cmd_vel                                        |
    |                                               |
    +--------------------+--------------------------+
                         |
                         v
                     twist_mux
                         |
                         v
                      /cmd_vel
                         |
                         v
             diff_drive_base_controller
                         |
               +---------+---------+
               |                   |
               v                   v
      base_to_left_wheel   base_to_right_wheel
               |                   |
               v                   v
          left wheel          right wheel
```

---

# 98. Complete Robot Description Architecture

```text
                         assy.urdf
                             |
        +--------------------+--------------------+
        |         |          |          |         |
        v         v          v          v         v
      body     left wheel  right wheel shaft    caster
        |         |          |          |         |
        +---------+----------+----------+---------+
                             |
                             v
                       Robot Model
                             |
                 +-----------+-----------+
                 |                       |
                 v                       v
        robot_state_publisher         Gazebo
                 |                       |
                 v                       v
                 TF               gazebo_ros2_control
                 |                       |
                 v                       v
                RViz              Controllers
```

---

# 99. Files That Are Actually Connected

## Robot description

```text
display.launch.py
       |
       v
assy.urdf
       |
       +-- body.urdf
       +-- wheel_left.urdf
       +-- wheel_right.urdf
       +-- shaft.urdf
       +-- caster.urdf
```

## Simulation

```text
simulation.launch.py
       |
       +-- display.launch.py
       |
       +-- control.launch.py
       |
       +-- robot_world.world
       |
       +-- diffdrive.yaml
```

## Control

```text
control.launch.py
       |
       +-- joy_config.yaml
       +-- teleop_twist.yaml
       +-- keyboard_twist.yaml
       +-- twist_mux.yaml
```

---

# 100. My Most Important Things to Remember

## If I want to change the robot shape

Go to:

```text
robot_description/urdf/
```

especially:

```text
assy.urdf
body.urdf
wheel_left.urdf
wheel_right.urdf
shaft.urdf
caster.urdf
```

---

## If I want to change RViz

Go to:

```text
robot_description/rviz/urdf.rviz
```

---

## If I want to change joystick mapping

Go to:

```text
robot_control/config/teleop_twist.yaml
```

---

## If I want to change joystick device settings

Go to:

```text
robot_control/config/joy_config.yaml
```

---

## If I want to change keyboard speed

Go to:

```text
robot_control/config/keyboard_twist.yaml
```

---

## If I want to change which command has priority

Go to:

```text
robot_control/config/twist_mux.yaml
```

---

## If I want to change wheel/controller settings

Go to:

```text
robot_simulation/config/diffdrive.yaml
```

---

## If I want to change the Gazebo world

Go to:

```text
robot_simulation/world/robot_world.world
```

and:

```text
robot_simulation/world/turtlebot3_world/
```

---

## If I want to change the main startup sequence

Go to:

```text
robot_simulation/launch/simulation.launch.py
```

---

## If I want to change joystick/keyboard startup

Go to:

```text
robot_control/launch/control.launch.py
```

---

## If I want to change robot visualization startup

Go to:

```text
robot_description/launch/display.launch.py
```

---

# 101. My Three Launch Files in One Sentence

```text
display.launch.py
    = robot model + robot state publisher + RViz

control.launch.py
    = joystick + keyboard + twist mux

simulation.launch.py
    = display + control + Gazebo + controllers + robot spawning
```

This is probably the most useful short summary of my project.

---

# 102. My Main Command

The command I should remember is:

```bash
ros2 launch robot_simulation simulation.launch.py
```

Because this launch file pulls the other parts of my system together.

---

# 103. Debugging My System

If the robot does not move:

```bash
ros2 topic list
```

Check:

```text
/joy
/joy/cmd_vel
/key/cmd_vel
/cmd_vel
```

Then:

```bash
ros2 topic echo /cmd_vel
```

If `/cmd_vel` changes when I use the controller, my control chain is working up to the mux output.

Then check:

```bash
ros2 node list
```

I should see the relevant nodes.

---

# 104. Debugging My Controller

Check:

```bash
ros2 control list_controllers
```

I should expect my controllers to include:

```text
joint_state_broadcaster
diff_drive_base_controller
```

If the diff-drive controller is not active, `/cmd_vel` may exist but the robot will not move.

---

# 105. Debugging My Topics

My important command topics are:

```text
/joy/cmd_vel
/key/cmd_vel
/rqt/cmd_vel
/cmd_vel
```

The flow is:

```text
/joy/cmd_vel
       |
       v
   twist_mux
       |
       v
   /cmd_vel

/key/cmd_vel
       |
       v
   twist_mux
```

---

# 106. Debugging My Robot Description

Check:

```bash
ros2 topic echo /robot_description
```

The robot description should be available after my `robot_state_publisher` starts.

If the robot does not appear correctly in RViz, first check:

```text
assy.urdf
robot_state_publisher
TF
RViz Fixed Frame
```

---

# 107. Important Current Code Notes

These are not changes. They are observations of my current implementation.

## `jsp` is currently unused

I declare:

```python
jsp
```

but don't use it to control a node.

---

## `jsp_gui` controls both joint-state publishers

Both currently use:

```python
IfCondition(LaunchConfiguration('jsp_gui'))
```

Therefore both start when `jsp_gui=true`.

---

## `world_path` is currently unused

I calculate:

```python
world_path
```

but the environment-variable action that uses it is commented out.

---

## Several imports are unused

Some imported launch classes and substitutions are currently not used.

---

## `joints.yaml` is not directly loaded by my active launch sequence

My Gazebo control configuration uses:

```text
diffdrive.yaml
```

through the Gazebo ROS 2 control plugin.

---

## Runtime dependencies are not fully declared

My current `package.xml` files are minimal.

The code itself depends on more ROS packages than are explicitly declared there.

This is something to remember if I move the workspace to another computer.

---

# 108. The One Diagram I Should Remember

```text
                    ros2 launch
                         |
                         v
              simulation.launch.py
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       DISPLAY         CONTROL        GAZEBO
          |              |              |
          |              |              |
          v              v              v
     robot_state       joystick      world
     publisher         keyboard      robot spawn
          |              |              |
          v              v              v
         TF          twist_mux      ros2_control
          |              |              |
          v              v              v
        RViz          /cmd_vel      controllers
                         |              |
                         +------+-------+
                                |
                                v
                              wheels
```

---

# 109. Final Personal Reference

My project is divided like this:

```text
robot_description
    |
    | "What is my robot?"
    |
    +-- URDF
    +-- robot_state_publisher
    +-- RViz
    +-- Node-RED script


robot_control
    |
    | "How do I control my robot?"
    |
    +-- Joystick
    +-- Keyboard
    +-- RQT input
    +-- twist_mux


robot_simulation
    |
    | "Where does my robot run?"
    |
    +-- Gazebo
    +-- World
    +-- Robot spawning
    +-- ros2_control
    +-- Diff-drive controller
```

And the three connect together like this:

```text
                    robot_description
                           |
                           v
                       Robot Model
                           |
              +------------+-------------+
              |                          |
              v                          v
             RViz                      Gazebo
                                         |
                                         v
                              ros2_control system
                                         |
                                         v
                              diff_drive_controller
                                         ^
                                         |
                                      /cmd_vel
                                         ^
                                         |
                                    twist_mux
                                    ^       ^
                                   /         \
                          /joy/cmd_vel     /key/cmd_vel
                               ^               ^
                               |               |
                         joystick          keyboard
```

That is the architecture of **my actual current code**.

---

# 110. Quick File Reference

| File | What I use it for |
|---|---|
| `robot_description/launch/display.launch.py` | Robot description, robot state publisher and RViz |
| `robot_description/urdf/assy.urdf` | Main robot assembly |
| `robot_description/urdf/body.urdf` | Main robot body |
| `robot_description/urdf/wheel_left.urdf` | Left wheel |
| `robot_description/urdf/wheel_right.urdf` | Right wheel |
| `robot_description/urdf/shaft.urdf` | Shaft |
| `robot_description/urdf/caster.urdf` | Caster |
| `robot_description/rviz/urdf.rviz` | RViz configuration |
| `robot_description/scripts/start_node_red.sh` | Start Node-RED with Node.js 24 |
| `robot_simulation/launch/simulation.launch.py` | Main simulation startup |
| `robot_simulation/world/robot_world.world` | Gazebo world |
| `robot_simulation/config/diffdrive.yaml` | ros2_control and diff-drive configuration |
| `robot_simulation/config/joints.yaml` | Joint state broadcaster configuration |
| `robot_control/launch/control.launch.py` | Joystick, keyboard and mux startup |
| `robot_control/config/joy_config.yaml` | Joystick device configuration |
| `robot_control/config/teleop_twist.yaml` | Joystick-to-velocity mapping |
| `robot_control/config/keyboard_twist.yaml` | Keyboard teleop configuration |
| `robot_control/config/twist_mux.yaml` | Velocity input priorities and muxing |

---

# 111. Final Mental Model

When I come back to this project later, I only need to remember:

```text
simulation.launch.py
        |
        +--> display.launch.py
        |       |
        |       +--> assy.urdf
        |       +--> robot_state_publisher
        |       +--> RViz
        |
        +--> control.launch.py
        |       |
        |       +--> joystick
        |       +--> joystick teleop
        |       +--> keyboard teleop
        |       +--> twist_mux
        |
        +--> Gazebo
        |       |
        |       +--> robot_world.world
        |       +--> robot spawn
        |       +--> ros2_control
        |
        +--> controllers
                |
                +--> joint_state_broadcaster
                +--> diff_drive_base_controller

Control:

/joy/cmd_vel
       \
        \
         --> twist_mux --> /cmd_vel --> diff_drive_controller
        /
/key/cmd_vel
```

This is how **my code is connected**.

The most important launch file is:

```text
robot_simulation/launch/simulation.launch.py
```

because it brings together my:

```text
robot_description
robot_control
Gazebo
controllers
```

into one system.
