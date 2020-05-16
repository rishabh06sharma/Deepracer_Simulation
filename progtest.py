#!/usr/bin/env python
# license removed for brevity

from __future__ import print_function
import rospy
import time
import os
import rospy
import time
import rosbag
from PIL import Image
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from ackermann_msgs.msg import AckermannDriveStamped
import sys, select, termios, tty
from sensor_msgs.msg import Image as sensor_image
import numpy as np


SIMULATION_WORKER = "SIMULATION_WORKER"
SAGEMAKER_TRAINING_WORKER = "SAGEMAKER_TRAINING_WORKER"

node_type = os.environ.get("NODE_TYPE", SIMULATION_WORKER)



moveBindings = {
	'r':(-1,0,0,-1),
    }

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if node_type == SIMULATION_WORKER:
    import rospy
    from ackermann_msgs.msg import AckermannDriveStamped
    from gazebo_msgs.msg import ModelState
    from gazebo_msgs.srv import SetModelState
    from sensor_msgs.msg import Image as sensor_image
    from deepracer_msgs.msg import Progress
    #print("success")

def callback(data):
    global flg,record
    print(data.distance_from_center,"\n")
    if flg==1:
        record.append(data.distance_from_center)

def main():
    global flg,record
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    
    rospy.init_node('listener', anonymous=True)
    while(1):
	    key=getKey()
	    if moveBindings[key][3]==-1 and moveBindings[key][0]==-1:
		if flg==0:
		    flg=1
		elif flg==1:
		    flg=0
		    record=np.array(record)
		    np.savez_compressed('record',a=record)
		    #print('done')

	    rospy.Subscriber("/progress", Progress, callback)




    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

if __name__ == '__main__':
    
    try:
	record=[]
	flg=0
	settings = termios.tcgetattr(sys.stdin)	
	main()
	
    except rospy.ROSInterruptException:
        pass
