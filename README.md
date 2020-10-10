# Deepracer_Simulation for Deep Learning
In this project I utilised [aws-robomaker-sample-application-deepracer](https://github.com/amazon-archives/aws-robomaker-sample-application-deepracer) repository to train and deploy the deep learning model in the simulated environment locally. Aws-robomaker-sample-application-deepracer repository was only used to utilize tracks  and car model as a platform to perform ML tasks. This package provides a car with a front facing camera and vehicle control(steering and acceleration) through four wheel. Because this package provides the simulation environment in gazebo, it alot easier to aquire data using ROSbag. Generally the above package is created to train Reinforcement Learning model on AWS platform (online), but in this I only used car model and gazebo race-tracks for to train and deploy locally.<br />

#### Requirements
* ROS Kinetic/Melodic
* Gazebo

<br /> 
While setting up the [repository](https://github.com/amazon-archives/aws-robomaker-sample-application-deepracer), we do not require few steps as we are not training our model on AWS <br /> 

#### Only step to follow
* [Building the sumulation Bundle](https://github.com/amazon-archives/aws-robomaker-sample-application-deepracer#building-the-simulation-bundle)
* [Running the Simulation](https://github.com/amazon-archives/aws-robomaker-sample-application-deepracer#running-the-simulation-1) <br />
#### Tasks performed: <br />
* Data Collection (Playing car using keyboard manually)
* Data Extraction (Image and corresponding Labels from collected data)
* Train
* Deploy

This repository deals with lateral control of vehicle Using DNN. <br />

NN model Details:
![Screenshot](docs/screenshot.png)

