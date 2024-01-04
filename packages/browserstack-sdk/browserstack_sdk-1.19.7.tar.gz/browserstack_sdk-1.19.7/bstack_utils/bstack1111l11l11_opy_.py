# coding: UTF-8
import sys
bstack11111ll_opy_ = sys.version_info [0] == 2
bstack1lll1ll_opy_ = 2048
bstack1l11l1l_opy_ = 7
def bstack111ll11_opy_ (bstack1111lll_opy_):
    global bstack111111_opy_
    bstack11l11l1_opy_ = ord (bstack1111lll_opy_ [-1])
    bstack1ll11l_opy_ = bstack1111lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack11l11l1_opy_ % len (bstack1ll11l_opy_)
    bstack1llllll_opy_ = bstack1ll11l_opy_ [:bstack1ll1lll_opy_] + bstack1ll11l_opy_ [bstack1ll1lll_opy_:]
    if bstack11111ll_opy_:
        bstack1l111l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1ll_opy_ - (bstack11111l_opy_ + bstack11l11l1_opy_) % bstack1l11l1l_opy_) for bstack11111l_opy_, char in enumerate (bstack1llllll_opy_)])
    else:
        bstack1l111l1_opy_ = str () .join ([chr (ord (char) - bstack1lll1ll_opy_ - (bstack11111l_opy_ + bstack11l11l1_opy_) % bstack1l11l1l_opy_) for bstack11111l_opy_, char in enumerate (bstack1llllll_opy_)])
    return eval (bstack1l111l1_opy_)
import threading
bstack1111l111ll_opy_ = 1000
bstack1111l1l1l1_opy_ = 5
bstack1111l11l1l_opy_ = 30
bstack1111l1l111_opy_ = 2
class bstack1111l1111l_opy_:
    def __init__(self, handler, bstack1111l11111_opy_=bstack1111l111ll_opy_, bstack1111l1l11l_opy_=bstack1111l1l1l1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1111l11111_opy_ = bstack1111l11111_opy_
        self.bstack1111l1l11l_opy_ = bstack1111l1l11l_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1111l11ll1_opy_()
    def bstack1111l11ll1_opy_(self):
        self.timer = threading.Timer(self.bstack1111l1l11l_opy_, self.bstack11111lllll_opy_)
        self.timer.start()
    def bstack1111l111l1_opy_(self):
        self.timer.cancel()
    def bstack1111l11lll_opy_(self):
        self.bstack1111l111l1_opy_()
        self.bstack1111l11ll1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1111l11111_opy_:
                t = threading.Thread(target=self.bstack11111lllll_opy_)
                t.start()
                self.bstack1111l11lll_opy_()
    def bstack11111lllll_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1111l11111_opy_]
        del self.queue[:self.bstack1111l11111_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1111l111l1_opy_()
        while len(self.queue) > 0:
            self.bstack11111lllll_opy_()