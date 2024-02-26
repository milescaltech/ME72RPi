#!/usr/bin/env python3

import picamera
import time

def record_video(output_file, duration=10):
    # Create a PiCamera object
    with picamera.PiCamera() as camera:
        # Set resolution (optional)
        camera.resolution = (640, 480)
        
        # Start recording
        camera.start_recording(output_file)
        
        # Record for the specified duration
        camera.wait_recording(duration)
        
        # Stop recording
        camera.stop_recording()

if __name__ == "__main__":
    # Specify the output file name
    video_file = "output_video.h264"
    
    # Specify the recording duration (in seconds)
    recording_duration = 10
    
    # Record the video
    record_video(video_file, recording_duration)
    
    print(f"Video recorded and saved to {video_file}")
