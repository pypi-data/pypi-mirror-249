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
import sys
class bstack1l1l111l1l_opy_:
    def __init__(self, handler):
        self._11ll1ll11l_opy_ = sys.stdout.write
        self._11ll1ll111_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11ll1ll1l1_opy_
        sys.stdout.error = self.bstack11ll1l1lll_opy_
    def bstack11ll1ll1l1_opy_(self, _str):
        self._11ll1ll11l_opy_(_str)
        if self.handler:
            self.handler({bstack111ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨຕ"): bstack111ll11_opy_ (u"ࠪࡍࡓࡌࡏࠨຖ"), bstack111ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬທ"): _str})
    def bstack11ll1l1lll_opy_(self, _str):
        self._11ll1ll111_opy_(_str)
        if self.handler:
            self.handler({bstack111ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫຘ"): bstack111ll11_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬນ"), bstack111ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨບ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11ll1ll11l_opy_
        sys.stderr.write = self._11ll1ll111_opy_