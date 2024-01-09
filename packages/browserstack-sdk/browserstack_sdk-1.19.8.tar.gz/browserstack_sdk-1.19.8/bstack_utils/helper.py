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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11ll11llll_opy_, bstack1ll1111ll1_opy_, bstack11111llll_opy_, bstack1l1l11llll_opy_
from bstack_utils.messages import bstack111l1111l_opy_, bstack1ll11l1111_opy_
from bstack_utils.proxy import bstack11lllllll_opy_, bstack1l1ll11l1l_opy_
from browserstack_sdk.bstack1111lllll_opy_ import *
from browserstack_sdk.bstack1l111l11ll_opy_ import *
bstack1lll11111_opy_ = Config.get_instance()
def bstack11lll1llll_opy_(config):
    return config[bstack11lllll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᄧ")]
def bstack11ll1ll1ll_opy_(config):
    return config[bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᄨ")]
def bstack111lll11l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1l111l1_opy_(obj):
    values = []
    bstack11ll111ll1_opy_ = re.compile(bstack11lllll_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣᄩ"), re.I)
    for key in obj.keys():
        if bstack11ll111ll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11ll1111l1_opy_(config):
    tags = []
    tags.extend(bstack11l1l111l1_opy_(os.environ))
    tags.extend(bstack11l1l111l1_opy_(config))
    return tags
def bstack11l1llll1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l11lllll_opy_(bstack11ll111l11_opy_):
    if not bstack11ll111l11_opy_:
        return bstack11lllll_opy_ (u"ࠬ࠭ᄪ")
    return bstack11lllll_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢᄫ").format(bstack11ll111l11_opy_.name, bstack11ll111l11_opy_.email)
def bstack11lll111ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11ll1111ll_opy_ = repo.common_dir
        info = {
            bstack11lllll_opy_ (u"ࠢࡴࡪࡤࠦᄬ"): repo.head.commit.hexsha,
            bstack11lllll_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦᄭ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11lllll_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤᄮ"): repo.active_branch.name,
            bstack11lllll_opy_ (u"ࠥࡸࡦ࡭ࠢᄯ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11lllll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢᄰ"): bstack11l11lllll_opy_(repo.head.commit.committer),
            bstack11lllll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨᄱ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11lllll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨᄲ"): bstack11l11lllll_opy_(repo.head.commit.author),
            bstack11lllll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧᄳ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11lllll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᄴ"): repo.head.commit.message,
            bstack11lllll_opy_ (u"ࠤࡵࡳࡴࡺࠢᄵ"): repo.git.rev_parse(bstack11lllll_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧᄶ")),
            bstack11lllll_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧᄷ"): bstack11ll1111ll_opy_,
            bstack11lllll_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᄸ"): subprocess.check_output([bstack11lllll_opy_ (u"ࠨࡧࡪࡶࠥᄹ"), bstack11lllll_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥᄺ"), bstack11lllll_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦᄻ")]).strip().decode(
                bstack11lllll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᄼ")),
            bstack11lllll_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᄽ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11lllll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᄾ"): repo.git.rev_list(
                bstack11lllll_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧᄿ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1ll1ll1_opy_ = []
        for remote in remotes:
            bstack11l1l1lll1_opy_ = {
                bstack11lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᅀ"): remote.name,
                bstack11lllll_opy_ (u"ࠢࡶࡴ࡯ࠦᅁ"): remote.url,
            }
            bstack11l1ll1ll1_opy_.append(bstack11l1l1lll1_opy_)
        return {
            bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᅂ"): bstack11lllll_opy_ (u"ࠤࡪ࡭ࡹࠨᅃ"),
            **info,
            bstack11lllll_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦᅄ"): bstack11l1ll1ll1_opy_
        }
    except Exception as err:
        print(bstack11lllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᅅ").format(err))
        return {}
def bstack1llll1111l_opy_():
    env = os.environ
    if (bstack11lllll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᅆ") in env and len(env[bstack11lllll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦᅇ")]) > 0) or (
            bstack11lllll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᅈ") in env and len(env[bstack11lllll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢᅉ")]) > 0):
        return {
            bstack11lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅊ"): bstack11lllll_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦᅋ"),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅌ"): env.get(bstack11lllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᅍ")),
            bstack11lllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᅎ"): env.get(bstack11lllll_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤᅏ")),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᅐ"): env.get(bstack11lllll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᅑ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠥࡇࡎࠨᅒ")) == bstack11lllll_opy_ (u"ࠦࡹࡸࡵࡦࠤᅓ") and bstack11l1l11l1_opy_(env.get(bstack11lllll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢᅔ"))):
        return {
            bstack11lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᅕ"): bstack11lllll_opy_ (u"ࠢࡄ࡫ࡵࡧࡱ࡫ࡃࡊࠤᅖ"),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᅗ"): env.get(bstack11lllll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᅘ")),
            bstack11lllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᅙ"): env.get(bstack11lllll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡏࡕࡂࠣᅚ")),
            bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᅛ"): env.get(bstack11lllll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠤᅜ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠢࡄࡋࠥᅝ")) == bstack11lllll_opy_ (u"ࠣࡶࡵࡹࡪࠨᅞ") and bstack11l1l11l1_opy_(env.get(bstack11lllll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࠤᅟ"))):
        return {
            bstack11lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣᅠ"): bstack11lllll_opy_ (u"࡙ࠦࡸࡡࡷ࡫ࡶࠤࡈࡏࠢᅡ"),
            bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᅢ"): env.get(bstack11lllll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤ࡝ࡅࡃࡡࡘࡖࡑࠨᅣ")),
            bstack11lllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᅤ"): env.get(bstack11lllll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᅥ")),
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᅦ"): env.get(bstack11lllll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᅧ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠦࡈࡏࠢᅨ")) == bstack11lllll_opy_ (u"ࠧࡺࡲࡶࡧࠥᅩ") and env.get(bstack11lllll_opy_ (u"ࠨࡃࡊࡡࡑࡅࡒࡋࠢᅪ")) == bstack11lllll_opy_ (u"ࠢࡤࡱࡧࡩࡸ࡮ࡩࡱࠤᅫ"):
        return {
            bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᅬ"): bstack11lllll_opy_ (u"ࠤࡆࡳࡩ࡫ࡳࡩ࡫ࡳࠦᅭ"),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅮ"): None,
            bstack11lllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅯ"): None,
            bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᅰ"): None
        }
    if env.get(bstack11lllll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠤᅱ")) and env.get(bstack11lllll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠥᅲ")):
        return {
            bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᅳ"): bstack11lllll_opy_ (u"ࠤࡅ࡭ࡹࡨࡵࡤ࡭ࡨࡸࠧᅴ"),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅵ"): env.get(bstack11lllll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡈࡋࡗࡣࡍ࡚ࡔࡑࡡࡒࡖࡎࡍࡉࡏࠤᅶ")),
            bstack11lllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᅷ"): None,
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᅸ"): env.get(bstack11lllll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᅹ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠣࡅࡌࠦᅺ")) == bstack11lllll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᅻ") and bstack11l1l11l1_opy_(env.get(bstack11lllll_opy_ (u"ࠥࡈࡗࡕࡎࡆࠤᅼ"))):
        return {
            bstack11lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅽ"): bstack11lllll_opy_ (u"ࠧࡊࡲࡰࡰࡨࠦᅾ"),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅿ"): env.get(bstack11lllll_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡒࡉࡏࡍࠥᆀ")),
            bstack11lllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆁ"): None,
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆂ"): env.get(bstack11lllll_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᆃ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠦࡈࡏࠢᆄ")) == bstack11lllll_opy_ (u"ࠧࡺࡲࡶࡧࠥᆅ") and bstack11l1l11l1_opy_(env.get(bstack11lllll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࠤᆆ"))):
        return {
            bstack11lllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆇ"): bstack11lllll_opy_ (u"ࠣࡕࡨࡱࡦࡶࡨࡰࡴࡨࠦᆈ"),
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆉ"): env.get(bstack11lllll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡏࡓࡉࡄࡒࡎࡠࡁࡕࡋࡒࡒࡤ࡛ࡒࡍࠤᆊ")),
            bstack11lllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᆋ"): env.get(bstack11lllll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᆌ")),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᆍ"): env.get(bstack11lllll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᆎ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠣࡅࡌࠦᆏ")) == bstack11lllll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᆐ") and bstack11l1l11l1_opy_(env.get(bstack11lllll_opy_ (u"ࠥࡋࡎ࡚ࡌࡂࡄࡢࡇࡎࠨᆑ"))):
        return {
            bstack11lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆒ"): bstack11lllll_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧᆓ"),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆔ"): env.get(bstack11lllll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏࠦᆕ")),
            bstack11lllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆖ"): env.get(bstack11lllll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᆗ")),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆘ"): env.get(bstack11lllll_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢᆙ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠧࡉࡉࠣᆚ")) == bstack11lllll_opy_ (u"ࠨࡴࡳࡷࡨࠦᆛ") and bstack11l1l11l1_opy_(env.get(bstack11lllll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࠥᆜ"))):
        return {
            bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᆝ"): bstack11lllll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤ࡬࡫ࡷࡩࠧᆞ"),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆟ"): env.get(bstack11lllll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᆠ")),
            bstack11lllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆡ"): env.get(bstack11lllll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡏࡅࡇࡋࡌࠣᆢ")) or env.get(bstack11lllll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥᆣ")),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆤ"): env.get(bstack11lllll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᆥ"))
        }
    if bstack11l1l11l1_opy_(env.get(bstack11lllll_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᆦ"))):
        return {
            bstack11lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆧ"): bstack11lllll_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧᆨ"),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆩ"): bstack11lllll_opy_ (u"ࠢࡼࡿࡾࢁࠧᆪ").format(env.get(bstack11lllll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᆫ")), env.get(bstack11lllll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࡉࡅࠩᆬ"))),
            bstack11lllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆭ"): env.get(bstack11lllll_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥᆮ")),
            bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆯ"): env.get(bstack11lllll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᆰ"))
        }
    if bstack11l1l11l1_opy_(env.get(bstack11lllll_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤᆱ"))):
        return {
            bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᆲ"): bstack11lllll_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦᆳ"),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆴ"): bstack11lllll_opy_ (u"ࠦࢀࢃ࠯ࡱࡴࡲ࡮ࡪࡩࡴ࠰ࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠥᆵ").format(env.get(bstack11lllll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡖࡔࡏࠫᆶ")), env.get(bstack11lllll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧᆷ")), env.get(bstack11lllll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡓࡖࡔࡐࡅࡄࡖࡢࡗࡑ࡛ࡇࠨᆸ")), env.get(bstack11lllll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬᆹ"))),
            bstack11lllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆺ"): env.get(bstack11lllll_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᆻ")),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆼ"): env.get(bstack11lllll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᆽ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠨࡁ࡛ࡗࡕࡉࡤࡎࡔࡕࡒࡢ࡙ࡘࡋࡒࡠࡃࡊࡉࡓ࡚ࠢᆾ")) and env.get(bstack11lllll_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤᆿ")):
        return {
            bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᇀ"): bstack11lllll_opy_ (u"ࠤࡄࡾࡺࡸࡥࠡࡅࡌࠦᇁ"),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᇂ"): bstack11lllll_opy_ (u"ࠦࢀࢃࡻࡾ࠱ࡢࡦࡺ࡯࡬ࡥ࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡦࡺ࡯࡬ࡥࡋࡧࡁࢀࢃࠢᇃ").format(env.get(bstack11lllll_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨᇄ")), env.get(bstack11lllll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࠫᇅ")), env.get(bstack11lllll_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧᇆ"))),
            bstack11lllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇇ"): env.get(bstack11lllll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᇈ")),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇉ"): env.get(bstack11lllll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᇊ"))
        }
    if any([env.get(bstack11lllll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᇋ")), env.get(bstack11lllll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᇌ")), env.get(bstack11lllll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᇍ"))]):
        return {
            bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᇎ"): bstack11lllll_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤᇏ"),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᇐ"): env.get(bstack11lllll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᇑ")),
            bstack11lllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇒ"): env.get(bstack11lllll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᇓ")),
            bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇔ"): env.get(bstack11lllll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᇕ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᇖ")):
        return {
            bstack11lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣᇗ"): bstack11lllll_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲࠦᇘ"),
            bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇙ"): env.get(bstack11lllll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬ࠣᇚ")),
            bstack11lllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇛ"): env.get(bstack11lllll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢᇜ")),
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇝ"): env.get(bstack11lllll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣᇞ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࠧᇟ")) or env.get(bstack11lllll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢᇠ")):
        return {
            bstack11lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇡ"): bstack11lllll_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣᇢ"),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇣ"): env.get(bstack11lllll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᇤ")),
            bstack11lllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇥ"): bstack11lllll_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠦᇦ") if env.get(bstack11lllll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢᇧ")) else None,
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇨ"): env.get(bstack11lllll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘࠧᇩ"))
        }
    if any([env.get(bstack11lllll_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᇪ")), env.get(bstack11lllll_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᇫ")), env.get(bstack11lllll_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᇬ"))]):
        return {
            bstack11lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇭ"): bstack11lllll_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦᇮ"),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇯ"): None,
            bstack11lllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇰ"): env.get(bstack11lllll_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧᇱ")),
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇲ"): env.get(bstack11lllll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᇳ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢᇴ")):
        return {
            bstack11lllll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇵ"): bstack11lllll_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤᇶ"),
            bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇷ"): env.get(bstack11lllll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᇸ")),
            bstack11lllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇹ"): bstack11lllll_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࢀࠦᇺ").format(env.get(bstack11lllll_opy_ (u"ࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧᇻ"))) if env.get(bstack11lllll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠣᇼ")) else None,
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇽ"): env.get(bstack11lllll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᇾ"))
        }
    if bstack11l1l11l1_opy_(env.get(bstack11lllll_opy_ (u"ࠣࡐࡈࡘࡑࡏࡆ࡚ࠤᇿ"))):
        return {
            bstack11lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሀ"): bstack11lllll_opy_ (u"ࠥࡒࡪࡺ࡬ࡪࡨࡼࠦሁ"),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢሂ"): env.get(bstack11lllll_opy_ (u"ࠧࡊࡅࡑࡎࡒ࡝ࡤ࡛ࡒࡍࠤሃ")),
            bstack11lllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሄ"): env.get(bstack11lllll_opy_ (u"ࠢࡔࡋࡗࡉࡤࡔࡁࡎࡇࠥህ")),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሆ"): env.get(bstack11lllll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦሇ"))
        }
    if bstack11l1l11l1_opy_(env.get(bstack11lllll_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡅࡈ࡚ࡉࡐࡐࡖࠦለ"))):
        return {
            bstack11lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሉ"): bstack11lllll_opy_ (u"ࠧࡍࡩࡵࡊࡸࡦࠥࡇࡣࡵ࡫ࡲࡲࡸࠨሊ"),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤላ"): bstack11lllll_opy_ (u"ࠢࡼࡿ࠲ࡿࢂ࠵ࡡࡤࡶ࡬ࡳࡳࡹ࠯ࡳࡷࡱࡷ࠴ࢁࡽࠣሌ").format(env.get(bstack11lllll_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡕࡈࡖ࡛ࡋࡒࡠࡗࡕࡐࠬል")), env.get(bstack11lllll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕࡉࡕࡕࡓࡊࡖࡒࡖ࡞࠭ሎ")), env.get(bstack11lllll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠪሏ"))),
            bstack11lllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሐ"): env.get(bstack11lllll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤ࡝ࡏࡓࡍࡉࡐࡔ࡝ࠢሑ")),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧሒ"): env.get(bstack11lllll_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠢሓ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠣࡅࡌࠦሔ")) == bstack11lllll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢሕ") and env.get(bstack11lllll_opy_ (u"࡚ࠥࡊࡘࡃࡆࡎࠥሖ")) == bstack11lllll_opy_ (u"ࠦ࠶ࠨሗ"):
        return {
            bstack11lllll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥመ"): bstack11lllll_opy_ (u"ࠨࡖࡦࡴࡦࡩࡱࠨሙ"),
            bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሚ"): bstack11lllll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࡽࢀࠦማ").format(env.get(bstack11lllll_opy_ (u"࡙ࠩࡉࡗࡉࡅࡍࡡࡘࡖࡑ࠭ሜ"))),
            bstack11lllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧም"): None,
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሞ"): None,
        }
    if env.get(bstack11lllll_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠣሟ")):
        return {
            bstack11lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሠ"): bstack11lllll_opy_ (u"ࠢࡕࡧࡤࡱࡨ࡯ࡴࡺࠤሡ"),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሢ"): None,
            bstack11lllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሣ"): env.get(bstack11lllll_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠦሤ")),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሥ"): env.get(bstack11lllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦሦ"))
        }
    if any([env.get(bstack11lllll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࠤሧ")), env.get(bstack11lllll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡗࡒࠢረ")), env.get(bstack11lllll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨሩ")), env.get(bstack11lllll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡚ࡅࡂࡏࠥሪ"))]):
        return {
            bstack11lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣራ"): bstack11lllll_opy_ (u"ࠦࡈࡵ࡮ࡤࡱࡸࡶࡸ࡫ࠢሬ"),
            bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣር"): None,
            bstack11lllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሮ"): env.get(bstack11lllll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣሯ")) or None,
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሰ"): env.get(bstack11lllll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦሱ"), 0)
        }
    if env.get(bstack11lllll_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣሲ")):
        return {
            bstack11lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሳ"): bstack11lllll_opy_ (u"ࠧࡍ࡯ࡄࡆࠥሴ"),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤስ"): None,
            bstack11lllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሶ"): env.get(bstack11lllll_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨሷ")),
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሸ"): env.get(bstack11lllll_opy_ (u"ࠥࡋࡔࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡅࡒ࡙ࡓ࡚ࡅࡓࠤሹ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤሺ")):
        return {
            bstack11lllll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሻ"): bstack11lllll_opy_ (u"ࠨࡃࡰࡦࡨࡊࡷ࡫ࡳࡩࠤሼ"),
            bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሽ"): env.get(bstack11lllll_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢሾ")),
            bstack11lllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሿ"): env.get(bstack11lllll_opy_ (u"ࠥࡇࡋࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨቀ")),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥቁ"): env.get(bstack11lllll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥቂ"))
        }
    return {bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቃ"): None}
def get_host_info():
    return {
        bstack11lllll_opy_ (u"ࠢࡩࡱࡶࡸࡳࡧ࡭ࡦࠤቄ"): platform.node(),
        bstack11lllll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥቅ"): platform.system(),
        bstack11lllll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢቆ"): platform.machine(),
        bstack11lllll_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦቇ"): platform.version(),
        bstack11lllll_opy_ (u"ࠦࡦࡸࡣࡩࠤቈ"): platform.architecture()[0]
    }
def bstack1111l1lll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1ll1111_opy_():
    if bstack1lll11111_opy_.get_property(bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭቉")):
        return bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬቊ")
    return bstack11lllll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩ࠭ቋ")
def bstack11ll11l1l1_opy_(driver):
    info = {
        bstack11lllll_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧቌ"): driver.capabilities,
        bstack11lllll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ቍ"): driver.session_id,
        bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ቎"): driver.capabilities.get(bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ቏"), None),
        bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧቐ"): driver.capabilities.get(bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧቑ"), None),
        bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩቒ"): driver.capabilities.get(bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧቓ"), None),
    }
    if bstack11l1ll1111_opy_() == bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨቔ"):
        info[bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫቕ")] = bstack11lllll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪቖ") if bstack11lll111l_opy_() else bstack11lllll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ቗")
    return info
