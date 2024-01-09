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
import os
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l111l11l_opy_
def bstack1111lll1l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111llll11_opy_(bstack1111lll1ll_opy_, bstack1111lllll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111lll1ll_opy_):
        with open(bstack1111lll1ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111lll1l1_opy_(bstack1111lll1ll_opy_):
        pac = get_pac(url=bstack1111lll1ll_opy_)
    else:
        raise Exception(bstack11lllll_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫ᎑").format(bstack1111lll1ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11lllll_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨ᎒"), 80))
        bstack1111llll1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1111llll1l_opy_ = bstack11lllll_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧ᎓")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111lllll1_opy_, bstack1111llll1l_opy_)
    return proxy_url
def bstack1lll1l111_opy_(config):
    return bstack11lllll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ᎔") in config or bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ᎕") in config
def bstack1l1ll11l1l_opy_(config):
    if not bstack1lll1l111_opy_(config):
        return
    if config.get(bstack11lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᎖")):
        return config.get(bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭᎗"))
    if config.get(bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ᎘")):
        return config.get(bstack11lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ᎙"))
def bstack11lllllll_opy_(config, bstack1111lllll1_opy_):
    proxy = bstack1l1ll11l1l_opy_(config)
    proxies = {}
    if config.get(bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᎚")) or config.get(bstack11lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᎛")):
        if proxy.endswith(bstack11lllll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭᎜")):
            proxies = bstack1ll111111_opy_(proxy, bstack1111lllll1_opy_)
        else:
            proxies = {
                bstack11lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ᎝"): proxy
            }
    return proxies
def bstack1ll111111_opy_(bstack1111lll1ll_opy_, bstack1111lllll1_opy_):
    proxies = {}
    global bstack1111llllll_opy_
    if bstack11lllll_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭᎞") in globals():
        return bstack1111llllll_opy_
    try:
        proxy = bstack1111llll11_opy_(bstack1111lll1ll_opy_, bstack1111lllll1_opy_)
        if bstack11lllll_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦ᎟") in proxy:
            proxies = {}
        elif bstack11lllll_opy_ (u"ࠧࡎࡔࡕࡒࠥᎠ") in proxy or bstack11lllll_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧᎡ") in proxy or bstack11lllll_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨᎢ") in proxy:
            bstack1111lll11l_opy_ = proxy.split(bstack11lllll_opy_ (u"ࠣࠢࠥᎣ"))
            if bstack11lllll_opy_ (u"ࠤ࠽࠳࠴ࠨᎤ") in bstack11lllll_opy_ (u"ࠥࠦᎥ").join(bstack1111lll11l_opy_[1:]):
                proxies = {
                    bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᎦ"): bstack11lllll_opy_ (u"ࠧࠨᎧ").join(bstack1111lll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᎨ"): str(bstack1111lll11l_opy_[0]).lower() + bstack11lllll_opy_ (u"ࠢ࠻࠱࠲ࠦᎩ") + bstack11lllll_opy_ (u"ࠣࠤᎪ").join(bstack1111lll11l_opy_[1:])
                }
        elif bstack11lllll_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣᎫ") in proxy:
            bstack1111lll11l_opy_ = proxy.split(bstack11lllll_opy_ (u"ࠥࠤࠧᎬ"))
            if bstack11lllll_opy_ (u"ࠦ࠿࠵࠯ࠣᎭ") in bstack11lllll_opy_ (u"ࠧࠨᎮ").join(bstack1111lll11l_opy_[1:]):
                proxies = {
                    bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᎯ"): bstack11lllll_opy_ (u"ࠢࠣᎰ").join(bstack1111lll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᎱ"): bstack11lllll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᎲ") + bstack11lllll_opy_ (u"ࠥࠦᎳ").join(bstack1111lll11l_opy_[1:])
                }
        else:
            proxies = {
                bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᎴ"): proxy
            }
    except Exception as e:
        print(bstack11lllll_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤᎵ"), bstack11l111l11l_opy_.format(bstack1111lll1ll_opy_, str(e)))
    bstack1111llllll_opy_ = proxies
    return proxies