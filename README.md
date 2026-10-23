# My Own ROS 2 Launch Files (`my-own-ros2-launch-file`)

![ROS 2 Humble](https://img.shields.io/badge/ROS_2-Humble-blue)
![Ubuntu](https://img.shields.io/badge/OS-Ubuntu_22.04-orange)
![License](https://img.shields.io/badge/License-Apache_2.0-green)

A personal reference and collection of custom **ROS 2 Humble** launch files (Python, XML, and YAML) designed for bringing up robot nodes, simulation environments, parameters, and remapping configurations.

---

## 📋 Table of Contents
1. [Prerequisites](#-prerequisites)
2. [Installation & Setup](#-installation--setup)
3. [Usage](#-usage)
4. [Package Configuration (`setup.py` / `CMakeLists.txt`)](#-package-configuration)
5. [Quick Reference Templates](#-quick-reference-templates)
6. [Useful Debugging Commands](#-useful-debugging-commands)

---

## 🛠 Prerequisites

Ensure you have the following installed on your system:
* **OS:** Ubuntu 22.04 LTS (Jammy Jellyfish)
* **ROS 2 Distribution:** ROS 2 Humble Hawksbill
* **Build Tool:** `colcon` (`sudo apt install python3-colcon-common-extensions`)

---

## 🚀 Installation & Setup

1. **Navigate to your ROS 2 workspace `src` directory:**
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
   ```

2. **Clone this repository:**
   ```bash
   git clone [https://github.com/imranlim/my-own-ros2-launch-file.git](https://github.com/imranlim/my-own-ros2-launch-file.git)
   ```

3. **Install dependencies (if any):**
   ```bash
   cd ~/ros2_ws
   rosdep install -i --from-path src --rosdistro humble -y
   ```

4. **Build the workspace:**
   ```bash
   colcon build --symlink-install
   ```
   *(Tip: Using `--symlink-install` allows you to edit Python launch files and YAML configs without needing to rebuild the package every time!)*

5. **Source the workspace:**
   ```bash
   source ~/ros2_ws/install/setup.bash
   ```

---

## 💻 Usage

### Running a Launch File Inside a Package
```bash
ros2 launch <package_name> <launch_file_name>.launch.py
```

### Running a Standalone Launch File Directly (By Path)
If you want to test a launch file directly without building a full package:
```bash
ros2 launch /path/to/your_file.launch.py
```

### Passing Launch Arguments via CLI
```bash
ros2 launch <package_name> <launch_file_name>.launch.py use_sim_time:=true
```

### Viewing Available Arguments for a Launch File
```bash
ros2 launch <package_name> <launch_file_name>.launch.py --show-args
```

---

## 📦 Package Configuration

When creating a new package that uses launch files, remember to include the `launch/` and `config/` directories in your build files so ROS 2 can find them.

### For Python Packages (`setup.py`)
Add `os` and `glob` imports at the top, and include the `launch` and `config` folders inside `data_files`:

```python
import os
from glob import glob
from setuptools import setup

package_name = 'your_package_name'

setup(
    # ... other setup parameters ...
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include all launch files
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        # Include all config/YAML files
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
    ],
)
```

### For C++ Packages (`CMakeLists.txt`)
Add the following before `ament_package()`:

```cmake
install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}/
)
```

### `package.xml` Dependencies
Add this to your `package.xml`:
```xml
<exec_depend>ros2launch</exec_depend>
```

---

## 📝 Quick Reference Templates

### 1. Basic Python Launch File (`example.launch.py`)
Starts nodes with custom parameters, namespaces, and topic remapping:

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    
    # 1. Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    declare_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    # 2. Path to YAML config file (Optional)
    # config_file = os.path.join(
    #     get_package_share_directory('your_package_name'),
    #     'config',
    #     'params.yaml'
    # )

    # 3. Define a Node
    my_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='custom_turtle',
        namespace='robot1',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}], # Or pass [config_file]
        remappings=[
            ('/robot1/turtle1/cmd_vel', '/cmd_vel'),
        ]
    )

    # 4. Return LaunchDescription
    return LaunchDescription([
        declare_sim_time_cmd,
        my_node
    ])
```

### 2. Including Another Launch File
Useful for combining multiple bringup files (e.g., LiDAR + Nav2 + Robot State Publisher):

```python
included_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        os.path.join(get_package_share_directory('other_package_name'), 'launch', 'other_file.launch.py')
    ]),
    launch_arguments={'use_sim_time': 'true'}.items()
)
```

---

## 🔍 Useful Debugging Commands

| Command | Description |
| :--- | :--- |
| `ros2 node list` | List all currently active nodes |
| `ros2 topic list` | List all active topics |
| `ros2 param list` | Check loaded parameters for active nodes |
| `rqt_graph` | Visualize node and topic connections |
| `ros2 run tf2_tools view_frames` | Generate a PDF of the current TF tree |

---

## 👤 Author
* **Muhammad Al Imran Bin Salim** - [@imranlim](https://github.com/imranlim)
