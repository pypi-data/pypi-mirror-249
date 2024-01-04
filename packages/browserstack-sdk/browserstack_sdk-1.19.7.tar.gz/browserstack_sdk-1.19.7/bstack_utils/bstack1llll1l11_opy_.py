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
from collections import deque
from bstack_utils.constants import *
class bstack1llll11lll_opy_:
    def __init__(self):
        self._111l11lll1_opy_ = deque()
        self._111l1111ll_opy_ = {}
        self._111l111111_opy_ = False
    def bstack111l11l111_opy_(self, test_name, bstack111l11ll1l_opy_):
        bstack111l11l1ll_opy_ = self._111l1111ll_opy_.get(test_name, {})
        return bstack111l11l1ll_opy_.get(bstack111l11ll1l_opy_, 0)
    def bstack111l111lll_opy_(self, test_name, bstack111l11ll1l_opy_):
        bstack111l1111l1_opy_ = self.bstack111l11l111_opy_(test_name, bstack111l11ll1l_opy_)
        self.bstack111l11l1l1_opy_(test_name, bstack111l11ll1l_opy_)
        return bstack111l1111l1_opy_
    def bstack111l11l1l1_opy_(self, test_name, bstack111l11ll1l_opy_):
        if test_name not in self._111l1111ll_opy_:
            self._111l1111ll_opy_[test_name] = {}
        bstack111l11l1ll_opy_ = self._111l1111ll_opy_[test_name]
        bstack111l1111l1_opy_ = bstack111l11l1ll_opy_.get(bstack111l11ll1l_opy_, 0)
        bstack111l11l1ll_opy_[bstack111l11ll1l_opy_] = bstack111l1111l1_opy_ + 1
    def bstack111111ll_opy_(self, bstack111l111l1l_opy_, bstack111l111ll1_opy_):
        bstack111l11111l_opy_ = self.bstack111l111lll_opy_(bstack111l111l1l_opy_, bstack111l111ll1_opy_)
        bstack111l111l11_opy_ = bstack11ll1l11l1_opy_[bstack111l111ll1_opy_]
        bstack111l11ll11_opy_ = bstack111ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᎏ").format(bstack111l111l1l_opy_, bstack111l111l11_opy_, bstack111l11111l_opy_)
        self._111l11lll1_opy_.append(bstack111l11ll11_opy_)
    def bstack1ll11ll1l_opy_(self):
        return len(self._111l11lll1_opy_) == 0
    def bstack111ll1l1_opy_(self):
        bstack111l11l11l_opy_ = self._111l11lll1_opy_.popleft()
        return bstack111l11l11l_opy_
    def capturing(self):
        return self._111l111111_opy_
    def bstack11l11l1ll_opy_(self):
        self._111l111111_opy_ = True
    def bstack11l11l11_opy_(self):
        self._111l111111_opy_ = False