var ptz;

const etxt0 = document.querySelector("#text0");
const elin0 = document.querySelector("#line0");
const edef0 = document.querySelector("#defs0");
const etxt1 = document.querySelector("#text1");
const elin1 = document.querySelector("#line1");
const edef1 = document.querySelector("#defs1");
const xvalue = document.querySelector("#xvalue");
const xinput = document.querySelector("#xoffset");
const yvalue = document.querySelector("#yvalue");
const yinput = document.querySelector("#yoffset");
const zvalue = document.querySelector("#zvalue");
const zinput = document.querySelector("#zoffset");
const xvalue0 = document.querySelector("#xvalue0");
const xinput0 = document.querySelector("#xoffset0");
const yvalue0 = document.querySelector("#yvalue0");
const yinput0 = document.querySelector("#yoffset0");
const xvalue1 = document.querySelector("#xvalue1");
const xinput1 = document.querySelector("#xoffset1");
const yvalue1 = document.querySelector("#yvalue1");
const yinput1 = document.querySelector("#yoffset1");

const hflip0 = document.querySelector("#hflip0");
const vflip0 = document.querySelector("#vflip0");
const pause0 = document.querySelector("#pause0");
const hflip1 = document.querySelector("#hflip1");
const vflip1 = document.querySelector("#vflip1");
const pause1 = document.querySelector("#pause1");

function init_sliders(port, width) {
  ptz = new WebSocket("ws://" + document.location.hostname + ":" + port + "/ptz/");
  ptz.addEventListener('message',function(event){
    const data = JSON.parse(event.data);
//    console.log(data);

    hflip0.checked = data[0].f.hor;
    vflip0.checked = data[0].f.ver;
    pause0.checked = data[0].f.pau;

    hflip1.checked = data[1].f.hor;
    vflip1.checked = data[1].f.ver;
    pause1.checked = data[1].f.pau;

    etxt0.checked = data[0].e.txt;
    elin0.checked = data[0].e.lin;
    edef0.checked = false;

    etxt1.checked = data[1].e.txt;
    elin1.checked = data[1].e.lin;
    edef1.checked = false;

    xinput0.min = data[0].x.min;
    xinput0.max = data[0].x.max;
    xinput0.value = data[0].x.val;
    xvalue0.textContent = xinput0.value;

    yinput0.min = data[0].y.min;
    yinput0.max = data[0].y.max;
    yinput0.value = data[0].y.val;
    yvalue0.textContent = yinput0.value;

    xinput1.min = data[1].x.min;
    xinput1.max = data[1].x.max;
    xinput1.value = data[1].x.val;
    xvalue1.textContent = xinput1.value;

    yinput1.min = data[1].y.min;
    yinput1.max = data[1].y.max;
    yinput1.value = data[1].y.val;
    yvalue1.textContent = yinput1.value;

    xinput.min = data[2].x.min;
    xinput.max = data[2].x.max;
    xinput.value = data[2].x.val;
    xvalue.textContent = xinput.value;

    yinput.min = data[2].y.min;
    yinput.max = data[2].y.max;
    yinput.value = data[2].y.val;
    yvalue.textContent = yinput.value;

    zinput.min = data[2].z.min;
    zinput.max = data[2].z.max;
    zinput.value = data[2].z.val;
    zvalue.textContent = zinput.value;
  });

  xinput.style["width"] = width * 7 / 4 + 'px';
  xvalue.textContent = xinput.value;
  xinput.addEventListener("input", (event) => {
    xvalue.textContent = event.target.value;
    ptz.send(ptz_send());
  });
  yinput.style["width"] = width * 7 / 4 + 'px';
  yvalue.textContent = yinput.value;
  yinput.addEventListener("input", (event) => {
    yvalue.textContent = event.target.value;
    ptz.send(ptz_send());
  });
  zinput.style["width"] = width * 7 / 4 + 'px';
  zvalue.textContent = parseFloat(zinput.value).toFixed(2);
  zinput.addEventListener("input", (event) => {
    zvalue.textContent = parseFloat(event.target.value).toFixed(2);
    ptz.send(ptz_send());
  });

  xinput0.style["width"] = width * 3 / 4 + 'px';
  xvalue0.textContent = xinput0.value;
  xinput0.addEventListener("input", (event) => {
    xvalue0.textContent = event.target.value;
    ptz.send(ptz_send());
  });
  yinput0.style["width"] = width * 3 / 4 + 'px';
  yvalue0.textContent = yinput0.value;
  yinput0.addEventListener("input", (event) => {
    yvalue0.textContent = event.target.value;
    ptz.send(ptz_send());
  });

  xinput1.style["width"] = width * 3 / 4 + 'px';
  xvalue1.textContent = xinput1.value;
  xinput1.addEventListener("input", (event) => {
    xvalue1.textContent = event.target.value;
    ptz.send(ptz_send());
  });
  yinput1.style["width"] = width * 3 / 4 + 'px';
  yvalue1.textContent = yinput1.value;
  yinput1.addEventListener("input", (event) => {
    yvalue1.textContent = event.target.value;
    ptz.send(ptz_send());
  });
}

function ptz_send() {
  var data = [
                { 'cam': 0,
                  'f': {
                      'hor': hflip0.checked ? 1 : 0,
                      'ver': vflip0.checked ? 1 : 0,
                      'pau': pause0.checked ? 1 : 0
                  },
                  'e': {
                      'txt': etxt0.checked,
                      'lin': elin0.checked,
                      'def': edef0.checked
                  },
                  'x': {
                    'min': parseInt(xinput0.min),
                    'val': parseInt(xinput0.value),
                    'max': parseInt(xinput0.max)
                  },
                  'y': {
                    'min': parseInt(yinput0.min),
                    'val': parseInt(yinput0.value),
                    'max': parseInt(yinput0.max)
                  }
                }, 
                { 'cam': 1,
                  'f': {
                      'hor': hflip1.checked ? 1 : 0,
                      'ver': vflip1.checked ? 1 : 0,
                      'pau': pause1.checked ? 1 : 0
                  },
                  'e': {
                      'txt': etxt1.checked,
                      'lin': elin1.checked,
                      'def': edef1.checked
                  },
                  'x': {
                    'min': parseInt(xinput1.min),
                    'val': parseInt(xinput1.value),
                    'max': parseInt(xinput1.max)
                  },
                  'y': {
                    'min': parseInt(yinput1.min),
                    'val': parseInt(yinput1.value),
                    'max': parseInt(yinput1.max)
                  }
                },
                { 'cam': 2,
                  'x': {
                    'min': parseInt(xinput.min),
                    'val': parseInt(xinput.value),
                    'max': parseInt(xinput.max)
                  },
                  'y': {
                    'min': parseInt(yinput.min),
                    'val': parseInt(yinput.value),
                    'max': parseInt(yinput.max)
                  },
                  'z': {
                  'min': parseFloat(zinput.min),
                  'val': parseFloat(zinput.value),
                  'max': parseFloat(zinput.max)
                }
              }
  ];
//  console.log(JSON.stringify(data));
  return JSON.stringify(data);
};
function handleCbClick(cb) {
  ptz.send(ptz_send());
}

