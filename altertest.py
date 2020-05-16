import rosbag
#from PIL import Image
import numpy as np
import time
from cv_bridge import CvBridge, CvBridgeError
import os.path
#bag1 = rosbag.Bag('2020-04-15-01-19-42.bag')
bag1=rosbag.Bag('hardclock.bag')
train=np.array([])
lim=[]
test=[]
i=0
for a,b,c in bag1:
    bridge = CvBridge()
    #print(a)

    if(a=='/camera/zed/rgb/image_rect_color'):

        frame = bridge.imgmsg_to_cv2(b, "bgr8")
#        img = Image.fromarray(frame,'RGB')
        #newsize = (160,120)
#        im1 = img.resize(newsize)
        lim.append(frame)
    elif(a=='/vesc/low_level/ackermann_cmd_mux/output'):
        i+=1
        print(i)
        steer=b.drive.steering_angle
        try:
            img = lim[0]
        except:
            continue
        #print(img.shape)
        try:
            train = np.vstack((train, np.array([img])))
            test = np.vstack((test, np.array([steer])))
        except:
            train=np.array([img])
            test = np.array([steer])
        #print(train.shape)
        # print(train)
        #test.append(steer)
        #flush list of images
        lim=[]
        if(i==10000):
            break


# train=np.array(train)
# test=np.array(test)
#
print(img.shape)
print(train.shape)
print(test.shape)



bag1.close()

np.savez_compressed('/tmp/hardclockv1',a=train,b=test)
