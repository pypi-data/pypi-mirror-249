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
class bstack1ll1lll111_opy_:
    def __init__(self, handler):
        self._11111lll11_opy_ = None
        self.handler = handler
        self._11111lll1l_opy_ = self.bstack11111ll1ll_opy_()
        self.patch()
    def patch(self):
        self._11111lll11_opy_ = self._11111lll1l_opy_.execute
        self._11111lll1l_opy_.execute = self.bstack11111llll1_opy_()
    def bstack11111llll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᏨ"), driver_command)
            response = self._11111lll11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111ll11_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᏩ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111lll1l_opy_.execute = self._11111lll11_opy_
    @staticmethod
    def bstack11111ll1ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver