
## run UR10 arm

```
cd ~/ROS2_Autogen
git clone https://github.com/ros-industrial/universal_robot.git

cp -r universal_robot/ur_description/urdf/* urdf/
cp -r universal_robot/ur_description/meshes/* meshes/

cp -r universal_robot/ur_description/config ./

# run main file

python main.py

User Interface dialog:

  package_name: ur_description
  urdf_filepath: urdf/ur10.xacro
  Ign Gazebo 
  
    Submit

# create new ws

mkdir -p ws_ur_description/src
cp -r ur_description ws_ur_description/src/

cd ws_ur_description

colcon build
source install/setup.bash

ros2 launch ur_description ur_description.launch.py

```
-------

git clone https://github.com/Spartan-Velanjeri/ROS2_Autogen.git

copy only robot_description from github repo


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


#### missing files; No such file or directory: error

```
Your Package is complete and called ur_description. Make sure to copy it in a colcon workspace and build
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen$ cp -r ur_description/ ws_ur10/src/
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen$ ls ws_ur10/src/ur_description/
CMakeLists.txt  env-hooks/      launch/         package.xml     src/            
config/         include/        meshes/         rviz/           urdf/           
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen$ ls ws_ur10/src/ur_description/urdf/
.gitkeep     inc/         ur10e.xacro  ur10.xacro   ur16e.xacro  ur3e.xacro   ur3.xacro    ur5e.xacro   ur5.xacro    ur.xacro     

(ros2) nemo@homelab:~/code/repos/ROS2_Autogen$ cd ws_ur10/
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen/ws_ur10$ ls
src  tmp
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen/ws_ur10$ colcon build
[0.744s] colcon ERROR colcon build: Duplicate package names not supported:
- ur_description:
  - src/ur_description
  - tmp/universal_robot/ur_description
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen/ws_ur10$ rm -rf tmp/
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen/ws_ur10$ colcon build
Starting >>> ur_description
[0.703s] colcon.colcon_ros.prefix_path.ament WARNING The path '/home/nemo/code/repos/ROS2_Autogen/ws_ur10/install/ur10' in the environment variable AMENT_PREFIX_PATH doesn't exist
[0.704s] colcon.colcon_ros.prefix_path.catkin WARNING The path '/home/nemo/code/repos/ROS2_Autogen/ws_ur10/install/ur10' in the environment variable CMAKE_PREFIX_PATH doesn't exist
Finished <<< ur_description [2.38s]

Summary: 1 package finished [2.63s]
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen/ws_ur10$ source install/setup.bash 
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen/ws_ur10$ ros2 launch ur_description ur_description.launch.py 
[INFO] [launch]: All log files can be found below /home/nemo/.ros/log/2024-01-12-17-02-19-490878-homelab-18993
[INFO] [launch]: Default logging verbosity is set to INFO
[ERROR] [launch]: Caught exception in launch (see debug for traceback): Caught exception when trying to load file of format [py]: [Errno 2] No such file or directory: '/home/nemo/code/repos/ROS2_Autogen/ws_ur10/install/ur_description/share/ur_description/config/ur10e/joint_limits.yaml' 
when evaluating expression 'xacro.load_yaml(joint_limits_parameters_file)' 
when evaluating expression 'config_joint_limit_parameters['joint_limits']' 
when evaluating expression 'sec_limits['shoulder_pan']['min_position']'
(ros2) nemo@homelab:~/code/repos/ROS2_Autogen/ws_ur10$ 

```

^^ fixed this by also copying config folder with urdf and meshes

now works with universal robots