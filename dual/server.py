import io
import os
import socket
from string import Template
#from threading import Condition

import tornado.ioloop
import tornado.web
import tornado.websocket

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import Output

# start configuration
serverPort     = 8000
frameRate      = 30
frameWidth     = 1000
frameHeight    = 1000
frameOffsetX0  = 1020 # 1080
frameOffsetY0  = 880  #740
frameOffsetX1  = 1740 #1750
frameOffsetY1  = 430  #360
enableView     = False
enableTexts0   = True
enableTexts1   = True
enableLines0   = True
enableLines1   = True
framehFlip0    = 1
framevFlip0    = 1
framePause0    = 0
framehFlip1    = 1
framevFlip1    = 1
framePause1    = 0

# Get host IP address
from subprocess import check_output
hostIPAddr = check_output(['hostname', '-I'], text=True).split()[0]

picam20 = Picamera2(0)
picam21 = Picamera2(1)

full_camera_res = picam20.camera_properties['PixelArraySize']
frameOffsetX0m  = full_camera_res[0]
frameOffsetY0m  = full_camera_res[1]
full_camera_res = picam21.camera_properties['PixelArraySize']
frameOffsetX1m  = full_camera_res[0]
frameOffsetY1m  = full_camera_res[1]

from libcamera import Transform
picam20.configure(picam20.create_video_configuration(main={"size": (frameWidth, 
      frameHeight)}, transform=Transform(hflip=framehFlip0, vflip=framevFlip0) ))
picam21.configure(picam21.create_video_configuration(main={"size": (frameWidth, 
      frameHeight)}, transform=Transform(hflip=framehFlip1, vflip=framevFlip1) ))

# use sudo apt install python3-opencv
import cv2
import time
from picamera2 import MappedArray

