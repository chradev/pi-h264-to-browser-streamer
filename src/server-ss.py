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

import sys, argparse

# Default properties and parce arguments and secon camera
# python3 server-ss.py -n 1 -p 8001 -X 1750 -Y 340
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--preView",       action='store_true', default=False)
parser.add_argument("-n", "--cameraNumb",    type=int, default=0)
parser.add_argument("-p", "--serverPort",    type=int, default=8000)
parser.add_argument("-r", "--frameRate",     type=int, default=30)
parser.add_argument("-X", "--Xoffset",       type=int, default=930) #680)
parser.add_argument("-Y", "--Yoffset",       type=int, default=400) #692)
parser.add_argument("-W", "--Width",         type=int, default=1000) #1920)
parser.add_argument("-H", "--Height",        type=int, default=1000) #1080)
parser.add_argument("-f", "--Flip", nargs=2, type=int, default=(1, 1))
args = parser.parse_args()
print('Arguments', args)

enableView   = args.preView
picam2Numb   = args.cameraNumb
serverPort   = args.serverPort
frameRate    = args.frameRate
frameOffsetX = args.Xoffset
frameOffsetY = args.Yoffset
frameWidth   = args.Width
frameHeight  = args.Height
framehFlip   = args.Flip[0]
framevFlip   = args.Flip[1]

from subprocess import check_output
hostIPAddr = check_output(['hostname', '-I'], text=True).split()[0]

print("Camera %r at flip(%r/%r), size(%rx%r), offset(%r/%r) -> h264 video stream at %rfps -> frame by frame over WebSocket -> http://%s:%r/" % 
     (picam2Numb, framehFlip, framevFlip, frameWidth, frameHeight, frameOffsetX, frameOffsetY, frameRate, hostIPAddr, serverPort))

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
    timestamp = time.strftime("%Y-%m-%d %X") + " - Camera: " + str(picam2Numb)
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)

from libcamera import Transform
picam2 = Picamera2(picam2Numb)
picam2.configure(picam2.create_video_configuration(main={"size": (frameWidth, frameHeight)}, transform=Transform(hflip=framehFlip, vflip=framevFlip) ))

# Set camera offset and zoom properties
scalerCrop = (frameOffsetX, frameOffsetY, frameWidth, frameHeight)
picam2.set_controls({"ScalerCrop": scalerCrop})
print("Camera ScalerCrop properties:", picam2.camera_controls["ScalerCrop"])

# add calback to print time stamp on the frame
picam2.pre_callback = apply_timestamp

from picamera2 import Preview
if enableView is True:
    picam2.start_preview(Preview.QTGL)

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

full_camera_res = picam2.camera_properties['PixelArraySize']

jmuxerJs = getFile('jmuxer.min.js')
styleCSS = getFile('clock-style.css')
clockSVG = getFile('clock.svg')
indexHtml  = templatize(getFile('index-ss.html'), {'port': serverPort, 'width': frameWidth, 'height': frameHeight, 'xmax': full_camera_res[0] - frameWidth, 'ymax': full_camera_res[1] - frameHeight, 'fps': frameRate})


class StreamingOutput(Output):
    def __init__(self):
        super().__init__()
        self.loop = None
        self.buffer = io.BytesIO()

    def setLoop(self, loop):
        self.loop = loop

    def outputframe(self, frame, keyframe=True, timestamp=None):
        self.buffer.write(frame)
        if self.loop is not None and wsHandler.hasConnections():
            self.loop.add_callback(callback=wsHandler.broadcast, message=self.buffer.getvalue())
        self.buffer.seek(0)
        self.buffer.truncate()


class wsHandler(tornado.websocket.WebSocketHandler):
    connections = []
    OffsetX = frameOffsetX
    OffsetY = frameOffsetY
    Width = frameWidth
    Height = frameHeight
    Zoom = 1

    def open(self):
        self.connections.append(self)

    def on_close(self):
        self.connections.remove(self)

    def on_message(self, message):
        if message.split(':')[0] == 'X':
            self.OffsetX = int(message.split(':')[1])
        elif message.split(':')[0] == 'Y':
            self.OffsetY = int(message.split(':')[1])
        elif message.split(':')[0] == 'Z':
            self.Zoom = float(message.split(':')[1])
        scalerCrop = (self.OffsetX, self.OffsetY, int(self.Width * self.Zoom), int(self.Height * self.Zoom))
        picam2.set_controls({"ScalerCrop": scalerCrop})

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

class styleHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/css')
        self.write(styleCSS)

class clocksvgHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'image/svg+xml')
        self.write(clockSVG)


requestHandlers = [
    (r"/ws/", wsHandler),
    (r"/", indexHandler),
    (r"/jmuxer.min.js", jmuxerHandler),
    (r"/clock-style.css", styleHandler),
    (r"/clock.svg", clocksvgHandler)
]

try:
    output = StreamingOutput()
    encoder = H264Encoder(repeat=True, framerate=frameRate, qp=23)
    encoder.output = output
    picam2.start_recording(encoder, output)

    application = tornado.web.Application(requestHandlers)
    application.listen(serverPort)
    loop = tornado.ioloop.IOLoop.current()
    output.setLoop(loop)
    loop.start()
except KeyboardInterrupt:
    picam2.stop_recording()
    loop.stop()

