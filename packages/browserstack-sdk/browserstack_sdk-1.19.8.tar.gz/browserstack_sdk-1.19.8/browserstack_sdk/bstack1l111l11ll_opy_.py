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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11llll1lll_opy_, bstack11llllllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11llll1lll_opy_ = bstack11llll1lll_opy_
        self.bstack11llllllll_opy_ = bstack11llllllll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l1111ll11_opy_(bstack11llll1l11_opy_):
        bstack11llll1ll1_opy_ = []
        if bstack11llll1l11_opy_:
            tokens = str(os.path.basename(bstack11llll1l11_opy_)).split(bstack11lllll_opy_ (u"ࠣࡡࠥ෺"))
            camelcase_name = bstack11lllll_opy_ (u"ࠤࠣࠦ෻").join(t.title() for t in tokens)
            suite_name, bstack1l1l1lll1l_opy_ = os.path.splitext(camelcase_name)
            bstack11llll1ll1_opy_.append(suite_name)
        return bstack11llll1ll1_opy_
    @staticmethod
    def bstack11llll1l1l_opy_(typename):
        if bstack11lllll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ෼") in typename:
            return bstack11lllll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ෽")
        return bstack11lllll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ෾")