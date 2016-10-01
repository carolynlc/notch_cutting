import cv2
import Tkinter
from Tkinter import *
import rospy, pickle, time
from geometry_msgs.msg import Pose
import multiprocessing
import numpy as np
import sys
from robot import *
import tfx

"""
This script contains functions and a GUI used for collecting points in robot frame (for PSM1). It dumps points to calibration_data/psm1_calibration.
"""

def exitCallback(fpsm1, psm1_pts):
    with open(fpsm1, "w+") as f:
        pickle.dump(psm1_pts, f)
    sys.exit()

def psm1_callback(psm1_pts, psm1):
    print list(psm1.get_current_cartesian_position().position)
    psm1_pts.append(list(psm1.get_current_cartesian_position().position))

def record(fpsm1):
    open(fpsm1, 'w+').close()
    psm1 = robot("PSM1")
    top = Tkinter.Tk()
    top.title('Calibration')
    top.geometry('400x200')
    psm1_pts = []
    B = Tkinter.Button(top, text="Record PSM1 Position", command = lambda: psm1_callback(psm1_pts, psm1))
    D = Tkinter.Button(top, text="Exit", command = lambda: exitCallback(fpsm1, psm1_pts))
    [a.pack() for a in B, D]
    top.mainloop()

if __name__ == '__main__':
    fpsm1 = 'experiment_data/psm1.p'
    open(fpsm1, 'w+').close()
    psm1 = robot("PSM1")
    top = Tkinter.Tk()
    top.title('Calibration')
    top.geometry('400x200')
    psm1_pts = []
    B = Tkinter.Button(top, text="Record PSM1 Position", command = lambda: psm1_callback(psm1_pts, psm1))
    D = Tkinter.Button(top, text="Exit", command = lambda: exitCallback(fpsm1, psm1_pts))
    [a.pack() for a in B, D]
    top.mainloop()
