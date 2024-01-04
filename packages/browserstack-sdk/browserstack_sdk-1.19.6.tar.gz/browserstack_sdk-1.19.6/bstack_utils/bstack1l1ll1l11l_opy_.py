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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l1l111ll_opy_, bstack1l1llll1l1_opy_, bstack11l1l1ll1_opy_, bstack1lllll11l1_opy_, \
    bstack11l1l1lll1_opy_
def bstack111llll1_opy_(bstack11111ll111_opy_):
    for driver in bstack11111ll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1111l1_opy_(driver, status, reason=bstack1lll11l_opy_ (u"ࠨࠩᏩ")):
    bstack1l1l1ll1ll_opy_ = Config.get_instance()
    if bstack1l1l1ll1ll_opy_.bstack1l11111111_opy_():
        return
    bstack1lll11lll_opy_ = bstack1l1l1l11ll_opy_(bstack1lll11l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᏪ"), bstack1lll11l_opy_ (u"ࠪࠫᏫ"), status, reason, bstack1lll11l_opy_ (u"ࠫࠬᏬ"), bstack1lll11l_opy_ (u"ࠬ࠭Ꮽ"))
    driver.execute_script(bstack1lll11lll_opy_)
def bstack1llllll1ll_opy_(page, status, reason=bstack1lll11l_opy_ (u"࠭ࠧᏮ")):
    try:
        if page is None:
            return
        bstack1l1l1ll1ll_opy_ = Config.get_instance()
        if bstack1l1l1ll1ll_opy_.bstack1l11111111_opy_():
            return
        bstack1lll11lll_opy_ = bstack1l1l1l11ll_opy_(bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᏯ"), bstack1lll11l_opy_ (u"ࠨࠩᏰ"), status, reason, bstack1lll11l_opy_ (u"ࠩࠪᏱ"), bstack1lll11l_opy_ (u"ࠪࠫᏲ"))
        page.evaluate(bstack1lll11l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᏳ"), bstack1lll11lll_opy_)
    except Exception as e:
        print(bstack1lll11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥᏴ"), e)
def bstack1l1l1l11ll_opy_(type, name, status, reason, bstack1l1l11ll1l_opy_, bstack1l1l111l1_opy_):
    bstack1l111ll1_opy_ = {
        bstack1lll11l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭Ᏽ"): type,
        bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ᏶"): {}
    }
    if type == bstack1lll11l_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ᏷"):
        bstack1l111ll1_opy_[bstack1lll11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᏸ")][bstack1lll11l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᏹ")] = bstack1l1l11ll1l_opy_
        bstack1l111ll1_opy_[bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᏺ")][bstack1lll11l_opy_ (u"ࠬࡪࡡࡵࡣࠪᏻ")] = json.dumps(str(bstack1l1l111l1_opy_))
    if type == bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᏼ"):
        bstack1l111ll1_opy_[bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᏽ")][bstack1lll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭᏾")] = name
    if type == bstack1lll11l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ᏿"):
        bstack1l111ll1_opy_[bstack1lll11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᐀")][bstack1lll11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᐁ")] = status
        if status == bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᐂ") and str(reason) != bstack1lll11l_opy_ (u"ࠨࠢᐃ"):
            bstack1l111ll1_opy_[bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᐄ")][bstack1lll11l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᐅ")] = json.dumps(str(reason))
    bstack1llll1l1l1_opy_ = bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧᐆ").format(json.dumps(bstack1l111ll1_opy_))
    return bstack1llll1l1l1_opy_
def bstack11llll11_opy_(url, config, logger, bstack1l1llll11_opy_=False):
    hostname = bstack1l1llll1l1_opy_(url)
    is_private = bstack1lllll11l1_opy_(hostname)
    try:
        if is_private or bstack1l1llll11_opy_:
            file_path = bstack11l1l111ll_opy_(bstack1lll11l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᐇ"), bstack1lll11l_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᐈ"), logger)
            if os.environ.get(bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᐉ")) and eval(
                    os.environ.get(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᐊ"))):
                return
            if (bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᐋ") in config and not config[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᐌ")]):
                os.environ[bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᐍ")] = str(True)
                bstack11111ll1l1_opy_ = {bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬᐎ"): hostname}
                bstack11l1l1lll1_opy_(bstack1lll11l_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᐏ"), bstack1lll11l_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪᐐ"), bstack11111ll1l1_opy_, logger)
    except Exception as e:
        pass
def bstack1ll11l11l1_opy_(caps, bstack11111ll1ll_opy_):
    if bstack1lll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᐑ") in caps:
        caps[bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᐒ")][bstack1lll11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧᐓ")] = True
        if bstack11111ll1ll_opy_:
            caps[bstack1lll11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᐔ")][bstack1lll11l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᐕ")] = bstack11111ll1ll_opy_
    else:
        caps[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᐖ")] = True
        if bstack11111ll1ll_opy_:
            caps[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᐗ")] = bstack11111ll1ll_opy_
def bstack1111lll11l_opy_(bstack1l1l1111ll_opy_):
    bstack11111ll11l_opy_ = bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᐘ"), bstack1lll11l_opy_ (u"ࠧࠨᐙ"))
    if bstack11111ll11l_opy_ == bstack1lll11l_opy_ (u"ࠨࠩᐚ") or bstack11111ll11l_opy_ == bstack1lll11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᐛ"):
        threading.current_thread().testStatus = bstack1l1l1111ll_opy_
    else:
        if bstack1l1l1111ll_opy_ == bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᐜ"):
            threading.current_thread().testStatus = bstack1l1l1111ll_opy_