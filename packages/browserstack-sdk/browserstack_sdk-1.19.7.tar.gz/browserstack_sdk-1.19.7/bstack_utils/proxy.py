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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l1111l1l_opy_
def bstack1111llll11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111llll1l_opy_(bstack1111lll11l_opy_, bstack1111lllll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111lll11l_opy_):
        with open(bstack1111lll11l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111llll11_opy_(bstack1111lll11l_opy_):
        pac = get_pac(url=bstack1111lll11l_opy_)
    else:
        raise Exception(bstack111ll11_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪ᎐").format(bstack1111lll11l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111ll11_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧ᎑"), 80))
        bstack1111lll1ll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1111lll1ll_opy_ = bstack111ll11_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭᎒")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111lllll1_opy_, bstack1111lll1ll_opy_)
    return proxy_url
def bstack111lllll_opy_(config):
    return bstack111ll11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᎓") in config or bstack111ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᎔") in config
def bstack11111ll1l_opy_(config):
    if not bstack111lllll_opy_(config):
        return
    if config.get(bstack111ll11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ᎕")):
        return config.get(bstack111ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᎖"))
    if config.get(bstack111ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᎗")):
        return config.get(bstack111ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ᎘"))
def bstack1l1llll1l1_opy_(config, bstack1111lllll1_opy_):
    proxy = bstack11111ll1l_opy_(config)
    proxies = {}
    if config.get(bstack111ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ᎙")) or config.get(bstack111ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ᎚")):
        if proxy.endswith(bstack111ll11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ᎛")):
            proxies = bstack1ll1l1l1l1_opy_(proxy, bstack1111lllll1_opy_)
        else:
            proxies = {
                bstack111ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ᎜"): proxy
            }
    return proxies
def bstack1ll1l1l1l1_opy_(bstack1111lll11l_opy_, bstack1111lllll1_opy_):
    proxies = {}
    global bstack1111lll1l1_opy_
    if bstack111ll11_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬ᎝") in globals():
        return bstack1111lll1l1_opy_
    try:
        proxy = bstack1111llll1l_opy_(bstack1111lll11l_opy_, bstack1111lllll1_opy_)
        if bstack111ll11_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥ᎞") in proxy:
            proxies = {}
        elif bstack111ll11_opy_ (u"ࠦࡍ࡚ࡔࡑࠤ᎟") in proxy or bstack111ll11_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᎠ") in proxy or bstack111ll11_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᎡ") in proxy:
            bstack1111llllll_opy_ = proxy.split(bstack111ll11_opy_ (u"ࠢࠡࠤᎢ"))
            if bstack111ll11_opy_ (u"ࠣ࠼࠲࠳ࠧᎣ") in bstack111ll11_opy_ (u"ࠤࠥᎤ").join(bstack1111llllll_opy_[1:]):
                proxies = {
                    bstack111ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᎥ"): bstack111ll11_opy_ (u"ࠦࠧᎦ").join(bstack1111llllll_opy_[1:])
                }
            else:
                proxies = {
                    bstack111ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᎧ"): str(bstack1111llllll_opy_[0]).lower() + bstack111ll11_opy_ (u"ࠨ࠺࠰࠱ࠥᎨ") + bstack111ll11_opy_ (u"ࠢࠣᎩ").join(bstack1111llllll_opy_[1:])
                }
        elif bstack111ll11_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᎪ") in proxy:
            bstack1111llllll_opy_ = proxy.split(bstack111ll11_opy_ (u"ࠤࠣࠦᎫ"))
            if bstack111ll11_opy_ (u"ࠥ࠾࠴࠵ࠢᎬ") in bstack111ll11_opy_ (u"ࠦࠧᎭ").join(bstack1111llllll_opy_[1:]):
                proxies = {
                    bstack111ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᎮ"): bstack111ll11_opy_ (u"ࠨࠢᎯ").join(bstack1111llllll_opy_[1:])
                }
            else:
                proxies = {
                    bstack111ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ꮀ"): bstack111ll11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᎱ") + bstack111ll11_opy_ (u"ࠤࠥᎲ").join(bstack1111llllll_opy_[1:])
                }
        else:
            proxies = {
                bstack111ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᎳ"): proxy
            }
    except Exception as e:
        print(bstack111ll11_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᎴ"), bstack11l1111l1l_opy_.format(bstack1111lll11l_opy_, str(e)))
    bstack1111lll1l1_opy_ = proxies
    return proxies