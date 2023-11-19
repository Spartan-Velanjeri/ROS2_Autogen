# ROS2_Autogen

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

Generates packages with launch files automatically from URDF for ROS2 with your required simulator. Built to view URDF quickly on RViz and Gazebo.
Currently supports Ignition Gazebo Fortress Simulator.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Upcoming Features](#Upcoming_Features)
- [Notes](#Notes)

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

## Usage

To utilize this project, follow these steps:

1. **Clone the repository:**  
   Clone this repository and copy your URDF file or folder into the cloned repository.

2. **Run the main.py file:**
   Execute the following command in your terminal:
   ```bash
   python3 main.py 
   
3.  **Provide package name and URDF path:**
    When prompted, enter your package name and copy the absolute path of the URDF present inside the repository. This will generate your ROS2 package inside the repository.

4.  **Copy the package into your workspace:**
    Once the package is generated, copy it into your ROS2 workspace, then build and launch it.


## Upcoming_Features

1. Support for Gazebo Classic and test with different ROS2 Versions
2. Support for additional scripts and nodes to be added in launch file

## Notes

1. If you have meshes, make sure to launch from inside the src folder to view all the meshes on the simulator. For some reason, it is not showing up when launching from another directory
