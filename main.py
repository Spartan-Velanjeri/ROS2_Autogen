import tkinter as tk
from tkinter import font
from generator import generator
import os

def get_inputs():
    package_name = entry_packagename.get()
    file_path = entry_filepath.get()
    sim_name = radio_var.get()
    jsp_gui = radio_jsp.get()

    # Do something with the inputs (for example, print them)
    print("Package Name:", package_name)
    print("File Path:", file_path)
    print("Gazebo Type:", sim_name)
    print(jsp_gui)
    generator(package_name,file_path,sim_name,jsp_gui)

def on_window_resize(event):
    # Update elements on window resize
    new_width = root.winfo_width()
    new_height = root.winfo_height()
    #print(f"Window resized to Width: {new_width}, Height: {new_height}")

# Create the main window
root = tk.Tk()
root.title("ROS_Autogen")
root.geometry("550x500")  # Set initial window size

# Customize fonts and colors
bg_color = "#121212"  # Dark background color
fg_color = "#00FF00"  # Green text color
entry_bg_color = "#303030"  # Darker entry background color
entry_fg_color = "#00FF00"  # Entry text color

# Set the background color
root.config(bg=bg_color)

# Prevent window from resizing based on its contents
root.pack_propagate(False)

# Create a custom font
custom_font = font.Font(family="Courier", size=12)


# Package Name input
label_packagename = tk.Label(root, text="Package Name:", fg=fg_color, bg=bg_color, font=custom_font)
label_packagename.pack()

entry_packagename = tk.Entry(root, bg=entry_bg_color, fg=entry_fg_color, font=custom_font)
entry_packagename.pack(fill=tk.X)

# File Path input, TRY ADDING THAT BROWSE BUTTON
label_filepath = tk.Label(root, text="File Path:", fg=fg_color, bg=bg_color, font=custom_font)
label_filepath.pack()

entry_filepath = tk.Entry(root, bg=entry_bg_color, fg=entry_fg_color, font=custom_font)
# entry_filepath.pack(fill=tk.X)

# file dialog / browse urdf file

from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# entry_filepath = tk.Entry(root, bg=entry_bg_color, fg=entry_fg_color, font=custom_font)
# entry_filepath.pack(fill=tk.X)
# entry_filepath.grid(row=2, column=2)

def browsefunc():
    filename =fd.askopenfilename(filetypes=(("urdf xacro files","*.xacro"), ("urdf files","*.urdf"), ("All files","*.*")))
    rel_filepath = os.path.relpath(filename, os.getcwd()) 
    entry_filepath.insert(tk.END, rel_filepath) # add this

entry_filepath_button = tk.Button(root, text="select_file", command=browsefunc, fg=fg_color, bg=bg_color, font=custom_font)
# entry_filepath_button.grid(row=2, column=8)

entry_filepath.pack(fill=tk.X)
entry_filepath_button.pack()

urdf_file_path = entry_filepath.get()
print(urdf_file_path)

# Radio Buttons for Gazebo Type
label_gazebo = tk.Label(root, text="Simulator of Choice:", fg=fg_color, bg=bg_color, font=custom_font)
label_gazebo.pack()

radio_var = tk.StringVar()
radio_var.set("Ignition Gazebo")  # Default selection

radio1 = tk.Radiobutton(root, text="Ignition Gazebo", variable=radio_var, value="Ignition Gazebo",
                        fg=fg_color, bg=bg_color, font=custom_font, selectcolor=bg_color)
radio1.pack()

radio2 = tk.Radiobutton(root, text="Gazebo Classic", variable=radio_var, value="Gazebo Classic",
                        fg=fg_color, bg=bg_color, font=custom_font, selectcolor=bg_color)
radio2.pack()

# Radio Buttons for Joint State Publisher

label_jsp = tk.Label(root, text="Launch Joint State Publisher GUI to test your joints?", fg=fg_color, bg=bg_color, font=custom_font)
label_jsp.pack()

radio_jsp = tk.StringVar()
radio_jsp.set("YES")  # Default selection

radio1 = tk.Radiobutton(root, text="YES", variable=radio_jsp, value="YES",
                        fg=fg_color, bg=bg_color, font=custom_font, selectcolor=bg_color)
radio1.pack()

radio2 = tk.Radiobutton(root, text="NO", variable=radio_jsp, value="NO",
                        fg=fg_color, bg=bg_color, font=custom_font, selectcolor=bg_color)
radio2.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=get_inputs, fg=fg_color, bg=bg_color, font=custom_font)
submit_button.pack()

# Bind the window resize event to the function
# root.bind("<Configure>", on_window_resize)

# Start the main loop
root.mainloop()
