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
from collections import deque
from bstack_utils.constants import *
class bstack1lllllll11_opy_:
    def __init__(self):
        self._111l111111_opy_ = deque()
        self._111l111lll_opy_ = {}
        self._111l11ll1l_opy_ = False
    def bstack111l111l1l_opy_(self, test_name, bstack111l11l111_opy_):
        bstack111l111l11_opy_ = self._111l111lll_opy_.get(test_name, {})
        return bstack111l111l11_opy_.get(bstack111l11l111_opy_, 0)
    def bstack111l1111l1_opy_(self, test_name, bstack111l11l111_opy_):
        bstack111l11lll1_opy_ = self.bstack111l111l1l_opy_(test_name, bstack111l11l111_opy_)
        self.bstack111l11111l_opy_(test_name, bstack111l11l111_opy_)
        return bstack111l11lll1_opy_
    def bstack111l11111l_opy_(self, test_name, bstack111l11l111_opy_):
        if test_name not in self._111l111lll_opy_:
            self._111l111lll_opy_[test_name] = {}
        bstack111l111l11_opy_ = self._111l111lll_opy_[test_name]
        bstack111l11lll1_opy_ = bstack111l111l11_opy_.get(bstack111l11l111_opy_, 0)
        bstack111l111l11_opy_[bstack111l11l111_opy_] = bstack111l11lll1_opy_ + 1
    def bstack1l111l1l_opy_(self, bstack111l11l11l_opy_, bstack111l11ll11_opy_):
        bstack111l11l1l1_opy_ = self.bstack111l1111l1_opy_(bstack111l11l11l_opy_, bstack111l11ll11_opy_)
        bstack111l1111ll_opy_ = bstack11ll1l111l_opy_[bstack111l11ll11_opy_]
        bstack111l111ll1_opy_ = bstack11lllll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾ࠯ࡾࢁࠧ᎐").format(bstack111l11l11l_opy_, bstack111l1111ll_opy_, bstack111l11l1l1_opy_)
        self._111l111111_opy_.append(bstack111l111ll1_opy_)
    def bstack1ll1l1l1l1_opy_(self):
        return len(self._111l111111_opy_) == 0
    def bstack111l111l_opy_(self):
        bstack111l11l1ll_opy_ = self._111l111111_opy_.popleft()
        return bstack111l11l1ll_opy_
    def capturing(self):
        return self._111l11ll1l_opy_
    def bstack1l111111l_opy_(self):
        self._111l11ll1l_opy_ = True
    def bstack1l1l1lll1_opy_(self):
        self._111l11ll1l_opy_ = False