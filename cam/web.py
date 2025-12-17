'''
    flask推流服务器
'''


import threading
import time
import logging

from flask import Flask, Response, jsonify, request
import log

_latest_jpeg = b""


def update(jpeg_bytes: bytes):
    global _latest_jpeg
    _latest_jpeg = jpeg_bytes


app = Flask(__name__)


@app.get("/")
def index():
    html = """
<!doctype html>
<html>
<head>
  <meta charset='utf-8'/>
  <meta name='viewport' content='width=device-width, initial-scale=1'/>
  <title>MaixCam</title>
  <style>
    body{margin:0;font-family:monospace;}
    .wrap{display:flex;height:100vh;}
    .left{flex:1;display:flex;align-items:center;justify-content:center;background:#000;}
    .left img{max-width:100%;max-height:100%;}
    .right{width:45vw;max-width:600px;border-left:1px solid #ddd;overflow:auto;padding:10px;}
    .line{white-space:pre-wrap;word-break:break-word;margin:0 0 6px 0;}
  </style>
</head>
<body>
  <div class='wrap'>
    <div class='left'>
      <img src='/stream.mjpg' />
    </div>
    <div class='right' id='log'></div>
  </div>

<script>
let since = 0;
const box = document.getElementById('log');

function append(lines){
  for (const s of lines){
    const p = document.createElement('div');
    p.className = 'line';
    p.textContent = s;
    box.appendChild(p);
  }
  box.scrollTop = box.scrollHeight;
}

async function loop(){
  while (true){
    try{
      const r = await fetch('/logs?since=' + since);
      const j = await r.json();
      since = j.latest;
      append(j.lines);
    }catch(e){
      console.log('log fetch failed:', e);
    }
    await new Promise(res => setTimeout(res, 300));
  }
}

loop();
</script>

</body>
</html>"""
    return html


@app.get("/logs")
def logs():
    since = request.args.get("since", "0")
    since = int(since) if since.isdigit() else 0
    items, latest = log.read_since(since)
    lines = [line for _, line in items]
    return jsonify({"latest": latest, "lines": lines})


@app.get("/stream.mjpg")
def stream():
    def gen():
        boundary = b"frame"
        while True:
            if _latest_jpeg:
                yield b"--" + boundary + b"\r\n"
                yield b"Content-Type: image/jpeg\r\n\r\n" + _latest_jpeg + b"\r\n"
            time.sleep(0.03)
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")


def start(host="0.0.0.0", port=5000):
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    t = threading.Thread(
        target=lambda: app.run(host=host, port=port, threaded=True, use_reloader=False),
        daemon=True
    )
    t.start()
    log.info(f"[WEB] Flask 服务器运行 http://{host}:{port}")
    return t
