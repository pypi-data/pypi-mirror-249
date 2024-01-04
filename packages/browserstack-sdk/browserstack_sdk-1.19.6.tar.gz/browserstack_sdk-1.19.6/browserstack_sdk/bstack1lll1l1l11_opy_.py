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
import multiprocessing
import os
import json
from browserstack_sdk.bstack111lllll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11111l1l1_opy_
class bstack1ll111111_opy_:
    def __init__(self, args, logger, bstack11lllll11l_opy_, bstack11llll1lll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lllll11l_opy_ = bstack11lllll11l_opy_
        self.bstack11llll1lll_opy_ = bstack11llll1lll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111l1l111_opy_ = []
        self.bstack11lllll1ll_opy_ = None
        self.bstack1ll1l1l11_opy_ = []
        self.bstack11lllll111_opy_ = self.bstack1ll1lll1l1_opy_()
        self.bstack1l11ll1l1_opy_ = -1
    def bstack1ll11111l_opy_(self, bstack11llllll11_opy_):
        self.parse_args()
        self.bstack1l11111l11_opy_()
        self.bstack1l111111ll_opy_(bstack11llllll11_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack11lllllll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l11ll1l1_opy_ = -1
        if bstack1lll11l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ෠") in self.bstack11lllll11l_opy_:
            self.bstack1l11ll1l1_opy_ = int(self.bstack11lllll11l_opy_[bstack1lll11l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෡")])
        try:
            bstack1l1111111l_opy_ = [bstack1lll11l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧ෢"), bstack1lll11l_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩ෣"), bstack1lll11l_opy_ (u"ࠧ࠮ࡲࠪ෤")]
            if self.bstack1l11ll1l1_opy_ >= 0:
                bstack1l1111111l_opy_.extend([bstack1lll11l_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ෥"), bstack1lll11l_opy_ (u"ࠩ࠰ࡲࠬ෦")])
            for arg in bstack1l1111111l_opy_:
                self.bstack11lllllll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1l11111l11_opy_(self):
        bstack11lllll1ll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11lllll1ll_opy_ = bstack11lllll1ll_opy_
        return bstack11lllll1ll_opy_
    def bstack11l1lll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack11llllll1l_opy_ = importlib.find_loader(bstack1lll11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ෧"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11111l1l1_opy_)
    def bstack1l111111ll_opy_(self, bstack11llllll11_opy_):
        bstack1l1l1ll1ll_opy_ = Config.get_instance()
        if bstack11llllll11_opy_:
            self.bstack11lllll1ll_opy_.append(bstack1lll11l_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ෨"))
            self.bstack11lllll1ll_opy_.append(bstack1lll11l_opy_ (u"࡚ࠬࡲࡶࡧࠪ෩"))
        if bstack1l1l1ll1ll_opy_.bstack1l11111111_opy_():
            self.bstack11lllll1ll_opy_.append(bstack1lll11l_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ෪"))
            self.bstack11lllll1ll_opy_.append(bstack1lll11l_opy_ (u"ࠧࡕࡴࡸࡩࠬ෫"))
        self.bstack11lllll1ll_opy_.append(bstack1lll11l_opy_ (u"ࠨ࠯ࡳࠫ෬"))
        self.bstack11lllll1ll_opy_.append(bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧ෭"))
        self.bstack11lllll1ll_opy_.append(bstack1lll11l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ෮"))
        self.bstack11lllll1ll_opy_.append(bstack1lll11l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ෯"))
        if self.bstack1l11ll1l1_opy_ > 1:
            self.bstack11lllll1ll_opy_.append(bstack1lll11l_opy_ (u"ࠬ࠳࡮ࠨ෰"))
            self.bstack11lllll1ll_opy_.append(str(self.bstack1l11ll1l1_opy_))
    def bstack1l111111l1_opy_(self):
        bstack1ll1l1l11_opy_ = []
        for spec in self.bstack111l1l111_opy_:
            bstack11111ll1_opy_ = [spec]
            bstack11111ll1_opy_ += self.bstack11lllll1ll_opy_
            bstack1ll1l1l11_opy_.append(bstack11111ll1_opy_)
        self.bstack1ll1l1l11_opy_ = bstack1ll1l1l11_opy_
        return bstack1ll1l1l11_opy_
    def bstack1ll1lll1l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11lllll111_opy_ = True
            return True
        except Exception as e:
            self.bstack11lllll111_opy_ = False
        return self.bstack11lllll111_opy_
    def bstack1l1l11l111_opy_(self, bstack11lllll1l1_opy_, bstack1ll11111l_opy_):
        bstack1ll11111l_opy_[bstack1lll11l_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭෱")] = self.bstack11lllll11l_opy_
        multiprocessing.set_start_method(bstack1lll11l_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭ෲ"))
        if bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫෳ") in self.bstack11lllll11l_opy_:
            bstack1l1l111l_opy_ = []
            manager = multiprocessing.Manager()
            bstack1l1lll1111_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11lllll11l_opy_[bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ෴")]):
                bstack1l1l111l_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11lllll1l1_opy_,
                                                           args=(self.bstack11lllll1ll_opy_, bstack1ll11111l_opy_, bstack1l1lll1111_opy_)))
            i = 0
            bstack11llllllll_opy_ = len(self.bstack11lllll11l_opy_[bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෵")])
            for t in bstack1l1l111l_opy_:
                os.environ[bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ෶")] = str(i)
                os.environ[bstack1lll11l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭෷")] = json.dumps(self.bstack11lllll11l_opy_[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෸")][i % bstack11llllllll_opy_])
                i += 1
                t.start()
            for t in bstack1l1l111l_opy_:
                t.join()
            return list(bstack1l1lll1111_opy_)