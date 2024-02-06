# ROS_Autogen

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

Generates packages with launch files automatically from URDF for ROS2 with your required simulator with a simple GUI. Built to view URDF quickly on RViz and Gazebo.
Currently supports **[Ignition Gazebo Fortress](https://gazebosim.org/docs/fortress/tutorials)** and **[Gazebo Classic](https://classic.gazebosim.org)** .

Also adds both **[Robot_state_publisher](https://index.ros.org/p/robot_state_publisher/github-ros-robot_state_publisher)**, **[Joint_state_publisher](https://index.ros.org/p/joint_state_publisher/)** and **[joint_state_publisher_gui](https://index.ros.org/p/joint_state_publisher_gui/github-ros-joint_state_publisher/)** if required to test your robot.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Upcoming Features](#Upcoming_Features)
- [Troubleshooting](#Troubleshooting)

## Installation

This project has been tested with Ubuntu 22.04. To install the necessary components, follow these steps:

- **ROS2 Humble Hawksbill:**  
  Follow the installation instructions for ROS2 Humble Hawksbill from [here](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html).

- **Ignition Gazebo Fortress:**  
  Install Ignition Gazebo Fortress by following the steps outlined [here](https://gazebosim.org/docs/fortress/install_ubuntu).


An easier way to install both ROS2 and Ignition Gazebo Fortress is to use `apt`:

```bash
sudo apt-get install ros-humble-desktop-full
```

Also if you would like to test the joint-states of your robot, don't forget to install joint-state-publisher-gui with 

```bash
sudo apt-get install ros-humble-joint-state-publisher-gui
```

Also do install the [send2trash](https://pypi.org/project/Send2Trash/) python library as it'll allow you to quickly send your older, redundant package to trash if you are creating a new one with the same name.

```bash
pip install send2trash
```

## Usage

   I'll be demonstrating the use of these repo with two examples: 
   * A Standalone URDF file without any meshes. I've taken the example from [gz_ros2_control](https://github.com/ros-controls/gz_ros2_control/blob/master/gz_ros2_control_demos/urdf/test_diff_drive.xacro.urdf)
    ![diff_drive](https://github.com/Spartan-Velanjeri/ROS2_Autogen/assets/26743932/d65591bb-0d99-40aa-9743-d95d3460f75d)  


   * An URDF with meshes. I've used the MiR 100 Robot developed as a community project. You can check it out [here](https://github.com/relffok/mir_robot/tree/humble-devel/mir_description)
   ![mir100](https://github.com/Spartan-Velanjeri/ROS2_Autogen/assets/26743932/a790612d-d042-47a5-8707-9bdc2b242135)  
   
Each step will be tried with these two examples. You can choose the suitable method based on your requirement. 

The same approach will work with Docker as well.

### Linux

To utilize this project, follow these steps:

1. #### **Clone the repository:**  
   Clone this repository and copy your URDF file or folder into the cloned repository inside the urdf folder. If you have meshes required with your URDF, copy them too inside the meshes folder.

    * Standalone URDF:
        Just copy the test_diff_drive.xacro.urdf into the URDF folder of our repo

        ![standalone_copy](https://github.com/Spartan-Velanjeri/ROS2_Autogen/assets/26743932/27176618-a4af-40ca-b3e9-378e0bb9a466)

    * URDF with Meshes:
        Copy the urdf and the include folder into the URDF folder and the mesh files in the mesh folder of the repo respectively. 
   
        ![mesh_copy](https://github.com/Spartan-Velanjeri/ROS2_Autogen/assets/26743932/cacf56c5-c8da-469c-a857-e15d114d0411)

2. #### **Run the main.py file:**
   Execute the following command in your terminal from within our repo:
   ```bash
   python main.py 


3. #### **Provide package name and URDF path:**

    Just enter your package name, path of the file relative to the urdf folder, simulators you want to work with and if you would like the joint state publisher GUI to test your joints 

    <br/>

    * Standalone URDF: 

    ![standalone_pkg](https://github.com/Spartan-Velanjeri/ROS2_Autogen/assets/26743932/48046c37-c087-4ed4-97ad-23556e3eafb8)  


    <br/>

    * URDF with Meshes: Since the urdf file links to other files in the include folder with a specific pkg name (in this case, mir_description), you MUST use the same name for the pkg name. Else you can change the pkg name in URDF file manually. 
    Let's keep the same default name given in the URDF.

    ![create_mesh_pkg](https://github.com/Spartan-Velanjeri/ROS2_Autogen/assets/26743932/ffeac530-1ea4-4c96-ab24-5244e8ee44e0)

    <br/>
4. #### **Copy the package into your workspace:**
    Once the package is generated, copy it into your ROS2 workspace, then build and launch it.

    * Standalone URDF:

        ![standalone_demo](https://github.com/Spartan-Velanjeri/ROS2_Autogen/assets/26743932/0cb15523-fa0a-4a6a-aeee-d748b324f8ee)

    * URDF with Meshes:

        ![mesh_demo](https://github.com/Spartan-Velanjeri/ROS2_Autogen/assets/26743932/aef0f014-ae13-4a08-beb9-3d4b35acd5d8)
        The reason for the lack of rear wheels is that we haven't initialised any controllers here. Once we do that, we can see the wheels as well (not included here)
###  Docker 

To run the demo with GUI we are going to use [Rocker](https://github.com/osrf/rocker/) which is a tool to run docker images with customized local support injected for things like nvidia support. Rocker also supports user id specific files for cleaner mounting file permissions. You can install this tool with the following [instructions](https://github.com/osrf/rocker/#installation). Make sure you meet all of the [prerequisites](https://github.com/osrf/rocker/#prerequisites).


1. **Clone the repository:**  
   Copy your URDF file or folder into the cloned repository inside the urdf folder. If you have meshes required with your URDF, copy them too inside the meshes folder

2. **Build the Dockerfile:** Navigate into the repo and run
    ```bash
    docker build . -t image_name
    ```


3. **Run the docker:** The following commands will open the main program which generates the pkg. Replace path_of_ros_autogen_on_your_host with the actual path.

    ```bash 
    rocker --x11 --nvidia --name ros_autogen image_name --volume /path_of_ros_autogen_on_your_host:/ros_autogen_runner
    ```

4. **Run the Script and provide package name and URDF path:**

    ```bash
    python3 main.py
    ```
    When prompted, enter your package name and copy the RELATIVE path of the URDF present inside the repository (usually urdf/your_urdf.urdf). This will generate your ROS2 package inside the repository.

5. **Launch your Package:** In another terminal, run the following commands. Replace package_name with your ros2_pkg generated by the autogen.

    ```bash
    cp -r package_name /ros2_ws/src
    cd /ros2_ws
    colcon build
    source install/setup.bash
    ros2 launch package_name package_name.launch.py
    ```

Note: If you have any other dependencies for your launch, use Rosdep or APT installs to install them.

## Upcoming_Features

1. Support for additional scripts and nodes to be added in launch file (Will be part of another project)

## Troubleshooting


1. If you are spawning the robot with Gazebo Classic, make sure that the main urdf is of format .urdf and NOT .urdf.xacro as it'll cause some troubles while trying to parse it on Gazebo Classic. 
Just run the command after sourcing the description pkg of the robot to convert the .urdf.
xacro to just .urdf 

    ```bash
    ros2 run xacro xacro your_file.urdf.xacro > your_file.urdf
    ```

    Then copy THIS .urdf file into the ROS Autogen's urdf folder along with all the other files from the description pkg's urdf folder.

    When running the main.py, make sure to point to this .urdf when asked about the path to the URDF.

There's no need to change anything with Ignition Gazebo as it can work with both .urdf and .urdf.xacro.

## Tkinter based gui nodes 

refer: [tkinter ros gui dev notes](./tk_nodes_notes.md)