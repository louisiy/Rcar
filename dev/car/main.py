'''
    主程序入口
'''

import setting as s
import time
from pwm import PWMs
from ps2 import PS2
from uart import UART2
import motion
import remote

def main():
    pwms = PWMs(s.PINs, s.FREQ)
    mv = motion.MOTION(pwms)
    mv.initial()

    ps2 = PS2(s.DAT_PIN, s.CMD_PIN, s.SEL_PIN, s.CLK_PIN)
    rm = remote.REMOTE(ps2,mv)
    rm.initial()

    #uart = UART2()

    while True:
        if rm.exit:
            rm.stop()
        #msg = uart.poll()
#         if msg:
#             print(int(time.time()*1000))
#             print("Received:", msg)
#             uart.send(msg)
#         if msg == 'q':
#             break
        time.sleep_ms(s.READ_DELAY_MS)
    pwms.close()
#     uart.close()

if __name__ == "__main__":
    main()