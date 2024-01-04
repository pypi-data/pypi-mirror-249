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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l11ll1ll_opy_, bstack1lllll11l_opy_, bstack1ll1ll1ll_opy_, bstack1lllllllll_opy_, \
    bstack11ll111l11_opy_
def bstack1ll1l111ll_opy_(bstack11111ll1l1_opy_):
    for driver in bstack11111ll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11llll11_opy_(driver, status, reason=bstack111ll11_opy_ (u"ࠩࠪᏪ")):
    bstack11ll1l1l_opy_ = Config.get_instance()
    if bstack11ll1l1l_opy_.bstack11lllll11l_opy_():
        return
    bstack1llll1l1l_opy_ = bstack11l1ll1ll_opy_(bstack111ll11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ꮻ"), bstack111ll11_opy_ (u"ࠫࠬᏬ"), status, reason, bstack111ll11_opy_ (u"ࠬ࠭Ꮽ"), bstack111ll11_opy_ (u"࠭ࠧᏮ"))
    driver.execute_script(bstack1llll1l1l_opy_)
def bstack111llll1l_opy_(page, status, reason=bstack111ll11_opy_ (u"ࠧࠨᏯ")):
    try:
        if page is None:
            return
        bstack11ll1l1l_opy_ = Config.get_instance()
        if bstack11ll1l1l_opy_.bstack11lllll11l_opy_():
            return
        bstack1llll1l1l_opy_ = bstack11l1ll1ll_opy_(bstack111ll11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᏰ"), bstack111ll11_opy_ (u"ࠩࠪᏱ"), status, reason, bstack111ll11_opy_ (u"ࠪࠫᏲ"), bstack111ll11_opy_ (u"ࠫࠬᏳ"))
        page.evaluate(bstack111ll11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᏴ"), bstack1llll1l1l_opy_)
    except Exception as e:
        print(bstack111ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᏵ"), e)
def bstack11l1ll1ll_opy_(type, name, status, reason, bstack111111lll_opy_, bstack1ll1l11lll_opy_):
    bstack1l111l1l1_opy_ = {
        bstack111ll11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ᏶"): type,
        bstack111ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᏷"): {}
    }
    if type == bstack111ll11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᏸ"):
        bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᏹ")][bstack111ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᏺ")] = bstack111111lll_opy_
        bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᏻ")][bstack111ll11_opy_ (u"࠭ࡤࡢࡶࡤࠫᏼ")] = json.dumps(str(bstack1ll1l11lll_opy_))
    if type == bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᏽ"):
        bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᏾")][bstack111ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᏿")] = name
    if type == bstack111ll11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭᐀"):
        bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᐁ")][bstack111ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᐂ")] = status
        if status == bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᐃ") and str(reason) != bstack111ll11_opy_ (u"ࠢࠣᐄ"):
            bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᐅ")][bstack111ll11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᐆ")] = json.dumps(str(reason))
    bstack1111lll1l_opy_ = bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᐇ").format(json.dumps(bstack1l111l1l1_opy_))
    return bstack1111lll1l_opy_
def bstack1l1ll1lll1_opy_(url, config, logger, bstack111ll11ll_opy_=False):
    hostname = bstack1lllll11l_opy_(url)
    is_private = bstack1lllllllll_opy_(hostname)
    try:
        if is_private or bstack111ll11ll_opy_:
            file_path = bstack11l11ll1ll_opy_(bstack111ll11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᐈ"), bstack111ll11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᐉ"), logger)
            if os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᐊ")) and eval(
                    os.environ.get(bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᐋ"))):
                return
            if (bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᐌ") in config and not config[bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᐍ")]):
                os.environ[bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᐎ")] = str(True)
                bstack11111ll11l_opy_ = {bstack111ll11_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᐏ"): hostname}
                bstack11ll111l11_opy_(bstack111ll11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᐐ"), bstack111ll11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᐑ"), bstack11111ll11l_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1l11l1_opy_(caps, bstack11111ll111_opy_):
    if bstack111ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᐒ") in caps:
        caps[bstack111ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᐓ")][bstack111ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᐔ")] = True
        if bstack11111ll111_opy_:
            caps[bstack111ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᐕ")][bstack111ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᐖ")] = bstack11111ll111_opy_
    else:
        caps[bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᐗ")] = True
        if bstack11111ll111_opy_:
            caps[bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᐘ")] = bstack11111ll111_opy_
def bstack1111ll1l1l_opy_(bstack1l11l11ll1_opy_):
    bstack11111l1lll_opy_ = bstack1ll1ll1ll_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᐙ"), bstack111ll11_opy_ (u"ࠨࠩᐚ"))
    if bstack11111l1lll_opy_ == bstack111ll11_opy_ (u"ࠩࠪᐛ") or bstack11111l1lll_opy_ == bstack111ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᐜ"):
        threading.current_thread().testStatus = bstack1l11l11ll1_opy_
    else:
        if bstack1l11l11ll1_opy_ == bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐝ"):
            threading.current_thread().testStatus = bstack1l11l11ll1_opy_