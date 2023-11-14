#
# We are using this program to auto-generate ROS packages with just a URDF folder (should include controllers in Config)
# The result would be a ROS_pkg with Launch files, package.xml and CMakelists.txt
# You can then directly build this ROS_pkg in your Colcon workspace

import subprocess
import shutil
from utils.launch_maker import launch_generator
import os
from utils.cmakelist_editor import appender

def input_func(input_sentence,checker):
    data = input(input_sentence)
    if checker != 1:
        condition = input("Is %s fine? Y or N" % data)

        if (condition == "Y" or condition == "y"):
            return data
        else:
            input_func(input_sentence)
    else:
        return data


def pkg_creator(package_name,launch_file):

    subprocess.call(['ros2','pkg','create','--build-type','ament_cmake',package_name])
    main_path = os.getcwd()
    print(main_path)
    pkg_path = os.path.join(main_path,package_name)
    os.chdir(pkg_path)

    launch_path = os.path.join(pkg_path,"launch")
    urdf_path = os.path.join(pkg_path,"urdf")
    launch_file_path = os.path.join(main_path,launch_file)
    urdf_file_path = os.path.join(main_path,"urdf")

    os.mkdir(launch_path)

    shutil.copytree(urdf_file_path,urdf_path,dirs_exist_ok=True) # Copies entire urdf folder content into the urdf folder of pkg
    shutil.copy(launch_file_path,launch_path) # Copies launch file to launch folder inside the pkg

    
questions = {}
questions['package_name'] = 'Package Name : '
questions['urdf_path'] = "Path to the URDF: "
questions['simulator_used'] = "Simulator of Choice: "

questions['nodes'] = "Nodes of Choice:"
checker = 1 # Not required for now
dir_list = ["include", "launch", "src", "urdf" ]
script_list = []    
package_name = input_func(questions['package_name'],checker)
urdf_path = input_func(questions['urdf_path'],checker)
sim_name = 'ignition_gazebo'
launch_file = f"{package_name}.launch.py"
launch_generator(package_name,urdf_path,sim_name)
pkg_creator(package_name,launch_file)
appender(dir_list,script_list)

print(f"Your Package is complete and called {package_name}. Make sure to copy it in colcon workspace and build")
