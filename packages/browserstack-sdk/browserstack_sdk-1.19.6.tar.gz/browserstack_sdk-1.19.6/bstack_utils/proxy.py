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
import os
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l1111l1l_opy_
def bstack1111lll1ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111lll1l1_opy_(bstack1111llll11_opy_, bstack1111llllll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111llll11_opy_):
        with open(bstack1111llll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111lll1ll_opy_(bstack1111llll11_opy_):
        pac = get_pac(url=bstack1111llll11_opy_)
    else:
        raise Exception(bstack1lll11l_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩᎏ").format(bstack1111llll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1lll11l_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦ᎐"), 80))
        bstack111l111111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l111111_opy_ = bstack1lll11l_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬ᎑")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111llllll_opy_, bstack111l111111_opy_)
    return proxy_url
def bstack1ll111llll_opy_(config):
    return bstack1lll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ᎒") in config or bstack1lll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ᎓") in config
def bstack1ll1ll1l11_opy_(config):
    if not bstack1ll111llll_opy_(config):
        return
    if config.get(bstack1lll11l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ᎔")):
        return config.get(bstack1lll11l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ᎕"))
    if config.get(bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭᎖")):
        return config.get(bstack1lll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᎗"))
def bstack1111l1l11_opy_(config, bstack1111llllll_opy_):
    proxy = bstack1ll1ll1l11_opy_(config)
    proxies = {}
    if config.get(bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ᎘")) or config.get(bstack1lll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ᎙")):
        if proxy.endswith(bstack1lll11l_opy_ (u"࠭࠮ࡱࡣࡦࠫ᎚")):
            proxies = bstack1l1l11ll11_opy_(proxy, bstack1111llllll_opy_)
        else:
            proxies = {
                bstack1lll11l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭᎛"): proxy
            }
    return proxies
def bstack1l1l11ll11_opy_(bstack1111llll11_opy_, bstack1111llllll_opy_):
    proxies = {}
    global bstack1111lllll1_opy_
    if bstack1lll11l_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫ᎜") in globals():
        return bstack1111lllll1_opy_
    try:
        proxy = bstack1111lll1l1_opy_(bstack1111llll11_opy_, bstack1111llllll_opy_)
        if bstack1lll11l_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤ᎝") in proxy:
            proxies = {}
        elif bstack1lll11l_opy_ (u"ࠥࡌ࡙࡚ࡐࠣ᎞") in proxy or bstack1lll11l_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥ᎟") in proxy or bstack1lll11l_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦᎠ") in proxy:
            bstack1111llll1l_opy_ = proxy.split(bstack1lll11l_opy_ (u"ࠨࠠࠣᎡ"))
            if bstack1lll11l_opy_ (u"ࠢ࠻࠱࠲ࠦᎢ") in bstack1lll11l_opy_ (u"ࠣࠤᎣ").join(bstack1111llll1l_opy_[1:]):
                proxies = {
                    bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᎤ"): bstack1lll11l_opy_ (u"ࠥࠦᎥ").join(bstack1111llll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᎦ"): str(bstack1111llll1l_opy_[0]).lower() + bstack1lll11l_opy_ (u"ࠧࡀ࠯࠰ࠤᎧ") + bstack1lll11l_opy_ (u"ࠨࠢᎨ").join(bstack1111llll1l_opy_[1:])
                }
        elif bstack1lll11l_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨᎩ") in proxy:
            bstack1111llll1l_opy_ = proxy.split(bstack1lll11l_opy_ (u"ࠣࠢࠥᎪ"))
            if bstack1lll11l_opy_ (u"ࠤ࠽࠳࠴ࠨᎫ") in bstack1lll11l_opy_ (u"ࠥࠦᎬ").join(bstack1111llll1l_opy_[1:]):
                proxies = {
                    bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᎭ"): bstack1lll11l_opy_ (u"ࠧࠨᎮ").join(bstack1111llll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᎯ"): bstack1lll11l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᎰ") + bstack1lll11l_opy_ (u"ࠣࠤᎱ").join(bstack1111llll1l_opy_[1:])
                }
        else:
            proxies = {
                bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᎲ"): proxy
            }
    except Exception as e:
        print(bstack1lll11l_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᎳ"), bstack11l1111l1l_opy_.format(bstack1111llll11_opy_, str(e)))
    bstack1111lllll1_opy_ = proxies
    return proxies