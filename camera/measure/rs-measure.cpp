// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2017 Intel Corporation. All Rights Reserved.

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
    float x =atof(argv[1]);
    float y =atof(argv[2]);

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



    float d_px[2] = { x, y }; // where x and y are 2D coordinates for a pixel on depth frame


    float depth = df.get_distance(d_px[0], d_px[1]);



    printf("%f",depth);


    return EXIT_SUCCESS;


 }
