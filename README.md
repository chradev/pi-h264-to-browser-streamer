### Dual camera, near-real-time, h.264 video streamer from RPi 5 to a bowser

Current status of [pi-h264-to-browser-streamer](https://github.com/chradev/pi-h264-to-browser-streamer) project: single and dual camera support with ePTZ control.

The project is intended to become a base for a stereo vision of a robot. The ePTZ control of the cameras will be similar to the human eye but without mechanical movement.

  * Fork of [kroketio/pi-h264-to-browser](https://github.com/kroketio/pi-h264-to-browser) by [chradev](https://github.com/chradev) Apr 2024: dual camera support and more
    * Fork of [dans98/pi-h264-to-browser](https://github.com/dans98/pi-h264-to-browser/)  by [nikola-j](https://github.com/nikola-j) Jan 2024: supports the new picamera2 Python library
      * Initial staff published by [dans98](https://github.com/dans98) Nov 2021 and based on:
        * [Picamera](https://picamera.readthedocs.io/en/release-1.13/) handles all the video related tasks.
        * [Tornado](https://www.tornadoweb.org/en/stable/) handles serving out the html and js assets via http, and the h264 stream via websockets.
        * [jMuxer](https://github.com/samirkumardas/jmuxer) handles muxing the h264 stream (in browser) and playing it via Media Source extensions. 

### How success with dual RPi camera h264 video streamer affects my robot project

The success with dual RPi camera h264 video streamer impact on my robot project:

 * robots can be equipped with single or dual cameras for stereo or panorama vision with ePTS;
 * cameras can be used are ESP32-Cam, RPi's Model 2 / 3 (wide), Arducam's 16MP (wide) / 64MP;
 * robots can be equipped with single or dual display with SPI or HDMI interface;
 * displays can be used are 3.2" / 5" / 7" in size with or without touchscreen;
 * SBCs used can be RPi 5 / 4, RPi Zero 2 (w), NanoPi NEO Core-LTS, RPi Pico, ESP-32(-S);
 * transmission will be based on PIO-Driven Stepper Motor Driver by V. Hunter Adams;
 * the software staff will be used is Linux, Espressif IDF, RPi Pico SDK, Arduino, C/C++, JS, Python.

<img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/ImpactOnMyRobotProject.png?raw=true" alt="Impact on my robot project" width="100%">

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

### Stereo geometry calculation

Thanks to Nerian - the Allied Vision [**Stereo Baseline Calculator**](https://en.nerian.alliedvision.com/support/calculator/) the calculation is done for:

 * 16MP IMX519 Arducam camera with sensor resolution of 4656 x 3496 px
 * Focused distance of 1 m, minimal depth of 35 cm and base line of 10 cm
 * Disparity range of 1024 px and expected disparity error of 1 px

The result is very good especially for the minimal depth of 35 cm and error of:

 * 0.28 cm at 1 m (less than 0.3%)
 * 28.7 cm at 10 m (less than 3%)

<img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/StereoCalculator-bl10cm.png?raw=true" alt="Stereo geometry calculation" width="100%">


### An example of ePTZ or difital PTZ Principle

ePTZ is a new digital technology, which stands for electronic pan, tilt, and zoom. There is a significant <a href="https://huddlecamhd.com/eptz-and-ptz/" target="_blank">difference</a> between old PTZ cameras and new ePTZ. Mainly because of its advantages like smaller price and size, this technology is extremely appropriate for robot vision especially in multi-camera cases.

<img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/ePTZ-example-landscape.webp?raw=true" alt="An example of ePTZ or difital PTZ Principle" width="100%">

### RPi cameras comparison table

<table style="overflow-y: hidden;width: 100%;height: 100%;text-align: center; border:1px; border-collapse: collapse;">
<thead>
<tr style="background-color: #f0f0c0;">
    <th style="text-align: end; padding-right: 5px;" > Vendor </th><th colspan="5" > Raspberry Pi </th><th colspan="3" > Arducam </th></tr>
<tr style="background-color: #f0f0c0;">
    <th> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Camera&nbsp;/&nbsp;Model&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </th>
    <th> Module v1 </th><th> Module v2 </th><th> Module 3 </th><th> Module 3 Wide </th><th> HQ </th><th> 16MP IMX519 </th><th> &nbsp;&nbsp;&nbsp;16MP&nbsp;Wide&nbsp;&nbsp;&nbsp; </th><th>64MP Hawkeye</th></tr>
</thead><tbody>
<tr><td> <img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/rpi_5.png?raw=true" width="auto" height="120px" ></td>
    <td> <img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/cm1-120.png?raw=true" width="auto" height="120px" ></td>
    <td> <img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/cm2-60.png?raw=true" width="190px" height="auto" ><br>Normal &amp; NoIR</td>
    <td> <img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/cm3-110.png?raw=true" width="190px" height="auto" ><br>Normal &amp; NoIR</td>
    <td> <img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/cm3-w-110.png?raw=true" width="190px" height="auto" ><br>Normal &amp; NoIR</td>
    <td> <img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/hq-110.png?raw=true" width="160px" height="auto" ><br>M12 &amp; C/CS</td>
    <td> <img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/ac16mp-110.png?raw=true" width="auto" height="120px"  ></td>
    <td> <img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/ac16mp-w-100.png?raw=true" width="auto" height="120px"  ></td>
    <td> <img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/ac64mp-120.png?raw=true" width="auto" height="120px"  ></td></tr>
<tr style="background-color: #fcfccc;">
    <td style="text-align: end; padding-right: 5px;"> Net price [$] </td><td> 25 </td><td> 25 </td><td> 25 </td><td> 35 </td><td> 50 </td><td>25</td><td>37</td><td>60</td></tr>
<tr>
    <td style="text-align: end; padding-right: 5px;"> Size [mm] </td><td> 25 x 24 x 9 </td><td> 25 x 24 x 9 </td><td> 25 x 24 x 11.5 </td><td> 25 x 24 x 12.4 </td><td> 38 x 38 x 18.4<br>(excluding lens) </td><td>25 x 24 x 8.26</td><td>25 x 24 x ??</td><td>25 x 24 x 11.5</td></tr>
<tr style="background-color: #fcfccc;">
    <td style="text-align: end; padding-right: 5px;"> Weight [g] </td><td> 3 </td><td> 3 </td><td> 4 </td><td> 4 </td><td> 30.4 </td><td></td><td></td><td></td></tr>
<tr>
    <td style="text-align: end; padding-right: 5px;"> Still resolution [MP] </td><td> 5 </td><td> 8 </td><td> 11.9 </td><td> 11.9 </td><td> 12.3 </td><td>16</td><td>16</td><td>64</td></tr>
<tr style="background-color: #fcfccc;">
    <td style="text-align: end; padding-right: 5px;"> Video modes<br>[px x px @ fps] </td><td> 1080@30,<br>720@60, 640x480@60/90 </td><td> 1640x1232@41, 1080@47, 640x480@206 </td><td> 2304x1296@30/HDR, 2304x1296@56, 1536x864@120 </td><td> 2304x1296@30/HDR, 2304x1296@56, 1536x864@120 </td><td> 2028x1520@40, 2028x1080@50, 1332x990@120 </td>
    <td>4656x3496@10, 3840x2160@21, 1920x1080@60, 1280x720@120</td><td>4656x3496@10, 3840x2160@21, 1920x1080@60, 1280x720@120</td><td>9152x6944@2.7, 8000x6000@3, 4624x3472@10, 3840x2160@20, 2312x1736@30, 1920x1080@60, 1280x720@120 </td></tr>
<tr>
    <td style="text-align: end; padding-right: 5px;"> Sensor </td><td> OmniVision&nbsp;OV5647 </td><td> Sony IMX219 </td><td> Sony IMX708 </td><td> Sony IMX708 </td><td> Sony IMX477 </td><td>Sony IMX519</td><td>Sony IMX519</td><td></td></tr>
<tr style="background-color: #fcfccc;">
    <td style="text-align: end; padding-right: 5px;"> Sensor resolution [px] </td><td> 2592 x 1944 </td><td> 3280 x 2464 </td><td> 4608 x 2592 </td><td> 4608 x 2592 </td><td> 4056 x 3040 </td><td>4656 x 3496 </td><td>4656 x 3496 </td><td>9152 x 6944 </td></tr>
<tr>
    <td style="text-align: end; padding-right: 5px;"> Sensor image area [mm] </td><td> 3.76 x 2.74 </td><td> 3.68 x 2.76<br>(4.6 diagonal) </td><td> 6.45 x 3.63<br>(7.4 diagonal) </td><td> 6.45 x 3.63<br>(7.4 diagonal) </td><td> 6.287 x 4.712<br>(7.9 diagonal) </td><td>5.680 x 4.265<br>(7.103 diagonal)</td><td>5.680 x 4.265<br>(7.103 diagonal)</td><td> 7.367 x 5.589<br>(9.25 diagonal) </td></tr>
<tr style="background-color: #fcfccc;">
    <td style="text-align: end; padding-right: 5px;"> Pixel size [&mu;m]</td><td> 1.4 x 1.4 </td><td> 1.12 x 1.12 </td><td> 1.4 x 1.4 </td><td> 1.4 x 1.4 </td><td> 1.55 x 1.55 </td><td> 1.22 x 1.22 </td><td> 1.22 x 1.22 </td><td> 0.8 x 0.8 </td></tr>
<tr>
    <td style="text-align: end; padding-right: 5px;"> Optical size [inch]</td><td> 1/4 </td><td> 1/4 </td><td> 1/2.43 </td><td> 1/2.43 </td><td> 1/2.3 </td><td> 1/2.534 </td><td>1/2.534</td><td> 1/1.7 </td></tr>
<tr style="background-color: #fcfccc;">
    <td style="text-align: end; padding-right: 5px;"> Focus </td><td> Fixed </td><td> Adjustable </td><td> Motorized </td><td> Motorized </td><td> Adjustable </td><td> Fixed/Auto </td><td> Manual Focus </td><td> Auto </td></tr>
<tr>
    <td style="text-align: end; padding-right: 5px;"> Depth of field </td><td> 1 m to &infin; </td><td> 10 cm to &infin; </td><td> 10 cm to &infin; </td><td> 5 cm to &infin; </td><td> N/A </td><td>10 cm to &infin;</td><td>10 cm to &infin;</td><td>8 cm to &infin;</td></tr>
<tr style="background-color: #fcfccc;">
    <td style="text-align: end; padding-right: 5px;"> Focal length [mm] </td><td> 3.60 &plusmn; 0.01 </td><td> 3.04 </td><td> 4.74 </td><td> Depends on lens </td><td> Depends on lens </td><td>4.28</td><td>2.87&plusmn;5%</td><td>5.1</td></tr>
<tr>
    <td style="text-align: end; padding-right: 5px;"> Horizontal FoV [degrees] </td><td> 53.50 &plusmn; 0.13 </td><td> 62.2 </td><td> 66 </td><td> Depends on lens </td><td> Depends on lens </td><td> 65 </td><td>120</td><td> 72 </td></tr>
<tr style="background-color: #fcfccc;">
    <td style="text-align: end; padding-right: 5px;"> Vertical FoV [degrees] </td><td> 41.41 &plusmn; 0.11 </td><td> 48.8 </td><td> 41 </td><td> Depends on lens </td><td> Depends on lens </td><td> 51 </td><td>95</td><td> 54.6 </td></tr>
<tr>
    <td style="text-align: end; padding-right: 5px;"> Focal ratio (F.No) </td><td> F2.9 </td><td> F2.0 </td><td> F1.8 </td><td> F2.2 </td><td> Depends on lens </td><td>F1.75</td><td>F2.85&plusmn;5%</td><td>F1.8</td></tr>
<tr style="background-color: #fcfccc;">
    <td style="text-align: end; padding-right: 5px;"> Maximum exposure time [s] </td><td> 0.97 </td><td> 11.76 </td><td> 112 </td><td> 112 </td><td> 670.74 </td><td>&gt; 100</td><td>&gt; 100</td><td>435</td></tr>
<tr>
    <td style="text-align: end; padding-right: 5px;"> Lens Mount </td><td> N/A </td><td> N/A </td><td> N/A </td><td> N/A </td><td> C/CS or M12 </td><td> N/A </td><td> M12*0.5mm </td><td>N/A</td></tr>
<tr style="background-color: #fcfccc;">
    <td style="text-align: end; padding-right: 5px;"> NoIR version available? </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> No </td><td>Yes</td><td>No</td><td>No</td></tr>
<tr>
    <td style="text-align: end; padding-right: 5px;"> Other options </td>
    <td>Digital zoom up to 2.7x</td>
    <td>Digital zoom up to 3.4x</td>
    <td>Digital zoom up to 3.5x</td>
    <td>Digital zoom up to 3.5x</td>
    <td>Digital zoom up to 4.2x</td>
    <td>Digital zoom up to 4.8x;<br>up to 4 cameras via UC-512 Camarray HAT;<br>2-lane CSI-2</td>
    <td>Digital zoom up to 4.8x;<br>up to 4 cameras via UC-512 Camarray HAT;<br>2-lane CSI-2</td>
    <td>Digital zoom up to 9.6x;<br>up to 4 cameras via UC-512 Camarray HAT;<br>2-lane CSI-2</td></tr>
</tbody></table>

### A snapshot of running dual camera streaming server and its web user interfase

<img src="https://github.com/chradev/pi-h264-to-browser-streamer/blob/main/assets/19.05.2024_15.18.59_REC.png?raw=true" alt="Dual camera streaming snapshot" width="100%">

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
 * default ePTZ camera values are updated in a file if ```Save to defaults``` is send
 * added support for horizontal and vertical flip of the cameras and pausing the streams

### Changes in the file and directory structure

 * Original files are kept in ```src``` folder
 * All files of single streamer are moved to ```single``` folder
 * Files of dual streamer are moved for:
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

<details>

```
.../dual $ python server.py
[88:30:44.614638443] [23604]  INFO Camera camera_manager.cpp:284 libcamera v0.2.0+120-eb00c13d
[88:30:44.629432640] [23611]  INFO RPI pisp.cpp:695 libpisp version v1.0.5 999da5acb4f4 17-04-2024 (14:29:29)
[88:30:44.646264053] [23611]  INFO RPI pisp.cpp:1154 Registered camera /base/axi/pcie@120000/rp1/i2c@88000/imx219@10 
                              to CFE device /dev/media0 and ISP device /dev/media3 using PiSP variant BCM2712_C0
[88:30:44.646354609] [23611]  INFO RPI pisp.cpp:695 libpisp version v1.0.5 999da5acb4f4 17-04-2024 (14:29:29)
[88:30:44.655104938] [23611]  INFO RPI pisp.cpp:1154 Registered camera /base/axi/pcie@120000/rp1/i2c@80000/imx219@10 
                              to CFE device /dev/media2 and ISP device /dev/media4 using PiSP variant BCM2712_C0
[88:30:44.656759744] [23604]  INFO Camera camera_manager.cpp:284 libcamera v0.2.0+120-eb00c13d
[88:30:44.667538862] [23616]  INFO RPI pisp.cpp:695 libpisp version v1.0.5 999da5acb4f4 17-04-2024 (14:29:29)
[88:30:44.678089405] [23616]  INFO RPI pisp.cpp:1154 Registered camera /base/axi/pcie@120000/rp1/i2c@88000/imx219@10 
                              to CFE device /dev/media0 and ISP device /dev/media3 using PiSP variant BCM2712_C0
[88:30:44.678179221] [23616]  INFO RPI pisp.cpp:695 libpisp version v1.0.5 999da5acb4f4 17-04-2024 (14:29:29)
[88:30:44.687418126] [23616]  INFO RPI pisp.cpp:1154 Registered camera /base/axi/pcie@120000/rp1/i2c@80000/imx219@10 
                              to CFE device /dev/media2 and ISP device /dev/media4 using PiSP variant BCM2712_C0
[88:30:44.690942740] [23604]  WARN V4L2 v4l2_pixelformat.cpp:344 Unsupported V4L2 pixel format RPBP
[88:30:44.691482354] [23604]  INFO Camera camera.cpp:1183 configuring streams: 
                              (0) 1000x1000-XBGR8888 (1) 1640x1232-RGGB_PISP_COMP1
[88:30:44.691600169] [23616]  INFO RPI pisp.cpp:1450 Sensor: /base/axi/pcie@120000/rp1/i2c@88000/imx219@10 
                              - Selected sensor format: 1640x1232-SRGGB10_1X10 - Selected CFE format: 1640x1232-PC1R
[88:30:44.704837746] [23604]  WARN V4L2 v4l2_pixelformat.cpp:344 Unsupported V4L2 pixel format RPBP
[88:30:44.705551399] [23604]  INFO Camera camera.cpp:1183 configuring streams: 
                              (0) 1000x1000-XBGR8888 (1) 1640x1232-RGGB_PISP_COMP1
[88:30:44.705704548] [23616]  INFO RPI pisp.cpp:1450 Sensor: /base/axi/pcie@120000/rp1/i2c@80000/imx219@10 
                              - Selected sensor format: 1640x1232-SRGGB10_1X10 - Selected CFE format: 1640x1232-PC1R
[2024-05-20 08:52:00] Starting chain for: Camera 0 (ready for streaming)
[2024-05-20 08:52:00] Starting chain for: Camera 1 (ready for streaming)
[2024-05-20 08:52:01] Starting: Dual camera streaming server & web interface on RPi 5
                                -> with two 8MP RPi cameras v.2 at size: 3280/2464 px
                                -> starting up at flip: 1/1, offset: 0-2280/0-1464 px
                                -> capturing at framerate: 30 fps, size: 1000/1000 px
                                -> streaming h264 video frame by frame over WebSocket
                                => run browser at address: http://192.168.1.111:8000/
[2024-05-20 08:52:12] Starting a service: Camera 0 (192.168.1.178)
[2024-05-20 08:52:12] Starting a service: Camera 1 (192.168.1.178)
[2024-05-20 08:52:12] Starting a service: CamPTZ - (192.168.1.178)
```

</details>

Server performance reported by ```htop```

<details>

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

</details>


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

<details>

```
Arguments Namespace(preView=False, cameraNumb=0, serverPort=8000, frameRate=30, Xoffset=950, Yoffset=350, Width=1000, Height=1000, Flip=(1, 1))
Camera 0 at flip(1/1), size(1000.1000), offset(950/350) -> h264 video stream at 30fps -> frame by frame over WebSocket -> http://192.168.1.111:8000/
...
Camera ScalerCrop properties: ((0, 0, 128, 128), (0, 0, 3280, 2464), (408, 0, 2464, 2464))
```

</details>

**Available options:**

<details>

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
</details>

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
