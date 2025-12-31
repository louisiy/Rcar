# Rcar

## 架构

MaixCam视觉+主控

车座 ESP32

- 通过UART直连MaixCam

机械臂

- TCP转UART直连MaixCam

移液枪（外设）

- ESP32-C3，5V供电，驱动舵机，WIFI与MaixCam连接

注射泵（外设）

- RS232转UART连接ESP32-C3，WIFI与MaixCam连接

## 组成部分

### MaixCam CAM

#### 功能

apriltag识别、颜色识别、串口监听、WIFI热点AP模式、TCP通信、任务管理、总线管理、视频管理、日志管理、命令处理、flask服务监看

原yolo功能代码已完善但已移除，代码可在`waste/yolo.py`查看

#### 模块代码介绍

##### 应用层

`main.py`程序入口，这里会调用各个模块来运行实际需要运行的任务

`state.py`定义了任务列表与状态

##### 硬件抽象层

`uart.py`定义了uart通信端口

`wifi.py`定义了WiFi AP热点

`tcp.py`定义了TCP服务器

`bus.py`定义了通信总线

`video.py`定义了摄像头和视频显示、推流

`log.py`定义了日志管理

`web.py`定义了flask服务

##### 逻辑执行层

`atag.py`定义实现了apriltag的识别

`color.py`定义实现了色块识别

`cmd.py`定义了命令处理

------

### 车座 CAR

#### 功能

pwm电机驱动、ps2手柄控制、循迹控制、串口发送

超声探距已完善但已移除，代码可在`waste/hcsr.py`查看

#### 模块代码介绍

`waste/ps2.c`是课程例程ps2手柄相关的c源码，课程例程的python源码截取改写自该程序，来源网络

##### 应用层

`main.py`程序入口，这里会调用各个模块来运行实际需要运行的任务

`setting.py`所有的常量，如针脚编号，存放归纳

##### 硬件抽象层

`pwm.py`定义了每个PWM输出引脚端口，即定义了所有的车轮

`ps2.py`定义了PS2手柄

`uart.py`定义了uart通信端口

`tcrt.py`定义了循迹传感器TCRT5000

##### 逻辑执行层

`motion.py`定义了如何调用PWM输出引脚来完成车座的运动的方法

`remote.py`定义了如何通过PS2手柄按键摇杆来控制车座的移动

`cmd.py`定义了命令处理

------

### 机械臂 ARM

#### 功能

不同任务的姿态点记录、姿态点间的移动、通信

#### 模块代码介绍

`main.py`定义了tcp连接和信息分发函数

`var.py`定义了所有具体的执行代码

------

### 移液枪舵机 PITE

#### 功能

与MaixCam主机TCP通信

驱动舵机

命令处理

------

### 注射泵 PUMP

#### 功能

与MaixCam主机TCP通信

与注射泵RS232转uart通信

命令处理

