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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll1ll1ll_opy_, bstack1l1lll1111_opy_, get_host_info, bstack11lll1l1ll_opy_, bstack11lll11ll1_opy_, bstack11l1ll1ll1_opy_, \
    bstack11l1lll1ll_opy_, bstack11ll1111l1_opy_, bstack1ll111lll1_opy_, bstack11l1l1111l_opy_, bstack1llll11l1_opy_, bstack1l11lll1ll_opy_
from bstack_utils.bstack1111l11l11_opy_ import bstack1111l1111l_opy_
from bstack_utils.bstack1l11l111ll_opy_ import bstack1l11l1ll11_opy_
bstack1111111111_opy_ = [
    bstack111ll11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᑜ"), bstack111ll11_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᑝ"), bstack111ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᑞ"), bstack111ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᑟ"),
    bstack111ll11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᑠ"), bstack111ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᑡ"), bstack111ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᑢ")
]
bstack11111111ll_opy_ = bstack111ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᑣ")
logger = logging.getLogger(__name__)
class bstack1ll1l1llll_opy_:
    bstack1111l11l11_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l11lll1ll_opy_(class_method=True)
    def launch(cls, bs_config, bstack1llllllllll_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1lllllllll1_opy_():
            return
        cls.bstack1llllll1l11_opy_()
        bstack11ll1lll11_opy_ = bstack11lll1l1ll_opy_(bs_config)
        bstack11lll1ll1l_opy_ = bstack11lll11ll1_opy_(bs_config)
        data = {
            bstack111ll11_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬᑤ"): bstack111ll11_opy_ (u"࠭ࡪࡴࡱࡱࠫᑥ"),
            bstack111ll11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ᑦ"): bs_config.get(bstack111ll11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᑧ"), bstack111ll11_opy_ (u"ࠩࠪᑨ")),
            bstack111ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨᑩ"): bs_config.get(bstack111ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᑪ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack111ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᑫ"): bs_config.get(bstack111ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᑬ")),
            bstack111ll11_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᑭ"): bs_config.get(bstack111ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᑮ"), bstack111ll11_opy_ (u"ࠩࠪᑯ")),
            bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧᑰ"): datetime.datetime.now().isoformat(),
            bstack111ll11_opy_ (u"ࠫࡹࡧࡧࡴࠩᑱ"): bstack11l1ll1ll1_opy_(bs_config),
            bstack111ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨᑲ"): get_host_info(),
            bstack111ll11_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧᑳ"): bstack1l1lll1111_opy_(),
            bstack111ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᑴ"): os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᑵ")),
            bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧᑶ"): os.environ.get(bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨᑷ"), False),
            bstack111ll11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ᑸ"): bstack11ll1ll1ll_opy_(),
            bstack111ll11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᑹ"): {
                bstack111ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᑺ"): bstack1llllllllll_opy_.get(bstack111ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨᑻ"), bstack111ll11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᑼ")),
                bstack111ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᑽ"): bstack1llllllllll_opy_.get(bstack111ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᑾ")),
                bstack111ll11_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᑿ"): bstack1llllllllll_opy_.get(bstack111ll11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᒀ"))
            }
        }
        config = {
            bstack111ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᒁ"): (bstack11ll1lll11_opy_, bstack11lll1ll1l_opy_),
            bstack111ll11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᒂ"): cls.default_headers()
        }
        response = bstack1ll111lll1_opy_(bstack111ll11_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᒃ"), cls.request_url(bstack111ll11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴࠩᒄ")), data, config)
        if response.status_code != 200:
            os.environ[bstack111ll11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᒅ")] = bstack111ll11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᒆ")
            os.environ[bstack111ll11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᒇ")] = bstack111ll11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᒈ")
            os.environ[bstack111ll11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᒉ")] = bstack111ll11_opy_ (u"ࠣࡰࡸࡰࡱࠨᒊ")
            os.environ[bstack111ll11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᒋ")] = bstack111ll11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᒌ")
            bstack1llllll11l1_opy_ = response.json()
            if bstack1llllll11l1_opy_ and bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᒍ")]:
                error_message = bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᒎ")]
                if bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᒏ")] == bstack111ll11_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬᒐ"):
                    logger.error(error_message)
                elif bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᒑ")] == bstack111ll11_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨᒒ"):
                    logger.info(error_message)
                elif bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ᒓ")] == bstack111ll11_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫᒔ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111ll11_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᒕ"))
            return [None, None, None]
        logger.debug(bstack111ll11_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᒖ"))
        os.environ[bstack111ll11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᒗ")] = bstack111ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᒘ")
        bstack1llllll11l1_opy_ = response.json()
        if bstack1llllll11l1_opy_.get(bstack111ll11_opy_ (u"ࠩ࡭ࡻࡹ࠭ᒙ")):
            os.environ[bstack111ll11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᒚ")] = bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"ࠫ࡯ࡽࡴࠨᒛ")]
            os.environ[bstack111ll11_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩᒜ")] = json.dumps({
                bstack111ll11_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨᒝ"): bstack11ll1lll11_opy_,
                bstack111ll11_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩᒞ"): bstack11lll1ll1l_opy_
            })
        if bstack1llllll11l1_opy_.get(bstack111ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᒟ")):
            os.environ[bstack111ll11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᒠ")] = bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᒡ")]
        if bstack1llllll11l1_opy_.get(bstack111ll11_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᒢ")):
            os.environ[bstack111ll11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᒣ")] = str(bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᒤ")])
        return [bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"ࠧ࡫ࡹࡷࠫᒥ")], bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᒦ")], bstack1llllll11l1_opy_[bstack111ll11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᒧ")]]
    @classmethod
    @bstack1l11lll1ll_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack111ll11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᒨ")] == bstack111ll11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᒩ") or os.environ[bstack111ll11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᒪ")] == bstack111ll11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᒫ"):
            print(bstack111ll11_opy_ (u"ࠧࡆ࡚ࡆࡉࡕ࡚ࡉࡐࡐࠣࡍࡓࠦࡳࡵࡱࡳࡆࡺ࡯࡬ࡥࡗࡳࡷࡹࡸࡥࡢ࡯ࠣࡖࡊࡗࡕࡆࡕࡗࠤ࡙ࡕࠠࡕࡇࡖࡘࠥࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠥࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᒬ"))
            return {
                bstack111ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᒭ"): bstack111ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᒮ"),
                bstack111ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᒯ"): bstack111ll11_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᒰ")
            }
        else:
            cls.bstack1111l11l11_opy_.shutdown()
            data = {
                bstack111ll11_opy_ (u"ࠬࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࠨᒱ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack111ll11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᒲ"): cls.default_headers()
            }
            bstack11ll11l1ll_opy_ = bstack111ll11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨᒳ").format(os.environ[bstack111ll11_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᒴ")])
            bstack1llllll1111_opy_ = cls.request_url(bstack11ll11l1ll_opy_)
            response = bstack1ll111lll1_opy_(bstack111ll11_opy_ (u"ࠩࡓ࡙࡙࠭ᒵ"), bstack1llllll1111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111ll11_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤᒶ"))
    @classmethod
    def bstack1l11111l1l_opy_(cls):
        if cls.bstack1111l11l11_opy_ is None:
            return
        cls.bstack1111l11l11_opy_.shutdown()
    @classmethod
    def bstack1llll111_opy_(cls):
        if cls.on():
            print(
                bstack111ll11_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧᒷ").format(os.environ[bstack111ll11_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦᒸ")]))
    @classmethod
    def bstack1llllll1l11_opy_(cls):
        if cls.bstack1111l11l11_opy_ is not None:
            return
        cls.bstack1111l11l11_opy_ = bstack1111l1111l_opy_(cls.bstack1lllllll1ll_opy_)
        cls.bstack1111l11l11_opy_.start()
    @classmethod
    def bstack1l11ll11l1_opy_(cls, bstack1l111l11l1_opy_, bstack1lllllll1l1_opy_=bstack111ll11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᒹ")):
        if not cls.on():
            return
        bstack1lll1l111_opy_ = bstack1l111l11l1_opy_[bstack111ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᒺ")]
        bstack111111111l_opy_ = {
            bstack111ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᒻ"): bstack111ll11_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᒼ"),
            bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᒽ"): bstack111ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᒾ"),
            bstack111ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᒿ"): bstack111ll11_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡱࡩࡱࡲࡨࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᓀ"),
            bstack111ll11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᓁ"): bstack111ll11_opy_ (u"ࠨࡎࡲ࡫ࡤ࡛ࡰ࡭ࡱࡤࡨࠬᓂ"),
            bstack111ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᓃ"): bstack111ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᓄ"),
            bstack111ll11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᓅ"): bstack111ll11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᓆ"),
            bstack111ll11_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᓇ"): bstack111ll11_opy_ (u"ࠧࡄࡄࡗࡣ࡚ࡶ࡬ࡰࡣࡧࠫᓈ")
        }.get(bstack1lll1l111_opy_)
        if bstack1lllllll1l1_opy_ == bstack111ll11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᓉ"):
            cls.bstack1llllll1l11_opy_()
            cls.bstack1111l11l11_opy_.add(bstack1l111l11l1_opy_)
        elif bstack1lllllll1l1_opy_ == bstack111ll11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᓊ"):
            cls.bstack1lllllll1ll_opy_([bstack1l111l11l1_opy_], bstack1lllllll1l1_opy_)
    @classmethod
    @bstack1l11lll1ll_opy_(class_method=True)
    def bstack1lllllll1ll_opy_(cls, bstack1l111l11l1_opy_, bstack1lllllll1l1_opy_=bstack111ll11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᓋ")):
        config = {
            bstack111ll11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᓌ"): cls.default_headers()
        }
        response = bstack1ll111lll1_opy_(bstack111ll11_opy_ (u"ࠬࡖࡏࡔࡖࠪᓍ"), cls.request_url(bstack1lllllll1l1_opy_), bstack1l111l11l1_opy_, config)
        bstack11lll1llll_opy_ = response.json()
    @classmethod
    @bstack1l11lll1ll_opy_(class_method=True)
    def bstack1l111lllll_opy_(cls, bstack1l11ll1111_opy_):
        bstack1llllllll11_opy_ = []
        for log in bstack1l11ll1111_opy_:
            bstack1llllll1l1l_opy_ = {
                bstack111ll11_opy_ (u"࠭࡫ࡪࡰࡧࠫᓎ"): bstack111ll11_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩᓏ"),
                bstack111ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᓐ"): log[bstack111ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᓑ")],
                bstack111ll11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᓒ"): log[bstack111ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᓓ")],
                bstack111ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬᓔ"): {},
                bstack111ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᓕ"): log[bstack111ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᓖ")],
            }
            if bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓗ") in log:
                bstack1llllll1l1l_opy_[bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓘ")] = log[bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓙ")]
            elif bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓚ") in log:
                bstack1llllll1l1l_opy_[bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᓛ")] = log[bstack111ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓜ")]
            bstack1llllllll11_opy_.append(bstack1llllll1l1l_opy_)
        cls.bstack1l11ll11l1_opy_({
            bstack111ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᓝ"): bstack111ll11_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᓞ"),
            bstack111ll11_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᓟ"): bstack1llllllll11_opy_
        })
    @classmethod
    @bstack1l11lll1ll_opy_(class_method=True)
    def bstack1llllll1ll1_opy_(cls, steps):
        bstack1llllll111l_opy_ = []
        for step in steps:
            bstack11111111l1_opy_ = {
                bstack111ll11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᓠ"): bstack111ll11_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧᓡ"),
                bstack111ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᓢ"): step[bstack111ll11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᓣ")],
                bstack111ll11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᓤ"): step[bstack111ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᓥ")],
                bstack111ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓦ"): step[bstack111ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᓧ")],
                bstack111ll11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᓨ"): step[bstack111ll11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᓩ")]
            }
            if bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓪ") in step:
                bstack11111111l1_opy_[bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᓫ")] = step[bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓬ")]
            elif bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓭ") in step:
                bstack11111111l1_opy_[bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓮ")] = step[bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓯ")]
            bstack1llllll111l_opy_.append(bstack11111111l1_opy_)
        cls.bstack1l11ll11l1_opy_({
            bstack111ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᓰ"): bstack111ll11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᓱ"),
            bstack111ll11_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᓲ"): bstack1llllll111l_opy_
        })
    @classmethod
    @bstack1l11lll1ll_opy_(class_method=True)
    def bstack11lll111_opy_(cls, screenshot):
        cls.bstack1l11ll11l1_opy_({
            bstack111ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᓳ"): bstack111ll11_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᓴ"),
            bstack111ll11_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᓵ"): [{
                bstack111ll11_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᓶ"): bstack111ll11_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᓷ"),
                bstack111ll11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᓸ"): datetime.datetime.utcnow().isoformat() + bstack111ll11_opy_ (u"࡛ࠧࠩᓹ"),
                bstack111ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᓺ"): screenshot[bstack111ll11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᓻ")],
                bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓼ"): screenshot[bstack111ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓽ")]
            }]
        }, bstack1lllllll1l1_opy_=bstack111ll11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᓾ"))
    @classmethod
    @bstack1l11lll1ll_opy_(class_method=True)
    def bstack1l1ll1l11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l11ll11l1_opy_({
            bstack111ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᓿ"): bstack111ll11_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᔀ"),
            bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᔁ"): {
                bstack111ll11_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᔂ"): cls.current_test_uuid(),
                bstack111ll11_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤᔃ"): cls.bstack1l111l11ll_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack111ll11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᔄ"), None) is None or os.environ[bstack111ll11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᔅ")] == bstack111ll11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᔆ"):
            return False
        return True
    @classmethod
    def bstack1lllllllll1_opy_(cls):
        return bstack1llll11l1_opy_(cls.bs_config.get(bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᔇ"), False))
    @staticmethod
    def request_url(url):
        return bstack111ll11_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᔈ").format(bstack11111111ll_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack111ll11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᔉ"): bstack111ll11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᔊ"),
            bstack111ll11_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧᔋ"): bstack111ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪᔌ")
        }
        if os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᔍ"), None):
            headers[bstack111ll11_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᔎ")] = bstack111ll11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᔏ").format(os.environ[bstack111ll11_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠥᔐ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᔑ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᔒ"), None)
    @staticmethod
    def bstack1l11111ll1_opy_():
        if getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᔓ"), None):
            return {
                bstack111ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫᔔ"): bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࠬᔕ"),
                bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᔖ"): getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᔗ"), None)
            }
        if getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᔘ"), None):
            return {
                bstack111ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩᔙ"): bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᔚ"),
                bstack111ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔛ"): getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᔜ"), None)
            }
        return None
    @staticmethod
    def bstack1l111l11ll_opy_(driver):
        return {
            bstack11ll1111l1_opy_(): bstack11l1lll1ll_opy_(driver)
        }
    @staticmethod
    def bstack1lllllll111_opy_(exception_info, report):
        return [{bstack111ll11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᔝ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11llll1l1l_opy_(typename):
        if bstack111ll11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᔞ") in typename:
            return bstack111ll11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᔟ")
        return bstack111ll11_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᔠ")
    @staticmethod
    def bstack1llllll1lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1l1llll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11111lll_opy_(test, hook_name=None):
        bstack1llllllll1l_opy_ = test.parent
        if hook_name in [bstack111ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᔡ"), bstack111ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᔢ"), bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᔣ"), bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᔤ")]:
            bstack1llllllll1l_opy_ = test
        scope = []
        while bstack1llllllll1l_opy_ is not None:
            scope.append(bstack1llllllll1l_opy_.name)
            bstack1llllllll1l_opy_ = bstack1llllllll1l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llllll11ll_opy_(hook_type):
        if hook_type == bstack111ll11_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢᔥ"):
            return bstack111ll11_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢᔦ")
        elif hook_type == bstack111ll11_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣᔧ"):
            return bstack111ll11_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧᔨ")
    @staticmethod
    def bstack1lllllll11l_opy_(bstack1ll1l1ll1l_opy_):
        try:
            if not bstack1ll1l1llll_opy_.on():
                return bstack1ll1l1ll1l_opy_
            if os.environ.get(bstack111ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦᔩ"), None) == bstack111ll11_opy_ (u"ࠢࡵࡴࡸࡩࠧᔪ"):
                tests = os.environ.get(bstack111ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧᔫ"), None)
                if tests is None or tests == bstack111ll11_opy_ (u"ࠤࡱࡹࡱࡲࠢᔬ"):
                    return bstack1ll1l1ll1l_opy_
                bstack1ll1l1ll1l_opy_ = tests.split(bstack111ll11_opy_ (u"ࠪ࠰ࠬᔭ"))
                return bstack1ll1l1ll1l_opy_
        except Exception as exc:
            print(bstack111ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧᔮ"), str(exc))
        return bstack1ll1l1ll1l_opy_
    @classmethod
    def bstack1l1l11111l_opy_(cls, event: str, bstack1l111l11l1_opy_: bstack1l11l1ll11_opy_):
        bstack1l11l1llll_opy_ = {
            bstack111ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᔯ"): event,
            bstack1l111l11l1_opy_.bstack1l11l1l11l_opy_(): bstack1l111l11l1_opy_.bstack1l111llll1_opy_(event)
        }
        bstack1ll1l1llll_opy_.bstack1l11ll11l1_opy_(bstack1l11l1llll_opy_)