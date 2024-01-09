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
import re
from bstack_utils.bstack1ll11ll11l_opy_ import bstack1111ll11ll_opy_
def bstack1111ll1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11lllll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᎶ")):
        return bstack11lllll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᎷ")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᎸ")):
        return bstack11lllll_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᎹ")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᎺ")):
        return bstack11lllll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᎻ")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᎼ")):
        return bstack11lllll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨᎽ")
def bstack1111ll11l1_opy_(fixture_name):
    return bool(re.match(bstack11lllll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᎾ"), fixture_name))
def bstack1111l1llll_opy_(fixture_name):
    return bool(re.match(bstack11lllll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᎿ"), fixture_name))
def bstack1111ll111l_opy_(fixture_name):
    return bool(re.match(bstack11lllll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᏀ"), fixture_name))
def bstack1111ll1111_opy_(fixture_name):
    if fixture_name.startswith(bstack11lllll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᏁ")):
        return bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᏂ"), bstack11lllll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᏃ")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꮔ")):
        return bstack11lllll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭Ꮕ"), bstack11lllll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᏆ")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᏇ")):
        return bstack11lllll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᏈ"), bstack11lllll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᏉ")
    elif fixture_name.startswith(bstack11lllll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᏊ")):
        return bstack11lllll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨᏋ"), bstack11lllll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᏌ")
    return None, None
def bstack1111ll1lll_opy_(hook_name):
    if hook_name in [bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᏍ"), bstack11lllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᏎ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111ll1l11_opy_(hook_name):
    if hook_name in [bstack11lllll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᏏ"), bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᏐ")]:
        return bstack11lllll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᏑ")
    elif hook_name in [bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᏒ"), bstack11lllll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᏓ")]:
        return bstack11lllll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᏔ")
    elif hook_name in [bstack11lllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ꮥ"), bstack11lllll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᏖ")]:
        return bstack11lllll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᏗ")
    elif hook_name in [bstack11lllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᏘ"), bstack11lllll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᏙ")]:
        return bstack11lllll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᏚ")
    return hook_name
def bstack1111l1lll1_opy_(node, scenario):
    if hasattr(node, bstack11lllll_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᏛ")):
        parts = node.nodeid.rsplit(bstack11lllll_opy_ (u"ࠤ࡞ࠦᏜ"))
        params = parts[-1]
        return bstack11lllll_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᏝ").format(scenario.name, params)
    return scenario.name
def bstack1111l1l1ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11lllll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭Ꮮ")):
            examples = list(node.callspec.params[bstack11lllll_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᏟ")].values())
        return examples
    except:
        return []
def bstack1111l1ll1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1111l1ll11_opy_(report):
    try:
        status = bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ꮰ")
        if report.passed or (report.failed and hasattr(report, bstack11lllll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᏡ"))):
            status = bstack11lllll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᏢ")
        elif report.skipped:
            status = bstack11lllll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᏣ")
        bstack1111ll11ll_opy_(status)
    except:
        pass
def bstack1ll1111l1_opy_(status):
    try:
        bstack1111ll1l1l_opy_ = bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᏤ")
        if status == bstack11lllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᏥ"):
            bstack1111ll1l1l_opy_ = bstack11lllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᏦ")
        elif status == bstack11lllll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᏧ"):
            bstack1111ll1l1l_opy_ = bstack11lllll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᏨ")
        bstack1111ll11ll_opy_(bstack1111ll1l1l_opy_)
    except:
        pass
def bstack1111lll111_opy_(item=None, report=None, summary=None, extra=None):
    return