import tkinter as tk
from tkinter import ttk
import rospy
from std_msgs.msg import Int16

"""
Simple Python subscriber to a ROS topic (/front_angle_low_res) which in my case is outputing an integer result 
and displays the result in a tkinter window

credit: https://www.pythontutorial.net/tkinter/tkinter-after/
credit: https://www.youtube.com/watch?v=EAAd5vXA8lE&t=260s

before running make sure to $ rostopic echo /front_angle_low_res to make sure data is available
This script can be started from the folder it resides in with $ python3 sensor_display.py

"""

TOPIC_TO_DISPLAY = "/front_angle_low_res"

class Display_Sensor_1(tk.Tk):

    def __init__(self):
        super().__init__()
        self.sub = rospy.Subscriber(TOPIC_TO_DISPLAY, Int16, self.callback_sensor_1)
        self.sensor_1_data = tk.IntVar()

        # configure the root window
        self.title('Sensor 1 Data')
        self.resizable(0, 0)
        self.geometry('250x80')
        self['bg'] = 'black'
        
        # change the background color to black
        self.style = ttk.Style(self)
        self.style.configure('TLabel', background='black', foreground='red')
        self.label = ttk.Label(self, text=self.get_sensor_data(), font=('Digital-7', 20))
        self.label.pack(expand=True)
        self.label.after(1000, self.update)     # schedule an update every 1 second

    def callback_sensor_1(self, data):   
        self.sensor_1_data = data.data
        #print(self.sensor_1_data)
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    def get_sensor_data(self):
        return self.sensor_1_data

    def update(self):
        """ update the label every 1 second """
        self.label.configure(text=self.get_sensor_data())
        self.label.after(1000, self.update)     # schedule another timer
 
if __name__ == "__main__":
    rospy.init_node('listener', anonymous=True)
    sensor = Display_Sensor_1()
    sensor.mainloop()