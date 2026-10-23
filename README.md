![ROS 2 Humble](https://img.shields.io/badge/ROS_2-Humble-blue)
![Ubuntu](https://img.shields.io/badge/OS-Ubuntu_22.04-orange)
![License](https://img.shields.io/badge/License-Apache_2.0-green)

# ROS 2 Robot Project

My ROS 2 robot project contains three main packages:

```text
src/
├── robot_description/
├── robot_control/
└── robot_simulation/
```

## 1. Packages

### `robot_description`

Contains the robot model and visualization.

```text
robot_description/
├── launch/
│   └── display.launch.py
├── urdf/
│   ├── assy.urdf
│   ├── body.urdf
│   ├── wheel_left.urdf
│   ├── wheel_right.urdf
│   ├── shaft.urdf
│   └── caster.urdf
└── rviz/
    └── urdf.rviz
```

`assy.urdf` is the main robot file. It combines the individual URDF files.

`display.launch.py` starts:

- `robot_state_publisher`
- joint state publisher
- RViz

---

### `robot_control`

Contains joystick, keyboard and velocity control.

```text
robot_control/
├── launch/
│   └── control.launch.py
└── config/
    ├── joy_config.yaml
    ├── teleop_twist.yaml
    ├── keyboard_twist.yaml
    └── twist_mux.yaml
```

Control flow:

```text
Joystick
   ↓
/joy
   ↓
teleop_twist_joy
   ↓
/joy/cmd_vel
          \
           ↓
        twist_mux
           ↑
          /
/key/cmd_vel
   ↑
Keyboard
```

The final output is:

```text
/cmd_vel
```

The keyboard teleop is started after a **5 second delay** in my `control.launch.py`.

---

### `robot_simulation`

Contains Gazebo and the robot controllers.

```text
robot_simulation/
├── launch/
│   └── simulation.launch.py
├── config/
│   ├── diffdrive.yaml
│   └── joints.yaml
└── world/
    └── robot_world.world
```

`simulation.launch.py` is my **main launch file**.

It starts:

- `display.launch.py`
- `control.launch.py`
- Gazebo
- robot spawning
- `joint_state_broadcaster`
- `diff_drive_base_controller`

---

# 2. Main Launch

Use:

```bash
ros2 launch robot_simulation simulation.launch.py
```

This is the main command I should remember.

The startup structure is:

```text
simulation.launch.py
        |
        +── display.launch.py
        |       |
        |       +── robot_state_publisher
        |       +── RViz
        |       +── joint state publisher
        |
        +── control.launch.py
        |       |
        |       +── joystick
        |       +── joystick teleop
        |       +── keyboard teleop
        |       +── twist_mux
        |
        +── Gazebo
        |       |
        |       +── robot_world.world
        |       +── spawn robot
        |       +── ros2_control
        |
        +── Controllers
                |
                +── joint_state_broadcaster
                +── diff_drive_base_controller
```

---

# 3. Launch File Relationship

The important part of my code is:

```text
simulation.launch.py
        |
        +── IncludeLaunchDescription
        |       ↓
        |   display.launch.py
        |
        +── IncludeLaunchDescription
                ↓
            control.launch.py
```

So I **do not need to launch `display.launch.py` and `control.launch.py` separately** when using the main simulation.

Just run:

```bash
ros2 launch robot_simulation simulation.launch.py
```

---

# 4. Robot Description Flow

My robot model works like this:

```text
assy.urdf
   |
   +── body.urdf
   +── wheel_left.urdf
   +── wheel_right.urdf
   +── shaft.urdf
   +── caster.urdf
   |
   ↓
xacro
   |
   ↓
robot_description
   |
   +── robot_state_publisher
   |
   +── Gazebo
   |
   +── RViz
```

If I want to change the robot shape, dimensions, wheels, caster, etc., I edit the files inside:

```text
robot_description/urdf/
```

---

# 5. Control Flow

My control system is:

```text
Joystick
    ↓
/joy
    ↓
teleop_twist_joy
    ↓
/joy/cmd_vel
    \
     \
      → twist_mux → /cmd_vel
     /
    /
/key/cmd_vel
    ↑
Keyboard
```

Then:

```text
/cmd_vel
    ↓
diff_drive_base_controller
    ↓
left/right wheels
```

---

# 6. Important Configuration Files

| File | Purpose |
|---|---|
| `assy.urdf` | Main robot assembly |
| `display.launch.py` | Robot model + RViz |
| `control.launch.py` | Joystick + keyboard + mux |
| `simulation.launch.py` | Main launch file |
| `diffdrive.yaml` | Differential drive controller |
| `joy_config.yaml` | Joystick settings |
| `teleop_twist.yaml` | Joystick movement mapping |
| `keyboard_twist.yaml` | Keyboard speed/settings |
| `twist_mux.yaml` | Control priority |
| `robot_world.world` | Gazebo world |

---

# 7. Build

From the workspace:

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

Then launch:

```bash
ros2 launch robot_simulation simulation.launch.py
```

---

# 8. Useful Debug Commands

Check nodes:

```bash
ros2 node list
```

Check topics:

```bash
ros2 topic list
```

Check velocity:

```bash
ros2 topic echo /cmd_vel
```

Check controllers:

```bash
ros2 control list_controllers
```

Check the ROS graph:

```bash
rqt_graph
```

---

# 9. Quick Reference

### Start everything

```bash
ros2 launch robot_simulation simulation.launch.py
```

### Robot model only

```bash
ros2 launch robot_description display.launch.py
```

### Control only

```bash
ros2 launch robot_control control.launch.py
```

### Main files to edit

Robot:

```text
src/robot_description/urdf/
```

Control:

```text
src/robot_control/config/
```

Simulation:

```text
src/robot_simulation/config/
src/robot_simulation/world/
```

Main startup:

```text
src/robot_simulation/launch/simulation.launch.py
```

**Remember:**

```text
simulation.launch.py
        ↓
display.launch.py + control.launch.py + Gazebo
        ↓
             /cmd_vel
                ↓
       diff_drive_controller
                ↓
              Robot
```
