#!/usr/bin/env python

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




# def callback_progress(self, data):

# self.distance_from_border_2 = data.distance_from_border_2 
# rospy.Subscriber('/progress', Progress, self.callback_progress)


session = tf.Session()
keras.backend.set_session(session)

xx=1
def build_model(og_img_shape):

    model = Sequential()

    model.add(Lambda(lambda x: x / 127.5 - 1.0, input_shape = og_img_shape))

    model.add(Conv2D(24, (5,5), strides=(2, 2), padding='same', activation='elu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='valid'))

    model.add(Conv2D(36, (5,5), strides=(2, 2), padding='same', activation='elu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='valid'))

    model.add(Conv2D(48, (5,5), strides=(2, 2), padding='same', activation='elu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='valid'))

    model.add(Conv2D(64, (3,3), strides=(1, 1), padding='valid', activation='elu'))

    model.add(Conv2D(64, (3,3), strides=(1, 1), padding='valid', activation='elu'))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(100, activation = 'elu'))
    model.add(Dense(50, activation = 'elu'))
    model.add(Dense(10, activation = 'elu'))
    model.add(Dense(1))

    model.summary()

    return model

model2 = build_model((480, 640,3))
model2.load_weights('deepracer_weights_hardtrackv2_7epochs.h5')
model2.compile(loss='mean_squared_error',optimizer='adam')



moveBindings = {
        'i':(1,0,0,0), #acc
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
	'k':(-1,0,0,-1),
	'u':(1,0,0,1),
	'b':(0,0,-1,0),
	't':(0,0,1,0)
    }

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

#abc=np.load('test_rgb.npz')['a']
k=0
def callback_image(data):
	global k,xx
	image = Image.frombytes('RGB', (data.width, data.height),data.data,'raw', 'BGR', 0, 1)
	img=np.array(image)
	#if k in [5,10,15,20,25]:
	#	np.savez_compressed('temp_{0}'.format(k),a=img)
		#img=color.rgb2gray(img)
		#io.imshow(img, cmap=plt.cm.gray)
	
		#print(np.shape(img))
        	#plt.show()
		#time.sleep(2)
	#k=k+1
	#img=color.rgb2gray(img)
	#print(img.sum())
	#plt.pause(0.01)
	#print(img.sum())
	#key=getKey()
	#if (moveBindings[key][3]==1 and moveBindings[key][0]==1):
	#	xx=1
		
	
	with session.as_default():
            with session.graph.as_default():	
	        keras.backend.set_session(session)
	        #output=model2.predict(abc[k,:,:,:].reshape(-1, 480, 640,3))
		#print(np.shape(img))
		output=model2.predict(img.reshape(-1, 480, 640,3))
	print(output)	
	ack_msg.drive.steering_angle=output[0][0]
	ack_msg.drive.speed = 0.5
	ack_publisher.publish(ack_msg)
	

def run():
	global ack_publisher,k,xx,flg
	ack_publisher = rospy.Publisher('/vesc/low_level/ackermann_cmd_mux/output',AckermannDriveStamped, queue_size=100)
	state_pub=rospy.Publisher('/gazebo/set_model_state',ModelState, queue_size=100)
	if flg==0:
            modelState.model_name='racecar'
	    modelState.pose.position.z = 0
	    modelState.pose.position.x = 5
	    modelState.pose.position.y = 2
	    time.sleep(2)
	    state_pub.publish(modelState)
	    flg=1
	ack_msg.drive.steering_angle=0
	while(1):		
		key=getKey()
		ct=5
		print(ack_msg.drive.steering_angle)
		if moveBindings[key][0]==1:
#				ack_publisher.drive.speed.publish(5)
#			if ack_msg.drive.steering_angle>0.5:
#				ack_msg.drive.speed=ack_msg.drive.speed
#			else:	 
#				ack_msg.drive.speed =ack_msg.drive.speed+0.08
			ack_msg.drive.speed = 0.5
#				pub_vel_left_rear_wheel.publish(5)
#				pub_vel_right_rear_wheel.publish(5)
#				pub_vel_left_front_wheel.publish(5)
#				pub_vel_right_front_wheel.publish(5)
		if moveBindings[key][3]==1:
			if ack_msg.drive.steering_angle>0.64:
				ack_msg.drive.steering_angle=ack_msg.drive.steering_angle
			else:	 
				ack_msg.drive.steering_angle =ack_msg.drive.steering_angle+0.08
#				ack_publisher.drive.steering_angle.publish(-1)
#				pub_pos_left_steering_hinge.publish(0.3)
#				pub_pos_right_steering_hinge.publish(0.3)
		if moveBindings[key][3]==-1:
			if ack_msg.drive.steering_angle<-0.64:
				ack_msg.drive.steering_angle=ack_msg.drive.steering_angle
			else:
#				ack_publisher.header.stamp = rospy.Time.now()
#				ack_publisher.drive.steering_angle.publish(1)		 
				ack_msg.drive.steering_angle =ack_msg.drive.steering_angle-0.08
#				pub_pos_left_steering_hinge.publish(-0.3)
#				pub_pos_right_steering_hinge.publish(-0.3)
		
		if moveBindings[key][3]==-1 and moveBindings[key][0]==-1:
#			if ack_msg.drive.steering_angle<=0:
#				ack_msg.drive.speed=ack_msg.drive.speed
#			else:	 
#				ack_msg.drive.speed =ack_msg.drive.speed-0.08

			ack_msg.drive.speed = 0
		
		if moveBindings[key][2]==-1 and moveBindings[key][0]==0:
			ack_msg.drive.steering_angle=0
		


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
