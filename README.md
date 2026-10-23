# My Own ROS 2 Launch Files

A personal ROS 2 launch-file reference and collection for learning, experimenting with, and building robot systems using ROS 2.

This repository contains custom ROS 2 launch files and examples for launching robot nodes, URDF models, RViz, simulation components, parameters, remappings, and other ROS 2 processes.

The main purpose of this repository is not only to run the robot, but also to serve as a **personal reference for understanding how ROS 2 launch files work**.

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [ROS 2 Environment](#2-ros-2-environment)
3. [Repository Structure](#3-repository-structure)
4. [Understanding a ROS 2 Workspace](#4-understanding-a-ros-2-workspace)
5. [What Happens When `ros2 launch` Is Used](#5-what-happens-when-ros2-launch-is-used)
6. [Basic Launch File Structure](#6-basic-launch-file-structure)
7. [The `generate_launch_description()` Function](#7-the-generate_launch_description-function)
8. [Launching a ROS 2 Node](#8-launching-a-ros-2-node)
9. [Understanding the `Node()` Action](#9-understanding-the-node-action)
10. [Calling Another Launch File](#10-calling-another-launch-file)
11. [Understanding `IncludeLaunchDescription`](#11-understanding-includelaunchdescription)
12. [Passing Arguments to Another Launch File](#12-passing-arguments-to-another-launch-file)
13. [Launch Arguments](#13-launch-arguments)
14. [LaunchConfiguration](#14-launchconfiguration)
15. [PathJoinSubstitution](#15-pathjoinsubstitution)
16. [FindPackageShare](#16-findpackageshare)
17. [Parameters](#17-parameters)
18. [ParameterValue](#18-parametervalue)
19. [Conditions](#19-conditions)
20. [IfCondition](#20-ifcondition)
21. [UnlessCondition](#21-unlesscondition)
22. [TimerAction](#22-timeraction)
23. [ExecuteProcess](#23-executeprocess)
24. [ROS 2 URDF Launch Architecture](#24-ros-2-urdf-launch-architecture)
25. [Robot State Publisher](#25-robot-state-publisher)
26. [Joint State Publisher](#26-joint-state-publisher)
27. [RViz](#27-rviz)
28. [Keyboard Teleoperation](#28-keyboard-teleoperation)
29. [Launch File Hierarchy](#29-launch-file-hierarchy)
30. [Python Launch File Template](#30-python-launch-file-template)
31. [Including Another Launch File Template](#31-including-another-launch-file-template)
32. [Launching Multiple Nodes](#32-launching-multiple-nodes)
33. [Build System](#33-build-system)
34. [CMakeLists.txt](#34-cmakelists.txt)
35. [package.xml](#35-package.xml)
36. [Installing Launch Files](#36-installing-launch-files)
37. [Using `--symlink-install`](#37-using---symlink-install)
38. [Building the Workspace](#38-building-the-workspace)
39. [Sourcing the Workspace](#39-sourcing-the-workspace)
40. [Running Launch Files](#40-running-launch-files)
41. [Launch Arguments From Terminal](#41-launch-arguments-from-terminal)
42. [Checking Available Launch Arguments](#42-checking-available-launch-arguments)
43. [ROS 2 Debugging Commands](#43-ros-2-debugging-commands)
44. [Node Debugging](#44-node-debugging)
45. [Topic Debugging](#45-topic-debugging)
46. [Parameter Debugging](#46-parameter-debugging)
47. [TF Debugging](#47-tf-debugging)
48. [RQT Graph](#48-rqt-graph)
49. [Common Problems](#49-common-problems)
50. [How to Add a New Launch File](#50-how-to-add-a-new-launch-file)
51. [How to Add a New Node](#51-how-to-add-a-new-node)
52. [How to Make One Launch File Start Another](#52-how-to-make-one-launch-file-start-another)
53. [How to Pass Values Between Launch Files](#53-how-to-pass-values-between-launch-files)
54. [How to Conditionally Start a Node](#54-how-to-conditionally-start-a-node)
55. [How to Delay a Node](#55-how-to-delay-a-node)
56. [How to Run a Normal Linux Command](#56-how-to-run-a-normal-linux-command)
57. [ROS 2 Launch Cheat Sheet](#57-ros-2-launch-cheat-sheet)
58. [Recommended Workflow](#58-recommended-workflow)
59. [Future Expansion](#59-future-expansion)

---

# 1. Project Overview

Repository:

`my-own-ros2-launch-file`

GitHub:

https://github.com/imranlim/my-own-ros2-launch-file

The repository is intended as a personal collection of ROS 2 launch-file examples and working configurations.

The repository focuses on understanding how different ROS 2 components can be started together using a launch system.

Examples include:

- robot description
- URDF
- RViz
- robot state publisher
- joint state publisher
- keyboard teleoperation
- ROS 2 nodes
- parameters
- launch arguments
- topic remapping
- conditions
- delayed startup
- including other launch files
- starting external processes

---

# 2. ROS 2 Environment

The original repository is intended for:

- Ubuntu 22.04 LTS
- ROS 2 Humble Hawksbill
- Python launch files
- `colcon`

The workspace is normally structured like this:

```text
~/ros2_ws/
├── src/
│   └── my-own-ros2-launch-file/
│
├── build/
├── install/
└── log/
```

---

# 3. Repository Structure

The repository currently contains the following main items:

```text
my-own-ros2-launch-file/
│
├── build/
├── install/
├── log/
├── src/
│
├── .gitignore
└── README.md
```

## `src/`

This is where ROS 2 packages are normally placed.

The actual ROS 2 source packages should be inside this directory.

For example:

```text
src/
├── package_1/
├── package_2/
└── package_3/
```

The `src` directory is the important part when developing the project.

---

# 4. Understanding a ROS 2 Workspace

A ROS 2 workspace normally has four important areas.

```text
ros2_ws/
│
├── src/
├── build/
├── install/
└── log/
```

## `src`

Contains the source code.

This is where you edit:

- Python files
- C++ files
- launch files
- URDF
- configuration files
- package files

---

## `build`

Generated by `colcon`.

It contains intermediate build information.

Normally, you do not edit files here manually.

---

## `install`

Contains the installed version of the packages.

When you run:

```bash
source ~/ros2_ws/install/setup.bash
```

ROS 2 learns about the packages installed into the workspace.

---

## `log`

Contains build and runtime logs.

Useful when debugging.

---

# 5. What Happens When `ros2 launch` Is Used

For example:

```bash
ros2 launch my_package robot.launch.py
```

The basic flow is:

```text
Terminal
   │
   │ ros2 launch
   ▼
ROS 2 Launch System
   │
   ▼
Find Package
   │
   ▼
Find Launch File
   │
   ▼
Read generate_launch_description()
   │
   ▼
Create Launch Actions
   │
   ├── Node
   ├── IncludeLaunchDescription
   ├── ExecuteProcess
   ├── TimerAction
   ├── DeclareLaunchArgument
   └── Conditions
   │
   ▼
Start Processes
   │
   ├── robot_state_publisher
   ├── joint_state_publisher
   ├── RViz
   ├── teleop
   └── other nodes
```

This is one of the most important concepts in ROS 2.

A launch file does not normally contain the actual implementation of the node.

Instead, the launch file tells ROS 2:

> "Start this executable, from this package, with these parameters."

---

# 6. Basic Launch File Structure

A Python launch file normally looks like:

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    my_node = Node(
        package='my_package',
        executable='my_node',
        output='screen'
    )

    return LaunchDescription([
        my_node
    ])
```

There are three important parts.

## 1. Import

```python
from launch import LaunchDescription
```

Imports the ROS 2 launch description system.

---

## 2. Create actions

```python
my_node = Node(...)
```

Creates an action that tells ROS 2 to start a node.

---

## 3. Return the launch description

```python
return LaunchDescription([
    my_node
])
```

This tells ROS 2 what actions should be executed.

---

# 7. The `generate_launch_description()` Function

Every Python launch file normally contains:

```python
def generate_launch_description():
```

ROS 2 calls this function when the launch file starts.

Inside this function you define:

- nodes
- arguments
- parameters
- included launch files
- timers
- processes
- conditions

At the end:

```python
return LaunchDescription([
    ...
])
```

The returned `LaunchDescription` contains all the actions ROS 2 should execute.

---

# 8. Launching a ROS 2 Node

The most important launch action is:

```python
Node()
```

Example:

```python
Node(
    package='turtlesim',
    executable='turtlesim_node',
    output='screen'
)
```

This means:

```text
Package:
turtlesim

Executable:
turtlesim_node

Output:
terminal
```

Equivalent manual command:

```bash
ros2 run turtlesim turtlesim_node
```

The launch file simply automates this.

---

# 9. Understanding the `Node()` Action

A typical node:

```python
Node(
    package='my_package',
    executable='my_node',
    name='my_node_name',
    namespace='robot1',
    output='screen',
    parameters=[...],
    remappings=[...]
)
```

## `package`

```python
package='my_package'
```

Specifies which ROS 2 package contains the executable.

---

## `executable`

```python
executable='my_node'
```

Specifies the executable that should be launched.

---

## `name`

```python
name='my_node_name'
```

Changes the runtime node name.

---

## `namespace`

```python
namespace='robot1'
```

Places the node inside a namespace.

For example:

```text
/robot1/my_node
```

---

## `output`

```python
output='screen'
```

Displays the node's output in the terminal.

This is extremely useful when debugging.

---

## `parameters`

```python
parameters=[
    {
        'use_sim_time': True
    }
]
```

Passes parameters to the node.

---

## `remappings`

Example:

```python
remappings=[
    ('cmd_vel', 'robot1/cmd_vel')
]
```

Changes topic names.

---

# 10. Calling Another Launch File

One of the most important things in this repository is understanding how one launch file can start another launch file.

For example:

```text
main.launch.py
       │
       ├── robot.launch.py
       │
       ├── rviz.launch.py
       │
       └── teleop.launch.py
```

Instead of putting everything into one huge launch file, you can separate functionality.

Example:

```python
IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        ...
    )
)
```

This means:

> Include and execute another launch file.

---

# 11. Understanding `IncludeLaunchDescription`

Import:

```python
from launch.actions import IncludeLaunchDescription
```

This action allows one launch file to include another launch file.

Example:

```python
included_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        ...
    ])
)
```

Conceptually:

```text
main.launch.py
       │
       │ IncludeLaunchDescription
       ▼
other.launch.py
       │
       ├── Node A
       ├── Node B
       └── Node C
```

The main launch file does not need to duplicate all the code from the other launch file.

This is useful for modular ROS 2 systems.

---

# 12. Passing Arguments to Another Launch File

You can pass launch arguments into the included launch file.

Example:

```python
IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        launch_file
    ]),
    launch_arguments={
        'use_sim_time': 'true'
    }.items()
)
```

The parent launch file passes:

```text
use_sim_time = true
```

to the child launch file.

The child launch file can then retrieve it using:

```python
LaunchConfiguration('use_sim_time')
```

---

# 13. Launch Arguments

Launch arguments allow values to be changed from the terminal without modifying the Python file.

Example:

```python
DeclareLaunchArgument(
    'use_sim_time',
    default_value='false',
    description='Use simulation time'
)
```

Then:

```bash
ros2 launch my_package robot.launch.py use_sim_time:=true
```

This is much better than hardcoding everything.

---

# 14. LaunchConfiguration

Import:

```python
from launch.substitutions import LaunchConfiguration
```

Example:

```python
use_sim_time = LaunchConfiguration('use_sim_time')
```

This means:

> Get the current value of the launch argument called `use_sim_time`.

Then:

```python
parameters=[
    {
        'use_sim_time': use_sim_time
    }
]
```

passes that value into a node.

---

# 15. PathJoinSubstitution

`PathJoinSubstitution` is useful for constructing file paths.

Example:

```python
PathJoinSubstitution([
    FindPackageShare('my_package'),
    'launch',
    'robot.launch.py'
])
```

Conceptually:

```text
package share directory
        +
launch
        +
robot.launch.py
```

becomes:

```text
/path/to/package/share/my_package/launch/robot.launch.py
```

This is useful because you do not need to hardcode the absolute path.

---

# 16. FindPackageShare

Import:

```python
from launch_ros.substitutions import FindPackageShare
```

Example:

```python
FindPackageShare('my_package')
```

This asks ROS 2:

> Where is the installed share directory of this package?

This is especially useful when locating:

- URDF
- RViz configurations
- launch files
- YAML files
- meshes
- other resources

---

# 17. Parameters

ROS 2 nodes can receive parameters.

Example:

```python
Node(
    package='my_package',
    executable='my_node',
    parameters=[
        {
            'use_sim_time': False
        }
    ]
)
```

The node receives:

```text
use_sim_time = false
```

Parameters are different from topics.

A topic continuously communicates data.

A parameter stores configuration for a node.

---

# 18. ParameterValue

`ParameterValue` can be useful when a substitution needs to be explicitly interpreted as a certain type.

For example:

```python
ParameterValue(
    some_value,
    value_type=str
)
```

This can prevent type interpretation problems.

This becomes particularly useful when launch substitutions are involved.

---

# 19. Conditions

ROS 2 launch files can conditionally start actions.

For example:

```text
if true
    start RViz

if false
    do not start RViz
```

Conditions are useful for making one launch file configurable.

---

# 20. IfCondition

Import:

```python
from launch.conditions import IfCondition
```

Example:

```python
Node(
    package='rviz2',
    executable='rviz2',
    condition=IfCondition(use_rviz)
)
```

If:

```text
use_rviz = true
```

RViz starts.

If:

```text
use_rviz = false
```

RViz does not start.

---

# 21. UnlessCondition

`UnlessCondition` is basically the opposite.

Example:

```python
condition=UnlessCondition(use_sim)
```

The action runs when the condition is false.

Conceptually:

```text
IfCondition:
    run when TRUE

UnlessCondition:
    run when FALSE
```

---

# 22. TimerAction

Import:

```python
from launch.actions import TimerAction
```

Example:

```python
TimerAction(
    period=3.0,
    actions=[
        my_node
    ]
)
```

This means:

```text
Start launch
    │
    │ wait 3 seconds
    ▼
Start my_node
```

This can be useful when one process needs time to initialize before another starts.

---

# 23. ExecuteProcess

`ExecuteProcess` allows a launch file to start a normal external process.

Example:

```python
ExecuteProcess(
    cmd=['some_command'],
    output='screen'
)
```

This is different from `Node()`.

### `Node()`

Used for ROS 2 nodes.

```python
Node(
    package='my_package',
    executable='my_node'
)
```

### `ExecuteProcess()`

Used for external commands/processes.

```python
ExecuteProcess(
    cmd=['python3', 'some_script.py']
)
```

A useful way to remember it:

```text
ROS executable
    ↓
Node()

Normal command/program
    ↓
ExecuteProcess()
```

---

# 24. ROS 2 URDF Launch Architecture

A common robot visualization setup is:

```text
                Launch File
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
       URDF      Joint State   RViz
                    Publisher
          │          │
          ▼          ▼
              Robot State
               Publisher
                    │
                    ▼
                    TF
                    │
                    ▼
                   RViz
```

The purpose of the launch file is to start all the components together.

---

# 25. Robot State Publisher

`robot_state_publisher` reads the robot description and publishes TF transforms for the robot's links.

Conceptually:

```text
URDF
 │
 ▼
robot_state_publisher
 │
 ▼
TF
 │
 ├── base_link
 ├── link1
 ├── link2
 └── ...
```

RViz uses these transforms to know where each robot link should be displayed.

---

# 26. Joint State Publisher

`joint_state_publisher` provides joint states for joints that are not being controlled by actual hardware.

This is particularly useful when visualizing a URDF in RViz.

Conceptually:

```text
Joint State Publisher
          │
          ▼
     Joint States
          │
          ▼
Robot State Publisher
          │
          ▼
          TF
```

If real hardware is used, joint states may instead come from:

```text
encoder
   ↓
hardware driver
   ↓
/joint_states
```

---

# 27. RViz

RViz is the visualization tool.

Typical flow:

```text
URDF
 │
 ▼
Robot State Publisher
 │
 ▼
TF
 │
 ▼
RViz
```

RViz does not normally calculate the robot's physical movement itself.

It displays information published by ROS 2.

---

# 28. Keyboard Teleoperation

Keyboard teleoperation is normally another ROS 2 node/process.

For example:

```text
Keyboard
   │
   ▼
Teleop Node
   │
   ▼
/cmd_vel
   │
   ▼
Robot Controller
   │
   ▼
Motors
```

If using a launch file, the teleoperation node can be started together with the rest of the robot system.

For example:

```python
Node(
    package='teleop_twist_keyboard',
    executable='teleop_twist_keyboard',
    output='screen'
)
```

The exact executable depends on the installed package.

---

# 29. Launch File Hierarchy

A large ROS 2 system should ideally be divided into smaller launch files.

For example:

```text
main.launch.py
│
├── robot_description.launch.py
│
├── sensors.launch.py
│
├── controller.launch.py
│
├── teleop.launch.py
│
└── rviz.launch.py
```

Then:

```text
main.launch.py
      │
      ├── Include robot_description.launch.py
      ├── Include sensors.launch.py
      ├── Include controller.launch.py
      ├── Include teleop.launch.py
      └── Include rviz.launch.py
```

This is much easier to maintain than putting everything inside one file.

---

# 30. Python Launch File Template

Basic template:

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    node = Node(
        package='my_package',
        executable='my_node',
        output='screen'
    )

    return LaunchDescription([
        node
    ])
```

---

# 31. Including Another Launch File Template

Basic pattern:

```python
import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    other_launch_file = os.path.join(
        get_package_share_directory('other_package'),
        'launch',
        'other.launch.py'
    )

    included_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            other_launch_file
        )
    )

    return LaunchDescription([
        included_launch
    ])
```

The important idea is:

```text
Find package
    ↓
Find launch directory
    ↓
Find launch file
    ↓
Include launch file
```

---

# 32. Launching Multiple Nodes

A launch file can start multiple nodes.

Example:

```python
node1 = Node(
    package='package_a',
    executable='node_a',
    output='screen'
)

node2 = Node(
    package='package_b',
    executable='node_b',
    output='screen'
)

node3 = Node(
    package='package_c',
    executable='node_c',
    output='screen'
)

return LaunchDescription([
    node1,
    node2,
    node3
])
```

Conceptually:

```text
                 launch
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      Node 1     Node 2     Node 3
```

---

# 33. Build System

The normal workflow is:

```bash
cd ~/ros2_ws
colcon build
```

For this repository, the recommended development command is:

```bash
colcon build --symlink-install
```

---

# 34. CMakeLists.txt

For a C++ package, `CMakeLists.txt` controls how the package is built and installed.

A launch directory should be installed so ROS 2 can find the launch files after building.

Example:

```cmake
install(
  DIRECTORY
    launch
    config
  DESTINATION share/${PROJECT_NAME}/
)
```

This means:

```text
launch/
config/
   ↓
install/
   ↓
share/<package_name>/
```

Without installing the files correctly, ROS 2 may not be able to find them.

---

# 35. package.xml

`package.xml` describes the ROS 2 package and its dependencies.

For launch functionality, dependencies can include:

```xml
<exec_depend>ros2launch</exec_depend>
```

Other dependencies depend on what the package actually uses.

For example:

```text
launch
launch_ros
robot_state_publisher
joint_state_publisher
rviz2
xacro
```

Only add dependencies that are actually required.

---

# 36. Installing Launch Files

Launch files must be installed into the package's share directory.

For CMake packages:

```cmake
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
```

For Python packages, launch files are normally included through `data_files`.

Example:

```python
data_files=[
    (
        'share/ament_index/resource_index/packages',
        ['resource/' + package_name]
    ),

    (
        'share/' + package_name,
        ['package.xml']
    ),

    (
        os.path.join('share', package_name, 'launch'),
        glob(os.path.join('launch', '*launch.[pxy][yma]*'))
    ),
]
```

---

# 37. Using `--symlink-install`

Use:

```bash
colcon build --symlink-install
```

This is particularly convenient during development.

Instead of copying certain files into the install directory, symlinks can be used.

This means changes to files such as Python launch files can be reflected more conveniently without rebuilding everything every time.

However, if you change package installation rules, CMake configuration, dependencies, or compiled code, rebuilding is still necessary.

---

# 38. Building the Workspace

From the workspace:

```bash
cd ~/ros2_ws
```

Build:

```bash
colcon build --symlink-install
```

Build a specific package:

```bash
colcon build --symlink-install --packages-select my_package
```

Build multiple packages:

```bash
colcon build --symlink-install --packages-select package_a package_b
```

---

# 39. Sourcing the Workspace

After building:

```bash
source ~/ros2_ws/install/setup.bash
```

This allows the current terminal to find your packages.

You can also source ROS 2 first:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

Typical order:

```text
ROS 2 Humble
     ↓
Your workspace
     ↓
Your packages
     ↓
Your launch files
```

---

# 40. Running Launch Files

General syntax:

```bash
ros2 launch <package_name> <launch_file>
```

Example:

```bash
ros2 launch my_package robot.launch.py
```

ROS 2 searches the installed package for the requested launch file.

---

# 41. Launch Arguments From Terminal

Example:

```bash
ros2 launch my_package robot.launch.py use_sim_time:=true
```

Multiple arguments:

```bash
ros2 launch my_package robot.launch.py \
    use_sim_time:=true \
    use_rviz:=false
```

This is one of the biggest advantages of launch files.

You can change configuration without editing Python code.

---

# 42. Checking Available Launch Arguments

Use:

```bash
ros2 launch my_package robot.launch.py --show-args
```

This displays the arguments declared by the launch file.

Very useful when you forget what options are available.

---

# 43. ROS 2 Debugging Commands

## List nodes

```bash
ros2 node list
```

---

## List topics

```bash
ros2 topic list
```

---

## List services

```bash
ros2 service list
```

---

## List actions

```bash
ros2 action list
```

---

## List parameters

```bash
ros2 param list
```

---

## Show package

```bash
ros2 pkg list
```

---

## Find package

```bash
ros2 pkg prefix <package_name>
```

---

# 44. Node Debugging

List nodes:

```bash
ros2 node list
```

Get information:

```bash
ros2 node info /node_name
```

This can show:

- publishers
- subscribers
- services
- action servers
- action clients

Very useful when debugging communication.

---

# 45. Topic Debugging

List topics:

```bash
ros2 topic list
```

Get information:

```bash
ros2 topic info /cmd_vel
```

See data:

```bash
ros2 topic echo /cmd_vel
```

Check publishing frequency:

```bash
ros2 topic hz /cmd_vel
```

This is useful for checking whether a node is actually publishing data.

---

# 46. Parameter Debugging

List parameters:

```bash
ros2 param list
```

Get a parameter:

```bash
ros2 param get /node_name parameter_name
```

Set a parameter:

```bash
ros2 param set /node_name parameter_name value
```

---

# 47. TF Debugging

For TF:

```bash
ros2 run tf2_tools view_frames
```

This can generate a TF tree.

The concept is:

```text
base_link
   │
   ├── link1
   │    │
   │    └── link2
   │
   └── camera_link
```

If RViz displays the robot incorrectly, TF is one of the first things to check.

---

# 48. RQT Graph

Run:

```bash
rqt_graph
```

This provides a visual representation of ROS nodes and topics.

Example:

```text
teleop
  │
  │ /cmd_vel
  ▼
controller
  │
  │ motor commands
  ▼
robot
```

If you expected two nodes to communicate but there is no connection, `rqt_graph` is very useful.

---

# 49. Common Problems

## Problem: `Package not found`

Example:

```text
Package 'my_package' not found
```

Try:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

Then:

```bash
ros2 pkg list | grep my_package
```

---

## Problem: Launch file not found

Example:

```text
file 'robot.launch.py' was not found
```

Check:

```bash
ros2 pkg prefix my_package
```

Then check whether the launch file was installed.

Usually the problem is that the `launch/` directory was not installed correctly.

---

## Problem: Python launch file changed but ROS still uses old code

Try:

```bash
colcon build --symlink-install
```

Then:

```bash
source ~/ros2_ws/install/setup.bash
```

---

## Problem: Node executable not found

Example:

```text
executable 'my_node' not found
```

Check:

```bash
ros2 pkg executables my_package
```

This shows the executable names ROS 2 knows about.

---

## Problem: RViz opens but robot does not appear

Check:

```bash
ros2 topic list
```

Check TF:

```bash
ros2 run tf2_tools view_frames
```

Check robot state publisher:

```bash
ros2 node list
```

Look for:

```text
/robot_state_publisher
```

Also check whether RViz has the correct:

```text
Fixed Frame
```

---

# 50. How to Add a New Launch File

Inside the package:

```text
my_package/
└── launch/
    └── new_robot.launch.py
```

Create:

```python
from launch import LaunchDescription


def generate_launch_description():

    return LaunchDescription([])
```

Then add actions.

For example:

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    robot_node = Node(
        package='my_package',
        executable='robot_node',
        output='screen'
    )

    return LaunchDescription([
        robot_node
    ])
```

Build:

```bash
cd ~/ros2_ws
colcon build --symlink-install
```

Source:

```bash
source ~/ros2_ws/install/setup.bash
```

Run:

```bash
ros2 launch my_package new_robot.launch.py
```

---

# 51. How to Add a New Node

Suppose you already have:

```text
my_package
└── my_node
```

To launch it:

```python
Node(
    package='my_package',
    executable='my_node',
    output='screen'
)
```

The important information is:

```text
package
   ↓
Which ROS package?

executable
   ↓
Which executable?

output
   ↓
Where should output appear?
```

---

# 52. How to Make One Launch File Start Another

Parent:

```text
main.launch.py
```

Child:

```text
robot.launch.py
```

Parent launch file:

```python
IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        robot_launch_file
    )
)
```

Result:

```text
main.launch.py
      │
      │ include
      ▼
robot.launch.py
      │
      ├── robot_state_publisher
      ├── joint_state_publisher
      └── RViz
```

This is useful for creating modular launch systems.

---

# 53. How to Pass Values Between Launch Files

Parent:

```python
IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        child_launch
    ),
    launch_arguments={
        'use_rviz': 'true'
    }.items()
)
```

Child:

```python
use_rviz = LaunchConfiguration('use_rviz')
```

Then:

```python
Node(
    package='rviz2',
    executable='rviz2',
    condition=IfCondition(use_rviz)
)
```

Flow:

```text
Parent
 │
 │ use_rviz=true
 ▼
Child
 │
 ▼
IfCondition
 │
 ▼
RViz starts
```

---

# 54. How to Conditionally Start a Node

Declare:

```python
DeclareLaunchArgument(
    'use_rviz',
    default_value='true'
)
```

Retrieve:

```python
use_rviz = LaunchConfiguration('use_rviz')
```

Use:

```python
Node(
    package='rviz2',
    executable='rviz2',
    condition=IfCondition(use_rviz)
)
```

Then run:

```bash
ros2 launch my_package robot.launch.py use_rviz:=false
```

RViz will not start.

---

# 55. How to Delay a Node

Example:

```python
TimerAction(
    period=5.0,
    actions=[
        my_node
    ]
)
```

The node starts approximately five seconds after the launch system starts that action.

Useful when:

```text
Node A
   │
   │ initialization
   ▼
wait
   │
   ▼
Node B
```

---

# 56. How to Run a Normal Linux Command

Use:

```python
ExecuteProcess(
    cmd=['command', 'argument'],
    output='screen'
)
```

For example:

```python
ExecuteProcess(
    cmd=['echo', 'Hello ROS 2'],
    output='screen'
)
```

This is not the same as:

```python
Node()
```

Remember:

```text
ROS 2 executable
    → Node()

External command
    → ExecuteProcess()
```

---

# 57. ROS 2 Launch Cheat Sheet

| What you want | Use |
|---|---|
| Start ROS node | `Node()` |
| Start another launch file | `IncludeLaunchDescription()` |
| Start normal Linux process | `ExecuteProcess()` |
| Wait before starting something | `TimerAction()` |
| Create CLI option | `DeclareLaunchArgument()` |
| Read CLI option | `LaunchConfiguration()` |
| Conditional startup | `IfCondition()` |
| Opposite condition | `UnlessCondition()` |
| Find package | `FindPackageShare()` |
| Build path | `PathJoinSubstitution()` |
| Create launch description | `LaunchDescription()` |
| Define launch file entry point | `generate_launch_description()` |

---

# 58. Recommended Workflow

When developing a ROS 2 system, use this workflow.

## Step 1: Source ROS 2

```bash
source /opt/ros/humble/setup.bash
```

---

## Step 2: Go to workspace

```bash
cd ~/ros2_ws
```

---

## Step 3: Build

```bash
colcon build --symlink-install
```

---

## Step 4: Source workspace

```bash
source install/setup.bash
```

---

## Step 5: Check package

```bash
ros2 pkg list | grep my_package
```

---

## Step 6: Check executables

```bash
ros2 pkg executables my_package
```

---

## Step 7: Run launch file

```bash
ros2 launch my_package robot.launch.py
```

---

## Step 8: Debug

In another terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

Then:

```bash
ros2 node list
```

```bash
ros2 topic list
```

```bash
rqt_graph
```

---

# 59. Future Expansion

This repository can eventually become a complete personal ROS 2 reference.

Potential sections/files to add:

```text
launch/
├── robot.launch.py
├── simulation.launch.py
├── rviz.launch.py
├── teleop.launch.py
├── sensors.launch.py
└── navigation.launch.py
```

A large system could then look like:

```text
                    main.launch.py
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
     robot.launch     sensors.launch    rviz.launch
          │               │                │
          │               │                │
          ▼               ▼                ▼
     Robot State       LiDAR/Camera       RViz
     Publisher
          │
          ▼
         TF
```

This approach keeps each launch file focused on one responsibility.

---

# Important Mental Model

The most important thing to remember is that a launch file is basically a **startup manager**.

It does not need to contain the implementation of every node.

Instead:

```text
Launch File
     │
     ├── Start Node
     │
     ├── Start Node
     │
     ├── Include Launch File
     │        │
     │        ├── Start Node
     │        └── Start Node
     │
     ├── Start external process
     │
     ├── Wait
     │
     └── Apply conditions
```

Think of it as a manager.

---

# The Most Important ROS 2 Launch Concepts

## 1. `Node`

Starts a ROS 2 node.

```python
Node(...)
```

---

## 2. `IncludeLaunchDescription`

Starts another launch file.

```python
IncludeLaunchDescription(...)
```

Think:

```text
launch file inside launch file
```

---

## 3. `ExecuteProcess`

Starts a normal external process.

```python
ExecuteProcess(...)
```

---

## 4. `TimerAction`

Delays an action.

```python
TimerAction(...)
```

---

## 5. `DeclareLaunchArgument`

Creates an option that can be changed from the terminal.

```python
DeclareLaunchArgument(...)
```

---

## 6. `LaunchConfiguration`

Reads the option.

```python
LaunchConfiguration(...)
```

---

## 7. `IfCondition`

Run something only when a condition is true.

```python
IfCondition(...)
```

---

## 8. `UnlessCondition`

Run something when a condition is false.

```python
UnlessCondition(...)
```

---

## 9. `LaunchDescription`

Contains the actions that should be launched.

```python
LaunchDescription([
    ...
])
```

---

# Complete Conceptual Example

Imagine this command:

```bash
ros2 launch my_robot main.launch.py use_rviz:=true
```

ROS 2 performs approximately this flow:

```text
ros2 launch
     │
     ▼
Find package:
my_robot
     │
     ▼
Find:
main.launch.py
     │
     ▼
Call:
generate_launch_description()
     │
     ▼
Declare:
use_rviz
     │
     ▼
Read:
use_rviz=true
     │
     ├───────────────────────────┐
     │                           │
     ▼                           ▼
Include robot.launch       Start teleop
     │
     ▼
robot_state_publisher
     │
     ▼
TF
     │
     ▼
RViz
```

This is the core idea behind ROS 2 launch files.

---

# Quick Daily Reference

When you forget what to use:

```text
"I want to start a ROS node."
        ↓
      Node()

"I want to start another launch file."
        ↓
IncludeLaunchDescription()

"I want to run a Linux command."
        ↓
ExecuteProcess()

"I want to wait before starting something."
        ↓
TimerAction()

"I want an option from terminal."
        ↓
DeclareLaunchArgument()

"I want to read that option."
        ↓
LaunchConfiguration()

"I want to run something only if true."
        ↓
IfCondition()

"I want to run something only if false."
        ↓
UnlessCondition()

"I need a package's installed location."
        ↓
FindPackageShare()

"I need to construct a path."
        ↓
PathJoinSubstitution()
```

---

# Basic Commands

```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Go to workspace
cd ~/ros2_ws

# Build
colcon build --symlink-install

# Source workspace
source install/setup.bash

# List packages
ros2 pkg list

# List executables
ros2 pkg executables

# Run launch file
ros2 launch <package> <launch_file>

# Show launch arguments
ros2 launch <package> <launch_file> --show-args

# List nodes
ros2 node list

# List topics
ros2 topic list

# List services
ros2 service list

# List parameters
ros2 param list

# Show node information
ros2 node info <node>

# Show topic information
ros2 topic info <topic>

# Read topic
ros2 topic echo <topic>

# Show topic frequency
ros2 topic hz <topic>

# Start RQT graph
rqt_graph

# Generate TF tree
ros2 run tf2_tools view_frames
```

---

# Author

**Muhammad Al Imran Bin Salim**

GitHub:

https://github.com/imranlim

Repository:

https://github.com/imranlim/my-own-ros2-launch-file

---

# Final Note

This repository is intended to be a **personal ROS 2 launch-file reference**.

When adding a new launch file, try to document:

1. What the launch file does.
2. Which nodes it starts.
3. Which launch files it includes.
4. Which arguments it accepts.
5. Which parameters it uses.
6. Which topics are remapped.
7. Which conditions are used.
8. Whether anything is delayed.
9. What external processes are started.
10. How to run it.

The goal is that months later, you can open this repository and understand **why each launch action exists and how the complete ROS 2 system starts** without having to relearn everything from the beginning.
