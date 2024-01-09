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
import multiprocessing
import os
import json
from browserstack_sdk.bstack111l11ll1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l11lll_opy_
class bstack11l111111_opy_:
    def __init__(self, args, logger, bstack11llll1lll_opy_, bstack11llllllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11llll1lll_opy_ = bstack11llll1lll_opy_
        self.bstack11llllllll_opy_ = bstack11llllllll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lll11l11l_opy_ = []
        self.bstack11lllll11l_opy_ = None
        self.bstack11l11l111_opy_ = []
        self.bstack11lllll111_opy_ = self.bstack11l11ll1l_opy_()
        self.bstack11ll1ll1_opy_ = -1
    def bstack1lll11l11_opy_(self, bstack1l11111111_opy_):
        self.parse_args()
        self.bstack1l11111l11_opy_()
        self.bstack11lllllll1_opy_(bstack1l11111111_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1l111111l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11ll1ll1_opy_ = -1
        if bstack11lllll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෡") in self.bstack11llll1lll_opy_:
            self.bstack11ll1ll1_opy_ = int(self.bstack11llll1lll_opy_[bstack11lllll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ෢")])
        try:
            bstack11lllll1ll_opy_ = [bstack11lllll_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ෣"), bstack11lllll_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ෤"), bstack11lllll_opy_ (u"ࠨ࠯ࡳࠫ෥")]
            if self.bstack11ll1ll1_opy_ >= 0:
                bstack11lllll1ll_opy_.extend([bstack11lllll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ෦"), bstack11lllll_opy_ (u"ࠪ࠱ࡳ࠭෧")])
            for arg in bstack11lllll1ll_opy_:
                self.bstack1l111111l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1l11111l11_opy_(self):
        bstack11lllll11l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11lllll11l_opy_ = bstack11lllll11l_opy_
        return bstack11lllll11l_opy_
    def bstack1ll1l11l11_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack11lllll1l1_opy_ = importlib.find_loader(bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭෨"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11l11lll_opy_)
    def bstack11lllllll1_opy_(self, bstack1l11111111_opy_):
        bstack1lll11111_opy_ = Config.get_instance()
        if bstack1l11111111_opy_:
            self.bstack11lllll11l_opy_.append(bstack11lllll_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ෩"))
            self.bstack11lllll11l_opy_.append(bstack11lllll_opy_ (u"࠭ࡔࡳࡷࡨࠫ෪"))
        if bstack1lll11111_opy_.bstack11llllll1l_opy_():
            self.bstack11lllll11l_opy_.append(bstack11lllll_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭෫"))
            self.bstack11lllll11l_opy_.append(bstack11lllll_opy_ (u"ࠨࡖࡵࡹࡪ࠭෬"))
        self.bstack11lllll11l_opy_.append(bstack11lllll_opy_ (u"ࠩ࠰ࡴࠬ෭"))
        self.bstack11lllll11l_opy_.append(bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨ෮"))
        self.bstack11lllll11l_opy_.append(bstack11lllll_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭෯"))
        self.bstack11lllll11l_opy_.append(bstack11lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ෰"))
        if self.bstack11ll1ll1_opy_ > 1:
            self.bstack11lllll11l_opy_.append(bstack11lllll_opy_ (u"࠭࠭࡯ࠩ෱"))
            self.bstack11lllll11l_opy_.append(str(self.bstack11ll1ll1_opy_))
    def bstack1l111111ll_opy_(self):
        bstack11l11l111_opy_ = []
        for spec in self.bstack1lll11l11l_opy_:
            bstack1l1l11l1_opy_ = [spec]
            bstack1l1l11l1_opy_ += self.bstack11lllll11l_opy_
            bstack11l11l111_opy_.append(bstack1l1l11l1_opy_)
        self.bstack11l11l111_opy_ = bstack11l11l111_opy_
        return bstack11l11l111_opy_
    def bstack11l11ll1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11lllll111_opy_ = True
            return True
        except Exception as e:
            self.bstack11lllll111_opy_ = False
        return self.bstack11lllll111_opy_
    def bstack111llll1l_opy_(self, bstack11llllll11_opy_, bstack1lll11l11_opy_):
        bstack1lll11l11_opy_[bstack11lllll_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧෲ")] = self.bstack11llll1lll_opy_
        multiprocessing.set_start_method(bstack11lllll_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧෳ"))
        if bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ෴") in self.bstack11llll1lll_opy_:
            bstack1lllll1ll1_opy_ = []
            manager = multiprocessing.Manager()
            bstack1lll1llll_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11llll1lll_opy_[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෵")]):
                bstack1lllll1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11llllll11_opy_,
                                                           args=(self.bstack11lllll11l_opy_, bstack1lll11l11_opy_, bstack1lll1llll_opy_)))
            i = 0
            bstack1l1111111l_opy_ = len(self.bstack11llll1lll_opy_[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෶")])
            for t in bstack1lllll1ll1_opy_:
                os.environ[bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ෷")] = str(i)
                os.environ[bstack11lllll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ෸")] = json.dumps(self.bstack11llll1lll_opy_[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ෹")][i % bstack1l1111111l_opy_])
                i += 1
                t.start()
            for t in bstack1lllll1ll1_opy_:
                t.join()
            return list(bstack1lll1llll_opy_)