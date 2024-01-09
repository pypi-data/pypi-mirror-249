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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1lll1ll1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1lllllll11_opy_
import time
import requests
def bstack1l1l1ll111_opy_():
  global CONFIG
  headers = {
        bstack11lllll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11lllll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11lllllll_opy_(CONFIG, bstack1ll1ll1ll_opy_)
  try:
    response = requests.get(bstack1ll1ll1ll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack111l1l1l1_opy_ = response.json()[bstack11lllll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1lll1ll11_opy_.format(response.json()))
      return bstack111l1l1l1_opy_
    else:
      logger.debug(bstack1ll111l1l_opy_.format(bstack11lllll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll111l1l_opy_.format(e))
def bstack11lllll11_opy_(hub_url):
  global CONFIG
  url = bstack11lllll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11lllll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11lllll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11lllll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11lllllll_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll1l1ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll11l111l_opy_.format(hub_url, e))
def bstack11l11111_opy_():
  try:
    global bstack111ll1l1_opy_
    bstack111l1l1l1_opy_ = bstack1l1l1ll111_opy_()
    bstack1l11l1l1_opy_ = []
    results = []
    for bstack1ll1llllll_opy_ in bstack111l1l1l1_opy_:
      bstack1l11l1l1_opy_.append(bstack1l111lll_opy_(target=bstack11lllll11_opy_,args=(bstack1ll1llllll_opy_,)))
    for t in bstack1l11l1l1_opy_:
      t.start()
    for t in bstack1l11l1l1_opy_:
      results.append(t.join())
    bstack1l1l1lll11_opy_ = {}
    for item in results:
      hub_url = item[bstack11lllll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11lllll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1l1lll11_opy_[hub_url] = latency
    bstack1lll1l1l11_opy_ = min(bstack1l1l1lll11_opy_, key= lambda x: bstack1l1l1lll11_opy_[x])
    bstack111ll1l1_opy_ = bstack1lll1l1l11_opy_
    logger.debug(bstack11l1l11l_opy_.format(bstack1lll1l1l11_opy_))
  except Exception as e:
    logger.debug(bstack1ll11l1l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1llll11ll_opy_, bstack1ll1111l1l_opy_, bstack1lllll1l11_opy_, bstack1111lll11_opy_, Notset, bstack1l1l11l11l_opy_, \
  bstack1ll11l1l1_opy_, bstack11lll1ll1_opy_, bstack1ll1l1l1ll_opy_, bstack1llll1111l_opy_, bstack1ll1l111l1_opy_, bstack1111l1lll_opy_, bstack111lll11l_opy_, \
  bstack1lllllll1l_opy_, bstack11111111l_opy_, bstack1ll1111ll_opy_, bstack1l1l1l11l1_opy_, bstack1l1ll1l1_opy_, bstack11l11lll1_opy_, \
  bstack1lll11l111_opy_, bstack11l1l11l1_opy_
from bstack_utils.bstack111111l1_opy_ import bstack1l1ll1l11_opy_
from bstack_utils.bstack1ll11ll11l_opy_ import bstack1lll1l11l1_opy_, bstack1lll11l1l_opy_
from bstack_utils.bstack11l1ll11l_opy_ import bstack1ll1llll1l_opy_
from bstack_utils.proxy import bstack1ll111111_opy_, bstack11lllllll_opy_, bstack1l1ll11l1l_opy_, bstack1lll1l111_opy_
import bstack_utils.bstack1lll1llll1_opy_ as bstack1111ll111_opy_
from browserstack_sdk.bstack1111lllll_opy_ import *
from browserstack_sdk.bstack111l11ll1_opy_ import *
from bstack_utils.bstack1111lll1_opy_ import bstack1ll1111l1_opy_
bstack1ll1ll11_opy_ = bstack11lllll_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1l1llllll1_opy_ = bstack11lllll_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1l11ll1l1_opy_ = None
CONFIG = {}
bstack11ll1llll_opy_ = {}
bstack1ll111l1l1_opy_ = {}
bstack1111l1l1_opy_ = None
bstack11l1lll1_opy_ = None
bstack11l1llll_opy_ = None
bstack11l1lll1l_opy_ = -1
bstack111l11l11_opy_ = 0
bstack1lllll11_opy_ = bstack1llllllll1_opy_
bstack1llll1l11l_opy_ = 1
bstack1ll1l11ll_opy_ = False
bstack1ll1lll1l_opy_ = False
bstack1l1ll1ll11_opy_ = bstack11lllll_opy_ (u"ࠨࠩࢂ")
bstack1ll11111l_opy_ = bstack11lllll_opy_ (u"ࠩࠪࢃ")
bstack1ll11ll11_opy_ = False
bstack1l1l111l_opy_ = True
bstack1lllll1l1_opy_ = bstack11lllll_opy_ (u"ࠪࠫࢄ")
bstack1lll11l1ll_opy_ = []
bstack111ll1l1_opy_ = bstack11lllll_opy_ (u"ࠫࠬࢅ")
bstack1ll1llll_opy_ = False
bstack1l1ll111_opy_ = None
bstack111ll1l11_opy_ = None
bstack1lll1l1ll_opy_ = None
bstack1l11llll1_opy_ = -1
bstack1l1l11l111_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠬࢄࠧࢆ")), bstack11lllll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack11lllll_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1l1111l11_opy_ = 0
bstack1lllll11ll_opy_ = []
bstack11llll1l_opy_ = []
bstack1llll1ll1_opy_ = []
bstack1ll1l1ll1l_opy_ = []
bstack1l1l11ll1_opy_ = bstack11lllll_opy_ (u"ࠨࠩࢉ")
bstack11l1l1l1_opy_ = bstack11lllll_opy_ (u"ࠩࠪࢊ")
bstack1ll11l11l1_opy_ = False
bstack11l1ll11_opy_ = False
bstack1l1l11l1l1_opy_ = {}
bstack11l1ll1l_opy_ = None
bstack1ll1lll111_opy_ = None
bstack11111l11_opy_ = None
bstack1l1l1ll1l_opy_ = None
bstack1l1l1l1lll_opy_ = None
bstack111l1llll_opy_ = None
bstack1l1ll1lll1_opy_ = None
bstack1ll11ll111_opy_ = None
bstack1lll1ll11l_opy_ = None
bstack11l11l11_opy_ = None
bstack1llll11ll1_opy_ = None
bstack1llllll11l_opy_ = None
bstack1llll1ll1l_opy_ = None
bstack1l1l1l1ll_opy_ = None
bstack1l1lll111l_opy_ = None
bstack1lll1lll1_opy_ = None
bstack11ll11l1_opy_ = None
bstack1l1ll11lll_opy_ = None
bstack1lll1l11ll_opy_ = None
bstack11l111l1_opy_ = None
bstack1llll1lll1_opy_ = None
bstack1111l111_opy_ = bstack11lllll_opy_ (u"ࠥࠦࢋ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1lllll11_opy_,
                    format=bstack11lllll_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩࢌ"),
                    datefmt=bstack11lllll_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧࢍ"),
                    stream=sys.stdout)
bstack1lll11111_opy_ = Config.get_instance()
percy = bstack11l1l1ll1_opy_()
bstack111llll1_opy_ = bstack1lllllll11_opy_()
def bstack111l1lll_opy_():
  global CONFIG
  global bstack1lllll11_opy_
  if bstack11lllll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ") in CONFIG:
    bstack1lllll11_opy_ = bstack1lllll111_opy_[CONFIG[bstack11lllll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ࢏")]]
    logging.getLogger().setLevel(bstack1lllll11_opy_)
def bstack11l11llll_opy_():
  global CONFIG
  global bstack1ll11l11l1_opy_
  global bstack1lll11111_opy_
  bstack1l1ll1llll_opy_ = bstack11l11l11l_opy_(CONFIG)
  if (bstack11lllll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐") in bstack1l1ll1llll_opy_ and str(bstack1l1ll1llll_opy_[bstack11lllll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ࢑")]).lower() == bstack11lllll_opy_ (u"ࠪࡸࡷࡻࡥࠨ࢒")):
    bstack1ll11l11l1_opy_ = True
  bstack1lll11111_opy_.bstack11l11111l_opy_(bstack1l1ll1llll_opy_.get(bstack11lllll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࢓"), False))
def bstack1l1ll1l1l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1l11lll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1111111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11lllll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࢔") == args[i].lower() or bstack11lllll_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࢕") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lllll1l1_opy_
      bstack1lllll1l1_opy_ += bstack11lllll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࢖") + path
      return path
  return None
bstack1l11ll11l_opy_ = re.compile(bstack11lllll_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂࠦࢗ"))
def bstack11ll1l11l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l11ll11l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11lllll_opy_ (u"ࠤࠧࡿࠧ࢘") + group + bstack11lllll_opy_ (u"ࠥࢁ࢙ࠧ"), os.environ.get(group))
  return value
def bstack11lll1l1_opy_():
  bstack11111ll11_opy_ = bstack1ll1111111_opy_()
  if bstack11111ll11_opy_ and os.path.exists(os.path.abspath(bstack11111ll11_opy_)):
    fileName = bstack11111ll11_opy_
  if bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࢚") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࢛ࠩ")])) and not bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ࢜") in locals():
    fileName = os.environ[bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢝")]
  if bstack11lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ࢞") in locals():
    bstack1l1l1l1_opy_ = os.path.abspath(fileName)
  else:
    bstack1l1l1l1_opy_ = bstack11lllll_opy_ (u"ࠩࠪ࢟")
  bstack111lll11_opy_ = os.getcwd()
  bstack1ll11l1l11_opy_ = bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࢠ")
  bstack1l111l111_opy_ = bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࢡ")
  while (not os.path.exists(bstack1l1l1l1_opy_)) and bstack111lll11_opy_ != bstack11lllll_opy_ (u"ࠧࠨࢢ"):
    bstack1l1l1l1_opy_ = os.path.join(bstack111lll11_opy_, bstack1ll11l1l11_opy_)
    if not os.path.exists(bstack1l1l1l1_opy_):
      bstack1l1l1l1_opy_ = os.path.join(bstack111lll11_opy_, bstack1l111l111_opy_)
    if bstack111lll11_opy_ != os.path.dirname(bstack111lll11_opy_):
      bstack111lll11_opy_ = os.path.dirname(bstack111lll11_opy_)
    else:
      bstack111lll11_opy_ = bstack11lllll_opy_ (u"ࠨࠢࢣ")
  if not os.path.exists(bstack1l1l1l1_opy_):
    bstack1l11lllll_opy_(
      bstack1l111lll1_opy_.format(os.getcwd()))
  try:
    with open(bstack1l1l1l1_opy_, bstack11lllll_opy_ (u"ࠧࡳࠩࢤ")) as stream:
      yaml.add_implicit_resolver(bstack11lllll_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࢥ"), bstack1l11ll11l_opy_)
      yaml.add_constructor(bstack11lllll_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࢦ"), bstack11ll1l11l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l1l1l1_opy_, bstack11lllll_opy_ (u"ࠪࡶࠬࢧ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1l11lllll_opy_(bstack1ll111ll1_opy_.format(str(exc)))
def bstack1l111l11l_opy_(config):
  bstack1111l1111_opy_ = bstack111111111_opy_(config)
  for option in list(bstack1111l1111_opy_):
    if option.lower() in bstack1ll1l1111_opy_ and option != bstack1ll1l1111_opy_[option.lower()]:
      bstack1111l1111_opy_[bstack1ll1l1111_opy_[option.lower()]] = bstack1111l1111_opy_[option]
      del bstack1111l1111_opy_[option]
  return config
def bstack1ll1ll11l_opy_():
  global bstack1ll111l1l1_opy_
  for key, bstack1l1ll1l11l_opy_ in bstack1ll111l111_opy_.items():
    if isinstance(bstack1l1ll1l11l_opy_, list):
      for var in bstack1l1ll1l11l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll111l1l1_opy_[key] = os.environ[var]
          break
    elif bstack1l1ll1l11l_opy_ in os.environ and os.environ[bstack1l1ll1l11l_opy_] and str(os.environ[bstack1l1ll1l11l_opy_]).strip():
      bstack1ll111l1l1_opy_[key] = os.environ[bstack1l1ll1l11l_opy_]
  if bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ") in os.environ:
    bstack1ll111l1l1_opy_[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢩ")] = {}
    bstack1ll111l1l1_opy_[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")][bstack11lllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢫ")] = os.environ[bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࢬ")]
def bstack1111ll1l_opy_():
  global bstack11ll1llll_opy_
  global bstack1lllll1l1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11lllll_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢭ").lower() == val.lower():
      bstack11ll1llll_opy_[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢮ")] = {}
      bstack11ll1llll_opy_[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢯ")][bstack11lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11l111lll_opy_ in bstack1lll111lll_opy_.items():
    if isinstance(bstack11l111lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11l111lll_opy_:
          if idx < len(sys.argv) and bstack11lllll_opy_ (u"࠭࠭࠮ࠩࢱ") + var.lower() == val.lower() and not key in bstack11ll1llll_opy_:
            bstack11ll1llll_opy_[key] = sys.argv[idx + 1]
            bstack1lllll1l1_opy_ += bstack11lllll_opy_ (u"ࠧࠡ࠯࠰ࠫࢲ") + var + bstack11lllll_opy_ (u"ࠨࠢࠪࢳ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11lllll_opy_ (u"ࠩ࠰࠱ࠬࢴ") + bstack11l111lll_opy_.lower() == val.lower() and not key in bstack11ll1llll_opy_:
          bstack11ll1llll_opy_[key] = sys.argv[idx + 1]
          bstack1lllll1l1_opy_ += bstack11lllll_opy_ (u"ࠪࠤ࠲࠳ࠧࢵ") + bstack11l111lll_opy_ + bstack11lllll_opy_ (u"ࠫࠥ࠭ࢶ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l111111_opy_(config):
  bstack1lllllllll_opy_ = config.keys()
  for bstack11ll1l111_opy_, bstack11ll1l1l_opy_ in bstack1l1l1llll_opy_.items():
    if bstack11ll1l1l_opy_ in bstack1lllllllll_opy_:
      config[bstack11ll1l111_opy_] = config[bstack11ll1l1l_opy_]
      del config[bstack11ll1l1l_opy_]
  for bstack11ll1l111_opy_, bstack11ll1l1l_opy_ in bstack1lll1l1l_opy_.items():
    if isinstance(bstack11ll1l1l_opy_, list):
      for bstack1ll1l11lll_opy_ in bstack11ll1l1l_opy_:
        if bstack1ll1l11lll_opy_ in bstack1lllllllll_opy_:
          config[bstack11ll1l111_opy_] = config[bstack1ll1l11lll_opy_]
          del config[bstack1ll1l11lll_opy_]
          break
    elif bstack11ll1l1l_opy_ in bstack1lllllllll_opy_:
      config[bstack11ll1l111_opy_] = config[bstack11ll1l1l_opy_]
      del config[bstack11ll1l1l_opy_]
  for bstack1ll1l11lll_opy_ in list(config):
    for bstack1l1llll1l1_opy_ in bstack11llll1l1_opy_:
      if bstack1ll1l11lll_opy_.lower() == bstack1l1llll1l1_opy_.lower() and bstack1ll1l11lll_opy_ != bstack1l1llll1l1_opy_:
        config[bstack1l1llll1l1_opy_] = config[bstack1ll1l11lll_opy_]
        del config[bstack1ll1l11lll_opy_]
  bstack1ll11l11ll_opy_ = []
  if bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࢷ") in config:
    bstack1ll11l11ll_opy_ = config[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࢸ")]
  for platform in bstack1ll11l11ll_opy_:
    for bstack1ll1l11lll_opy_ in list(platform):
      for bstack1l1llll1l1_opy_ in bstack11llll1l1_opy_:
        if bstack1ll1l11lll_opy_.lower() == bstack1l1llll1l1_opy_.lower() and bstack1ll1l11lll_opy_ != bstack1l1llll1l1_opy_:
          platform[bstack1l1llll1l1_opy_] = platform[bstack1ll1l11lll_opy_]
          del platform[bstack1ll1l11lll_opy_]
  for bstack11ll1l111_opy_, bstack11ll1l1l_opy_ in bstack1lll1l1l_opy_.items():
    for platform in bstack1ll11l11ll_opy_:
      if isinstance(bstack11ll1l1l_opy_, list):
        for bstack1ll1l11lll_opy_ in bstack11ll1l1l_opy_:
          if bstack1ll1l11lll_opy_ in platform:
            platform[bstack11ll1l111_opy_] = platform[bstack1ll1l11lll_opy_]
            del platform[bstack1ll1l11lll_opy_]
            break
      elif bstack11ll1l1l_opy_ in platform:
        platform[bstack11ll1l111_opy_] = platform[bstack11ll1l1l_opy_]
        del platform[bstack11ll1l1l_opy_]
  for bstack1l1lllll1_opy_ in bstack1l1l1ll1l1_opy_:
    if bstack1l1lllll1_opy_ in config:
      if not bstack1l1l1ll1l1_opy_[bstack1l1lllll1_opy_] in config:
        config[bstack1l1l1ll1l1_opy_[bstack1l1lllll1_opy_]] = {}
      config[bstack1l1l1ll1l1_opy_[bstack1l1lllll1_opy_]].update(config[bstack1l1lllll1_opy_])
      del config[bstack1l1lllll1_opy_]
  for platform in bstack1ll11l11ll_opy_:
    for bstack1l1lllll1_opy_ in bstack1l1l1ll1l1_opy_:
      if bstack1l1lllll1_opy_ in list(platform):
        if not bstack1l1l1ll1l1_opy_[bstack1l1lllll1_opy_] in platform:
          platform[bstack1l1l1ll1l1_opy_[bstack1l1lllll1_opy_]] = {}
        platform[bstack1l1l1ll1l1_opy_[bstack1l1lllll1_opy_]].update(platform[bstack1l1lllll1_opy_])
        del platform[bstack1l1lllll1_opy_]
  config = bstack1l111l11l_opy_(config)
  return config
def bstack11l1lllll_opy_(config):
  global bstack1ll11111l_opy_
  if bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࢹ") in config and str(config[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢺ")]).lower() != bstack11lllll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࢻ"):
    if not bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢼ") in config:
      config[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢽ")] = {}
    if not bstack11lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢾ") in config[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")]:
      bstack111l11lll_opy_ = datetime.datetime.now()
      bstack1l1lll1111_opy_ = bstack111l11lll_opy_.strftime(bstack11lllll_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫࣀ"))
      hostname = socket.gethostname()
      bstack1l1l1l1l1l_opy_ = bstack11lllll_opy_ (u"ࠨࠩࣁ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11lllll_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫࣂ").format(bstack1l1lll1111_opy_, hostname, bstack1l1l1l1l1l_opy_)
      config[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣃ")][bstack11lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")] = identifier
    bstack1ll11111l_opy_ = config[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣅ")][bstack11lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")]
  return config
def bstack1ll11llll_opy_():
  bstack1l1l11ll11_opy_ =  bstack1llll1111l_opy_()[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭ࣇ")]
  return bstack1l1l11ll11_opy_ if bstack1l1l11ll11_opy_ else -1
def bstack1l1ll111l_opy_(bstack1l1l11ll11_opy_):
  global CONFIG
  if not bstack11lllll_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ") in CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")]:
    return
  CONFIG[bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")] = CONFIG[bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋")].replace(
    bstack11lllll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ࣌"),
    str(bstack1l1l11ll11_opy_)
  )
def bstack1111l1l1l_opy_():
  global CONFIG
  if not bstack11lllll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬ࣍") in CONFIG[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣎")]:
    return
  bstack111l11lll_opy_ = datetime.datetime.now()
  bstack1l1lll1111_opy_ = bstack111l11lll_opy_.strftime(bstack11lllll_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࣏࠭"))
  CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")] = CONFIG[bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")].replace(
    bstack11lllll_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿ࣒ࠪ"),
    bstack1l1lll1111_opy_
  )
def bstack1lll11lll1_opy_():
  global CONFIG
  if bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ") in CONFIG and not bool(CONFIG[bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]):
    del CONFIG[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ")]
    return
  if not bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ") in CONFIG:
    CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣗ")] = bstack11lllll_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣘ")
  if bstack11lllll_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪࣙ") in CONFIG[bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    bstack1111l1l1l_opy_()
    os.environ[bstack11lllll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪࣛ")] = CONFIG[bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣜ")]
  if not bstack11lllll_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣝ") in CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣞ")]:
    return
  bstack1l1l11ll11_opy_ = bstack11lllll_opy_ (u"ࠪࠫࣟ")
  bstack1lll1111l1_opy_ = bstack1ll11llll_opy_()
  if bstack1lll1111l1_opy_ != -1:
    bstack1l1l11ll11_opy_ = bstack11lllll_opy_ (u"ࠫࡈࡏࠠࠨ࣠") + str(bstack1lll1111l1_opy_)
  if bstack1l1l11ll11_opy_ == bstack11lllll_opy_ (u"ࠬ࠭࣡"):
    bstack1l11ll1ll_opy_ = bstack11ll1l11_opy_(CONFIG[bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࣢")])
    if bstack1l11ll1ll_opy_ != -1:
      bstack1l1l11ll11_opy_ = str(bstack1l11ll1ll_opy_)
  if bstack1l1l11ll11_opy_:
    bstack1l1ll111l_opy_(bstack1l1l11ll11_opy_)
    os.environ[bstack11lllll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࣣࠫ")] = CONFIG[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")]
def bstack1ll1l11ll1_opy_(bstack1lll1ll111_opy_, bstack111ll11l_opy_, path):
  bstack1ll1l11l_opy_ = {
    bstack11lllll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣥ"): bstack111ll11l_opy_
  }
  if os.path.exists(path):
    bstack11l1l1l1l_opy_ = json.load(open(path, bstack11lllll_opy_ (u"ࠪࡶࡧࣦ࠭")))
  else:
    bstack11l1l1l1l_opy_ = {}
  bstack11l1l1l1l_opy_[bstack1lll1ll111_opy_] = bstack1ll1l11l_opy_
  with open(path, bstack11lllll_opy_ (u"ࠦࡼ࠱ࠢࣧ")) as outfile:
    json.dump(bstack11l1l1l1l_opy_, outfile)
def bstack11ll1l11_opy_(bstack1lll1ll111_opy_):
  bstack1lll1ll111_opy_ = str(bstack1lll1ll111_opy_)
  bstack11ll11111_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠬࢄࠧࣨ")), bstack11lllll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࣩ࠭"))
  try:
    if not os.path.exists(bstack11ll11111_opy_):
      os.makedirs(bstack11ll11111_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠧࡿࠩ࣪")), bstack11lllll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ࣫"), bstack11lllll_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ࣬"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11lllll_opy_ (u"ࠪࡻ࣭ࠬ")):
        pass
      with open(file_path, bstack11lllll_opy_ (u"ࠦࡼ࠱࣮ࠢ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11lllll_opy_ (u"ࠬࡸ࣯ࠧ")) as bstack1l1lll111_opy_:
      bstack11ll111l1_opy_ = json.load(bstack1l1lll111_opy_)
    if bstack1lll1ll111_opy_ in bstack11ll111l1_opy_:
      bstack1l1lllll1l_opy_ = bstack11ll111l1_opy_[bstack1lll1ll111_opy_][bstack11lllll_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣰࠪ")]
      bstack1l111l11_opy_ = int(bstack1l1lllll1l_opy_) + 1
      bstack1ll1l11ll1_opy_(bstack1lll1ll111_opy_, bstack1l111l11_opy_, file_path)
      return bstack1l111l11_opy_
    else:
      bstack1ll1l11ll1_opy_(bstack1lll1ll111_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack111l1111l_opy_.format(str(e)))
    return -1
def bstack1l1l11lll_opy_(config):
  if not config[bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࣱࠩ")] or not config[bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࣲࠫ")]:
    return True
  else:
    return False
def bstack111l1ll11_opy_(config, index=0):
  global bstack1ll11ll11_opy_
  bstack1l11111l1_opy_ = {}
  caps = bstack11111lll1_opy_ + bstack11l11l1l_opy_
  if bstack1ll11ll11_opy_:
    caps += bstack11l1l111l_opy_
  for key in config:
    if key in caps + [bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ")]:
      continue
    bstack1l11111l1_opy_[key] = config[key]
  if bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ") in config:
    for bstack1lll11ll1_opy_ in config[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index]:
      if bstack1lll11ll1_opy_ in caps + [bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࣶࠪ"), bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣷ")]:
        continue
      bstack1l11111l1_opy_[bstack1lll11ll1_opy_] = config[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ")][index][bstack1lll11ll1_opy_]
  bstack1l11111l1_opy_[bstack11lllll_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࣹࠪ")] = socket.gethostname()
  if bstack11lllll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࣺࠪ") in bstack1l11111l1_opy_:
    del (bstack1l11111l1_opy_[bstack11lllll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫࣻ")])
  return bstack1l11111l1_opy_
def bstack11ll1l1l1_opy_(config):
  global bstack1ll11ll11_opy_
  bstack1l1llllll_opy_ = {}
  caps = bstack11l11l1l_opy_
  if bstack1ll11ll11_opy_:
    caps += bstack11l1l111l_opy_
  for key in caps:
    if key in config:
      bstack1l1llllll_opy_[key] = config[key]
  return bstack1l1llllll_opy_
def bstack1l1llll111_opy_(bstack1l11111l1_opy_, bstack1l1llllll_opy_):
  bstack11lll1ll_opy_ = {}
  for key in bstack1l11111l1_opy_.keys():
    if key in bstack1l1l1llll_opy_:
      bstack11lll1ll_opy_[bstack1l1l1llll_opy_[key]] = bstack1l11111l1_opy_[key]
    else:
      bstack11lll1ll_opy_[key] = bstack1l11111l1_opy_[key]
  for key in bstack1l1llllll_opy_:
    if key in bstack1l1l1llll_opy_:
      bstack11lll1ll_opy_[bstack1l1l1llll_opy_[key]] = bstack1l1llllll_opy_[key]
    else:
      bstack11lll1ll_opy_[key] = bstack1l1llllll_opy_[key]
  return bstack11lll1ll_opy_
def bstack1l11111ll_opy_(config, index=0):
  global bstack1ll11ll11_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1l1llllll_opy_ = bstack11ll1l1l1_opy_(config)
  bstack1l1ll1111l_opy_ = bstack11l11l1l_opy_
  bstack1l1ll1111l_opy_ += bstack111l1l11_opy_
  if bstack1ll11ll11_opy_:
    bstack1l1ll1111l_opy_ += bstack11l1l111l_opy_
  if bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ") in config:
    if bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ") in config[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣾ")][index]:
      caps[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬࣿ")] = config[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index][bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧँ")]
    if bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं") in config[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
      caps[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऄ")] = str(config[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨआ")])
    bstack1l11l111_opy_ = {}
    for bstack1ll1l111_opy_ in bstack1l1ll1111l_opy_:
      if bstack1ll1l111_opy_ in config[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index]:
        if bstack1ll1l111_opy_ == bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫई"):
          try:
            bstack1l11l111_opy_[bstack1ll1l111_opy_] = str(config[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1ll1l111_opy_] * 1.0)
          except:
            bstack1l11l111_opy_[bstack1ll1l111_opy_] = str(config[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1ll1l111_opy_])
        else:
          bstack1l11l111_opy_[bstack1ll1l111_opy_] = config[bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऋ")][index][bstack1ll1l111_opy_]
        del (config[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩऌ")][index][bstack1ll1l111_opy_])
    bstack1l1llllll_opy_ = update(bstack1l1llllll_opy_, bstack1l11l111_opy_)
  bstack1l11111l1_opy_ = bstack111l1ll11_opy_(config, index)
  for bstack1ll1l11lll_opy_ in bstack11l11l1l_opy_ + [bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऍ"), bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऎ")]:
    if bstack1ll1l11lll_opy_ in bstack1l11111l1_opy_:
      bstack1l1llllll_opy_[bstack1ll1l11lll_opy_] = bstack1l11111l1_opy_[bstack1ll1l11lll_opy_]
      del (bstack1l11111l1_opy_[bstack1ll1l11lll_opy_])
  if bstack1l1l11l11l_opy_(config):
    bstack1l11111l1_opy_[bstack11lllll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩए")] = True
    caps.update(bstack1l1llllll_opy_)
    caps[bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫऐ")] = bstack1l11111l1_opy_
  else:
    bstack1l11111l1_opy_[bstack11lllll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫऑ")] = False
    caps.update(bstack1l1llll111_opy_(bstack1l11111l1_opy_, bstack1l1llllll_opy_))
    if bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ") in caps:
      caps[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧओ")] = caps[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऔ")]
      del (caps[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭क")])
    if bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख") in caps:
      caps[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬग")] = caps[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬघ")]
      del (caps[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ङ")])
  return caps
def bstack1l111ll1_opy_():
  global bstack111ll1l1_opy_
  if bstack1l1l11lll1_opy_() <= version.parse(bstack11lllll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭च")):
    if bstack111ll1l1_opy_ != bstack11lllll_opy_ (u"ࠧࠨछ"):
      return bstack11lllll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤज") + bstack111ll1l1_opy_ + bstack11lllll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨझ")
    return bstack11111llll_opy_
  if bstack111ll1l1_opy_ != bstack11lllll_opy_ (u"ࠪࠫञ"):
    return bstack11lllll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨट") + bstack111ll1l1_opy_ + bstack11lllll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨठ")
  return bstack1l1l11llll_opy_
def bstack1l1ll111ll_opy_(options):
  return hasattr(options, bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧड"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111l1111_opy_(options, bstack111l1ll1_opy_):
  for bstack11l11ll1_opy_ in bstack111l1ll1_opy_:
    if bstack11l11ll1_opy_ in [bstack11lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬढ"), bstack11lllll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण")]:
      continue
    if bstack11l11ll1_opy_ in options._experimental_options:
      options._experimental_options[bstack11l11ll1_opy_] = update(options._experimental_options[bstack11l11ll1_opy_],
                                                         bstack111l1ll1_opy_[bstack11l11ll1_opy_])
    else:
      options.add_experimental_option(bstack11l11ll1_opy_, bstack111l1ll1_opy_[bstack11l11ll1_opy_])
  if bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत") in bstack111l1ll1_opy_:
    for arg in bstack111l1ll1_opy_[bstack11lllll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨथ")]:
      options.add_argument(arg)
    del (bstack111l1ll1_opy_[bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡴࠩद")])
  if bstack11lllll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध") in bstack111l1ll1_opy_:
    for ext in bstack111l1ll1_opy_[bstack11lllll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪन")]:
      options.add_extension(ext)
    del (bstack111l1ll1_opy_[bstack11lllll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫऩ")])
def bstack1ll1ll1l_opy_(options, bstack11l111ll_opy_):
  if bstack11lllll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप") in bstack11l111ll_opy_:
    for bstack1l1llll11_opy_ in bstack11l111ll_opy_[bstack11lllll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")]:
      if bstack1l1llll11_opy_ in options._preferences:
        options._preferences[bstack1l1llll11_opy_] = update(options._preferences[bstack1l1llll11_opy_], bstack11l111ll_opy_[bstack11lllll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩब")][bstack1l1llll11_opy_])
      else:
        options.set_preference(bstack1l1llll11_opy_, bstack11l111ll_opy_[bstack11lllll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪभ")][bstack1l1llll11_opy_])
  if bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡵࠪम") in bstack11l111ll_opy_:
    for arg in bstack11l111ll_opy_[bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      options.add_argument(arg)
def bstack1lll1111ll_opy_(options, bstack1ll111lll1_opy_):
  if bstack11lllll_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨर") in bstack1ll111lll1_opy_:
    options.use_webview(bool(bstack1ll111lll1_opy_[bstack11lllll_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩऱ")]))
  bstack111l1111_opy_(options, bstack1ll111lll1_opy_)
def bstack111lllll_opy_(options, bstack1l11l11ll_opy_):
  for bstack111lll1l1_opy_ in bstack1l11l11ll_opy_:
    if bstack111lll1l1_opy_ in [bstack11lllll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल"), bstack11lllll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ")]:
      continue
    options.set_capability(bstack111lll1l1_opy_, bstack1l11l11ll_opy_[bstack111lll1l1_opy_])
  if bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡴࠩऴ") in bstack1l11l11ll_opy_:
    for arg in bstack1l11l11ll_opy_[bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      options.add_argument(arg)
  if bstack11lllll_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪश") in bstack1l11l11ll_opy_:
    options.bstack111l111l1_opy_(bool(bstack1l11l11ll_opy_[bstack11lllll_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫष")]))
def bstack1ll1111l_opy_(options, bstack1ll11lll1_opy_):
  for bstack1ll11l1ll_opy_ in bstack1ll11lll1_opy_:
    if bstack1ll11l1ll_opy_ in [bstack11lllll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस"), bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह")]:
      continue
    options._options[bstack1ll11l1ll_opy_] = bstack1ll11lll1_opy_[bstack1ll11l1ll_opy_]
  if bstack11lllll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ") in bstack1ll11lll1_opy_:
    for bstack1l11lll1_opy_ in bstack1ll11lll1_opy_[bstack11lllll_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऻ")]:
      options.bstack1ll1l11111_opy_(
        bstack1l11lll1_opy_, bstack1ll11lll1_opy_[bstack11lllll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")][bstack1l11lll1_opy_])
  if bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡶࠫऽ") in bstack1ll11lll1_opy_:
    for arg in bstack1ll11lll1_opy_[bstack11lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬा")]:
      options.add_argument(arg)
def bstack111l1l1l_opy_(options, caps):
  if not hasattr(options, bstack11lllll_opy_ (u"ࠨࡍࡈ࡝ࠬि")):
    return
  if options.KEY == bstack11lllll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧी") and options.KEY in caps:
    bstack111l1111_opy_(options, caps[bstack11lllll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨु")])
  elif options.KEY == bstack11lllll_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩू") and options.KEY in caps:
    bstack1ll1ll1l_opy_(options, caps[bstack11lllll_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪृ")])
  elif options.KEY == bstack11lllll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧॄ") and options.KEY in caps:
    bstack111lllll_opy_(options, caps[bstack11lllll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨॅ")])
  elif options.KEY == bstack11lllll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॆ") and options.KEY in caps:
    bstack1lll1111ll_opy_(options, caps[bstack11lllll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪे")])
  elif options.KEY == bstack11lllll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩै") and options.KEY in caps:
    bstack1ll1111l_opy_(options, caps[bstack11lllll_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪॉ")])
def bstack1111l11l1_opy_(caps):
  global bstack1ll11ll11_opy_
  if isinstance(os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ॊ")), str):
    bstack1ll11ll11_opy_ = eval(os.getenv(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧो")))
  if bstack1ll11ll11_opy_:
    if bstack1l1ll1l1l1_opy_() < version.parse(bstack11lllll_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ौ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11lllll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ्")
    if bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ") in caps:
      browser = caps[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॏ")]
    elif bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬॐ") in caps:
      browser = caps[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭॑")]
    browser = str(browser).lower()
    if browser == bstack11lllll_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ॒࠭") or browser == bstack11lllll_opy_ (u"ࠧࡪࡲࡤࡨࠬ॓"):
      browser = bstack11lllll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ॔")
    if browser == bstack11lllll_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪॕ"):
      browser = bstack11lllll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪॖ")
    if browser not in [bstack11lllll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॗ"), bstack11lllll_opy_ (u"ࠬ࡫ࡤࡨࡧࠪक़"), bstack11lllll_opy_ (u"࠭ࡩࡦࠩख़"), bstack11lllll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧग़"), bstack11lllll_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩज़")]:
      return None
    try:
      package = bstack11lllll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫड़").format(browser)
      name = bstack11lllll_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫढ़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1ll111ll_opy_(options):
        return None
      for bstack1ll1l11lll_opy_ in caps.keys():
        options.set_capability(bstack1ll1l11lll_opy_, caps[bstack1ll1l11lll_opy_])
      bstack111l1l1l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1l1l1l11_opy_(options, bstack1l1lll1ll_opy_):
  if not bstack1l1ll111ll_opy_(options):
    return
  for bstack1ll1l11lll_opy_ in bstack1l1lll1ll_opy_.keys():
    if bstack1ll1l11lll_opy_ in bstack111l1l11_opy_:
      continue
    if bstack1ll1l11lll_opy_ in options._caps and type(options._caps[bstack1ll1l11lll_opy_]) in [dict, list]:
      options._caps[bstack1ll1l11lll_opy_] = update(options._caps[bstack1ll1l11lll_opy_], bstack1l1lll1ll_opy_[bstack1ll1l11lll_opy_])
    else:
      options.set_capability(bstack1ll1l11lll_opy_, bstack1l1lll1ll_opy_[bstack1ll1l11lll_opy_])
  bstack111l1l1l_opy_(options, bstack1l1lll1ll_opy_)
  if bstack11lllll_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़") in options._caps:
    if options._caps[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")] and options._caps[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")].lower() != bstack11lllll_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨॡ"):
      del options._caps[bstack11lllll_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧॢ")]
def bstack1ll111l1_opy_(proxy_config):
  if bstack11lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ") in proxy_config:
    proxy_config[bstack11lllll_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ।")] = proxy_config[bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ॥")]
    del (proxy_config[bstack11lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ०")])
  if bstack11lllll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१") in proxy_config and proxy_config[bstack11lllll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ२")].lower() != bstack11lllll_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ३"):
    proxy_config[bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack11lllll_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪ५")
  if bstack11lllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩ६") in proxy_config:
    proxy_config[bstack11lllll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ७")] = bstack11lllll_opy_ (u"࠭ࡰࡢࡥࠪ८")
  return proxy_config
def bstack1llll11lll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11lllll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९") in config:
    return proxy
  config[bstack11lllll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")] = bstack1ll111l1_opy_(config[bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨॱ")])
  if proxy == None:
    proxy = Proxy(config[bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩॲ")])
  return proxy
def bstack1l11l1ll_opy_(self):
  global CONFIG
  global bstack1llllll11l_opy_
  try:
    proxy = bstack1l1ll11l1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11lllll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॳ")):
        proxies = bstack1ll111111_opy_(proxy, bstack1l111ll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1ll11ll_opy_ = proxies.popitem()
          if bstack11lllll_opy_ (u"ࠧࡀ࠯࠰ࠤॴ") in bstack1l1ll11ll_opy_:
            return bstack1l1ll11ll_opy_
          else:
            return bstack11lllll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢॵ") + bstack1l1ll11ll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦॶ").format(str(e)))
  return bstack1llllll11l_opy_(self)
def bstack1l1ll11111_opy_():
  global CONFIG
  return bstack1lll1l111_opy_(CONFIG) and bstack1111l1lll_opy_() and bstack1l1l11lll1_opy_() >= version.parse(bstack1111ll11_opy_)
def bstack1lllll1l1l_opy_():
  global CONFIG
  return (bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫॷ") in CONFIG or bstack11lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॸ") in CONFIG) and bstack111lll11l_opy_()
def bstack111111111_opy_(config):
  bstack1111l1111_opy_ = {}
  if bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॹ") in config:
    bstack1111l1111_opy_ = config[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॺ")]
  if bstack11lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॻ") in config:
    bstack1111l1111_opy_ = config[bstack11lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॼ")]
  proxy = bstack1l1ll11l1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack11lllll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬॽ")) and os.path.isfile(proxy):
      bstack1111l1111_opy_[bstack11lllll_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫॾ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11lllll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧॿ")):
        proxies = bstack11lllllll_opy_(config, bstack1l111ll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1ll11ll_opy_ = proxies.popitem()
          if bstack11lllll_opy_ (u"ࠥ࠾࠴࠵ࠢঀ") in bstack1l1ll11ll_opy_:
            parsed_url = urlparse(bstack1l1ll11ll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11lllll_opy_ (u"ࠦ࠿࠵࠯ࠣঁ") + bstack1l1ll11ll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1111l1111_opy_[bstack11lllll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨং")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1111l1111_opy_[bstack11lllll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩঃ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1111l1111_opy_[bstack11lllll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ঄")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1111l1111_opy_[bstack11lllll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫঅ")] = str(parsed_url.password)
  return bstack1111l1111_opy_
def bstack11l11l11l_opy_(config):
  if bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧআ") in config:
    return config[bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨই")]
  return {}
def bstack11l1ll1ll_opy_(caps):
  global bstack1ll11111l_opy_
  if bstack11lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ") in caps:
    caps[bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭উ")][bstack11lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬঊ")] = True
    if bstack1ll11111l_opy_:
      caps[bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨঋ")][bstack11lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঌ")] = bstack1ll11111l_opy_
  else:
    caps[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ঍")] = True
    if bstack1ll11111l_opy_:
      caps[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ঎")] = bstack1ll11111l_opy_
def bstack111l111ll_opy_():
  global CONFIG
  if bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨএ") in CONFIG and bstack11l1l11l1_opy_(CONFIG[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঐ")]):
    bstack1111l1111_opy_ = bstack111111111_opy_(CONFIG)
    bstack1lll1l1ll1_opy_(CONFIG[bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1111l1111_opy_)
def bstack1lll1l1ll1_opy_(key, bstack1111l1111_opy_):
  global bstack1l11ll1l1_opy_
  logger.info(bstack1ll1l1ll11_opy_)
  try:
    bstack1l11ll1l1_opy_ = Local()
    bstack1111111ll_opy_ = {bstack11lllll_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1111111ll_opy_.update(bstack1111l1111_opy_)
    logger.debug(bstack1l11lll11_opy_.format(str(bstack1111111ll_opy_)))
    bstack1l11ll1l1_opy_.start(**bstack1111111ll_opy_)
    if bstack1l11ll1l1_opy_.isRunning():
      logger.info(bstack1llllll1l_opy_)
  except Exception as e:
    bstack1l11lllll_opy_(bstack1l11l1lll_opy_.format(str(e)))
def bstack1lll111ll1_opy_():
  global bstack1l11ll1l1_opy_
  if bstack1l11ll1l1_opy_.isRunning():
    logger.info(bstack111llll11_opy_)
    bstack1l11ll1l1_opy_.stop()
  bstack1l11ll1l1_opy_ = None
def bstack1llll11l_opy_(bstack1l1ll1ll1_opy_=[]):
  global CONFIG
  bstack1111l1ll1_opy_ = []
  bstack111l1l11l_opy_ = [bstack11lllll_opy_ (u"ࠨࡱࡶࠫও"), bstack11lllll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack11lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack1l1ll1ll1_opy_:
      bstack1lll1lll1l_opy_ = {}
      for k in bstack111l1l11l_opy_:
        val = CONFIG[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack11lllll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1lll1lll1l_opy_[k] = val
      if(err[bstack11lllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack11lllll_opy_ (u"ࠪࠫজ")):
        bstack1lll1lll1l_opy_[bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack11lllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack1111l1ll1_opy_.append(bstack1lll1lll1l_opy_)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack1111l1ll1_opy_
def bstack1l1l11l11_opy_(file_name):
  bstack1lll1ll1ll_opy_ = []
  try:
    bstack1lllll111l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1lllll111l_opy_):
      with open(bstack1lllll111l_opy_) as f:
        bstack111l11l1l_opy_ = json.load(f)
        bstack1lll1ll1ll_opy_ = bstack111l11l1l_opy_
      os.remove(bstack1lllll111l_opy_)
    return bstack1lll1ll1ll_opy_
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
def bstack11ll11l11_opy_():
  global bstack1111l111_opy_
  global bstack1lll11l1ll_opy_
  global bstack1lllll11ll_opy_
  global bstack11llll1l_opy_
  global bstack1llll1ll1_opy_
  global bstack11l1l1l1_opy_
  percy.shutdown()
  bstack1ll11ll1ll_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1ll11ll1ll_opy_ in [bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack11lllll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1llll111l1_opy_()
  if bstack1111l111_opy_:
    logger.warning(bstack1ll1lll11_opy_.format(str(bstack1111l111_opy_)))
  else:
    try:
      bstack11l1l1l1l_opy_ = bstack1ll11l1l1_opy_(bstack11lllll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack11l1l1l1l_opy_.get(bstack11lllll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack11l1l1l1l_opy_.get(bstack11lllll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack11lllll_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1ll1lll11_opy_.format(str(bstack11l1l1l1l_opy_[bstack11lllll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack11lllll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1ll11l11_opy_)
  global bstack1l11ll1l1_opy_
  if bstack1l11ll1l1_opy_:
    bstack1lll111ll1_opy_()
  try:
    for driver in bstack1lll11l1ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1lllll1lll_opy_)
  if bstack11l1l1l1_opy_ == bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack1llll1ll1_opy_ = bstack1l1l11l11_opy_(bstack11lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack11l1l1l1_opy_ == bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack11llll1l_opy_) == 0:
    bstack11llll1l_opy_ = bstack1l1l11l11_opy_(bstack11lllll_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack11llll1l_opy_) == 0:
      bstack11llll1l_opy_ = bstack1l1l11l11_opy_(bstack11lllll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1llll1ll11_opy_ = bstack11lllll_opy_ (u"ࠩࠪর")
  if len(bstack1lllll11ll_opy_) > 0:
    bstack1llll1ll11_opy_ = bstack1llll11l_opy_(bstack1lllll11ll_opy_)
  elif len(bstack11llll1l_opy_) > 0:
    bstack1llll1ll11_opy_ = bstack1llll11l_opy_(bstack11llll1l_opy_)
  elif len(bstack1llll1ll1_opy_) > 0:
    bstack1llll1ll11_opy_ = bstack1llll11l_opy_(bstack1llll1ll1_opy_)
  elif len(bstack1ll1l1ll1l_opy_) > 0:
    bstack1llll1ll11_opy_ = bstack1llll11l_opy_(bstack1ll1l1ll1l_opy_)
  if bool(bstack1llll1ll11_opy_):
    bstack11ll111ll_opy_(bstack1llll1ll11_opy_)
  else:
    bstack11ll111ll_opy_()
  bstack11lll1ll1_opy_(bstack1l1l111l1_opy_, logger)
def bstack111llllll_opy_(self, *args):
  logger.error(bstack1l1111ll_opy_)
  bstack11ll11l11_opy_()
  sys.exit(1)
def bstack1l11lllll_opy_(err):
  logger.critical(bstack1l11ll1l_opy_.format(str(err)))
  bstack11ll111ll_opy_(bstack1l11ll1l_opy_.format(str(err)), True)
  atexit.unregister(bstack11ll11l11_opy_)
  bstack1llll111l1_opy_()
  sys.exit(1)
def bstack1ll111llll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11ll111ll_opy_(message, True)
  atexit.unregister(bstack11ll11l11_opy_)
  bstack1llll111l1_opy_()
  sys.exit(1)
def bstack1l11l1111_opy_():
  global CONFIG
  global bstack11ll1llll_opy_
  global bstack1ll111l1l1_opy_
  global bstack1l1l111l_opy_
  CONFIG = bstack11lll1l1_opy_()
  bstack1ll1ll11l_opy_()
  bstack1111ll1l_opy_()
  CONFIG = bstack1l111111_opy_(CONFIG)
  update(CONFIG, bstack1ll111l1l1_opy_)
  update(CONFIG, bstack11ll1llll_opy_)
  CONFIG = bstack11l1lllll_opy_(CONFIG)
  bstack1l1l111l_opy_ = bstack1111lll11_opy_(CONFIG)
  bstack1lll11111_opy_.bstack1lll11l1l1_opy_(bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ঱"), bstack1l1l111l_opy_)
  if (bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") in bstack11ll1llll_opy_) or (
          bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঴") in CONFIG and bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ঵") not in bstack1ll111l1l1_opy_):
    if os.getenv(bstack11lllll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ")):
      CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫষ")] = os.getenv(bstack11lllll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧস"))
    else:
      bstack1lll11lll1_opy_()
  elif (bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") not in CONFIG and bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঺") in CONFIG) or (
          bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঻") in bstack1ll111l1l1_opy_ and bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") not in bstack11ll1llll_opy_):
    del (CONFIG[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঽ")])
  if bstack1l1l11lll_opy_(CONFIG):
    bstack1l11lllll_opy_(bstack111l1ll1l_opy_)
  bstack1llllll11_opy_()
  bstack1llll1llll_opy_()
  if bstack1ll11ll11_opy_:
    CONFIG[bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࠭া")] = bstack11l1ll1l1_opy_(CONFIG)
    logger.info(bstack1llll1l1l_opy_.format(CONFIG[bstack11lllll_opy_ (u"ࠪࡥࡵࡶࠧি")]))
def bstack11l1111l1_opy_(config, bstack11lll111l_opy_):
  global CONFIG
  global bstack1ll11ll11_opy_
  CONFIG = config
  bstack1ll11ll11_opy_ = bstack11lll111l_opy_
def bstack1llll1llll_opy_():
  global CONFIG
  global bstack1ll11ll11_opy_
  if bstack11lllll_opy_ (u"ࠫࡦࡶࡰࠨী") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll111llll_opy_(e, bstack1ll1lll1ll_opy_)
    bstack1ll11ll11_opy_ = True
    bstack1lll11111_opy_.bstack1lll11l1l1_opy_(bstack11lllll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫু"), True)
def bstack11l1ll1l1_opy_(config):
  bstack11lll1lll_opy_ = bstack11lllll_opy_ (u"࠭ࠧূ")
  app = config[bstack11lllll_opy_ (u"ࠧࡢࡲࡳࠫৃ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack111l11l1_opy_:
      if os.path.exists(app):
        bstack11lll1lll_opy_ = bstack111ll1111_opy_(config, app)
      elif bstack111ll111l_opy_(app):
        bstack11lll1lll_opy_ = app
      else:
        bstack1l11lllll_opy_(bstack1l1l1lll_opy_.format(app))
    else:
      if bstack111ll111l_opy_(app):
        bstack11lll1lll_opy_ = app
      elif os.path.exists(app):
        bstack11lll1lll_opy_ = bstack111ll1111_opy_(app)
      else:
        bstack1l11lllll_opy_(bstack111ll1ll1_opy_)
  else:
    if len(app) > 2:
      bstack1l11lllll_opy_(bstack1llllll111_opy_)
    elif len(app) == 2:
      if bstack11lllll_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৄ") in app and bstack11lllll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৅") in app:
        if os.path.exists(app[bstack11lllll_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆")]):
          bstack11lll1lll_opy_ = bstack111ll1111_opy_(config, app[bstack11lllll_opy_ (u"ࠫࡵࡧࡴࡩࠩে")], app[bstack11lllll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨৈ")])
        else:
          bstack1l11lllll_opy_(bstack1l1l1lll_opy_.format(app))
      else:
        bstack1l11lllll_opy_(bstack1llllll111_opy_)
    else:
      for key in app:
        if key in bstack1lll1ll1l1_opy_:
          if key == bstack11lllll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ৉"):
            if os.path.exists(app[key]):
              bstack11lll1lll_opy_ = bstack111ll1111_opy_(config, app[key])
            else:
              bstack1l11lllll_opy_(bstack1l1l1lll_opy_.format(app))
          else:
            bstack11lll1lll_opy_ = app[key]
        else:
          bstack1l11lllll_opy_(bstack11llll11l_opy_)
  return bstack11lll1lll_opy_
def bstack111ll111l_opy_(bstack11lll1lll_opy_):
  import re
  bstack1111111l_opy_ = re.compile(bstack11lllll_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ৊"))
  bstack1lllll1ll_opy_ = re.compile(bstack11lllll_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧো"))
  if bstack11lllll_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨৌ") in bstack11lll1lll_opy_ or re.fullmatch(bstack1111111l_opy_, bstack11lll1lll_opy_) or re.fullmatch(bstack1lllll1ll_opy_, bstack11lll1lll_opy_):
    return True
  else:
    return False
def bstack111ll1111_opy_(config, path, bstack1l1l11l1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11lllll_opy_ (u"ࠪࡶࡧ্࠭")).read()).hexdigest()
  bstack1lllll11l1_opy_ = bstack1l111l1ll_opy_(md5_hash)
  bstack11lll1lll_opy_ = None
  if bstack1lllll11l1_opy_:
    logger.info(bstack1lll1111l_opy_.format(bstack1lllll11l1_opy_, md5_hash))
    return bstack1lllll11l1_opy_
  bstack1l1ll1ll1l_opy_ = MultipartEncoder(
    fields={
      bstack11lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࠩৎ"): (os.path.basename(path), open(os.path.abspath(path), bstack11lllll_opy_ (u"ࠬࡸࡢࠨ৏")), bstack11lllll_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ৐")),
      bstack11lllll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ৑"): bstack1l1l11l1l_opy_
    }
  )
  response = requests.post(bstack1l11l1l11_opy_, data=bstack1l1ll1ll1l_opy_,
                           headers={bstack11lllll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ৒"): bstack1l1ll1ll1l_opy_.content_type},
                           auth=(config[bstack11lllll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ৓")], config[bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭৔")]))
  try:
    res = json.loads(response.text)
    bstack11lll1lll_opy_ = res[bstack11lllll_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ৕")]
    logger.info(bstack1ll1ll11l1_opy_.format(bstack11lll1lll_opy_))
    bstack1l1lll11l_opy_(md5_hash, bstack11lll1lll_opy_)
  except ValueError as err:
    bstack1l11lllll_opy_(bstack1l11111l_opy_.format(str(err)))
  return bstack11lll1lll_opy_
def bstack1llllll11_opy_():
  global CONFIG
  global bstack1llll1l11l_opy_
  bstack11lll11l1_opy_ = 0
  bstack1l1l1l11_opy_ = 1
  if bstack11lllll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ৖") in CONFIG:
    bstack1l1l1l11_opy_ = CONFIG[bstack11lllll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ৗ")]
  if bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৘") in CONFIG:
    bstack11lll11l1_opy_ = len(CONFIG[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ৙")])
  bstack1llll1l11l_opy_ = int(bstack1l1l1l11_opy_) * int(bstack11lll11l1_opy_)
def bstack1l111l1ll_opy_(md5_hash):
  bstack1lll11l1_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠩࢁࠫ৚")), bstack11lllll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ৛"), bstack11lllll_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬড়"))
  if os.path.exists(bstack1lll11l1_opy_):
    bstack1ll1ll1l11_opy_ = json.load(open(bstack1lll11l1_opy_, bstack11lllll_opy_ (u"ࠬࡸࡢࠨঢ়")))
    if md5_hash in bstack1ll1ll1l11_opy_:
      bstack1111l1ll_opy_ = bstack1ll1ll1l11_opy_[md5_hash]
      bstack1ll1l1111l_opy_ = datetime.datetime.now()
      bstack1lllllll1_opy_ = datetime.datetime.strptime(bstack1111l1ll_opy_[bstack11lllll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ৞")], bstack11lllll_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫয়"))
      if (bstack1ll1l1111l_opy_ - bstack1lllllll1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1111l1ll_opy_[bstack11lllll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ৠ")]):
        return None
      return bstack1111l1ll_opy_[bstack11lllll_opy_ (u"ࠩ࡬ࡨࠬৡ")]
  else:
    return None
def bstack1l1lll11l_opy_(md5_hash, bstack11lll1lll_opy_):
  bstack11ll11111_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠪࢂࠬৢ")), bstack11lllll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫৣ"))
  if not os.path.exists(bstack11ll11111_opy_):
    os.makedirs(bstack11ll11111_opy_)
  bstack1lll11l1_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠬࢄࠧ৤")), bstack11lllll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৥"), bstack11lllll_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ০"))
  bstack1l111ll1l_opy_ = {
    bstack11lllll_opy_ (u"ࠨ࡫ࡧࠫ১"): bstack11lll1lll_opy_,
    bstack11lllll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ২"): datetime.datetime.strftime(datetime.datetime.now(), bstack11lllll_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ৩")),
    bstack11lllll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ৪"): str(__version__)
  }
  if os.path.exists(bstack1lll11l1_opy_):
    bstack1ll1ll1l11_opy_ = json.load(open(bstack1lll11l1_opy_, bstack11lllll_opy_ (u"ࠬࡸࡢࠨ৫")))
  else:
    bstack1ll1ll1l11_opy_ = {}
  bstack1ll1ll1l11_opy_[md5_hash] = bstack1l111ll1l_opy_
  with open(bstack1lll11l1_opy_, bstack11lllll_opy_ (u"ࠨࡷࠬࠤ৬")) as outfile:
    json.dump(bstack1ll1ll1l11_opy_, outfile)
def bstack1llll1l111_opy_(self):
  return
def bstack1l11l1l1l_opy_(self):
  return
def bstack11ll1l1ll_opy_(self):
  global bstack1llll1ll1l_opy_
  bstack1llll1ll1l_opy_(self)
def bstack111l1l1ll_opy_():
  global bstack1lll1l1ll_opy_
  bstack1lll1l1ll_opy_ = True
def bstack11ll11ll_opy_(self):
  global bstack1l1ll1ll11_opy_
  global bstack1111l1l1_opy_
  global bstack1ll1lll111_opy_
  try:
    if bstack11lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ৭") in bstack1l1ll1ll11_opy_ and self.session_id != None and bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ৮"), bstack11lllll_opy_ (u"ࠩࠪ৯")) != bstack11lllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫৰ"):
      bstack11111l1l1_opy_ = bstack11lllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫৱ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৲")
      if bstack11111l1l1_opy_ == bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭৳"):
        bstack1l1ll1l1_opy_(logger)
      if self != None:
        bstack1lll1l11l1_opy_(self, bstack11111l1l1_opy_, bstack11lllll_opy_ (u"ࠧ࠭ࠢࠪ৴").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11lllll_opy_ (u"ࠨࠩ৵")
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ৶") + str(e))
  bstack1ll1lll111_opy_(self)
  self.session_id = None
def bstack1l1ll1l1l_opy_(self, command_executor=bstack11lllll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲࠵࠷࠽࠮࠱࠰࠳࠲࠶ࡀ࠴࠵࠶࠷ࠦ৷"), *args, **kwargs):
  bstack1ll11ll1_opy_ = bstack11l1ll1l_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack11lllll_opy_ (u"ࠫࡈࡵ࡭࡮ࡣࡱࡨࠥࡋࡸࡦࡥࡸࡸࡴࡸࠠࡸࡪࡨࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫ࡧ࡬ࡴࡧࠣ࠱ࠥࢁࡽࠨ৸").format(str(command_executor)))
    logger.debug(bstack11lllll_opy_ (u"ࠬࡎࡵࡣࠢࡘࡖࡑࠦࡩࡴࠢ࠰ࠤࢀࢃࠧ৹").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ৺") in command_executor._url:
      bstack1lll11111_opy_.bstack1lll11l1l1_opy_(bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ৻"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫৼ") in command_executor):
    bstack1lll11111_opy_.bstack1lll11l1l1_opy_(bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ৽"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1ll1llll1l_opy_.bstack111ll11l1_opy_(self)
  return bstack1ll11ll1_opy_
def bstack1ll1l1l1_opy_(self, driver_command, *args, **kwargs):
  global bstack11l111l1_opy_
  response = bstack11l111l1_opy_(self, driver_command, *args, **kwargs)
  try:
    if driver_command == bstack11lllll_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ৾"):
      bstack1ll1llll1l_opy_.bstack111l1lll1_opy_({
          bstack11lllll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ৿"): response[bstack11lllll_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ਀")],
          bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ਁ"): bstack1ll1llll1l_opy_.current_test_uuid() if bstack1ll1llll1l_opy_.current_test_uuid() else bstack1ll1llll1l_opy_.current_hook_uuid()
      })
  except:
    pass
  return response
def bstack1l11l111l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1111l1l1_opy_
  global bstack11l1lll1l_opy_
  global bstack11l1llll_opy_
  global bstack1ll1l11ll_opy_
  global bstack1ll1lll1l_opy_
  global bstack1l1ll1ll11_opy_
  global bstack11l1ll1l_opy_
  global bstack1lll11l1ll_opy_
  global bstack1l11llll1_opy_
  global bstack1l1l11l1l1_opy_
  CONFIG[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩਂ")] = str(bstack1l1ll1ll11_opy_) + str(__version__)
  command_executor = bstack1l111ll1_opy_()
  logger.debug(bstack1111llll_opy_.format(command_executor))
  proxy = bstack1llll11lll_opy_(CONFIG, proxy)
  bstack11lllll1l_opy_ = 0 if bstack11l1lll1l_opy_ < 0 else bstack11l1lll1l_opy_
  try:
    if bstack1ll1l11ll_opy_ is True:
      bstack11lllll1l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1ll1lll1l_opy_ is True:
      bstack11lllll1l_opy_ = int(threading.current_thread().name)
  except:
    bstack11lllll1l_opy_ = 0
  bstack1l1lll1ll_opy_ = bstack1l11111ll_opy_(CONFIG, bstack11lllll1l_opy_)
  logger.debug(bstack1llll11l1_opy_.format(str(bstack1l1lll1ll_opy_)))
  if bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਃ") in CONFIG and bstack11l1l11l1_opy_(CONFIG[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭਄")]):
    bstack11l1ll1ll_opy_(bstack1l1lll1ll_opy_)
  if desired_capabilities:
    bstack1llll111l_opy_ = bstack1l111111_opy_(desired_capabilities)
    bstack1llll111l_opy_[bstack11lllll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪਅ")] = bstack1l1l11l11l_opy_(CONFIG)
    bstack1l1111lll_opy_ = bstack1l11111ll_opy_(bstack1llll111l_opy_)
    if bstack1l1111lll_opy_:
      bstack1l1lll1ll_opy_ = update(bstack1l1111lll_opy_, bstack1l1lll1ll_opy_)
    desired_capabilities = None
  if options:
    bstack1l1l1l1l11_opy_(options, bstack1l1lll1ll_opy_)
  if not options:
    options = bstack1111l11l1_opy_(bstack1l1lll1ll_opy_)
  bstack1l1l11l1l1_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਆ"))[bstack11lllll1l_opy_]
  if bstack1111ll111_opy_.bstack1ll1ll1lll_opy_(CONFIG, bstack11lllll1l_opy_) and bstack1111ll111_opy_.bstack11111lll_opy_(bstack1l1lll1ll_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1111ll111_opy_.set_capabilities(bstack1l1lll1ll_opy_, CONFIG)
  if proxy and bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬਇ")):
    options.proxy(proxy)
  if options and bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਈ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1l11lll1_opy_() < version.parse(bstack11lllll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ਉ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l1lll1ll_opy_)
  logger.info(bstack1ll1l1l1l_opy_)
  if bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨਊ")):
    bstack11l1ll1l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ਋")):
    bstack11l1ll1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ਌")):
    bstack11l1ll1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11l1ll1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack11l1l11ll_opy_ = bstack11lllll_opy_ (u"ࠫࠬ਍")
    if bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭਎")):
      bstack11l1l11ll_opy_ = self.caps.get(bstack11lllll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਏ"))
    else:
      bstack11l1l11ll_opy_ = self.capabilities.get(bstack11lllll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢਐ"))
    if bstack11l1l11ll_opy_:
      bstack1ll1111ll_opy_(bstack11l1l11ll_opy_)
      if bstack1l1l11lll1_opy_() <= version.parse(bstack11lllll_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ਑")):
        self.command_executor._url = bstack11lllll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ਒") + bstack111ll1l1_opy_ + bstack11lllll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢਓ")
      else:
        self.command_executor._url = bstack11lllll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨਔ") + bstack11l1l11ll_opy_ + bstack11lllll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨਕ")
      logger.debug(bstack1l1111ll1_opy_.format(bstack11l1l11ll_opy_))
    else:
      logger.debug(bstack11ll1ll1l_opy_.format(bstack11lllll_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢਖ")))
  except Exception as e:
    logger.debug(bstack11ll1ll1l_opy_.format(e))
  if bstack11lllll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਗ") in bstack1l1ll1ll11_opy_:
    bstack111111ll_opy_(bstack11l1lll1l_opy_, bstack1l11llll1_opy_)
  bstack1111l1l1_opy_ = self.session_id
  if bstack11lllll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਘ") in bstack1l1ll1ll11_opy_ or bstack11lllll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩਙ") in bstack1l1ll1ll11_opy_ or bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਚ") in bstack1l1ll1ll11_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1ll1llll1l_opy_.bstack111ll11l1_opy_(self)
  bstack1lll11l1ll_opy_.append(self)
  if bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਛ") in CONFIG and bstack11lllll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਜ") in CONFIG[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਝ")][bstack11lllll1l_opy_]:
    bstack11l1llll_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਞ")][bstack11lllll1l_opy_][bstack11lllll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਟ")]
  logger.debug(bstack111ll11ll_opy_.format(bstack1111l1l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1lll111ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll1llll_opy_
      if(bstack11lllll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦਠ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠪࢂࠬਡ")), bstack11lllll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫਢ"), bstack11lllll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧਣ")), bstack11lllll_opy_ (u"࠭ࡷࠨਤ")) as fp:
          fp.write(bstack11lllll_opy_ (u"ࠢࠣਥ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11lllll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥਦ")))):
          with open(args[1], bstack11lllll_opy_ (u"ࠩࡵࠫਧ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11lllll_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩਨ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll1ll11_opy_)
            lines.insert(1, bstack1l1llllll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11lllll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਩")), bstack11lllll_opy_ (u"ࠬࡽࠧਪ")) as bstack1ll11111l1_opy_:
              bstack1ll11111l1_opy_.writelines(lines)
        CONFIG[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack1l1ll1ll11_opy_) + str(__version__)
        bstack11lllll1l_opy_ = 0 if bstack11l1lll1l_opy_ < 0 else bstack11l1lll1l_opy_
        try:
          if bstack1ll1l11ll_opy_ is True:
            bstack11lllll1l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1ll1lll1l_opy_ is True:
            bstack11lllll1l_opy_ = int(threading.current_thread().name)
        except:
          bstack11lllll1l_opy_ = 0
        CONFIG[bstack11lllll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢਬ")] = False
        CONFIG[bstack11lllll_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢਭ")] = True
        bstack1l1lll1ll_opy_ = bstack1l11111ll_opy_(CONFIG, bstack11lllll1l_opy_)
        logger.debug(bstack1llll11l1_opy_.format(str(bstack1l1lll1ll_opy_)))
        if CONFIG.get(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ਮ")):
          bstack11l1ll1ll_opy_(bstack1l1lll1ll_opy_)
        if bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ") in CONFIG and bstack11lllll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਰ") in CONFIG[bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਱")][bstack11lllll1l_opy_]:
          bstack11l1llll_opy_ = CONFIG[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਲ")][bstack11lllll1l_opy_][bstack11lllll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਲ਼")]
        args.append(os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠨࢀࠪ਴")), bstack11lllll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਵ"), bstack11lllll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬਸ਼")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l1lll1ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11lllll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਷"))
      bstack1ll1llll_opy_ = True
      return bstack1l1lll111l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll1l1l11_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11l1lll1l_opy_
    global bstack11l1llll_opy_
    global bstack1ll1l11ll_opy_
    global bstack1ll1lll1l_opy_
    global bstack1l1ll1ll11_opy_
    CONFIG[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਸ")] = str(bstack1l1ll1ll11_opy_) + str(__version__)
    bstack11lllll1l_opy_ = 0 if bstack11l1lll1l_opy_ < 0 else bstack11l1lll1l_opy_
    try:
      if bstack1ll1l11ll_opy_ is True:
        bstack11lllll1l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1ll1lll1l_opy_ is True:
        bstack11lllll1l_opy_ = int(threading.current_thread().name)
    except:
      bstack11lllll1l_opy_ = 0
    CONFIG[bstack11lllll_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧਹ")] = True
    bstack1l1lll1ll_opy_ = bstack1l11111ll_opy_(CONFIG, bstack11lllll1l_opy_)
    logger.debug(bstack1llll11l1_opy_.format(str(bstack1l1lll1ll_opy_)))
    if CONFIG.get(bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ਺")):
      bstack11l1ll1ll_opy_(bstack1l1lll1ll_opy_)
    if bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਻") in CONFIG and bstack11lllll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫਼ࠧ") in CONFIG[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack11lllll1l_opy_]:
      bstack11l1llll_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਾ")][bstack11lllll1l_opy_][bstack11lllll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਿ")]
    import urllib
    import json
    bstack111l11ll_opy_ = bstack11lllll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨੀ") + urllib.parse.quote(json.dumps(bstack1l1lll1ll_opy_))
    browser = self.connect(bstack111l11ll_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1l1l111_opy_():
    global bstack1ll1llll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1l1l11_opy_
        bstack1ll1llll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1lll111ll_opy_
      bstack1ll1llll_opy_ = True
    except Exception as e:
      pass
def bstack1l1ll1111_opy_(context, bstack1lll11ll1l_opy_):
  try:
    context.page.evaluate(bstack11lllll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣੁ"), bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬੂ")+ json.dumps(bstack1lll11ll1l_opy_) + bstack11lllll_opy_ (u"ࠤࢀࢁࠧ੃"))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣ੄"), e)
def bstack1ll11111ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11lllll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ੅"), bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ੆") + json.dumps(message) + bstack11lllll_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩੇ") + json.dumps(level) + bstack11lllll_opy_ (u"ࠧࡾࡿࠪੈ"))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦ੉"), e)
def bstack1l1l11ll_opy_(self, url):
  global bstack1l1l1l1ll_opy_
  try:
    bstack1llll1l1l1_opy_(url)
  except Exception as err:
    logger.debug(bstack1lll1lll_opy_.format(str(err)))
  try:
    bstack1l1l1l1ll_opy_(self, url)
  except Exception as e:
    try:
      bstack1llll1111_opy_ = str(e)
      if any(err_msg in bstack1llll1111_opy_ for err_msg in bstack111lll1ll_opy_):
        bstack1llll1l1l1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1lll1lll_opy_.format(str(err)))
    raise e
def bstack1lll1lll11_opy_(self):
  global bstack111ll1l11_opy_
  bstack111ll1l11_opy_ = self
  return
def bstack11lll1l1l_opy_(self):
  global bstack1l1ll111_opy_
  bstack1l1ll111_opy_ = self
  return
def bstack1ll111l1ll_opy_(self, test):
  global CONFIG
  global bstack11111l11_opy_
  if CONFIG.get(bstack11lllll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ੊"), False):
    test_name = str(test.data)
    bstack11l1ll111_opy_ = str(test.source)
    bstack1l111ll11_opy_ = os.path.relpath(bstack11l1ll111_opy_, start=os.getcwd())
    suite_name, bstack1l1l1lll1l_opy_ = os.path.splitext(bstack1l111ll11_opy_)
    bstack1l11l11l1_opy_ = suite_name + bstack11lllll_opy_ (u"ࠥ࠱ࠧੋ") + test_name
    threading.current_thread().percySessionName = bstack1l11l11l1_opy_
  bstack11111l11_opy_(self, test)
def bstack1ll1111lll_opy_(self, test):
  global CONFIG
  global bstack1l1ll111_opy_
  global bstack111ll1l11_opy_
  global bstack1111l1l1_opy_
  global bstack11l1lll1_opy_
  global bstack11l1llll_opy_
  global bstack1l1l1ll1l_opy_
  global bstack1l1l1l1lll_opy_
  global bstack111l1llll_opy_
  global bstack1llll1lll1_opy_
  global bstack1lll11l1ll_opy_
  global bstack1l1l11l1l1_opy_
  try:
    if not bstack1111l1l1_opy_:
      with open(os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠫࢃ࠭ੌ")), bstack11lllll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯੍ࠬ"), bstack11lllll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ੎"))) as f:
        bstack1l11llll_opy_ = json.loads(bstack11lllll_opy_ (u"ࠢࡼࠤ੏") + f.read().strip() + bstack11lllll_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ੐") + bstack11lllll_opy_ (u"ࠤࢀࠦੑ"))
        bstack1111l1l1_opy_ = bstack1l11llll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1lll11l1ll_opy_:
    for driver in bstack1lll11l1ll_opy_:
      if bstack1111l1l1_opy_ == driver.session_id:
        if test:
          bstack1l11l11l1_opy_ = str(test.data)
          if CONFIG.get(bstack11lllll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ੒"), False):
            if CONFIG.get(bstack11lllll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ੓"), bstack11lllll_opy_ (u"ࠧࡧࡵࡵࡱࠥ੔")) == bstack11lllll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ੕"):
              bstack111ll111_opy_ = bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ੖"), None)
              bstack1l1ll11l_opy_(driver, bstack111ll111_opy_)
          if bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ੗"), None) and bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੘"), None):
            logger.info(bstack11lllll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠢࠥਖ਼"))
            bstack1111ll111_opy_.bstack1lll111l11_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack1ll1lll11l_opy_=bstack1l1l11l1l1_opy_)
        if not bstack1ll11l11l1_opy_ and bstack1l11l11l1_opy_:
          bstack11111l11l_opy_ = {
            bstack11lllll_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫਗ਼"): bstack11lllll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਜ਼"),
            bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩੜ"): {
              bstack11lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ੝"): bstack1l11l11l1_opy_
            }
          }
          bstack1l1ll1l111_opy_ = bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ਫ਼").format(json.dumps(bstack11111l11l_opy_))
          driver.execute_script(bstack1l1ll1l111_opy_)
        if bstack11l1lll1_opy_:
          bstack1ll11lll1l_opy_ = {
            bstack11lllll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ੟"): bstack11lllll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ੠"),
            bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੡"): {
              bstack11lllll_opy_ (u"ࠬࡪࡡࡵࡣࠪ੢"): bstack1l11l11l1_opy_ + bstack11lllll_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ੣"),
              bstack11lllll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭੤"): bstack11lllll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭੥")
            }
          }
          if bstack11l1lll1_opy_.status == bstack11lllll_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ੦"):
            bstack1ll111l11_opy_ = bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ੧").format(json.dumps(bstack1ll11lll1l_opy_))
            driver.execute_script(bstack1ll111l11_opy_)
            bstack1lll1l11l1_opy_(driver, bstack11lllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ੨"))
          elif bstack11l1lll1_opy_.status == bstack11lllll_opy_ (u"ࠬࡌࡁࡊࡎࠪ੩"):
            reason = bstack11lllll_opy_ (u"ࠨࠢ੪")
            bstack1ll11l1l1l_opy_ = bstack1l11l11l1_opy_ + bstack11lllll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨ੫")
            if bstack11l1lll1_opy_.message:
              reason = str(bstack11l1lll1_opy_.message)
              bstack1ll11l1l1l_opy_ = bstack1ll11l1l1l_opy_ + bstack11lllll_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ੬") + reason
            bstack1ll11lll1l_opy_[bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ੭")] = {
              bstack11lllll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ੮"): bstack11lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ੯"),
              bstack11lllll_opy_ (u"ࠬࡪࡡࡵࡣࠪੰ"): bstack1ll11l1l1l_opy_
            }
            bstack1ll111l11_opy_ = bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫੱ").format(json.dumps(bstack1ll11lll1l_opy_))
            driver.execute_script(bstack1ll111l11_opy_)
            bstack1lll1l11l1_opy_(driver, bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧੲ"), reason)
            bstack11l11lll1_opy_(reason, str(bstack11l1lll1_opy_), str(bstack11l1lll1l_opy_), logger)
  elif bstack1111l1l1_opy_:
    try:
      data = {}
      bstack1l11l11l1_opy_ = None
      if test:
        bstack1l11l11l1_opy_ = str(test.data)
      if not bstack1ll11l11l1_opy_ and bstack1l11l11l1_opy_:
        data[bstack11lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ੳ")] = bstack1l11l11l1_opy_
      if bstack11l1lll1_opy_:
        if bstack11l1lll1_opy_.status == bstack11lllll_opy_ (u"ࠩࡓࡅࡘ࡙ࠧੴ"):
          data[bstack11lllll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪੵ")] = bstack11lllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ੶")
        elif bstack11l1lll1_opy_.status == bstack11lllll_opy_ (u"ࠬࡌࡁࡊࡎࠪ੷"):
          data[bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭੸")] = bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ੹")
          if bstack11l1lll1_opy_.message:
            data[bstack11lllll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ੺")] = str(bstack11l1lll1_opy_.message)
      user = CONFIG[bstack11lllll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੻")]
      key = CONFIG[bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭੼")]
      url = bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩ੽").format(user, key, bstack1111l1l1_opy_)
      headers = {
        bstack11lllll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ੾"): bstack11lllll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ੿"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1lll1111_opy_.format(str(e)))
  if bstack1l1ll111_opy_:
    bstack1l1l1l1lll_opy_(bstack1l1ll111_opy_)
  if bstack111ll1l11_opy_:
    bstack111l1llll_opy_(bstack111ll1l11_opy_)
  if bstack1lll1l1ll_opy_:
    bstack1llll1lll1_opy_()
  bstack1l1l1ll1l_opy_(self, test)
def bstack1ll111lll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1ll1lll1_opy_
  global CONFIG
  global bstack1lll11l1ll_opy_
  global bstack1111l1l1_opy_
  bstack1111ll1l1_opy_ = None
  try:
    if bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭઀"), None):
      try:
        if not bstack1111l1l1_opy_:
          with open(os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠨࢀࠪઁ")), bstack11lllll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩં"), bstack11lllll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬઃ"))) as f:
            bstack1l11llll_opy_ = json.loads(bstack11lllll_opy_ (u"ࠦࢀࠨ઄") + f.read().strip() + bstack11lllll_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧઅ") + bstack11lllll_opy_ (u"ࠨࡽࠣઆ"))
            bstack1111l1l1_opy_ = bstack1l11llll_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1lll11l1ll_opy_:
        for driver in bstack1lll11l1ll_opy_:
          if bstack1111l1l1_opy_ == driver.session_id:
            bstack1111ll1l1_opy_ = driver
    bstack1111llll1_opy_ = bstack1111ll111_opy_.bstack11lll1111_opy_(CONFIG, test.tags)
    if bstack1111ll1l1_opy_:
      threading.current_thread().isA11yTest = bstack1111ll111_opy_.bstack1111l111l_opy_(bstack1111ll1l1_opy_, bstack1111llll1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1111llll1_opy_
  except:
    pass
  bstack1l1ll1lll1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l1lll1_opy_
  bstack11l1lll1_opy_ = self._test
def bstack11ll111l_opy_():
  global bstack1l1l11l111_opy_
  try:
    if os.path.exists(bstack1l1l11l111_opy_):
      os.remove(bstack1l1l11l111_opy_)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪઇ") + str(e))
def bstack1ll1ll1l1l_opy_():
  global bstack1l1l11l111_opy_
  bstack11l1l1l1l_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1l11l111_opy_):
      with open(bstack1l1l11l111_opy_, bstack11lllll_opy_ (u"ࠨࡹࠪઈ")):
        pass
      with open(bstack1l1l11l111_opy_, bstack11lllll_opy_ (u"ࠤࡺ࠯ࠧઉ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1l11l111_opy_):
      bstack11l1l1l1l_opy_ = json.load(open(bstack1l1l11l111_opy_, bstack11lllll_opy_ (u"ࠪࡶࡧ࠭ઊ")))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ઋ") + str(e))
  finally:
    return bstack11l1l1l1l_opy_
def bstack111111ll_opy_(platform_index, item_index):
  global bstack1l1l11l111_opy_
  try:
    bstack11l1l1l1l_opy_ = bstack1ll1ll1l1l_opy_()
    bstack11l1l1l1l_opy_[item_index] = platform_index
    with open(bstack1l1l11l111_opy_, bstack11lllll_opy_ (u"ࠧࡽࠫࠣઌ")) as outfile:
      json.dump(bstack11l1l1l1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫઍ") + str(e))
def bstack1lll111111_opy_(bstack1l1lllll_opy_):
  global CONFIG
  bstack1l1lll11l1_opy_ = bstack11lllll_opy_ (u"ࠧࠨ઎")
  if not bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫએ") in CONFIG:
    logger.info(bstack11lllll_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ઐ"))
  try:
    platform = CONFIG[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ઑ")][bstack1l1lllll_opy_]
    if bstack11lllll_opy_ (u"ࠫࡴࡹࠧ઒") in platform:
      bstack1l1lll11l1_opy_ += str(platform[bstack11lllll_opy_ (u"ࠬࡵࡳࠨઓ")]) + bstack11lllll_opy_ (u"࠭ࠬࠡࠩઔ")
    if bstack11lllll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪક") in platform:
      bstack1l1lll11l1_opy_ += str(platform[bstack11lllll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫખ")]) + bstack11lllll_opy_ (u"ࠩ࠯ࠤࠬગ")
    if bstack11lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧઘ") in platform:
      bstack1l1lll11l1_opy_ += str(platform[bstack11lllll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨઙ")]) + bstack11lllll_opy_ (u"ࠬ࠲ࠠࠨચ")
    if bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨછ") in platform:
      bstack1l1lll11l1_opy_ += str(platform[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩજ")]) + bstack11lllll_opy_ (u"ࠨ࠮ࠣࠫઝ")
    if bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧઞ") in platform:
      bstack1l1lll11l1_opy_ += str(platform[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨટ")]) + bstack11lllll_opy_ (u"ࠫ࠱ࠦࠧઠ")
    if bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ડ") in platform:
      bstack1l1lll11l1_opy_ += str(platform[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧઢ")]) + bstack11lllll_opy_ (u"ࠧ࠭ࠢࠪણ")
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨત") + str(e))
  finally:
    if bstack1l1lll11l1_opy_[len(bstack1l1lll11l1_opy_) - 2:] == bstack11lllll_opy_ (u"ࠩ࠯ࠤࠬથ"):
      bstack1l1lll11l1_opy_ = bstack1l1lll11l1_opy_[:-2]
    return bstack1l1lll11l1_opy_
def bstack11ll11l1l_opy_(path, bstack1l1lll11l1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11111l1ll_opy_ = ET.parse(path)
    bstack1lllll1111_opy_ = bstack11111l1ll_opy_.getroot()
    bstack1l1111l1_opy_ = None
    for suite in bstack1lllll1111_opy_.iter(bstack11lllll_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩદ")):
      if bstack11lllll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫધ") in suite.attrib:
        suite.attrib[bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪન")] += bstack11lllll_opy_ (u"࠭ࠠࠨ઩") + bstack1l1lll11l1_opy_
        bstack1l1111l1_opy_ = suite
    bstack1lll1l11l_opy_ = None
    for robot in bstack1lllll1111_opy_.iter(bstack11lllll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭પ")):
      bstack1lll1l11l_opy_ = robot
    bstack1ll111l11l_opy_ = len(bstack1lll1l11l_opy_.findall(bstack11lllll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧફ")))
    if bstack1ll111l11l_opy_ == 1:
      bstack1lll1l11l_opy_.remove(bstack1lll1l11l_opy_.findall(bstack11lllll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨબ"))[0])
      bstack1ll11ll1l_opy_ = ET.Element(bstack11lllll_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩભ"), attrib={bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩમ"): bstack11lllll_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬય"), bstack11lllll_opy_ (u"࠭ࡩࡥࠩર"): bstack11lllll_opy_ (u"ࠧࡴ࠲ࠪ઱")})
      bstack1lll1l11l_opy_.insert(1, bstack1ll11ll1l_opy_)
      bstack1ll11lll_opy_ = None
      for suite in bstack1lll1l11l_opy_.iter(bstack11lllll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧલ")):
        bstack1ll11lll_opy_ = suite
      bstack1ll11lll_opy_.append(bstack1l1111l1_opy_)
      bstack1lll1l1111_opy_ = None
      for status in bstack1l1111l1_opy_.iter(bstack11lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩળ")):
        bstack1lll1l1111_opy_ = status
      bstack1ll11lll_opy_.append(bstack1lll1l1111_opy_)
    bstack11111l1ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨ઴") + str(e))
def bstack111lllll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1ll11lll_opy_
  global CONFIG
  if bstack11lllll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣવ") in options:
    del options[bstack11lllll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤશ")]
  bstack1ll1l11l_opy_ = bstack1ll1ll1l1l_opy_()
  for bstack1ll1l11l1_opy_ in bstack1ll1l11l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11lllll_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭ષ"), str(bstack1ll1l11l1_opy_), bstack11lllll_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫસ"))
    bstack11ll11l1l_opy_(path, bstack1lll111111_opy_(bstack1ll1l11l_opy_[bstack1ll1l11l1_opy_]))
  bstack11ll111l_opy_()
  return bstack1l1ll11lll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1l1ll11l_opy_(self, ff_profile_dir):
  global bstack1ll11ll111_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll11ll111_opy_(self, ff_profile_dir)
def bstack1llll1l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll11111l_opy_
  bstack1llll1ll_opy_ = []
  if bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫહ") in CONFIG:
    bstack1llll1ll_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ઺")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11lllll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ઻")],
      pabot_args[bstack11lllll_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩ઼ࠧ")],
      argfile,
      pabot_args.get(bstack11lllll_opy_ (u"ࠧ࡮ࡩࡷࡧࠥઽ")),
      pabot_args[bstack11lllll_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤા")],
      platform[0],
      bstack1ll11111l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11lllll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢિ")] or [(bstack11lllll_opy_ (u"ࠣࠤી"), None)]
    for platform in enumerate(bstack1llll1ll_opy_)
  ]
def bstack11l1l1111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11lll11ll_opy_=bstack11lllll_opy_ (u"ࠩࠪુ")):
  global bstack11l11l11_opy_
  self.platform_index = platform_index
  self.bstack1ll1lllll_opy_ = bstack11lll11ll_opy_
  bstack11l11l11_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1lllll1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1llll11ll1_opy_
  global bstack1lllll1l1_opy_
  if not bstack11lllll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૂ") in item.options:
    item.options[bstack11lllll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ૃ")] = []
  for v in item.options[bstack11lllll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧૄ")]:
    if bstack11lllll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬૅ") in v:
      item.options[bstack11lllll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૆")].remove(v)
    if bstack11lllll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨે") in v:
      item.options[bstack11lllll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫૈ")].remove(v)
  item.options[bstack11lllll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૉ")].insert(0, bstack11lllll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭૊").format(item.platform_index))
  item.options[bstack11lllll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧો")].insert(0, bstack11lllll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭ૌ").format(item.bstack1ll1lllll_opy_))
  if bstack1lllll1l1_opy_:
    item.options[bstack11lllll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦ્ࠩ")].insert(0, bstack11lllll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫ૎").format(bstack1lllll1l1_opy_))
  return bstack1llll11ll1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1lll111l1_opy_(command, item_index):
  if bstack1lll11111_opy_.get_property(bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ૏")):
    os.environ[bstack11lllll_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫૐ")] = json.dumps(CONFIG[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૑")][item_index % bstack111l11l11_opy_])
  global bstack1lllll1l1_opy_
  if bstack1lllll1l1_opy_:
    command[0] = command[0].replace(bstack11lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ૒"), bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ૓") + str(
      item_index) + bstack11lllll_opy_ (u"ࠧࠡࠩ૔") + bstack1lllll1l1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૕"),
                                    bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭૖") + str(item_index), 1)
def bstack1l1llll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1lll1ll11l_opy_
  bstack1lll111l1_opy_(command, item_index)
  return bstack1lll1ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1ll11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1lll1ll11l_opy_
  bstack1lll111l1_opy_(command, item_index)
  return bstack1lll1ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11lll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1lll1ll11l_opy_
  bstack1lll111l1_opy_(command, item_index)
  return bstack1lll1ll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11llll11_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll1ll11ll_opy_
  bstack11111l111_opy_ = bstack1ll1ll11ll_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack11lllll_opy_ (u"ࠪࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡥࡡࡳࡴࠪ૗")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11lllll_opy_ (u"ࠫࡪࡾࡣࡠࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࡣࡦࡸࡲࠨ૘")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11111l111_opy_
def bstack1lll1l1l1_opy_(self, name, context, *args):
  os.environ[bstack11lllll_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭૙")] = json.dumps(CONFIG[bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૚")][int(threading.current_thread()._name) % bstack111l11l11_opy_])
  global bstack111ll1l1l_opy_
  if name == bstack11lllll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨ૛"):
    bstack111ll1l1l_opy_(self, name, context, *args)
    try:
      if not bstack1ll11l11l1_opy_:
        bstack1111ll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l1l11_opy_(bstack11lllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ૜")) else context.browser
        bstack1lll11ll1l_opy_ = str(self.feature.name)
        bstack1l1ll1111_opy_(context, bstack1lll11ll1l_opy_)
        bstack1111ll1l1_opy_.execute_script(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ૝") + json.dumps(bstack1lll11ll1l_opy_) + bstack11lllll_opy_ (u"ࠪࢁࢂ࠭૞"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ૟").format(str(e)))
  elif name == bstack11lllll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧૠ"):
    bstack111ll1l1l_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack11lllll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨૡ")):
        self.driver_before_scenario = True
      if (not bstack1ll11l11l1_opy_):
        scenario_name = args[0].name
        feature_name = bstack1lll11ll1l_opy_ = str(self.feature.name)
        bstack1lll11ll1l_opy_ = feature_name + bstack11lllll_opy_ (u"ࠧࠡ࠯ࠣࠫૢ") + scenario_name
        bstack1111ll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l1l11_opy_(bstack11lllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧૣ")) else context.browser
        if self.driver_before_scenario:
          bstack1l1ll1111_opy_(context, bstack1lll11ll1l_opy_)
          bstack1111ll1l1_opy_.execute_script(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ૤") + json.dumps(bstack1lll11ll1l_opy_) + bstack11lllll_opy_ (u"ࠪࢁࢂ࠭૥"))
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬ૦").format(str(e)))
  elif name == bstack11lllll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭૧"):
    try:
      bstack111111lll_opy_ = args[0].status.name
      bstack1111ll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ૨") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack111111lll_opy_).lower() == bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ૩"):
        bstack1ll1llll1_opy_ = bstack11lllll_opy_ (u"ࠨࠩ૪")
        bstack1l1lll1ll1_opy_ = bstack11lllll_opy_ (u"ࠩࠪ૫")
        bstack11ll1lll1_opy_ = bstack11lllll_opy_ (u"ࠪࠫ૬")
        try:
          import traceback
          bstack1ll1llll1_opy_ = self.exception.__class__.__name__
          bstack1llll1lll_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1l1lll1ll1_opy_ = bstack11lllll_opy_ (u"ࠫࠥ࠭૭").join(bstack1llll1lll_opy_)
          bstack11ll1lll1_opy_ = bstack1llll1lll_opy_[-1]
        except Exception as e:
          logger.debug(bstack1lll1l1l1l_opy_.format(str(e)))
        bstack1ll1llll1_opy_ += bstack11ll1lll1_opy_
        bstack1ll11111ll_opy_(context, json.dumps(str(args[0].name) + bstack11lllll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ૮") + str(bstack1l1lll1ll1_opy_)),
                            bstack11lllll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ૯"))
        if self.driver_before_scenario:
          bstack1lll11l1l_opy_(getattr(context, bstack11lllll_opy_ (u"ࠧࡱࡣࡪࡩࠬ૰"), None), bstack11lllll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ૱"), bstack1ll1llll1_opy_)
          bstack1111ll1l1_opy_.execute_script(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ૲") + json.dumps(str(args[0].name) + bstack11lllll_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤ૳") + str(bstack1l1lll1ll1_opy_)) + bstack11lllll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫ૴"))
        if self.driver_before_scenario:
          bstack1lll1l11l1_opy_(bstack1111ll1l1_opy_, bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ૵"), bstack11lllll_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ૶") + str(bstack1ll1llll1_opy_))
      else:
        bstack1ll11111ll_opy_(context, bstack11lllll_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣ૷"), bstack11lllll_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ૸"))
        if self.driver_before_scenario:
          bstack1lll11l1l_opy_(getattr(context, bstack11lllll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧૹ"), None), bstack11lllll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥૺ"))
        bstack1111ll1l1_opy_.execute_script(bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩૻ") + json.dumps(str(args[0].name) + bstack11lllll_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤૼ")) + bstack11lllll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ૽"))
        if self.driver_before_scenario:
          bstack1lll1l11l1_opy_(bstack1111ll1l1_opy_, bstack11lllll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ૾"))
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ૿").format(str(e)))
  elif name == bstack11lllll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ଀"):
    try:
      bstack1111ll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l1l11_opy_(bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଁ")) else context.browser
      if context.failed is True:
        bstack1ll11111_opy_ = []
        bstack1l1l1l11ll_opy_ = []
        bstack1ll1ll111_opy_ = []
        bstack1ll1lll1_opy_ = bstack11lllll_opy_ (u"ࠫࠬଂ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll11111_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1llll1lll_opy_ = traceback.format_tb(exc_tb)
            bstack1l1111111_opy_ = bstack11lllll_opy_ (u"ࠬࠦࠧଃ").join(bstack1llll1lll_opy_)
            bstack1l1l1l11ll_opy_.append(bstack1l1111111_opy_)
            bstack1ll1ll111_opy_.append(bstack1llll1lll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1lll1l1l1l_opy_.format(str(e)))
        bstack1ll1llll1_opy_ = bstack11lllll_opy_ (u"࠭ࠧ଄")
        for i in range(len(bstack1ll11111_opy_)):
          bstack1ll1llll1_opy_ += bstack1ll11111_opy_[i] + bstack1ll1ll111_opy_[i] + bstack11lllll_opy_ (u"ࠧ࡝ࡰࠪଅ")
        bstack1ll1lll1_opy_ = bstack11lllll_opy_ (u"ࠨࠢࠪଆ").join(bstack1l1l1l11ll_opy_)
        if not self.driver_before_scenario:
          bstack1ll11111ll_opy_(context, bstack1ll1lll1_opy_, bstack11lllll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣଇ"))
          bstack1lll11l1l_opy_(getattr(context, bstack11lllll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨଈ"), None), bstack11lllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦଉ"), bstack1ll1llll1_opy_)
          bstack1111ll1l1_opy_.execute_script(bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪଊ") + json.dumps(bstack1ll1lll1_opy_) + bstack11lllll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ଋ"))
          bstack1lll1l11l1_opy_(bstack1111ll1l1_opy_, bstack11lllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢଌ"), bstack11lllll_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨ଍") + str(bstack1ll1llll1_opy_))
          bstack1l11l11l_opy_ = bstack1l1l1l11l1_opy_(bstack1ll1lll1_opy_, self.feature.name, logger)
          if (bstack1l11l11l_opy_ != None):
            bstack1ll1l1ll1l_opy_.append(bstack1l11l11l_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1ll11111ll_opy_(context, bstack11lllll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧ଎") + str(self.feature.name) + bstack11lllll_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧଏ"), bstack11lllll_opy_ (u"ࠦ࡮ࡴࡦࡰࠤଐ"))
          bstack1lll11l1l_opy_(getattr(context, bstack11lllll_opy_ (u"ࠬࡶࡡࡨࡧࠪ଑"), None), bstack11lllll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ଒"))
          bstack1111ll1l1_opy_.execute_script(bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬଓ") + json.dumps(bstack11lllll_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦଔ") + str(self.feature.name) + bstack11lllll_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦକ")) + bstack11lllll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩଖ"))
          bstack1lll1l11l1_opy_(bstack1111ll1l1_opy_, bstack11lllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫଗ"))
          bstack1l11l11l_opy_ = bstack1l1l1l11l1_opy_(bstack1ll1lll1_opy_, self.feature.name, logger)
          if (bstack1l11l11l_opy_ != None):
            bstack1ll1l1ll1l_opy_.append(bstack1l11l11l_opy_)
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧଘ").format(str(e)))
  else:
    bstack111ll1l1l_opy_(self, name, context, *args)
  if name in [bstack11lllll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ଙ"), bstack11lllll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨଚ")]:
    bstack111ll1l1l_opy_(self, name, context, *args)
    if (name == bstack11lllll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩଛ") and self.driver_before_scenario) or (
            name == bstack11lllll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩଜ") and not self.driver_before_scenario):
      try:
        bstack1111ll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l1l11_opy_(bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଝ")) else context.browser
        bstack1111ll1l1_opy_.quit()
      except Exception:
        pass
def bstack1llllll1ll_opy_(config, startdir):
  return bstack11lllll_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤଞ").format(bstack11lllll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦଟ"))
notset = Notset()
def bstack1ll11ll1l1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lll1lll1_opy_
  if str(name).lower() == bstack11lllll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ଠ"):
    return bstack11lllll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨଡ")
  else:
    return bstack1lll1lll1_opy_(self, name, default, skip)
def bstack11111ll1_opy_(item, when):
  global bstack11ll11l1_opy_
  try:
    bstack11ll11l1_opy_(item, when)
  except Exception as e:
    pass
def bstack11llll111_opy_():
  return
def bstack11lll111_opy_(type, name, status, reason, bstack1l111l1l1_opy_, bstack11llll1ll_opy_):
  bstack11111l11l_opy_ = {
    bstack11lllll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨଢ"): type,
    bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬଣ"): {}
  }
  if type == bstack11lllll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬତ"):
    bstack11111l11l_opy_[bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଥ")][bstack11lllll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫଦ")] = bstack1l111l1l1_opy_
    bstack11111l11l_opy_[bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଧ")][bstack11lllll_opy_ (u"ࠧࡥࡣࡷࡥࠬନ")] = json.dumps(str(bstack11llll1ll_opy_))
  if type == bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ଩"):
    bstack11111l11l_opy_[bstack11lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬପ")][bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨଫ")] = name
  if type == bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧବ"):
    bstack11111l11l_opy_[bstack11lllll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଭ")][bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ମ")] = status
    if status == bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧଯ"):
      bstack11111l11l_opy_[bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫର")][bstack11lllll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ଱")] = json.dumps(str(reason))
  bstack1l1ll1l111_opy_ = bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨଲ").format(json.dumps(bstack11111l11l_opy_))
  return bstack1l1ll1l111_opy_
def bstack1ll11lllll_opy_(driver_command, response):
    if driver_command == bstack11lllll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨଳ"):
        bstack1ll1llll1l_opy_.bstack111l1lll1_opy_({
            bstack11lllll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ଴"): response[bstack11lllll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬଵ")],
            bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧଶ"): bstack1ll1llll1l_opy_.current_test_uuid()
        })
def bstack11l11l1ll_opy_(item, call, rep):
  global bstack1lll1l11ll_opy_
  global bstack1lll11l1ll_opy_
  global bstack1ll11l11l1_opy_
  name = bstack11lllll_opy_ (u"ࠨࠩଷ")
  try:
    if rep.when == bstack11lllll_opy_ (u"ࠩࡦࡥࡱࡲࠧସ"):
      bstack1111l1l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll11l11l1_opy_:
          name = str(rep.nodeid)
          bstack1ll11llll1_opy_ = bstack11lll111_opy_(bstack11lllll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫହ"), name, bstack11lllll_opy_ (u"ࠫࠬ଺"), bstack11lllll_opy_ (u"ࠬ࠭଻"), bstack11lllll_opy_ (u"଼࠭ࠧ"), bstack11lllll_opy_ (u"ࠧࠨଽ"))
          threading.current_thread().bstack1llll11l11_opy_ = name
          for driver in bstack1lll11l1ll_opy_:
            if bstack1111l1l1_opy_ == driver.session_id:
              driver.execute_script(bstack1ll11llll1_opy_)
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨା").format(str(e)))
      try:
        bstack1ll1111l1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11lllll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪି"):
          status = bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪୀ") if rep.outcome.lower() == bstack11lllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫୁ") else bstack11lllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬୂ")
          reason = bstack11lllll_opy_ (u"࠭ࠧୃ")
          if status == bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧୄ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11lllll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭୅") if status == bstack11lllll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୆") else bstack11lllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩେ")
          data = name + bstack11lllll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ୈ") if status == bstack11lllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ୉") else name + bstack11lllll_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ୊") + reason
          bstack11ll1111_opy_ = bstack11lll111_opy_(bstack11lllll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩୋ"), bstack11lllll_opy_ (u"ࠨࠩୌ"), bstack11lllll_opy_ (u"୍ࠩࠪ"), bstack11lllll_opy_ (u"ࠪࠫ୎"), level, data)
          for driver in bstack1lll11l1ll_opy_:
            if bstack1111l1l1_opy_ == driver.session_id:
              driver.execute_script(bstack11ll1111_opy_)
      except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ୏").format(str(e)))
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ୐").format(str(e)))
  bstack1lll1l11ll_opy_(item, call, rep)
def bstack1l1ll11l_opy_(driver, bstack1l11ll111_opy_):
  PercySDK.screenshot(driver, bstack1l11ll111_opy_)
def bstack1lll11111l_opy_(driver):
  if bstack111llll1_opy_.bstack1ll1l1l1l1_opy_() is True or bstack111llll1_opy_.capturing() is True:
    return
  bstack111llll1_opy_.bstack1l111111l_opy_()
  while not bstack111llll1_opy_.bstack1ll1l1l1l1_opy_():
    bstack1l11l1ll1_opy_ = bstack111llll1_opy_.bstack111l111l_opy_()
    bstack1l1ll11l_opy_(driver, bstack1l11l1ll1_opy_)
  bstack111llll1_opy_.bstack1l1l1lll1_opy_()
def bstack11111l1l_opy_(sequence, driver_command, response = None):
    try:
      if sequence != bstack11lllll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭୑"):
        return
      if not CONFIG.get(bstack11lllll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭୒"), False):
        return
      bstack1l11l1ll1_opy_ = bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ୓"), None)
      for command in bstack1ll1l1l11l_opy_:
        if command == driver_command:
          for driver in bstack1lll11l1ll_opy_:
            bstack1lll11111l_opy_(driver)
      bstack1l1ll1ll_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ୔"), bstack11lllll_opy_ (u"ࠥࡥࡺࡺ࡯ࠣ୕"))
      if driver_command in bstack1lll1ll1l_opy_[bstack1l1ll1ll_opy_]:
        bstack111llll1_opy_.bstack1l111l1l_opy_(bstack1l11l1ll1_opy_, driver_command)
    except Exception as e:
      pass
def bstack1lll11llll_opy_(framework_name):
  global bstack1l1ll1ll11_opy_
  global bstack1ll1llll_opy_
  global bstack11l1ll11_opy_
  bstack1l1ll1ll11_opy_ = framework_name
  logger.info(bstack11l1llll1_opy_.format(bstack1l1ll1ll11_opy_.split(bstack11lllll_opy_ (u"ࠫ࠲࠭ୖ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1l111l_opy_:
      Service.start = bstack1llll1l111_opy_
      Service.stop = bstack1l11l1l1l_opy_
      webdriver.Remote.get = bstack1l1l11ll_opy_
      WebDriver.close = bstack11ll1l1ll_opy_
      WebDriver.quit = bstack11ll11ll_opy_
      webdriver.Remote.__init__ = bstack1l11l111l_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack11l111l1l_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1l1lll1l_opy_ = getAccessibilityResultsSummary
    if not bstack1l1l111l_opy_ and bstack1ll1llll1l_opy_.on():
      webdriver.Remote.__init__ = bstack1l1ll1l1l_opy_
    if bstack11lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫୗ") in str(framework_name).lower() and bstack1ll1llll1l_opy_.on():
      WebDriver.execute = bstack1ll1l1l1_opy_
    bstack1ll1llll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1l111l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack111l1l1ll_opy_
  except Exception as e:
    pass
  bstack1l1l1l111_opy_()
  if not bstack1ll1llll_opy_:
    bstack1ll111llll_opy_(bstack11lllll_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣ୘"), bstack111l11111_opy_)
  if bstack1l1ll11111_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l11l1ll_opy_
    except Exception as e:
      logger.error(bstack1ll11l1111_opy_.format(str(e)))
  if bstack1lllll1l1l_opy_():
    bstack1lllllll1l_opy_(CONFIG, logger)
  if (bstack11lllll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭୙") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack11lllll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ୚"), False):
          bstack1l1ll1l11_opy_(bstack11111l1l_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l1l1ll11l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11lll1l1l_opy_
      except Exception as e:
        logger.warn(bstack1lll1l1lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1lll1lll11_opy_
      except Exception as e:
        logger.debug(bstack1ll1l1llll_opy_ + str(e))
    except Exception as e:
      bstack1ll111llll_opy_(e, bstack1lll1l1lll_opy_)
    Output.start_test = bstack1ll111l1ll_opy_
    Output.end_test = bstack1ll1111lll_opy_
    TestStatus.__init__ = bstack1ll111lll_opy_
    QueueItem.__init__ = bstack11l1l1111_opy_
    pabot._create_items = bstack1llll1l1_opy_
    try:
      from pabot import __version__ as bstack11l1lll11_opy_
      if version.parse(bstack11l1lll11_opy_) >= version.parse(bstack11lllll_opy_ (u"ࠩ࠵࠲࠶࠻࠮࠱ࠩ୛")):
        pabot._run = bstack11lll1l11_opy_
      elif version.parse(bstack11l1lll11_opy_) >= version.parse(bstack11lllll_opy_ (u"ࠪ࠶࠳࠷࠳࠯࠲ࠪଡ଼")):
        pabot._run = bstack1l1ll11l1_opy_
      else:
        pabot._run = bstack1l1llll1l_opy_
    except Exception as e:
      pabot._run = bstack1l1llll1l_opy_
    pabot._create_command_for_execution = bstack1ll1lllll1_opy_
    pabot._report_results = bstack111lllll1_opy_
  if bstack11lllll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫଢ଼") in str(framework_name).lower():
    if not bstack1l1l111l_opy_:
      return
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll111llll_opy_(e, bstack1l1lllll11_opy_)
    Runner.run_hook = bstack1lll1l1l1_opy_
    Step.run = bstack11llll11_opy_
  if bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ୞") in str(framework_name).lower():
    if not bstack1l1l111l_opy_:
      return
    try:
      if CONFIG.get(bstack11lllll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬୟ"), False):
          bstack1l1ll1l11_opy_(bstack11111l1l_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1llllll1ll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11llll111_opy_
      Config.getoption = bstack1ll11ll1l1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l11l1ll_opy_
    except Exception as e:
      pass
def bstack1l1llll1ll_opy_():
  global CONFIG
  if bstack11lllll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧୠ") in CONFIG and int(CONFIG[bstack11lllll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨୡ")]) > 1:
    logger.warn(bstack1lll11ll_opy_)
def bstack11lll11l_opy_(arg, bstack1lll11l11_opy_, bstack1lll1ll1ll_opy_=None):
  global CONFIG
  global bstack111ll1l1_opy_
  global bstack1ll11ll11_opy_
  global bstack1l1l111l_opy_
  global bstack1lll11111_opy_
  bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩୢ")
  if bstack1lll11l11_opy_ and isinstance(bstack1lll11l11_opy_, str):
    bstack1lll11l11_opy_ = eval(bstack1lll11l11_opy_)
  CONFIG = bstack1lll11l11_opy_[bstack11lllll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪୣ")]
  bstack111ll1l1_opy_ = bstack1lll11l11_opy_[bstack11lllll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ୤")]
  bstack1ll11ll11_opy_ = bstack1lll11l11_opy_[bstack11lllll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ୥")]
  bstack1l1l111l_opy_ = bstack1lll11l11_opy_[bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ୦")]
  bstack1lll11111_opy_.bstack1lll11l1l1_opy_(bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ୧"), bstack1l1l111l_opy_)
  os.environ[bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ୨")] = bstack1ll11ll1ll_opy_
  os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ୩")] = json.dumps(CONFIG)
  os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ୪")] = bstack111ll1l1_opy_
  os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ୫")] = str(bstack1ll11ll11_opy_)
  os.environ[bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫ୬")] = str(True)
  if bstack1ll1l1l1ll_opy_(arg, [bstack11lllll_opy_ (u"࠭࠭࡯ࠩ୭"), bstack11lllll_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ୮")]) != -1:
    os.environ[bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ୯")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1l1ll_opy_)
    return
  bstack1l1l1l1l1_opy_()
  global bstack1llll1l11l_opy_
  global bstack11l1lll1l_opy_
  global bstack1ll11111l_opy_
  global bstack1lllll1l1_opy_
  global bstack11llll1l_opy_
  global bstack11l1ll11_opy_
  global bstack1ll1l11ll_opy_
  arg.append(bstack11lllll_opy_ (u"ࠤ࠰࡛ࠧ୰"))
  arg.append(bstack11lllll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨୱ"))
  arg.append(bstack11lllll_opy_ (u"ࠦ࠲࡝ࠢ୲"))
  arg.append(bstack11lllll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿࡚ࡨࡦࠢ࡫ࡳࡴࡱࡩ࡮ࡲ࡯ࠦ୳"))
  global bstack11l1ll1l_opy_
  global bstack1ll1lll111_opy_
  global bstack1l1ll1lll1_opy_
  global bstack1ll11ll111_opy_
  global bstack11l11l11_opy_
  global bstack1llll11ll1_opy_
  global bstack1llll1ll1l_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1llllll11l_opy_
  global bstack1lll1lll1_opy_
  global bstack11ll11l1_opy_
  global bstack1lll1l11ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1ll1l_opy_ = webdriver.Remote.__init__
    bstack1ll1lll111_opy_ = WebDriver.quit
    bstack1llll1ll1l_opy_ = WebDriver.close
    bstack1l1l1l1ll_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1lll1l111_opy_(CONFIG) and bstack1111l1lll_opy_():
    if bstack1l1l11lll1_opy_() < version.parse(bstack1111ll11_opy_):
      logger.error(bstack11ll11ll1_opy_.format(bstack1l1l11lll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1llllll11l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll11l1111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1lll1lll1_opy_ = Config.getoption
    from _pytest import runner
    bstack11ll11l1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11l11lll_opy_)
  try:
    from pytest_bdd import reporting
    bstack1lll1l11ll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11lllll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ୴"))
  bstack1ll11111l_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୵"), {}).get(bstack11lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ୶"))
  bstack1ll1l11ll_opy_ = True
  bstack1lll11llll_opy_(bstack11ll1ll11_opy_)
  os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ୷")] = CONFIG[bstack11lllll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ୸")]
  os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ୹")] = CONFIG[bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ୺")]
  os.environ[bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ୻")] = bstack1l1l111l_opy_.__str__()
  from _pytest.config import main as bstack1l1lllllll_opy_
  bstack1l1lllllll_opy_(arg)
  if bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ୼") in multiprocessing.current_process().__dict__.keys():
    for bstack1ll11l11l_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack1lll1ll1ll_opy_.append(bstack1ll11l11l_opy_)
def bstack1lll11lll_opy_(arg):
  bstack1lll11llll_opy_(bstack1ll111ll1l_opy_)
  os.environ[bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ୽")] = str(bstack1ll11ll11_opy_)
  from behave.__main__ import main as bstack1l1ll111l1_opy_
  bstack1l1ll111l1_opy_(arg)
def bstack1lll111l_opy_():
  logger.info(bstack1l1111l1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11lllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ୾"), help=bstack11lllll_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫ୿"))
  parser.add_argument(bstack11lllll_opy_ (u"ࠫ࠲ࡻࠧ஀"), bstack11lllll_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ஁"), help=bstack11lllll_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬஂ"))
  parser.add_argument(bstack11lllll_opy_ (u"ࠧ࠮࡭ࠪஃ"), bstack11lllll_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧ஄"), help=bstack11lllll_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪஅ"))
  parser.add_argument(bstack11lllll_opy_ (u"ࠪ࠱࡫࠭ஆ"), bstack11lllll_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩஇ"), help=bstack11lllll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫஈ"))
  bstack1l1lll11ll_opy_ = parser.parse_args()
  try:
    bstack1l1l1l111l_opy_ = bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪஉ")
    if bstack1l1lll11ll_opy_.framework and bstack1l1lll11ll_opy_.framework not in (bstack11lllll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧஊ"), bstack11lllll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ஋")):
      bstack1l1l1l111l_opy_ = bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ஌")
    bstack1l1l1l1111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l1l111l_opy_)
    bstack1llllllll_opy_ = open(bstack1l1l1l1111_opy_, bstack11lllll_opy_ (u"ࠪࡶࠬ஍"))
    bstack1l1llll1_opy_ = bstack1llllllll_opy_.read()
    bstack1llllllll_opy_.close()
    if bstack1l1lll11ll_opy_.username:
      bstack1l1llll1_opy_ = bstack1l1llll1_opy_.replace(bstack11lllll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫஎ"), bstack1l1lll11ll_opy_.username)
    if bstack1l1lll11ll_opy_.key:
      bstack1l1llll1_opy_ = bstack1l1llll1_opy_.replace(bstack11lllll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧஏ"), bstack1l1lll11ll_opy_.key)
    if bstack1l1lll11ll_opy_.framework:
      bstack1l1llll1_opy_ = bstack1l1llll1_opy_.replace(bstack11lllll_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧஐ"), bstack1l1lll11ll_opy_.framework)
    file_name = bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ஑")
    file_path = os.path.abspath(file_name)
    bstack1ll11lll11_opy_ = open(file_path, bstack11lllll_opy_ (u"ࠨࡹࠪஒ"))
    bstack1ll11lll11_opy_.write(bstack1l1llll1_opy_)
    bstack1ll11lll11_opy_.close()
    logger.info(bstack1l1l1ll1ll_opy_)
    try:
      os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫஓ")] = bstack1l1lll11ll_opy_.framework if bstack1l1lll11ll_opy_.framework != None else bstack11lllll_opy_ (u"ࠥࠦஔ")
      config = yaml.safe_load(bstack1l1llll1_opy_)
      config[bstack11lllll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫக")] = bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫ஖")
      bstack1lll111l1l_opy_(bstack1111l1l11_opy_, config)
    except Exception as e:
      logger.debug(bstack1ll1l1lll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack111111ll1_opy_.format(str(e)))
def bstack1lll111l1l_opy_(bstack1ll111ll_opy_, config, bstack1l1l111ll_opy_={}):
  global bstack1l1l111l_opy_
  global bstack11l1l1l1_opy_
  if not config:
    return
  bstack1l1ll11l11_opy_ = bstack1llll1l1ll_opy_ if not bstack1l1l111l_opy_ else (
    bstack1lllll11l_opy_ if bstack11lllll_opy_ (u"࠭ࡡࡱࡲࠪ஗") in config else bstack1llll111_opy_)
  data = {
    bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ஘"): config[bstack11lllll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪங")],
    bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬச"): config[bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭஛")],
    bstack11lllll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨஜ"): bstack1ll111ll_opy_,
    bstack11lllll_opy_ (u"ࠬࡪࡥࡵࡧࡦࡸࡪࡪࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ஝"): os.environ.get(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨஞ"), bstack11l1l1l1_opy_),
    bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩட"): bstack1l1l11ll1_opy_,
    bstack11lllll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮ࠪ஠"): bstack11111111l_opy_(),
    bstack11lllll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ஡"): {
      bstack11lllll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ஢"): str(config[bstack11lllll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫண")]) if bstack11lllll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬத") in config else bstack11lllll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ஥"),
      bstack11lllll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡘࡨࡶࡸ࡯࡯࡯ࠩ஦"): sys.version,
      bstack11lllll_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪ஧"): bstack1l1l1111_opy_(os.getenv(bstack11lllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦந"), bstack11lllll_opy_ (u"ࠥࠦன"))),
      bstack11lllll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ப"): bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ஫"),
      bstack11lllll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ஬"): bstack1l1ll11l11_opy_,
      bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஭"): config[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫம")] if config[bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬய")] else bstack11lllll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦர"),
      bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ற"): str(config[bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧல")]) if bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨள") in config else bstack11lllll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣழ"),
      bstack11lllll_opy_ (u"ࠨࡱࡶࠫவ"): sys.platform,
      bstack11lllll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫஶ"): socket.gethostname()
    }
  }
  update(data[bstack11lllll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ஷ")], bstack1l1l111ll_opy_)
  try:
    response = bstack1llll11ll_opy_(bstack11lllll_opy_ (u"ࠫࡕࡕࡓࡕࠩஸ"), bstack1ll1111l1l_opy_(bstack1l11lll1l_opy_), data, {
      bstack11lllll_opy_ (u"ࠬࡧࡵࡵࡪࠪஹ"): (config[bstack11lllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ஺")], config[bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ஻")])
    })
    if response:
      logger.debug(bstack11ll11lll_opy_.format(bstack1ll111ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll11l1ll1_opy_.format(str(e)))
def bstack1l1l1111_opy_(framework):
  return bstack11lllll_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ஼").format(str(framework), __version__) if framework else bstack11lllll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥ஽").format(
    __version__)
def bstack1l1l1l1l1_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1l11l1111_opy_()
    logger.debug(bstack1l1l1lllll_opy_.format(str(CONFIG)))
    bstack111l1lll_opy_()
    bstack11l11llll_opy_()
  except Exception as e:
    logger.error(bstack11lllll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢா") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1lll1l1_opy_
  atexit.register(bstack11ll11l11_opy_)
  signal.signal(signal.SIGINT, bstack111llllll_opy_)
  signal.signal(signal.SIGTERM, bstack111llllll_opy_)
def bstack1l1lll1l1_opy_(exctype, value, traceback):
  global bstack1lll11l1ll_opy_
  try:
    for driver in bstack1lll11l1ll_opy_:
      bstack1lll1l11l1_opy_(driver, bstack11lllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫி"), bstack11lllll_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣீ") + str(value))
  except Exception:
    pass
  bstack11ll111ll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11ll111ll_opy_(message=bstack11lllll_opy_ (u"࠭ࠧு"), bstack11l1l111_opy_ = False):
  global CONFIG
  bstack1ll111ll11_opy_ = bstack11lllll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠩூ") if bstack11l1l111_opy_ else bstack11lllll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ௃")
  try:
    if message:
      bstack1l1l111ll_opy_ = {
        bstack1ll111ll11_opy_ : str(message)
      }
      bstack1lll111l1l_opy_(bstack11l111l11_opy_, CONFIG, bstack1l1l111ll_opy_)
    else:
      bstack1lll111l1l_opy_(bstack11l111l11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1l1l11l_opy_.format(str(e)))
def bstack1l1lll1lll_opy_(bstack111lll1l_opy_, size):
  bstack1ll1ll1l1_opy_ = []
  while len(bstack111lll1l_opy_) > size:
    bstack1l1ll1lll_opy_ = bstack111lll1l_opy_[:size]
    bstack1ll1ll1l1_opy_.append(bstack1l1ll1lll_opy_)
    bstack111lll1l_opy_ = bstack111lll1l_opy_[size:]
  bstack1ll1ll1l1_opy_.append(bstack111lll1l_opy_)
  return bstack1ll1ll1l1_opy_
def bstack1ll1ll111l_opy_(args):
  if bstack11lllll_opy_ (u"ࠩ࠰ࡱࠬ௄") in args and bstack11lllll_opy_ (u"ࠪࡴࡩࡨࠧ௅") in args:
    return True
  return False
def run_on_browserstack(bstack1ll1l1lll_opy_=None, bstack1lll1ll1ll_opy_=None, bstack111l1l111_opy_=False):
  global CONFIG
  global bstack111ll1l1_opy_
  global bstack1ll11ll11_opy_
  global bstack11l1l1l1_opy_
  bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠫࠬெ")
  bstack11lll1ll1_opy_(bstack1l1l111l1_opy_, logger)
  if bstack1ll1l1lll_opy_ and isinstance(bstack1ll1l1lll_opy_, str):
    bstack1ll1l1lll_opy_ = eval(bstack1ll1l1lll_opy_)
  if bstack1ll1l1lll_opy_:
    CONFIG = bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬே")]
    bstack111ll1l1_opy_ = bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧை")]
    bstack1ll11ll11_opy_ = bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ௉")]
    bstack1lll11111_opy_.bstack1lll11l1l1_opy_(bstack11lllll_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪொ"), bstack1ll11ll11_opy_)
    bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩோ")
  if not bstack111l1l111_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1l1ll_opy_)
      return
    if sys.argv[1] == bstack11lllll_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ௌ") or sys.argv[1] == bstack11lllll_opy_ (u"ࠫ࠲ࡼ்ࠧ"):
      logger.info(bstack11lllll_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬ௎").format(__version__))
      return
    if sys.argv[1] == bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ௏"):
      bstack1lll111l_opy_()
      return
  args = sys.argv
  bstack1l1l1l1l1_opy_()
  global bstack1llll1l11l_opy_
  global bstack111l11l11_opy_
  global bstack1ll1l11ll_opy_
  global bstack1ll1lll1l_opy_
  global bstack11l1lll1l_opy_
  global bstack1ll11111l_opy_
  global bstack1lllll1l1_opy_
  global bstack1lllll11ll_opy_
  global bstack11llll1l_opy_
  global bstack11l1ll11_opy_
  global bstack1l1111l11_opy_
  bstack111l11l11_opy_ = len(CONFIG[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪௐ")])
  if not bstack1ll11ll1ll_opy_:
    if args[1] == bstack11lllll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௑") or args[1] == bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ௒"):
      bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௓")
      args = args[2:]
    elif args[1] == bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௔"):
      bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௕")
      args = args[2:]
    elif args[1] == bstack11lllll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ௖"):
      bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ௗ")
      args = args[2:]
    elif args[1] == bstack11lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ௘"):
      bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௙")
      args = args[2:]
    elif args[1] == bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௚"):
      bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௛")
      args = args[2:]
    elif args[1] == bstack11lllll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௜"):
      bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௝")
      args = args[2:]
    else:
      if not bstack11lllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ௞") in CONFIG or str(CONFIG[bstack11lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௟")]).lower() in [bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௠"), bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ௡")]:
        bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௢")
        args = args[1:]
      elif str(CONFIG[bstack11lllll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௣")]).lower() == bstack11lllll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௤"):
        bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௥")
        args = args[1:]
      elif str(CONFIG[bstack11lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௦")]).lower() == bstack11lllll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௧"):
        bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ௨")
        args = args[1:]
      elif str(CONFIG[bstack11lllll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ௩")]).lower() == bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௪"):
        bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௫")
        args = args[1:]
      elif str(CONFIG[bstack11lllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ௬")]).lower() == bstack11lllll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ௭"):
        bstack1ll11ll1ll_opy_ = bstack11lllll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ௮")
        args = args[1:]
      else:
        os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ௯")] = bstack1ll11ll1ll_opy_
        bstack1l11lllll_opy_(bstack1l111llll_opy_)
  os.environ[bstack11lllll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ௰")] = bstack1ll11ll1ll_opy_
  bstack11l1l1l1_opy_ = bstack1ll11ll1ll_opy_
  global bstack1l1lll111l_opy_
  if bstack1ll1l1lll_opy_:
    try:
      os.environ[bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ௱")] = bstack1ll11ll1ll_opy_
      bstack1lll111l1l_opy_(bstack11llllll1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l1l1l11l_opy_.format(str(e)))
  global bstack11l1ll1l_opy_
  global bstack1ll1lll111_opy_
  global bstack11111l11_opy_
  global bstack1l1l1ll1l_opy_
  global bstack111l1llll_opy_
  global bstack1l1l1l1lll_opy_
  global bstack1l1ll1lll1_opy_
  global bstack1ll11ll111_opy_
  global bstack1lll1ll11l_opy_
  global bstack11l11l11_opy_
  global bstack1llll11ll1_opy_
  global bstack1llll1ll1l_opy_
  global bstack111ll1l1l_opy_
  global bstack1ll1ll11ll_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1llllll11l_opy_
  global bstack1lll1lll1_opy_
  global bstack11ll11l1_opy_
  global bstack1l1ll11lll_opy_
  global bstack1lll1l11ll_opy_
  global bstack11l111l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1ll1l_opy_ = webdriver.Remote.__init__
    bstack1ll1lll111_opy_ = WebDriver.quit
    bstack1llll1ll1l_opy_ = WebDriver.close
    bstack1l1l1l1ll_opy_ = WebDriver.get
    bstack11l111l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1lll111l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack1llll1lll1_opy_
    from QWeb.keywords import browser
    bstack1llll1lll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1lll1l111_opy_(CONFIG) and bstack1111l1lll_opy_():
    if bstack1l1l11lll1_opy_() < version.parse(bstack1111ll11_opy_):
      logger.error(bstack11ll11ll1_opy_.format(bstack1l1l11lll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1llllll11l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll11l1111_opy_.format(str(e)))
  if bstack1ll11ll1ll_opy_ != bstack11lllll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௲") or (bstack1ll11ll1ll_opy_ == bstack11lllll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ௳") and not bstack1ll1l1lll_opy_):
    bstack11l11111_opy_()
  if (bstack1ll11ll1ll_opy_ in [bstack11lllll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௴"), bstack11lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௵"), bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௶")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l1l1ll11l_opy_
        bstack1l1l1l1lll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1lll1l1lll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack111l1llll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll1l1llll_opy_ + str(e))
    except Exception as e:
      bstack1ll111llll_opy_(e, bstack1lll1l1lll_opy_)
    if bstack1ll11ll1ll_opy_ != bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ௷"):
      bstack11ll111l_opy_()
    bstack11111l11_opy_ = Output.start_test
    bstack1l1l1ll1l_opy_ = Output.end_test
    bstack1l1ll1lll1_opy_ = TestStatus.__init__
    bstack1lll1ll11l_opy_ = pabot._run
    bstack11l11l11_opy_ = QueueItem.__init__
    bstack1llll11ll1_opy_ = pabot._create_command_for_execution
    bstack1l1ll11lll_opy_ = pabot._report_results
  if bstack1ll11ll1ll_opy_ == bstack11lllll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௸"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll111llll_opy_(e, bstack1l1lllll11_opy_)
    bstack111ll1l1l_opy_ = Runner.run_hook
    bstack1ll1ll11ll_opy_ = Step.run
  if bstack1ll11ll1ll_opy_ == bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௹"):
    try:
      from _pytest.config import Config
      bstack1lll1lll1_opy_ = Config.getoption
      from _pytest import runner
      bstack11ll11l1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11l11lll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1lll1l11ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11lllll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ௺"))
  if bstack1ll11ll1ll_opy_ in bstack111lll111_opy_:
    try:
      framework_name = bstack11lllll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ௻") if bstack1ll11ll1ll_opy_ in [bstack11lllll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௼"), bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௽"), bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ௾")] else bstack11l11l1l1_opy_(bstack1ll11ll1ll_opy_)
      bstack1ll1llll1l_opy_.launch(CONFIG, {
        bstack11lllll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭௿"): bstack11lllll_opy_ (u"࠭ࡻ࠱ࡿ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬఀ").format(framework_name) if bstack1ll11ll1ll_opy_ == bstack11lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧఁ") and bstack1ll1l111l1_opy_() else framework_name,
        bstack11lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬం"): bstack1lll11l111_opy_(framework_name),
        bstack11lllll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧః"): __version__
      })
    except Exception as e:
      logger.debug(bstack1ll1ll1ll1_opy_.format(bstack11lllll_opy_ (u"ࠪࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪఄ"), str(e)))
  if bstack1ll11ll1ll_opy_ in bstack1l1l11111_opy_:
    try:
      framework_name = bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪఅ") if bstack1ll11ll1ll_opy_ in [bstack11lllll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫఆ"), bstack11lllll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬఇ")] else bstack1ll11ll1ll_opy_
      if bstack1l1l111l_opy_ and bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧఈ") in CONFIG and CONFIG[bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨఉ")] == True:
        if bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩఊ") in CONFIG:
          os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫఋ")] = os.getenv(bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬఌ"), json.dumps(CONFIG[bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ఍")]))
          CONFIG[bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ఎ")].pop(bstack11lllll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬఏ"), None)
          CONFIG[bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨఐ")].pop(bstack11lllll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ఑"), None)
        bstack1l11ll11_opy_, bstack1111l11l_opy_ = bstack1111ll111_opy_.bstack111ll1ll_opy_(CONFIG, bstack1ll11ll1ll_opy_, bstack1lll11l111_opy_(framework_name))
        if not bstack1l11ll11_opy_ is None:
          os.environ[bstack11lllll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨఒ")] = bstack1l11ll11_opy_
          os.environ[bstack11lllll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤ࡚ࡅࡔࡖࡢࡖ࡚ࡔ࡟ࡊࡆࠪఓ")] = str(bstack1111l11l_opy_)
    except Exception as e:
      logger.debug(bstack1ll1ll1ll1_opy_.format(bstack11lllll_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬఔ"), str(e)))
  if bstack1ll11ll1ll_opy_ == bstack11lllll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭క"):
    bstack1ll1l11ll_opy_ = True
    if bstack1ll1l1lll_opy_ and bstack111l1l111_opy_:
      bstack1ll11111l_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫఖ"), {}).get(bstack11lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪగ"))
      bstack1lll11llll_opy_(bstack1l1l1l1l_opy_)
    elif bstack1ll1l1lll_opy_:
      bstack1ll11111l_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ఘ"), {}).get(bstack11lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬఙ"))
      global bstack1lll11l1ll_opy_
      try:
        if bstack1ll1ll111l_opy_(bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧచ")]) and multiprocessing.current_process().name == bstack11lllll_opy_ (u"ࠬ࠶ࠧఛ"):
          bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩజ")].remove(bstack11lllll_opy_ (u"ࠧ࠮࡯ࠪఝ"))
          bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఞ")].remove(bstack11lllll_opy_ (u"ࠩࡳࡨࡧ࠭ట"))
          bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఠ")] = bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧడ")][0]
          with open(bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఢ")], bstack11lllll_opy_ (u"࠭ࡲࠨణ")) as f:
            bstack11ll1111l_opy_ = f.read()
          bstack11l1l1lll_opy_ = bstack11lllll_opy_ (u"ࠢࠣࠤࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡥ࡭ࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡁࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࠫࡿࢂ࠯࠻ࠡࡨࡵࡳࡲࠦࡰࡥࡤࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡔࡩࡨ࠻ࠡࡱࡪࡣࡩࡨࠠ࠾ࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫࠼ࠌࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࡸࡷࡿ࠺ࠋࠢࠣࠤࠥࡧࡲࡨࠢࡀࠤࡸࡺࡲࠩ࡫ࡱࡸ࠭ࡧࡲࡨࠫ࠮࠵࠵࠯ࠊࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࡐࡥࡤ࠱ࡨࡴࡥࡢࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࡔࡩࡨࠨࠪ࠰ࡶࡩࡹࡥࡴࡳࡣࡦࡩ࠭࠯࡜࡯ࠤࠥࠦత").format(str(bstack1ll1l1lll_opy_))
          bstack1lll1l11_opy_ = bstack11l1l1lll_opy_ + bstack11ll1111l_opy_
          bstack1llll111ll_opy_ = bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫథ")] + bstack11lllll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡸࡪࡳࡰ࠯ࡲࡼࠫద")
          with open(bstack1llll111ll_opy_, bstack11lllll_opy_ (u"ࠪࡻࠬధ")):
            pass
          with open(bstack1llll111ll_opy_, bstack11lllll_opy_ (u"ࠦࡼ࠱ࠢన")) as f:
            f.write(bstack1lll1l11_opy_)
          import subprocess
          bstack1111lll1l_opy_ = subprocess.run([bstack11lllll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧ఩"), bstack1llll111ll_opy_])
          if os.path.exists(bstack1llll111ll_opy_):
            os.unlink(bstack1llll111ll_opy_)
          os._exit(bstack1111lll1l_opy_.returncode)
        else:
          if bstack1ll1ll111l_opy_(bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩప")]):
            bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఫ")].remove(bstack11lllll_opy_ (u"ࠨ࠯ࡰࠫబ"))
            bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬభ")].remove(bstack11lllll_opy_ (u"ࠪࡴࡩࡨࠧమ"))
            bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧయ")] = bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨర")][0]
          bstack1lll11llll_opy_(bstack1l1l1l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩఱ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11lllll_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩల")] = bstack11lllll_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪళ")
          mod_globals[bstack11lllll_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫఴ")] = os.path.abspath(bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭వ")])
          exec(open(bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧశ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11lllll_opy_ (u"ࠬࡉࡡࡶࡩ࡫ࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠬష").format(str(e)))
          for driver in bstack1lll11l1ll_opy_:
            bstack1lll1ll1ll_opy_.append({
              bstack11lllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫస"): bstack1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪహ")],
              bstack11lllll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ఺"): str(e),
              bstack11lllll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ఻"): multiprocessing.current_process().name
            })
            bstack1lll1l11l1_opy_(driver, bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦ఼ࠪ"), bstack11lllll_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢఽ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1lll11l1ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1ll11ll11_opy_, CONFIG, logger)
      bstack111l111ll_opy_()
      bstack1l1llll1ll_opy_()
      bstack1lll11l11_opy_ = {
        bstack11lllll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨా"): args[0],
        bstack11lllll_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭ి"): CONFIG,
        bstack11lllll_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨీ"): bstack111ll1l1_opy_,
        bstack11lllll_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪు"): bstack1ll11ll11_opy_
      }
      percy.bstack111ll1lll_opy_()
      if bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬూ") in CONFIG:
        bstack1lllll1ll1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1llll_opy_ = manager.list()
        if bstack1ll1ll111l_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ృ")]):
            if index == 0:
              bstack1lll11l11_opy_[bstack11lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧౄ")] = args
            bstack1lllll1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1lll11l11_opy_, bstack1lll1llll_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౅")]):
            bstack1lllll1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1lll11l11_opy_, bstack1lll1llll_opy_)))
        for t in bstack1lllll1ll1_opy_:
          t.start()
        for t in bstack1lllll1ll1_opy_:
          t.join()
        bstack1lllll11ll_opy_ = list(bstack1lll1llll_opy_)
      else:
        if bstack1ll1ll111l_opy_(args):
          bstack1lll11l11_opy_[bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩె")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1lll11l11_opy_,))
          test.start()
          test.join()
        else:
          bstack1lll11llll_opy_(bstack1l1l1l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11lllll_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩే")] = bstack11lllll_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪై")
          mod_globals[bstack11lllll_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ౉")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll11ll1ll_opy_ == bstack11lllll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩొ") or bstack1ll11ll1ll_opy_ == bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪో"):
    percy.init(bstack1ll11ll11_opy_, CONFIG, logger)
    percy.bstack111ll1lll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll111llll_opy_(e, bstack1lll1l1lll_opy_)
    bstack111l111ll_opy_()
    bstack1lll11llll_opy_(bstack1111l11ll_opy_)
    if bstack11lllll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪౌ") in args:
      i = args.index(bstack11lllll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶ్ࠫ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1llll1l11l_opy_))
    args.insert(0, str(bstack11lllll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ౎")))
    if bstack1ll1llll1l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll1l111l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1lll1l111l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11lllll_opy_ (u"ࠣࡔࡒࡆࡔ࡚࡟ࡐࡒࡗࡍࡔࡔࡓࠣ౏"),
        ).parse_args(bstack1ll1l111l_opy_)
        args.insert(args.index(bstack1lll1l111l_opy_[0]), str(bstack11lllll_opy_ (u"ࠩ࠰࠱ࡱ࡯ࡳࡵࡧࡱࡩࡷ࠭౐")))
        args.insert(args.index(bstack1lll1l111l_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡶࡴࡨ࡯ࡵࡡ࡯࡭ࡸࡺࡥ࡯ࡧࡵ࠲ࡵࡿࠧ౑"))))
        if bstack11l1l11l1_opy_(os.environ.get(bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩ౒"))) and str(os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩ౓"), bstack11lllll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ౔"))) != bstack11lllll_opy_ (u"ࠧ࡯ࡷ࡯ࡰౕࠬ"):
          for bstack1ll111111l_opy_ in bstack1lll1l111l_opy_:
            args.remove(bstack1ll111111l_opy_)
          bstack1l1lll1l1l_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗౖࠬ")).split(bstack11lllll_opy_ (u"ࠩ࠯ࠫ౗"))
          for bstack1l1l1ll11_opy_ in bstack1l1lll1l1l_opy_:
            args.append(bstack1l1l1ll11_opy_)
      except Exception as e:
        logger.error(bstack11lllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡷࡸࡦࡩࡨࡪࡰࡪࠤࡱ࡯ࡳࡵࡧࡱࡩࡷࠦࡦࡰࡴࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࠨౘ").format(e))
    pabot.main(args)
  elif bstack1ll11ll1ll_opy_ == bstack11lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬౙ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll111llll_opy_(e, bstack1lll1l1lll_opy_)
    for a in args:
      if bstack11lllll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫౚ") in a:
        bstack11l1lll1l_opy_ = int(a.split(bstack11lllll_opy_ (u"࠭࠺ࠨ౛"))[1])
      if bstack11lllll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ౜") in a:
        bstack1ll11111l_opy_ = str(a.split(bstack11lllll_opy_ (u"ࠨ࠼ࠪౝ"))[1])
      if bstack11lllll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩ౞") in a:
        bstack1lllll1l1_opy_ = str(a.split(bstack11lllll_opy_ (u"ࠪ࠾ࠬ౟"))[1])
    bstack1ll1111l11_opy_ = None
    if bstack11lllll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪౠ") in args:
      i = args.index(bstack11lllll_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫౡ"))
      args.pop(i)
      bstack1ll1111l11_opy_ = args.pop(i)
    if bstack1ll1111l11_opy_ is not None:
      global bstack1l11llll1_opy_
      bstack1l11llll1_opy_ = bstack1ll1111l11_opy_
    bstack1lll11llll_opy_(bstack1111l11ll_opy_)
    run_cli(args)
    if bstack11lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪౢ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll11l11l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll1ll1ll_opy_.append(bstack1ll11l11l_opy_)
  elif bstack1ll11ll1ll_opy_ == bstack11lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧౣ"):
    percy.init(bstack1ll11ll11_opy_, CONFIG, logger)
    percy.bstack111ll1lll_opy_()
    bstack11l11ll11_opy_ = bstack11l111111_opy_(args, logger, CONFIG, bstack1l1l111l_opy_)
    bstack11l11ll11_opy_.bstack1ll1l11l11_opy_()
    bstack111l111ll_opy_()
    bstack1ll1lll1l_opy_ = True
    bstack11l1ll11_opy_ = bstack11l11ll11_opy_.bstack11l11ll1l_opy_()
    bstack11l11ll11_opy_.bstack1lll11l11_opy_(bstack1ll11l11l1_opy_)
    bstack11llll1l_opy_ = bstack11l11ll11_opy_.bstack111llll1l_opy_(bstack11lll11l_opy_, {
      bstack11lllll_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ౤"): bstack111ll1l1_opy_,
      bstack11lllll_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ౥"): bstack1ll11ll11_opy_,
      bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭౦"): bstack1l1l111l_opy_
    })
    bstack1l1111l11_opy_ = 1 if len(bstack11llll1l_opy_) > 0 else 0
  elif bstack1ll11ll1ll_opy_ == bstack11lllll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ౧"):
    try:
      from behave.__main__ import main as bstack1l1ll111l1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll111llll_opy_(e, bstack1l1lllll11_opy_)
    bstack111l111ll_opy_()
    bstack1ll1lll1l_opy_ = True
    bstack11ll1ll1_opy_ = 1
    if bstack11lllll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ౨") in CONFIG:
      bstack11ll1ll1_opy_ = CONFIG[bstack11lllll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭౩")]
    bstack11l1111l_opy_ = int(bstack11ll1ll1_opy_) * int(len(CONFIG[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౪")]))
    config = Configuration(args)
    bstack11lllll1_opy_ = config.paths
    if len(bstack11lllll1_opy_) == 0:
      import glob
      pattern = bstack11lllll_opy_ (u"ࠨࠬ࠭࠳࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠧ౫")
      bstack1llll11l1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1llll11l1l_opy_)
      config = Configuration(args)
      bstack11lllll1_opy_ = config.paths
    bstack1lll11l11l_opy_ = [os.path.normpath(item) for item in bstack11lllll1_opy_]
    bstack1llll11111_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll11l111_opy_ = [item for item in bstack1llll11111_opy_ if item not in bstack1lll11l11l_opy_]
    import platform as pf
    if pf.system().lower() == bstack11lllll_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪ౬"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll11l11l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1llll1l11_opy_)))
                    for bstack1llll1l11_opy_ in bstack1lll11l11l_opy_]
    bstack11l11l111_opy_ = []
    for spec in bstack1lll11l11l_opy_:
      bstack1l1l11l1_opy_ = []
      bstack1l1l11l1_opy_ += bstack1ll11l111_opy_
      bstack1l1l11l1_opy_.append(spec)
      bstack11l11l111_opy_.append(bstack1l1l11l1_opy_)
    execution_items = []
    for bstack1l1l11l1_opy_ in bstack11l11l111_opy_:
      for index, _ in enumerate(CONFIG[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౭")]):
        item = {}
        item[bstack11lllll_opy_ (u"ࠫࡦࡸࡧࠨ౮")] = bstack11lllll_opy_ (u"ࠬࠦࠧ౯").join(bstack1l1l11l1_opy_)
        item[bstack11lllll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ౰")] = index
        execution_items.append(item)
    bstack1111111l1_opy_ = bstack1l1lll1lll_opy_(execution_items, bstack11l1111l_opy_)
    for execution_item in bstack1111111l1_opy_:
      bstack1lllll1ll1_opy_ = []
      for item in execution_item:
        bstack1lllll1ll1_opy_.append(bstack1l111lll_opy_(name=str(item[bstack11lllll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭౱")]),
                                             target=bstack1lll11lll_opy_,
                                             args=(item[bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࠬ౲")],)))
      for t in bstack1lllll1ll1_opy_:
        t.start()
      for t in bstack1lllll1ll1_opy_:
        t.join()
  else:
    bstack1l11lllll_opy_(bstack1l111llll_opy_)
  if not bstack1ll1l1lll_opy_:
    bstack1llll111l1_opy_()
def browserstack_initialize(bstack1l1ll1l1ll_opy_=None):
  run_on_browserstack(bstack1l1ll1l1ll_opy_, None, True)
def bstack1llll111l1_opy_():
  global CONFIG
  global bstack11l1l1l1_opy_
  global bstack1l1111l11_opy_
  bstack1ll1llll1l_opy_.stop()
  bstack1ll1llll1l_opy_.bstack1lll11ll11_opy_()
  if bstack1111ll111_opy_.bstack1l1l11ll1l_opy_(CONFIG):
    bstack1111ll111_opy_.bstack1l1l1l1ll1_opy_()
  [bstack1l1l1ll1_opy_, bstack111111l1l_opy_] = bstack1l1l11l1ll_opy_()
  if bstack1l1l1ll1_opy_ is not None and bstack1ll11llll_opy_() != -1:
    sessions = bstack1lll1lllll_opy_(bstack1l1l1ll1_opy_)
    bstack1l1l1111l_opy_(sessions, bstack111111l1l_opy_)
  if bstack11l1l1l1_opy_ == bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ౳") and bstack1l1111l11_opy_ != 0:
    sys.exit(bstack1l1111l11_opy_)
def bstack11l11l1l1_opy_(bstack1111ll1ll_opy_):
  if bstack1111ll1ll_opy_:
    return bstack1111ll1ll_opy_.capitalize()
  else:
    return bstack11lllll_opy_ (u"ࠪࠫ౴")
def bstack11llllll_opy_(bstack111111l11_opy_):
  if bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ౵") in bstack111111l11_opy_ and bstack111111l11_opy_[bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౶")] != bstack11lllll_opy_ (u"࠭ࠧ౷"):
    return bstack111111l11_opy_[bstack11lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ౸")]
  else:
    bstack1l11l11l1_opy_ = bstack11lllll_opy_ (u"ࠣࠤ౹")
    if bstack11lllll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ౺") in bstack111111l11_opy_ and bstack111111l11_opy_[bstack11lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ౻")] != None:
      bstack1l11l11l1_opy_ += bstack111111l11_opy_[bstack11lllll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ౼")] + bstack11lllll_opy_ (u"ࠧ࠲ࠠࠣ౽")
      if bstack111111l11_opy_[bstack11lllll_opy_ (u"࠭࡯ࡴࠩ౾")] == bstack11lllll_opy_ (u"ࠢࡪࡱࡶࠦ౿"):
        bstack1l11l11l1_opy_ += bstack11lllll_opy_ (u"ࠣ࡫ࡒࡗࠥࠨಀ")
      bstack1l11l11l1_opy_ += (bstack111111l11_opy_[bstack11lllll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ಁ")] or bstack11lllll_opy_ (u"ࠪࠫಂ"))
      return bstack1l11l11l1_opy_
    else:
      bstack1l11l11l1_opy_ += bstack11l11l1l1_opy_(bstack111111l11_opy_[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬಃ")]) + bstack11lllll_opy_ (u"ࠧࠦࠢ಄") + (
              bstack111111l11_opy_[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨಅ")] or bstack11lllll_opy_ (u"ࠧࠨಆ")) + bstack11lllll_opy_ (u"ࠣ࠮ࠣࠦಇ")
      if bstack111111l11_opy_[bstack11lllll_opy_ (u"ࠩࡲࡷࠬಈ")] == bstack11lllll_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦಉ"):
        bstack1l11l11l1_opy_ += bstack11lllll_opy_ (u"ࠦ࡜࡯࡮ࠡࠤಊ")
      bstack1l11l11l1_opy_ += bstack111111l11_opy_[bstack11lllll_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಋ")] or bstack11lllll_opy_ (u"࠭ࠧಌ")
      return bstack1l11l11l1_opy_
def bstack11l111ll1_opy_(bstack1ll1ll1111_opy_):
  if bstack1ll1ll1111_opy_ == bstack11lllll_opy_ (u"ࠢࡥࡱࡱࡩࠧ಍"):
    return bstack11lllll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಎ")
  elif bstack1ll1ll1111_opy_ == bstack11lllll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤಏ"):
    return bstack11lllll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಐ")
  elif bstack1ll1ll1111_opy_ == bstack11lllll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ಑"):
    return bstack11lllll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಒ")
  elif bstack1ll1ll1111_opy_ == bstack11lllll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧಓ"):
    return bstack11lllll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩಔ")
  elif bstack1ll1ll1111_opy_ == bstack11lllll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤಕ"):
    return bstack11lllll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧಖ")
  elif bstack1ll1ll1111_opy_ == bstack11lllll_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦಗ"):
    return bstack11lllll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಘ")
  else:
    return bstack11lllll_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩಙ") + bstack11l11l1l1_opy_(
      bstack1ll1ll1111_opy_) + bstack11lllll_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಚ")
def bstack11l1l1ll_opy_(session):
  return bstack11lllll_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧಛ").format(
    session[bstack11lllll_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬಜ")], bstack11llllll_opy_(session), bstack11l111ll1_opy_(session[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨಝ")]),
    bstack11l111ll1_opy_(session[bstack11lllll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಞ")]),
    bstack11l11l1l1_opy_(session[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬಟ")] or session[bstack11lllll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬಠ")] or bstack11lllll_opy_ (u"࠭ࠧಡ")) + bstack11lllll_opy_ (u"ࠢࠡࠤಢ") + (session[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪಣ")] or bstack11lllll_opy_ (u"ࠩࠪತ")),
    session[bstack11lllll_opy_ (u"ࠪࡳࡸ࠭ಥ")] + bstack11lllll_opy_ (u"ࠦࠥࠨದ") + session[bstack11lllll_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಧ")], session[bstack11lllll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨನ")] or bstack11lllll_opy_ (u"ࠧࠨ಩"),
    session[bstack11lllll_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬಪ")] if session[bstack11lllll_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ಫ")] else bstack11lllll_opy_ (u"ࠪࠫಬ"))
def bstack1l1l1111l_opy_(sessions, bstack111111l1l_opy_):
  try:
    bstack11111111_opy_ = bstack11lllll_opy_ (u"ࠦࠧಭ")
    if not os.path.exists(bstack11ll1lll_opy_):
      os.mkdir(bstack11ll1lll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lllll_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪಮ")), bstack11lllll_opy_ (u"࠭ࡲࠨಯ")) as f:
      bstack11111111_opy_ = f.read()
    bstack11111111_opy_ = bstack11111111_opy_.replace(bstack11lllll_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫರ"), str(len(sessions)))
    bstack11111111_opy_ = bstack11111111_opy_.replace(bstack11lllll_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨಱ"), bstack111111l1l_opy_)
    bstack11111111_opy_ = bstack11111111_opy_.replace(bstack11lllll_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪಲ"),
                                              sessions[0].get(bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧಳ")) if sessions[0] else bstack11lllll_opy_ (u"ࠫࠬ಴"))
    with open(os.path.join(bstack11ll1lll_opy_, bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩವ")), bstack11lllll_opy_ (u"࠭ࡷࠨಶ")) as stream:
      stream.write(bstack11111111_opy_.split(bstack11lllll_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫಷ"))[0])
      for session in sessions:
        stream.write(bstack11l1l1ll_opy_(session))
      stream.write(bstack11111111_opy_.split(bstack11lllll_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬಸ"))[1])
    logger.info(bstack11lllll_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬಹ").format(bstack11ll1lll_opy_));
  except Exception as e:
    logger.debug(bstack1ll1l111ll_opy_.format(str(e)))
def bstack1lll1lllll_opy_(bstack1l1l1ll1_opy_):
  global CONFIG
  try:
    host = bstack11lllll_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭಺") if bstack11lllll_opy_ (u"ࠫࡦࡶࡰࠨ಻") in CONFIG else bstack11lllll_opy_ (u"ࠬࡧࡰࡪ಼ࠩ")
    user = CONFIG[bstack11lllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨಽ")]
    key = CONFIG[bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪಾ")]
    bstack1llllll1l1_opy_ = bstack11lllll_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧಿ") if bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࠭ೀ") in CONFIG else bstack11lllll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬು")
    url = bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠲࡯ࡹ࡯࡯ࠩೂ").format(user, key, host, bstack1llllll1l1_opy_,
                                                                                bstack1l1l1ll1_opy_)
    headers = {
      bstack11lllll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫೃ"): bstack11lllll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩೄ"),
    }
    proxies = bstack11lllllll_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11lllll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ೅")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1lll11_opy_.format(str(e)))
def bstack1l1l11l1ll_opy_():
  global CONFIG
  global bstack1l1l11ll1_opy_
  try:
    if bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫೆ") in CONFIG:
      host = bstack11lllll_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬೇ") if bstack11lllll_opy_ (u"ࠪࡥࡵࡶࠧೈ") in CONFIG else bstack11lllll_opy_ (u"ࠫࡦࡶࡩࠨ೉")
      user = CONFIG[bstack11lllll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧೊ")]
      key = CONFIG[bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩೋ")]
      bstack1llllll1l1_opy_ = bstack11lllll_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ೌ") if bstack11lllll_opy_ (u"ࠨࡣࡳࡴ್ࠬ") in CONFIG else bstack11lllll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ೎")
      url = bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠪ೏").format(user, key, host, bstack1llllll1l1_opy_)
      headers = {
        bstack11lllll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ೐"): bstack11lllll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ೑"),
      }
      if bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೒") in CONFIG:
        params = {bstack11lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ೓"): CONFIG[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ೔")], bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬೕ"): CONFIG[bstack11lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬೖ")]}
      else:
        params = {bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೗"): CONFIG[bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ೘")]}
      proxies = bstack11lllllll_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11111ll1l_opy_ = response.json()[0][bstack11lllll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡦࡺ࡯࡬ࡥࠩ೙")]
        if bstack11111ll1l_opy_:
          bstack111111l1l_opy_ = bstack11111ll1l_opy_[bstack11lllll_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫ೚")].split(bstack11lllll_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣ࠮ࡤࡸ࡭ࡱࡪࠧ೛"))[0] + bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴ࠱ࠪ೜") + bstack11111ll1l_opy_[
            bstack11lllll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ೝ")]
          logger.info(bstack1l1l1llll1_opy_.format(bstack111111l1l_opy_))
          bstack1l1l11ll1_opy_ = bstack11111ll1l_opy_[bstack11lllll_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧೞ")]
          bstack1l1ll11ll1_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ೟")]
          if bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨೠ") in CONFIG:
            bstack1l1ll11ll1_opy_ += bstack11lllll_opy_ (u"ࠧࠡࠩೡ") + CONFIG[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪೢ")]
          if bstack1l1ll11ll1_opy_ != bstack11111ll1l_opy_[bstack11lllll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧೣ")]:
            logger.debug(bstack1ll1l1l111_opy_.format(bstack11111ll1l_opy_[bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨ೤")], bstack1l1ll11ll1_opy_))
          return [bstack11111ll1l_opy_[bstack11lllll_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ೥")], bstack111111l1l_opy_]
    else:
      logger.warn(bstack1ll1llll11_opy_)
  except Exception as e:
    logger.debug(bstack11l1111ll_opy_.format(str(e)))
  return [None, None]
def bstack1llll1l1l1_opy_(url, bstack1ll1l11l1l_opy_=False):
  global CONFIG
  global bstack1111l111_opy_
  if not bstack1111l111_opy_:
    hostname = bstack1l1lll1l11_opy_(url)
    is_private = bstack1l1llll11l_opy_(hostname)
    if (bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ೦") in CONFIG and not bstack11l1l11l1_opy_(CONFIG[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ೧")])) and (is_private or bstack1ll1l11l1l_opy_):
      bstack1111l111_opy_ = hostname
def bstack1l1lll1l11_opy_(url):
  return urlparse(url).hostname
def bstack1l1llll11l_opy_(hostname):
  for bstack1111ll11l_opy_ in bstack1ll1111ll1_opy_:
    regex = re.compile(bstack1111ll11l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11l1l1l11_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11l1lll1l_opy_
  if not bstack1111ll111_opy_.bstack1ll1ll1lll_opy_(CONFIG, bstack11l1lll1l_opy_):
    logger.warning(bstack11lllll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ೨"))
    return {}
  try:
    results = driver.execute_script(bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮ࡲࡦࡵࡲࡰࡻ࡫ࠬࠡࡴࡨ࡮ࡪࡩࡴࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡶࡾࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࡺࡪࡴࡴࠡ࠿ࠣࡲࡪࡽࠠࡄࡷࡶࡸࡴࡳࡅࡷࡧࡱࡸ࠭࠭ࡁ࠲࠳࡜ࡣ࡙ࡇࡐࡠࡉࡈࡘࡤࡘࡅࡔࡗࡏࡘࡘ࠭ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡪࡳࠦ࠽ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬࡪࡼࡥ࡯ࡶࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡸࡥ࡮ࡱࡹࡩࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡖࡊ࡙ࡕࡍࡖࡖࡣࡗࡋࡓࡑࡑࡑࡗࡊ࠭ࠬࠡࡨࡱ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡴࡱ࡯ࡺࡪ࠮ࡥࡷࡧࡱࡸ࠳ࡪࡥࡵࡣ࡬ࡰ࠳ࡪࡡࡵࡣࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡔࡈࡗࡕࡕࡎࡔࡇࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡪࡩࡴࡲࡤࡸࡨ࡮ࡅࡷࡧࡱࡸ࠭࡫ࡶࡦࡰࡷ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠦࡣࡢࡶࡦ࡬ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩ࡯࡫ࡣࡵࠪࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠣࠤࠥ೩"))
    return results
  except Exception:
    logger.error(bstack11lllll_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ೪"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11l1lll1l_opy_
  if not bstack1111ll111_opy_.bstack1ll1ll1lll_opy_(CONFIG, bstack11l1lll1l_opy_):
    logger.warning(bstack11lllll_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴ࠢ೫"))
    return {}
  try:
    bstack1ll1lll1l1_opy_ = driver.execute_script(bstack11lllll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪࡵࡩࡸࡵ࡬ࡷࡧ࠯ࠤࡷ࡫ࡪࡦࡥࡷ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࡶࡦࡰࡷࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣࡌࡋࡔࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡖ࡙ࡒࡓࡁࡓ࡛ࠪ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡧࡰࠣࡁࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩࡧࡹࡩࡳࡺࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡵࡩࡲࡵࡶࡦࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡹ࡯࡭ࡸࡨࠬࡪࡼࡥ࡯ࡶ࠱ࡨࡪࡺࡡࡪ࡮࠱ࡷࡺࡳ࡭ࡢࡴࡼ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡡࡥࡦࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡖ࡙ࡒࡓࡁࡓ࡛ࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࡸࡨࡲࡹ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠡࡥࡤࡸࡨ࡮ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡪࡦࡥࡷࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࡿࠬ࠿ࠏࠦࠠࠡࠢࠥࠦࠧ೬"))
    return bstack1ll1lll1l1_opy_
  except Exception:
    logger.error(bstack11lllll_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨ೭"))
    return {}