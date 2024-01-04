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
import re
from bstack_utils.bstack1lll111ll_opy_ import bstack1111ll1l1l_opy_
def bstack1111lll111_opy_(fixture_name):
    if fixture_name.startswith(bstack111ll11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᎵ")):
        return bstack111ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᎶ")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᎷ")):
        return bstack111ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᎸ")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᎹ")):
        return bstack111ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᎺ")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᎻ")):
        return bstack111ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᎼ")
def bstack1111l1llll_opy_(fixture_name):
    return bool(re.match(bstack111ll11_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᎽ"), fixture_name))
def bstack1111l1lll1_opy_(fixture_name):
    return bool(re.match(bstack111ll11_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᎾ"), fixture_name))
def bstack1111ll1111_opy_(fixture_name):
    return bool(re.match(bstack111ll11_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᎿ"), fixture_name))
def bstack1111ll1l11_opy_(fixture_name):
    if fixture_name.startswith(bstack111ll11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᏀ")):
        return bstack111ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᏁ"), bstack111ll11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᏂ")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᏃ")):
        return bstack111ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᏄ"), bstack111ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᏅ")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꮖ")):
        return bstack111ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ꮗ"), bstack111ll11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᏈ")
    elif fixture_name.startswith(bstack111ll11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᏉ")):
        return bstack111ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᏊ"), bstack111ll11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᏋ")
    return None, None
def bstack1111ll1ll1_opy_(hook_name):
    if hook_name in [bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭Ꮜ"), bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᏍ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111ll11l1_opy_(hook_name):
    if hook_name in [bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᏎ"), bstack111ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᏏ")]:
        return bstack111ll11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᏐ")
    elif hook_name in [bstack111ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᏑ"), bstack111ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᏒ")]:
        return bstack111ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᏓ")
    elif hook_name in [bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᏔ"), bstack111ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᏕ")]:
        return bstack111ll11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᏖ")
    elif hook_name in [bstack111ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭Ꮧ"), bstack111ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭Ꮨ")]:
        return bstack111ll11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᏙ")
    return hook_name
def bstack1111ll111l_opy_(node, scenario):
    if hasattr(node, bstack111ll11_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᏚ")):
        parts = node.nodeid.rsplit(bstack111ll11_opy_ (u"ࠣ࡝ࠥᏛ"))
        params = parts[-1]
        return bstack111ll11_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᏜ").format(scenario.name, params)
    return scenario.name
def bstack1111ll11ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᏝ")):
            examples = list(node.callspec.params[bstack111ll11_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᏞ")].values())
        return examples
    except:
        return []
def bstack1111l1ll1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1111l1l1ll_opy_(report):
    try:
        status = bstack111ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᏟ")
        if report.passed or (report.failed and hasattr(report, bstack111ll11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᏠ"))):
            status = bstack111ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᏡ")
        elif report.skipped:
            status = bstack111ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᏢ")
        bstack1111ll1l1l_opy_(status)
    except:
        pass
def bstack11ll1l11l_opy_(status):
    try:
        bstack1111ll1lll_opy_ = bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᏣ")
        if status == bstack111ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᏤ"):
            bstack1111ll1lll_opy_ = bstack111ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᏥ")
        elif status == bstack111ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭Ꮶ"):
            bstack1111ll1lll_opy_ = bstack111ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᏧ")
        bstack1111ll1l1l_opy_(bstack1111ll1lll_opy_)
    except:
        pass
def bstack1111l1ll11_opy_(item=None, report=None, summary=None, extra=None):
    return