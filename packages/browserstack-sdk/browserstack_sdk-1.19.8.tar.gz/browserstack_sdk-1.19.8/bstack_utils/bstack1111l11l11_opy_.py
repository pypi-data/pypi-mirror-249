# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack111ll11_opy_ = 2048
bstack11l1ll1_opy_ = 7
def bstack11lllll_opy_ (bstack11ll11_opy_):
    global bstack11ll1l_opy_
    bstack11l1lll_opy_ = ord (bstack11ll11_opy_ [-1])
    bstack1l11111_opy_ = bstack11ll11_opy_ [:-1]
    bstack1l111ll_opy_ = bstack11l1lll_opy_ % len (bstack1l11111_opy_)
    bstack1l1l1l_opy_ = bstack1l11111_opy_ [:bstack1l111ll_opy_] + bstack1l11111_opy_ [bstack1l111ll_opy_:]
    if bstack1111l11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll11_opy_ - (bstack1llll11_opy_ + bstack11l1lll_opy_) % bstack11l1ll1_opy_) for bstack1llll11_opy_, char in enumerate (bstack1l1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack111ll11_opy_ - (bstack1llll11_opy_ + bstack11l1lll_opy_) % bstack11l1ll1_opy_) for bstack1llll11_opy_, char in enumerate (bstack1l1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import threading
bstack1111l1l1l1_opy_ = 1000
bstack1111l1l11l_opy_ = 5
bstack1111l11l1l_opy_ = 30
bstack1111l1l111_opy_ = 2
class bstack11111lllll_opy_:
    def __init__(self, handler, bstack1111l111ll_opy_=bstack1111l1l1l1_opy_, bstack1111l111l1_opy_=bstack1111l1l11l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1111l111ll_opy_ = bstack1111l111ll_opy_
        self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1111l1111l_opy_()
    def bstack1111l1111l_opy_(self):
        self.timer = threading.Timer(self.bstack1111l111l1_opy_, self.bstack1111l11lll_opy_)
        self.timer.start()
    def bstack1111l11ll1_opy_(self):
        self.timer.cancel()
    def bstack1111l11111_opy_(self):
        self.bstack1111l11ll1_opy_()
        self.bstack1111l1111l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1111l111ll_opy_:
                t = threading.Thread(target=self.bstack1111l11lll_opy_)
                t.start()
                self.bstack1111l11111_opy_()
    def bstack1111l11lll_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1111l111ll_opy_]
        del self.queue[:self.bstack1111l111ll_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1111l11ll1_opy_()
        while len(self.queue) > 0:
            self.bstack1111l11lll_opy_()