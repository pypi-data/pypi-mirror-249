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
import re
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1111lll11l_opy_
def bstack1111lll111_opy_(fixture_name):
    if fixture_name.startswith(bstack1lll11l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꮄ")):
        return bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ꮅ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꮆ")):
        return bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭Ꮇ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꮈ")):
        return bstack1lll11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ꮉ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᎺ")):
        return bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭Ꮋ")
def bstack1111l1ll1l_opy_(fixture_name):
    return bool(re.match(bstack1lll11l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࢁࡳ࡯ࡥࡷ࡯ࡩ࠮ࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᎼ"), fixture_name))
def bstack1111ll11l1_opy_(fixture_name):
    return bool(re.match(bstack1lll11l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᎽ"), fixture_name))
def bstack1111l1ll11_opy_(fixture_name):
    return bool(re.match(bstack1lll11l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᎾ"), fixture_name))
def bstack1111ll1111_opy_(fixture_name):
    if fixture_name.startswith(bstack1lll11l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᎿ")):
        return bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᏀ"), bstack1lll11l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᏁ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᏂ")):
        return bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᏃ"), bstack1lll11l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᏄ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᏅ")):
        return bstack1lll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᏆ"), bstack1lll11l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭Ꮗ")
    elif fixture_name.startswith(bstack1lll11l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꮘ")):
        return bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭Ꮙ"), bstack1lll11l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨᏊ")
    return None, None
def bstack1111ll111l_opy_(hook_name):
    if hook_name in [bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᏋ"), bstack1lll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᏌ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111ll1lll_opy_(hook_name):
    if hook_name in [bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᏍ"), bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᏎ")]:
        return bstack1lll11l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᏏ")
    elif hook_name in [bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᏐ"), bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᏑ")]:
        return bstack1lll11l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᏒ")
    elif hook_name in [bstack1lll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᏓ"), bstack1lll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᏔ")]:
        return bstack1lll11l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭Ꮥ")
    elif hook_name in [bstack1lll11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᏖ"), bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᏗ")]:
        return bstack1lll11l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨᏘ")
    return hook_name
def bstack1111l1lll1_opy_(node, scenario):
    if hasattr(node, bstack1lll11l_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᏙ")):
        parts = node.nodeid.rsplit(bstack1lll11l_opy_ (u"ࠢ࡜ࠤᏚ"))
        params = parts[-1]
        return bstack1lll11l_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣᏛ").format(scenario.name, params)
    return scenario.name
def bstack1111ll1l1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1lll11l_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᏜ")):
            examples = list(node.callspec.params[bstack1lll11l_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᏝ")].values())
        return examples
    except:
        return []
def bstack1111ll11ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1111l1llll_opy_(report):
    try:
        status = bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᏞ")
        if report.passed or (report.failed and hasattr(report, bstack1lll11l_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᏟ"))):
            status = bstack1lll11l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ꮰ")
        elif report.skipped:
            status = bstack1lll11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᏡ")
        bstack1111lll11l_opy_(status)
    except:
        pass
def bstack11ll1l111_opy_(status):
    try:
        bstack1111ll1ll1_opy_ = bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᏢ")
        if status == bstack1lll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᏣ"):
            bstack1111ll1ll1_opy_ = bstack1lll11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᏤ")
        elif status == bstack1lll11l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᏥ"):
            bstack1111ll1ll1_opy_ = bstack1lll11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭Ꮶ")
        bstack1111lll11l_opy_(bstack1111ll1ll1_opy_)
    except:
        pass
def bstack1111ll1l11_opy_(item=None, report=None, summary=None, extra=None):
    return