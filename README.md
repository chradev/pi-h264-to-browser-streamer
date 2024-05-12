### Dual camera, near-real-time, h.264 video streamer from RPi 5 to a bowser

Current status of [pi-h264-to-browser-stramer](https://github.com/chradev/pi-h264-to-browser-stramer): single and dual camera support with PTZ control (only in single camera streaming for now).

The project is intended to become a base for a stereo vision of a robot. The PTZ control of the cameras will be similar to the human eye but without mechanical movement.
 * Fork of [kroketio/pi-h264-to-browser](https://github.com/kroketio/pi-h264-to-browser) by [chradev](https://github.com/chradev) Apr 2024: dual camera support and more
   * Fork of [dans98/pi-h264-to-browser](https://github.com/dans98/pi-h264-to-browser/)  by [nikola-j](https://github.com/nikola-j) Jan 2024: supports the new picamera2 Python library
     * Initial staff published by [dans98](https://github.com/dans98) Nov 2021 and based on:
       * [Picamera](https://picamera.readthedocs.io/en/release-1.13/) handles all the video related tasks.
       * [Tornado](https://www.tornadoweb.org/en/stable/) handles serving out the html and js assets via http, and the h264 stream via websockets.
       * [jMuxer](https://github.com/samirkumardas/jmuxer) handles muxing the h264 stream (in browser) and playing it via Media Source extensions. 

### Motivation for extension

The parent project is an excellent solution for near-real-time video capturing, encoding and streaming. Extending it to reach the robot's stereo vision requirements is a challenge that could be solved thanks to advances in embedded and mobile devices supporting video processing with hardware acceleration.

The main reasons for extending the project are:
  * The new PRi 5 board is much more powerful and supports two 5, 8, 12 and 16 MP CSI cameras;
  * There is a feature-rich set of picamera2 library supporting the video processing;
  * Extremely low latency is a main reason for choosing the project for stereo vision of a robot.

**Notes:** Requirements are like in [rpi5-h264-live-stereo-streamer](https://github.com/chradev/rpi5-h264-live-stereo-streamer/) but include following once:
 * KISS (Keep It as Simple as poSsible)
 * The streaming server has to be able to change picamera2 properties like ```ScalerCrop``` for implementing pan & tilt eye movements.

### Basic changes in:
 * src/server.py
   - changes to send to web page: ```{'port': serverPort, 'width': frameWidth, 'height': frameHeight, 'fps': frameRate}```
   - create two rpicamera2 instances for both RPi 5 CSI cameras
   - add timestamps to both video streams usung ```python3-opencv``` library
   - dublicate ```StreamingOutput``` and ```wsHandler``` classes for bulding two video paths
   - add logic to move range-of-interest for both cameras in ```StreamingOutput``` objects (for testing)
   - add ```requestHandlers``` for both ```cam0``` and ```cam1``` streams
   - initialize classes, build video paths and start cameras
 * src/index.html
   - define two ```<video></video>``` elements
   - instantiate and initialize two ```JMuxer``` classes
   - create two ```WebSocket``` instances with right URLs
   - add ```WebSocket``` listeners for visualization of both camera streams

### Problems not solved for now:
 * dublication of ```StreamingOutput``` and ```wsHandler``` classes
 * using of ```offsetX``` and ```offsetY``` variables calculated by independent process 
    - **solved in single streamer case from browser via WebSocket connection**
    * **in dual streamer case will be divided into a separate WS interface**

### Basic changes usage
 * run in src: ```python3 server.py```
 * browse: ```http://RPi-IP:8000/```
 * watch moving image in X direction of both RPi 5 camera streams

![All staff snapshot](https://github.com/chradev/pi-h264-to-browser-stramer/blob/main/readmeAssets/09.05.2024_23.10.33_REC.png)

### Streaming from a single camera with PTZ control

Streaming from a single camera is based on the original application and web interface with some extends like:
 * reading of customization parameters from the command line
 * adding of time stamp to the video using opencv2 and local preview
 * testing and adding of picam2.set_controls({"ScalerCrop": scalerCrop}) for PTZ control
 * adding more camera parameters to index-ss.html at its templatization
 * building right WS url and adding of sliders for PTZ controls of the camera
 * adding message protocol to WS to send back to the server PTZ controls commands
 * implement PTZ controls in server WS message handler when PTZ command is received
 * adding client synchronized analog clock to the web interface
   * it was done tnaks to https://github.com/MrTech-AK/Analog.OnlineClock
   * style.css was added to index-ss.html head section because of .clock -> background: url(clock.svg)
   * components styles was modified to keep the clock transparent and on top of the video

**Notes:** 
 * clock and video components styles are not optimized and well done;
 * single camera streamer will be used mainly for experimental and test purposes

### New changes in single camera streamer usage

 * run in src: ```python3 server-ss.py``` and/or ```python3 server-ss.py -n 1 -p 8001```
 * browse: ```http://RPi-IP:8000/``` and/or ```http://RPi-IP:8001/```
 * watch stream(s) from choosen RPi 5 camera or from both cameras
 * watch both desktop clock from RPi 5 via camera streaming and web clock from client machine
 * use X/Y/Z sliders for each camera to do Pan/Tilt/Zoom

**Default parameters:**
```
Arguments Namespace(preView=False, cameraNumb=0, serverPort=8000, frameRate=30, Xoffset=950, Yoffset=350, Width=1000, Height=1000, Flip=(1, 1))
Camera 0 at flip(1/1), size(1000.1000), offset(950/350) -> h264 video stream at 30fps -> frame by frame over WebSocket -> http://192.168.1.111:8000/
...
Camera ScalerCrop properties: ((0, 0, 128, 128), (0, 0, 3280, 2464), (408, 0, 2464, 2464))
```

**Available options:**
```
python3 server-ss.py -h
usage: server-ss.py [-h] [-v] [-n CAMERANUMB] [-p SERVERPORT] [-r FRAMERATE]
                    [-X XOFFSET] [-Y YOFFSET] [-W WIDTH] [-H HEIGHT] [-f FLIP FLIP]

options:
  -h, --help            show this help message and exit
  -v, --preView
  -n CAMERANUMB, --cameraNumb CAMERANUMB
  -p SERVERPORT, --serverPort SERVERPORT
  -r FRAMERATE, --frameRate FRAMERATE
  -X XOFFSET, --Xoffset XOFFSET
  -Y YOFFSET, --Yoffset YOFFSET
  -W WIDTH, --Width WIDTH
  -H HEIGHT, --Height HEIGHT
  -f FLIP FLIP, --Flip FLIP FLIP
```

![All staff snapshot](https://github.com/chradev/pi-h264-to-browser-stramer/blob/main/readmeAssets/12.05.2024_14.10.57_REC.png)

**Notes:**
 * To make X/Y offset available use none standard resolutions like 1200x1200 (for now).
 * Two server application can be run for both RPi 5 cameras (0/1) on different ports (8000/8001);
 * In browser application the web clock is synchronized with the client machine and it is laying on top of the video stream comming from RPi 5 camera directed to RPi 5 HDMI display where is running desktop ```xclock```. Both clocks were synchronized via NTP with Internet time server. The clocks are precisely positioned one over another thanks to pan/tilt functionality;


### Motivation of the original project

Fork of [dans98/pi-h264-to-browser](https://github.com/dans98/pi-h264-to-browser/) that supports the new picamera2 Python library.

### About

Stream hardware encoded h.264 from a Raspberry Pi equiped with a V1, V2, or HQ camera module, directly to a browser. Latency is good, maybe 1sec. If you want to go realtime, find a webrtc solution.

For installation instructions, [check out our blogpost](https://kroket.io/blog/pi4-h264-camera-web.html)

### Credits

[nikola-j](https://github.com/nikola-j) made the picamera2 support in [this comment](https://github.com/dans98/pi-h264-to-browser/discussions/12#discussioncomment-7901632).
