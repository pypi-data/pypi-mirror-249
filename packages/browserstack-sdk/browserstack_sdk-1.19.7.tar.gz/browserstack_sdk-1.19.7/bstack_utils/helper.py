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
from bstack_utils.constants import bstack11ll1l111l_opy_, bstack1ll111ll1_opy_, bstack1lll1l1111_opy_, bstack1ll11ll1l1_opy_
from bstack_utils.messages import bstack1lllll1l1_opy_, bstack1l11ll11_opy_
from bstack_utils.proxy import bstack1l1llll1l1_opy_, bstack11111ll1l_opy_
from browserstack_sdk.bstack11l111ll_opy_ import *
from browserstack_sdk.bstack1l111l1l1l_opy_ import *
bstack11ll1l1l_opy_ = Config.get_instance()
def bstack11lll1l1ll_opy_(config):
    return config[bstack111ll11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᄦ")]
def bstack11lll11ll1_opy_(config):
    return config[bstack111ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᄧ")]
def bstack1l1lllllll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1l1ll1l_opy_(obj):
    values = []
    bstack11l11lllll_opy_ = re.compile(bstack111ll11_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢᄨ"), re.I)
    for key in obj.keys():
        if bstack11l11lllll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1ll1ll1_opy_(config):
    tags = []
    tags.extend(bstack11l1l1ll1l_opy_(os.environ))
    tags.extend(bstack11l1l1ll1l_opy_(config))
    return tags
def bstack11ll111111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1ll11l1_opy_(bstack11ll11l111_opy_):
    if not bstack11ll11l111_opy_:
        return bstack111ll11_opy_ (u"ࠫࠬᄩ")
    return bstack111ll11_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨᄪ").format(bstack11ll11l111_opy_.name, bstack11ll11l111_opy_.email)
def bstack11ll1ll1ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1l11l11_opy_ = repo.common_dir
        info = {
            bstack111ll11_opy_ (u"ࠨࡳࡩࡣࠥᄫ"): repo.head.commit.hexsha,
            bstack111ll11_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥᄬ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack111ll11_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣᄭ"): repo.active_branch.name,
            bstack111ll11_opy_ (u"ࠤࡷࡥ࡬ࠨᄮ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack111ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨᄯ"): bstack11l1ll11l1_opy_(repo.head.commit.committer),
            bstack111ll11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧᄰ"): repo.head.commit.committed_datetime.isoformat(),
            bstack111ll11_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧᄱ"): bstack11l1ll11l1_opy_(repo.head.commit.author),
            bstack111ll11_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦᄲ"): repo.head.commit.authored_datetime.isoformat(),
            bstack111ll11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᄳ"): repo.head.commit.message,
            bstack111ll11_opy_ (u"ࠣࡴࡲࡳࡹࠨᄴ"): repo.git.rev_parse(bstack111ll11_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦᄵ")),
            bstack111ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᄶ"): bstack11l1l11l11_opy_,
            bstack111ll11_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᄷ"): subprocess.check_output([bstack111ll11_opy_ (u"ࠧ࡭ࡩࡵࠤᄸ"), bstack111ll11_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤᄹ"), bstack111ll11_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥᄺ")]).strip().decode(
                bstack111ll11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᄻ")),
            bstack111ll11_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᄼ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack111ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᄽ"): repo.git.rev_list(
                bstack111ll11_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦᄾ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1l1l1l1_opy_ = []
        for remote in remotes:
            bstack11l1lll1l1_opy_ = {
                bstack111ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᄿ"): remote.name,
                bstack111ll11_opy_ (u"ࠨࡵࡳ࡮ࠥᅀ"): remote.url,
            }
            bstack11l1l1l1l1_opy_.append(bstack11l1lll1l1_opy_)
        return {
            bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅁ"): bstack111ll11_opy_ (u"ࠣࡩ࡬ࡸࠧᅂ"),
            **info,
            bstack111ll11_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥᅃ"): bstack11l1l1l1l1_opy_
        }
    except Exception as err:
        print(bstack111ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᅄ").format(err))
        return {}
def bstack1l1lll1111_opy_():
    env = os.environ
    if (bstack111ll11_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᅅ") in env and len(env[bstack111ll11_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᅆ")]) > 0) or (
            bstack111ll11_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᅇ") in env and len(env[bstack111ll11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᅈ")]) > 0):
        return {
            bstack111ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᅉ"): bstack111ll11_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥᅊ"),
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅋ"): env.get(bstack111ll11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᅌ")),
            bstack111ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᅍ"): env.get(bstack111ll11_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣᅎ")),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᅏ"): env.get(bstack111ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᅐ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠤࡆࡍࠧᅑ")) == bstack111ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣᅒ") and bstack1llll11l1_opy_(env.get(bstack111ll11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨᅓ"))):
        return {
            bstack111ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᅔ"): bstack111ll11_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣᅕ"),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᅖ"): env.get(bstack111ll11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᅗ")),
            bstack111ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᅘ"): env.get(bstack111ll11_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢᅙ")),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᅚ"): env.get(bstack111ll11_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣᅛ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠨࡃࡊࠤᅜ")) == bstack111ll11_opy_ (u"ࠢࡵࡴࡸࡩࠧᅝ") and bstack1llll11l1_opy_(env.get(bstack111ll11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣᅞ"))):
        return {
            bstack111ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅟ"): bstack111ll11_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨᅠ"),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅡ"): env.get(bstack111ll11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧᅢ")),
            bstack111ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᅣ"): env.get(bstack111ll11_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᅤ")),
            bstack111ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᅥ"): env.get(bstack111ll11_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᅦ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠥࡇࡎࠨᅧ")) == bstack111ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤᅨ") and env.get(bstack111ll11_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨᅩ")) == bstack111ll11_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣᅪ"):
        return {
            bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅫ"): bstack111ll11_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥᅬ"),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅭ"): None,
            bstack111ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᅮ"): None,
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᅯ"): None
        }
    if env.get(bstack111ll11_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣᅰ")) and env.get(bstack111ll11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤᅱ")):
        return {
            bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅲ"): bstack111ll11_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦᅳ"),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅴ"): env.get(bstack111ll11_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣᅵ")),
            bstack111ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅶ"): None,
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᅷ"): env.get(bstack111ll11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᅸ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠢࡄࡋࠥᅹ")) == bstack111ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨᅺ") and bstack1llll11l1_opy_(env.get(bstack111ll11_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣᅻ"))):
        return {
            bstack111ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣᅼ"): bstack111ll11_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥᅽ"),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᅾ"): env.get(bstack111ll11_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤᅿ")),
            bstack111ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆀ"): None,
            bstack111ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆁ"): env.get(bstack111ll11_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᆂ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠥࡇࡎࠨᆃ")) == bstack111ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤᆄ") and bstack1llll11l1_opy_(env.get(bstack111ll11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣᆅ"))):
        return {
            bstack111ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆆ"): bstack111ll11_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥᆇ"),
            bstack111ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᆈ"): env.get(bstack111ll11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣᆉ")),
            bstack111ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆊ"): env.get(bstack111ll11_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᆋ")),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆌ"): env.get(bstack111ll11_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤᆍ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠢࡄࡋࠥᆎ")) == bstack111ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨᆏ") and bstack1llll11l1_opy_(env.get(bstack111ll11_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧᆐ"))):
        return {
            bstack111ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣᆑ"): bstack111ll11_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦᆒ"),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆓ"): env.get(bstack111ll11_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥᆔ")),
            bstack111ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆕ"): env.get(bstack111ll11_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᆖ")),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆗ"): env.get(bstack111ll11_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨᆘ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠦࡈࡏࠢᆙ")) == bstack111ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥᆚ") and bstack1llll11l1_opy_(env.get(bstack111ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤᆛ"))):
        return {
            bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆜ"): bstack111ll11_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦᆝ"),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆞ"): env.get(bstack111ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᆟ")),
            bstack111ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᆠ"): env.get(bstack111ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢᆡ")) or env.get(bstack111ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᆢ")),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆣ"): env.get(bstack111ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᆤ"))
        }
    if bstack1llll11l1_opy_(env.get(bstack111ll11_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᆥ"))):
        return {
            bstack111ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣᆦ"): bstack111ll11_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦᆧ"),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆨ"): bstack111ll11_opy_ (u"ࠨࡻࡾࡽࢀࠦᆩ").format(env.get(bstack111ll11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᆪ")), env.get(bstack111ll11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨᆫ"))),
            bstack111ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆬ"): env.get(bstack111ll11_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤᆭ")),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆮ"): env.get(bstack111ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᆯ"))
        }
    if bstack1llll11l1_opy_(env.get(bstack111ll11_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣᆰ"))):
        return {
            bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆱ"): bstack111ll11_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥᆲ"),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆳ"): bstack111ll11_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤᆴ").format(env.get(bstack111ll11_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪᆵ")), env.get(bstack111ll11_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ᆶ")), env.get(bstack111ll11_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧᆷ")), env.get(bstack111ll11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫᆸ"))),
            bstack111ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆹ"): env.get(bstack111ll11_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᆺ")),
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆻ"): env.get(bstack111ll11_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᆼ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨᆽ")) and env.get(bstack111ll11_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᆾ")):
        return {
            bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆿ"): bstack111ll11_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥᇀ"),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᇁ"): bstack111ll11_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨᇂ").format(env.get(bstack111ll11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᇃ")), env.get(bstack111ll11_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪᇄ")), env.get(bstack111ll11_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ᇅ"))),
            bstack111ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇆ"): env.get(bstack111ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᇇ")),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇈ"): env.get(bstack111ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᇉ"))
        }
    if any([env.get(bstack111ll11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᇊ")), env.get(bstack111ll11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᇋ")), env.get(bstack111ll11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᇌ"))]):
        return {
            bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇍ"): bstack111ll11_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣᇎ"),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᇏ"): env.get(bstack111ll11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᇐ")),
            bstack111ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇑ"): env.get(bstack111ll11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᇒ")),
            bstack111ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇓ"): env.get(bstack111ll11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᇔ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᇕ")):
        return {
            bstack111ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇖ"): bstack111ll11_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥᇗ"),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇘ"): env.get(bstack111ll11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢᇙ")),
            bstack111ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇚ"): env.get(bstack111ll11_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨᇛ")),
            bstack111ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇜ"): env.get(bstack111ll11_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᇝ"))
        }
    if env.get(bstack111ll11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦᇞ")) or env.get(bstack111ll11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᇟ")):
        return {
            bstack111ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇠ"): bstack111ll11_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢᇡ"),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇢ"): env.get(bstack111ll11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᇣ")),
            bstack111ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇤ"): bstack111ll11_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥᇥ") if env.get(bstack111ll11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᇦ")) else None,
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇧ"): env.get(bstack111ll11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦᇨ"))
        }
    if any([env.get(bstack111ll11_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧᇩ")), env.get(bstack111ll11_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᇪ")), env.get(bstack111ll11_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᇫ"))]):
        return {
            bstack111ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣᇬ"): bstack111ll11_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥᇭ"),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇮ"): None,
            bstack111ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇯ"): env.get(bstack111ll11_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦᇰ")),
            bstack111ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇱ"): env.get(bstack111ll11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᇲ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨᇳ")):
        return {
            bstack111ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇴ"): bstack111ll11_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣᇵ"),
            bstack111ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇶ"): env.get(bstack111ll11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᇷ")),
            bstack111ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇸ"): bstack111ll11_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥᇹ").format(env.get(bstack111ll11_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭ᇺ"))) if env.get(bstack111ll11_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢᇻ")) else None,
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇼ"): env.get(bstack111ll11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᇽ"))
        }
    if bstack1llll11l1_opy_(env.get(bstack111ll11_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣᇾ"))):
        return {
            bstack111ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᇿ"): bstack111ll11_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥሀ"),
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨሁ"): env.get(bstack111ll11_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣሂ")),
            bstack111ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሃ"): env.get(bstack111ll11_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤሄ")),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨህ"): env.get(bstack111ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥሆ"))
        }
    if bstack1llll11l1_opy_(env.get(bstack111ll11_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥሇ"))):
        return {
            bstack111ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣለ"): bstack111ll11_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧሉ"),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሊ"): bstack111ll11_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢላ").format(env.get(bstack111ll11_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫሌ")), env.get(bstack111ll11_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬል")), env.get(bstack111ll11_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩሎ"))),
            bstack111ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሏ"): env.get(bstack111ll11_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨሐ")),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሑ"): env.get(bstack111ll11_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨሒ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠢࡄࡋࠥሓ")) == bstack111ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨሔ") and env.get(bstack111ll11_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤሕ")) == bstack111ll11_opy_ (u"ࠥ࠵ࠧሖ"):
        return {
            bstack111ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሗ"): bstack111ll11_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧመ"),
            bstack111ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሙ"): bstack111ll11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥሚ").format(env.get(bstack111ll11_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬማ"))),
            bstack111ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሜ"): None,
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤም"): None,
        }
    if env.get(bstack111ll11_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢሞ")):
        return {
            bstack111ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሟ"): bstack111ll11_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣሠ"),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሡ"): None,
            bstack111ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥሢ"): env.get(bstack111ll11_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥሣ")),
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤሤ"): env.get(bstack111ll11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥሥ"))
        }
    if any([env.get(bstack111ll11_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣሦ")), env.get(bstack111ll11_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨሧ")), env.get(bstack111ll11_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧረ")), env.get(bstack111ll11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤሩ"))]):
        return {
            bstack111ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሪ"): bstack111ll11_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨራ"),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢሬ"): None,
            bstack111ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢር"): env.get(bstack111ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢሮ")) or None,
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨሯ"): env.get(bstack111ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥሰ"), 0)
        }
    if env.get(bstack111ll11_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢሱ")):
        return {
            bstack111ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣሲ"): bstack111ll11_opy_ (u"ࠦࡌࡵࡃࡅࠤሳ"),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሴ"): None,
            bstack111ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣስ"): env.get(bstack111ll11_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧሶ")),
            bstack111ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሷ"): env.get(bstack111ll11_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣሸ"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣሹ")):
        return {
            bstack111ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሺ"): bstack111ll11_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣሻ"),
            bstack111ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሼ"): env.get(bstack111ll11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨሽ")),
            bstack111ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥሾ"): env.get(bstack111ll11_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧሿ")),
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤቀ"): env.get(bstack111ll11_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤቁ"))
        }
    return {bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦቂ"): None}
def get_host_info():
    return {
        bstack111ll11_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣቃ"): platform.node(),
        bstack111ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤቄ"): platform.system(),
        bstack111ll11_opy_ (u"ࠣࡶࡼࡴࡪࠨቅ"): platform.machine(),
        bstack111ll11_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥቆ"): platform.version(),
        bstack111ll11_opy_ (u"ࠥࡥࡷࡩࡨࠣቇ"): platform.architecture()[0]
    }
def bstack1111l111l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11ll1111l1_opy_():
    if bstack11ll1l1l_opy_.get_property(bstack111ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬቈ")):
        return bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ቉")
    return bstack111ll11_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬቊ")
def bstack11l1lll1ll_opy_(driver):
    info = {
        bstack111ll11_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ቋ"): driver.capabilities,
        bstack111ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬቌ"): driver.session_id,
        bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪቍ"): driver.capabilities.get(bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ቎"), None),
        bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭቏"): driver.capabilities.get(bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ቐ"), None),
        bstack111ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨቑ"): driver.capabilities.get(bstack111ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ቒ"), None),
    }
    if bstack11ll1111l1_opy_() == bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧቓ"):
        info[bstack111ll11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪቔ")] = bstack111ll11_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩቕ") if bstack1l1111l1l_opy_() else bstack111ll11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ቖ")
    return info
