'''
    主程序入口 ID:CAR
'''

import setting as s
import time
from pwm import PWMs
from ps2 import PS2
from uart import UART2
import motion
import remote
import cmd

def main():
    pwms = PWMs(s.PINs, s.FREQ)
    mv = motion.MOTION(pwms)
    mv.initial()

    ps2 = PS2(s.DAT_PIN, s.CMD_PIN, s.SEL_PIN, s.CLK_PIN)
    rm = remote.REMOTE(ps2,mv)
    rm.initial()

    uart = UART2()
    uart.send("CAR:HELLO\n")
    uart.start()
    uart.cb = lambda raw: cmd.dispatch(uart, raw)

    while True:
        if getattr(rm, "task_start", True):
            print("[CAR] 结束手柄控制，任务正式开始")
            uart.send("CAR:GOGOGO")
            rm.task_start = False
        time.sleep(0.02)
    pwms.close()
    uart.stop()
    uart.close()

if __name__ == "__main__":
    main()