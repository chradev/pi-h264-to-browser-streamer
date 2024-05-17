### Dual camera, near-real-time, h.264 video streamer from RPi 5 to a bowser

Current status of [pi-h264-to-browser-streamer](https://github.com/chradev/pi-h264-to-browser-streamer) project: single and dual camera support with ePTZ control.

The project is intended to become a base for a stereo vision of a robot. The ePTZ control of the cameras will be similar to the human eye but without mechanical movement.

  * Fork of [kroketio/pi-h264-to-browser](https://github.com/kroketio/pi-h264-to-browser) by [chradev](https://github.com/chradev) Apr 2024: dual camera support and more
    * Fork of [dans98/pi-h264-to-browser](https://github.com/dans98/pi-h264-to-browser/)  by [nikola-j](https://github.com/nikola-j) Jan 2024: supports the new picamera2 Python library
      * Initial staff published by [dans98](https://github.com/dans98) Nov 2021 and based on:
        * [Picamera](https://picamera.readthedocs.io/en/release-1.13/) handles all the video related tasks.
        * [Tornado](https://www.tornadoweb.org/en/stable/) handles serving out the html and js assets via http, and the h264 stream via websockets.
        * [jMuxer](https://github.com/samirkumardas/jmuxer) handles muxing the h264 stream (in browser) and playing it via Media Source extensions. 

### Motivation to use and extend choosen projects

The main goal is to implement h.264 video streaming from dual RPi cameras to a bowser with near-real-time latency. In addition to it following opportunities are possible

  * by using of RPi 5, UC-512 Camarray HAT and 5 RPi cameras with high resolution:
    * full 2&pi; steradians video streaming 
  * by using 3 sets of RPi 5 and dual RPi cameras with high resolution:
    * 360 degree panoramic real time video streaming
    * ePTZ based on 360 degree panoramic real time video

The main reasons to use and extend above projects are:

 * KISS (Keep It as Simple as poSsible)
 * The new PRi 5 board is much more powerful and supports two 5, 8, 12, 16 or 64 MP CSI cameras;
 * There is a feature-rich set of picamera2 library supporting the video processing;
 * There is a feature-rich set of opencv2 library supporting the video pre-processing;
 * Extremely low latency is a main advantage for using the project for stereo vision of a robot.
 * The streaming server is able to change properties like ```ScalerCrop``` thanks to picamera2 library features while streaming for implementing of motorless ePTZ control.

Requirements are like in the [rpi5-h264-live-stereo-streamer](https://github.com/chradev/rpi5-h264-live-stereo-streamer/) project but an essential difference is that with usage of the picamera2 library for capturing and encoding in the streaming server the video process is under complete control. In addition the ability to combine the opencv2 library in the video processing chain gives almost endless possibilities.

### A Standard Stereo Vision Principle

<img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/AStandardStereoVisionPrinciple.png?raw=true" alt="A Standard Stereo Vision Principle drawings" width="100%">


### An example of ePTZ or difital PTZ Principle

ePTZ is a new digital technology, which stands for electronic pan, tilt, and zoom. There is a significant <a href="https://huddlecamhd.com/eptz-and-ptz/" target="_blank">difference</a> between old PTZ cameras and new ePTZ. Mainly because of its advantages like smaller price and size, this technology is extremely appropriate for robot vision especially in multi-camera cases.

<img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/ePTZ-example-landscape.webp?raw=true" alt="An example of ePTZ or difital PTZ Principle" width="100%">

### RPi cameras comparisn table

<table width="100%"><thead><tr style="background-color: #f8f8c0;">
<th> Feature </th><th> Camera Module v1 </th><th> Camera Module v2 </th><th> Camera Module 3 </th><th> Camera Module 3 Wide </th><th> HQ Camera </th>
 </tr></thead><tbody><tr>
<td style="text-align: end; padding-right: 5px;"> Net price </td><td> $25 </td><td> $25 </td><td> $25 </td><td> $35 </td><td> $50 </td>
</tr><tr style="background-color: #fcfcec;">
<td style="text-align: end; padding-right: 5px;"> Size </td><td> 25 x 24 x 9 mm </td><td> 25 x 24 x 9 mm </td><td> 25 x 24 x 11.5 mm </td><td> 25 x 24 x 12.4 mm </td><td> 38 x 38 x 18.4mm<br>(excluding lens) </td>
</tr><tr>
<td style="text-align: end; padding-right: 5px;"> Weight </td><td> 3g </td><td> 3g </td><td> 4g </td><td> 4g </td><td> 30.4g </td>
</tr><tr style="background-color: #fcfcec;">
<td style="text-align: end; padding-right: 5px;"> Still resolution </td><td> 5 Megapixels  </td><td> 8 Megapixels </td><td> 11.9 Megapixels </td><td> 11.9 Megapixels </td><td> 12.3 Megapixels </td>
</tr><tr>
<td style="text-align: end; padding-right: 5px;"> Video modes </td><td> 1080p30,<br>720p60 and<br>640 x 480p60/90 </td><td> 1080p47,<br>1640 x 1232p41 and<br>640 x 480p206 </td><td> 2304 x 1296p56,<br>2304 x 1296p30 HDR,<br>1536 x 864p120 </td><td> 2304 x 1296p56,<br>2304 x 1296p30 HDR,<br>1536 x 864p120 </td><td> 2028 x 1080p50,<br>2028 x 1520p40 and<br>1332 x 990p120 </td>
</tr><tr style="background-color: #fcfcec;">
<td style="text-align: end; padding-right: 5px;"> Sensor </td><td> OmniVision OV5647 </td><td> Sony IMX219 </td><td> Sony IMX708 </td><td> Sony IMX708 </td><td> Sony IMX477 </td>
</tr><tr>
<td style="text-align: end; padding-right: 5px;"> Sensor resolution </td><td> 2592 x 1944 pixels </td><td> 3280 x 2464 pixels </td><td> 4608 x 2592 pixels </td><td> 4608 x 2592 pixels </td><td> 4056 x 3040 pixels </td>
</tr><tr style="background-color: #fcfcec;">
<td style="text-align: end; padding-right: 5px;"> Sensor image area </td><td> 3.76 x 2.74 mm </td><td> 3.68 x 2.76 mm<br>(4.6 mm diagonal) </td><td> 6.45 x 3.63mm<br>(7.4mm diagonal) </td><td> 6.45 x 3.63mm<br>(7.4mm diagonal) </td><td> 6.287mm x 4.712 mm<br>(7.9mm diagonal) </td>
</tr><tr>
<td style="text-align: end; padding-right: 5px;"> Pixel size </td><td> 1.4 &mu;m x 1.4 &mu;m </td><td> 1.12 &mu;m x 1.12 &mu;m </td><td> 1.4 b5&mu;m x 1.4 &mu;m </td><td> 1.4 &mu;m x 1.4 &mu;m </td><td> 1.55 &mu;m x 1.55 &mu;m </td>
</tr><tr style="background-color: #fcfcec;">
<td style="text-align: end; padding-right: 5px;"> Optical size </td><td> 1/4" </td><td> 1/4" </td><td> 1/2.43" </td><td> 1/2.43" </td><td> 1/2.3" </td>
</tr><tr>
<td style="text-align: end; padding-right: 5px;"> Focus </td><td> Fixed </td><td> Adjustable </td><td> Motorized </td><td> Motorized </td><td> Adjustable </td>
</tr><tr style="background-color: #fcfcec;">
<td style="text-align: end; padding-right: 5px;"> Depth of field </td><td> Approx 1 m to 8 </td><td> Approx 10 cm to 8 </td><td> Approx 10 cm to 8 </td><td> Approx 5 cm to 8 </td><td> N/A </td>
</tr><tr>
<td style="text-align: end; padding-right: 5px;"> Focal length </td><td> 3.60 mm +/- 0.01 </td><td> 3.04 mm </td><td> 4.74 mm </td><td> Depends on lens </td><td> Depends on lens </td>
</tr><tr style="background-color: #fcfcec;">
<td style="text-align: end; padding-right: 5px;"> Horizontal Field of View (FoV) </td><td> 53.50 +/- 0.13 degrees </td><td> 62.2 degrees </td><td> 66 degrees </td><td> Depends on lens </td><td> Depends on lens </td>
</tr><tr>
<td style="text-align: end; padding-right: 5px;"> Vertical Field of View (FoV) </td><td> 41.41 +/- 0.11 degrees </td><td> 48.8 degrees </td><td> 41 degrees </td><td> Depends on lens </td><td> Depends on lens </td>
</tr><tr style="background-color: #fcfcec;">
<td style="text-align: end; padding-right: 5px;"> Focal ratio (F-Stop) </td><td> F2.9 </td><td> F2.0 </td><td> F1.8 </td><td> F2.2 </td><td> Depends on lens </td>
</tr><tr>
<td style="text-align: end; padding-right: 5px;"> Maximum exposure times [s] </td><td> 0.97 </td><td> 11.76 </td><td> 112 </td><td> 112 </td><td> 670.74 </td>
</tr><tr style="background-color: #fcfcec;">
<td style="text-align: end; padding-right: 5px;"> Lens Mount </td><td> N/A </td><td> N/A </td><td> N/A </td><td> N/A </td><td> C/CS- or M12-mount </td>
</tr><tr>
<td style="text-align: end; padding-right: 5px;"> NoIR version available? </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> No </td>
</tr><tr></tbody></table>


### A snapshot of running dual camera streaming server and its web user interfase

<img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/15.05.2024_00.12.38_REC.png?raw=true" alt="Dual camera streaming snapshot" width="100%">

### A short video of dual camera streaming server with ePTZ control

https://github.com/chradev/pi-h264-to-browser-streamer/assets/11261306/cbac77e0-3cdb-4b67-8a05-6e53c996912c

**Notes:**

 * in above video clip you can only see usage of ePTZ control for both cameras simultaneously
 * in addition each camera can be PT controled separately and can be used for tuning
 * individual PT parameters for both cameras can be set as defaults
 * ePTZ parameters of the cameras will be reset to defaults at browser refresh
 * additional actions available are: enable/disable of texts and lines drawn on the frames
 * ePTZ control is available to any user connected to the server but result is visible by all of them 


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

### Problems <del>not</del> solved <del>for now</del>:

 * dublication of ```StreamingOutput``` and ```wsHandler``` classes - **solved**
    * **added second ```WebSocket``` handler ```ptzHandler``` for ePTZ camera control**
 * using of ```offsetX``` and ```offsetY``` variables calculated by independent process 
    * **solved in single streamer case from browser via ```WebSocket``` connection**
    * **in dual streamer case will <del>be</del> is divided into a separate WS interface**

### Advanced changes for double camera streaming with ePTZ control

Dual camera streaming is based on the basic modifications in server application and web interface with following extensions:

 * problem with dublication of ```StreamingOutput``` and ```wsHandler``` classes is solved
 * extended startup settings, added camera preview, logging functionality and more
 * added second ```WebSocket``` handler ```ptzHandler``` for ePTZ control of both cameras
 * added sliders in web page for ePTZ control of both cameras separately and simultaneously
 * added server support for ePTZ control for both cameras separately and simultaneously
 * added server support for changing of default ePTZ values for tuning of cameras position

### Changes to be done (TBD)

 * saving default ePTZ values in a file

### Changes in the file and directory structure

Original files are kept in ```src``` folder

All files of single streamer are moved to ```single``` folder

Files of dual streamer are moved for:

 * server to ```dual``` folder
 * web user interfase to ```dual/web``` folder


### Dual camera streamer usage

 * run as user in ```dual``` folder: ```python3 server.py```
 * run as user: ```export DISPLAY=:0 && xclock -analog -update 0.1 -bw 100```
 * direct both RPi cameras to RPi 5 desktop monitor
 * browse other computer: ```http://RPi-IP:8000/```
 * watch streams of both cameras
 * use ePTZ cameras controls

Server log at startup:
```
.../dual $ python server.py
...
[2024-05-14 03:26:07] Starting: Dual camera streaming server & web interface on RPi 5
                                -> with two 8MP RPi cameras v.2 at size: 3280/2464 px
                                -> starting up at flip: 1/1, offset: 0-2280/0-1464 px
                                -> capturing at framerate: 30 fps, size: 1000/1000 px
                                -> streaming h264 video frame by frame over WebSocket
                                => run browser at address: http://192.168.1.111:8000/
[2024-05-14 03:26:07] Starting chain for: Stream 0 (ready for streaming)
[2024-05-14 03:26:07] Starting chain for: Stream 1 (ready for streaming)
[2024-05-14 03:26:10] Starting a service: Camera 0 (192.168.1.178)
[2024-05-14 03:26:10] Starting a service: Camera 1 (192.168.1.178)
[2024-05-14 03:26:10] Starting a service: CamPTZ - (192.168.1.178)
```

Server performance reported by ```htop```
```
    0[|||||||||||||||||                       34.5%] Tasks: 91, 122 thr, 120 kthr; 3 running
    1[||||||||||||||||||||||||||              55.0%] Load average: 2.38 2.31 2.18
    2[||||||||||||||||||                      38.6%] Uptime: 1 day, 09:25:13
    3[||||||||||||||||||||                    41.4%]
  Mem[||||||||||||||||||                 702M/3.95G]
  Swp[|||||||||||||||||||||||||||||||||83.8M/100.0M]

  [Main] [I/O]
    PID USER       PRI  NI  VIRT   RES   SHR S  CPU%?MEM%   TIME+  Command
   9510 chr         20   0 1839M  290M  135M S 166.8  7.2 33:40.74 python server.py
   9529 chr         20   0 1839M  290M  135M S  45.2  7.2  8:03.60 python server.py
   9531 chr         20   0 1839M  290M  135M S  45.2  7.2  7:36.82 python server.py
   9522 chr         20   0 1839M  290M  135M S  23.3  7.2  5:20.35 python server.py
   9533 chr         20   0 1839M  290M  135M S   5.3  7.2  1:07.46 python server.py
```


### Streaming from a single camera with ePTZ control

Streaming from a single camera is based on the original application and web interface with some extends like:

 * reading of customization parameters from the command line
 * adding of time stamp and two lines to the video using opencv2 and local preview
 * testing and adding of ```picam2.set_controls({"ScalerCrop": scalerCrop})``` for ePTZ control
 * adding more camera parameters to index-ss.html at its templatization
 * building right WS url and adding of sliders for ePTZ controls of the camera
 * adding message protocol to WS to send back to the server ePTZ controls commands
 * implement ePTZ controls in server WS message handler when ePTZ command is received
 * adding client synchronized analog clock to the web interface
   * it was done tnaks to https://github.com/MrTech-AK/Analog.OnlineClock
   * style.css was added to index-ss.html head section because of ```.clock -> background: url(clock.svg)```
   * components styles was modified to keep the clock transparent and on top of the video

**Notes:** 

 * clock and video components styles are not optimized;
 * single camera streamer will be used mainly for experimental and test purposes

### Single camera streamer usage

 * run in ```single``` folder: ```python3 server.py``` and/or ```python3 server.py -n 1 -p 8001 -X 1730 -Y 410```
 * run as user: ```export DISPLAY=:0 && xclock -analog -update 0.1 -bw 100```
 * direct both RPi cameras to RPi 5 desktop monitor
 * browse other computer: ```http://RPi-IP:8000/``` and/or ```http://RPi-IP:8001/```
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
python3 server.py -h
usage: server.py [-h] [-v] [-n CAMERANUMB] [-p SERVERPORT] [-r FRAMERATE]
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

<img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/12.05.2024_14.10.57_REC.png?raw=true" alt="Single camera streaming snapshot" width="100%">

**Notes:**

 * To make X/Y offset available use none standard resolutions like 1200x1200 (for now).
 * Two server application can be run for both RPi 5 cameras (0/1) on different ports (8000/8001);
 * In browser application the web clock is synchronized with the client machine and it is laying on top of the video stream comming from RPi 5 camera directed to RPi 5 HDMI display where is running desktop ```xclock```. Both clocks were synchronized via NTP with Internet time server. The clocks are precisely positioned one over another thanks to pan/tilt functionality;

Watch a short video of single camera streaming latency:

https://github.com/chradev/pi-h264-to-browser-streamer/assets/11261306/35d78562-eade-4b3c-9026-b9a101f1fcf4



### Motivation of the original project

Fork of [dans98/pi-h264-to-browser](https://github.com/dans98/pi-h264-to-browser/) that supports the new picamera2 Python library.

### About

Stream hardware encoded h.264 from a Raspberry Pi equiped with a V1, V2, or HQ camera module, directly to a browser. Latency is good, maybe 1sec. If you want to go realtime, find a webrtc solution.

For installation instructions, [check out our blogpost](https://kroket.io/blog/pi4-h264-camera-web.html)

### Credits

[nikola-j](https://github.com/nikola-j) made the picamera2 support in [this comment](https://github.com/dans98/pi-h264-to-browser/discussions/12#discussioncomment-7901632).
