'''
    主程序入口
'''

import setting, time
from pwm import PWMs
from ps2 import PS2
from uart import UART2
import motion as mn
import remote as rm

def main():
    ctrl = PWMs(PINs, FREQ)
    mn.initial(ctrl)
    mv = mn.MOVE()
    ps2 = PS2(DAT_PIN, CMD_PIN, SEL_PIN, CLK_PIN)
    rm.initial(ps2)
    pctrl = rm.PS2CTRL()
    uart = UART2()
    while True:
        if not ps2.read():
            continue
        if rm.handler(ps2,ctrl,mv,pctrl):
            break
        msg = uart.poll()
        if msg:
            print(int(time.time()*1000))
            print("Received:", msg)
            uart.send(msg)
        if msg == 'q':
            break
        time.sleep_ms(READ_DELAY_MS)
    ctrl.close()
    uart.close()

if __name__ == "__main__":
    main()