# Using-CNN-for-real-time-object-detection-on-Jetson-TX2-with-Intel-realsense-camera
> [Abstract](#abstract)

> [System flowchart](#system-flowchart)

> [Techniques](#techniques)

  - [Real-time object detection by CNN](#real-time-object-detection-by-CNN)
  
  - Deploy model on Jetson TX2 and intel real-sense 3D camera 
  
  - Robotics
  
  - Cloud monitoring and cloud-based product resume
  
> [Highlights](#highlights)

# Abstract
This project is an automatic intelligent robot system providing argicultural and industrial solution. Our pupose is to integrate the processes from fruit cleaning to sales, including picking up from the water, drying, packing and marking. We achieve the goal through deep learning computer vision and improve the entire process by cloud monitoring.

Here is a peak of what we do:

## Entire process:

| <a></a> | <a></a> | 
| :---: |:---:| 
![ezgif com-video-to-gif](https://user-images.githubusercontent.com/36265245/49698794-a2216880-fc03-11e8-964f-df079c1723ab.gif)|![screen shot 2018-12-12 at 12 13 15 am](https://user-images.githubusercontent.com/36265245/49813669-e5660d80-fda2-11e8-80fa-3f5eae3f667e.png)

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

  SCARA robot arm will receive position information from the processor and send compressor pressure information to control pneumatic gripper and than the fruit in water will be gripped out.

- Air-drying machine: 

  The arm will move to the air-drying area and stays. The arm gripped with the fruit will rotates in r axes so that the high-pressure air released by the air compressor could blown water droplets away. After all, the fruit will be placed neatly in the box.

- Air-powered Platform and Laser Marking machine: 

  Air-powered Platform moves the box to the marking area. Through the laser marking machine, two-dimensional QRcode of the production resume is printed on the box. After scanning, it can be linked to the cloud data.

- Cloud monitoring: 

  During the operation of this system, the whole process can be monitored by cloud API. If the box on the air-powered platform is interupted by improper external force, the operation of arm marking and laser marking will be stopped immediately to avoid danger.
  
     ![screen shot 2018-12-10 at 10 57 59 pm](https://user-images.githubusercontent.com/36265245/49740423-1c6aef00-fccf-11e8-822b-717e67e4fbe7.png)

# Techniques

## Real time object detection by CNN

- Environment setting:

  There are many algorithms and frameworks using for object detection, in this project I will build our own object detection system on Yolov3-tiny. Reasons are followed: Simply because it is stronger, better and faster.
  YOLOv3 feature extractor is a residual model, because it contains 53 convolution layers, so it is called Darknet-53. From the network structure, compared with Darknet-19 network, it uses residual units, so it can be built deeper. Another point is to use FPN architecture (Feature Pyramid Networks for Object Detection) to achieve multi-scale detection. YOLOv3 uses three scale feature maps (when the input is 416 times13), (26 times26), (52\ times52). The picture below shows that the Yolov3 out-compete others in speed. 
  
  ![screen shot 2018-12-11 at 6 27 40 pm](https://user-images.githubusercontent.com/36265245/49794917-ad93a180-fd73-11e8-8377-8f23830a5aa5.png)

  > Environment:
  
  Opencv 3.4.0
  
  Python 2.7
  
  Cuda 9.0
  
  cudnn 7
  
  GPU:Nvidia GTX 1080TI 
  
  > Installing Yolov3
  ```shell
  $ cd
  $ git clone https://github.com/pjreddie/darknet darknet
  $ cd darknet
  $ vim Makefile
  ```
  (Note: The line in ‘ARCH’ means the compute power of the GPU,mine gpu is 61 )
  
  ```C
  GPU=1
  CUDNN=1
  OPENCV=1
  OPENMP=0
  DEBUG=0

  ARCH= -gencode arch=compute_62,code=[sm_62,compute_62]
  ```
  ```shell
  $ make
  ```
- Getting Raw Data, Data Augmentation & Data Preprocessing

  Get about 4000 images of various mangoes from IMAGENET and 4000 images from photography. Besides, so as to obtain more feature photo data, data augmentation is carried out to simulate various situations in water by rotating the fruit photos horizontally and vertically. Furthermore, before entering the training of deep learning algorithm, we must pre-process and regularize the huge amount of data, classify all data in the first step, and adjust them to the same pixels and size.
  
  | <a>**Getting bid data from IMAGNET**</a> | <a>**Photograpghy**</a> | 
  | :--------: |:---:| 
  |![screen shot 2018-12-11 at 8 34 17 pm](https://user-images.githubusercontent.com/36265245/49802064-d83b2580-fd86-11e8-857f-8241ecea5a84.png)| ![1_color](https://user-images.githubusercontent.com/36265245/49801600-9493ec00-fd85-11e8-9e8b-9ac6c33f3c5e.png)|
  
- Labeling
  
  A great labeling could have a profound effect on predicting the width and height of the box as offsets from cluster centroids. Fig.1 shows how Yolov3 predict the center coordinates of the box relative to the location of filter application using a sigmoid function.
  In order to operating a great label process, I use the efficient labeling tool yolo_mark to label all the pictures/data in 2 classes. Here is what I am doing:
  
  > Installing Yolo_mark
  
  ```shell
  $ git clone https://github.com/AlexeyAB/Yolo_mark
  $ cmake  .
  $ make
  $ sudo ./linux_mark
  ```
  (If you encounter some bugs like ‘sudo ./ command no found’,try this:
  
   ```shell
  $ chmod +x linux_mark.sh
  $ ./linux_mark.sh)
  ```
  If this application can compile properly, then it’s time to label our own data

  1.Clean all the images in ``x64/Release/data/img``
  
  2.Move all the training images data to ``x64/Release/data/img``
  
  (Note: The filename should be ``.jpeg``, not ``.JPEG``,we could change all the filename by this command ``$ rename -v s/jpeg/JPEG/ *jpeg``)
  
  3.Change the number of classes you want to train and label in ``obj.data``
  
  4.Change the names of your labels and classes in each line of ``obj.names``
  
  ```shell
  $ ./linux_mark
  ```

  (Note: Press the number on the keyboard you want to label and drag your mouse.For instance, if this one is classes 0, then press 0 and drag it, then it will create a file ``images_name.txt`` automatically which contains ``<object-class>`` ``<x>`` ``<y>`` ``<width>`` ``<height>``), just like the Fig.2 below.
   
  | <a>**Bounding boxes with dimension priors and location prediction.**</a> | <a>**Labeling**</a> 
  | :---: |:---:| 
  |![screen shot 2018-12-11 at 9 13 47 pm](https://user-images.githubusercontent.com/36265245/49803308-6664db00-fd8a-11e8-9ecb-8413a8942b34.png)   | ![screen shot 2018-12-11 at 9 07 47 pm](https://user-images.githubusercontent.com/36265245/49802792-e8540480-fd88-11e8-8ffa-d1180afa04e6.png)
  | <a>**Fig.1**</a> | <a>**Fig.2**</a> 

- Training and improving Model

  At first, the algorithm we used is Convolutional Neural Network (CNN). This learning method is a special kind of neural network structure, which includes several Convolutional Layers, Subsampling Layers, and Fully Connected Layer. In this training, we use multiple Convolutional Kernel (Convolutional Kernel) to convolute and extract features from a large number of previously collected and processed data, and enhance the mapping relationship between learning pictures and Target values through the hyper paramteter Epoch, BatchSize and the learning rate of back propagation in the training model. In addition, in order to achieve more efficient and immediate learning, the dimension of the image is reduced through the down-sampling layer (also known as pooling Layer), but feature is restored while dimension is reduced, thus it could accelerate the learning process. Finally, in the output full-connection layer, as in the general neural network, the non-linear transformation is done through the activation function after the product. We use the Rectified Linear Units (ReLUs) to make the training of convolutional neural network converge faster. The position information obtained by object detection is transmitted to the robot arm controller, and then the following arm automatic gripping will be carried out.
   
   This is our first model, but it wasn't precise and fast at all.
   
   ```python
   def model(images, n_last_channels=425):
    net = conv2d(images, 32, 3, 1, name="conv1")
    net = maxpool(net, name="pool1")
    net = conv2d(net, 64, 3, 1, name="conv2")
    net = maxpool(net, name="pool2")
    net = conv2d(net, 128, 3, 1, name="conv3_1")
    net = conv2d(net, 64, 1, name="conv3_2")
    net = conv2d(net, 128, 3, 1, name="conv3_3")
    net = maxpool(net, name="pool3")
    net = conv2d(net, 256, 3, 1, name="conv4_1")
    net = conv2d(net, 128, 1, name="conv4_2")
    net = conv2d(net, 256, 3, 1, name="conv4_3")
    net = maxpool(net, name="pool4")
    net = conv2d(net, 512, 3, 1, name="conv5_1")
    net = conv2d(net, 256, 1, name="conv5_2")
    net = conv2d(net, 512, 3, 1, name="conv5_3")
    net = conv2d(net, 256, 1, name="conv5_4")
    net = conv2d(net, 512, 3, 1, name="conv5_5")
    shortcut = net
    net = maxpool(net, name="pool5")
    net = conv2d(net, 1024, 3, 1, name="conv6_1")
    net = conv2d(net, 512, 1, name="conv6_2")
    net = conv2d(net, 1024, 3, 1, name="conv6_3")
    net = conv2d(net, 512, 1, name="conv6_4")
    net = conv2d(net, 1024, 3, 1, name="conv6_5")
    # ---------
    net = conv2d(net, 1024, 3, 1, name="conv7_1")
    net = conv2d(net, 1024, 3, 1, name="conv7_2")
    # shortcut
    shortcut = conv2d(shortcut, 64, 1, name="conv_shortcut")
    shortcut = reorg(shortcut, 2)
    net = tf.concat([shortcut, net], axis=-1)
    net = conv2d(net, 1024, 3, 1, name="conv8")
    # detection layer
    net = conv2d(net, n_last_channels, 1, batch_normalize=0,
                 activation=None, use_bias=True, name="conv_dec")
    return net
   ```
   
   In order to prevent over-fitting and boost the prediction accuracy, I choose Yolov3-tiny as the final model, and it really works incredibly well (Shown in Fig.3).
   The newer architecture (shown in Fig.4) boasts of residual skip connections, and upsampling. The most salient feature of Yolov3 is that it makes detections at three different scales, which are precisely given by downsampling the dimensions of the input image by 32, 16 and 8 respectively and is obviously better at detecting smaller objects.
  
  | <a>**Prediction of good and bad mangoes (with score)**</a> | <a>**Nerual network layers**</a> 
  | :---: |:---:| 
  |![screen shot 2018-12-09 at 2 00 21 pm](https://user-images.githubusercontent.com/36265245/49804936-de350480-fd8e-11e8-99f5-9c397e8c4745.png)|  ![screen shot 2018-12-11 at 9 48 17 pm](https://user-images.githubusercontent.com/36265245/49804805-839ba880-fd8e-11e8-9c57-52e120c73909.png)
  | <a>**Fig.3**</a> | <a>**Fig.4**</a> 
  
  Here is a peak of what I do:
  
  Copy ``yolov3-tiny_obj.cfg`` and rename it as ``yolov3-tiny-obj.cfg``. Then,began to tune the hyperparameter!!
  
  > Hyperparameter tunning:

  First change the numbers of classes to yours in the layer ``[yolo]``, then change the number of filter in the layer ``[convolutional]`` before the layer``[yolo]`` by this equation: 
  
  filters=(classes + 5)x3

  Then rewrite the context in ``obj.data`` to:
  
  ```C
  classes= #our number of object classes
  train  = data/train.txt
  valid  = data/test.txt
  names = data/obj.names
  backup = backup/
  ```
  > Download pre-trained weights:
  
  ```shell
  $ git clone  https://pjreddie.com/media/files/yolov3-tiny.weights
  $ ./darknet partial cfg/yolov3-tiny.cfg yolov3-tiny.weights yolov3-tiny.conv.15 15
  ```
  > Start Training:
  
  ```shell
  $./detector train data/obj.data yolov3-tiny-obj.cfg yolov3-tiny.conv.15
  ```
  (Note:the trained wieghts wiil be saved in the folder ``backup/``)
  (Note: we could use the command ``$ watch --color -n1 gpustat -cpu`` to monitor the gpu usage while training)
 

## Deploy model on Jetson TX2 and intel real-sense RGBD camera

- Running on jetson TX2

- mapping to world coordinates(X,Y,Z)

  > Installing Intle realsense SDK:
  
  ```shell
  $ git clone https://github.com/IntelRealSense/librealsense
  ```
  After downloaded you can plug your D400 series depth camera through type c connector and start you first application.

  > Get 3D World coordinates:

    Actually, there isn’t a direct examples that shows how to mapping coordinates, but we can get some clue from the examples ``rs-measure`` and ``rs-get_distance``.
 
    First, we can acquired the x,y coordinates from yolo, but how to get the corresponding z coordinates?

    From the few lines of codes in example ``librealsense/examples/C/distance/rs-distance.c`` we can get some hints:
    
    It includes some useful library first.
    ```C
    #include <librealsense2/rs.hpp>
    #include "example.hpp"
    ```
   
    The code below is opening the camera then start streaming and capture the frame simultaneously.But if you look closer, you will find out they call a function called rs2_depth_frame_get_distance,this seems like the camera measure the distance between the center of instantaneous frame and the camera. 
    
    ```C
    rs2::config cfg;
    rs2::pipeline pipe;
    rs2_config_enable_stream(config, STREAM, STREAM_INDEX, WIDTH, HEIGHT, FORMAT, FPS, &e);
    rs2::pipeline_profile prf = pipe.start(cfg);
    rs2::frameset frames = pipe.wait_for_frames();
    rs2::frame depth_frame = aligned_frames.get_depth_frame();
    rs2_frame* frame = rs2_extract_frame(frames, i, &e);
    if (0 == rs2_is_frame_extendable_to(frame, RS2_EXTENSION_DEPTH_FRAME, &e))
    continue;
    int width = rs2_get_frame_width(frame, &e);
    int height = rs2_get_frame_height(frame, &e);
    float dist_to_center = rs2_depth_frame_get_distance(frame, width / 2, height / 2, &e);
    ```
    Since we could modify the function to let we insert the arguments (x,y) to get the z coordinates as well as “distance”.

    ```C
    float x=atof(argv[1]);
    float y=atof(argv[2]);
    ```

    Unfortunately, the x.y coordinates is captured by color frame but the z coordinates is come from depth frames. In other words, the values aren’t really corresponding according to the distance between depth camera and RGB camera.

    In ``librealsense/examples/measure/rs-distance.cpp`` we could peak some solution:

    It includes the useful library first as well.
    
    ``#include <librealsense2/rsutil.h>``

    Then we configure camera pipeline for depth + color streaming
    
    ```C
    rs2::pipeline pipe;
    rs2::config cfg;
    cfg.enable_stream(RS2_STREAM_DEPTH); 
    cfg.enable_stream(RS2_STREAM_COLOR, RS2_FORMAT_RGBA8);
    auto profile = pipe.start(cfg);
    auto sensor = profile.get_device().first<rs2::depth_sensor>();
    ```
    The below is what we need, applying the align processing block to align color frame to depth viewport
    ```C
    rs2::align align_to(RS2_STREAM_DEPTH);
    data = align_to.process(data);
    auto colorized = color_map(depth);
    ```

    To convert pixels in the depth image into 3D points we are calling ``rs2_deproject_pixel_to_point`` function (declared in ``rsutil.h``). This function needs depths intrinsics, 2D pixel and distance in meters. Here is how we fetch depth intrinsics and get distance in meters can be acquired using get_distance function of depth_frame class just like the previous one.
    ```C
    auto stream = profile.get_stream(RS2_STREAM_DEPTH).as<rs2::video_stream_profile>();
    auto intrinsics = stream.get_intrinsics(); // Calibration data

    float dist_3d(const rs2_intrinsics& intr, const rs2::depth_frame& frame, pixel u, pixel v)
    {
        float upixel[2]; 
        float upoint[3];

        float vpixel[2]; 
        float vpoint[3]; 
         upixel[0] = u.first;
     upixel[1] = u.second;
     vpixel[0] = v.first;
     vpixel[1] = v.second
    auto udist = frame.get_distance(upixel[0], upixel[1]);
    auto vdist = frame.get_distance(vpixel[0], vpixel[1]);

     rs2_deproject_pixel_to_point(upoint, &intr, upixel, udist);
     rs2_deproject_pixel_to_point(vpoint, &intr, vpixel, vdist);
    ```
    
    Now we can combine all the mapping process together :
    
    ```C
    #include <librealsense2/rs.hpp> // Include RealSense Cross Platform API
    #include <librealsense2/rsutil.h>
    #include "example.hpp"          // Include short list of convenience functions for rendering

    // This example will require several standard data-structures and algorithms:
    #define _USE_MATH_DEFINES
    #include <math.h>
    #include <queue>
    #include <unordered_set>
    #include <map>
    #include <thread>
    #include <atomic>
    #include <mutex>
    #include <stdlib.h>
     int main(int argc, char * argv[])
     {
        float x=atof(argv[1]);
        float y=atof(argv[2]);
        rs2::config cfg;
        rs2::pipeline pipe;
        cfg.enable_stream(RS2_STREAM_COLOR, 640, 480, RS2_FORMAT_BGR8, 30);
        cfg.enable_stream(RS2_STREAM_DEPTH, 640, 480, RS2_FORMAT_Z16, 30);
        rs2::pipeline_profile prf = pipe.start(cfg);
        //auto profile = pipe.start(cfg);
        auto stream = prf.get_stream(RS2_STREAM_DEPTH).as<rs2::video_stream_profile>();
        struct rs2_intrinsics intrin = stream.get_intrinsics();
        rs2::frameset frames = pipe.wait_for_frames();
        rs2::align align(rs2_stream::RS2_STREAM_COLOR);
        rs2::frameset aligned_frames = align.process(frames);
        rs2::frame color_frame = frames.get_color_frame();
        rs2::frame depth_frame = aligned_frames.get_depth_frame();
        rs2::depth_frame df = depth_frame.as<rs2::depth_frame>();
        float d_pt[3] = { 0 };
        float d_px[2] = { x, y }; // where x and y are 2D coordinates for a pixel on depth frame
        float depth = df.get_distance(x, y);
        rs2_deproject_pixel_to_point(d_pt, &intrin, d_px, depth);
        printf("%f %f %f",d_pt[0], d_pt[1],d_pt[2]);
        return EXIT_SUCCESS;
     }
    ```
## Cloud supervising

- Product Resume

  We compile a web page that can upload fruit information by Weebly, producing a QR-code marked by lazer machine so that we can connect out cloud-based product resume via smart phone with the advantage of the Internet.

- Cloud monitoring

  We capture the real-time system operating data and send it immediately by Node-Red to the Intelligent Manufacturing platform(developed by Syntec) so that we are able to monitor the entire process through the API which we developed in Javascript.

## IoT Communication 
     
# Highlights