def bstack11lll111l_opy_():
    if bstack1lll11111_opy_.get_property(bstack11lllll_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬቘ")):
        return True
    if bstack11l1l11l1_opy_(os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ቙"), None)):
        return True
    return False
def bstack1llll11ll_opy_(bstack11l11ll1ll_opy_, url, data, config):
    headers = config.get(bstack11lllll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩቚ"), None)
    proxies = bstack11lllllll_opy_(config, url)
    auth = config.get(bstack11lllll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧቛ"), None)
    response = requests.request(
            bstack11l11ll1ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1lll1lll_opy_(bstack111lll1l_opy_, size):
    bstack1ll1ll1l1_opy_ = []
    while len(bstack111lll1l_opy_) > size:
        bstack1l1ll1lll_opy_ = bstack111lll1l_opy_[:size]
        bstack1ll1ll1l1_opy_.append(bstack1l1ll1lll_opy_)
        bstack111lll1l_opy_ = bstack111lll1l_opy_[size:]
    bstack1ll1ll1l1_opy_.append(bstack111lll1l_opy_)
    return bstack1ll1ll1l1_opy_
def bstack11l11llll1_opy_(message, bstack11l1llllll_opy_=False):
    os.write(1, bytes(message, bstack11lllll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩቜ")))
    os.write(1, bytes(bstack11lllll_opy_ (u"ࠫࡡࡴࠧቝ"), bstack11lllll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ቞")))
    if bstack11l1llllll_opy_:
        with open(bstack11lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬ቟") + os.environ[bstack11lllll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭በ")] + bstack11lllll_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭ቡ"), bstack11lllll_opy_ (u"ࠩࡤࠫቢ")) as f:
            f.write(message + bstack11lllll_opy_ (u"ࠪࡠࡳ࠭ባ"))
def bstack11ll111l1l_opy_():
    return os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧቤ")].lower() == bstack11lllll_opy_ (u"ࠬࡺࡲࡶࡧࠪብ")
def bstack1ll1111l1l_opy_(bstack11l11lll1l_opy_):
    return bstack11lllll_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬቦ").format(bstack11ll11llll_opy_, bstack11l11lll1l_opy_)
def bstack111l11lll_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11lllll_opy_ (u"࡛ࠧࠩቧ")
def bstack11l1l1l11l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11lllll_opy_ (u"ࠨ࡜ࠪቨ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11lllll_opy_ (u"ࠩ࡝ࠫቩ")))).total_seconds() * 1000
def bstack11ll111111_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11lllll_opy_ (u"ࠪ࡞ࠬቪ")
def bstack11l1l1llll_opy_(bstack11l1l11lll_opy_):
    date_format = bstack11lllll_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩቫ")
    bstack11l1ll1l1l_opy_ = datetime.datetime.strptime(bstack11l1l11lll_opy_, date_format)
    return bstack11l1ll1l1l_opy_.isoformat() + bstack11lllll_opy_ (u"ࠬࡠࠧቬ")
def bstack11l1l1ll11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ቭ")
    else:
        return bstack11lllll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧቮ")
def bstack11l1l11l1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11lllll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ቯ")
def bstack11l1lll1ll_opy_(val):
    return val.__str__().lower() == bstack11lllll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨተ")
def bstack1l11111lll_opy_(bstack11l1l1ll1l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l1ll1l_opy_ as e:
                print(bstack11lllll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥቱ").format(func.__name__, bstack11l1l1ll1l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1ll111l_opy_(bstack11l1lllll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1lllll1_opy_(cls, *args, **kwargs)
            except bstack11l1l1ll1l_opy_ as e:
                print(bstack11lllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦቲ").format(bstack11l1lllll1_opy_.__name__, bstack11l1l1ll1l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1ll111l_opy_
    else:
        return decorator
def bstack1111lll11_opy_(bstack11llll1lll_opy_):
    if bstack11lllll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩታ") in bstack11llll1lll_opy_ and bstack11l1lll1ll_opy_(bstack11llll1lll_opy_[bstack11lllll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪቴ")]):
        return False
    if bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩት") in bstack11llll1lll_opy_ and bstack11l1lll1ll_opy_(bstack11llll1lll_opy_[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪቶ")]):
        return False
    return True
def bstack1ll1l111l1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l111ll1_opy_(hub_url):
    if bstack1l1l11lll1_opy_() <= version.parse(bstack11lllll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩቷ")):
        if hub_url != bstack11lllll_opy_ (u"ࠪࠫቸ"):
            return bstack11lllll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧቹ") + hub_url + bstack11lllll_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤቺ")
        return bstack11111llll_opy_
    if hub_url != bstack11lllll_opy_ (u"࠭ࠧቻ"):
        return bstack11lllll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤቼ") + hub_url + bstack11lllll_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤች")
    return bstack1l1l11llll_opy_
def bstack11ll11l111_opy_():
    return isinstance(os.getenv(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨቾ")), str)
def bstack1l1lll1l11_opy_(url):
    return urlparse(url).hostname
def bstack1l1llll11l_opy_(hostname):
    for bstack1111ll11l_opy_ in bstack1ll1111ll1_opy_:
        regex = re.compile(bstack1111ll11l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11ll11l1ll_opy_(bstack11ll111lll_opy_, file_name, logger):
    bstack11ll11111_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠪࢂࠬቿ")), bstack11ll111lll_opy_)
    try:
        if not os.path.exists(bstack11ll11111_opy_):
            os.makedirs(bstack11ll11111_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠫࢃ࠭ኀ")), bstack11ll111lll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11lllll_opy_ (u"ࠬࡽࠧኁ")):
                pass
            with open(file_path, bstack11lllll_opy_ (u"ࠨࡷࠬࠤኂ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111l1111l_opy_.format(str(e)))
def bstack11l11lll11_opy_(file_name, key, value, logger):
    file_path = bstack11ll11l1ll_opy_(bstack11lllll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧኃ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l1l1l1l_opy_ = json.load(open(file_path, bstack11lllll_opy_ (u"ࠨࡴࡥࠫኄ")))
        else:
            bstack11l1l1l1l_opy_ = {}
        bstack11l1l1l1l_opy_[key] = value
        with open(file_path, bstack11lllll_opy_ (u"ࠤࡺ࠯ࠧኅ")) as outfile:
            json.dump(bstack11l1l1l1l_opy_, outfile)
def bstack1ll11l1l1_opy_(file_name, logger):
    file_path = bstack11ll11l1ll_opy_(bstack11lllll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪኆ"), file_name, logger)
    bstack11l1l1l1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11lllll_opy_ (u"ࠫࡷ࠭ኇ")) as bstack1l1lll111_opy_:
            bstack11l1l1l1l_opy_ = json.load(bstack1l1lll111_opy_)
    return bstack11l1l1l1l_opy_
def bstack11lll1ll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩኈ") + file_path + bstack11lllll_opy_ (u"࠭ࠠࠨ኉") + str(e))
def bstack1l1l11lll1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11lllll_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤኊ")
def bstack1l1l11l11l_opy_(config):
    if bstack11lllll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧኋ") in config:
        del (config[bstack11lllll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨኌ")])
        return False
    if bstack1l1l11lll1_opy_() < version.parse(bstack11lllll_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩኍ")):
        return False
    if bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪ኎")):
        return True
    if bstack11lllll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ኏") in config and config[bstack11lllll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ነ")] is False:
        return False
    else:
        return True
def bstack1ll1l1l1ll_opy_(args_list, bstack11l11ll1l1_opy_):
    index = -1
    for value in bstack11l11ll1l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11lllll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11lllll1_opy_ = bstack1l11lllll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11lllll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧኑ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11lllll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨኒ"), exception=exception)
    def bstack11llll1l1l_opy_(self):
        if self.result != bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩና"):
            return None
        if bstack11lllll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨኔ") in self.exception_type:
            return bstack11lllll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧን")
        return bstack11lllll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨኖ")
    def bstack11l1lll1l1_opy_(self):
        if self.result != bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ኗ"):
            return None
        if self.bstack1l11lllll1_opy_:
            return self.bstack1l11lllll1_opy_
        return bstack11l1ll1l11_opy_(self.exception)
def bstack11l1ll1l11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll11111l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lllll1l11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1lllllll1l_opy_(config, logger):
    try:
        import playwright
        bstack11l1l1l1ll_opy_ = playwright.__file__
        bstack11l1llll11_opy_ = os.path.split(bstack11l1l1l1ll_opy_)
        bstack11l1ll1lll_opy_ = bstack11l1llll11_opy_[0] + bstack11lllll_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪኘ")
        os.environ[bstack11lllll_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫኙ")] = bstack1l1ll11l1l_opy_(config)
        with open(bstack11l1ll1lll_opy_, bstack11lllll_opy_ (u"ࠩࡵࠫኚ")) as f:
            bstack11ll1111l_opy_ = f.read()
            bstack11l1l1l1l1_opy_ = bstack11lllll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩኛ")
            bstack11l1l11l11_opy_ = bstack11ll1111l_opy_.find(bstack11l1l1l1l1_opy_)
            if bstack11l1l11l11_opy_ == -1:
              process = subprocess.Popen(bstack11lllll_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣኜ"), shell=True, cwd=bstack11l1llll11_opy_[0])
              process.wait()
              bstack11l1lll111_opy_ = bstack11lllll_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬኝ")
              bstack11l1lll11l_opy_ = bstack11lllll_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥኞ")
              bstack11l1l11l1l_opy_ = bstack11ll1111l_opy_.replace(bstack11l1lll111_opy_, bstack11l1lll11l_opy_)
              with open(bstack11l1ll1lll_opy_, bstack11lllll_opy_ (u"ࠧࡸࠩኟ")) as f:
                f.write(bstack11l1l11l1l_opy_)
    except Exception as e:
        logger.error(bstack1ll11l1111_opy_.format(str(e)))
def bstack11111111l_opy_():
  try:
    bstack11l1l11111_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨአ"))
    bstack11l11ll11l_opy_ = []
    if os.path.exists(bstack11l1l11111_opy_):
      with open(bstack11l1l11111_opy_) as f:
        bstack11l11ll11l_opy_ = json.load(f)
      os.remove(bstack11l1l11111_opy_)
    return bstack11l11ll11l_opy_
  except:
    pass
  return []
def bstack1ll1111ll_opy_(bstack11l1l11ll_opy_):
  try:
    bstack11l11ll11l_opy_ = []
    bstack11l1l11111_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩኡ"))
    if os.path.exists(bstack11l1l11111_opy_):
      with open(bstack11l1l11111_opy_) as f:
        bstack11l11ll11l_opy_ = json.load(f)
    bstack11l11ll11l_opy_.append(bstack11l1l11ll_opy_)
    with open(bstack11l1l11111_opy_, bstack11lllll_opy_ (u"ࠪࡻࠬኢ")) as f:
        json.dump(bstack11l11ll11l_opy_, f)
  except:
    pass
def bstack1l1ll1l1_opy_(logger, bstack11l1l11ll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack11lllll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧኣ"), bstack11lllll_opy_ (u"ࠬ࠭ኤ"))
    if test_name == bstack11lllll_opy_ (u"࠭ࠧእ"):
        test_name = threading.current_thread().__dict__.get(bstack11lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ኦ"), bstack11lllll_opy_ (u"ࠨࠩኧ"))
    bstack11ll11l11l_opy_ = bstack11lllll_opy_ (u"ࠩ࠯ࠤࠬከ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1l11ll1_opy_:
        bstack11lllll1l_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪኩ"), bstack11lllll_opy_ (u"ࠫ࠵࠭ኪ"))
        bstack1l11l11l_opy_ = {bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪካ"): test_name, bstack11lllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬኬ"): bstack11ll11l11l_opy_, bstack11lllll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ክ"): bstack11lllll1l_opy_}
        bstack11l1l1111l_opy_ = []
        bstack11l1l111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧኮ"))
        if os.path.exists(bstack11l1l111ll_opy_):
            with open(bstack11l1l111ll_opy_) as f:
                bstack11l1l1111l_opy_ = json.load(f)
        bstack11l1l1111l_opy_.append(bstack1l11l11l_opy_)
        with open(bstack11l1l111ll_opy_, bstack11lllll_opy_ (u"ࠩࡺࠫኯ")) as f:
            json.dump(bstack11l1l1111l_opy_, f)
    else:
        bstack1l11l11l_opy_ = {bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨኰ"): test_name, bstack11lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ኱"): bstack11ll11l11l_opy_, bstack11lllll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫኲ"): str(multiprocessing.current_process().name)}
        if bstack11lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪኳ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l11l11l_opy_)
  except Exception as e:
      logger.warn(bstack11lllll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦኴ").format(e))
def bstack11l11lll1_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1ll11l1_opy_ = []
    bstack1l11l11l_opy_ = {bstack11lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ኵ"): test_name, bstack11lllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ኶"): error_message, bstack11lllll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ኷"): index}
    bstack11l1ll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬኸ"))
    if os.path.exists(bstack11l1ll11ll_opy_):
        with open(bstack11l1ll11ll_opy_) as f:
            bstack11l1ll11l1_opy_ = json.load(f)
    bstack11l1ll11l1_opy_.append(bstack1l11l11l_opy_)
    with open(bstack11l1ll11ll_opy_, bstack11lllll_opy_ (u"ࠬࡽࠧኹ")) as f:
        json.dump(bstack11l1ll11l1_opy_, f)
  except Exception as e:
    logger.warn(bstack11lllll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤኺ").format(e))
def bstack1l1l1l11l1_opy_(bstack1ll1lll1_opy_, name, logger):
  try:
    bstack1l11l11l_opy_ = {bstack11lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬኻ"): name, bstack11lllll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧኼ"): bstack1ll1lll1_opy_, bstack11lllll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨኽ"): str(threading.current_thread()._name)}
    return bstack1l11l11l_opy_
  except Exception as e:
    logger.warn(bstack11lllll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢኾ").format(e))
  return
def bstack1lll11l111_opy_(framework):
    if framework.lower() == bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ኿"):
        return bstack11l111111_opy_.version()
    elif framework.lower() == bstack11lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫዀ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11lllll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭዁"):
        import behave
        return behave.__version__
    else:
        return bstack11lllll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨዂ")
def bstack11l1l1l111_opy_():
    return platform.system() == bstack11lllll_opy_ (u"ࠨ࡙࡬ࡲࡩࡵࡷࡴࠩዃ")