def bstack1l1111l1l_opy_():
    if bstack11ll1l1l_opy_.get_property(bstack111ll11_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ቗")):
        return True
    if bstack1llll11l1_opy_(os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧቘ"), None)):
        return True
    return False
def bstack1ll111lll1_opy_(bstack11l11llll1_opy_, url, data, config):
    headers = config.get(bstack111ll11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ቙"), None)
    proxies = bstack1l1llll1l1_opy_(config, url)
    auth = config.get(bstack111ll11_opy_ (u"ࠨࡣࡸࡸ࡭࠭ቚ"), None)
    response = requests.request(
            bstack11l11llll1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1l1l11_opy_(bstack1lllll1l1l_opy_, size):
    bstack11ll11111_opy_ = []
    while len(bstack1lllll1l1l_opy_) > size:
        bstack1ll111l1l1_opy_ = bstack1lllll1l1l_opy_[:size]
        bstack11ll11111_opy_.append(bstack1ll111l1l1_opy_)
        bstack1lllll1l1l_opy_ = bstack1lllll1l1l_opy_[size:]
    bstack11ll11111_opy_.append(bstack1lllll1l1l_opy_)
    return bstack11ll11111_opy_
def bstack11l1l1111l_opy_(message, bstack11ll1111ll_opy_=False):
    os.write(1, bytes(message, bstack111ll11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨቛ")))
    os.write(1, bytes(bstack111ll11_opy_ (u"ࠪࡠࡳ࠭ቜ"), bstack111ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪቝ")))
    if bstack11ll1111ll_opy_:
        with open(bstack111ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫ቞") + os.environ[bstack111ll11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ቟")] + bstack111ll11_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬበ"), bstack111ll11_opy_ (u"ࠨࡣࠪቡ")) as f:
            f.write(message + bstack111ll11_opy_ (u"ࠩ࡟ࡲࠬቢ"))
def bstack11l1ll11ll_opy_():
    return os.environ[bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ባ")].lower() == bstack111ll11_opy_ (u"ࠫࡹࡸࡵࡦࠩቤ")
def bstack1l1l1l1l1_opy_(bstack11ll11l1ll_opy_):
    return bstack111ll11_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫብ").format(bstack11ll1l111l_opy_, bstack11ll11l1ll_opy_)
def bstack111l11ll1_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack111ll11_opy_ (u"࡚࠭ࠨቦ")
def bstack11l1l1l11l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack111ll11_opy_ (u"࡛ࠧࠩቧ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack111ll11_opy_ (u"ࠨ࡜ࠪቨ")))).total_seconds() * 1000
def bstack11l1ll1l1l_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack111ll11_opy_ (u"ࠩ࡝ࠫቩ")
def bstack11l1l11l1l_opy_(bstack11l1l11111_opy_):
    date_format = bstack111ll11_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨቪ")
    bstack11l1l1l111_opy_ = datetime.datetime.strptime(bstack11l1l11111_opy_, date_format)
    return bstack11l1l1l111_opy_.isoformat() + bstack111ll11_opy_ (u"ࠫ࡟࠭ቫ")
def bstack11l1ll1l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack111ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬቬ")
    else:
        return bstack111ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ቭ")
def bstack1llll11l1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack111ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬቮ")
def bstack11l1lll11l_opy_(val):
    return val.__str__().lower() == bstack111ll11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧቯ")
def bstack1l11lll1ll_opy_(bstack11l1l1l1ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l1l1ll_opy_ as e:
                print(bstack111ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤተ").format(func.__name__, bstack11l1l1l1ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1l11lll_opy_(bstack11l1ll1111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1ll1111_opy_(cls, *args, **kwargs)
            except bstack11l1l1l1ll_opy_ as e:
                print(bstack111ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥቱ").format(bstack11l1ll1111_opy_.__name__, bstack11l1l1l1ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1l11lll_opy_
    else:
        return decorator
def bstack1l1l111ll_opy_(bstack1l111111ll_opy_):
    if bstack111ll11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨቲ") in bstack1l111111ll_opy_ and bstack11l1lll11l_opy_(bstack1l111111ll_opy_[bstack111ll11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩታ")]):
        return False
    if bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨቴ") in bstack1l111111ll_opy_ and bstack11l1lll11l_opy_(bstack1l111111ll_opy_[bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩት")]):
        return False
    return True
def bstack1ll11l1l1l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l11ll1l1_opy_(hub_url):
    if bstack1llll11ll1_opy_() <= version.parse(bstack111ll11_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨቶ")):
        if hub_url != bstack111ll11_opy_ (u"ࠩࠪቷ"):
            return bstack111ll11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦቸ") + hub_url + bstack111ll11_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣቹ")
        return bstack1lll1l1111_opy_
    if hub_url != bstack111ll11_opy_ (u"ࠬ࠭ቺ"):
        return bstack111ll11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣቻ") + hub_url + bstack111ll11_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣቼ")
    return bstack1ll11ll1l1_opy_
def bstack11l1lllll1_opy_():
    return isinstance(os.getenv(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧች")), str)
def bstack1lllll11l_opy_(url):
    return urlparse(url).hostname
def bstack1lllllllll_opy_(hostname):
    for bstack1l1lll1ll_opy_ in bstack1ll111ll1_opy_:
        regex = re.compile(bstack1l1lll1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l11ll1ll_opy_(bstack11l1llll11_opy_, file_name, logger):
    bstack1ll1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack111ll11_opy_ (u"ࠩࢁࠫቾ")), bstack11l1llll11_opy_)
    try:
        if not os.path.exists(bstack1ll1ll1l1_opy_):
            os.makedirs(bstack1ll1ll1l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack111ll11_opy_ (u"ࠪࢂࠬቿ")), bstack11l1llll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack111ll11_opy_ (u"ࠫࡼ࠭ኀ")):
                pass
            with open(file_path, bstack111ll11_opy_ (u"ࠧࡽࠫࠣኁ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lllll1l1_opy_.format(str(e)))
def bstack11ll111l11_opy_(file_name, key, value, logger):
    file_path = bstack11l11ll1ll_opy_(bstack111ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ኂ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1111lll11_opy_ = json.load(open(file_path, bstack111ll11_opy_ (u"ࠧࡳࡤࠪኃ")))
        else:
            bstack1111lll11_opy_ = {}
        bstack1111lll11_opy_[key] = value
        with open(file_path, bstack111ll11_opy_ (u"ࠣࡹ࠮ࠦኄ")) as outfile:
            json.dump(bstack1111lll11_opy_, outfile)
def bstack11l1l1l1_opy_(file_name, logger):
    file_path = bstack11l11ll1ll_opy_(bstack111ll11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩኅ"), file_name, logger)
    bstack1111lll11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack111ll11_opy_ (u"ࠪࡶࠬኆ")) as bstack1lll1111_opy_:
            bstack1111lll11_opy_ = json.load(bstack1lll1111_opy_)
    return bstack1111lll11_opy_
def bstack1l1l1lll1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨኇ") + file_path + bstack111ll11_opy_ (u"ࠬࠦࠧኈ") + str(e))
def bstack1llll11ll1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack111ll11_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣ኉")
def bstack1ll111111_opy_(config):
    if bstack111ll11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ኊ") in config:
        del (config[bstack111ll11_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧኋ")])
        return False
    if bstack1llll11ll1_opy_() < version.parse(bstack111ll11_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨኌ")):
        return False
    if bstack1llll11ll1_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩኍ")):
        return True
    if bstack111ll11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ኎") in config and config[bstack111ll11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ኏")] is False:
        return False
    else:
        return True
def bstack1lll1l1lll_opy_(args_list, bstack11l11lll1l_opy_):
    index = -1
    for value in bstack11l11lll1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l1111l1l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l1111l1l1_opy_ = bstack1l1111l1l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack111ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ነ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack111ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧኑ"), exception=exception)
    def bstack11llll1l1l_opy_(self):
        if self.result != bstack111ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨኒ"):
            return None
        if bstack111ll11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧና") in self.exception_type:
            return bstack111ll11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦኔ")
        return bstack111ll11_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧን")
    def bstack11l1l1ll11_opy_(self):
        if self.result != bstack111ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬኖ"):
            return None
        if self.bstack1l1111l1l1_opy_:
            return self.bstack1l1111l1l1_opy_
        return bstack11l1llllll_opy_(self.exception)
def bstack11l1llllll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1l11ll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll1ll1ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1ll11ll1_opy_(config, logger):
    try:
        import playwright
        bstack11l11lll11_opy_ = playwright.__file__
        bstack11l1ll111l_opy_ = os.path.split(bstack11l11lll11_opy_)
        bstack11l1l1lll1_opy_ = bstack11l1ll111l_opy_[0] + bstack111ll11_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴࠩኗ")
        os.environ[bstack111ll11_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠪኘ")] = bstack11111ll1l_opy_(config)
        with open(bstack11l1l1lll1_opy_, bstack111ll11_opy_ (u"ࠨࡴࠪኙ")) as f:
            bstack1l1lll1l1_opy_ = f.read()
            bstack11l1l111l1_opy_ = bstack111ll11_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨኚ")
            bstack11ll11111l_opy_ = bstack1l1lll1l1_opy_.find(bstack11l1l111l1_opy_)
            if bstack11ll11111l_opy_ == -1:
              process = subprocess.Popen(bstack111ll11_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠢኛ"), shell=True, cwd=bstack11l1ll111l_opy_[0])
              process.wait()
              bstack11l1l1llll_opy_ = bstack111ll11_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫኜ")
              bstack11l11ll11l_opy_ = bstack111ll11_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤኝ")
              bstack11l11ll1l1_opy_ = bstack1l1lll1l1_opy_.replace(bstack11l1l1llll_opy_, bstack11l11ll11l_opy_)
              with open(bstack11l1l1lll1_opy_, bstack111ll11_opy_ (u"࠭ࡷࠨኞ")) as f:
                f.write(bstack11l11ll1l1_opy_)
    except Exception as e:
        logger.error(bstack1l11ll11_opy_.format(str(e)))
def bstack11ll1l111_opy_():
  try:
    bstack11l1lll111_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧኟ"))
    bstack11ll11l11l_opy_ = []
    if os.path.exists(bstack11l1lll111_opy_):
      with open(bstack11l1lll111_opy_) as f:
        bstack11ll11l11l_opy_ = json.load(f)
      os.remove(bstack11l1lll111_opy_)
    return bstack11ll11l11l_opy_
  except:
    pass
  return []
def bstack1ll1l1l1ll_opy_(bstack1lll11ll11_opy_):
  try:
    bstack11ll11l11l_opy_ = []
    bstack11l1lll111_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨአ"))
    if os.path.exists(bstack11l1lll111_opy_):
      with open(bstack11l1lll111_opy_) as f:
        bstack11ll11l11l_opy_ = json.load(f)
    bstack11ll11l11l_opy_.append(bstack1lll11ll11_opy_)
    with open(bstack11l1lll111_opy_, bstack111ll11_opy_ (u"ࠩࡺࠫኡ")) as f:
        json.dump(bstack11ll11l11l_opy_, f)
  except:
    pass
def bstack1l1ll1111_opy_(logger, bstack11ll111lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack111ll11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ኢ"), bstack111ll11_opy_ (u"ࠫࠬኣ"))
    if test_name == bstack111ll11_opy_ (u"ࠬ࠭ኤ"):
        test_name = threading.current_thread().__dict__.get(bstack111ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬእ"), bstack111ll11_opy_ (u"ࠧࠨኦ"))
    bstack11l1l111ll_opy_ = bstack111ll11_opy_ (u"ࠨ࠮ࠣࠫኧ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll111lll_opy_:
        bstack1ll1l1ll_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩከ"), bstack111ll11_opy_ (u"ࠪ࠴ࠬኩ"))
        bstack11ll11l1_opy_ = {bstack111ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩኪ"): test_name, bstack111ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫካ"): bstack11l1l111ll_opy_, bstack111ll11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬኬ"): bstack1ll1l1ll_opy_}
        bstack11ll111ll1_opy_ = []
        bstack11l1llll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ክ"))
        if os.path.exists(bstack11l1llll1l_opy_):
            with open(bstack11l1llll1l_opy_) as f:
                bstack11ll111ll1_opy_ = json.load(f)
        bstack11ll111ll1_opy_.append(bstack11ll11l1_opy_)
        with open(bstack11l1llll1l_opy_, bstack111ll11_opy_ (u"ࠨࡹࠪኮ")) as f:
            json.dump(bstack11ll111ll1_opy_, f)
    else:
        bstack11ll11l1_opy_ = {bstack111ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧኯ"): test_name, bstack111ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩኰ"): bstack11l1l111ll_opy_, bstack111ll11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ኱"): str(multiprocessing.current_process().name)}
        if bstack111ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩኲ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11ll11l1_opy_)
  except Exception as e:
      logger.warn(bstack111ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥኳ").format(e))
def bstack11l1l1l1l_opy_(error_message, test_name, index, logger):
  try:
    bstack11ll11l1l1_opy_ = []
    bstack11ll11l1_opy_ = {bstack111ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬኴ"): test_name, bstack111ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧኵ"): error_message, bstack111ll11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ኶"): index}
    bstack11l1ll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ኷"))
    if os.path.exists(bstack11l1ll1lll_opy_):
        with open(bstack11l1ll1lll_opy_) as f:
            bstack11ll11l1l1_opy_ = json.load(f)
    bstack11ll11l1l1_opy_.append(bstack11ll11l1_opy_)
    with open(bstack11l1ll1lll_opy_, bstack111ll11_opy_ (u"ࠫࡼ࠭ኸ")) as f:
        json.dump(bstack11ll11l1l1_opy_, f)
  except Exception as e:
    logger.warn(bstack111ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣኹ").format(e))
def bstack111lll1ll_opy_(bstack1l1lll11_opy_, name, logger):
  try:
    bstack11ll11l1_opy_ = {bstack111ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫኺ"): name, bstack111ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ኻ"): bstack1l1lll11_opy_, bstack111ll11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧኼ"): str(threading.current_thread()._name)}
    return bstack11ll11l1_opy_
  except Exception as e:
    logger.warn(bstack111ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨኽ").format(e))
  return
def bstack11l1ll11l_opy_(framework):
    if framework.lower() == bstack111ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪኾ"):
        return bstack1l1ll1ll_opy_.version()
    elif framework.lower() == bstack111ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ኿"):
        return RobotHandler.version()
    elif framework.lower() == bstack111ll11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬዀ"):
        import behave
        return behave.__version__
    else:
        return bstack111ll11_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧ዁")
def bstack11ll111l1l_opy_():
    return platform.system() == bstack111ll11_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨዂ")