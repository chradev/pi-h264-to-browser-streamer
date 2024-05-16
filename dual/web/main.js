window.onload = function(){	
    var jmuxer0 = new JMuxer({
    	node: 'stream0', mode: 'video', flushingTime: 0,
            fps: $fps, width: $width, height: $height, debug: false
     });
    var jmuxer1 = new JMuxer({
    	node: 'stream1', mode: 'video', flushingTime: 0,
            fps: $fps, width: $width, height: $height, debug: false
     });
    var ws0 = new WebSocket("ws://" + document.location.hostname + ":" + $port + "/cam0/");
    ws0.binaryType = 'arraybuffer';
    ws0.addEventListener('message',function(event){
    	if (!document.hidden){ jmuxer0.feed({ video: new Uint8Array(event.data) }); }
    });
    var ws1 = new WebSocket("ws://" + document.location.hostname + ":" + $port + "/cam1/");
    ws1.binaryType = 'arraybuffer';
    ws1.addEventListener('message',function(event){
    	if (!document.hidden){ jmuxer1.feed({ video: new Uint8Array(event.data) }); }
    });
    init_sliders($port, $width);
} 

