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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11lll111ll_opy_, bstack1llll1111l_opy_, get_host_info, bstack11lll1llll_opy_, bstack11ll1ll1ll_opy_, bstack11ll1111l1_opy_, \
    bstack11ll11l1l1_opy_, bstack11l1ll1111_opy_, bstack1llll11ll_opy_, bstack11l11llll1_opy_, bstack11l1l11l1_opy_, bstack1l11111lll_opy_
from bstack_utils.bstack1111l11l11_opy_ import bstack11111lllll_opy_
from bstack_utils.bstack1l11l1lll1_opy_ import bstack1l11l1l1ll_opy_
bstack1llllll11ll_opy_ = [
    bstack11lllll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᑝ"), bstack11lllll_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᑞ"), bstack11lllll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᑟ"), bstack11lllll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᑠ"),
    bstack11lllll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᑡ"), bstack11lllll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᑢ"), bstack11lllll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᑣ")
]
bstack1lllllll11l_opy_ = bstack11lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᑤ")
logger = logging.getLogger(__name__)
class bstack1ll1llll1l_opy_:
    bstack1111l11l11_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l11111lll_opy_(class_method=True)
    def launch(cls, bs_config, bstack111111111l_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1lllllll1l1_opy_():
            return
        cls.bstack1lllllllll1_opy_()
        bstack11llll11l1_opy_ = bstack11lll1llll_opy_(bs_config)
        bstack11lll1l1l1_opy_ = bstack11ll1ll1ll_opy_(bs_config)
        data = {
            bstack11lllll_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭ᑥ"): bstack11lllll_opy_ (u"ࠧ࡫ࡵࡲࡲࠬᑦ"),
            bstack11lllll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧᑧ"): bs_config.get(bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᑨ"), bstack11lllll_opy_ (u"ࠪࠫᑩ")),
            bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᑪ"): bs_config.get(bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᑫ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᑬ"): bs_config.get(bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᑭ")),
            bstack11lllll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᑮ"): bs_config.get(bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᑯ"), bstack11lllll_opy_ (u"ࠪࠫᑰ")),
            bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡢࡸ࡮ࡳࡥࠨᑱ"): datetime.datetime.now().isoformat(),
            bstack11lllll_opy_ (u"ࠬࡺࡡࡨࡵࠪᑲ"): bstack11ll1111l1_opy_(bs_config),
            bstack11lllll_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩᑳ"): get_host_info(),
            bstack11lllll_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨᑴ"): bstack1llll1111l_opy_(),
            bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᑵ"): os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᑶ")),
            bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨᑷ"): os.environ.get(bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩᑸ"), False),
            bstack11lllll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧᑹ"): bstack11lll111ll_opy_(),
            bstack11lllll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᑺ"): {
                bstack11lllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᑻ"): bstack111111111l_opy_.get(bstack11lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩᑼ"), bstack11lllll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᑽ")),
                bstack11lllll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᑾ"): bstack111111111l_opy_.get(bstack11lllll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᑿ")),
                bstack11lllll_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᒀ"): bstack111111111l_opy_.get(bstack11lllll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᒁ"))
            }
        }
        config = {
            bstack11lllll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᒂ"): (bstack11llll11l1_opy_, bstack11lll1l1l1_opy_),
            bstack11lllll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᒃ"): cls.default_headers()
        }
        response = bstack1llll11ll_opy_(bstack11lllll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᒄ"), cls.request_url(bstack11lllll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵࠪᒅ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11lllll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪᒆ")] = bstack11lllll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᒇ")
            os.environ[bstack11lllll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᒈ")] = bstack11lllll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᒉ")
            os.environ[bstack11lllll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᒊ")] = bstack11lllll_opy_ (u"ࠤࡱࡹࡱࡲࠢᒋ")
            os.environ[bstack11lllll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᒌ")] = bstack11lllll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᒍ")
            bstack1lllllll111_opy_ = response.json()
            if bstack1lllllll111_opy_ and bstack1lllllll111_opy_[bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᒎ")]:
                error_message = bstack1lllllll111_opy_[bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᒏ")]
                if bstack1lllllll111_opy_[bstack11lllll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࡚ࡹࡱࡧࠪᒐ")] == bstack11lllll_opy_ (u"ࠨࡇࡕࡖࡔࡘ࡟ࡊࡐ࡙ࡅࡑࡏࡄࡠࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘ࠭ᒑ"):
                    logger.error(error_message)
                elif bstack1lllllll111_opy_[bstack11lllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᒒ")] == bstack11lllll_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠩᒓ"):
                    logger.info(error_message)
                elif bstack1lllllll111_opy_[bstack11lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᒔ")] == bstack11lllll_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡘࡊࡋࡠࡆࡈࡔࡗࡋࡃࡂࡖࡈࡈࠬᒕ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11lllll_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᒖ"))
            return [None, None, None]
        logger.debug(bstack11lllll_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᒗ"))
        os.environ[bstack11lllll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᒘ")] = bstack11lllll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᒙ")
        bstack1lllllll111_opy_ = response.json()
        if bstack1lllllll111_opy_.get(bstack11lllll_opy_ (u"ࠪ࡮ࡼࡺࠧᒚ")):
            os.environ[bstack11lllll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᒛ")] = bstack1lllllll111_opy_[bstack11lllll_opy_ (u"ࠬࡰࡷࡵࠩᒜ")]
            os.environ[bstack11lllll_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪᒝ")] = json.dumps({
                bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩᒞ"): bstack11llll11l1_opy_,
                bstack11lllll_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪᒟ"): bstack11lll1l1l1_opy_
            })
        if bstack1lllllll111_opy_.get(bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᒠ")):
            os.environ[bstack11lllll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᒡ")] = bstack1lllllll111_opy_[bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᒢ")]
        if bstack1lllllll111_opy_.get(bstack11lllll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᒣ")):
            os.environ[bstack11lllll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧᒤ")] = str(bstack1lllllll111_opy_[bstack11lllll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᒥ")])
        return [bstack1lllllll111_opy_[bstack11lllll_opy_ (u"ࠨ࡬ࡺࡸࠬᒦ")], bstack1lllllll111_opy_[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᒧ")], bstack1lllllll111_opy_[bstack11lllll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᒨ")]]
    @classmethod
    @bstack1l11111lll_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11lllll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᒩ")] == bstack11lllll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᒪ") or os.environ[bstack11lllll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᒫ")] == bstack11lllll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᒬ"):
            print(bstack11lllll_opy_ (u"ࠨࡇ࡛ࡇࡊࡖࡔࡊࡑࡑࠤࡎࡔࠠࡴࡶࡲࡴࡇࡻࡩ࡭ࡦࡘࡴࡸࡺࡲࡦࡣࡰࠤࡗࡋࡑࡖࡇࡖࡘ࡚ࠥࡏࠡࡖࡈࡗ࡙ࠦࡏࡃࡕࡈࡖ࡛ࡇࡂࡊࡎࡌࡘ࡞ࠦ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩᒭ"))
            return {
                bstack11lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᒮ"): bstack11lllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᒯ"),
                bstack11lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᒰ"): bstack11lllll_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪᒱ")
            }
        else:
            cls.bstack1111l11l11_opy_.shutdown()
            data = {
                bstack11lllll_opy_ (u"࠭ࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࠩᒲ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11lllll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᒳ"): cls.default_headers()
            }
            bstack11l11lll1l_opy_ = bstack11lllll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩᒴ").format(os.environ[bstack11lllll_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠣᒵ")])
            bstack1llllll1lll_opy_ = cls.request_url(bstack11l11lll1l_opy_)
            response = bstack1llll11ll_opy_(bstack11lllll_opy_ (u"ࠪࡔ࡚࡚ࠧᒶ"), bstack1llllll1lll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11lllll_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥᒷ"))
    @classmethod
    def bstack1l11l1111l_opy_(cls):
        if cls.bstack1111l11l11_opy_ is None:
            return
        cls.bstack1111l11l11_opy_.shutdown()
    @classmethod
    def bstack1lll11ll11_opy_(cls):
        if cls.on():
            print(
                bstack11lllll_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨᒸ").format(os.environ[bstack11lllll_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧᒹ")]))
    @classmethod
    def bstack1lllllllll1_opy_(cls):
        if cls.bstack1111l11l11_opy_ is not None:
            return
        cls.bstack1111l11l11_opy_ = bstack11111lllll_opy_(cls.bstack11111111ll_opy_)
        cls.bstack1111l11l11_opy_.start()
    @classmethod
    def bstack1l111l1111_opy_(cls, bstack1l111l11l1_opy_, bstack1llllll111l_opy_=bstack11lllll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᒺ")):
        if not cls.on():
            return
        bstack1ll111ll_opy_ = bstack1l111l11l1_opy_[bstack11lllll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᒻ")]
        bstack1111111111_opy_ = {
            bstack11lllll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᒼ"): bstack11lllll_opy_ (u"ࠪࡘࡪࡹࡴࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᒽ"),
            bstack11lllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᒾ"): bstack11lllll_opy_ (u"࡚ࠬࡥࡴࡶࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᒿ"),
            bstack11lllll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᓀ"): bstack11lllll_opy_ (u"ࠧࡕࡧࡶࡸࡤ࡙࡫ࡪࡲࡳࡩࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᓁ"),
            bstack11lllll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᓂ"): bstack11lllll_opy_ (u"ࠩࡏࡳ࡬ࡥࡕࡱ࡮ࡲࡥࡩ࠭ᓃ"),
            bstack11lllll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᓄ"): bstack11lllll_opy_ (u"ࠫࡍࡵ࡯࡬ࡡࡖࡸࡦࡸࡴࡠࡗࡳࡰࡴࡧࡤࠨᓅ"),
            bstack11lllll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᓆ"): bstack11lllll_opy_ (u"࠭ࡈࡰࡱ࡮ࡣࡊࡴࡤࡠࡗࡳࡰࡴࡧࡤࠨᓇ"),
            bstack11lllll_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᓈ"): bstack11lllll_opy_ (u"ࠨࡅࡅࡘࡤ࡛ࡰ࡭ࡱࡤࡨࠬᓉ")
        }.get(bstack1ll111ll_opy_)
        if bstack1llllll111l_opy_ == bstack11lllll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᓊ"):
            cls.bstack1lllllllll1_opy_()
            cls.bstack1111l11l11_opy_.add(bstack1l111l11l1_opy_)
        elif bstack1llllll111l_opy_ == bstack11lllll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᓋ"):
            cls.bstack11111111ll_opy_([bstack1l111l11l1_opy_], bstack1llllll111l_opy_)
    @classmethod
    @bstack1l11111lll_opy_(class_method=True)
    def bstack11111111ll_opy_(cls, bstack1l111l11l1_opy_, bstack1llllll111l_opy_=bstack11lllll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᓌ")):
        config = {
            bstack11lllll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᓍ"): cls.default_headers()
        }
        response = bstack1llll11ll_opy_(bstack11lllll_opy_ (u"࠭ࡐࡐࡕࡗࠫᓎ"), cls.request_url(bstack1llllll111l_opy_), bstack1l111l11l1_opy_, config)
        bstack11ll1lll11_opy_ = response.json()
    @classmethod
    @bstack1l11111lll_opy_(class_method=True)
    def bstack1l11ll1111_opy_(cls, bstack1l1l1111ll_opy_):
        bstack1llllllll11_opy_ = []
        for log in bstack1l1l1111ll_opy_:
            bstack11111111l1_opy_ = {
                bstack11lllll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᓏ"): bstack11lllll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪᓐ"),
                bstack11lllll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᓑ"): log[bstack11lllll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᓒ")],
                bstack11lllll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᓓ"): log[bstack11lllll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᓔ")],
                bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭ᓕ"): {},
                bstack11lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᓖ"): log[bstack11lllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᓗ")],
            }
            if bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓘ") in log:
                bstack11111111l1_opy_[bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓙ")] = log[bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓚ")]
            elif bstack11lllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᓛ") in log:
                bstack11111111l1_opy_[bstack11lllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓜ")] = log[bstack11lllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᓝ")]
            bstack1llllllll11_opy_.append(bstack11111111l1_opy_)
        cls.bstack1l111l1111_opy_({
            bstack11lllll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᓞ"): bstack11lllll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᓟ"),
            bstack11lllll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᓠ"): bstack1llllllll11_opy_
        })
    @classmethod
    @bstack1l11111lll_opy_(class_method=True)
    def bstack1llllll1l1l_opy_(cls, steps):
        bstack1llllllllll_opy_ = []
        for step in steps:
            bstack1llllll11l1_opy_ = {
                bstack11lllll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᓡ"): bstack11lllll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨᓢ"),
                bstack11lllll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᓣ"): step[bstack11lllll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᓤ")],
                bstack11lllll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᓥ"): step[bstack11lllll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᓦ")],
                bstack11lllll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᓧ"): step[bstack11lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᓨ")],
                bstack11lllll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᓩ"): step[bstack11lllll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᓪ")]
            }
            if bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᓫ") in step:
                bstack1llllll11l1_opy_[bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓬ")] = step[bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓭ")]
            elif bstack11lllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓮ") in step:
                bstack1llllll11l1_opy_[bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓯ")] = step[bstack11lllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᓰ")]
            bstack1llllllllll_opy_.append(bstack1llllll11l1_opy_)
        cls.bstack1l111l1111_opy_({
            bstack11lllll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᓱ"): bstack11lllll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᓲ"),
            bstack11lllll_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᓳ"): bstack1llllllllll_opy_
        })
    @classmethod
    @bstack1l11111lll_opy_(class_method=True)
    def bstack111l1lll1_opy_(cls, screenshot):
        cls.bstack1l111l1111_opy_({
            bstack11lllll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᓴ"): bstack11lllll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᓵ"),
            bstack11lllll_opy_ (u"ࠫࡱࡵࡧࡴࠩᓶ"): [{
                bstack11lllll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᓷ"): bstack11lllll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨᓸ"),
                bstack11lllll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᓹ"): datetime.datetime.utcnow().isoformat() + bstack11lllll_opy_ (u"ࠨ࡜ࠪᓺ"),
                bstack11lllll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓻ"): screenshot[bstack11lllll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᓼ")],
                bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓽ"): screenshot[bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᓾ")]
            }]
        }, bstack1llllll111l_opy_=bstack11lllll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᓿ"))
    @classmethod
    @bstack1l11111lll_opy_(class_method=True)
    def bstack111ll11l1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111l1111_opy_({
            bstack11lllll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᔀ"): bstack11lllll_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᔁ"),
            bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᔂ"): {
                bstack11lllll_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᔃ"): cls.current_test_uuid(),
                bstack11lllll_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥᔄ"): cls.bstack1l11l1l1l1_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᔅ"), None) is None or os.environ[bstack11lllll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᔆ")] == bstack11lllll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᔇ"):
            return False
        return True
    @classmethod
    def bstack1lllllll1l1_opy_(cls):
        return bstack11l1l11l1_opy_(cls.bs_config.get(bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᔈ"), False))
    @staticmethod
    def request_url(url):
        return bstack11lllll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨᔉ").format(bstack1lllllll11l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11lllll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᔊ"): bstack11lllll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᔋ"),
            bstack11lllll_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨᔌ"): bstack11lllll_opy_ (u"࠭ࡴࡳࡷࡨࠫᔍ")
        }
        if os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᔎ"), None):
            headers[bstack11lllll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᔏ")] = bstack11lllll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬᔐ").format(os.environ[bstack11lllll_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠦᔑ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᔒ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᔓ"), None)
    @staticmethod
    def bstack1l1111llll_opy_():
        if getattr(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᔔ"), None):
            return {
                bstack11lllll_opy_ (u"ࠧࡵࡻࡳࡩࠬᔕ"): bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᔖ"),
                bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᔗ"): getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᔘ"), None)
            }
        if getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᔙ"), None):
            return {
                bstack11lllll_opy_ (u"ࠬࡺࡹࡱࡧࠪᔚ"): bstack11lllll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᔛ"),
                bstack11lllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᔜ"): getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᔝ"), None)
            }
        return None
    @staticmethod
    def bstack1l11l1l1l1_opy_(driver):
        return {
            bstack11l1ll1111_opy_(): bstack11ll11l1l1_opy_(driver)
        }
    @staticmethod
    def bstack1llllllll1l_opy_(exception_info, report):
        return [{bstack11lllll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᔞ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11llll1l1l_opy_(typename):
        if bstack11lllll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᔟ") in typename:
            return bstack11lllll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᔠ")
        return bstack11lllll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᔡ")
    @staticmethod
    def bstack1llllll1111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1llll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l1111ll11_opy_(test, hook_name=None):
        bstack1llllll1ll1_opy_ = test.parent
        if hook_name in [bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᔢ"), bstack11lllll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᔣ"), bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᔤ"), bstack11lllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᔥ")]:
            bstack1llllll1ll1_opy_ = test
        scope = []
        while bstack1llllll1ll1_opy_ is not None:
            scope.append(bstack1llllll1ll1_opy_.name)
            bstack1llllll1ll1_opy_ = bstack1llllll1ll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lllllll1ll_opy_(hook_type):
        if hook_type == bstack11lllll_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣᔦ"):
            return bstack11lllll_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣᔧ")
        elif hook_type == bstack11lllll_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤᔨ"):
            return bstack11lllll_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨᔩ")
    @staticmethod
    def bstack1llllll1l11_opy_(bstack1lll11l11l_opy_):
        try:
            if not bstack1ll1llll1l_opy_.on():
                return bstack1lll11l11l_opy_
            if os.environ.get(bstack11lllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧᔪ"), None) == bstack11lllll_opy_ (u"ࠣࡶࡵࡹࡪࠨᔫ"):
                tests = os.environ.get(bstack11lllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨᔬ"), None)
                if tests is None or tests == bstack11lllll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᔭ"):
                    return bstack1lll11l11l_opy_
                bstack1lll11l11l_opy_ = tests.split(bstack11lllll_opy_ (u"ࠫ࠱࠭ᔮ"))
                return bstack1lll11l11l_opy_
        except Exception as exc:
            print(bstack11lllll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨᔯ"), str(exc))
        return bstack1lll11l11l_opy_
    @classmethod
    def bstack1l1111l11l_opy_(cls, event: str, bstack1l111l11l1_opy_: bstack1l11l1l1ll_opy_):
        bstack1l11l1l11l_opy_ = {
            bstack11lllll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᔰ"): event,
            bstack1l111l11l1_opy_.bstack1l11l1l111_opy_(): bstack1l111l11l1_opy_.bstack1l11l11lll_opy_(event)
        }
        bstack1ll1llll1l_opy_.bstack1l111l1111_opy_(bstack1l11l1l11l_opy_)