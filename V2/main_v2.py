#!/usr/bin/env python2
import rospy
import time
import rosbag
from PIL import Image
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from ackermann_msgs.msg import AckermannDriveStamped
from gazebo_msgs.msg import ModelState
import sys, select, termios, tty
from sensor_msgs.msg import Image as sensor_image
import numpy as np
import time
import matplotlib.pyplot as plt
from skimage import color,io

from keras.models import Sequential
from keras.layers import Cropping2D, Lambda, Dropout, ELU
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import load_model
import keras
import numpy as np
import tensorflow as tf
import os
import signal
from time import sleep
import keyboard
from pynput.keyboard import Listener
from pynput import keyboard
import logging


xx=1
moveBindings = {
        'i':(1,0,0,0), #acc
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
	'k':(-1,0,0,-1),
	'u':(1,0,0,1),
	'b':(0,0,-1,0),
	't':(0,0,1,0),
	'f':(-1,-1,-1,-1)
    }
button=True

def getKey():

	# def on_press(key):  # The function that's called when a key is pressed
	# 	print('pressed')
	# 	print(key)

	# def on_release(key):  # The function that's called when a key is released
	# 	print('released')
	# 	print(key)
		

	# with Listener(on_press=on_press, on_release=on_release) as listener:  # Create an instance of Listener

	# 	if button==False:
	# 		key='f'
	# 	else:
	# 		# print(keyboard.is_pressed('i'))
	# 		tty.setraw(sys.stdin.fileno())
	# 		key = sys.stdin.readline(1)
	# 		select.select([sys.stdin], [], [], 0)
	# 		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)




	def on_press(key):
		try:
			# print('pressed')
			# print('{0}'.format(key.char))
			if '{0}'.format(key.char)==str(u'i'):
				############### acceleration ########
				print('bhaago')

			if '{0}'.format(key.char)==str(u'j'):
				############### left ################
				print('baii taraf jao')


			if '{0}'.format(key.char)==str(u'l'):
				############### right ################
				print('dai taraf jao')


			if '{0}'.format(key.char)==str(u'k'):
				############### break ################
				print('bhosdike ruk')

		except AttributeError:
			# print(str({0}.format(key)))
			print('no')

	def on_release(key):

		if '{0}'.format(key)==str(key+str(key)):
		# print('released')
		print('{0}'.format(key))

		# print(str({0}.format(key)))


		if key == keyboard.Key.esc:
		# Stop listener
			return False

	with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
		listener.join()

		# ...or, in a non-blocking fashion:
		listener = keyboard.Listener(on_press=on_press,on_release=on_release)
		listener.start()


	# print(keyboard.is_pressed('i'))
	tty.setraw(sys.stdin.fileno())
	key = sys.stdin.readline(1)
	select.select([sys.stdin], [], [], 0)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	


	return key



def run():
	global ack_publisher,k,xx,flg
	ack_publisher = rospy.Publisher('/vesc/low_level/ackermann_cmd_mux/output',AckermannDriveStamped, queue_size=100)
	state_pub=rospy.Publisher('/gazebo/set_model_state',ModelState, queue_size=100)
	if flg==0:
		modelState.model_name='racecar'
		modelState.pose.position.z = 0
		modelState.pose.position.x = 5
		modelState.pose.position.y = 2
		ack_msg.drive.steering_angle=0
		time.sleep(2)
		state_pub.publish(modelState)
		ack_publisher.publish(ack_msg)
		flg=1
	while(1):		
		key=getKey()
		ct=5
		if moveBindings[key][0]==1:
			ack_msg.drive.speed = 0.5
		if moveBindings[key][3]==1:
			if ack_msg.drive.steering_angle>0.64:
				ack_msg.drive.steering_angle=ack_msg.drive.steering_angle
			else:	 
				ack_msg.drive.steering_angle =ack_msg.drive.steering_angle+0.08
		if moveBindings[key][3]==-1:
			if ack_msg.drive.steering_angle<-0.64:
				ack_msg.drive.steering_angle=ack_msg.drive.steering_angle
			else:		 
				ack_msg.drive.steering_angle =ack_msg.drive.steering_angle-0.08
		
		if moveBindings[key][3]==-1 and moveBindings[key][0]==-1:

			ack_msg.drive.speed = 0
		
		if moveBindings[key][2]==-1 and moveBindings[key][0]==0:
			ack_msg.drive.steering_angle=0
		
		if moveBindings[key][0]==-1 and moveBindings[key][1]==-1 and moveBindings[key][2]==-1 and moveBindings[key][3]==-1:
			print('xxxxxxxxxxxxxxxxx')
		


		ack_publisher.publish(ack_msg)
		
		if (moveBindings[key][3]==1 and moveBindings[key][0]==1) or xx==0:
			rospy.Subscriber('/camera/zed/rgb/image_rect_color', sensor_image, callback_image)
			xx=0


	

if __name__ == '__main__':
	try:
		flg=0
		settings = termios.tcgetattr(sys.stdin)
		rospy.init_node('manc', anonymous=True)	
		ack_msg = AckermannDriveStamped()
		modelState = ModelState()	
		run()

	except rospy.ROSInterruptException:
		pass
