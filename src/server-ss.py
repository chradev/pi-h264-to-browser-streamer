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

# Default properties and parce arguments
# python3 server-ss.py -n 0 -p 8000 -r 30 -X 700 -Y 200 -W 1600 -H 1200 -f 1 1
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--preView",       action='store_true', default=False)
parser.add_argument("-n", "--cameraNumb",    type=int, default=0)
parser.add_argument("-p", "--serverPort",    type=int, default=8000)
parser.add_argument("-r", "--frameRate",     type=int, default=30)
parser.add_argument("-X", "--Xoffset",       type=int, default=950) #680)
parser.add_argument("-Y", "--Yoffset",       type=int, default=350) #692)
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

cropChanged = False

from subprocess import check_output
hostIPAddr = check_output(['hostname', '-I'], text=True).split()[0]

print("Camera %r at flip(%r/%r), size(%r.%r), offset(%r/%r) -> h264 video stream at %rfps -> frame by frame over WebSocket -> http://%s:%r/" % 
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


indexHtml = templatize(getFile('index-ss.html'), {'port': serverPort, 'fps': frameRate})
jmuxerJs = getFile('jmuxer.min.js')


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
        if cropChanged is True:
          # Set camera offset and zoom properties if changed
          scalerCrop = (frameOffsetX, frameOffsetY, frameWidth, frameHeight)
          picam2.set_controls({"ScalerCrop": scalerCrop})


class wsHandler(tornado.websocket.WebSocketHandler):
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
    (r"/ws/", wsHandler),
    (r"/", indexHandler),
    (r"/jmuxer.min.js", jmuxerHandler)
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

