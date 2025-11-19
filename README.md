# Rcar

## 架构

MaixCam视觉+主控

车座 ESP32

- 通过UART直连MaixCam

机械臂

- TCP转UART直连MaixCam

移液枪（外设）

- ESP32-C3，5V供电，驱动舵机，WIFI与MaixCam连接

天平（外设）

- 待确认串口形式，但通过ESP32-C3转WIFI与MaixCam连接

搅拌电机（外设）

- 待确认串口形式，但通过ESP32-C3转WIFI与MaixCam连接

## 组成部分

### MaixCam

#### 预期功能

apriltag识别、YOLOv5识别、串口监听、WIFI热点AP模式、TCP通信

#### 模块代码介绍

##### 应用层

`main.py`

程序入口，这里会调用各个模块来运行实际需要运行的任务

##### 硬件抽象层

`uart.py`

定义了uart通信端口

`wifi.py`

定义了WiFi AP热点

`tcp.py`

定义了TCP服务器

##### 逻辑执行层

`atag.py`

定义实现了apriltag的识别

`yolo.py`

定义实现了YOLOv5模型的识别

`color.py`

定义实现了色块识别

##### TODO

希望完成TCP通信的逻辑执行层代码`device.py`

斟酌考虑是否需要把2个UART通信、3个TCP通信封装为一个逻辑执行层

### 车座

#### 预期功能

pwm电机驱动、ps2手柄控制、循迹控制、超声探距、串口发送

#### 模块代码介绍

##### 应用层

`main.py`

程序入口，这里会调用各个模块来运行实际需要运行的任务

`setting.py`

所有的常量，如针脚编号，存放归纳

##### 硬件抽象层

`pwm.py`

定义了每个PWM输出引脚端口，即定义了所有的车轮

`ps2.py`

定义了PS2手柄

`uart.py`

定义了uart通信端口

`hcsr.py`

定义了超声波测距传感器HC-SR04

`tcrt.py`

定义了循迹传感器TCRT5000

##### 逻辑执行层

`motion.py`

定义了如何调用PWM输出引脚来完成车座的运动的方法

`remote.py`

定义了如何通过PS2手柄按键摇杆来控制车座的移动

#### TODO

希望完成mode+select实现切换

- PS2手动模式
- MaixCam主机通讯控制模式

且不能同时控制

希望完成循迹传感器控制车座具体运动的逻辑层代码`follow.py`

希望完善PS2手柄的按键识别逻辑

### 机械臂

#### 预期功能

不同任务的姿态点记录、姿态点间的移动、通信

#### TODO

希望完善TCP通信代码

希望实现具体任务的机械臂移动、抓取等实例逻辑实现层代码

### ESP32-C3

#### 预期功能

外设与MaixCam主机TCP通信

#### TODO

正在等货

正在学习


https://www.nologo.tech/product/esp32/esp32c3/esp32c3supermini/esp32C3SuperMini.html