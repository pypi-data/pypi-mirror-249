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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11lll11l1_opy_ = {}
        bstack1l1l111ll1_opy_ = os.environ.get(bstack11lllll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ೮"), bstack11lllll_opy_ (u"ࠧࠨ೯"))
        if not bstack1l1l111ll1_opy_:
            return bstack11lll11l1_opy_
        try:
            bstack1l1l111lll_opy_ = json.loads(bstack1l1l111ll1_opy_)
            if bstack11lllll_opy_ (u"ࠣࡱࡶࠦ೰") in bstack1l1l111lll_opy_:
                bstack11lll11l1_opy_[bstack11lllll_opy_ (u"ࠤࡲࡷࠧೱ")] = bstack1l1l111lll_opy_[bstack11lllll_opy_ (u"ࠥࡳࡸࠨೲ")]
            if bstack11lllll_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣೳ") in bstack1l1l111lll_opy_ or bstack11lllll_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೴") in bstack1l1l111lll_opy_:
                bstack11lll11l1_opy_[bstack11lllll_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤ೵")] = bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦ೶"), bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦ೷")))
            if bstack11lllll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ೸") in bstack1l1l111lll_opy_ or bstack11lllll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ೹") in bstack1l1l111lll_opy_:
                bstack11lll11l1_opy_[bstack11lllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ೺")] = bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨ೻"), bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ೼")))
            if bstack11lllll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ೽") in bstack1l1l111lll_opy_ or bstack11lllll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ೾") in bstack1l1l111lll_opy_:
                bstack11lll11l1_opy_[bstack11lllll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ೿")] = bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧഀ"), bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧഁ")))
            if bstack11lllll_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧം") in bstack1l1l111lll_opy_ or bstack11lllll_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥഃ") in bstack1l1l111lll_opy_:
                bstack11lll11l1_opy_[bstack11lllll_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦഄ")] = bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣഅ"), bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨആ")))
            if bstack11lllll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧഇ") in bstack1l1l111lll_opy_ or bstack11lllll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥഈ") in bstack1l1l111lll_opy_:
                bstack11lll11l1_opy_[bstack11lllll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦഉ")] = bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣഊ"), bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨഋ")))
            if bstack11lllll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦഌ") in bstack1l1l111lll_opy_ or bstack11lllll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ഍") in bstack1l1l111lll_opy_:
                bstack11lll11l1_opy_[bstack11lllll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧഎ")] = bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢഏ"), bstack1l1l111lll_opy_.get(bstack11lllll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢഐ")))
            if bstack11lllll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ഑") in bstack1l1l111lll_opy_:
                bstack11lll11l1_opy_[bstack11lllll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤഒ")] = bstack1l1l111lll_opy_[bstack11lllll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥഓ")]
        except Exception as error:
            logger.error(bstack11lllll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡤࡸࡦࡀࠠࠣഔ") +  str(error))
        return bstack11lll11l1_opy_