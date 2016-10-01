import numpy as np
import sys, os, pickle, time
from simulation import *
# from tensioner import *
from shapecloth import *
# from davinci_interface.interface import * # COMMENT BACK IN
import IPython
import os.path as osp
# from simulation_policy import *
from registration import *
from notch_finder import *
from mouse import *
# from endoscope.image_utils.blob_tracker import *


"""
This file contains a script that takes a trajectory and executes it on the DVRK.
"""

if __name__ == '__main__':

    ##================================================================================
    ## Load points after recording them using pose_recorder.py in davinci_interface
    ##================================================================================

    experiment_directory = "experiment_data"
    pts_file = osp.join(experiment_directory, "psm1.p")

    d = pickle.load(open(pts_file, "rb"))
    corners = [d[1], d[2], d[0], d[3]]
    points = d[4:]
    
    ##================================================================================
    ## Visualize trajectory before executing it
    ##================================================================================

    mouse = Mouse(down=True, button=0)
    armOrientation = "right"
    shape_fn = get_shape_fn(corners, points, True)
    cloth = ShapeCloth(shape_fn, mouse, width=50, height=50, dx=10, dy=10)
    trajectory = get_trajectory(corners, points, True)
    
    # Find the notch points and segments to complete the trajectory
    npf = NotchPointFinder(cloth, trajectory, [])
    npf.find_pts(armOrientation)
    segments, indices = npf.find_segments(armOrientation)


    # Visualize the trajectory
    for i in range(10):
        cloth.update()
        if i % 10 == 0:
            print "Iteration", i
    fig = plt.figure()
    plt.hold(True)
    plot = fig.add_subplot(111)
    plt.clf()
    pts = np.array([[p.x, p.y] for p in cloth.normalpts])
    cpts = np.array([[p.x, p.y] for p in cloth.shapepts])
    if len(pts) > 0:
        plt.scatter(pts[:,0], pts[:,1], c='w')
    if len(cpts) > 0:
        plt.scatter(cpts[:,0], cpts[:,1], c='b')
    plt.draw()
    plt.waitforbuttonpress()

    # Visualize the mins and maxes
    minpts = np.array(npf.min_pts)
    maxpts = np.array(npf.max_pts)
    if len(minpts) > 0:
        plt.scatter(minpts[:,0], minpts[:,1], c='g', marker='s', edgecolors='none', s=80)
    if len(maxpts) > 0:
        plt.scatter(maxpts[:,0], maxpts[:,1], c='r', marker='s', edgecolors='none', s=80)
    plt.draw()
    plt.waitforbuttonpress()

    # Visualize the segments in different colors
    numSegs = len(npf.segments)
    color = iter(plt.cm.jet(np.linspace(0, 1, numSegs)))
    for i in range(numSegs):
        segpts = np.array(npf.segments[i])
        c = next(color)
        # for j in range(len(segpts[:,0])):
        #     plt.scatter(segpts[j, 0], segpts[j, 1], c=c, marker='o', edgecolors='none', s=20)
        #     plt.draw()
        #     plt.waitforbuttonpress()
        plt.scatter(segpts[:,0], segpts[:,1], c=c, marker='o', edgecolors='none', s=20)
    plt.draw()
    plt.waitforbuttonpress()

    ##================================================================================
    ## Find the trajectory in terms of the 3D points using indices
    ##================================================================================

    trajectory = np.array(get_robot_trajectory(points))
    lst = []
    i = 0
    for seg in indices:
        for elem in seg:
            lst.append(np.array(trajectory[elem]).tolist())
        i += 1
    trajectory = lst
    trajlen = len(trajectory)

    # grippers = GripperArm("PSM2", policy)
    scissors = ScissorArm("PSM1", trajectory, [])

    # pt = [280, 480]
    # grab_point = px_to_robot(pt, corners_file, pts_file)

    for i in range(trajlen):
        scissors.step()

