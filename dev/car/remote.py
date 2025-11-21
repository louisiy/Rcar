'''
    ps2手柄控制
'''

import setting as s
# import motion as mn
import time
import _thread

class REMOTE:
    def __init__(self,ps2):
        self.ps2 = ps2
        self.joy_active = 0
        self.joy_mode = 0
        self.car_mode = 0
        self.exit = False
        self.th = None

    def reading(self):
        while True:
            print("reading...")
            if not self.ps2.read():
                print("no read")
                continue
            if self.ps2.is_held('START') and self.ps2.is_held('SELECT'):
                print("START and SELECT pressed together. Exiting...")
                self.exit = True
                break
            #time.sleep_ms(s.READ_DELAY_MS)

    def listen(self):
        self.th = _thread.start_new_thread(self.reading,())

    def initial(self):
        error = self.ps2.config(pressure=True, rumble=True)
        if error:
            print("Error configuring PS2")
            while True:
                pass
        print("Found PS2, configured successful")
        if self.ps2.is_rumble_enabled:
            print("Vibrating controller for 1 second...")
            self.ps2.read(True, 255)
            time.sleep(1)
            self.ps2.read(False, 0)
        print("Controller is ready. Press START + SELECT together to exit.")
        #self.listen()

    def stop(self):
        _thread.exit()

if __name__ == "__main__":
    from ps2 import PS2
    def ps2_test(ps2):
        for name in s.BUTTONS:
            if ps2.is_held(name):
                print(f"{name} is being held")
        if ps2.is_pressure_enabled:
            if ps2.is_held('L1') or ps2.is_held('R1'):
                value = ps2.get_joysticks("all")
                for axis, val in value.items():
                    print(f"{axis.upper()} = {val}")
        return 0

    ps2 = PS2(s.DAT_PIN, s.CMD_PIN, s.SEL_PIN, s.CLK_PIN)
    rm = REMOTE(ps2)
    rm.initial()
    while not rm.exit:
        ps2_test(ps2)
    rm.stop()