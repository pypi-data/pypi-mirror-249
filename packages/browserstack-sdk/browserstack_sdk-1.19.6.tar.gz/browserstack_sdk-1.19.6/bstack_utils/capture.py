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
import sys
class bstack1l11lll1ll_opy_:
    def __init__(self, handler):
        self._11ll1ll111_opy_ = sys.stdout.write
        self._11ll1ll11l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11ll1l1lll_opy_
        sys.stdout.error = self.bstack11ll1ll1l1_opy_
    def bstack11ll1l1lll_opy_(self, _str):
        self._11ll1ll111_opy_(_str)
        if self.handler:
            self.handler({bstack1lll11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨຕ"): bstack1lll11l_opy_ (u"ࠪࡍࡓࡌࡏࠨຖ"), bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬທ"): _str})
    def bstack11ll1ll1l1_opy_(self, _str):
        self._11ll1ll11l_opy_(_str)
        if self.handler:
            self.handler({bstack1lll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫຘ"): bstack1lll11l_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬນ"), bstack1lll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨບ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11ll1ll111_opy_
        sys.stderr.write = self._11ll1ll11l_opy_