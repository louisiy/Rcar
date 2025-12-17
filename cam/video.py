'''
    视频显示
'''


import threading
import time

from maix import app, camera, display

import log
import web


class VIDEO:
    def __init__(self, state, bus, at, ch, w=640, h=480):
        self.s = state
        self.b = bus
        self.at = at
        self.ch = ch
        self.w = w
        self.h = h

        self.cam = None
        self.dis = None

        self.run = False
        self.t = None

    def start(self):
        self.cam = camera.Camera(self.w, self.h)
        self.dis = display.Display()
        self.run = True
        self.t = threading.Thread(target=self._loop)
        self.t.start()
        log.info("[VIDEO] 视频开始")

    def stop(self):
        self.run = False
        time.sleep(0.05)
        if self.dis:
            self.dis.close()
        if self.cam:
            self.cam.close()
        log.info("[VIDEO] 视频结束")

    def _loop(self):
        while self.run and not app.need_exit():
            img = self.cam.read()

            if self.s.at:
                img = self.at.search(img)
                if not self.at.err:
                    msg = "ATAG=" + self.at.xyz()
                    self.b.send("ARM", msg)
                    self.s.at = False

            if self.s.ch:
                img = self.ch.search(img)
                if not self.ch.err:
                    msg = "PHASE=" + self.ch.dis()
                    self.b.send("ARM", msg)
                    self.s.ch = False

            self.dis.show(img)
            jpg = img.to_jpeg().to_bytes()
            web.update(jpg)
