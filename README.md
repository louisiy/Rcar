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

apriltag识别

YOLOv5识别

串口监听

WIFI热点AP模式

### 车座

pwm电机驱动

ps2手柄控制

循迹控制

超声探距

串口发送

### 机械臂

不同任务的姿态点记录

姿态点间的移动

通信

### ESP32-C3

外设通信


https://www.nologo.tech/product/esp32/esp32c3/esp32c3supermini/esp32C3SuperMini.html