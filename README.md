# Rcar

## 架构

MaixCam视觉+主控

底盘小车

机械臂



## 底盘小车

### 模块

#### `main.py`

主程序入口

#### `pwm.py`

pwm控制器类

#### `ps2.py`
```python
#CMD_READ_TYPE=[0x01, 0x45, 0x00, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A]
CMD_SET_MODE=[0x01, 0x44, 0x00, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00]
# 4th byte: 00 normal; 01 red or analog
# 5th byte: 03 lock; ee no lock
```
## 视觉、主控

### 视觉

### 通信







https://www.nologo.tech/product/esp32/esp32c3/esp32c3supermini/esp32C3SuperMini.html