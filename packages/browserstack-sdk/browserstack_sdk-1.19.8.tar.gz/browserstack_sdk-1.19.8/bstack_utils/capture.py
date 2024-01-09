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
import sys
class bstack1l11lll1ll_opy_:
    def __init__(self, handler):
        self._11ll1ll1l1_opy_ = sys.stdout.write
        self._11ll1ll11l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11ll1l1lll_opy_
        sys.stdout.error = self.bstack11ll1ll111_opy_
    def bstack11ll1l1lll_opy_(self, _str):
        self._11ll1ll1l1_opy_(_str)
        if self.handler:
            self.handler({bstack11lllll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩຖ"): bstack11lllll_opy_ (u"ࠫࡎࡔࡆࡐࠩທ"), bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຘ"): _str})
    def bstack11ll1ll111_opy_(self, _str):
        self._11ll1ll11l_opy_(_str)
        if self.handler:
            self.handler({bstack11lllll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬນ"): bstack11lllll_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭ບ"), bstack11lllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩປ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11ll1ll1l1_opy_
        sys.stderr.write = self._11ll1ll11l_opy_