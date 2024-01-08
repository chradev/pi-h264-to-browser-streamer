Fork of [dans98/pi-h264-to-browser](https://github.com/dans98/pi-h264-to-browser/) that supports the new picamera2 Python library.

### About

Stream hardware encoded h.264 from a Raspberry Pi equiped with a V1, V2, or HQ camera module, directly to a browser. Latency is good, maybe 1sec. If you want to go realtime, find a webrtc solution.

Tip regarding bandwidth: Tweak `qp`, e.g a value of `26` generates 5.3MBit/s of video data at 1080p, while `19` generates 30MBit/s. For raspberry pi cameras you can get away with lower compression because the cameras themselves are not super high quality. I'm running at `26`, fine for my use-case.

For more info, check the original project over at [dans98/pi-h264-to-browser](https://github.com/dans98/pi-h264-to-browser/).

### Credits

[nikola-j](https://github.com/nikola-j) made the picamera2 support in [this comment](https://github.com/dans98/pi-h264-to-browser/discussions/12#discussioncomment-7901632).