# Define and attach camera2.pre_callback to put date & time into the video frame
colour = (0, 255, 0)
origin = (0, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

def apply_timestamp0(request):
    timestamp = time.strftime("%Y-%m-%d %X") + " - Camera: 0"
    with MappedArray(request, "main") as m:
        if enableTexts0 is True:
            cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
        if enableLines0 is True:
            cv2.line(m.array, (0, int(frameHeight/2)), (frameWidth, int(frameHeight/2)), [0, 255, 0], 2)
            cv2.line(m.array, (int(frameWidth/2), 0), (int(frameWidth/2), frameHeight), [0, 255, 0], 2)

def apply_timestamp1(request):
    timestamp = time.strftime("%Y-%m-%d %X") + " - Camera: 1"
    with MappedArray(request, "main") as m:
        if enableTexts1 is True:
            cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
        if enableLines1 is True:
            cv2.line(m.array, (0, int(frameHeight/2)), (frameWidth, int(frameHeight/2)), [0, 255, 0], 2)
            cv2.line(m.array, (int(frameWidth/2), 0), (int(frameWidth/2), frameHeight), [0, 255, 0], 2)

picam20.pre_callback = apply_timestamp0
picam21.pre_callback = apply_timestamp1

'''
# Set camera offset and size properties
scalerCrop = (frameOffsetX0, frameOffsetY0, frameWidth, frameHeight)
picam20.set_controls({"ScalerCrop": scalerCrop})
scalerCrop = (frameOffsetX1, frameOffsetY1, frameWidth, frameHeight)
picam21.set_controls({"ScalerCrop": scalerCrop})
'''

from picamera2 import Preview
if enableView is True:
    picam20.start_preview(Preview.QTGL, x=10, y=40, width=500, height=500)
    picam21.start_preview(Preview.QTGL, x=1400, y=540, width=500, height=500)

# Main class streaming output
class StreamingOutput(Output):
    stream = -1
    def __init__(self, stream):
        super().__init__()
        self.stream = stream
#        print("[%s] Starting chain for: Stream %r (ready for streaming)" % 
#              (time.strftime("%Y-%m-%d %X"), self.stream))
        self.loop = None
        self.buffer = io.BytesIO()
        super(StreamingOutput, self).__init__(stream)

    def setLoop(self, loop):
        self.loop = loop

    def outputframe(self, frame, keyframe=True, timestamp=None):
        self.buffer.write(frame)
        if self.loop is not None and camHandler.hasConnections(cam=self.stream):
            self.loop.add_callback(callback=camHandler.broadcast, 
                cam=self.stream, message=self.buffer.getvalue())
        self.buffer.seek(0)
        self.buffer.truncate()

# WebSocketHandler for camera streaming
class camHandler(tornado.websocket.WebSocketHandler):
    camera = -1
    connsCam0 = []
    connsCam1 = []
    remoteIP = ""

    '''
    self.request: HTTPServerRequest(protocol='http', host='192.168.1.111:8000', 
    method='GET', uri='/cam0/', version='HTTP/1.1', remote_ip='192.168.1.178')
    '''
    def open(self, camera):
        self.remoteIP = str(self.request.remote_ip)
        self.camera = int(camera)
        print("[%s] Starting a service: Camera %r (%s)" % 
              (time.strftime("%Y-%m-%d %X"), self.camera, self.remoteIP))
        if self.camera == 0:
            self.connsCam0.append(self)
        else:
            self.connsCam1.append(self)

    def on_close(self):
        print("[%s] Stopping a service: Camera %r (%s)" % 
              (time.strftime("%Y-%m-%d %X"), self.camera, self.remoteIP))
        if self.camera == 0:
            self.connsCam0.remove(self)
        else:
            self.connsCam1.remove(self)

    def on_message(self, message):
        pass

    @classmethod
    def hasConnections(cl, cam):
        if cam == 0 and len(cl.connsCam0) == 0:
            return False
        elif cam == 1 and len(cl.connsCam1) == 0:
            return False
        return True

    @classmethod
    async def broadcast(cl, cam, message):
        if cam == 0:
            conns = cl.connsCam0
        else:
            conns = cl.connsCam1
        for connection in conns:
            try:
                await connection.write_message(message, True)
            except tornado.websocket.WebSocketClosedError:
                pass
            except tornado.iostream.StreamClosedError:
                pass

    def check_origin(self, origin):
        return True

import json
def ptz_send_data():
    return json.dumps([
                { 'cam': 0,
                  'f': {
                      'hor': framehFlip0,
                      'ver': framevFlip0,
                      'pau': 0
                  },
                  'e': {
                      'txt': enableTexts0,
                      'lin': enableLines0,
                      'def': False
                  },
                  'x': {
                    'min': int(frameWidth / 2),
                    'val': int(frameOffsetX0 + frameWidth / 2),
                    'max': int(frameOffsetX0m - frameWidth / 2)
                  },
                  'y': {
                    'min': int(frameHeight / 2),
                    'val': int(frameOffsetY0 + frameHeight / 2),
                    'max': int(frameOffsetY0m - frameHeight / 2)
                  }
                }, 
                { 'cam': 1,
                  'f': {
                      'hor': framehFlip1,
                      'ver': framevFlip1,
                      'pau': 0
                  },
                  'e': {
                      'txt': enableTexts1,
                      'lin': enableLines1,
                      'def': False
                  },
                  'x': {
                    'min': int(frameWidth / 2),
                    'val': int(frameOffsetX1 + frameWidth / 2),
                    'max': int(frameOffsetX1m - frameWidth / 2)
                  },
                  'y': {
                    'min': int(frameHeight / 2),
                    'val': int(frameOffsetY1 + frameHeight / 2),
                    'max': int(frameOffsetY1m - frameHeight / 2)
                  }
                },
                { 'cam': 2,
                  'x': {
                    'min': -1500,
                    'val': 0,
                    'max': 1500
                  },
                  'y': {
                    'min': -1500,
                    'val': 0,
                    'max': 1500
                  },
                  'z': {
                    'min': 0.5,
                    'val': 1.0,
                    'max': 2.0
                  }
                }
                ])

class Streamer():
    camera = -1
    running = False
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        print("[%s] Starting chain for: Camera %r (ready for streaming)" % 
              (time.strftime("%Y-%m-%d %X"), self.camera))
        self.loop = None
        self.output = StreamingOutput(stream=self.camera)
        self.encoder = H264Encoder(repeat=True, framerate=frameRate, qp=23)
        self.encoder.output = self.output
    
    def setLoop(self, loop):
        self.output.setLoop(loop)

    def isRunning(self):
        return running

    def start(self):
        if self.camera == 0:
            picam20.start_recording(self.encoder, self.output)
            running = True
        elif self.camera > 0:
            picam21.start_recording(self.encoder, self.output)
            running = True

    def stop(self):
        if self.camera == 0:
            picam20.stop_recording()
            running = False
        elif self.camera > 0:
            picam21.stop_recording()
            running = False
        
streamer0 = Streamer(camera=0)
streamer1 = Streamer(camera=1)

def set_ptz_data(data, skip):
        global enableTexts0
        global enableTexts1
        global enableLines0
        global enableLines1

        if skip:
            return

#        print(data)

        enableTexts0   = data[0]['e']['txt']
        enableTexts1   = data[1]['e']['txt']
        enableLines0   = data[0]['e']['lin']
        enableLines1   = data[1]['e']['lin']

        global framehFlip0
        global framevFlip0
        global framePause0
        global framehFlip1
        global framevFlip1
        global framePause1
        changeFlip = not framehFlip0   == data[0]['f']['hor'] or\
                     not framevFlip0   == data[0]['f']['ver'] or\
                     not framePause0   == data[0]['f']['pau'] or\
                     not framehFlip1   == data[1]['f']['hor'] or\
                     not framevFlip1   == data[1]['f']['ver'] or\
                     not framePause1   == data[1]['f']['pau']

        framehFlip0 = data[0]['f']['hor']
        framevFlip0 = data[0]['f']['ver']
        framePause0 = data[0]['f']['pau']
        framehFlip1 = data[1]['f']['hor']
        framevFlip1 = data[1]['f']['ver']
        framePause1 = data[1]['f']['pau']

        global streamer0
        global streamer1
        if changeFlip:
            if streamer0.isRunning: 
                streamer0.stop()
            if streamer1.isRunning: 
                streamer1.stop()
            if framePause0 or framePause1:
                return
            picam20.configure(picam20.create_video_configuration(main={"size": (frameWidth, 
                  frameHeight)}, transform=Transform(hflip=framehFlip0, vflip=framevFlip0) ))
            picam21.configure(picam21.create_video_configuration(main={"size": (frameWidth, 
                  frameHeight)}, transform=Transform(hflip=framehFlip1, vflip=framevFlip1) ))
            streamer0.start()
            streamer1.start()

        if data[0]['e']['def'] or data[1]['e']['def']:
            global frameOffsetX0 # = 1080
            global frameOffsetY0 # = 740
            global frameOffsetX1 # = 1750
            global frameOffsetY1 # = 360
            frameOffsetX0  = data[0]['x']['val'] - data[0]['x']['min'] + data[2]['x']['val']
            frameOffsetY0  = data[0]['y']['val'] - data[0]['y']['min'] + data[2]['y']['val']
            frameOffsetX1  = data[1]['x']['val'] - data[1]['x']['min'] + data[2]['x']['val']
            frameOffsetY1  = data[1]['y']['val'] - data[1]['y']['min'] + data[2]['y']['val']

        scalerCrop = (
            data[0]['x']['val'] - data[0]['x']['min'] + data[2]['x']['val'] + int((frameWidth - frameWidth * data[2]['z']['val']) / 2), 
            data[0]['y']['val'] - data[0]['y']['min'] + data[2]['y']['val'] + int((frameHeight - frameHeight * data[2]['z']['val']) / 2), 
            int(frameWidth * data[2]['z']['val']), 
            int(frameHeight * data[2]['z']['val']))
        picam20.set_controls({"ScalerCrop": scalerCrop})
        scalerCrop = (
            data[1]['x']['val'] - data[1]['x']['min'] + data[2]['x']['val'] + int((frameWidth - frameWidth * data[2]['z']['val']) / 2),
            data[1]['y']['val'] - data[1]['y']['min'] + data[2]['y']['val'] + int((frameHeight - frameHeight * data[2]['z']['val']) / 2),
            int(frameWidth * data[2]['z']['val']), 
            int(frameHeight * data[2]['z']['val']))
        picam21.set_controls({"ScalerCrop": scalerCrop})

# WebSocketHandler for camera PTZ control
class ptzHandler(tornado.websocket.WebSocketHandler):
    connections = []
    remoteIP = ""

    def open(self):
        global enableTexts0
        global enableTexts1
        global enableLines0
        global enableLines1
        global framehFlip0
        global framevFlip0
        global framePause0
        global framehFlip1
        global framevFlip1
        global framePause1
        self.remoteIP = str(self.request.remote_ip)
        print("[%s] Starting a service: CamPTZ - (%s)" % 
              (time.strftime("%Y-%m-%d %X"), self.remoteIP))
        self.connections.append(self)
        # Reset camera offset and size properties
        set_ptz_data(json.loads(getFile("data.json")), False)
        enableTexts0   = True
        enableTexts1   = True
        enableLines0   = True
        enableLines1   = True
#        framehFlip0    = 1
#        framevFlip0    = 1
#        framePause0    = 0
#        framehFlip1    = 1
#        framevFlip1    = 1
#        framePause1    = 0
        scalerCrop = (frameOffsetX0, frameOffsetY0, frameWidth, frameHeight)
        picam20.set_controls({"ScalerCrop": scalerCrop})
        scalerCrop = (frameOffsetX1, frameOffsetY1, frameWidth, frameHeight)
        picam21.set_controls({"ScalerCrop": scalerCrop})
        # Send initial data
        message = ptz_send_data()
        self.broadcast(message)

    def on_close(self):
        print("[%s] Stopping a service: CamPTZ - (%s)" % 
              (time.strftime("%Y-%m-%d %X"), self.remoteIP))
        self.connections.remove(self)

    def on_message(self, message):
        data = json.loads(message)
        set_ptz_data(data, False)
        with open('data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.broadcast(message)

    @classmethod
    def hasConnections(cl):
        if len(cl.connections) == 0:
            return False
        return True

    @classmethod
    def broadcast(cl, message):
        for connection in cl.connections:
            try:
                connection.write_message(message)
            except tornado.websocket.WebSocketClosedError:
                pass
            except tornado.iostream.StreamClosedError:
                pass

    def check_origin(self, origin):
        return True

# Define file handlers and index.html templatization
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def getFile(filePath):
    file = open(filePath, 'r')
    content = file.read()
    file.close()
    return content

def templatize(content, replacements):
    tmpl = Template(content)
    return tmpl.substitute(replacements)

mainJs    = templatize(getFile('web/main.js'), {'port': serverPort, 
              'fps': frameRate, 'width': frameWidth, 'height': frameHeight})

# Load defaults from the file
set_ptz_data(json.loads(getFile("data.json")), True)

import markdown
# sudo apt install python3-markdown
readmeHtml = markdown.markdown(getFile('../README.md'), extensions=['fenced_code', 'codehilite', 'markdown.extensions.tables'])

for item in readmeHtml.split("\n"):
    if "https://github.com/chradev/pi-h264-to-browser-streamer/assets/" in item:
        strToChange = '<video autoplay loop muted src=' + item[3:-4] + '></video>'
        readmeHtml = readmeHtml.replace(item, strToChange)
#        print (strToChange)

readmeHtml = '<!doctype html><html lang="en"><head><title>Readme.md</title><style>table, th, td {text-align: center; border:1px solid black; border-collapse: collapse;}</style></head><body>' + readmeHtml + '</body></html>'

# RequestHandler for files access
class readmeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(readmeHtml)

class mainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/javascript')
        self.write(mainJs)

# web application requestHandlers
requestHandlers = [
    (r"/cam(\d+)/", camHandler),
    (r"/ptz/", ptzHandler),
    (r"/main.js", mainHandler),
    (r"/readme", readmeHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {
        "path": "web/",
        "default_filename": "index.html"
    })
]

# server startup staff and main loop
print(('[%s] Starting: Dual camera streaming server & web interface on RPi 5'
                '\n\t\t\t\t-> with two 8MP RPi cameras v.2 at size: %r/%r px'
              '\n\t\t\t\t-> starting up at flip: %r/%r, offset: 0-%r/0-%r px'
                '\n\t\t\t\t-> capturing at framerate: %r fps, size: %r/%r px'
            '\n\t\t\t\t-> streaming h264 video frame by frame over WebSocket'
                         '\n\t\t\t\t=> run browser at address: http://%s:%r/') % 
    (time.strftime("%Y-%m-%d %X"), frameOffsetX0m, frameOffsetY0m, framehFlip0, 
     framevFlip0, frameOffsetX0m - frameWidth, frameOffsetY0m - frameHeight, 
     frameRate, frameWidth, frameHeight, hostIPAddr, serverPort))

try:
    # streamer pipe set up and cameras start up
    streamer0.start()
    streamer1.start()

    # web application set up and main loop start
    application = tornado.web.Application(requestHandlers)
    application.listen(serverPort)
    loop = tornado.ioloop.IOLoop.current()
    streamer0.setLoop(loop)
    streamer1.setLoop(loop)
    loop.start()
except KeyboardInterrupt:
    streamer0.stop()
    streamer1.stop()
    loop.stop()


