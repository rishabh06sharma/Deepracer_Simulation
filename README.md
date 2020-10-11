# Deepracer_Simulation using Deep Learning
In this project we utilised [aws-robomaker-sample-application-deepracer](https://github.com/amazon-archives/aws-robomaker-sample-application-deepracer) repository to train and deploy the deep learning model in the simulated environment locally. Aws-robomaker-sample-application-deepracer repository was only used to utilize tracks  and car model as a platform to perform ML tasks. This package provides a car with a front facing camera and vehicle control(steering and acceleration) through four wheel. Because this package provides the simulation environment in gazebo, it alot easier to aquire data using ROSbag. Generally the above package is created to train Reinforcement Learning model on AWS platform (online), but in this we only used car model and gazebo race-tracks for to train and deploy locally.<br />

![](https://github.com/rs278/Deepracer_Simulation/blob/master/Docs/giff.gif)

#### Requirements
* ROS Kinetic/Melodic
* Gazebo
* Tensorflow
 
While setting up the [repository](https://github.com/amazon-archives/aws-robomaker-sample-application-deepracer), we do not require few steps as we are not training our model on AWS <br /> 

#### Setting up repository (Steps required)
* [Building the sumulation Bundle](https://github.com/amazon-archives/aws-robomaker-sample-application-deepracer#building-the-simulation-bundle)
* [Colcon Install](https://github.com/amazon-archives/aws-robomaker-sample-application-deepracer#using-this-sample-with-aws-robomaker) <br />

To launch track (hard_track, medium_track and easy_track) in Gazebo, you can run following line in a terminal
```python
roslaunch deepracer_simulation racetrack_with_racecar.launch world_name:=easy_track gui:=true
```
#### Easy track
<img src="https://github.com/rs278/Deepracer_Simulation/blob/master/Docs/easy.png" width="600" height="400">

#### Medium track
<img src="https://github.com/rs278/Deepracer_Simulation/blob/master/Docs/medium.png" width="600" height="400">

#### Hard Track
<img src="https://github.com/rs278/Deepracer_Simulation/blob/master/Docs/hard.png" width="600" height="400">

#### Tasks performed: <br />
* Data Collection (Playing car using keyboard manually)
* Data Extraction (Image and corresponding Labels from collected data)
* Train
* Deploy

This repository only deals with lateral control of vehicle Using DNN. <br />

#### NN model Details:  <br />
[NVIDIA Research paper](https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf) <br />
<img src="https://github.com/rs278/Deepracer_Simulation/blob/master/Docs/model.png" width="450" height="580">

To collect data while running the car we used keyboard to give acceleration and steerign commands. We utilised the following function and static movebindings to do so.

```python
import sys, select, termios, tty
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
```
This data is further collected by running ROSbag command in seprate terminal simultaneously. To run car uing keyboard or to deploy the model run main.py in seprate terminal.

#### Files Description
main.py: Keyboard and Computer interface <br />
main.py: model deployment <br />
train.ipynb: train model <br />
extract_bag.py: data extraction <br />
distace_from_centre.py: Analyse <br />
