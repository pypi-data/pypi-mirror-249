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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1l111111ll_opy_, bstack1l1111111l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l111111ll_opy_ = bstack1l111111ll_opy_
        self.bstack1l1111111l_opy_ = bstack1l1111111l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11111lll_opy_(bstack11llll1ll1_opy_):
        bstack11llll1l11_opy_ = []
        if bstack11llll1ll1_opy_:
            tokens = str(os.path.basename(bstack11llll1ll1_opy_)).split(bstack111ll11_opy_ (u"ࠢࡠࠤ෹"))
            camelcase_name = bstack111ll11_opy_ (u"ࠣࠢࠥ෺").join(t.title() for t in tokens)
            suite_name, bstack1lll1ll111_opy_ = os.path.splitext(camelcase_name)
            bstack11llll1l11_opy_.append(suite_name)
        return bstack11llll1l11_opy_
    @staticmethod
    def bstack11llll1l1l_opy_(typename):
        if bstack111ll11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ෻") in typename:
            return bstack111ll11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ෼")
        return bstack111ll11_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ෽")