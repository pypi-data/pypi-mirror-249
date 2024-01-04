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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll1llll1_opy_, bstack1ll11111ll_opy_, get_host_info, bstack11lll1l111_opy_, bstack11ll1ll1ll_opy_, bstack11ll111l11_opy_, \
    bstack11l1ll1lll_opy_, bstack11l1l111l1_opy_, bstack1l1llllll1_opy_, bstack11l11lll11_opy_, bstack1l1l1ll11_opy_, bstack1l1111l111_opy_
from bstack_utils.bstack1111l11111_opy_ import bstack1111l1l111_opy_
from bstack_utils.bstack1l11lllll1_opy_ import bstack1l11l11l11_opy_
bstack1llllll11l1_opy_ = [
    bstack1lll11l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᑛ"), bstack1lll11l_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᑜ"), bstack1lll11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᑝ"), bstack1lll11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᑞ"),
    bstack1lll11l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᑟ"), bstack1lll11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᑠ"), bstack1lll11l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᑡ")
]
bstack1llllllllll_opy_ = bstack1lll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᑢ")
logger = logging.getLogger(__name__)
class bstack1l11ll1ll_opy_:
    bstack1111l11111_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1111l111_opy_(class_method=True)
    def launch(cls, bs_config, bstack1111111111_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1111111l11_opy_():
            return
        cls.bstack11111111l1_opy_()
        bstack11lll11ll1_opy_ = bstack11lll1l111_opy_(bs_config)
        bstack11ll1lllll_opy_ = bstack11ll1ll1ll_opy_(bs_config)
        data = {
            bstack1lll11l_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫᑣ"): bstack1lll11l_opy_ (u"ࠬࡰࡳࡰࡰࠪᑤ"),
            bstack1lll11l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬᑥ"): bs_config.get(bstack1lll11l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᑦ"), bstack1lll11l_opy_ (u"ࠨࠩᑧ")),
            bstack1lll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᑨ"): bs_config.get(bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᑩ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᑪ"): bs_config.get(bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᑫ")),
            bstack1lll11l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᑬ"): bs_config.get(bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᑭ"), bstack1lll11l_opy_ (u"ࠨࠩᑮ")),
            bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡠࡶ࡬ࡱࡪ࠭ᑯ"): datetime.datetime.now().isoformat(),
            bstack1lll11l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᑰ"): bstack11ll111l11_opy_(bs_config),
            bstack1lll11l_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧᑱ"): get_host_info(),
            bstack1lll11l_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ᑲ"): bstack1ll11111ll_opy_(),
            bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᑳ"): os.environ.get(bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᑴ")),
            bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ᑵ"): os.environ.get(bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧᑶ"), False),
            bstack1lll11l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬᑷ"): bstack11ll1llll1_opy_(),
            bstack1lll11l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᑸ"): {
                bstack1lll11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᑹ"): bstack1111111111_opy_.get(bstack1lll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧᑺ"), bstack1lll11l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᑻ")),
                bstack1lll11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᑼ"): bstack1111111111_opy_.get(bstack1lll11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᑽ")),
                bstack1lll11l_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᑾ"): bstack1111111111_opy_.get(bstack1lll11l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᑿ"))
            }
        }
        config = {
            bstack1lll11l_opy_ (u"ࠬࡧࡵࡵࡪࠪᒀ"): (bstack11lll11ll1_opy_, bstack11ll1lllll_opy_),
            bstack1lll11l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᒁ"): cls.default_headers()
        }
        response = bstack1l1llllll1_opy_(bstack1lll11l_opy_ (u"ࠧࡑࡑࡖࡘࠬᒂ"), cls.request_url(bstack1lll11l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳࠨᒃ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1lll11l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨᒄ")] = bstack1lll11l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᒅ")
            os.environ[bstack1lll11l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᒆ")] = bstack1lll11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᒇ")
            os.environ[bstack1lll11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᒈ")] = bstack1lll11l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᒉ")
            os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᒊ")] = bstack1lll11l_opy_ (u"ࠤࡱࡹࡱࡲࠢᒋ")
            bstack1llllll1ll1_opy_ = response.json()
            if bstack1llllll1ll1_opy_ and bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᒌ")]:
                error_message = bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᒍ")]
                if bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡘࡾࡶࡥࠨᒎ")] == bstack1lll11l_opy_ (u"࠭ࡅࡓࡔࡒࡖࡤࡏࡎࡗࡃࡏࡍࡉࡥࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࠫᒏ"):
                    logger.error(error_message)
                elif bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࡚ࡹࡱࡧࠪᒐ")] == bstack1lll11l_opy_ (u"ࠨࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠧᒑ"):
                    logger.info(error_message)
                elif bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᒒ")] == bstack1lll11l_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡖࡈࡐࡥࡄࡆࡒࡕࡉࡈࡇࡔࡆࡆࠪᒓ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1lll11l_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡙࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᒔ"))
            return [None, None, None]
        logger.debug(bstack1lll11l_opy_ (u"࡚ࠬࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩᒕ"))
        os.environ[bstack1lll11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᒖ")] = bstack1lll11l_opy_ (u"ࠧࡵࡴࡸࡩࠬᒗ")
        bstack1llllll1ll1_opy_ = response.json()
        if bstack1llllll1ll1_opy_.get(bstack1lll11l_opy_ (u"ࠨ࡬ࡺࡸࠬᒘ")):
            os.environ[bstack1lll11l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᒙ")] = bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"ࠪ࡮ࡼࡺࠧᒚ")]
            os.environ[bstack1lll11l_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨᒛ")] = json.dumps({
                bstack1lll11l_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧᒜ"): bstack11lll11ll1_opy_,
                bstack1lll11l_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨᒝ"): bstack11ll1lllll_opy_
            })
        if bstack1llllll1ll1_opy_.get(bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᒞ")):
            os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᒟ")] = bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᒠ")]
        if bstack1llllll1ll1_opy_.get(bstack1lll11l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᒡ")):
            os.environ[bstack1lll11l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬᒢ")] = str(bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᒣ")])
        return [bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"࠭ࡪࡸࡶࠪᒤ")], bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᒥ")], bstack1llllll1ll1_opy_[bstack1lll11l_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᒦ")]]
    @classmethod
    @bstack1l1111l111_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1lll11l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᒧ")] == bstack1lll11l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᒨ") or os.environ[bstack1lll11l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᒩ")] == bstack1lll11l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᒪ"):
            print(bstack1lll11l_opy_ (u"࠭ࡅ࡙ࡅࡈࡔ࡙ࡏࡏࡏࠢࡌࡒࠥࡹࡴࡰࡲࡅࡹ࡮ࡲࡤࡖࡲࡶࡸࡷ࡫ࡡ࡮ࠢࡕࡉࡖ࡛ࡅࡔࡖࠣࡘࡔࠦࡔࡆࡕࡗࠤࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠤ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᒫ"))
            return {
                bstack1lll11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᒬ"): bstack1lll11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᒭ"),
                bstack1lll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᒮ"): bstack1lll11l_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨᒯ")
            }
        else:
            cls.bstack1111l11111_opy_.shutdown()
            data = {
                bstack1lll11l_opy_ (u"ࠫࡸࡺ࡯ࡱࡡࡷ࡭ࡲ࡫ࠧᒰ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1lll11l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᒱ"): cls.default_headers()
            }
            bstack11l1l1ll11_opy_ = bstack1lll11l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧᒲ").format(os.environ[bstack1lll11l_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨᒳ")])
            bstack1lllllll111_opy_ = cls.request_url(bstack11l1l1ll11_opy_)
            response = bstack1l1llllll1_opy_(bstack1lll11l_opy_ (u"ࠨࡒࡘࡘࠬᒴ"), bstack1lllllll111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1lll11l_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣᒵ"))
    @classmethod
    def bstack1l11ll111l_opy_(cls):
        if cls.bstack1111l11111_opy_ is None:
            return
        cls.bstack1111l11111_opy_.shutdown()
    @classmethod
    def bstack1l1ll1l1ll_opy_(cls):
        if cls.on():
            print(
                bstack1lll11l_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭ᒶ").format(os.environ[bstack1lll11l_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠥᒷ")]))
    @classmethod
    def bstack11111111l1_opy_(cls):
        if cls.bstack1111l11111_opy_ is not None:
            return
        cls.bstack1111l11111_opy_ = bstack1111l1l111_opy_(cls.bstack1llllllll1l_opy_)
        cls.bstack1111l11111_opy_.start()
    @classmethod
    def bstack1l1111lll1_opy_(cls, bstack1l11lll11l_opy_, bstack1lllllll1l1_opy_=bstack1lll11l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᒸ")):
        if not cls.on():
            return
        bstack1ll1ll1111_opy_ = bstack1l11lll11l_opy_[bstack1lll11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᒹ")]
        bstack11111111ll_opy_ = {
            bstack1lll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᒺ"): bstack1lll11l_opy_ (u"ࠨࡖࡨࡷࡹࡥࡓࡵࡣࡵࡸࡤ࡛ࡰ࡭ࡱࡤࡨࠬᒻ"),
            bstack1lll11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᒼ"): bstack1lll11l_opy_ (u"ࠪࡘࡪࡹࡴࡠࡇࡱࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᒽ"),
            bstack1lll11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᒾ"): bstack1lll11l_opy_ (u"࡚ࠬࡥࡴࡶࡢࡗࡰ࡯ࡰࡱࡧࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫᒿ"),
            bstack1lll11l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᓀ"): bstack1lll11l_opy_ (u"ࠧࡍࡱࡪࡣ࡚ࡶ࡬ࡰࡣࡧࠫᓁ"),
            bstack1lll11l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᓂ"): bstack1lll11l_opy_ (u"ࠩࡋࡳࡴࡱ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᓃ"),
            bstack1lll11l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᓄ"): bstack1lll11l_opy_ (u"ࠫࡍࡵ࡯࡬ࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᓅ"),
            bstack1lll11l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᓆ"): bstack1lll11l_opy_ (u"࠭ࡃࡃࡖࡢ࡙ࡵࡲ࡯ࡢࡦࠪᓇ")
        }.get(bstack1ll1ll1111_opy_)
        if bstack1lllllll1l1_opy_ == bstack1lll11l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᓈ"):
            cls.bstack11111111l1_opy_()
            cls.bstack1111l11111_opy_.add(bstack1l11lll11l_opy_)
        elif bstack1lllllll1l1_opy_ == bstack1lll11l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᓉ"):
            cls.bstack1llllllll1l_opy_([bstack1l11lll11l_opy_], bstack1lllllll1l1_opy_)
    @classmethod
    @bstack1l1111l111_opy_(class_method=True)
    def bstack1llllllll1l_opy_(cls, bstack1l11lll11l_opy_, bstack1lllllll1l1_opy_=bstack1lll11l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᓊ")):
        config = {
            bstack1lll11l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᓋ"): cls.default_headers()
        }
        response = bstack1l1llllll1_opy_(bstack1lll11l_opy_ (u"ࠫࡕࡕࡓࡕࠩᓌ"), cls.request_url(bstack1lllllll1l1_opy_), bstack1l11lll11l_opy_, config)
        bstack11ll1lll11_opy_ = response.json()
    @classmethod
    @bstack1l1111l111_opy_(class_method=True)
    def bstack1l11ll11l1_opy_(cls, bstack1l11ll1ll1_opy_):
        bstack111111111l_opy_ = []
        for log in bstack1l11ll1ll1_opy_:
            bstack1llllllll11_opy_ = {
                bstack1lll11l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᓍ"): bstack1lll11l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨᓎ"),
                bstack1lll11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᓏ"): log[bstack1lll11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᓐ")],
                bstack1lll11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᓑ"): log[bstack1lll11l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᓒ")],
                bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫᓓ"): {},
                bstack1lll11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᓔ"): log[bstack1lll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᓕ")],
            }
            if bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᓖ") in log:
                bstack1llllllll11_opy_[bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓗ")] = log[bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓘ")]
            elif bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓙ") in log:
                bstack1llllllll11_opy_[bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓚ")] = log[bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᓛ")]
            bstack111111111l_opy_.append(bstack1llllllll11_opy_)
        cls.bstack1l1111lll1_opy_({
            bstack1lll11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᓜ"): bstack1lll11l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᓝ"),
            bstack1lll11l_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᓞ"): bstack111111111l_opy_
        })
    @classmethod
    @bstack1l1111l111_opy_(class_method=True)
    def bstack1lllllll11l_opy_(cls, steps):
        bstack1llllll1l11_opy_ = []
        for step in steps:
            bstack1lllllllll1_opy_ = {
                bstack1lll11l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᓟ"): bstack1lll11l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭ᓠ"),
                bstack1lll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᓡ"): step[bstack1lll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᓢ")],
                bstack1lll11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᓣ"): step[bstack1lll11l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᓤ")],
                bstack1lll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᓥ"): step[bstack1lll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓦ")],
                bstack1lll11l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᓧ"): step[bstack1lll11l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᓨ")]
            }
            if bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᓩ") in step:
                bstack1lllllllll1_opy_[bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓪ")] = step[bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᓫ")]
            elif bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓬ") in step:
                bstack1lllllllll1_opy_[bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓭ")] = step[bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓮ")]
            bstack1llllll1l11_opy_.append(bstack1lllllllll1_opy_)
        cls.bstack1l1111lll1_opy_({
            bstack1lll11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᓯ"): bstack1lll11l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᓰ"),
            bstack1lll11l_opy_ (u"࠭࡬ࡰࡩࡶࠫᓱ"): bstack1llllll1l11_opy_
        })
    @classmethod
    @bstack1l1111l111_opy_(class_method=True)
    def bstack111ll1l1l_opy_(cls, screenshot):
        cls.bstack1l1111lll1_opy_({
            bstack1lll11l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᓲ"): bstack1lll11l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᓳ"),
            bstack1lll11l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᓴ"): [{
                bstack1lll11l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᓵ"): bstack1lll11l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭ᓶ"),
                bstack1lll11l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᓷ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"࡚࠭ࠨᓸ"),
                bstack1lll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᓹ"): screenshot[bstack1lll11l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧᓺ")],
                bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓻ"): screenshot[bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓼ")]
            }]
        }, bstack1lllllll1l1_opy_=bstack1lll11l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᓽ"))
    @classmethod
    @bstack1l1111l111_opy_(class_method=True)
    def bstack11111111l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1111lll1_opy_({
            bstack1lll11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᓾ"): bstack1lll11l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᓿ"),
            bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᔀ"): {
                bstack1lll11l_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᔁ"): cls.current_test_uuid(),
                bstack1lll11l_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣᔂ"): cls.bstack1l11llll11_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1lll11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᔃ"), None) is None or os.environ[bstack1lll11l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᔄ")] == bstack1lll11l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᔅ"):
            return False
        return True
    @classmethod
    def bstack1111111l11_opy_(cls):
        return bstack1l1l1ll11_opy_(cls.bs_config.get(bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᔆ"), False))
    @staticmethod
    def request_url(url):
        return bstack1lll11l_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᔇ").format(bstack1llllllllll_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1lll11l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᔈ"): bstack1lll11l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᔉ"),
            bstack1lll11l_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭ᔊ"): bstack1lll11l_opy_ (u"ࠫࡹࡸࡵࡦࠩᔋ")
        }
        if os.environ.get(bstack1lll11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᔌ"), None):
            headers[bstack1lll11l_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᔍ")] = bstack1lll11l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪᔎ").format(os.environ[bstack1lll11l_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠤᔏ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᔐ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᔑ"), None)
    @staticmethod
    def bstack1l11ll1l1l_opy_():
        if getattr(threading.current_thread(), bstack1lll11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᔒ"), None):
            return {
                bstack1lll11l_opy_ (u"ࠬࡺࡹࡱࡧࠪᔓ"): bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࠫᔔ"),
                bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᔕ"): getattr(threading.current_thread(), bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᔖ"), None)
            }
        if getattr(threading.current_thread(), bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᔗ"), None):
            return {
                bstack1lll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨᔘ"): bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᔙ"),
                bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᔚ"): getattr(threading.current_thread(), bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᔛ"), None)
            }
        return None
    @staticmethod
    def bstack1l11llll11_opy_(driver):
        return {
            bstack11l1l111l1_opy_(): bstack11l1ll1lll_opy_(driver)
        }
    @staticmethod
    def bstack1lllllll1ll_opy_(exception_info, report):
        return [{bstack1lll11l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᔜ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11llll1l11_opy_(typename):
        if bstack1lll11l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᔝ") in typename:
            return bstack1lll11l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᔞ")
        return bstack1lll11l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᔟ")
    @staticmethod
    def bstack1llllll1l1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11ll1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11l1l11l_opy_(test, hook_name=None):
        bstack1llllll111l_opy_ = test.parent
        if hook_name in [bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᔠ"), bstack1lll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᔡ"), bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᔢ"), bstack1lll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᔣ")]:
            bstack1llllll111l_opy_ = test
        scope = []
        while bstack1llllll111l_opy_ is not None:
            scope.append(bstack1llllll111l_opy_.name)
            bstack1llllll111l_opy_ = bstack1llllll111l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llllll11ll_opy_(hook_type):
        if hook_type == bstack1lll11l_opy_ (u"ࠣࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍࠨᔤ"):
            return bstack1lll11l_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡪࡲࡳࡰࠨᔥ")
        elif hook_type == bstack1lll11l_opy_ (u"ࠥࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠢᔦ"):
            return bstack1lll11l_opy_ (u"࡙ࠦ࡫ࡡࡳࡦࡲࡻࡳࠦࡨࡰࡱ࡮ࠦᔧ")
    @staticmethod
    def bstack1llllll1lll_opy_(bstack111l1l111_opy_):
        try:
            if not bstack1l11ll1ll_opy_.on():
                return bstack111l1l111_opy_
            if os.environ.get(bstack1lll11l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠥᔨ"), None) == bstack1lll11l_opy_ (u"ࠨࡴࡳࡷࡨࠦᔩ"):
                tests = os.environ.get(bstack1lll11l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠦᔪ"), None)
                if tests is None or tests == bstack1lll11l_opy_ (u"ࠣࡰࡸࡰࡱࠨᔫ"):
                    return bstack111l1l111_opy_
                bstack111l1l111_opy_ = tests.split(bstack1lll11l_opy_ (u"ࠩ࠯ࠫᔬ"))
                return bstack111l1l111_opy_
        except Exception as exc:
            print(bstack1lll11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡩࡷࡻ࡮ࠡࡪࡤࡲࡩࡲࡥࡳ࠼ࠣࠦᔭ"), str(exc))
        return bstack111l1l111_opy_
    @classmethod
    def bstack1l111l1lll_opy_(cls, event: str, bstack1l11lll11l_opy_: bstack1l11l11l11_opy_):
        bstack1l1l11111l_opy_ = {
            bstack1lll11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᔮ"): event,
            bstack1l11lll11l_opy_.bstack1l111ll1ll_opy_(): bstack1l11lll11l_opy_.bstack1l111ll11l_opy_(event)
        }
        bstack1l11ll1ll_opy_.bstack1l1111lll1_opy_(bstack1l1l11111l_opy_)