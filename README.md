# Deepracer_Simulation for Deep Learning
In this project I utilised [aws-robomaker-sample-application-deepracer](https://github.com/amazon-archives/aws-robomaker-sample-application-deepracer) repository to train and deploy the deep learning model in the simulated environment locally. Aws-robomaker-sample-application-deepracer repository was only used to utilize tracks  and car model as a platform to perform ML tasks. This package provides a car with a front facing camera and vehicle control(steering and acceleration) through four wheel. Because this package provides the simulation environment in gazebo, it alot easier to aquire data using ROSbag. Generally the above package is created to train Reinforcement Learning model on AWS platform (online), but in this I only used car model and gazebo race-tracks for to train and deploy locally.<br />

#### Tasks performed: <br />
* Data Collection (Playing car using keyboard manually)
* Data Extraction (Image and corresponding Labels from collected data)
* Train
* Deploy



