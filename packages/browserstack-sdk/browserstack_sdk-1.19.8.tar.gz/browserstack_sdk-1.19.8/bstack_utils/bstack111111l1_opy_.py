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
class bstack1l1ll1l11_opy_:
    def __init__(self, handler):
        self._11111ll1ll_opy_ = None
        self.handler = handler
        self._11111lll11_opy_ = self.bstack11111llll1_opy_()
        self.patch()
    def patch(self):
        self._11111ll1ll_opy_ = self._11111lll11_opy_.execute
        self._11111lll11_opy_.execute = self.bstack11111lll1l_opy_()
    def bstack11111lll1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11lllll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣᏩ"), driver_command)
            response = self._11111ll1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11lllll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣᏪ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111lll11_opy_.execute = self._11111ll1ll_opy_
    @staticmethod
    def bstack11111llll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver