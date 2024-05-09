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

from libcamera import Transform

# use sudo apt install python3-opencv
import cv2
import time
from picamera2 import MappedArray

colour = (0, 255, 0)
origin = (0, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

def apply_timestamp(request):
    timestamp = time.strftime("%Y-%m-%d %X")
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)

# start configuration
serverPort = 8000
frameRate = 30
frameWidth = 960
frameHeight = 1080
frameTransform = 180

picam20 = Picamera2(0)
picam21 = Picamera2(1)

picam20.configure(picam20.create_video_configuration(main={"size": (frameWidth, frameHeight)}, transform=Transform(frameTransform) ))
picam21.configure(picam21.create_video_configuration(main={"size": (frameWidth, frameHeight)}, transform=Transform(frameTransform) ))

picam20.pre_callback = apply_timestamp
picam21.pre_callback = apply_timestamp

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

indexHtml  = templatize(getFile('index.html'), {'port': serverPort, 'width': frameWidth, 'height': frameHeight, 'fps': frameRate})
jmuxerJs = getFile('jmuxer.min.js')

class StreamingOutput0(Output):
    def __init__(self):
        super().__init__()
        self.loop = None
        self.buffer = io.BytesIO()

        # Test camera "movement"
        self.offsetX = 0
        self.offmaxX = 2320
        self.crop = (1160, 692, 960, 1080)

    def setLoop(self, loop):
        self.loop = loop

    def outputframe(self, frame, keyframe=True, timestamp=None):
        self.buffer.write(frame)
        if self.loop is not None and ws0Handler.hasConnections():
            self.loop.add_callback(callback=ws0Handler.broadcast, message=self.buffer.getvalue())
        self.buffer.seek(0)
        self.buffer.truncate()

        # Test camera "movement"
        if self.offsetX == self.offmaxX:
            self.offsetX = 0
        else:
            self.offsetX = self.offsetX + 1
        self.crop = (self.offsetX, 360, 960, 1080)
        picam20.set_controls({"ScalerCrop": self.crop})

class StreamingOutput1(Output):
    def __init__(self):
        super().__init__()
        self.loop = None
        self.buffer = io.BytesIO()

        # Test camera "movement"
        self.offsetX = 620
        self.offmaxX = 2320
        self.crop = (1160, 692, 960, 1080)

    def setLoop(self, loop):
        self.loop = loop

    def outputframe(self, frame, keyframe=True, timestamp=None):
        self.buffer.write(frame)
        if self.loop is not None and ws1Handler.hasConnections():
            self.loop.add_callback(callback=ws1Handler.broadcast, message=self.buffer.getvalue())
        self.buffer.seek(0)
        self.buffer.truncate()

        # Test camera "movement"
        if self.offsetX == self.offmaxX:
            self.offsetX = 0
        else:
            self.offsetX = self.offsetX + 1
        self.crop = (self.offsetX, 360, 960, 1080)
        picam21.set_controls({"ScalerCrop": self.crop})

class ws0Handler(tornado.websocket.WebSocketHandler):
    connections = []

    def open(self):
        self.connections.append(self)

    def on_close(self):
        self.connections.remove(self)

    def on_message(self, message):
        pass

    @classmethod
    def hasConnections(cl):
        if len(cl.connections) == 0:
            return False
        return True

    @classmethod
    async def broadcast(cl, message):
        for connection in cl.connections:
            try:
                await connection.write_message(message, True)
            except tornado.websocket.WebSocketClosedError:
                pass
            except tornado.iostream.StreamClosedError:
                pass

    def check_origin(self, origin):
        return True

class ws1Handler(tornado.websocket.WebSocketHandler):
    connections = []

    def open(self):
        self.connections.append(self)

    def on_close(self):
        self.connections.remove(self)

    def on_message(self, message):
        pass

    @classmethod
    def hasConnections(cl):
        if len(cl.connections) == 0:
            return False
        return True

    @classmethod
    async def broadcast(cl, message):
        for connection in cl.connections:
            try:
                await connection.write_message(message, True)
            except tornado.websocket.WebSocketClosedError:
                pass
            except tornado.iostream.StreamClosedError:
                pass

    def check_origin(self, origin):
        return True

class indexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(indexHtml)

class jmuxerHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/javascript')
        self.write(jmuxerJs)

requestHandlers = [
    (r"/cam0/", ws0Handler),
    (r"/cam1/", ws1Handler),
    (r"/", indexHandler),
    (r"/jmuxer.min.js", jmuxerHandler)
]

try:
    output0 = StreamingOutput0()
    output1 = StreamingOutput1()
    encoder0 = H264Encoder(repeat=True, framerate=frameRate, qp=23)
    encoder1 = H264Encoder(repeat=True, framerate=frameRate, qp=23)
    encoder0.output = output0
    encoder1.output = output1
    picam20.start_recording(encoder0, output0)
    picam21.start_recording(encoder1, output1)

    application = tornado.web.Application(requestHandlers)
    application.listen(serverPort)
    loop = tornado.ioloop.IOLoop.current()
    output0.setLoop(loop)
    output1.setLoop(loop)
    loop.start()
except KeyboardInterrupt:
    picam20.stop_recording()
    picam21.stop_recording()
    loop.stop()

