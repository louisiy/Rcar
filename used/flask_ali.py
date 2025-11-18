from flask import Flask, request, Response, render_template_string, send_file, send_from_directory
from maix import camera, time, app,  display, image, uart
import threading

app = Flask(__name__)

# 初始化摄像头
cam = camera.Camera(640, 480,  fps=60 )
cam.skip_frames(30)   #跳过开头帧
disp = display.Display()
# 串口初始化
device = "/dev/ttyS0"
serial = uart.UART(device, 115200)

HTML_TEMPLATE = """
<!DOCTYPE html> =
<html>
<head>
    <title>MaixCam Web</title>
    <link rel="icon" src="/tp/WYBZ.jpg" type="image/jpeg">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f0f0f0;
        }

        .video-container {
            margin: 20px auto;
            width: 640px;
            height: 480px;
            border: 2px solid #333;
        }

        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .button-group {
            margin-top: 20px;
        }

        button {
            padding: 10px 20px;
            margin: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        .result { 
            margin-top: 10px; 
            font-weight: bold; 
            background-color: #8E44AD; /* 紫色背景 */
            color: #ffffff; /* 白色文字 */ 
        }
    </style>
</head>
<body>
    <h1>Tsinghua car test</h1>
    <div class="video-container">
        <img src="/stream1" alt="实时视频流">
    </div>
    <div class="button-group">
        <button onclick="executeAction1(event, '/anjian_1')" style="width: 10%; ">测试1</button>
        <button onclick="executeAction1(event, '/anjian_2')" style="width: 10%; ">测试2</button>
        <button onclick="executeAction1(event, '/anjian_3')" style="width: 10%; ">测试3</button>
        <button onclick="executeAction1(event, '/anjian_4')" style="width: 10%; ">测试4</button>
    </div>
    <!-- 设置成功提示框（页面最底部） -->
    <div id="bottom-feedback1"></div>
<script>
    function executeAction1(event1, endpoint) {
        const btn = event1.target;
        btn.disabled = true;
        btn.style.opacity = 0.6;

        fetch(endpoint, {
                method: "POST"
            })
        .then(response => {
                if (!response.ok) {
                throw new Error("Network response was not ok");
                }
                return response.json();
            })
        .then(data => {
                const feedback = document.getElementById("bottom-feedback1");
                if (data.status === "success") {
                feedback.textContent = data.message;
                feedback.classList.remove("error");

                } else {
                feedback.textContent = data.message;
                feedback.classList.add("error");
                }
            })
        .catch(error => {
                console.error("Error:", error);
                document.getElementById("bottom-feedback1").textContent = "操作失败，请重试。";
            })
        .finally(() => {
                btn.disabled = false;
                btn.style.opacity = 1;
            });
        }
</script>
</body>
</html>
"""

def vedio1(): # 摄像头图像
    while 1:
        img = cam.read()
        disp.show(img)
        jpg1 = img.to_jpeg().to_bytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg1 + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/stream1")
def video_feed1():
    return Response(vedio1(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/anjian_1", methods=["POST"])
def anjian_1():  
    return {"status": "success", "message": "测试1OK"}

@app.route("/anjian_2", methods=["POST"])
def anjian_2():  
                       # 
    return {"status": "success", "message": "测试2OK"}

@app.route("/anjian_3", methods=["POST"])
def anjian_3():  
                        # 
    return {"status": "success", "message": "测试3OK"}

@app.route("/anjian_4", methods=["POST"])
def anjian_4():  
                        # 
    return {"status": "success", "message": "测试4OK"}

def run_flask():
    app.run(host="0.0.0.0", port=8000)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    while 1 :
        time.sleep(2)