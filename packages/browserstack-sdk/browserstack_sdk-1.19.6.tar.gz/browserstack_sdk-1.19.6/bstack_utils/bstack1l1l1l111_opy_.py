# coding: UTF-8
import sys
bstack1l1ll_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1l1ll1l_opy_ = 7
def bstack1lll11l_opy_ (bstack1ll11_opy_):
    global bstack11llll_opy_
    bstack1111ll1_opy_ = ord (bstack1ll11_opy_ [-1])
    bstack1111111_opy_ = bstack1ll11_opy_ [:-1]
    bstack1ll1_opy_ = bstack1111ll1_opy_ % len (bstack1111111_opy_)
    bstack1l11lll_opy_ = bstack1111111_opy_ [:bstack1ll1_opy_] + bstack1111111_opy_ [bstack1ll1_opy_:]
    if bstack1l1ll_opy_:
        bstack1ll1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack11ll11l_opy_ + bstack1111ll1_opy_) % bstack1l1ll1l_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack1ll1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack11ll11l_opy_ + bstack1111ll1_opy_) % bstack1l1ll1l_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack1ll1l11_opy_)
class bstack1l1ll1l1_opy_:
    def __init__(self, handler):
        self._11111llll1_opy_ = None
        self.handler = handler
        self._11111lll1l_opy_ = self.bstack11111lllll_opy_()
        self.patch()
    def patch(self):
        self._11111llll1_opy_ = self._11111lll1l_opy_.execute
        self._11111lll1l_opy_.execute = self.bstack11111lll11_opy_()
    def bstack11111lll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1lll11l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨᏧ"), driver_command)
            response = self._11111llll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1lll11l_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨᏨ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111lll1l_opy_.execute = self._11111llll1_opy_
    @staticmethod
    def bstack11111lllll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver