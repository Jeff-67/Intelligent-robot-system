// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API
#include "example.hpp"          // Include short list of convenience functions for rendering

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams

// 3rd party header for writing png files
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"
#define _USE_MATH_DEFINES
#include <math.h>
#include <queue>
#include <unordered_set>
#include <map>
#include <thread>
#include <atomic>
#include <mutex>


// Helper function for writing metadata to disk as a csv file
//void metadata_to_csv(const rs2::frame& frm, const std::string& filename);

// This sample captures 30 frames and writes the last frame to disk.
// It can be useful for debugging an embedded system with no display.
int main(int argc, char * argv[]) try
{
    rs2::colorizer color_map;
    // Decimation filter reduces the amount of data (while preserving best samples)
    rs2::decimation_filter dec;
    // If the demo is too slow, make sure you run in Release (-DCMAKE_BUILD_TYPE=Release)
    // but you can also increase the following parameter to decimate depth more (reducing quality)
    dec.set_option(RS2_OPTION_FILTER_MAGNITUDE, 2);
    // Define transformations from and to Disparity domain
    rs2::disparity_transform depth2disparity;
    rs2::disparity_transform disparity2depth(false);
    // Define spatial filter (edge-preserving)
    rs2::spatial_filter spat;
    // Enable hole-filling
    // Hole filling is an agressive heuristic and it gets the depth wrong many times
    // However, this demo is not built to handle holes
    // (the shortest-path will always prefer to "cut" through the holes since they have zero 3D distance)
    spat.set_option(RS2_OPTION_HOLES_FILL, 5); // 5 = fill all the zero pixels
    // Define temporal filter
    rs2::temporal_filter temp;
    // Spatially align all streams to depth viewport
    // We do this because:
    //   a. Usually depth has wider FOV, and we only really need depth for this demo
    //   b. We don't want to introduce new holes
    rs2::align align_to(RS2_STREAM_DEPTH);
    // Declare depth colorizer for pretty visualization of depth data
    //rs2::colorizer color_map;

    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe;
    rs2::config cfg;
    cfg.enable_stream(RS2_STREAM_DEPTH); // Enable default depth
    // For the color stream, set format to RGBA
    // To allow blending of the color frame on top of the depth frame
    cfg.enable_stream(RS2_STREAM_COLOR, RS2_FORMAT_RGBA8);
    auto profile = pipe.start(cfg);
    auto sensor = profile.get_device().first<rs2::depth_sensor>();

    // TODO: At the moment the SDK does not offer a closed enum for D400 visual presets
    // (because they keep changing)
    // As a work-around we try to find the High-Density preset by name
    // We do this to reduce the number of black pixels
    // The hardware can perform hole-filling much better and much more power efficient then our software
    auto range = sensor.get_option_range(RS2_OPTION_VISUAL_PRESET);
    for (auto i = range.min; i < range.max; i += range.step)
        if (std::string(sensor.get_option_value_description(RS2_OPTION_VISUAL_PRESET, i)) == "High Density")
            sensor.set_option(RS2_OPTION_VISUAL_PRESET, i);
    // After initial post-processing, frames will flow into this queue:
    //auto stream = profile.get_stream(RS2_STREAM_DEPTH).as<rs2::video_stream_profile>();

        // Create a simple OpenGL window for rendering:
    //window app(stream.width(), stream.height(), "RealSense Measure Example");

    rs2::frame_queue postprocessed_frames;

    // In addition, depth frames will also flow into this queue:
    rs2::frame_queue pathfinding_queue;

    // Alive boolean will signal the worker threads to finish-up
    std::atomic_bool alive{ true };

    std::thread video_processing_thread([&]() {
        // In order to generate new composite frames, we have to wrap the processing
        // code in a lambda
        rs2::processing_block frame_processor(
            [&](rs2::frameset data, // Input frameset (from the pipeline)
                rs2::frame_source& source) // Frame pool that can allocate new frames
        {
            // First make the frames spatially aligned
            data = align_to.process(data);

            // Next, apply depth post-processing
            rs2::frame depth = data.get_depth_frame();
            // Decimation will reduce the resultion of the depth image,
            // closing small holes and speeding-up the algorithm
            depth = dec.process(depth);
            // To make sure far-away objects are filtered proportionally
            // we try to switch to disparity domain
            depth = depth2disparity.process(depth);
            // Apply spatial filtering
            depth = spat.process(depth);
            // Apply temporal filtering
            depth = temp.process(depth);
            // If we are in disparity domain, switch back to depth
            depth = disparity2depth.process(depth);
            // Send the post-processed depth for path-finding
            pathfinding_queue.enqueue(depth);

            // Apply color map for visualization of depth
            auto colorized = color_map(depth);
            auto color = data.get_color_frame();
            // Group the two frames together (to make sure they are rendered in sync)
            rs2::frameset combined = source.allocate_composite_frame({ colorized, color });
            // Send the composite frame for rendering
            source.frame_ready(combined);
        });
        // Indicate that we want the results of frame_processor
        // to be pushed into postprocessed_frames queue
        frame_processor >> postprocessed_frames;

        while (alive)
        {
            // Fetch frames from the pipeline and send them for processing
            rs2::frameset fs;
            if (pipe.poll_for_frames(&fs)) frame_processor.invoke(fs);
            static rs2::frameset current_frameset;
            postprocessed_frames.poll_for_frame(&current_frameset);

            if (auto vf = current_frameset.as<rs2::video_frame>())
            {
                std::stringstream png_file;
                png_file << "/home/nvidia/darknet/data/123/" << vf.get_profile().stream_name() << ".png";
                stbi_write_png(png_file.str().c_str(), vf.get_width(), vf.get_height(),
                               vf.get_bytes_per_pixel(), vf.get_data(), vf.get_stride_in_bytes());
                std::cout << "Saved " << png_file.str() << std::endl;

             }

        }
    });



    return EXIT_SUCCESS;
}
catch(const rs2::error & e)
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return EXIT_FAILURE;
}
catch(const std::exception & e)
{
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}

//void metadata_to_csv(const rs2::frame& frm, const std::string& filename)
//{
    //std::ofstream csv;

    //csv.open(filename);

    //    std::cout << "Writing metadata to " << filename << endl;
    //csv << "Stream," << rs2_stream_to_string(frm.get_profile().stream_type()) << "\nMetadata Attribute,Value\n";

    // Record all the available metadata attributes
    //for (size_t i = 0; i < RS2_FRAME_METADATA_COUNT; i++)
    //{
        //if (frm.supports_frame_metadata((rs2_frame_metadata_value)i))
        //{
            //csv << rs2_frame_metadata_to_string((rs2_frame_metadata_value)i) << ","
                //<< frm.get_frame_metadata((rs2_frame_metadata_value)i) << "\n";
        //}
    //}

    //csv.close();
//}
