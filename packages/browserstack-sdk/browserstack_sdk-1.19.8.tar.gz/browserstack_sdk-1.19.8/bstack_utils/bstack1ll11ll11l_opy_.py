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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11ll11l1ll_opy_, bstack1l1lll1l11_opy_, bstack1lllll1l11_opy_, bstack1l1llll11l_opy_, \
    bstack11l11lll11_opy_
def bstack11ll11l11_opy_(bstack11111ll1l1_opy_):
    for driver in bstack11111ll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1l11l1_opy_(driver, status, reason=bstack11lllll_opy_ (u"ࠪࠫᏫ")):
    bstack1lll11111_opy_ = Config.get_instance()
    if bstack1lll11111_opy_.bstack11llllll1l_opy_():
        return
    bstack1ll11llll1_opy_ = bstack11lll111_opy_(bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᏬ"), bstack11lllll_opy_ (u"ࠬ࠭Ꮽ"), status, reason, bstack11lllll_opy_ (u"࠭ࠧᏮ"), bstack11lllll_opy_ (u"ࠧࠨᏯ"))
    driver.execute_script(bstack1ll11llll1_opy_)
def bstack1lll11l1l_opy_(page, status, reason=bstack11lllll_opy_ (u"ࠨࠩᏰ")):
    try:
        if page is None:
            return
        bstack1lll11111_opy_ = Config.get_instance()
        if bstack1lll11111_opy_.bstack11llllll1l_opy_():
            return
        bstack1ll11llll1_opy_ = bstack11lll111_opy_(bstack11lllll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᏱ"), bstack11lllll_opy_ (u"ࠪࠫᏲ"), status, reason, bstack11lllll_opy_ (u"ࠫࠬᏳ"), bstack11lllll_opy_ (u"ࠬ࠭Ᏼ"))
        page.evaluate(bstack11lllll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᏵ"), bstack1ll11llll1_opy_)
    except Exception as e:
        print(bstack11lllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧ᏶"), e)
def bstack11lll111_opy_(type, name, status, reason, bstack1l111l1l1_opy_, bstack11llll1ll_opy_):
    bstack11111l11l_opy_ = {
        bstack11lllll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ᏷"): type,
        bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᏸ"): {}
    }
    if type == bstack11lllll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬᏹ"):
        bstack11111l11l_opy_[bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᏺ")][bstack11lllll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᏻ")] = bstack1l111l1l1_opy_
        bstack11111l11l_opy_[bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᏼ")][bstack11lllll_opy_ (u"ࠧࡥࡣࡷࡥࠬᏽ")] = json.dumps(str(bstack11llll1ll_opy_))
    if type == bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ᏾"):
        bstack11111l11l_opy_[bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᏿")][bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᐀")] = name
    if type == bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᐁ"):
        bstack11111l11l_opy_[bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᐂ")][bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᐃ")] = status
        if status == bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᐄ") and str(reason) != bstack11lllll_opy_ (u"ࠣࠤᐅ"):
            bstack11111l11l_opy_[bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᐆ")][bstack11lllll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᐇ")] = json.dumps(str(reason))
    bstack1l1ll1l111_opy_ = bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᐈ").format(json.dumps(bstack11111l11l_opy_))
    return bstack1l1ll1l111_opy_
def bstack1llll1l1l1_opy_(url, config, logger, bstack1ll1l11l1l_opy_=False):
    hostname = bstack1l1lll1l11_opy_(url)
    is_private = bstack1l1llll11l_opy_(hostname)
    try:
        if is_private or bstack1ll1l11l1l_opy_:
            file_path = bstack11ll11l1ll_opy_(bstack11lllll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᐉ"), bstack11lllll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᐊ"), logger)
            if os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᐋ")) and eval(
                    os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᐌ"))):
                return
            if (bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᐍ") in config and not config[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᐎ")]):
                os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᐏ")] = str(True)
                bstack11111ll11l_opy_ = {bstack11lllll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧᐐ"): hostname}
                bstack11l11lll11_opy_(bstack11lllll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᐑ"), bstack11lllll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬᐒ"), bstack11111ll11l_opy_, logger)
    except Exception as e:
        pass
def bstack11l1ll1ll_opy_(caps, bstack11111l1lll_opy_):
    if bstack11lllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᐓ") in caps:
        caps[bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᐔ")][bstack11lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᐕ")] = True
        if bstack11111l1lll_opy_:
            caps[bstack11lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᐖ")][bstack11lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᐗ")] = bstack11111l1lll_opy_
    else:
        caps[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫᐘ")] = True
        if bstack11111l1lll_opy_:
            caps[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᐙ")] = bstack11111l1lll_opy_
def bstack1111ll11ll_opy_(bstack1l111l1l1l_opy_):
    bstack11111ll111_opy_ = bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬᐚ"), bstack11lllll_opy_ (u"ࠩࠪᐛ"))
    if bstack11111ll111_opy_ == bstack11lllll_opy_ (u"ࠪࠫᐜ") or bstack11111ll111_opy_ == bstack11lllll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᐝ"):
        threading.current_thread().testStatus = bstack1l111l1l1l_opy_
    else:
        if bstack1l111l1l1l_opy_ == bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᐞ"):
            threading.current_thread().testStatus = bstack1l111l1l1l_opy_