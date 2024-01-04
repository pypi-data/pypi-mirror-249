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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11lllll11l_opy_, bstack11llll1lll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lllll11l_opy_ = bstack11lllll11l_opy_
        self.bstack11llll1lll_opy_ = bstack11llll1lll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11l1l11l_opy_(bstack11llll1ll1_opy_):
        bstack11llll1l1l_opy_ = []
        if bstack11llll1ll1_opy_:
            tokens = str(os.path.basename(bstack11llll1ll1_opy_)).split(bstack1lll11l_opy_ (u"ࠢࡠࠤ෹"))
            camelcase_name = bstack1lll11l_opy_ (u"ࠣࠢࠥ෺").join(t.title() for t in tokens)
            suite_name, bstack1ll1llll1l_opy_ = os.path.splitext(camelcase_name)
            bstack11llll1l1l_opy_.append(suite_name)
        return bstack11llll1l1l_opy_
    @staticmethod
    def bstack11llll1l11_opy_(typename):
        if bstack1lll11l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ෻") in typename:
            return bstack1lll11l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ෼")
        return bstack1lll11l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ෽")