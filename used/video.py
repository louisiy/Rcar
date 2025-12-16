from maix import camera,display
import threading
import time

class VIDEO:
    def __init__(self, at, ch, state, bus):
        self.cam = camera.Camera(640,480)
        self.dis = display.Display()
        self.at = at
        self.ch = ch
        self.s = state
        self.b = bus
        self._run = False

    def start(self):
        if self._run:
            return
        self._run = True
        t = threading.Thread(target=self.loop)
        t.start()
        #log("[VIDEO] 视频开始")

    def stop(self):
        self._run = False
        #log("[VIDEO] 视频结束")

    def loop(self):
        while self._run and not app.need_exit():
            img = self.cam.read()
            if self.s.at:
                img = self.at.search(img)
                if not self.at.err:
                    msg = "ATAG=" + self.at.xyz()
                    self.b.send("ARM", msg)
                    self.s.at = False
                    #log("[VIDEO]", msg)
            if self.s.ch:
                img = self.ch.search(img)
                if not self.ch.err:
                    msg = "PHASE=" + self.ch.dis()
                    self.b.send("ARM", msg)
                    self.s.ch = False
                    #log("[VIDEO]", msg)

            self.dis.show(img)
            # TODO: 做完推流
            #webui.push_frame(img)
            time.sleep(0.01)