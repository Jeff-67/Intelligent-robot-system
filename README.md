# Using-CNN-for-real-time-object-detection-on-Jetson-TX2-with-Intel-realsense-camera
> [Abstract](#abstract)

> [System flowchart](#system-flowchart)

> [Techniques](#techniques)

  - Real-time object detection by CNN
  
  - Deploy model on Jetson TX2 and intel real-sense 3D camera 
  
  - Robotics
  
  - Cloud monitoring and cloud-based product resume
  
> [Highlights](#highlights)

# Abstract
This project is an automatic intelligent robot system providing argicultural and industrial solution. Our pupose is to integrate the processes from fruit cleaning to sales, including picking up from the water, drying, packing and marking. We achieve the goal through deep learning computer vision and improve the entire process by cloud monitoring.

Here is a peak of what we do:

## Entire process:

![ezgif com-video-to-gif](https://user-images.githubusercontent.com/36265245/49698794-a2216880-fc03-11e8-964f-df079c1723ab.gif)

## Special features:

| <a>**Compare all the mangos and choose the beautiful one**</a> | <a>**Observe the situation and deal with the problem if mangos are too closed**</a> | 
| :---: |:---:| 
|![ezgif com-video-to-gif 1](https://user-images.githubusercontent.com/36265245/49698920-566fbe80-fc05-11e8-9ae2-163b56ff0d35.gif) | ![ezgif com-crop](https://user-images.githubusercontent.com/36265245/49698979-21b03700-fc06-11e8-9a46-57dfa2ef61b4.gif) | 

# System flowchart

- Environment: 

  Many mangoes float freely in the water.

- Object detection: 

  Real-time pixel information will transmitted from Intel realsense depth camera to Jetson TX2 processor and the 3D object coordinates will be transmitted to the robot arm controller and gripping situation will also be recognized by deep leaning algorithm.

- Fruit gripping: 

  SCARA robot arm will receive position information and from the processor and send compressor pressure information to control pneumatic gripper than the fruit in water will be gripped out.

- Air-drying machine: 

  The arm will move to the air-drying area and stays. The arm gripped with the fruit will rotates in r axes so that the high-pressure air released by the air compressor could blown water droplets away. After all, the fruit will be placed neatly in the box.

- Air-powered Platform and Laser Marking machine: 

  Air-powered Platform moves the box to the marking area. Through the laser marking machine, two-dimensional QRcode of the production resume is printed on the box. After scanning, it can be linked to the cloud data.

- Cloud monitoring: 

  During the operation of this system, the whole process can be monitored by cloud API. If the box on the air-powered platform is interupted by improper external force, the operation of arm marking and laser marking will be stopped immediately to avoid danger.
  
![screen shot 2018-12-10 at 10 57 59 pm](https://user-images.githubusercontent.com/36265245/49740423-1c6aef00-fccf-11e8-822b-717e67e4fbe7.png)

# Techniques

## Real-time object detection by CNN

- Environment setting

- Getting Raw Data

- Data Preprocessing & Features Extraction

- Training Model

- Test Data, improve model 

## Deploy model on Jetson TX2 and intel real-sense RGBD camera

- Running on jetson TX2

- mapping to world coordinates(X,Y,Z)

## Robotics 

## Cloud supervising
     
# Highlights
