#
# We are using this program to auto-generate ROS packages with just a URDF folder (should include controllers in Config)
# The result would be a ROS_pkg with Launch files, package.xml and CMakelists.txt
# You can then directly build this ROS_pkg in your Colcon workspace

import subprocess
import shutil
from utils.launch_maker import launch_generator
import os
from utils.cmakelist_editor import appender
import send2trash
import sys

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

    
def pkg_creator(package_name,launch_file,urdf_relative_path):
    
    meshes_available = False
    main_path = os.getcwd()
    existing_folder = os.path.join(main_path, package_name)
    if os.path.exists(existing_folder) and os.path.isdir(existing_folder):
        print("But we gotta a slight problem ! \n")
        print("Do you want to replace the package",package_name,"\nsince it has the same name as the pkg to be created, Y or N: ")
        decision = input("Y or N: ")
    
        if decision == "Y" or decision =="y":
            print("Deleting existing pkg to make way for the new one")
            try:
                send2trash.send2trash(existing_folder)
                print(f"Successfully moved '{package_name}' to trash.")
            except OSError as e:
                print(f"Failed to move '{package_name}' to trash: {e}")
                sys.exit(1)
        else:
            print("Exiting Program Now")
            sys.exit(1)




    subprocess.call(['ros2','pkg','create','--build-type','ament_cmake',package_name])
    urdf_path = os.path.join(main_path,urdf_relative_path) 

    pkg_path = os.path.join(main_path,package_name)
    os.chdir(pkg_path)

    # os.rmdir("include")
    # os.rmdir("src")

    pkg_launch_path = os.path.join(pkg_path,"launch") # Inside created pkg
    pkg_urdf_path = os.path.join(pkg_path,"urdf") # Inside created pkg
    pkg_config_path = os.path.join(pkg_path,"config") #Inside created pkg
    pkg_rviz_path = os.path.join(pkg_path,"rviz") #Inside created pkg
    pkg_meshes_path = os.path.join(pkg_path,"meshes") #Inside created pkg
    pkg_env_hooks_path = os.path.join(pkg_path,"env-hooks") # Inside created pkg

    launch_automaton_path = os.path.join(main_path,launch_file) # In source
    urdf_automaton_path = os.path.join(main_path,"urdf") # In source
    rviz_automaton_path = os.path.join(main_path,"default.rviz")
    meshes_automaton_path = os.path.join(main_path,"meshes")

    os.mkdir(pkg_launch_path)
    os.mkdir(pkg_config_path)
    os.mkdir(pkg_rviz_path)

    if os.path.isdir(urdf_automaton_path): # If a URDF folder already exists
        shutil.copytree(urdf_automaton_path,pkg_urdf_path,dirs_exist_ok=True) # Copies entire urdf folder content into the urdf folder of pkg
    
    else: # If just one urdf, create a directory in pkg and copies the file
        os.mkdir(pkg_urdf_path)
        shutil.copy(urdf_path,pkg_urdf_path)

    if os.path.isdir(meshes_automaton_path): # Only if you have additional meshes, it'll create a folder in the pkg
        shutil.copytree(meshes_automaton_path,pkg_meshes_path,dirs_exist_ok=True)
        meshes_available=True
        os.mkdir(pkg_env_hooks_path)
        env_hook_file = os.path.join(main_path,pkg_env_hooks_path,f"{package_name}.sh.in")
        with open(env_hook_file,'w') as file:
            file.writelines('ament_prepend_unique_value GAZEBO_MODEL_PATH "@CMAKE_INSTALL_PREFIX@/share"')
            file.write("\n")
            file.writelines('ament_prepend_unique_value GZ_SIM_RESOURCE_PATH "@CMAKE_INSTALL_PREFIX@/share"')
            file.write("\n")
            file.writelines('ament_prepend_unique_value IGN_GAZEBO_RESOURCE_PATH "@CMAKE_INSTALL_PREFIX@/share"')

    

    shutil.copy(launch_automaton_path,pkg_launch_path) # Copies launch file to launch folder inside the pkg
    shutil.copy(rviz_automaton_path,pkg_rviz_path) # Copies default rviz config into config folder
    os.remove(launch_automaton_path)
    
    return meshes_available
    
questions = {}
questions['package_name'] = 'Your ROS Package Name (named autogen_pkg by DEFAULT) : '
questions['urdf_relative_path'] = "Path to the URDF relative from the ROS_Autogen Repo, something like urdf/.... \n\nPath to the URDF :  "
questions['simulator_used'] = "Simulator of Choice: Currently Supported are \n\n 1)  Ignition_gazebo \n\n 2)  Gazebo Classic (DEFAULT) \n\n 1 or 2: "
questions['nodes'] = "Nodes of Choice:"
questions['jsp-gui'] = "Do you want to test your joints with the joint state publisher GUI? \n Y or N: "
# questions['meshes'] = "Would you be using meshes/worlds now or in the future, Y/N? \n Autogen will create an env hook for you, \n so that gazebo can recognise the meshes and worlds for you. RECOMMENDED "
checker = 1 # Not required for now
dir_list = ["include", "launch", "src", "urdf","config", "rviz","meshes"]
script_list = [] # Until nodes start coming
package_name = "autogen_pkg"
package_name = input_func(questions['package_name'],checker)
print("\n")
urdf_relative_path = input_func(questions['urdf_relative_path'],checker)
base_name, extension = os.path.splitext(urdf_relative_path)
print(base_name)
print("\n")
sim_name = input_func(questions['simulator_used'],checker)
print("\n")
# meshes_required = input_func(questions['meshes'],checker)
jsp_gui = input_func(questions['jsp-gui'],checker)
jsp_gui = 1 if jsp_gui =="Y" or jsp_gui == "y" else 0
if jsp_gui:
    print("Make sure to install Joint_state_publisher_gui")
print("\n")

mesh_include = False
simulators = {"1":"Ignition Gazebo","2":"Gazebo Classic"}



print(" \n ***********************************  ROS_AUTOGEN PROCESSING********************************* \n ")

# print("\n \n A New Package named",package_name,"with Robot State Publisher, Joint State Publisher, Rviz and",simulators[sim_name],"coming right up ! \n \n ")

launch_file = f"{package_name}.launch.py"
launch_generator(package_name,urdf_relative_path,sim_name,jsp_gui)
meshes_available = pkg_creator(package_name,launch_file,urdf_relative_path)
# if meshes_available or meshes_required=="Y" or meshes_required=="y":
#     print("meshes support will be added")
#     dir_list.append("meshes")
#     mesh_include = True
appender(dir_list,script_list) #Make sure the previous func brings you into the pkg dir

print(f"Your Package is complete and called {package_name}. Make sure to copy it in colcon workspace and build")
