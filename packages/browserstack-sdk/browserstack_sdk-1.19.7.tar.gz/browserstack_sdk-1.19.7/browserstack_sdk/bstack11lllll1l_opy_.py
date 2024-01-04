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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack111l11lll_opy_ = {}
        bstack1l1l111lll_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭೭"), bstack111ll11_opy_ (u"࠭ࠧ೮"))
        if not bstack1l1l111lll_opy_:
            return bstack111l11lll_opy_
        try:
            bstack1l1l111ll1_opy_ = json.loads(bstack1l1l111lll_opy_)
            if bstack111ll11_opy_ (u"ࠢࡰࡵࠥ೯") in bstack1l1l111ll1_opy_:
                bstack111l11lll_opy_[bstack111ll11_opy_ (u"ࠣࡱࡶࠦ೰")] = bstack1l1l111ll1_opy_[bstack111ll11_opy_ (u"ࠤࡲࡷࠧೱ")]
            if bstack111ll11_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢೲ") in bstack1l1l111ll1_opy_ or bstack111ll11_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢೳ") in bstack1l1l111ll1_opy_:
                bstack111l11lll_opy_[bstack111ll11_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೴")] = bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ೵"), bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥ೶")))
            if bstack111ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤ೷") in bstack1l1l111ll1_opy_ or bstack111ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ೸") in bstack1l1l111ll1_opy_:
                bstack111l11lll_opy_[bstack111ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ೹")] = bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧ೺"), bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ೻")))
            if bstack111ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ೼") in bstack1l1l111ll1_opy_ or bstack111ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೽") in bstack1l1l111ll1_opy_:
                bstack111l11lll_opy_[bstack111ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ೾")] = bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦ೿"), bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦഀ")))
            if bstack111ll11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦഁ") in bstack1l1l111ll1_opy_ or bstack111ll11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤം") in bstack1l1l111ll1_opy_:
                bstack111l11lll_opy_[bstack111ll11_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥഃ")] = bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢഄ"), bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧഅ")))
            if bstack111ll11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦആ") in bstack1l1l111ll1_opy_ or bstack111ll11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤഇ") in bstack1l1l111ll1_opy_:
                bstack111l11lll_opy_[bstack111ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥഈ")] = bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢഉ"), bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧഊ")))
            if bstack111ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥഋ") in bstack1l1l111ll1_opy_ or bstack111ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥഌ") in bstack1l1l111ll1_opy_:
                bstack111l11lll_opy_[bstack111ll11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ഍")] = bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨഎ"), bstack1l1l111ll1_opy_.get(bstack111ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨഏ")))
            if bstack111ll11_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢഐ") in bstack1l1l111ll1_opy_:
                bstack111l11lll_opy_[bstack111ll11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ഑")] = bstack1l1l111ll1_opy_[bstack111ll11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤഒ")]
        except Exception as error:
            logger.error(bstack111ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡣࡷࡥ࠿ࠦࠢഓ") +  str(error))
        return bstack111l11lll_opy_