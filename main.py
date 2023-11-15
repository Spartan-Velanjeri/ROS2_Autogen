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


def pkg_creator(package_name,launch_file,urdf_path):

    subprocess.call(['ros2','pkg','create','--build-type','ament_cmake',package_name])
    main_path = os.getcwd()

    pkg_path = os.path.join(main_path,package_name)
    os.chdir(pkg_path)

    pkg_launch_path = os.path.join(pkg_path,"launch") # Inside created pkg
    pkg_urdf_path = os.path.join(pkg_path,"urdf") # Inside created pkg
    pkg_config_path = os.path.join(pkg_path,"config") #Inside created pkg
    pkg_rviz_path = os.path.join(pkg_path,"rviz")

    launch_automaton_path = os.path.join(main_path,launch_file) # In source
    urdf_automaton_path = os.path.join(main_path,"urdf") # In source
    rviz_automaton_path = os.path.join(main_path,"default.rviz")

    os.mkdir(pkg_launch_path)
    os.mkdir(pkg_config_path)
    os.mkdir(pkg_rviz_path)

    if os.path.isdir(urdf_automaton_path): # If a URDF folder already exists
        shutil.copytree(urdf_automaton_path,pkg_urdf_path,dirs_exist_ok=True) # Copies entire urdf folder content into the urdf folder of pkg
    
    else: # If just one urdf, create a directory in pkg and copies the file
        os.mkdir(pkg_urdf_path)
        shutil.copy(urdf_path,pkg_urdf_path)

    shutil.copy(launch_automaton_path,pkg_launch_path) # Copies launch file to launch folder inside the pkg
    shutil.copy(rviz_automaton_path,pkg_rviz_path) # Copies default rviz config into config folder
    os.remove(launch_automaton_path)
    
questions = {}
questions['package_name'] = 'Package Name : '
questions['urdf_path'] = "Path to the URDF: "
questions['simulator_used'] = "Simulator of Choice: "

questions['nodes'] = "Nodes of Choice:"
checker = 1 # Not required for now
dir_list = ["include", "launch", "src", "urdf","config", "rviz"]
script_list = [] # Until nodes start coming
package_name = input_func(questions['package_name'],checker)
urdf_path = input_func(questions['urdf_path'],checker)
sim_name = 'ignition_gazebo'
launch_file = f"{package_name}.launch.py"
launch_generator(package_name,urdf_path,sim_name)
pkg_creator(package_name,launch_file,urdf_path)
appender(dir_list,script_list) #Make sure the previous func brings you into the pkg dir

print(f"Your Package is complete and called {package_name}. Make sure to copy it in colcon workspace and build")
