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
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11lll1l111_opy_ as bstack11lll11l11_opy_
from bstack_utils.helper import bstack111l11ll1_opy_, bstack1l1l111ll_opy_, bstack11lll1l1ll_opy_, bstack11lll11ll1_opy_, bstack1l1lll1111_opy_, get_host_info, bstack11ll1ll1ll_opy_, bstack1ll111lll1_opy_, bstack1l11lll1ll_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l11lll1ll_opy_(class_method=False)
def _11ll1lllll_opy_(driver, bstack111lll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111ll11_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭෾"): caps.get(bstack111ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬ෿"), None),
        bstack111ll11_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ฀"): bstack111lll11_opy_.get(bstack111ll11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫก"), None),
        bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨข"): caps.get(bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨฃ"), None),
        bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ค"): caps.get(bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ฅ"), None)
    }
  except Exception as error:
    logger.debug(bstack111ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪฆ") + str(error))
  return response
def bstack1l111l11_opy_(config):
  return config.get(bstack111ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧง"), False) or any([p.get(bstack111ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨจ"), False) == True for p in config[bstack111ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬฉ")]])
def bstack1ll111l1l_opy_(config, bstack1ll1l1ll_opy_):
  try:
    if not bstack1l1l111ll_opy_(config):
      return False
    bstack11llll11ll_opy_ = config.get(bstack111ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪช"), False)
    bstack11lll1l11l_opy_ = config[bstack111ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧซ")][bstack1ll1l1ll_opy_].get(bstack111ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬฌ"), None)
    if bstack11lll1l11l_opy_ != None:
      bstack11llll11ll_opy_ = bstack11lll1l11l_opy_
    bstack11lll1l1l1_opy_ = os.getenv(bstack111ll11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫญ")) is not None and len(os.getenv(bstack111ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬฎ"))) > 0 and os.getenv(bstack111ll11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ฏ")) != bstack111ll11_opy_ (u"ࠩࡱࡹࡱࡲࠧฐ")
    return bstack11llll11ll_opy_ and bstack11lll1l1l1_opy_
  except Exception as error:
    logger.debug(bstack111ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪฑ") + str(error))
  return False
def bstack1llll11l1l_opy_(bstack11lll111ll_opy_, test_tags):
  bstack11lll111ll_opy_ = os.getenv(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬฒ"))
  if bstack11lll111ll_opy_ is None:
    return True
  bstack11lll111ll_opy_ = json.loads(bstack11lll111ll_opy_)
  try:
    include_tags = bstack11lll111ll_opy_[bstack111ll11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪณ")] if bstack111ll11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫด") in bstack11lll111ll_opy_ and isinstance(bstack11lll111ll_opy_[bstack111ll11_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬต")], list) else []
    exclude_tags = bstack11lll111ll_opy_[bstack111ll11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ถ")] if bstack111ll11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧท") in bstack11lll111ll_opy_ and isinstance(bstack11lll111ll_opy_[bstack111ll11_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨธ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦน") + str(error))
  return False
def bstack1l11l11l_opy_(config, bstack11llll11l1_opy_, bstack11lll11lll_opy_):
  bstack11ll1lll11_opy_ = bstack11lll1l1ll_opy_(config)
  bstack11lll1ll1l_opy_ = bstack11lll11ll1_opy_(config)
  if bstack11ll1lll11_opy_ is None or bstack11lll1ll1l_opy_ is None:
    logger.error(bstack111ll11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭บ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧป"), bstack111ll11_opy_ (u"ࠧࡼࡿࠪผ")))
    data = {
        bstack111ll11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ฝ"): config[bstack111ll11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧพ")],
        bstack111ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ฟ"): config.get(bstack111ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧภ"), os.path.basename(os.getcwd())),
        bstack111ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨม"): bstack111l11ll1_opy_(),
        bstack111ll11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫย"): config.get(bstack111ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪร"), bstack111ll11_opy_ (u"ࠨࠩฤ")),
        bstack111ll11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩล"): {
            bstack111ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪฦ"): bstack11llll11l1_opy_,
            bstack111ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧว"): bstack11lll11lll_opy_,
            bstack111ll11_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩศ"): __version__
        },
        bstack111ll11_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨษ"): settings,
        bstack111ll11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨส"): bstack11ll1ll1ll_opy_(),
        bstack111ll11_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨห"): bstack1l1lll1111_opy_(),
        bstack111ll11_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫฬ"): get_host_info(),
        bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬอ"): bstack1l1l111ll_opy_(config)
    }
    headers = {
        bstack111ll11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪฮ"): bstack111ll11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨฯ"),
    }
    config = {
        bstack111ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫะ"): (bstack11ll1lll11_opy_, bstack11lll1ll1l_opy_),
        bstack111ll11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨั"): headers
    }
    response = bstack1ll111lll1_opy_(bstack111ll11_opy_ (u"ࠨࡒࡒࡗ࡙࠭า"), bstack11lll11l11_opy_ + bstack111ll11_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠭ำ"), data, config)
    bstack11lll1llll_opy_ = response.json()
    if bstack11lll1llll_opy_[bstack111ll11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫิ")]:
      parsed = json.loads(os.getenv(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬี"), bstack111ll11_opy_ (u"ࠬࢁࡽࠨึ")))
      parsed[bstack111ll11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧื")] = bstack11lll1llll_opy_[bstack111ll11_opy_ (u"ࠧࡥࡣࡷࡥุࠬ")][bstack111ll11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ูࠩ")]
      os.environ[bstack111ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎฺࠪ")] = json.dumps(parsed)
      return bstack11lll1llll_opy_[bstack111ll11_opy_ (u"ࠪࡨࡦࡺࡡࠨ฻")][bstack111ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩ฼")], bstack11lll1llll_opy_[bstack111ll11_opy_ (u"ࠬࡪࡡࡵࡣࠪ฽")][bstack111ll11_opy_ (u"࠭ࡩࡥࠩ฾")]
    else:
      logger.error(bstack111ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨ฿") + bstack11lll1llll_opy_[bstack111ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩเ")])
      if bstack11lll1llll_opy_[bstack111ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪแ")] == bstack111ll11_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬโ"):
        for bstack11ll1llll1_opy_ in bstack11lll1llll_opy_[bstack111ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫใ")]:
          logger.error(bstack11ll1llll1_opy_[bstack111ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ไ")])
      return None, None
  except Exception as error:
    logger.error(bstack111ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢๅ") +  str(error))
    return None, None
def bstack111l1111l_opy_():
  if os.getenv(bstack111ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬๆ")) is None:
    return {
        bstack111ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ็"): bstack111ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ่"),
        bstack111ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨ้ࠫ"): bstack111ll11_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰๊ࠪ")
    }
  data = {bstack111ll11_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ๋࠭"): bstack111l11ll1_opy_()}
  headers = {
      bstack111ll11_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭์"): bstack111ll11_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨํ") + os.getenv(bstack111ll11_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨ๎")),
      bstack111ll11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ๏"): bstack111ll11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭๐")
  }
  response = bstack1ll111lll1_opy_(bstack111ll11_opy_ (u"ࠫࡕ࡛ࡔࠨ๑"), bstack11lll11l11_opy_ + bstack111ll11_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧ๒"), data, { bstack111ll11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ๓"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111ll11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣ๔") + datetime.utcnow().isoformat() + bstack111ll11_opy_ (u"ࠨ࡜ࠪ๕"))
      return {bstack111ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ๖"): bstack111ll11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ๗"), bstack111ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ๘"): bstack111ll11_opy_ (u"ࠬ࠭๙")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤ๚") + str(error))
    return {
        bstack111ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ๛"): bstack111ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ๜"),
        bstack111ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ๝"): str(error)
    }
def bstack1l11lll11_opy_(caps, options):
  try:
    bstack11lll11l1l_opy_ = caps.get(bstack111ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ๞"), {}).get(bstack111ll11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ๟"), caps.get(bstack111ll11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ๠"), bstack111ll11_opy_ (u"࠭ࠧ๡")))
    if bstack11lll11l1l_opy_:
      logger.warn(bstack111ll11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ๢"))
      return False
    browser = caps.get(bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭๣"), bstack111ll11_opy_ (u"ࠩࠪ๤")).lower()
    if browser != bstack111ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ๥"):
      logger.warn(bstack111ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ๦"))
      return False
    browser_version = caps.get(bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๧"), caps.get(bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๨")))
    if browser_version and browser_version != bstack111ll11_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧ๩") and int(browser_version.split(bstack111ll11_opy_ (u"ࠨ࠰ࠪ๪"))[0]) <= 94:
      logger.warn(bstack111ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣ࠽࠹࠴ࠢ๫"))
      return False
    if not options is None:
      bstack11lll1lll1_opy_ = options.to_capabilities().get(bstack111ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ๬"), {})
      if bstack111ll11_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨ๭") in bstack11lll1lll1_opy_.get(bstack111ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪ๮"), []):
        logger.warn(bstack111ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣ๯"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack111ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤ๰") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11lll111l1_opy_ = config.get(bstack111ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ๱"), {})
    bstack11lll111l1_opy_[bstack111ll11_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬ๲")] = os.getenv(bstack111ll11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ๳"))
    bstack11lll1111l_opy_ = json.loads(os.getenv(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ๴"), bstack111ll11_opy_ (u"ࠬࢁࡽࠨ๵"))).get(bstack111ll11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ๶"))
    caps[bstack111ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ๷")] = True
    if bstack111ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ๸") in caps:
      caps[bstack111ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ๹")][bstack111ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ๺")] = bstack11lll111l1_opy_
      caps[bstack111ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ๻")][bstack111ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ๼")][bstack111ll11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ๽")] = bstack11lll1111l_opy_
    else:
      caps[bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭๾")] = bstack11lll111l1_opy_
      caps[bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ๿")][bstack111ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ຀")] = bstack11lll1111l_opy_
  except Exception as error:
    logger.debug(bstack111ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦກ") +  str(error))
def bstack1l1l1l11l1_opy_(driver, bstack11llll1111_opy_):
  try:
    session = driver.session_id
    if session:
      bstack11llll111l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11llll111l_opy_ = False
      bstack11llll111l_opy_ = url.scheme in [bstack111ll11_opy_ (u"ࠦ࡭ࡺࡴࡱࠤຂ"), bstack111ll11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ຃")]
      if bstack11llll111l_opy_:
        if bstack11llll1111_opy_:
          logger.info(bstack111ll11_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨຄ"))
          driver.execute_async_script(bstack111ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡂࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴ࡝ࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡪࡳࠦ࠽ࠡࠪࠬࠤࡂࡄࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡡࡥࡦࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡖࡄࡔࡤ࡙ࡔࡂࡔࡗࡉࡉ࠭ࠬࠡࡨࡱ࠶࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡩࠥࡃࠠ࡯ࡧࡺࠤࡈࡻࡳࡵࡱࡰࡉࡻ࡫࡮ࡵࠪࠪࡅ࠶࠷࡙ࡠࡈࡒࡖࡈࡋ࡟ࡔࡖࡄࡖ࡙࠭ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡤࡪࡵࡳࡥࡹࡩࡨࡆࡸࡨࡲࡹ࠮ࡥࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡬࡮࠳ࠢࡀࠤ࠭࠯ࠠ࠾ࡀࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡵࡩࡲࡵࡶࡦࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣࡘ࡚ࡁࡓࡖࡈࡈࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡩࡲ࠭࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ຅"))
          logger.info(bstack111ll11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠣຆ"))
        else:
          driver.execute_script(bstack111ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡪࠦ࠽ࠡࡰࡨࡻࠥࡉࡵࡴࡶࡲࡱࡊࡼࡥ࡯ࡶࠫࠫࡆ࠷࠱࡚ࡡࡉࡓࡗࡉࡅࡠࡕࡗࡓࡕ࠭ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡉࡻ࡫࡮ࡵࠪࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧງ"))
      return bstack11llll1111_opy_
  except Exception as e:
    logger.error(bstack111ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨຈ") + str(e))
    return False
def bstack1l1l1l1lll_opy_(driver, class_name, name, module_name, path, bstack111lll11_opy_):
  try:
    bstack11lll1ll11_opy_ = [class_name] if not class_name is None else []
    bstack11lll11111_opy_ = {
        bstack111ll11_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤຉ"): True,
        bstack111ll11_opy_ (u"ࠧࡺࡥࡴࡶࡇࡩࡹࡧࡩ࡭ࡵࠥຊ"): {
            bstack111ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ຋"): name,
            bstack111ll11_opy_ (u"ࠢࡵࡧࡶࡸࡗࡻ࡮ࡊࡦࠥຌ"): os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡗࡉࡘ࡚࡟ࡓࡗࡑࡣࡎࡊࠧຍ")),
            bstack111ll11_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡐࡢࡶ࡫ࠦຎ"): str(path),
            bstack111ll11_opy_ (u"ࠥࡷࡨࡵࡰࡦࡎ࡬ࡷࡹࠨຏ"): [module_name, *bstack11lll1ll11_opy_, name],
        },
        bstack111ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨຐ"): _11ll1lllll_opy_(driver, bstack111lll11_opy_)
    }
    driver.execute_script(bstack111ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡁࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳ࡜ࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡩࡴ࠰ࡵࡩࡸࠦ࠽ࠡࡰࡸࡰࡱࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡩࠤ࠭ࡧࡲࡨࡷࡰࡩࡳࡺࡳ࡜࠲ࡠ࠲ࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡥࡩࡪࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤ࡚ࡁࡑࡡࡗࡖࡆࡔࡓࡑࡑࡕࡘࡊࡘࠧ࠭ࠢࠫࡩࡻ࡫࡮ࡵࠫࠣࡁࡃࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡸࡦࡶࡔࡳࡣࡱࡷࡵࡵࡲࡵࡧࡵࡈࡦࡺࡡࠡ࠿ࠣࡩࡻ࡫࡮ࡵ࠰ࡧࡩࡹࡧࡩ࡭࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡪࡵ࠱ࡶࡪࡹࠠ࠾ࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡷࡥࡵ࡚ࡲࡢࡰࡶࡴࡴࡸࡴࡦࡴࡇࡥࡹࡧ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠭ࡺࡨࡪࡵ࠱ࡶࡪࡹࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡦࠢࡀࠤࡳ࡫ࡷࠡࡅࡸࡷࡹࡵ࡭ࡆࡸࡨࡲࡹ࠮ࠧࡂ࠳࠴࡝ࡤ࡚ࡅࡔࡖࡢࡉࡓࡊࠧ࠭ࠢࡾࠤࡩ࡫ࡴࡢ࡫࡯࠾ࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳ࡜࠲ࡠࠤࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡉࡻ࡫࡮ࡵࠪࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࠬࠦࡧࡲࡨࡷࡰࡩࡳࡺࡳ࡜࠲ࡠ࠲ࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠭࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠤࠥࠦຑ"), bstack11lll11111_opy_)
    logger.info(bstack111ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤຒ"))
  except Exception as bstack11ll1lll1l_opy_:
    logger.error(bstack111ll11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤຓ") + str(path) + bstack111ll11_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥດ") + str(bstack11ll1lll1l_opy_))