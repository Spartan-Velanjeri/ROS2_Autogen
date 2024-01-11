


git clone https://github.com/Spartan-Velanjeri/ROS2_Autogen.git

copy only robot_description from github repo



----

UR5 arm

ur_description



----


USing the [ROBOTIS-GIT/turtlebot3_manipulation](https://github.com/ROBOTIS-GIT/turtlebot3_manipulation) repo

```

$REPO_NAME=turtlebot3_manipulation

mkdir -p $REPO_NAME_desc

cd turtlebot3_manipulation_desc

```

Take only robot_description subfolder





```

export REPO_NAME=turtlebot3_manipulation \
    && export REPO_URL=https://github.com/ROBOTIS-GIT/turtlebot3_manipulation \
    && export DESC_SUBDIR_URL=turtlebot3_manipulation/turtlebot3_manipulation_description

mkdir -p $REPO_NAME\_desc \
    && cd $REPO_NAME\_desc \
    && git clone $REPO_URL




cp $DESC_SUBDIR_URL/urdf/* ../urdf/ 

cp $DESC_SUBDIR_URL/meshes/* ../meshes/

cd ..

rm -rf $REPO_NAME\_desc

pip install send2trash

```

sparse checkout (need to test more)

```
export REPO_NAME=turtlebot3_manipulation \
    && export REPO_URL=https://github.com/ROBOTIS-GIT/turtlebot3_manipulation && \
    && export DESC_DIR_URL=turtlebot3_manipulation/turtlebot3_manipulation_description


git clone --depth 1 --no-checkout $REPO_URL && \
    git sparse-checkout set $DESC_DIR_URL && \
    git checkout
```
refs: 

- [SO | How do I clone a subdirectory only of a Git repository?](https://stackoverflow.com/questions/600079/how-do-i-clone-a-subdirectory-only-of-a-git-repository)
- [Clone Specific Subdirectory/Branch with Git](https://medium.com/@judyess/how-to-clone-specific-subdirectory-branch-with-git-3fb02fd35b68)
- [ Github Engineering Blog: Get up to speed with partial clone and shallow clone](https://github.blog/2020-12-21-get-up-to-speed-with-partial-clone-and-shallow-clone/)



### run main file


```
python main.py
```

package_name = turtlebot3_manipulation_description

urdf_file_path = urdf/turtlebot3_manipulation_robot.urdf.xacro

```
mkdir -p ros2_ws/src


cp -r turtlebot3_manipulation_description ros2_ws/src
cd ros2_ws
colcon build
source install/setup.bash
ros2 launch turtlebot3_manipulation turtlebot3_manipulation.launch.py
```

### misc notes, 

Provide package name and URDF path: When prompted, enter your package name (IMPORTANT: Make sure to name it with the same pkg name as present in the URDF file especially if the URDF file points to other resources(meshes,other urdfs) with the pkg name as path) and copy the RELATIVE path of the URDF present inside the repository (usually urdf/your_urdf.urdf). This will generate your ROS2 package inside the repository.

^^ found this confusing ion first glance


#### package not found error

(ros2) nemo@homelab:~/code/repos/ROS2_Autogen/test_ws$ ros2 launch turtlebot3_manipulation turtlebot3_manipulation.launch.py 
[INFO] [launch]: All log files can be found below /home/nemo/.ros/log/2024-01-11-19-53-48-608133-homelab-17061
[INFO] [launch]: Default logging verbosity is set to INFO
[ERROR] [launch]: Caught exception in launch (see debug for traceback): Caught exception when trying to load file of format [py]: package not found: "package 'turtlebot3_description' not found, searching: ['/home/nemo/code/repos/ROS2_Autogen/test_ws/install/turtlebot3_manipulation', '/home/nemo/miniconda3/envs/ros2']"


urdf file 

```
<?xml version="1.0"?>
<robot name="turtlebot3_manipulation" xmlns:xacro="http://ros.org/wiki/xacro">

  <!-- Include TurtleBot3 Waffle URDF -->
  <xacro:include filename="$(find turtlebot3_description)/urdf/turtlebot3_waffle_pi_for_open_manipulator.urdf.xacro"/>

  <!-- Include OpenMANIPULATOR URDF -->
  <xacro:include filename="$(find turtlebot3_manipulation_description)/urdf/open_manipulator_x.urdf.xacro"/>

  <!-- Base fixed joint -->
  <joint name="base_fixed" type="fixed">
    <origin xyz="-0.092 0.0 0.091" rpy="0 0 0"/>
    <parent link="base_link"/>
    <child link="link1"/>
  </joint>

</robot>

```

#### Duplicate package names not supported:

```
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen/ur_ws$ colcon build
[0.675s] colcon ERROR colcon build: Duplicate package names not supported:
- ur_description:
  - src/Universal_Robots_ROS2_Description
  - src/ur_description

```


```
(ros2) nemo@homelab:~/code/repos/ur_ws2$ ros2 launch ur_description ur_description.launch.py 
[INFO] [launch]: All log files can be found below /home/nemo/.ros/log/2024-01-11-21-10-35-704443-homelab-20470
[INFO] [launch]: Default logging verbosity is set to INFO
[ERROR] [launch]: Caught exception in launch (see debug for traceback): Caught exception when trying to load file of format [py]: Undefined substitution argument name

```