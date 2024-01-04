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
from browserstack_sdk.bstack11llll111_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll1l1ll1_opy_ import bstack1lll11111l_opy_
import time
import requests
def bstack1l1111l11_opy_():
  global CONFIG
  headers = {
        bstack1lll11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1lll11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1111l1l11_opy_(CONFIG, bstack1lllll111l_opy_)
  try:
    response = requests.get(bstack1lllll111l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1ll11l1l_opy_ = response.json()[bstack1lll11l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1111ll11l_opy_.format(response.json()))
      return bstack1ll11l1l_opy_
    else:
      logger.debug(bstack1l1l1l1111_opy_.format(bstack1lll11l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l1l1l1111_opy_.format(e))
def bstack1llll1l1l_opy_(hub_url):
  global CONFIG
  url = bstack1lll11l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1lll11l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1lll11l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1lll11l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1111l1l11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l1l111_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll11l1111_opy_.format(hub_url, e))
def bstack1ll11l1ll1_opy_():
  try:
    global bstack1l1l1l11_opy_
    bstack1ll11l1l_opy_ = bstack1l1111l11_opy_()
    bstack1l11lll1_opy_ = []
    results = []
    for bstack1l1l1l1lll_opy_ in bstack1ll11l1l_opy_:
      bstack1l11lll1_opy_.append(bstack1lll1l1ll1_opy_(target=bstack1llll1l1l_opy_,args=(bstack1l1l1l1lll_opy_,)))
    for t in bstack1l11lll1_opy_:
      t.start()
    for t in bstack1l11lll1_opy_:
      results.append(t.join())
    bstack1ll1lllll1_opy_ = {}
    for item in results:
      hub_url = item[bstack1lll11l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1lll11l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1ll1lllll1_opy_[hub_url] = latency
    bstack111lll111_opy_ = min(bstack1ll1lllll1_opy_, key= lambda x: bstack1ll1lllll1_opy_[x])
    bstack1l1l1l11_opy_ = bstack111lll111_opy_
    logger.debug(bstack1ll1lll1_opy_.format(bstack111lll111_opy_))
  except Exception as e:
    logger.debug(bstack1llllll11l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l1llllll1_opy_, bstack1lll1l1l1l_opy_, bstack11l1l1ll1_opy_, bstack1lll11ll_opy_, Notset, bstack11ll1ll11_opy_, \
  bstack1lll1ll1l1_opy_, bstack11l111ll1_opy_, bstack1l1l1l11l1_opy_, bstack1ll11111ll_opy_, bstack1111l111_opy_, bstack1lll11lll1_opy_, bstack1111l111l_opy_, \
  bstack1llllllll1_opy_, bstack1l11llll_opy_, bstack1l1lll1l11_opy_, bstack1llll1111_opy_, bstack1llll1l11l_opy_, bstack11l111111_opy_, \
  bstack1l1ll11l11_opy_, bstack1l1l1ll11_opy_
from bstack_utils.bstack1l1l1l111_opy_ import bstack1l1ll1l1_opy_
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1l1111l1_opy_, bstack1llllll1ll_opy_
from bstack_utils.bstack1l1llll111_opy_ import bstack1l11ll1ll_opy_
from bstack_utils.proxy import bstack1l1l11ll11_opy_, bstack1111l1l11_opy_, bstack1ll1ll1l11_opy_, bstack1ll111llll_opy_
import bstack_utils.bstack1ll1lll1l_opy_ as bstack111ll11l1_opy_
from browserstack_sdk.bstack1lll1l1l11_opy_ import *
from browserstack_sdk.bstack111lllll_opy_ import *
from bstack_utils.bstack1ll111lll1_opy_ import bstack11ll1l111_opy_
bstack1l1l1l11l_opy_ = bstack1lll11l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1ll1l11ll_opy_ = bstack1lll11l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1llllllll_opy_ = None
CONFIG = {}
bstack11ll11ll1_opy_ = {}
bstack1lll1111_opy_ = {}
bstack1l1lllll1l_opy_ = None
bstack1l1ll11111_opy_ = None
bstack1l1ll1ll1_opy_ = None
bstack1ll1l1l111_opy_ = -1
bstack111llllll_opy_ = 0
bstack11l111ll_opy_ = bstack1ll11ll11_opy_
bstack1ll1l111ll_opy_ = 1
bstack1l111l1l_opy_ = False
bstack1ll11lll_opy_ = False
bstack11l1111l1_opy_ = bstack1lll11l_opy_ (u"ࠨࠩࢂ")
bstack1l1lllll11_opy_ = bstack1lll11l_opy_ (u"ࠩࠪࢃ")
bstack111l1ll1_opy_ = False
bstack1ll1ll1l_opy_ = True
bstack1l11l1l11_opy_ = bstack1lll11l_opy_ (u"ࠪࠫࢄ")
bstack11l1ll1ll_opy_ = []
bstack1l1l1l11_opy_ = bstack1lll11l_opy_ (u"ࠫࠬࢅ")
bstack11l11l11_opy_ = False
bstack1ll1l11lll_opy_ = None
bstack1111l1l1l_opy_ = None
bstack1l1llll1_opy_ = None
bstack1l1ll1ll11_opy_ = -1
bstack1111l1111_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠬࢄࠧࢆ")), bstack1lll11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack1lll11l_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack111l111l1_opy_ = 0
bstack1ll1ll1lll_opy_ = []
bstack1l1l1lll1l_opy_ = []
bstack1l11l11l1_opy_ = []
bstack1l1lll1lll_opy_ = []
bstack1llll1llll_opy_ = bstack1lll11l_opy_ (u"ࠨࠩࢉ")
bstack1ll11111_opy_ = bstack1lll11l_opy_ (u"ࠩࠪࢊ")
bstack111l11lll_opy_ = False
bstack1l1111lll_opy_ = False
bstack11l11ll1_opy_ = {}
bstack1llll11l_opy_ = None
bstack1l1l11ll_opy_ = None
bstack1lllll1lll_opy_ = None
bstack1lll11llll_opy_ = None
bstack1llll1l1ll_opy_ = None
bstack1l1ll1lll1_opy_ = None
bstack1ll1111l_opy_ = None
bstack1l1lll111_opy_ = None
bstack1ll111l1_opy_ = None
bstack1lllll1111_opy_ = None
bstack1ll1ll11ll_opy_ = None
bstack1l1l11llll_opy_ = None
bstack1llll11l1l_opy_ = None
bstack1ll1ll111_opy_ = None
bstack1l1l1l1l1l_opy_ = None
bstack11llll1ll_opy_ = None
bstack1l111l1ll_opy_ = None
bstack1l1l11ll1_opy_ = None
bstack11111llll_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack11l111l1_opy_ = None
bstack111ll11ll_opy_ = bstack1lll11l_opy_ (u"ࠥࠦࢋ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l111ll_opy_,
                    format=bstack1lll11l_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩࢌ"),
                    datefmt=bstack1lll11l_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧࢍ"),
                    stream=sys.stdout)
bstack1l1l1ll1ll_opy_ = Config.get_instance()
percy = bstack11l111l1l_opy_()
bstack11lll11ll_opy_ = bstack1lll11111l_opy_()
def bstack1lll1l11l1_opy_():
  global CONFIG
  global bstack11l111ll_opy_
  if bstack1lll11l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ") in CONFIG:
    bstack11l111ll_opy_ = bstack111lll11_opy_[CONFIG[bstack1lll11l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ࢏")]]
    logging.getLogger().setLevel(bstack11l111ll_opy_)
def bstack11l1lllll_opy_():
  global CONFIG
  global bstack111l11lll_opy_
  global bstack1l1l1ll1ll_opy_
  bstack1l1l1111_opy_ = bstack11lll111l_opy_(CONFIG)
  if (bstack1lll11l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐") in bstack1l1l1111_opy_ and str(bstack1l1l1111_opy_[bstack1lll11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ࢑")]).lower() == bstack1lll11l_opy_ (u"ࠪࡸࡷࡻࡥࠨ࢒")):
    bstack111l11lll_opy_ = True
  bstack1l1l1ll1ll_opy_.bstack1lllll11ll_opy_(bstack1l1l1111_opy_.get(bstack1lll11l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࢓"), False))
def bstack1111ll111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lll1ll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11ll1l11l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1lll11l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࢔") == args[i].lower() or bstack1lll11l_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࢕") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l11l1l11_opy_
      bstack1l11l1l11_opy_ += bstack1lll11l_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࢖") + path
      return path
  return None
bstack1l11111l_opy_ = re.compile(bstack1lll11l_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂࠦࢗ"))
def bstack1lll1ll1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l11111l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1lll11l_opy_ (u"ࠤࠧࡿࠧ࢘") + group + bstack1lll11l_opy_ (u"ࠥࢁ࢙ࠧ"), os.environ.get(group))
  return value
def bstack1l1l1l1ll1_opy_():
  bstack111111l1l_opy_ = bstack11ll1l11l_opy_()
  if bstack111111l1l_opy_ and os.path.exists(os.path.abspath(bstack111111l1l_opy_)):
    fileName = bstack111111l1l_opy_
  if bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࢚") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࢛ࠩ")])) and not bstack1lll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ࢜") in locals():
    fileName = os.environ[bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢝")]
  if bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ࢞") in locals():
    bstack11l11ll_opy_ = os.path.abspath(fileName)
  else:
    bstack11l11ll_opy_ = bstack1lll11l_opy_ (u"ࠩࠪ࢟")
  bstack1ll1l11l11_opy_ = os.getcwd()
  bstack11lll1l1_opy_ = bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࢠ")
  bstack1ll11ll1ll_opy_ = bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࢡ")
  while (not os.path.exists(bstack11l11ll_opy_)) and bstack1ll1l11l11_opy_ != bstack1lll11l_opy_ (u"ࠧࠨࢢ"):
    bstack11l11ll_opy_ = os.path.join(bstack1ll1l11l11_opy_, bstack11lll1l1_opy_)
    if not os.path.exists(bstack11l11ll_opy_):
      bstack11l11ll_opy_ = os.path.join(bstack1ll1l11l11_opy_, bstack1ll11ll1ll_opy_)
    if bstack1ll1l11l11_opy_ != os.path.dirname(bstack1ll1l11l11_opy_):
      bstack1ll1l11l11_opy_ = os.path.dirname(bstack1ll1l11l11_opy_)
    else:
      bstack1ll1l11l11_opy_ = bstack1lll11l_opy_ (u"ࠨࠢࢣ")
  if not os.path.exists(bstack11l11ll_opy_):
    bstack11l1llll_opy_(
      bstack1111l11ll_opy_.format(os.getcwd()))
  try:
    with open(bstack11l11ll_opy_, bstack1lll11l_opy_ (u"ࠧࡳࠩࢤ")) as stream:
      yaml.add_implicit_resolver(bstack1lll11l_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࢥ"), bstack1l11111l_opy_)
      yaml.add_constructor(bstack1lll11l_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࢦ"), bstack1lll1ll1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11l11ll_opy_, bstack1lll11l_opy_ (u"ࠪࡶࠬࢧ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11l1llll_opy_(bstack11111l1ll_opy_.format(str(exc)))
def bstack1111ll1l1_opy_(config):
  bstack1llll11lll_opy_ = bstack1l1l11l1l_opy_(config)
  for option in list(bstack1llll11lll_opy_):
    if option.lower() in bstack1ll1l111l1_opy_ and option != bstack1ll1l111l1_opy_[option.lower()]:
      bstack1llll11lll_opy_[bstack1ll1l111l1_opy_[option.lower()]] = bstack1llll11lll_opy_[option]
      del bstack1llll11lll_opy_[option]
  return config
def bstack1ll1ll11l1_opy_():
  global bstack1lll1111_opy_
  for key, bstack1l1lllll1_opy_ in bstack11l1l1l1_opy_.items():
    if isinstance(bstack1l1lllll1_opy_, list):
      for var in bstack1l1lllll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lll1111_opy_[key] = os.environ[var]
          break
    elif bstack1l1lllll1_opy_ in os.environ and os.environ[bstack1l1lllll1_opy_] and str(os.environ[bstack1l1lllll1_opy_]).strip():
      bstack1lll1111_opy_[key] = os.environ[bstack1l1lllll1_opy_]
  if bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ") in os.environ:
    bstack1lll1111_opy_[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢩ")] = {}
    bstack1lll1111_opy_[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")][bstack1lll11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢫ")] = os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࢬ")]
def bstack1ll1111111_opy_():
  global bstack11ll11ll1_opy_
  global bstack1l11l1l11_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1lll11l_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢭ").lower() == val.lower():
      bstack11ll11ll1_opy_[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢮ")] = {}
      bstack11ll11ll1_opy_[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢯ")][bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11ll111l_opy_ in bstack1l111111l_opy_.items():
    if isinstance(bstack11ll111l_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11ll111l_opy_:
          if idx < len(sys.argv) and bstack1lll11l_opy_ (u"࠭࠭࠮ࠩࢱ") + var.lower() == val.lower() and not key in bstack11ll11ll1_opy_:
            bstack11ll11ll1_opy_[key] = sys.argv[idx + 1]
            bstack1l11l1l11_opy_ += bstack1lll11l_opy_ (u"ࠧࠡ࠯࠰ࠫࢲ") + var + bstack1lll11l_opy_ (u"ࠨࠢࠪࢳ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1lll11l_opy_ (u"ࠩ࠰࠱ࠬࢴ") + bstack11ll111l_opy_.lower() == val.lower() and not key in bstack11ll11ll1_opy_:
          bstack11ll11ll1_opy_[key] = sys.argv[idx + 1]
          bstack1l11l1l11_opy_ += bstack1lll11l_opy_ (u"ࠪࠤ࠲࠳ࠧࢵ") + bstack11ll111l_opy_ + bstack1lll11l_opy_ (u"ࠫࠥ࠭ࢶ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1lll1ll11_opy_(config):
  bstack1ll1ll1l1l_opy_ = config.keys()
  for bstack1l1l1ll1l_opy_, bstack111l111l_opy_ in bstack1ll1lll11l_opy_.items():
    if bstack111l111l_opy_ in bstack1ll1ll1l1l_opy_:
      config[bstack1l1l1ll1l_opy_] = config[bstack111l111l_opy_]
      del config[bstack111l111l_opy_]
  for bstack1l1l1ll1l_opy_, bstack111l111l_opy_ in bstack1l1lll111l_opy_.items():
    if isinstance(bstack111l111l_opy_, list):
      for bstack1llll1lll1_opy_ in bstack111l111l_opy_:
        if bstack1llll1lll1_opy_ in bstack1ll1ll1l1l_opy_:
          config[bstack1l1l1ll1l_opy_] = config[bstack1llll1lll1_opy_]
          del config[bstack1llll1lll1_opy_]
          break
    elif bstack111l111l_opy_ in bstack1ll1ll1l1l_opy_:
      config[bstack1l1l1ll1l_opy_] = config[bstack111l111l_opy_]
      del config[bstack111l111l_opy_]
  for bstack1llll1lll1_opy_ in list(config):
    for bstack1111llll_opy_ in bstack1ll11111l1_opy_:
      if bstack1llll1lll1_opy_.lower() == bstack1111llll_opy_.lower() and bstack1llll1lll1_opy_ != bstack1111llll_opy_:
        config[bstack1111llll_opy_] = config[bstack1llll1lll1_opy_]
        del config[bstack1llll1lll1_opy_]
  bstack1ll11l111l_opy_ = []
  if bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࢷ") in config:
    bstack1ll11l111l_opy_ = config[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࢸ")]
  for platform in bstack1ll11l111l_opy_:
    for bstack1llll1lll1_opy_ in list(platform):
      for bstack1111llll_opy_ in bstack1ll11111l1_opy_:
        if bstack1llll1lll1_opy_.lower() == bstack1111llll_opy_.lower() and bstack1llll1lll1_opy_ != bstack1111llll_opy_:
          platform[bstack1111llll_opy_] = platform[bstack1llll1lll1_opy_]
          del platform[bstack1llll1lll1_opy_]
  for bstack1l1l1ll1l_opy_, bstack111l111l_opy_ in bstack1l1lll111l_opy_.items():
    for platform in bstack1ll11l111l_opy_:
      if isinstance(bstack111l111l_opy_, list):
        for bstack1llll1lll1_opy_ in bstack111l111l_opy_:
          if bstack1llll1lll1_opy_ in platform:
            platform[bstack1l1l1ll1l_opy_] = platform[bstack1llll1lll1_opy_]
            del platform[bstack1llll1lll1_opy_]
            break
      elif bstack111l111l_opy_ in platform:
        platform[bstack1l1l1ll1l_opy_] = platform[bstack111l111l_opy_]
        del platform[bstack111l111l_opy_]
  for bstack1l111l111_opy_ in bstack1111lll1l_opy_:
    if bstack1l111l111_opy_ in config:
      if not bstack1111lll1l_opy_[bstack1l111l111_opy_] in config:
        config[bstack1111lll1l_opy_[bstack1l111l111_opy_]] = {}
      config[bstack1111lll1l_opy_[bstack1l111l111_opy_]].update(config[bstack1l111l111_opy_])
      del config[bstack1l111l111_opy_]
  for platform in bstack1ll11l111l_opy_:
    for bstack1l111l111_opy_ in bstack1111lll1l_opy_:
      if bstack1l111l111_opy_ in list(platform):
        if not bstack1111lll1l_opy_[bstack1l111l111_opy_] in platform:
          platform[bstack1111lll1l_opy_[bstack1l111l111_opy_]] = {}
        platform[bstack1111lll1l_opy_[bstack1l111l111_opy_]].update(platform[bstack1l111l111_opy_])
        del platform[bstack1l111l111_opy_]
  config = bstack1111ll1l1_opy_(config)
  return config
def bstack1ll1l11l1l_opy_(config):
  global bstack1l1lllll11_opy_
  if bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࢹ") in config and str(config[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢺ")]).lower() != bstack1lll11l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࢻ"):
    if not bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢼ") in config:
      config[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢽ")] = {}
    if not bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢾ") in config[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")]:
      bstack1ll11ll1l_opy_ = datetime.datetime.now()
      bstack11lll1111_opy_ = bstack1ll11ll1l_opy_.strftime(bstack1lll11l_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫࣀ"))
      hostname = socket.gethostname()
      bstack1l11llll1_opy_ = bstack1lll11l_opy_ (u"ࠨࠩࣁ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1lll11l_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫࣂ").format(bstack11lll1111_opy_, hostname, bstack1l11llll1_opy_)
      config[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣃ")][bstack1lll11l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")] = identifier
    bstack1l1lllll11_opy_ = config[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣅ")][bstack1lll11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")]
  return config
def bstack1ll1l111_opy_():
  bstack1lll1lllll_opy_ =  bstack1ll11111ll_opy_()[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭ࣇ")]
  return bstack1lll1lllll_opy_ if bstack1lll1lllll_opy_ else -1
def bstack1l1111ll_opy_(bstack1lll1lllll_opy_):
  global CONFIG
  if not bstack1lll11l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ") in CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")]:
    return
  CONFIG[bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")] = CONFIG[bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋")].replace(
    bstack1lll11l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ࣌"),
    str(bstack1lll1lllll_opy_)
  )
def bstack1lll111ll_opy_():
  global CONFIG
  if not bstack1lll11l_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬ࣍") in CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣎")]:
    return
  bstack1ll11ll1l_opy_ = datetime.datetime.now()
  bstack11lll1111_opy_ = bstack1ll11ll1l_opy_.strftime(bstack1lll11l_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࣏࠭"))
  CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")] = CONFIG[bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")].replace(
    bstack1lll11l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿ࣒ࠪ"),
    bstack11lll1111_opy_
  )
def bstack1lllll1ll_opy_():
  global CONFIG
  if bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ") in CONFIG and not bool(CONFIG[bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]):
    del CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ")]
    return
  if not bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ") in CONFIG:
    CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣗ")] = bstack1lll11l_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣘ")
  if bstack1lll11l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪࣙ") in CONFIG[bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    bstack1lll111ll_opy_()
    os.environ[bstack1lll11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪࣛ")] = CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣜ")]
  if not bstack1lll11l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣝ") in CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣞ")]:
    return
  bstack1lll1lllll_opy_ = bstack1lll11l_opy_ (u"ࠪࠫࣟ")
  bstack11l1ll111_opy_ = bstack1ll1l111_opy_()
  if bstack11l1ll111_opy_ != -1:
    bstack1lll1lllll_opy_ = bstack1lll11l_opy_ (u"ࠫࡈࡏࠠࠨ࣠") + str(bstack11l1ll111_opy_)
  if bstack1lll1lllll_opy_ == bstack1lll11l_opy_ (u"ࠬ࠭࣡"):
    bstack1ll11l11ll_opy_ = bstack11l1111ll_opy_(CONFIG[bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࣢")])
    if bstack1ll11l11ll_opy_ != -1:
      bstack1lll1lllll_opy_ = str(bstack1ll11l11ll_opy_)
  if bstack1lll1lllll_opy_:
    bstack1l1111ll_opy_(bstack1lll1lllll_opy_)
    os.environ[bstack1lll11l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࣣࠫ")] = CONFIG[bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")]
def bstack1ll1l1l1l_opy_(bstack11l1l1111_opy_, bstack1l1l11l1l1_opy_, path):
  bstack111l111ll_opy_ = {
    bstack1lll11l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣥ"): bstack1l1l11l1l1_opy_
  }
  if os.path.exists(path):
    bstack1l1l1ll1l1_opy_ = json.load(open(path, bstack1lll11l_opy_ (u"ࠪࡶࡧࣦ࠭")))
  else:
    bstack1l1l1ll1l1_opy_ = {}
  bstack1l1l1ll1l1_opy_[bstack11l1l1111_opy_] = bstack111l111ll_opy_
  with open(path, bstack1lll11l_opy_ (u"ࠦࡼ࠱ࠢࣧ")) as outfile:
    json.dump(bstack1l1l1ll1l1_opy_, outfile)
def bstack11l1111ll_opy_(bstack11l1l1111_opy_):
  bstack11l1l1111_opy_ = str(bstack11l1l1111_opy_)
  bstack1lll111l11_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠬࢄࠧࣨ")), bstack1lll11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࣩ࠭"))
  try:
    if not os.path.exists(bstack1lll111l11_opy_):
      os.makedirs(bstack1lll111l11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠧࡿࠩ࣪")), bstack1lll11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ࣫"), bstack1lll11l_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ࣬"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1lll11l_opy_ (u"ࠪࡻ࣭ࠬ")):
        pass
      with open(file_path, bstack1lll11l_opy_ (u"ࠦࡼ࠱࣮ࠢ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1lll11l_opy_ (u"ࠬࡸ࣯ࠧ")) as bstack1l111ll1l_opy_:
      bstack1ll1ll11l_opy_ = json.load(bstack1l111ll1l_opy_)
    if bstack11l1l1111_opy_ in bstack1ll1ll11l_opy_:
      bstack11111l1l_opy_ = bstack1ll1ll11l_opy_[bstack11l1l1111_opy_][bstack1lll11l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣰࠪ")]
      bstack11111ll11_opy_ = int(bstack11111l1l_opy_) + 1
      bstack1ll1l1l1l_opy_(bstack11l1l1111_opy_, bstack11111ll11_opy_, file_path)
      return bstack11111ll11_opy_
    else:
      bstack1ll1l1l1l_opy_(bstack11l1l1111_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11111l111_opy_.format(str(e)))
    return -1
def bstack1l1l1lll11_opy_(config):
  if not config[bstack1lll11l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࣱࠩ")] or not config[bstack1lll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࣲࠫ")]:
    return True
  else:
    return False
def bstack1ll1l1111l_opy_(config, index=0):
  global bstack111l1ll1_opy_
  bstack1l1lllllll_opy_ = {}
  caps = bstack111l11l1l_opy_ + bstack1lll1lll11_opy_
  if bstack111l1ll1_opy_:
    caps += bstack1l111lll1_opy_
  for key in config:
    if key in caps + [bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ")]:
      continue
    bstack1l1lllllll_opy_[key] = config[key]
  if bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ") in config:
    for bstack11lll1ll1_opy_ in config[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index]:
      if bstack11lll1ll1_opy_ in caps + [bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࣶࠪ"), bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣷ")]:
        continue
      bstack1l1lllllll_opy_[bstack11lll1ll1_opy_] = config[bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ")][index][bstack11lll1ll1_opy_]
  bstack1l1lllllll_opy_[bstack1lll11l_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࣹࠪ")] = socket.gethostname()
  if bstack1lll11l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࣺࠪ") in bstack1l1lllllll_opy_:
    del (bstack1l1lllllll_opy_[bstack1lll11l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫࣻ")])
  return bstack1l1lllllll_opy_
def bstack1l1ll11l_opy_(config):
  global bstack111l1ll1_opy_
  bstack1lllllll11_opy_ = {}
  caps = bstack1lll1lll11_opy_
  if bstack111l1ll1_opy_:
    caps += bstack1l111lll1_opy_
  for key in caps:
    if key in config:
      bstack1lllllll11_opy_[key] = config[key]
  return bstack1lllllll11_opy_
def bstack1ll1lll1ll_opy_(bstack1l1lllllll_opy_, bstack1lllllll11_opy_):
  bstack11l1l111l_opy_ = {}
  for key in bstack1l1lllllll_opy_.keys():
    if key in bstack1ll1lll11l_opy_:
      bstack11l1l111l_opy_[bstack1ll1lll11l_opy_[key]] = bstack1l1lllllll_opy_[key]
    else:
      bstack11l1l111l_opy_[key] = bstack1l1lllllll_opy_[key]
  for key in bstack1lllllll11_opy_:
    if key in bstack1ll1lll11l_opy_:
      bstack11l1l111l_opy_[bstack1ll1lll11l_opy_[key]] = bstack1lllllll11_opy_[key]
    else:
      bstack11l1l111l_opy_[key] = bstack1lllllll11_opy_[key]
  return bstack11l1l111l_opy_
def bstack1l11ll1l_opy_(config, index=0):
  global bstack111l1ll1_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1lllllll11_opy_ = bstack1l1ll11l_opy_(config)
  bstack1l1lll1l1_opy_ = bstack1lll1lll11_opy_
  bstack1l1lll1l1_opy_ += bstack1lllll11l_opy_
  if bstack111l1ll1_opy_:
    bstack1l1lll1l1_opy_ += bstack1l111lll1_opy_
  if bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ") in config:
    if bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ") in config[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣾ")][index]:
      caps[bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬࣿ")] = config[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index][bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧँ")]
    if bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं") in config[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
      caps[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऄ")] = str(config[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨआ")])
    bstack1l1l1l1l_opy_ = {}
    for bstack1l1l1l1ll_opy_ in bstack1l1lll1l1_opy_:
      if bstack1l1l1l1ll_opy_ in config[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index]:
        if bstack1l1l1l1ll_opy_ == bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫई"):
          try:
            bstack1l1l1l1l_opy_[bstack1l1l1l1ll_opy_] = str(config[bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1l1l1l1ll_opy_] * 1.0)
          except:
            bstack1l1l1l1l_opy_[bstack1l1l1l1ll_opy_] = str(config[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1l1l1l1ll_opy_])
        else:
          bstack1l1l1l1l_opy_[bstack1l1l1l1ll_opy_] = config[bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऋ")][index][bstack1l1l1l1ll_opy_]
        del (config[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩऌ")][index][bstack1l1l1l1ll_opy_])
    bstack1lllllll11_opy_ = update(bstack1lllllll11_opy_, bstack1l1l1l1l_opy_)
  bstack1l1lllllll_opy_ = bstack1ll1l1111l_opy_(config, index)
  for bstack1llll1lll1_opy_ in bstack1lll1lll11_opy_ + [bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऍ"), bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऎ")]:
    if bstack1llll1lll1_opy_ in bstack1l1lllllll_opy_:
      bstack1lllllll11_opy_[bstack1llll1lll1_opy_] = bstack1l1lllllll_opy_[bstack1llll1lll1_opy_]
      del (bstack1l1lllllll_opy_[bstack1llll1lll1_opy_])
  if bstack11ll1ll11_opy_(config):
    bstack1l1lllllll_opy_[bstack1lll11l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩए")] = True
    caps.update(bstack1lllllll11_opy_)
    caps[bstack1lll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫऐ")] = bstack1l1lllllll_opy_
  else:
    bstack1l1lllllll_opy_[bstack1lll11l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫऑ")] = False
    caps.update(bstack1ll1lll1ll_opy_(bstack1l1lllllll_opy_, bstack1lllllll11_opy_))
    if bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ") in caps:
      caps[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧओ")] = caps[bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऔ")]
      del (caps[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭क")])
    if bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख") in caps:
      caps[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬग")] = caps[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬघ")]
      del (caps[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ङ")])
  return caps
def bstack11lll1l1l_opy_():
  global bstack1l1l1l11_opy_
  if bstack1lll1ll1l_opy_() <= version.parse(bstack1lll11l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭च")):
    if bstack1l1l1l11_opy_ != bstack1lll11l_opy_ (u"ࠧࠨछ"):
      return bstack1lll11l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤज") + bstack1l1l1l11_opy_ + bstack1lll11l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨझ")
    return bstack1l1l1l1l11_opy_
  if bstack1l1l1l11_opy_ != bstack1lll11l_opy_ (u"ࠪࠫञ"):
    return bstack1lll11l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨट") + bstack1l1l1l11_opy_ + bstack1lll11l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨठ")
  return bstack1lll1111l1_opy_
def bstack1l1ll11ll_opy_(options):
  return hasattr(options, bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧड"))
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
def bstack1l1111ll1_opy_(options, bstack1111l1l1_opy_):
  for bstack111l1l11l_opy_ in bstack1111l1l1_opy_:
    if bstack111l1l11l_opy_ in [bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬढ"), bstack1lll11l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण")]:
      continue
    if bstack111l1l11l_opy_ in options._experimental_options:
      options._experimental_options[bstack111l1l11l_opy_] = update(options._experimental_options[bstack111l1l11l_opy_],
                                                         bstack1111l1l1_opy_[bstack111l1l11l_opy_])
    else:
      options.add_experimental_option(bstack111l1l11l_opy_, bstack1111l1l1_opy_[bstack111l1l11l_opy_])
  if bstack1lll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत") in bstack1111l1l1_opy_:
    for arg in bstack1111l1l1_opy_[bstack1lll11l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨथ")]:
      options.add_argument(arg)
    del (bstack1111l1l1_opy_[bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩद")])
  if bstack1lll11l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध") in bstack1111l1l1_opy_:
    for ext in bstack1111l1l1_opy_[bstack1lll11l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪन")]:
      options.add_extension(ext)
    del (bstack1111l1l1_opy_[bstack1lll11l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫऩ")])
def bstack11lllllll_opy_(options, bstack1l1llllll_opy_):
  if bstack1lll11l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप") in bstack1l1llllll_opy_:
    for bstack1ll111lll_opy_ in bstack1l1llllll_opy_[bstack1lll11l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")]:
      if bstack1ll111lll_opy_ in options._preferences:
        options._preferences[bstack1ll111lll_opy_] = update(options._preferences[bstack1ll111lll_opy_], bstack1l1llllll_opy_[bstack1lll11l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩब")][bstack1ll111lll_opy_])
      else:
        options.set_preference(bstack1ll111lll_opy_, bstack1l1llllll_opy_[bstack1lll11l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪभ")][bstack1ll111lll_opy_])
  if bstack1lll11l_opy_ (u"ࠬࡧࡲࡨࡵࠪम") in bstack1l1llllll_opy_:
    for arg in bstack1l1llllll_opy_[bstack1lll11l_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      options.add_argument(arg)
def bstack1111ll1ll_opy_(options, bstack1ll1111l1_opy_):
  if bstack1lll11l_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨर") in bstack1ll1111l1_opy_:
    options.use_webview(bool(bstack1ll1111l1_opy_[bstack1lll11l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩऱ")]))
  bstack1l1111ll1_opy_(options, bstack1ll1111l1_opy_)
def bstack1ll11ll111_opy_(options, bstack1l111ll11_opy_):
  for bstack1lll11l1l1_opy_ in bstack1l111ll11_opy_:
    if bstack1lll11l1l1_opy_ in [bstack1lll11l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल"), bstack1lll11l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ")]:
      continue
    options.set_capability(bstack1lll11l1l1_opy_, bstack1l111ll11_opy_[bstack1lll11l1l1_opy_])
  if bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩऴ") in bstack1l111ll11_opy_:
    for arg in bstack1l111ll11_opy_[bstack1lll11l_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      options.add_argument(arg)
  if bstack1lll11l_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪश") in bstack1l111ll11_opy_:
    options.bstack11l1l11l_opy_(bool(bstack1l111ll11_opy_[bstack1lll11l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫष")]))
def bstack111111111_opy_(options, bstack1ll1ll1l1_opy_):
  for bstack1ll11ll1_opy_ in bstack1ll1ll1l1_opy_:
    if bstack1ll11ll1_opy_ in [bstack1lll11l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस"), bstack1lll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह")]:
      continue
    options._options[bstack1ll11ll1_opy_] = bstack1ll1ll1l1_opy_[bstack1ll11ll1_opy_]
  if bstack1lll11l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ") in bstack1ll1ll1l1_opy_:
    for bstack1llll111_opy_ in bstack1ll1ll1l1_opy_[bstack1lll11l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऻ")]:
      options.bstack1ll111l11l_opy_(
        bstack1llll111_opy_, bstack1ll1ll1l1_opy_[bstack1lll11l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")][bstack1llll111_opy_])
  if bstack1lll11l_opy_ (u"࠭ࡡࡳࡩࡶࠫऽ") in bstack1ll1ll1l1_opy_:
    for arg in bstack1ll1ll1l1_opy_[bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬा")]:
      options.add_argument(arg)
def bstack11l1ll1l1_opy_(options, caps):
  if not hasattr(options, bstack1lll11l_opy_ (u"ࠨࡍࡈ࡝ࠬि")):
    return
  if options.KEY == bstack1lll11l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧी") and options.KEY in caps:
    bstack1l1111ll1_opy_(options, caps[bstack1lll11l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨु")])
  elif options.KEY == bstack1lll11l_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩू") and options.KEY in caps:
    bstack11lllllll_opy_(options, caps[bstack1lll11l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪृ")])
  elif options.KEY == bstack1lll11l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧॄ") and options.KEY in caps:
    bstack1ll11ll111_opy_(options, caps[bstack1lll11l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨॅ")])
  elif options.KEY == bstack1lll11l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॆ") and options.KEY in caps:
    bstack1111ll1ll_opy_(options, caps[bstack1lll11l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪे")])
  elif options.KEY == bstack1lll11l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩै") and options.KEY in caps:
    bstack111111111_opy_(options, caps[bstack1lll11l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪॉ")])
def bstack1lll1lll1_opy_(caps):
  global bstack111l1ll1_opy_
  if isinstance(os.environ.get(bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ॊ")), str):
    bstack111l1ll1_opy_ = eval(os.getenv(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧो")))
  if bstack111l1ll1_opy_:
    if bstack1111ll111_opy_() < version.parse(bstack1lll11l_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ौ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1lll11l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ्")
    if bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ") in caps:
      browser = caps[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॏ")]
    elif bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬॐ") in caps:
      browser = caps[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭॑")]
    browser = str(browser).lower()
    if browser == bstack1lll11l_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ॒࠭") or browser == bstack1lll11l_opy_ (u"ࠧࡪࡲࡤࡨࠬ॓"):
      browser = bstack1lll11l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ॔")
    if browser == bstack1lll11l_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪॕ"):
      browser = bstack1lll11l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪॖ")
    if browser not in [bstack1lll11l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॗ"), bstack1lll11l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪक़"), bstack1lll11l_opy_ (u"࠭ࡩࡦࠩख़"), bstack1lll11l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧग़"), bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩज़")]:
      return None
    try:
      package = bstack1lll11l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫड़").format(browser)
      name = bstack1lll11l_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫढ़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1ll11ll_opy_(options):
        return None
      for bstack1llll1lll1_opy_ in caps.keys():
        options.set_capability(bstack1llll1lll1_opy_, caps[bstack1llll1lll1_opy_])
      bstack11l1ll1l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11llllll1_opy_(options, bstack1ll11lll1l_opy_):
  if not bstack1l1ll11ll_opy_(options):
    return
  for bstack1llll1lll1_opy_ in bstack1ll11lll1l_opy_.keys():
    if bstack1llll1lll1_opy_ in bstack1lllll11l_opy_:
      continue
    if bstack1llll1lll1_opy_ in options._caps and type(options._caps[bstack1llll1lll1_opy_]) in [dict, list]:
      options._caps[bstack1llll1lll1_opy_] = update(options._caps[bstack1llll1lll1_opy_], bstack1ll11lll1l_opy_[bstack1llll1lll1_opy_])
    else:
      options.set_capability(bstack1llll1lll1_opy_, bstack1ll11lll1l_opy_[bstack1llll1lll1_opy_])
  bstack11l1ll1l1_opy_(options, bstack1ll11lll1l_opy_)
  if bstack1lll11l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़") in options._caps:
    if options._caps[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")] and options._caps[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")].lower() != bstack1lll11l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨॡ"):
      del options._caps[bstack1lll11l_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧॢ")]
def bstack1111llll1_opy_(proxy_config):
  if bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ") in proxy_config:
    proxy_config[bstack1lll11l_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ।")] = proxy_config[bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ॥")]
    del (proxy_config[bstack1lll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ०")])
  if bstack1lll11l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१") in proxy_config and proxy_config[bstack1lll11l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ२")].lower() != bstack1lll11l_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ३"):
    proxy_config[bstack1lll11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack1lll11l_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪ५")
  if bstack1lll11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩ६") in proxy_config:
    proxy_config[bstack1lll11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ७")] = bstack1lll11l_opy_ (u"࠭ࡰࡢࡥࠪ८")
  return proxy_config
def bstack1l1ll1llll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1lll11l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९") in config:
    return proxy
  config[bstack1lll11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")] = bstack1111llll1_opy_(config[bstack1lll11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨॱ")])
  if proxy == None:
    proxy = Proxy(config[bstack1lll11l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩॲ")])
  return proxy
def bstack1llll11ll_opy_(self):
  global CONFIG
  global bstack1l1l11llll_opy_
  try:
    proxy = bstack1ll1ll1l11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1lll11l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॳ")):
        proxies = bstack1l1l11ll11_opy_(proxy, bstack11lll1l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack111l1llll_opy_ = proxies.popitem()
          if bstack1lll11l_opy_ (u"ࠧࡀ࠯࠰ࠤॴ") in bstack111l1llll_opy_:
            return bstack111l1llll_opy_
          else:
            return bstack1lll11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢॵ") + bstack111l1llll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1lll11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦॶ").format(str(e)))
  return bstack1l1l11llll_opy_(self)
def bstack11l11ll11_opy_():
  global CONFIG
  return bstack1ll111llll_opy_(CONFIG) and bstack1lll11lll1_opy_() and bstack1lll1ll1l_opy_() >= version.parse(bstack1lll1l111l_opy_)
def bstack1l1ll1l1l_opy_():
  global CONFIG
  return (bstack1lll11l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫॷ") in CONFIG or bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॸ") in CONFIG) and bstack1111l111l_opy_()
def bstack1l1l11l1l_opy_(config):
  bstack1llll11lll_opy_ = {}
  if bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॹ") in config:
    bstack1llll11lll_opy_ = config[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॺ")]
  if bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॻ") in config:
    bstack1llll11lll_opy_ = config[bstack1lll11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॼ")]
  proxy = bstack1ll1ll1l11_opy_(config)
  if proxy:
    if proxy.endswith(bstack1lll11l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬॽ")) and os.path.isfile(proxy):
      bstack1llll11lll_opy_[bstack1lll11l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫॾ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1lll11l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧॿ")):
        proxies = bstack1111l1l11_opy_(config, bstack11lll1l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack111l1llll_opy_ = proxies.popitem()
          if bstack1lll11l_opy_ (u"ࠥ࠾࠴࠵ࠢঀ") in bstack111l1llll_opy_:
            parsed_url = urlparse(bstack111l1llll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1lll11l_opy_ (u"ࠦ࠿࠵࠯ࠣঁ") + bstack111l1llll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1llll11lll_opy_[bstack1lll11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨং")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1llll11lll_opy_[bstack1lll11l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩঃ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1llll11lll_opy_[bstack1lll11l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ঄")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1llll11lll_opy_[bstack1lll11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫঅ")] = str(parsed_url.password)
  return bstack1llll11lll_opy_
def bstack11lll111l_opy_(config):
  if bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧআ") in config:
    return config[bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨই")]
  return {}
def bstack1ll11l11l1_opy_(caps):
  global bstack1l1lllll11_opy_
  if bstack1lll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ") in caps:
    caps[bstack1lll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭উ")][bstack1lll11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬঊ")] = True
    if bstack1l1lllll11_opy_:
      caps[bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨঋ")][bstack1lll11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঌ")] = bstack1l1lllll11_opy_
  else:
    caps[bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ঍")] = True
    if bstack1l1lllll11_opy_:
      caps[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ঎")] = bstack1l1lllll11_opy_
def bstack1l1ll1l1l1_opy_():
  global CONFIG
  if bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨএ") in CONFIG and bstack1l1l1ll11_opy_(CONFIG[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঐ")]):
    bstack1llll11lll_opy_ = bstack1l1l11l1l_opy_(CONFIG)
    bstack1l1l1lllll_opy_(CONFIG[bstack1lll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1llll11lll_opy_)
def bstack1l1l1lllll_opy_(key, bstack1llll11lll_opy_):
  global bstack1llllllll_opy_
  logger.info(bstack1ll111l1l_opy_)
  try:
    bstack1llllllll_opy_ = Local()
    bstack111l1111_opy_ = {bstack1lll11l_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack111l1111_opy_.update(bstack1llll11lll_opy_)
    logger.debug(bstack11ll1llll_opy_.format(str(bstack111l1111_opy_)))
    bstack1llllllll_opy_.start(**bstack111l1111_opy_)
    if bstack1llllllll_opy_.isRunning():
      logger.info(bstack1ll1l1l1_opy_)
  except Exception as e:
    bstack11l1llll_opy_(bstack1ll11l11l_opy_.format(str(e)))
def bstack1lll1llll1_opy_():
  global bstack1llllllll_opy_
  if bstack1llllllll_opy_.isRunning():
    logger.info(bstack1l1l1111l_opy_)
    bstack1llllllll_opy_.stop()
  bstack1llllllll_opy_ = None
def bstack1ll1l1lll_opy_(bstack11lll11l_opy_=[]):
  global CONFIG
  bstack11l11l1l1_opy_ = []
  bstack11l11l11l_opy_ = [bstack1lll11l_opy_ (u"ࠨࡱࡶࠫও"), bstack1lll11l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack1lll11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack11lll11l_opy_:
      bstack1ll1ll11_opy_ = {}
      for k in bstack11l11l11l_opy_:
        val = CONFIG[bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack1lll11l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1ll1ll11_opy_[k] = val
      if(err[bstack1lll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack1lll11l_opy_ (u"ࠪࠫজ")):
        bstack1ll1ll11_opy_[bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack1lll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack1lll11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack11l11l1l1_opy_.append(bstack1ll1ll11_opy_)
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack11l11l1l1_opy_
def bstack1l11l111l_opy_(file_name):
  bstack1l111111_opy_ = []
  try:
    bstack1lll111l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1lll111l_opy_):
      with open(bstack1lll111l_opy_) as f:
        bstack11111lll1_opy_ = json.load(f)
        bstack1l111111_opy_ = bstack11111lll1_opy_
      os.remove(bstack1lll111l_opy_)
    return bstack1l111111_opy_
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
def bstack111llll1_opy_():
  global bstack111ll11ll_opy_
  global bstack11l1ll1ll_opy_
  global bstack1ll1ll1lll_opy_
  global bstack1l1l1lll1l_opy_
  global bstack1l11l11l1_opy_
  global bstack1ll11111_opy_
  percy.shutdown()
  bstack11l11l1ll_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack11l11l1ll_opy_ in [bstack1lll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack1lll11l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1lll1l1ll_opy_()
  if bstack111ll11ll_opy_:
    logger.warning(bstack1l1lll11_opy_.format(str(bstack111ll11ll_opy_)))
  else:
    try:
      bstack1l1l1ll1l1_opy_ = bstack1lll1ll1l1_opy_(bstack1lll11l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1l1l1ll1l1_opy_.get(bstack1lll11l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1l1l1ll1l1_opy_.get(bstack1lll11l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack1lll11l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1l1lll11_opy_.format(str(bstack1l1l1ll1l1_opy_[bstack1lll11l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1llll11111_opy_)
  global bstack1llllllll_opy_
  if bstack1llllllll_opy_:
    bstack1lll1llll1_opy_()
  try:
    for driver in bstack11l1ll1ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1ll111l_opy_)
  if bstack1ll11111_opy_ == bstack1lll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack1l11l11l1_opy_ = bstack1l11l111l_opy_(bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack1ll11111_opy_ == bstack1lll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1l1l1lll1l_opy_) == 0:
    bstack1l1l1lll1l_opy_ = bstack1l11l111l_opy_(bstack1lll11l_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1l1l1lll1l_opy_) == 0:
      bstack1l1l1lll1l_opy_ = bstack1l11l111l_opy_(bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1111lll11_opy_ = bstack1lll11l_opy_ (u"ࠩࠪর")
  if len(bstack1ll1ll1lll_opy_) > 0:
    bstack1111lll11_opy_ = bstack1ll1l1lll_opy_(bstack1ll1ll1lll_opy_)
  elif len(bstack1l1l1lll1l_opy_) > 0:
    bstack1111lll11_opy_ = bstack1ll1l1lll_opy_(bstack1l1l1lll1l_opy_)
  elif len(bstack1l11l11l1_opy_) > 0:
    bstack1111lll11_opy_ = bstack1ll1l1lll_opy_(bstack1l11l11l1_opy_)
  elif len(bstack1l1lll1lll_opy_) > 0:
    bstack1111lll11_opy_ = bstack1ll1l1lll_opy_(bstack1l1lll1lll_opy_)
  if bool(bstack1111lll11_opy_):
    bstack1llll1ll_opy_(bstack1111lll11_opy_)
  else:
    bstack1llll1ll_opy_()
  bstack11l111ll1_opy_(bstack1ll1l1lll1_opy_, logger)
def bstack1lllll11_opy_(self, *args):
  logger.error(bstack1l1l11l1ll_opy_)
  bstack111llll1_opy_()
  sys.exit(1)
def bstack11l1llll_opy_(err):
  logger.critical(bstack11ll1l1ll_opy_.format(str(err)))
  bstack1llll1ll_opy_(bstack11ll1l1ll_opy_.format(str(err)), True)
  atexit.unregister(bstack111llll1_opy_)
  bstack1lll1l1ll_opy_()
  sys.exit(1)
def bstack1l11ll11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1llll1ll_opy_(message, True)
  atexit.unregister(bstack111llll1_opy_)
  bstack1lll1l1ll_opy_()
  sys.exit(1)
def bstack1ll111ll11_opy_():
  global CONFIG
  global bstack11ll11ll1_opy_
  global bstack1lll1111_opy_
  global bstack1ll1ll1l_opy_
  CONFIG = bstack1l1l1l1ll1_opy_()
  bstack1ll1ll11l1_opy_()
  bstack1ll1111111_opy_()
  CONFIG = bstack1lll1ll11_opy_(CONFIG)
  update(CONFIG, bstack1lll1111_opy_)
  update(CONFIG, bstack11ll11ll1_opy_)
  CONFIG = bstack1ll1l11l1l_opy_(CONFIG)
  bstack1ll1ll1l_opy_ = bstack1lll11ll_opy_(CONFIG)
  bstack1l1l1ll1ll_opy_.bstack11l1l1ll_opy_(bstack1lll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ঱"), bstack1ll1ll1l_opy_)
  if (bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") in bstack11ll11ll1_opy_) or (
          bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঴") in CONFIG and bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ঵") not in bstack1lll1111_opy_):
    if os.getenv(bstack1lll11l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ")):
      CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫষ")] = os.getenv(bstack1lll11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧস"))
    else:
      bstack1lllll1ll_opy_()
  elif (bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") not in CONFIG and bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঺") in CONFIG) or (
          bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঻") in bstack1lll1111_opy_ and bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") not in bstack11ll11ll1_opy_):
    del (CONFIG[bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঽ")])
  if bstack1l1l1lll11_opy_(CONFIG):
    bstack11l1llll_opy_(bstack1lll111lll_opy_)
  bstack1ll11lll11_opy_()
  bstack111lll1l_opy_()
  if bstack111l1ll1_opy_:
    CONFIG[bstack1lll11l_opy_ (u"ࠩࡤࡴࡵ࠭া")] = bstack1ll1l11l_opy_(CONFIG)
    logger.info(bstack111ll1111_opy_.format(CONFIG[bstack1lll11l_opy_ (u"ࠪࡥࡵࡶࠧি")]))
def bstack1l11l1l1l_opy_(config, bstack1ll1ll1ll1_opy_):
  global CONFIG
  global bstack111l1ll1_opy_
  CONFIG = config
  bstack111l1ll1_opy_ = bstack1ll1ll1ll1_opy_
def bstack111lll1l_opy_():
  global CONFIG
  global bstack111l1ll1_opy_
  if bstack1lll11l_opy_ (u"ࠫࡦࡶࡰࠨী") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l11ll11_opy_(e, bstack11ll111ll_opy_)
    bstack111l1ll1_opy_ = True
    bstack1l1l1ll1ll_opy_.bstack11l1l1ll_opy_(bstack1lll11l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫু"), True)
def bstack1ll1l11l_opy_(config):
  bstack11l1lll11_opy_ = bstack1lll11l_opy_ (u"࠭ࠧূ")
  app = config[bstack1lll11l_opy_ (u"ࠧࡢࡲࡳࠫৃ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1l1lll1_opy_:
      if os.path.exists(app):
        bstack11l1lll11_opy_ = bstack111lll1l1_opy_(config, app)
      elif bstack111llll1l_opy_(app):
        bstack11l1lll11_opy_ = app
      else:
        bstack11l1llll_opy_(bstack111l1l1ll_opy_.format(app))
    else:
      if bstack111llll1l_opy_(app):
        bstack11l1lll11_opy_ = app
      elif os.path.exists(app):
        bstack11l1lll11_opy_ = bstack111lll1l1_opy_(app)
      else:
        bstack11l1llll_opy_(bstack1l11l111_opy_)
  else:
    if len(app) > 2:
      bstack11l1llll_opy_(bstack11lll1l11_opy_)
    elif len(app) == 2:
      if bstack1lll11l_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৄ") in app and bstack1lll11l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৅") in app:
        if os.path.exists(app[bstack1lll11l_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆")]):
          bstack11l1lll11_opy_ = bstack111lll1l1_opy_(config, app[bstack1lll11l_opy_ (u"ࠫࡵࡧࡴࡩࠩে")], app[bstack1lll11l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨৈ")])
        else:
          bstack11l1llll_opy_(bstack111l1l1ll_opy_.format(app))
      else:
        bstack11l1llll_opy_(bstack11lll1l11_opy_)
    else:
      for key in app:
        if key in bstack111111l1_opy_:
          if key == bstack1lll11l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ৉"):
            if os.path.exists(app[key]):
              bstack11l1lll11_opy_ = bstack111lll1l1_opy_(config, app[key])
            else:
              bstack11l1llll_opy_(bstack111l1l1ll_opy_.format(app))
          else:
            bstack11l1lll11_opy_ = app[key]
        else:
          bstack11l1llll_opy_(bstack1lllll1l1_opy_)
  return bstack11l1lll11_opy_
def bstack111llll1l_opy_(bstack11l1lll11_opy_):
  import re
  bstack1llll1l1_opy_ = re.compile(bstack1lll11l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ৊"))
  bstack1lll1lll_opy_ = re.compile(bstack1lll11l_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧো"))
  if bstack1lll11l_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨৌ") in bstack11l1lll11_opy_ or re.fullmatch(bstack1llll1l1_opy_, bstack11l1lll11_opy_) or re.fullmatch(bstack1lll1lll_opy_, bstack11l1lll11_opy_):
    return True
  else:
    return False
def bstack111lll1l1_opy_(config, path, bstack11ll1111l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1lll11l_opy_ (u"ࠪࡶࡧ্࠭")).read()).hexdigest()
  bstack1ll1l1llll_opy_ = bstack1llll111l_opy_(md5_hash)
  bstack11l1lll11_opy_ = None
  if bstack1ll1l1llll_opy_:
    logger.info(bstack11l11lll_opy_.format(bstack1ll1l1llll_opy_, md5_hash))
    return bstack1ll1l1llll_opy_
  bstack1ll1llll11_opy_ = MultipartEncoder(
    fields={
      bstack1lll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࠩৎ"): (os.path.basename(path), open(os.path.abspath(path), bstack1lll11l_opy_ (u"ࠬࡸࡢࠨ৏")), bstack1lll11l_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ৐")),
      bstack1lll11l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ৑"): bstack11ll1111l_opy_
    }
  )
  response = requests.post(bstack11lll1lll_opy_, data=bstack1ll1llll11_opy_,
                           headers={bstack1lll11l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ৒"): bstack1ll1llll11_opy_.content_type},
                           auth=(config[bstack1lll11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ৓")], config[bstack1lll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭৔")]))
  try:
    res = json.loads(response.text)
    bstack11l1lll11_opy_ = res[bstack1lll11l_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ৕")]
    logger.info(bstack1lllllll1_opy_.format(bstack11l1lll11_opy_))
    bstack1llll11l1_opy_(md5_hash, bstack11l1lll11_opy_)
  except ValueError as err:
    bstack11l1llll_opy_(bstack1l1111111_opy_.format(str(err)))
  return bstack11l1lll11_opy_
def bstack1ll11lll11_opy_():
  global CONFIG
  global bstack1ll1l111ll_opy_
  bstack1llll111l1_opy_ = 0
  bstack1ll1llll1_opy_ = 1
  if bstack1lll11l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ৖") in CONFIG:
    bstack1ll1llll1_opy_ = CONFIG[bstack1lll11l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ৗ")]
  if bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৘") in CONFIG:
    bstack1llll111l1_opy_ = len(CONFIG[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ৙")])
  bstack1ll1l111ll_opy_ = int(bstack1ll1llll1_opy_) * int(bstack1llll111l1_opy_)
def bstack1llll111l_opy_(md5_hash):
  bstack11111lll_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠩࢁࠫ৚")), bstack1lll11l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ৛"), bstack1lll11l_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬড়"))
  if os.path.exists(bstack11111lll_opy_):
    bstack11l111lll_opy_ = json.load(open(bstack11111lll_opy_, bstack1lll11l_opy_ (u"ࠬࡸࡢࠨঢ়")))
    if md5_hash in bstack11l111lll_opy_:
      bstack11ll11lll_opy_ = bstack11l111lll_opy_[md5_hash]
      bstack1ll1111ll_opy_ = datetime.datetime.now()
      bstack1l111l11l_opy_ = datetime.datetime.strptime(bstack11ll11lll_opy_[bstack1lll11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ৞")], bstack1lll11l_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫয়"))
      if (bstack1ll1111ll_opy_ - bstack1l111l11l_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11ll11lll_opy_[bstack1lll11l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ৠ")]):
        return None
      return bstack11ll11lll_opy_[bstack1lll11l_opy_ (u"ࠩ࡬ࡨࠬৡ")]
  else:
    return None
def bstack1llll11l1_opy_(md5_hash, bstack11l1lll11_opy_):
  bstack1lll111l11_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠪࢂࠬৢ")), bstack1lll11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫৣ"))
  if not os.path.exists(bstack1lll111l11_opy_):
    os.makedirs(bstack1lll111l11_opy_)
  bstack11111lll_opy_ = os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠬࢄࠧ৤")), bstack1lll11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৥"), bstack1lll11l_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ০"))
  bstack1lllll1l1l_opy_ = {
    bstack1lll11l_opy_ (u"ࠨ࡫ࡧࠫ১"): bstack11l1lll11_opy_,
    bstack1lll11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ২"): datetime.datetime.strftime(datetime.datetime.now(), bstack1lll11l_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ৩")),
    bstack1lll11l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ৪"): str(__version__)
  }
  if os.path.exists(bstack11111lll_opy_):
    bstack11l111lll_opy_ = json.load(open(bstack11111lll_opy_, bstack1lll11l_opy_ (u"ࠬࡸࡢࠨ৫")))
  else:
    bstack11l111lll_opy_ = {}
  bstack11l111lll_opy_[md5_hash] = bstack1lllll1l1l_opy_
  with open(bstack11111lll_opy_, bstack1lll11l_opy_ (u"ࠨࡷࠬࠤ৬")) as outfile:
    json.dump(bstack11l111lll_opy_, outfile)
def bstack1ll1ll111l_opy_(self):
  return
def bstack1ll11ll1l1_opy_(self):
  return
def bstack1lll11111_opy_(self):
  global bstack1llll11l1l_opy_
  bstack1llll11l1l_opy_(self)
def bstack11lll111_opy_():
  global bstack1l1llll1_opy_
  bstack1l1llll1_opy_ = True
def bstack11111l11l_opy_(self):
  global bstack11l1111l1_opy_
  global bstack1l1lllll1l_opy_
  global bstack1l1l11ll_opy_
  try:
    if bstack1lll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ৭") in bstack11l1111l1_opy_ and self.session_id != None and bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ৮"), bstack1lll11l_opy_ (u"ࠩࠪ৯")) != bstack1lll11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫৰ"):
      bstack1l1l11lll_opy_ = bstack1lll11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫৱ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৲")
      if bstack1l1l11lll_opy_ == bstack1lll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭৳"):
        bstack1llll1l11l_opy_(logger)
      if self != None:
        bstack1l1111l1_opy_(self, bstack1l1l11lll_opy_, bstack1lll11l_opy_ (u"ࠧ࠭ࠢࠪ৴").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1lll11l_opy_ (u"ࠨࠩ৵")
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ৶") + str(e))
  bstack1l1l11ll_opy_(self)
  self.session_id = None
def bstack1llll1l111_opy_(self, command_executor=bstack1lll11l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲࠵࠷࠽࠮࠱࠰࠳࠲࠶ࡀ࠴࠵࠶࠷ࠦ৷"), *args, **kwargs):
  bstack1l111l1l1_opy_ = bstack1llll11l_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack1lll11l_opy_ (u"ࠫࡈࡵ࡭࡮ࡣࡱࡨࠥࡋࡸࡦࡥࡸࡸࡴࡸࠠࡸࡪࡨࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫ࡧ࡬ࡴࡧࠣ࠱ࠥࢁࡽࠨ৸").format(str(command_executor)))
    logger.debug(bstack1lll11l_opy_ (u"ࠬࡎࡵࡣࠢࡘࡖࡑࠦࡩࡴࠢ࠰ࠤࢀࢃࠧ৹").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ৺") in command_executor._url:
      bstack1l1l1ll1ll_opy_.bstack11l1l1ll_opy_(bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ৻"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫৼ") in command_executor):
    bstack1l1l1ll1ll_opy_.bstack11l1l1ll_opy_(bstack1lll11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ৽"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l11ll1ll_opy_.bstack11111111l_opy_(self)
  return bstack1l111l1l1_opy_
def bstack11lllll11_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1l11ll1_opy_
  response = bstack1ll1l11ll1_opy_(self, driver_command, *args, **kwargs)
  try:
    if driver_command == bstack1lll11l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ৾"):
      bstack1l11ll1ll_opy_.bstack111ll1l1l_opy_({
          bstack1lll11l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ৿"): response[bstack1lll11l_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ਀")],
          bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ਁ"): bstack1l11ll1ll_opy_.current_test_uuid() if bstack1l11ll1ll_opy_.current_test_uuid() else bstack1l11ll1ll_opy_.current_hook_uuid()
      })
  except:
    pass
  return response
def bstack1ll111l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l1lllll1l_opy_
  global bstack1ll1l1l111_opy_
  global bstack1l1ll1ll1_opy_
  global bstack1l111l1l_opy_
  global bstack1ll11lll_opy_
  global bstack11l1111l1_opy_
  global bstack1llll11l_opy_
  global bstack11l1ll1ll_opy_
  global bstack1l1ll1ll11_opy_
  global bstack11l11ll1_opy_
  CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩਂ")] = str(bstack11l1111l1_opy_) + str(__version__)
  command_executor = bstack11lll1l1l_opy_()
  logger.debug(bstack111l1l1l_opy_.format(command_executor))
  proxy = bstack1l1ll1llll_opy_(CONFIG, proxy)
  bstack1l1lll1l1l_opy_ = 0 if bstack1ll1l1l111_opy_ < 0 else bstack1ll1l1l111_opy_
  try:
    if bstack1l111l1l_opy_ is True:
      bstack1l1lll1l1l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1ll11lll_opy_ is True:
      bstack1l1lll1l1l_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1lll1l1l_opy_ = 0
  bstack1ll11lll1l_opy_ = bstack1l11ll1l_opy_(CONFIG, bstack1l1lll1l1l_opy_)
  logger.debug(bstack11ll1l11_opy_.format(str(bstack1ll11lll1l_opy_)))
  if bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਃ") in CONFIG and bstack1l1l1ll11_opy_(CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭਄")]):
    bstack1ll11l11l1_opy_(bstack1ll11lll1l_opy_)
  if desired_capabilities:
    bstack1l11lll1l_opy_ = bstack1lll1ll11_opy_(desired_capabilities)
    bstack1l11lll1l_opy_[bstack1lll11l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪਅ")] = bstack11ll1ll11_opy_(CONFIG)
    bstack1l1111l1l_opy_ = bstack1l11ll1l_opy_(bstack1l11lll1l_opy_)
    if bstack1l1111l1l_opy_:
      bstack1ll11lll1l_opy_ = update(bstack1l1111l1l_opy_, bstack1ll11lll1l_opy_)
    desired_capabilities = None
  if options:
    bstack11llllll1_opy_(options, bstack1ll11lll1l_opy_)
  if not options:
    options = bstack1lll1lll1_opy_(bstack1ll11lll1l_opy_)
  bstack11l11ll1_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਆ"))[bstack1l1lll1l1l_opy_]
  if bstack111ll11l1_opy_.bstack1lll1l11ll_opy_(CONFIG, bstack1l1lll1l1l_opy_) and bstack111ll11l1_opy_.bstack1lll1l11l_opy_(bstack1ll11lll1l_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack111ll11l1_opy_.set_capabilities(bstack1ll11lll1l_opy_, CONFIG)
  if proxy and bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬਇ")):
    options.proxy(proxy)
  if options and bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਈ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1lll1ll1l_opy_() < version.parse(bstack1lll11l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ਉ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll11lll1l_opy_)
  logger.info(bstack1lll11ll1_opy_)
  if bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨਊ")):
    bstack1llll11l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ਋")):
    bstack1llll11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ਌")):
    bstack1llll11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1llll11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1lll1ll11l_opy_ = bstack1lll11l_opy_ (u"ࠫࠬ਍")
    if bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭਎")):
      bstack1lll1ll11l_opy_ = self.caps.get(bstack1lll11l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਏ"))
    else:
      bstack1lll1ll11l_opy_ = self.capabilities.get(bstack1lll11l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢਐ"))
    if bstack1lll1ll11l_opy_:
      bstack1l1lll1l11_opy_(bstack1lll1ll11l_opy_)
      if bstack1lll1ll1l_opy_() <= version.parse(bstack1lll11l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ਑")):
        self.command_executor._url = bstack1lll11l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ਒") + bstack1l1l1l11_opy_ + bstack1lll11l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢਓ")
      else:
        self.command_executor._url = bstack1lll11l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨਔ") + bstack1lll1ll11l_opy_ + bstack1lll11l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨਕ")
      logger.debug(bstack1111ll11_opy_.format(bstack1lll1ll11l_opy_))
    else:
      logger.debug(bstack1l11l1l1_opy_.format(bstack1lll11l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢਖ")))
  except Exception as e:
    logger.debug(bstack1l11l1l1_opy_.format(e))
  if bstack1lll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਗ") in bstack11l1111l1_opy_:
    bstack111l11ll_opy_(bstack1ll1l1l111_opy_, bstack1l1ll1ll11_opy_)
  bstack1l1lllll1l_opy_ = self.session_id
  if bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਘ") in bstack11l1111l1_opy_ or bstack1lll11l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩਙ") in bstack11l1111l1_opy_ or bstack1lll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਚ") in bstack11l1111l1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l11ll1ll_opy_.bstack11111111l_opy_(self)
  bstack11l1ll1ll_opy_.append(self)
  if bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਛ") in CONFIG and bstack1lll11l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਜ") in CONFIG[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਝ")][bstack1l1lll1l1l_opy_]:
    bstack1l1ll1ll1_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਞ")][bstack1l1lll1l1l_opy_][bstack1lll11l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਟ")]
  logger.debug(bstack1l11ll111_opy_.format(bstack1l1lllll1l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack11ll11ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11l11l11_opy_
      if(bstack1lll11l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦਠ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠪࢂࠬਡ")), bstack1lll11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫਢ"), bstack1lll11l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧਣ")), bstack1lll11l_opy_ (u"࠭ࡷࠨਤ")) as fp:
          fp.write(bstack1lll11l_opy_ (u"ࠢࠣਥ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1lll11l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥਦ")))):
          with open(args[1], bstack1lll11l_opy_ (u"ࠩࡵࠫਧ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1lll11l_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩਨ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1l1l11l_opy_)
            lines.insert(1, bstack1ll1l11ll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1lll11l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਩")), bstack1lll11l_opy_ (u"ࠬࡽࠧਪ")) as bstack1l1lll1ll1_opy_:
              bstack1l1lll1ll1_opy_.writelines(lines)
        CONFIG[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack11l1111l1_opy_) + str(__version__)
        bstack1l1lll1l1l_opy_ = 0 if bstack1ll1l1l111_opy_ < 0 else bstack1ll1l1l111_opy_
        try:
          if bstack1l111l1l_opy_ is True:
            bstack1l1lll1l1l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1ll11lll_opy_ is True:
            bstack1l1lll1l1l_opy_ = int(threading.current_thread().name)
        except:
          bstack1l1lll1l1l_opy_ = 0
        CONFIG[bstack1lll11l_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢਬ")] = False
        CONFIG[bstack1lll11l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢਭ")] = True
        bstack1ll11lll1l_opy_ = bstack1l11ll1l_opy_(CONFIG, bstack1l1lll1l1l_opy_)
        logger.debug(bstack11ll1l11_opy_.format(str(bstack1ll11lll1l_opy_)))
        if CONFIG.get(bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ਮ")):
          bstack1ll11l11l1_opy_(bstack1ll11lll1l_opy_)
        if bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ") in CONFIG and bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਰ") in CONFIG[bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਱")][bstack1l1lll1l1l_opy_]:
          bstack1l1ll1ll1_opy_ = CONFIG[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਲ")][bstack1l1lll1l1l_opy_][bstack1lll11l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਲ਼")]
        args.append(os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠨࢀࠪ਴")), bstack1lll11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਵ"), bstack1lll11l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬਸ਼")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll11lll1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1lll11l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਷"))
      bstack11l11l11_opy_ = True
      return bstack1l1l1l1l1l_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack1ll1111l1l_opy_(self,
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
    global bstack1ll1l1l111_opy_
    global bstack1l1ll1ll1_opy_
    global bstack1l111l1l_opy_
    global bstack1ll11lll_opy_
    global bstack11l1111l1_opy_
    CONFIG[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਸ")] = str(bstack11l1111l1_opy_) + str(__version__)
    bstack1l1lll1l1l_opy_ = 0 if bstack1ll1l1l111_opy_ < 0 else bstack1ll1l1l111_opy_
    try:
      if bstack1l111l1l_opy_ is True:
        bstack1l1lll1l1l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1ll11lll_opy_ is True:
        bstack1l1lll1l1l_opy_ = int(threading.current_thread().name)
    except:
      bstack1l1lll1l1l_opy_ = 0
    CONFIG[bstack1lll11l_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧਹ")] = True
    bstack1ll11lll1l_opy_ = bstack1l11ll1l_opy_(CONFIG, bstack1l1lll1l1l_opy_)
    logger.debug(bstack11ll1l11_opy_.format(str(bstack1ll11lll1l_opy_)))
    if CONFIG.get(bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ਺")):
      bstack1ll11l11l1_opy_(bstack1ll11lll1l_opy_)
    if bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਻") in CONFIG and bstack1lll11l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫਼ࠧ") in CONFIG[bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack1l1lll1l1l_opy_]:
      bstack1l1ll1ll1_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਾ")][bstack1l1lll1l1l_opy_][bstack1lll11l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਿ")]
    import urllib
    import json
    bstack111l1111l_opy_ = bstack1lll11l_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨੀ") + urllib.parse.quote(json.dumps(bstack1ll11lll1l_opy_))
    browser = self.connect(bstack111l1111l_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll1l1l1l1_opy_():
    global bstack11l11l11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1111l1l_opy_
        bstack11l11l11_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11ll11ll_opy_
      bstack11l11l11_opy_ = True
    except Exception as e:
      pass
def bstack1llllll111_opy_(context, bstack1lll1l1lll_opy_):
  try:
    context.page.evaluate(bstack1lll11l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣੁ"), bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬੂ")+ json.dumps(bstack1lll1l1lll_opy_) + bstack1lll11l_opy_ (u"ࠤࢀࢁࠧ੃"))
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣ੄"), e)
def bstack11lllll1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1lll11l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ੅"), bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ੆") + json.dumps(message) + bstack1lll11l_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩੇ") + json.dumps(level) + bstack1lll11l_opy_ (u"ࠧࡾࡿࠪੈ"))
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦ੉"), e)
def bstack1llll11l11_opy_(self, url):
  global bstack1ll1ll111_opy_
  try:
    bstack11llll11_opy_(url)
  except Exception as err:
    logger.debug(bstack1llll1ll1l_opy_.format(str(err)))
  try:
    bstack1ll1ll111_opy_(self, url)
  except Exception as e:
    try:
      bstack1lll1llll_opy_ = str(e)
      if any(err_msg in bstack1lll1llll_opy_ for err_msg in bstack11ll1ll1_opy_):
        bstack11llll11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1llll1ll1l_opy_.format(str(err)))
    raise e
def bstack1ll11ll11l_opy_(self):
  global bstack1111l1l1l_opy_
  bstack1111l1l1l_opy_ = self
  return
def bstack1llll1ll11_opy_(self):
  global bstack1ll1l11lll_opy_
  bstack1ll1l11lll_opy_ = self
  return
def bstack1ll1ll1ll_opy_(self, test):
  global CONFIG
  global bstack1lllll1lll_opy_
  if CONFIG.get(bstack1lll11l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ੊"), False):
    test_name = str(test.data)
    bstack111l11l11_opy_ = str(test.source)
    bstack1lll111111_opy_ = os.path.relpath(bstack111l11l11_opy_, start=os.getcwd())
    suite_name, bstack1ll1llll1l_opy_ = os.path.splitext(bstack1lll111111_opy_)
    bstack1ll11l1l1_opy_ = suite_name + bstack1lll11l_opy_ (u"ࠥ࠱ࠧੋ") + test_name
    threading.current_thread().percySessionName = bstack1ll11l1l1_opy_
  bstack1lllll1lll_opy_(self, test)
def bstack111ll1ll1_opy_(self, test):
  global CONFIG
  global bstack1ll1l11lll_opy_
  global bstack1111l1l1l_opy_
  global bstack1l1lllll1l_opy_
  global bstack1l1ll11111_opy_
  global bstack1l1ll1ll1_opy_
  global bstack1lll11llll_opy_
  global bstack1llll1l1ll_opy_
  global bstack1l1ll1lll1_opy_
  global bstack11l111l1_opy_
  global bstack11l1ll1ll_opy_
  global bstack11l11ll1_opy_
  try:
    if not bstack1l1lllll1l_opy_:
      with open(os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠫࢃ࠭ੌ")), bstack1lll11l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯੍ࠬ"), bstack1lll11l_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ੎"))) as f:
        bstack1l1lllll_opy_ = json.loads(bstack1lll11l_opy_ (u"ࠢࡼࠤ੏") + f.read().strip() + bstack1lll11l_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ੐") + bstack1lll11l_opy_ (u"ࠤࢀࠦੑ"))
        bstack1l1lllll1l_opy_ = bstack1l1lllll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11l1ll1ll_opy_:
    for driver in bstack11l1ll1ll_opy_:
      if bstack1l1lllll1l_opy_ == driver.session_id:
        if test:
          bstack1ll11l1l1_opy_ = str(test.data)
          if CONFIG.get(bstack1lll11l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ੒"), False):
            if CONFIG.get(bstack1lll11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ੓"), bstack1lll11l_opy_ (u"ࠧࡧࡵࡵࡱࠥ੔")) == bstack1lll11l_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ੕"):
              bstack1111111l_opy_ = bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ੖"), None)
              bstack1l1lll1l_opy_(driver, bstack1111111l_opy_)
          if bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ੗"), None) and bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੘"), None):
            logger.info(bstack1lll11l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠢࠥਖ਼"))
            bstack111ll11l1_opy_.bstack11l11111_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack111l1lll1_opy_=bstack11l11ll1_opy_)
        if not bstack111l11lll_opy_ and bstack1ll11l1l1_opy_:
          bstack1l111ll1_opy_ = {
            bstack1lll11l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫਗ਼"): bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਜ਼"),
            bstack1lll11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩੜ"): {
              bstack1lll11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ੝"): bstack1ll11l1l1_opy_
            }
          }
          bstack1llll1l1l1_opy_ = bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ਫ਼").format(json.dumps(bstack1l111ll1_opy_))
          driver.execute_script(bstack1llll1l1l1_opy_)
        if bstack1l1ll11111_opy_:
          bstack1111l1ll_opy_ = {
            bstack1lll11l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ੟"): bstack1lll11l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ੠"),
            bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੡"): {
              bstack1lll11l_opy_ (u"ࠬࡪࡡࡵࡣࠪ੢"): bstack1ll11l1l1_opy_ + bstack1lll11l_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ੣"),
              bstack1lll11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭੤"): bstack1lll11l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭੥")
            }
          }
          if bstack1l1ll11111_opy_.status == bstack1lll11l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ੦"):
            bstack11ll11111_opy_ = bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ੧").format(json.dumps(bstack1111l1ll_opy_))
            driver.execute_script(bstack11ll11111_opy_)
            bstack1l1111l1_opy_(driver, bstack1lll11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ੨"))
          elif bstack1l1ll11111_opy_.status == bstack1lll11l_opy_ (u"ࠬࡌࡁࡊࡎࠪ੩"):
            reason = bstack1lll11l_opy_ (u"ࠨࠢ੪")
            bstack1l11l11l_opy_ = bstack1ll11l1l1_opy_ + bstack1lll11l_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨ੫")
            if bstack1l1ll11111_opy_.message:
              reason = str(bstack1l1ll11111_opy_.message)
              bstack1l11l11l_opy_ = bstack1l11l11l_opy_ + bstack1lll11l_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ੬") + reason
            bstack1111l1ll_opy_[bstack1lll11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ੭")] = {
              bstack1lll11l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ੮"): bstack1lll11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ੯"),
              bstack1lll11l_opy_ (u"ࠬࡪࡡࡵࡣࠪੰ"): bstack1l11l11l_opy_
            }
            bstack11ll11111_opy_ = bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫੱ").format(json.dumps(bstack1111l1ll_opy_))
            driver.execute_script(bstack11ll11111_opy_)
            bstack1l1111l1_opy_(driver, bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧੲ"), reason)
            bstack11l111111_opy_(reason, str(bstack1l1ll11111_opy_), str(bstack1ll1l1l111_opy_), logger)
  elif bstack1l1lllll1l_opy_:
    try:
      data = {}
      bstack1ll11l1l1_opy_ = None
      if test:
        bstack1ll11l1l1_opy_ = str(test.data)
      if not bstack111l11lll_opy_ and bstack1ll11l1l1_opy_:
        data[bstack1lll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ੳ")] = bstack1ll11l1l1_opy_
      if bstack1l1ll11111_opy_:
        if bstack1l1ll11111_opy_.status == bstack1lll11l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧੴ"):
          data[bstack1lll11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪੵ")] = bstack1lll11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ੶")
        elif bstack1l1ll11111_opy_.status == bstack1lll11l_opy_ (u"ࠬࡌࡁࡊࡎࠪ੷"):
          data[bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭੸")] = bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ੹")
          if bstack1l1ll11111_opy_.message:
            data[bstack1lll11l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ੺")] = str(bstack1l1ll11111_opy_.message)
      user = CONFIG[bstack1lll11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੻")]
      key = CONFIG[bstack1lll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭੼")]
      url = bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩ੽").format(user, key, bstack1l1lllll1l_opy_)
      headers = {
        bstack1lll11l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ੾"): bstack1lll11l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ੿"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll1lllll_opy_.format(str(e)))
  if bstack1ll1l11lll_opy_:
    bstack1llll1l1ll_opy_(bstack1ll1l11lll_opy_)
  if bstack1111l1l1l_opy_:
    bstack1l1ll1lll1_opy_(bstack1111l1l1l_opy_)
  if bstack1l1llll1_opy_:
    bstack11l111l1_opy_()
  bstack1lll11llll_opy_(self, test)
def bstack1lll1ll1ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll1111l_opy_
  global CONFIG
  global bstack11l1ll1ll_opy_
  global bstack1l1lllll1l_opy_
  bstack1ll1l11l1_opy_ = None
  try:
    if bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭઀"), None):
      try:
        if not bstack1l1lllll1l_opy_:
          with open(os.path.join(os.path.expanduser(bstack1lll11l_opy_ (u"ࠨࢀࠪઁ")), bstack1lll11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩં"), bstack1lll11l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬઃ"))) as f:
            bstack1l1lllll_opy_ = json.loads(bstack1lll11l_opy_ (u"ࠦࢀࠨ઄") + f.read().strip() + bstack1lll11l_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧઅ") + bstack1lll11l_opy_ (u"ࠨࡽࠣઆ"))
            bstack1l1lllll1l_opy_ = bstack1l1lllll_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack11l1ll1ll_opy_:
        for driver in bstack11l1ll1ll_opy_:
          if bstack1l1lllll1l_opy_ == driver.session_id:
            bstack1ll1l11l1_opy_ = driver
    bstack11ll11l11_opy_ = bstack111ll11l1_opy_.bstack111ll11l_opy_(CONFIG, test.tags)
    if bstack1ll1l11l1_opy_:
      threading.current_thread().isA11yTest = bstack111ll11l1_opy_.bstack111l1lll_opy_(bstack1ll1l11l1_opy_, bstack11ll11l11_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11ll11l11_opy_
  except:
    pass
  bstack1ll1111l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1ll11111_opy_
  bstack1l1ll11111_opy_ = self._test
def bstack111l1ll11_opy_():
  global bstack1111l1111_opy_
  try:
    if os.path.exists(bstack1111l1111_opy_):
      os.remove(bstack1111l1111_opy_)
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪઇ") + str(e))
def bstack1l1l1l111l_opy_():
  global bstack1111l1111_opy_
  bstack1l1l1ll1l1_opy_ = {}
  try:
    if not os.path.isfile(bstack1111l1111_opy_):
      with open(bstack1111l1111_opy_, bstack1lll11l_opy_ (u"ࠨࡹࠪઈ")):
        pass
      with open(bstack1111l1111_opy_, bstack1lll11l_opy_ (u"ࠤࡺ࠯ࠧઉ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1111l1111_opy_):
      bstack1l1l1ll1l1_opy_ = json.load(open(bstack1111l1111_opy_, bstack1lll11l_opy_ (u"ࠪࡶࡧ࠭ઊ")))
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ઋ") + str(e))
  finally:
    return bstack1l1l1ll1l1_opy_
def bstack111l11ll_opy_(platform_index, item_index):
  global bstack1111l1111_opy_
  try:
    bstack1l1l1ll1l1_opy_ = bstack1l1l1l111l_opy_()
    bstack1l1l1ll1l1_opy_[item_index] = platform_index
    with open(bstack1111l1111_opy_, bstack1lll11l_opy_ (u"ࠧࡽࠫࠣઌ")) as outfile:
      json.dump(bstack1l1l1ll1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫઍ") + str(e))
def bstack11l1llll1_opy_(bstack111l1l11_opy_):
  global CONFIG
  bstack111ll1l11_opy_ = bstack1lll11l_opy_ (u"ࠧࠨ઎")
  if not bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫએ") in CONFIG:
    logger.info(bstack1lll11l_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ઐ"))
  try:
    platform = CONFIG[bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ઑ")][bstack111l1l11_opy_]
    if bstack1lll11l_opy_ (u"ࠫࡴࡹࠧ઒") in platform:
      bstack111ll1l11_opy_ += str(platform[bstack1lll11l_opy_ (u"ࠬࡵࡳࠨઓ")]) + bstack1lll11l_opy_ (u"࠭ࠬࠡࠩઔ")
    if bstack1lll11l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪક") in platform:
      bstack111ll1l11_opy_ += str(platform[bstack1lll11l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫખ")]) + bstack1lll11l_opy_ (u"ࠩ࠯ࠤࠬગ")
    if bstack1lll11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧઘ") in platform:
      bstack111ll1l11_opy_ += str(platform[bstack1lll11l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨઙ")]) + bstack1lll11l_opy_ (u"ࠬ࠲ࠠࠨચ")
    if bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨછ") in platform:
      bstack111ll1l11_opy_ += str(platform[bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩજ")]) + bstack1lll11l_opy_ (u"ࠨ࠮ࠣࠫઝ")
    if bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧઞ") in platform:
      bstack111ll1l11_opy_ += str(platform[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨટ")]) + bstack1lll11l_opy_ (u"ࠫ࠱ࠦࠧઠ")
    if bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ડ") in platform:
      bstack111ll1l11_opy_ += str(platform[bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧઢ")]) + bstack1lll11l_opy_ (u"ࠧ࠭ࠢࠪણ")
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨત") + str(e))
  finally:
    if bstack111ll1l11_opy_[len(bstack111ll1l11_opy_) - 2:] == bstack1lll11l_opy_ (u"ࠩ࠯ࠤࠬથ"):
      bstack111ll1l11_opy_ = bstack111ll1l11_opy_[:-2]
    return bstack111ll1l11_opy_
def bstack1lll1l11_opy_(path, bstack111ll1l11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1ll1l1ll11_opy_ = ET.parse(path)
    bstack1l1llll1l_opy_ = bstack1ll1l1ll11_opy_.getroot()
    bstack1ll111ll_opy_ = None
    for suite in bstack1l1llll1l_opy_.iter(bstack1lll11l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩદ")):
      if bstack1lll11l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫધ") in suite.attrib:
        suite.attrib[bstack1lll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪન")] += bstack1lll11l_opy_ (u"࠭ࠠࠨ઩") + bstack111ll1l11_opy_
        bstack1ll111ll_opy_ = suite
    bstack1ll1l11111_opy_ = None
    for robot in bstack1l1llll1l_opy_.iter(bstack1lll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭પ")):
      bstack1ll1l11111_opy_ = robot
    bstack1l1ll1ll_opy_ = len(bstack1ll1l11111_opy_.findall(bstack1lll11l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧફ")))
    if bstack1l1ll1ll_opy_ == 1:
      bstack1ll1l11111_opy_.remove(bstack1ll1l11111_opy_.findall(bstack1lll11l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨબ"))[0])
      bstack1ll11l1l1l_opy_ = ET.Element(bstack1lll11l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩભ"), attrib={bstack1lll11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩમ"): bstack1lll11l_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬય"), bstack1lll11l_opy_ (u"࠭ࡩࡥࠩર"): bstack1lll11l_opy_ (u"ࠧࡴ࠲ࠪ઱")})
      bstack1ll1l11111_opy_.insert(1, bstack1ll11l1l1l_opy_)
      bstack1lll1ll111_opy_ = None
      for suite in bstack1ll1l11111_opy_.iter(bstack1lll11l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧલ")):
        bstack1lll1ll111_opy_ = suite
      bstack1lll1ll111_opy_.append(bstack1ll111ll_opy_)
      bstack11l1ll11l_opy_ = None
      for status in bstack1ll111ll_opy_.iter(bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩળ")):
        bstack11l1ll11l_opy_ = status
      bstack1lll1ll111_opy_.append(bstack11l1ll11l_opy_)
    bstack1ll1l1ll11_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨ઴") + str(e))
def bstack1lll1l1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1l11ll1_opy_
  global CONFIG
  if bstack1lll11l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣવ") in options:
    del options[bstack1lll11l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤશ")]
  bstack111l111ll_opy_ = bstack1l1l1l111l_opy_()
  for bstack1l1ll11l1_opy_ in bstack111l111ll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1lll11l_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭ષ"), str(bstack1l1ll11l1_opy_), bstack1lll11l_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫસ"))
    bstack1lll1l11_opy_(path, bstack11l1llll1_opy_(bstack111l111ll_opy_[bstack1l1ll11l1_opy_]))
  bstack111l1ll11_opy_()
  return bstack1l1l11ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll1llllll_opy_(self, ff_profile_dir):
  global bstack1l1lll111_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1lll111_opy_(self, ff_profile_dir)
def bstack1l1l11l11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1lllll11_opy_
  bstack1lll11ll11_opy_ = []
  if bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫહ") in CONFIG:
    bstack1lll11ll11_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ઺")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1lll11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ઻")],
      pabot_args[bstack1lll11l_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩ઼ࠧ")],
      argfile,
      pabot_args.get(bstack1lll11l_opy_ (u"ࠧ࡮ࡩࡷࡧࠥઽ")),
      pabot_args[bstack1lll11l_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤા")],
      platform[0],
      bstack1l1lllll11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1lll11l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢિ")] or [(bstack1lll11l_opy_ (u"ࠣࠤી"), None)]
    for platform in enumerate(bstack1lll11ll11_opy_)
  ]
def bstack111ll1lll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1ll111l1_opy_=bstack1lll11l_opy_ (u"ࠩࠪુ")):
  global bstack1lllll1111_opy_
  self.platform_index = platform_index
  self.bstack1l11l1ll1_opy_ = bstack1l1ll111l1_opy_
  bstack1lllll1111_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11ll1lll1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1ll11ll_opy_
  global bstack1l11l1l11_opy_
  if not bstack1lll11l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૂ") in item.options:
    item.options[bstack1lll11l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ૃ")] = []
  for v in item.options[bstack1lll11l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧૄ")]:
    if bstack1lll11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬૅ") in v:
      item.options[bstack1lll11l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૆")].remove(v)
    if bstack1lll11l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨે") in v:
      item.options[bstack1lll11l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫૈ")].remove(v)
  item.options[bstack1lll11l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૉ")].insert(0, bstack1lll11l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭૊").format(item.platform_index))
  item.options[bstack1lll11l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧો")].insert(0, bstack1lll11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭ૌ").format(item.bstack1l11l1ll1_opy_))
  if bstack1l11l1l11_opy_:
    item.options[bstack1lll11l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦ્ࠩ")].insert(0, bstack1lll11l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫ૎").format(bstack1l11l1l11_opy_))
  return bstack1ll1ll11ll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack11ll111l1_opy_(command, item_index):
  os.environ[bstack1lll11l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ૏")] = json.dumps(CONFIG[bstack1lll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૐ")][item_index % bstack111llllll_opy_])
  global bstack1l11l1l11_opy_
  if bstack1l11l1l11_opy_:
    command[0] = command[0].replace(bstack1lll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૑"), bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ૒") + str(
      item_index) + bstack1lll11l_opy_ (u"࠭ࠠࠨ૓") + bstack1l11l1l11_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1lll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૔"),
                                    bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ૕") + str(item_index), 1)
def bstack1ll111l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll111l1_opy_
  bstack11ll111l1_opy_(command, item_index)
  return bstack1ll111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack111ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1ll111l1_opy_
  bstack11ll111l1_opy_(command, item_index)
  return bstack1ll111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1ll111l1_opy_
  bstack11ll111l1_opy_(command, item_index)
  return bstack1ll111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1ll11llll1_opy_(self, runner, quiet=False, capture=True):
  global bstack1llll1111l_opy_
  bstack11l1lll1l_opy_ = bstack1llll1111l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1lll11l_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡤࡧࡲࡳࠩ૖")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1lll11l_opy_ (u"ࠪࡩࡽࡩ࡟ࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࡢࡥࡷࡸࠧ૗")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11l1lll1l_opy_
def bstack111llll11_opy_(self, name, context, *args):
  os.environ[bstack1lll11l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ૘")] = json.dumps(CONFIG[bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૙")][int(threading.current_thread()._name) % bstack111llllll_opy_])
  global bstack1lll1lll1l_opy_
  if name == bstack1lll11l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ૚"):
    bstack1lll1lll1l_opy_(self, name, context, *args)
    try:
      if not bstack111l11lll_opy_:
        bstack1ll1l11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11ll1l_opy_(bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭૛")) else context.browser
        bstack1lll1l1lll_opy_ = str(self.feature.name)
        bstack1llllll111_opy_(context, bstack1lll1l1lll_opy_)
        bstack1ll1l11l1_opy_.execute_script(bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭૜") + json.dumps(bstack1lll1l1lll_opy_) + bstack1lll11l_opy_ (u"ࠩࢀࢁࠬ૝"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1lll11l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ૞").format(str(e)))
  elif name == bstack1lll11l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭૟"):
    bstack1lll1lll1l_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack1lll11l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧૠ")):
        self.driver_before_scenario = True
      if (not bstack111l11lll_opy_):
        scenario_name = args[0].name
        feature_name = bstack1lll1l1lll_opy_ = str(self.feature.name)
        bstack1lll1l1lll_opy_ = feature_name + bstack1lll11l_opy_ (u"࠭ࠠ࠮ࠢࠪૡ") + scenario_name
        bstack1ll1l11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11ll1l_opy_(bstack1lll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ૢ")) else context.browser
        if self.driver_before_scenario:
          bstack1llllll111_opy_(context, bstack1lll1l1lll_opy_)
          bstack1ll1l11l1_opy_.execute_script(bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ૣ") + json.dumps(bstack1lll1l1lll_opy_) + bstack1lll11l_opy_ (u"ࠩࢀࢁࠬ૤"))
    except Exception as e:
      logger.debug(bstack1lll11l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ૥").format(str(e)))
  elif name == bstack1lll11l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૦"):
    try:
      bstack1l1l11111_opy_ = args[0].status.name
      bstack1ll1l11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૧") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1l1l11111_opy_).lower() == bstack1lll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭૨"):
        bstack1ll111111l_opy_ = bstack1lll11l_opy_ (u"ࠧࠨ૩")
        bstack111lll1ll_opy_ = bstack1lll11l_opy_ (u"ࠨࠩ૪")
        bstack1l11lllll_opy_ = bstack1lll11l_opy_ (u"ࠩࠪ૫")
        try:
          import traceback
          bstack1ll111111l_opy_ = self.exception.__class__.__name__
          bstack1lllllllll_opy_ = traceback.format_tb(self.exc_traceback)
          bstack111lll1ll_opy_ = bstack1lll11l_opy_ (u"ࠪࠤࠬ૬").join(bstack1lllllllll_opy_)
          bstack1l11lllll_opy_ = bstack1lllllllll_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l111lll_opy_.format(str(e)))
        bstack1ll111111l_opy_ += bstack1l11lllll_opy_
        bstack11lllll1l_opy_(context, json.dumps(str(args[0].name) + bstack1lll11l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ૭") + str(bstack111lll1ll_opy_)),
                            bstack1lll11l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ૮"))
        if self.driver_before_scenario:
          bstack1llllll1ll_opy_(getattr(context, bstack1lll11l_opy_ (u"࠭ࡰࡢࡩࡨࠫ૯"), None), bstack1lll11l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ૰"), bstack1ll111111l_opy_)
          bstack1ll1l11l1_opy_.execute_script(bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭૱") + json.dumps(str(args[0].name) + bstack1lll11l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ૲") + str(bstack111lll1ll_opy_)) + bstack1lll11l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪ૳"))
        if self.driver_before_scenario:
          bstack1l1111l1_opy_(bstack1ll1l11l1_opy_, bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૴"), bstack1lll11l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ૵") + str(bstack1ll111111l_opy_))
      else:
        bstack11lllll1l_opy_(context, bstack1lll11l_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ૶"), bstack1lll11l_opy_ (u"ࠢࡪࡰࡩࡳࠧ૷"))
        if self.driver_before_scenario:
          bstack1llllll1ll_opy_(getattr(context, bstack1lll11l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭૸"), None), bstack1lll11l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤૹ"))
        bstack1ll1l11l1_opy_.execute_script(bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨૺ") + json.dumps(str(args[0].name) + bstack1lll11l_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣૻ")) + bstack1lll11l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫૼ"))
        if self.driver_before_scenario:
          bstack1l1111l1_opy_(bstack1ll1l11l1_opy_, bstack1lll11l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ૽"))
    except Exception as e:
      logger.debug(bstack1lll11l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ૾").format(str(e)))
  elif name == bstack1lll11l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ૿"):
    try:
      bstack1ll1l11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11ll1l_opy_(bstack1lll11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ଀")) else context.browser
      if context.failed is True:
        bstack1l11l11ll_opy_ = []
        bstack1l1lll11ll_opy_ = []
        bstack11l11l111_opy_ = []
        bstack1lll1l111_opy_ = bstack1lll11l_opy_ (u"ࠪࠫଁ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l11l11ll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1lllllllll_opy_ = traceback.format_tb(exc_tb)
            bstack1l1lll11l1_opy_ = bstack1lll11l_opy_ (u"ࠫࠥ࠭ଂ").join(bstack1lllllllll_opy_)
            bstack1l1lll11ll_opy_.append(bstack1l1lll11l1_opy_)
            bstack11l11l111_opy_.append(bstack1lllllllll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l111lll_opy_.format(str(e)))
        bstack1ll111111l_opy_ = bstack1lll11l_opy_ (u"ࠬ࠭ଃ")
        for i in range(len(bstack1l11l11ll_opy_)):
          bstack1ll111111l_opy_ += bstack1l11l11ll_opy_[i] + bstack11l11l111_opy_[i] + bstack1lll11l_opy_ (u"࠭࡜࡯ࠩ଄")
        bstack1lll1l111_opy_ = bstack1lll11l_opy_ (u"ࠧࠡࠩଅ").join(bstack1l1lll11ll_opy_)
        if not self.driver_before_scenario:
          bstack11lllll1l_opy_(context, bstack1lll1l111_opy_, bstack1lll11l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢଆ"))
          bstack1llllll1ll_opy_(getattr(context, bstack1lll11l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧଇ"), None), bstack1lll11l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥଈ"), bstack1ll111111l_opy_)
          bstack1ll1l11l1_opy_.execute_script(bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଉ") + json.dumps(bstack1lll1l111_opy_) + bstack1lll11l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬଊ"))
          bstack1l1111l1_opy_(bstack1ll1l11l1_opy_, bstack1lll11l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨଋ"), bstack1lll11l_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧଌ") + str(bstack1ll111111l_opy_))
          bstack1l11l1111_opy_ = bstack1llll1111_opy_(bstack1lll1l111_opy_, self.feature.name, logger)
          if (bstack1l11l1111_opy_ != None):
            bstack1l1lll1lll_opy_.append(bstack1l11l1111_opy_)
      else:
        if not self.driver_before_scenario:
          bstack11lllll1l_opy_(context, bstack1lll11l_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦ଍") + str(self.feature.name) + bstack1lll11l_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦ଎"), bstack1lll11l_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣଏ"))
          bstack1llllll1ll_opy_(getattr(context, bstack1lll11l_opy_ (u"ࠫࡵࡧࡧࡦࠩଐ"), None), bstack1lll11l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ଑"))
          bstack1ll1l11l1_opy_.execute_script(bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ଒") + json.dumps(bstack1lll11l_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥଓ") + str(self.feature.name) + bstack1lll11l_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥଔ")) + bstack1lll11l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨକ"))
          bstack1l1111l1_opy_(bstack1ll1l11l1_opy_, bstack1lll11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪଖ"))
          bstack1l11l1111_opy_ = bstack1llll1111_opy_(bstack1lll1l111_opy_, self.feature.name, logger)
          if (bstack1l11l1111_opy_ != None):
            bstack1l1lll1lll_opy_.append(bstack1l11l1111_opy_)
    except Exception as e:
      logger.debug(bstack1lll11l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ଗ").format(str(e)))
  else:
    bstack1lll1lll1l_opy_(self, name, context, *args)
  if name in [bstack1lll11l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬଘ"), bstack1lll11l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧଙ")]:
    bstack1lll1lll1l_opy_(self, name, context, *args)
    if (name == bstack1lll11l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨଚ") and self.driver_before_scenario) or (
            name == bstack1lll11l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨଛ") and not self.driver_before_scenario):
      try:
        bstack1ll1l11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11ll1l_opy_(bstack1lll11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨଜ")) else context.browser
        bstack1ll1l11l1_opy_.quit()
      except Exception:
        pass
def bstack1l1ll11lll_opy_(config, startdir):
  return bstack1lll11l_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣଝ").format(bstack1lll11l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥଞ"))
notset = Notset()
def bstack1llllll1l1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11llll1ll_opy_
  if str(name).lower() == bstack1lll11l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬଟ"):
    return bstack1lll11l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧଠ")
  else:
    return bstack11llll1ll_opy_(self, name, default, skip)
def bstack111111lll_opy_(item, when):
  global bstack1l111l1ll_opy_
  try:
    bstack1l111l1ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll111ll1_opy_():
  return
def bstack1l1l1l11ll_opy_(type, name, status, reason, bstack1l1l11ll1l_opy_, bstack1l1l111l1_opy_):
  bstack1l111ll1_opy_ = {
    bstack1lll11l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧଡ"): type,
    bstack1lll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଢ"): {}
  }
  if type == bstack1lll11l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫଣ"):
    bstack1l111ll1_opy_[bstack1lll11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ତ")][bstack1lll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪଥ")] = bstack1l1l11ll1l_opy_
    bstack1l111ll1_opy_[bstack1lll11l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଦ")][bstack1lll11l_opy_ (u"࠭ࡤࡢࡶࡤࠫଧ")] = json.dumps(str(bstack1l1l111l1_opy_))
  if type == bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨନ"):
    bstack1l111ll1_opy_[bstack1lll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ଩")][bstack1lll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧପ")] = name
  if type == bstack1lll11l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ଫ"):
    bstack1l111ll1_opy_[bstack1lll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧବ")][bstack1lll11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬଭ")] = status
    if status == bstack1lll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ମ"):
      bstack1l111ll1_opy_[bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଯ")][bstack1lll11l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨର")] = json.dumps(str(reason))
  bstack1llll1l1l1_opy_ = bstack1lll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ଱").format(json.dumps(bstack1l111ll1_opy_))
  return bstack1llll1l1l1_opy_
def bstack111ll111l_opy_(driver_command, response):
    if driver_command == bstack1lll11l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧଲ"):
        bstack1l11ll1ll_opy_.bstack111ll1l1l_opy_({
            bstack1lll11l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪଳ"): response[bstack1lll11l_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ଴")],
            bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ଵ"): bstack1l11ll1ll_opy_.current_test_uuid()
        })
def bstack1ll1llll_opy_(item, call, rep):
  global bstack11111llll_opy_
  global bstack11l1ll1ll_opy_
  global bstack111l11lll_opy_
  name = bstack1lll11l_opy_ (u"ࠧࠨଶ")
  try:
    if rep.when == bstack1lll11l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ଷ"):
      bstack1l1lllll1l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack111l11lll_opy_:
          name = str(rep.nodeid)
          bstack1lll11lll_opy_ = bstack1l1l1l11ll_opy_(bstack1lll11l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪସ"), name, bstack1lll11l_opy_ (u"ࠪࠫହ"), bstack1lll11l_opy_ (u"ࠫࠬ଺"), bstack1lll11l_opy_ (u"ࠬ࠭଻"), bstack1lll11l_opy_ (u"଼࠭ࠧ"))
          threading.current_thread().bstack1l1llll11l_opy_ = name
          for driver in bstack11l1ll1ll_opy_:
            if bstack1l1lllll1l_opy_ == driver.session_id:
              driver.execute_script(bstack1lll11lll_opy_)
      except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧଽ").format(str(e)))
      try:
        bstack11ll1l111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1lll11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩା"):
          status = bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩି") if rep.outcome.lower() == bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪୀ") else bstack1lll11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୁ")
          reason = bstack1lll11l_opy_ (u"ࠬ࠭ୂ")
          if status == bstack1lll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ୃ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1lll11l_opy_ (u"ࠧࡪࡰࡩࡳࠬୄ") if status == bstack1lll11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ୅") else bstack1lll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ୆")
          data = name + bstack1lll11l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬେ") if status == bstack1lll11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୈ") else name + bstack1lll11l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ୉") + reason
          bstack11l111l11_opy_ = bstack1l1l1l11ll_opy_(bstack1lll11l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ୊"), bstack1lll11l_opy_ (u"ࠧࠨୋ"), bstack1lll11l_opy_ (u"ࠨࠩୌ"), bstack1lll11l_opy_ (u"୍ࠩࠪ"), level, data)
          for driver in bstack11l1ll1ll_opy_:
            if bstack1l1lllll1l_opy_ == driver.session_id:
              driver.execute_script(bstack11l111l11_opy_)
      except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ୎").format(str(e)))
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨ୏").format(str(e)))
  bstack11111llll_opy_(item, call, rep)
def bstack1l1lll1l_opy_(driver, bstack1111lllll_opy_):
  PercySDK.screenshot(driver, bstack1111lllll_opy_)
def bstack1ll1111lll_opy_(driver):
  if bstack11lll11ll_opy_.bstack1l1ll1l11_opy_() is True or bstack11lll11ll_opy_.capturing() is True:
    return
  bstack11lll11ll_opy_.bstack1l1ll1lll_opy_()
  while not bstack11lll11ll_opy_.bstack1l1ll1l11_opy_():
    bstack1ll1111ll1_opy_ = bstack11lll11ll_opy_.bstack1ll1lll111_opy_()
    bstack1l1lll1l_opy_(driver, bstack1ll1111ll1_opy_)
  bstack11lll11ll_opy_.bstack11ll1ll1l_opy_()
def bstack1l1ll1111_opy_(sequence, driver_command, response = None):
    try:
      if sequence != bstack1lll11l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ୐"):
        return
      if not CONFIG.get(bstack1lll11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ୑"), False):
        return
      bstack1ll1111ll1_opy_ = bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୒"), None)
      for command in bstack1ll11llll_opy_:
        if command == driver_command:
          for driver in bstack11l1ll1ll_opy_:
            bstack1ll1111lll_opy_(driver)
      bstack1ll11l1l11_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫ୓"), bstack1lll11l_opy_ (u"ࠤࡤࡹࡹࡵࠢ୔"))
      if driver_command in bstack1ll11lllll_opy_[bstack1ll11l1l11_opy_]:
        bstack11lll11ll_opy_.bstack1lllll111_opy_(bstack1ll1111ll1_opy_, driver_command)
    except Exception as e:
      pass
def bstack1lllll1ll1_opy_(framework_name):
  global bstack11l1111l1_opy_
  global bstack11l11l11_opy_
  global bstack1l1111lll_opy_
  bstack11l1111l1_opy_ = framework_name
  logger.info(bstack1ll11lll1_opy_.format(bstack11l1111l1_opy_.split(bstack1lll11l_opy_ (u"ࠪ࠱ࠬ୕"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll1ll1l_opy_:
      Service.start = bstack1ll1ll111l_opy_
      Service.stop = bstack1ll11ll1l1_opy_
      webdriver.Remote.get = bstack1llll11l11_opy_
      WebDriver.close = bstack1lll11111_opy_
      WebDriver.quit = bstack11111l11l_opy_
      webdriver.Remote.__init__ = bstack1ll111l11_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack1ll1lll11_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1l1l11l11l_opy_ = getAccessibilityResultsSummary
    if not bstack1ll1ll1l_opy_ and bstack1l11ll1ll_opy_.on():
      webdriver.Remote.__init__ = bstack1llll1l111_opy_
    if bstack1lll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪୖ") in str(framework_name).lower() and bstack1l11ll1ll_opy_.on():
      WebDriver.execute = bstack11lllll11_opy_
    bstack11l11l11_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1ll1ll1l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11lll111_opy_
  except Exception as e:
    pass
  bstack1ll1l1l1l1_opy_()
  if not bstack11l11l11_opy_:
    bstack1l11ll11_opy_(bstack1lll11l_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢୗ"), bstack11l1111l_opy_)
  if bstack11l11ll11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1llll11ll_opy_
    except Exception as e:
      logger.error(bstack1111lll1_opy_.format(str(e)))
  if bstack1l1ll1l1l_opy_():
    bstack1llllllll1_opy_(CONFIG, logger)
  if (bstack1lll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ୘") in str(framework_name).lower()):
    if not bstack1ll1ll1l_opy_:
      return
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack1lll11l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭୙"), False):
          bstack1l1ll1l1_opy_(bstack1l1ll1111_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll1llllll_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1llll1ll11_opy_
      except Exception as e:
        logger.warn(bstack1l1l1ll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1ll11ll11l_opy_
      except Exception as e:
        logger.debug(bstack11llll1l_opy_ + str(e))
    except Exception as e:
      bstack1l11ll11_opy_(e, bstack1l1l1ll1_opy_)
    Output.start_test = bstack1ll1ll1ll_opy_
    Output.end_test = bstack111ll1ll1_opy_
    TestStatus.__init__ = bstack1lll1ll1ll_opy_
    QueueItem.__init__ = bstack111ll1lll_opy_
    pabot._create_items = bstack1l1l11l11_opy_
    try:
      from pabot import __version__ as bstack11l1ll1l_opy_
      if version.parse(bstack11l1ll1l_opy_) >= version.parse(bstack1lll11l_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨ୚")):
        pabot._run = bstack11lll1ll_opy_
      elif version.parse(bstack11l1ll1l_opy_) >= version.parse(bstack1lll11l_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ୛")):
        pabot._run = bstack111ll111_opy_
      else:
        pabot._run = bstack1ll111l111_opy_
    except Exception as e:
      pabot._run = bstack1ll111l111_opy_
    pabot._create_command_for_execution = bstack11ll1lll1_opy_
    pabot._report_results = bstack1lll1l1l_opy_
  if bstack1lll11l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪଡ଼") in str(framework_name).lower():
    if not bstack1ll1ll1l_opy_:
      return
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11ll11_opy_(e, bstack11llllll_opy_)
    Runner.run_hook = bstack111llll11_opy_
    Step.run = bstack1ll11llll1_opy_
  if bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫଢ଼") in str(framework_name).lower():
    if not bstack1ll1ll1l_opy_:
      return
    try:
      if CONFIG.get(bstack1lll11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ୞"), False):
          bstack1l1ll1l1_opy_(bstack1l1ll1111_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l1ll11lll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll111ll1_opy_
      Config.getoption = bstack1llllll1l1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1ll1llll_opy_
    except Exception as e:
      pass
def bstack1l111l11_opy_():
  global CONFIG
  if bstack1lll11l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ୟ") in CONFIG and int(CONFIG[bstack1lll11l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧୠ")]) > 1:
    logger.warn(bstack1l1ll1l111_opy_)
def bstack11ll1lll_opy_(arg, bstack1ll11111l_opy_, bstack1l111111_opy_=None):
  global CONFIG
  global bstack1l1l1l11_opy_
  global bstack111l1ll1_opy_
  global bstack1ll1ll1l_opy_
  global bstack1l1l1ll1ll_opy_
  bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨୡ")
  if bstack1ll11111l_opy_ and isinstance(bstack1ll11111l_opy_, str):
    bstack1ll11111l_opy_ = eval(bstack1ll11111l_opy_)
  CONFIG = bstack1ll11111l_opy_[bstack1lll11l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩୢ")]
  bstack1l1l1l11_opy_ = bstack1ll11111l_opy_[bstack1lll11l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫୣ")]
  bstack111l1ll1_opy_ = bstack1ll11111l_opy_[bstack1lll11l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭୤")]
  bstack1ll1ll1l_opy_ = bstack1ll11111l_opy_[bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ୥")]
  bstack1l1l1ll1ll_opy_.bstack11l1l1ll_opy_(bstack1lll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ୦"), bstack1ll1ll1l_opy_)
  os.environ[bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ୧")] = bstack11l11l1ll_opy_
  os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ୨")] = json.dumps(CONFIG)
  os.environ[bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ୩")] = bstack1l1l1l11_opy_
  os.environ[bstack1lll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ୪")] = str(bstack111l1ll1_opy_)
  os.environ[bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪ୫")] = str(True)
  if bstack1l1l1l11l1_opy_(arg, [bstack1lll11l_opy_ (u"ࠬ࠳࡮ࠨ୬"), bstack1lll11l_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ୭")]) != -1:
    os.environ[bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ୮")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111lllll1_opy_)
    return
  bstack11111ll1l_opy_()
  global bstack1ll1l111ll_opy_
  global bstack1ll1l1l111_opy_
  global bstack1l1lllll11_opy_
  global bstack1l11l1l11_opy_
  global bstack1l1l1lll1l_opy_
  global bstack1l1111lll_opy_
  global bstack1l111l1l_opy_
  arg.append(bstack1lll11l_opy_ (u"ࠣ࠯࡚ࠦ୯"))
  arg.append(bstack1lll11l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡐࡳࡩࡻ࡬ࡦࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡲࡶ࡯ࡳࡶࡨࡨ࠿ࡶࡹࡵࡧࡶࡸ࠳ࡖࡹࡵࡧࡶࡸ࡜ࡧࡲ࡯࡫ࡱ࡫ࠧ୰"))
  arg.append(bstack1lll11l_opy_ (u"ࠥ࠱࡜ࠨୱ"))
  arg.append(bstack1lll11l_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾࡙࡮ࡥࠡࡪࡲࡳࡰ࡯࡭ࡱ࡮ࠥ୲"))
  global bstack1llll11l_opy_
  global bstack1l1l11ll_opy_
  global bstack1ll1111l_opy_
  global bstack1l1lll111_opy_
  global bstack1lllll1111_opy_
  global bstack1ll1ll11ll_opy_
  global bstack1llll11l1l_opy_
  global bstack1ll1ll111_opy_
  global bstack1l1l11llll_opy_
  global bstack11llll1ll_opy_
  global bstack1l111l1ll_opy_
  global bstack11111llll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1llll11l_opy_ = webdriver.Remote.__init__
    bstack1l1l11ll_opy_ = WebDriver.quit
    bstack1llll11l1l_opy_ = WebDriver.close
    bstack1ll1ll111_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1ll111llll_opy_(CONFIG) and bstack1lll11lll1_opy_():
    if bstack1lll1ll1l_opy_() < version.parse(bstack1lll1l111l_opy_):
      logger.error(bstack11l11l1l_opy_.format(bstack1lll1ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l11llll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1111lll1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack11llll1ll_opy_ = Config.getoption
    from _pytest import runner
    bstack1l111l1ll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11111l1l1_opy_)
  try:
    from pytest_bdd import reporting
    bstack11111llll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1lll11l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭୳"))
  bstack1l1lllll11_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ୴"), {}).get(bstack1lll11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ୵"))
  bstack1l111l1l_opy_ = True
  bstack1lllll1ll1_opy_(bstack1111ll1l_opy_)
  os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ୶")] = CONFIG[bstack1lll11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ୷")]
  os.environ[bstack1lll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭୸")] = CONFIG[bstack1lll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ୹")]
  os.environ[bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ୺")] = bstack1ll1ll1l_opy_.__str__()
  from _pytest.config import main as bstack1111111ll_opy_
  bstack1111111ll_opy_(arg)
  if bstack1lll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ୻") in multiprocessing.current_process().__dict__.keys():
    for bstack1111l11l1_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack1l111111_opy_.append(bstack1111l11l1_opy_)
def bstack11111111_opy_(arg):
  bstack1lllll1ll1_opy_(bstack1l1ll1ll1l_opy_)
  os.environ[bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ୼")] = str(bstack111l1ll1_opy_)
  from behave.__main__ import main as bstack1lll111l1l_opy_
  bstack1lll111l1l_opy_(arg)
def bstack1lll1l1111_opy_():
  logger.info(bstack1l1ll11l1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ୽"), help=bstack1lll11l_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪ୾"))
  parser.add_argument(bstack1lll11l_opy_ (u"ࠪ࠱ࡺ࠭୿"), bstack1lll11l_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨ஀"), help=bstack1lll11l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ஁"))
  parser.add_argument(bstack1lll11l_opy_ (u"࠭࠭࡬ࠩஂ"), bstack1lll11l_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ஃ"), help=bstack1lll11l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩ஄"))
  parser.add_argument(bstack1lll11l_opy_ (u"ࠩ࠰ࡪࠬஅ"), bstack1lll11l_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨஆ"), help=bstack1lll11l_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪஇ"))
  bstack1l1l11l1_opy_ = parser.parse_args()
  try:
    bstack1lll11l1l_opy_ = bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩஈ")
    if bstack1l1l11l1_opy_.framework and bstack1l1l11l1_opy_.framework not in (bstack1lll11l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭உ"), bstack1lll11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨஊ")):
      bstack1lll11l1l_opy_ = bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧ஋")
    bstack1ll1l1111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll11l1l_opy_)
    bstack1lll11ll1l_opy_ = open(bstack1ll1l1111_opy_, bstack1lll11l_opy_ (u"ࠩࡵࠫ஌"))
    bstack1l11111l1_opy_ = bstack1lll11ll1l_opy_.read()
    bstack1lll11ll1l_opy_.close()
    if bstack1l1l11l1_opy_.username:
      bstack1l11111l1_opy_ = bstack1l11111l1_opy_.replace(bstack1lll11l_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ஍"), bstack1l1l11l1_opy_.username)
    if bstack1l1l11l1_opy_.key:
      bstack1l11111l1_opy_ = bstack1l11111l1_opy_.replace(bstack1lll11l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭எ"), bstack1l1l11l1_opy_.key)
    if bstack1l1l11l1_opy_.framework:
      bstack1l11111l1_opy_ = bstack1l11111l1_opy_.replace(bstack1lll11l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ஏ"), bstack1l1l11l1_opy_.framework)
    file_name = bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩஐ")
    file_path = os.path.abspath(file_name)
    bstack1ll11l11_opy_ = open(file_path, bstack1lll11l_opy_ (u"ࠧࡸࠩ஑"))
    bstack1ll11l11_opy_.write(bstack1l11111l1_opy_)
    bstack1ll11l11_opy_.close()
    logger.info(bstack1l1l1ll11l_opy_)
    try:
      os.environ[bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪஒ")] = bstack1l1l11l1_opy_.framework if bstack1l1l11l1_opy_.framework != None else bstack1lll11l_opy_ (u"ࠤࠥஓ")
      config = yaml.safe_load(bstack1l11111l1_opy_)
      config[bstack1lll11l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪஔ")] = bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪக")
      bstack1ll111l1ll_opy_(bstack1lll111l1_opy_, config)
    except Exception as e:
      logger.debug(bstack1lll111ll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack111l1l1l1_opy_.format(str(e)))
def bstack1ll111l1ll_opy_(bstack1ll1ll1111_opy_, config, bstack1ll1l1l11l_opy_={}):
  global bstack1ll1ll1l_opy_
  global bstack1ll11111_opy_
  if not config:
    return
  bstack1lll1111l_opy_ = bstack1llllll11_opy_ if not bstack1ll1ll1l_opy_ else (
    bstack1111l1lll_opy_ if bstack1lll11l_opy_ (u"ࠬࡧࡰࡱࠩ஖") in config else bstack1l1lll11l_opy_)
  data = {
    bstack1lll11l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ஗"): config[bstack1lll11l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ஘")],
    bstack1lll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫங"): config[bstack1lll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬச")],
    bstack1lll11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ஛"): bstack1ll1ll1111_opy_,
    bstack1lll11l_opy_ (u"ࠫࡩ࡫ࡴࡦࡥࡷࡩࡩࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨஜ"): os.environ.get(bstack1lll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ஝"), bstack1ll11111_opy_),
    bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨஞ"): bstack1llll1llll_opy_,
    bstack1lll11l_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭ࠩட"): bstack1l11llll_opy_(),
    bstack1lll11l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ஠"): {
      bstack1lll11l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ஡"): str(config[bstack1lll11l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ஢")]) if bstack1lll11l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫண") in config else bstack1lll11l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨத"),
      bstack1lll11l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡗࡧࡵࡷ࡮ࡵ࡮ࠨ஥"): sys.version,
      bstack1lll11l_opy_ (u"ࠧࡳࡧࡩࡩࡷࡸࡥࡳࠩ஦"): bstack1lll11l1_opy_(os.getenv(bstack1lll11l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥ஧"), bstack1lll11l_opy_ (u"ࠤࠥந"))),
      bstack1lll11l_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬன"): bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫப"),
      bstack1lll11l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭஫"): bstack1lll1111l_opy_,
      bstack1lll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ஬"): config[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஭")] if config[bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫம")] else bstack1lll11l_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥய"),
      bstack1lll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬர"): str(config[bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ற")]) if bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧல") in config else bstack1lll11l_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢள"),
      bstack1lll11l_opy_ (u"ࠧࡰࡵࠪழ"): sys.platform,
      bstack1lll11l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪவ"): socket.gethostname()
    }
  }
  update(data[bstack1lll11l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬஶ")], bstack1ll1l1l11l_opy_)
  try:
    response = bstack1l1llllll1_opy_(bstack1lll11l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨஷ"), bstack1lll1l1l1l_opy_(bstack111ll1l1_opy_), data, {
      bstack1lll11l_opy_ (u"ࠫࡦࡻࡴࡩࠩஸ"): (config[bstack1lll11l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧஹ")], config[bstack1lll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ஺")])
    })
    if response:
      logger.debug(bstack11l11111l_opy_.format(bstack1ll1ll1111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1ll1111l_opy_.format(str(e)))
def bstack1lll11l1_opy_(framework):
  return bstack1lll11l_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦ஻").format(str(framework), __version__) if framework else bstack1lll11l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ஼").format(
    __version__)
def bstack11111ll1l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1ll111ll11_opy_()
    logger.debug(bstack1lll1111ll_opy_.format(str(CONFIG)))
    bstack1lll1l11l1_opy_()
    bstack11l1lllll_opy_()
  except Exception as e:
    logger.error(bstack1lll11l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨ஽") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1llll11ll1_opy_
  atexit.register(bstack111llll1_opy_)
  signal.signal(signal.SIGINT, bstack1lllll11_opy_)
  signal.signal(signal.SIGTERM, bstack1lllll11_opy_)
def bstack1llll11ll1_opy_(exctype, value, traceback):
  global bstack11l1ll1ll_opy_
  try:
    for driver in bstack11l1ll1ll_opy_:
      bstack1l1111l1_opy_(driver, bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪா"), bstack1lll11l_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢி") + str(value))
  except Exception:
    pass
  bstack1llll1ll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1llll1ll_opy_(message=bstack1lll11l_opy_ (u"ࠬ࠭ீ"), bstack11l1ll11_opy_ = False):
  global CONFIG
  bstack1l1l1ll111_opy_ = bstack1lll11l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨு") if bstack11l1ll11_opy_ else bstack1lll11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ூ")
  try:
    if message:
      bstack1ll1l1l11l_opy_ = {
        bstack1l1l1ll111_opy_ : str(message)
      }
      bstack1ll111l1ll_opy_(bstack1l1l1llll1_opy_, CONFIG, bstack1ll1l1l11l_opy_)
    else:
      bstack1ll111l1ll_opy_(bstack1l1l1llll1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1lllll1l11_opy_.format(str(e)))
def bstack1l1l1llll_opy_(bstack1ll11l111_opy_, size):
  bstack1l11111ll_opy_ = []
  while len(bstack1ll11l111_opy_) > size:
    bstack1l1l1lll_opy_ = bstack1ll11l111_opy_[:size]
    bstack1l11111ll_opy_.append(bstack1l1l1lll_opy_)
    bstack1ll11l111_opy_ = bstack1ll11l111_opy_[size:]
  bstack1l11111ll_opy_.append(bstack1ll11l111_opy_)
  return bstack1l11111ll_opy_
def bstack11l1l11l1_opy_(args):
  if bstack1lll11l_opy_ (u"ࠨ࠯ࡰࠫ௃") in args and bstack1lll11l_opy_ (u"ࠩࡳࡨࡧ࠭௄") in args:
    return True
  return False
def run_on_browserstack(bstack11ll1111_opy_=None, bstack1l111111_opy_=None, bstack111l11ll1_opy_=False):
  global CONFIG
  global bstack1l1l1l11_opy_
  global bstack111l1ll1_opy_
  global bstack1ll11111_opy_
  bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠪࠫ௅")
  bstack11l111ll1_opy_(bstack1ll1l1lll1_opy_, logger)
  if bstack11ll1111_opy_ and isinstance(bstack11ll1111_opy_, str):
    bstack11ll1111_opy_ = eval(bstack11ll1111_opy_)
  if bstack11ll1111_opy_:
    CONFIG = bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫெ")]
    bstack1l1l1l11_opy_ = bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ே")]
    bstack111l1ll1_opy_ = bstack11ll1111_opy_[bstack1lll11l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨை")]
    bstack1l1l1ll1ll_opy_.bstack11l1l1ll_opy_(bstack1lll11l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ௉"), bstack111l1ll1_opy_)
    bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨொ")
  if not bstack111l11ll1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111lllll1_opy_)
      return
    if sys.argv[1] == bstack1lll11l_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬோ") or sys.argv[1] == bstack1lll11l_opy_ (u"ࠪ࠱ࡻ࠭ௌ"):
      logger.info(bstack1lll11l_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀ்ࠫ").format(__version__))
      return
    if sys.argv[1] == bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ௎"):
      bstack1lll1l1111_opy_()
      return
  args = sys.argv
  bstack11111ll1l_opy_()
  global bstack1ll1l111ll_opy_
  global bstack111llllll_opy_
  global bstack1l111l1l_opy_
  global bstack1ll11lll_opy_
  global bstack1ll1l1l111_opy_
  global bstack1l1lllll11_opy_
  global bstack1l11l1l11_opy_
  global bstack1ll1ll1lll_opy_
  global bstack1l1l1lll1l_opy_
  global bstack1l1111lll_opy_
  global bstack111l111l1_opy_
  bstack111llllll_opy_ = len(CONFIG[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௏")])
  if not bstack11l11l1ll_opy_:
    if args[1] == bstack1lll11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧௐ") or args[1] == bstack1lll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ௑"):
      bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௒")
      args = args[2:]
    elif args[1] == bstack1lll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௓"):
      bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௔")
      args = args[2:]
    elif args[1] == bstack1lll11l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ௕"):
      bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ௖")
      args = args[2:]
    elif args[1] == bstack1lll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨௗ"):
      bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ௘")
      args = args[2:]
    elif args[1] == bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ௙"):
      bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௚")
      args = args[2:]
    elif args[1] == bstack1lll11l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ௛"):
      bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௜")
      args = args[2:]
    else:
      if not bstack1lll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௝") in CONFIG or str(CONFIG[bstack1lll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ௞")]).lower() in [bstack1lll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௟"), bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ௠")]:
        bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௡")
        args = args[1:]
      elif str(CONFIG[bstack1lll11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ௢")]).lower() == bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௣"):
        bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௤")
        args = args[1:]
      elif str(CONFIG[bstack1lll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ௥")]).lower() == bstack1lll11l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௦"):
        bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௧")
        args = args[1:]
      elif str(CONFIG[bstack1lll11l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭௨")]).lower() == bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௩"):
        bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௪")
        args = args[1:]
      elif str(CONFIG[bstack1lll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௫")]).lower() == bstack1lll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௬"):
        bstack11l11l1ll_opy_ = bstack1lll11l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ௭")
        args = args[1:]
      else:
        os.environ[bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ௮")] = bstack11l11l1ll_opy_
        bstack11l1llll_opy_(bstack1llll1l11_opy_)
  os.environ[bstack1lll11l_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫ௯")] = bstack11l11l1ll_opy_
  bstack1ll11111_opy_ = bstack11l11l1ll_opy_
  global bstack1l1l1l1l1l_opy_
  if bstack11ll1111_opy_:
    try:
      os.environ[bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭௰")] = bstack11l11l1ll_opy_
      bstack1ll111l1ll_opy_(bstack11llll11l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1lllll1l11_opy_.format(str(e)))
  global bstack1llll11l_opy_
  global bstack1l1l11ll_opy_
  global bstack1lllll1lll_opy_
  global bstack1lll11llll_opy_
  global bstack1l1ll1lll1_opy_
  global bstack1llll1l1ll_opy_
  global bstack1ll1111l_opy_
  global bstack1l1lll111_opy_
  global bstack1ll111l1_opy_
  global bstack1lllll1111_opy_
  global bstack1ll1ll11ll_opy_
  global bstack1llll11l1l_opy_
  global bstack1lll1lll1l_opy_
  global bstack1llll1111l_opy_
  global bstack1ll1ll111_opy_
  global bstack1l1l11llll_opy_
  global bstack11llll1ll_opy_
  global bstack1l111l1ll_opy_
  global bstack1l1l11ll1_opy_
  global bstack11111llll_opy_
  global bstack1ll1l11ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1llll11l_opy_ = webdriver.Remote.__init__
    bstack1l1l11ll_opy_ = WebDriver.quit
    bstack1llll11l1l_opy_ = WebDriver.close
    bstack1ll1ll111_opy_ = WebDriver.get
    bstack1ll1l11ll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1l1l1l1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack11l111l1_opy_
    from QWeb.keywords import browser
    bstack11l111l1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll111llll_opy_(CONFIG) and bstack1lll11lll1_opy_():
    if bstack1lll1ll1l_opy_() < version.parse(bstack1lll1l111l_opy_):
      logger.error(bstack11l11l1l_opy_.format(bstack1lll1ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l11llll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1111lll1_opy_.format(str(e)))
  if bstack11l11l1ll_opy_ != bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௱") or (bstack11l11l1ll_opy_ == bstack1lll11l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௲") and not bstack11ll1111_opy_):
    bstack1ll11l1ll1_opy_()
  if (bstack11l11l1ll_opy_ in [bstack1lll11l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭௳"), bstack1lll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௴"), bstack1lll11l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௵")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll1llllll_opy_
        bstack1llll1l1ll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1l1ll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l1ll1lll1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11llll1l_opy_ + str(e))
    except Exception as e:
      bstack1l11ll11_opy_(e, bstack1l1l1ll1_opy_)
    if bstack11l11l1ll_opy_ != bstack1lll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௶"):
      bstack111l1ll11_opy_()
    bstack1lllll1lll_opy_ = Output.start_test
    bstack1lll11llll_opy_ = Output.end_test
    bstack1ll1111l_opy_ = TestStatus.__init__
    bstack1ll111l1_opy_ = pabot._run
    bstack1lllll1111_opy_ = QueueItem.__init__
    bstack1ll1ll11ll_opy_ = pabot._create_command_for_execution
    bstack1l1l11ll1_opy_ = pabot._report_results
  if bstack11l11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ௷"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11ll11_opy_(e, bstack11llllll_opy_)
    bstack1lll1lll1l_opy_ = Runner.run_hook
    bstack1llll1111l_opy_ = Step.run
  if bstack11l11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௸"):
    try:
      from _pytest.config import Config
      bstack11llll1ll_opy_ = Config.getoption
      from _pytest import runner
      bstack1l111l1ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11111l1l1_opy_)
    try:
      from pytest_bdd import reporting
      bstack11111llll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1lll11l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ௹"))
  if bstack11l11l1ll_opy_ in bstack111l11l1_opy_:
    try:
      framework_name = bstack1lll11l_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭௺") if bstack11l11l1ll_opy_ in [bstack1lll11l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௻"), bstack1lll11l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௼"), bstack1lll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௽")] else bstack1l11l1ll_opy_(bstack11l11l1ll_opy_)
      bstack1l11ll1ll_opy_.launch(CONFIG, {
        bstack1lll11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ௾"): bstack1lll11l_opy_ (u"ࠬࢁ࠰ࡾ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ௿").format(framework_name) if bstack11l11l1ll_opy_ == bstack1lll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ఀ") and bstack1111l111_opy_() else framework_name,
        bstack1lll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫఁ"): bstack1l1ll11l11_opy_(framework_name),
        bstack1lll11l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ం"): __version__
      })
    except Exception as e:
      logger.debug(bstack111l11111_opy_.format(bstack1lll11l_opy_ (u"ࠩࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩః"), str(e)))
  if bstack11l11l1ll_opy_ in bstack1l1lll1ll_opy_:
    try:
      framework_name = bstack1lll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩఄ") if bstack11l11l1ll_opy_ in [bstack1lll11l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪఅ"), bstack1lll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫఆ")] else bstack11l11l1ll_opy_
      if bstack1ll1ll1l_opy_ and bstack1lll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ఇ") in CONFIG and CONFIG[bstack1lll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧఈ")] == True:
        if bstack1lll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨఉ") in CONFIG:
          os.environ[bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪఊ")] = os.getenv(bstack1lll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫఋ"), json.dumps(CONFIG[bstack1lll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫఌ")]))
          CONFIG[bstack1lll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ఍")].pop(bstack1lll11l_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫఎ"), None)
          CONFIG[bstack1lll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧఏ")].pop(bstack1lll11l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ఐ"), None)
        bstack1l1l1l1l1_opy_, bstack111111ll_opy_ = bstack111ll11l1_opy_.bstack1l1l11lll1_opy_(CONFIG, bstack11l11l1ll_opy_, bstack1l1ll11l11_opy_(framework_name))
        if not bstack1l1l1l1l1_opy_ is None:
          os.environ[bstack1lll11l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ఑")] = bstack1l1l1l1l1_opy_
          os.environ[bstack1lll11l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡕ࡙ࡓࡥࡉࡅࠩఒ")] = str(bstack111111ll_opy_)
    except Exception as e:
      logger.debug(bstack111l11111_opy_.format(bstack1lll11l_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫఓ"), str(e)))
  if bstack11l11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬఔ"):
    bstack1l111l1l_opy_ = True
    if bstack11ll1111_opy_ and bstack111l11ll1_opy_:
      bstack1l1lllll11_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪక"), {}).get(bstack1lll11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఖ"))
      bstack1lllll1ll1_opy_(bstack111111l11_opy_)
    elif bstack11ll1111_opy_:
      bstack1l1lllll11_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬగ"), {}).get(bstack1lll11l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫఘ"))
      global bstack11l1ll1ll_opy_
      try:
        if bstack11l1l11l1_opy_(bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఙ")]) and multiprocessing.current_process().name == bstack1lll11l_opy_ (u"ࠫ࠵࠭చ"):
          bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఛ")].remove(bstack1lll11l_opy_ (u"࠭࠭࡮ࠩజ"))
          bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఝ")].remove(bstack1lll11l_opy_ (u"ࠨࡲࡧࡦࠬఞ"))
          bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬట")] = bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఠ")][0]
          with open(bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧడ")], bstack1lll11l_opy_ (u"ࠬࡸࠧఢ")) as f:
            bstack1ll11l1ll_opy_ = f.read()
          bstack1ll111ll1l_opy_ = bstack1lll11l_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࡷࡶࡾࡀࠊࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࡧࡻࡧࡪࡶࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡦࡹࠠࡦ࠼ࠍࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࡓࡨࡧ࠮ࠩ࠯ࡵࡨࡸࡤࡺࡲࡢࡥࡨࠬ࠮ࡢ࡮ࠣࠤࠥణ").format(str(bstack11ll1111_opy_))
          bstack111l1ll1l_opy_ = bstack1ll111ll1l_opy_ + bstack1ll11l1ll_opy_
          bstack1llll1ll1_opy_ = bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪత")] + bstack1lll11l_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻࠪథ")
          with open(bstack1llll1ll1_opy_, bstack1lll11l_opy_ (u"ࠩࡺࠫద")):
            pass
          with open(bstack1llll1ll1_opy_, bstack1lll11l_opy_ (u"ࠥࡻ࠰ࠨధ")) as f:
            f.write(bstack111l1ll1l_opy_)
          import subprocess
          bstack1lll11l11_opy_ = subprocess.run([bstack1lll11l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦన"), bstack1llll1ll1_opy_])
          if os.path.exists(bstack1llll1ll1_opy_):
            os.unlink(bstack1llll1ll1_opy_)
          os._exit(bstack1lll11l11_opy_.returncode)
        else:
          if bstack11l1l11l1_opy_(bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ఩")]):
            bstack11ll1111_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩప")].remove(bstack1lll11l_opy_ (u"ࠧ࠮࡯ࠪఫ"))
            bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫబ")].remove(bstack1lll11l_opy_ (u"ࠩࡳࡨࡧ࠭భ"))
            bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭మ")] = bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧయ")][0]
          bstack1lllll1ll1_opy_(bstack111111l11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨర")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1lll11l_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨఱ")] = bstack1lll11l_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩల")
          mod_globals[bstack1lll11l_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪళ")] = os.path.abspath(bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఴ")])
          exec(open(bstack11ll1111_opy_[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭వ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1lll11l_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫశ").format(str(e)))
          for driver in bstack11l1ll1ll_opy_:
            bstack1l111111_opy_.append({
              bstack1lll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪష"): bstack11ll1111_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩస")],
              bstack1lll11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭హ"): str(e),
              bstack1lll11l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ఺"): multiprocessing.current_process().name
            })
            bstack1l1111l1_opy_(driver, bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ఻"), bstack1lll11l_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ఼") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l1ll1ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack111l1ll1_opy_, CONFIG, logger)
      bstack1l1ll1l1l1_opy_()
      bstack1l111l11_opy_()
      bstack1ll11111l_opy_ = {
        bstack1lll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧఽ"): args[0],
        bstack1lll11l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬా"): CONFIG,
        bstack1lll11l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧి"): bstack1l1l1l11_opy_,
        bstack1lll11l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩీ"): bstack111l1ll1_opy_
      }
      percy.bstack11l1l11ll_opy_()
      if bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫు") in CONFIG:
        bstack1l1l111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1lll1111_opy_ = manager.list()
        if bstack11l1l11l1_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬూ")]):
            if index == 0:
              bstack1ll11111l_opy_[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ృ")] = args
            bstack1l1l111l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1ll11111l_opy_, bstack1l1lll1111_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౄ")]):
            bstack1l1l111l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1ll11111l_opy_, bstack1l1lll1111_opy_)))
        for t in bstack1l1l111l_opy_:
          t.start()
        for t in bstack1l1l111l_opy_:
          t.join()
        bstack1ll1ll1lll_opy_ = list(bstack1l1lll1111_opy_)
      else:
        if bstack11l1l11l1_opy_(args):
          bstack1ll11111l_opy_[bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ౅")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1ll11111l_opy_,))
          test.start()
          test.join()
        else:
          bstack1lllll1ll1_opy_(bstack111111l11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1lll11l_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨె")] = bstack1lll11l_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩే")
          mod_globals[bstack1lll11l_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪై")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11l11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ౉") or bstack11l11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩొ"):
    percy.init(bstack111l1ll1_opy_, CONFIG, logger)
    percy.bstack11l1l11ll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l11ll11_opy_(e, bstack1l1l1ll1_opy_)
    bstack1l1ll1l1l1_opy_()
    bstack1lllll1ll1_opy_(bstack11l1l1l1l_opy_)
    if bstack1lll11l_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩో") in args:
      i = args.index(bstack1lll11l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪౌ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1ll1l111ll_opy_))
    args.insert(0, str(bstack1lll11l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶ్ࠫ")))
    if bstack1l11ll1ll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1lll1l1l1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1llllll1l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1lll11l_opy_ (u"ࠢࡓࡑࡅࡓ࡙ࡥࡏࡑࡖࡌࡓࡓ࡙ࠢ౎"),
        ).parse_args(bstack1lll1l1l1_opy_)
        args.insert(args.index(bstack1llllll1l_opy_[0]), str(bstack1lll11l_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬ౏")))
        args.insert(args.index(bstack1llllll1l_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴ࠱ࡴࡾ࠭౐"))))
        if bstack1l1l1ll11_opy_(os.environ.get(bstack1lll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ౑"))) and str(os.environ.get(bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨ౒"), bstack1lll11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ౓"))) != bstack1lll11l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ౔"):
          for bstack1llll111ll_opy_ in bstack1llllll1l_opy_:
            args.remove(bstack1llll111ll_opy_)
          bstack111111ll1_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖౕࠫ")).split(bstack1lll11l_opy_ (u"ࠨ࠮ౖࠪ"))
          for bstack1l11ll11l_opy_ in bstack111111ll1_opy_:
            args.append(bstack1l11ll11l_opy_)
      except Exception as e:
        logger.error(bstack1lll11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࠧ౗").format(e))
    pabot.main(args)
  elif bstack11l11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫౘ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l11ll11_opy_(e, bstack1l1l1ll1_opy_)
    for a in args:
      if bstack1lll11l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪౙ") in a:
        bstack1ll1l1l111_opy_ = int(a.split(bstack1lll11l_opy_ (u"ࠬࡀࠧౚ"))[1])
      if bstack1lll11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ౛") in a:
        bstack1l1lllll11_opy_ = str(a.split(bstack1lll11l_opy_ (u"ࠧ࠻ࠩ౜"))[1])
      if bstack1lll11l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨౝ") in a:
        bstack1l11l1l11_opy_ = str(a.split(bstack1lll11l_opy_ (u"ࠩ࠽ࠫ౞"))[1])
    bstack11l11lll1_opy_ = None
    if bstack1lll11l_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩ౟") in args:
      i = args.index(bstack1lll11l_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪౠ"))
      args.pop(i)
      bstack11l11lll1_opy_ = args.pop(i)
    if bstack11l11lll1_opy_ is not None:
      global bstack1l1ll1ll11_opy_
      bstack1l1ll1ll11_opy_ = bstack11l11lll1_opy_
    bstack1lllll1ll1_opy_(bstack11l1l1l1l_opy_)
    run_cli(args)
    if bstack1lll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩౡ") in multiprocessing.current_process().__dict__.keys():
      for bstack1111l11l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l111111_opy_.append(bstack1111l11l1_opy_)
  elif bstack11l11l1ll_opy_ == bstack1lll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ౢ"):
    percy.init(bstack111l1ll1_opy_, CONFIG, logger)
    percy.bstack11l1l11ll_opy_()
    bstack1lll11l111_opy_ = bstack1ll111111_opy_(args, logger, CONFIG, bstack1ll1ll1l_opy_)
    bstack1lll11l111_opy_.bstack11l1lll1_opy_()
    bstack1l1ll1l1l1_opy_()
    bstack1ll11lll_opy_ = True
    bstack1l1111lll_opy_ = bstack1lll11l111_opy_.bstack1ll1lll1l1_opy_()
    bstack1lll11l111_opy_.bstack1ll11111l_opy_(bstack111l11lll_opy_)
    bstack1l1l1lll1l_opy_ = bstack1lll11l111_opy_.bstack1l1l11l111_opy_(bstack11ll1lll_opy_, {
      bstack1lll11l_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨౣ"): bstack1l1l1l11_opy_,
      bstack1lll11l_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ౤"): bstack111l1ll1_opy_,
      bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ౥"): bstack1ll1ll1l_opy_
    })
    bstack111l111l1_opy_ = 1 if len(bstack1l1l1lll1l_opy_) > 0 else 0
  elif bstack11l11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ౦"):
    try:
      from behave.__main__ import main as bstack1lll111l1l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l11ll11_opy_(e, bstack11llllll_opy_)
    bstack1l1ll1l1l1_opy_()
    bstack1ll11lll_opy_ = True
    bstack1l11ll1l1_opy_ = 1
    if bstack1lll11l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ౧") in CONFIG:
      bstack1l11ll1l1_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ౨")]
    bstack1ll1111l11_opy_ = int(bstack1l11ll1l1_opy_) * int(len(CONFIG[bstack1lll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౩")]))
    config = Configuration(args)
    bstack1ll1l111l_opy_ = config.paths
    if len(bstack1ll1l111l_opy_) == 0:
      import glob
      pattern = bstack1lll11l_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭౪")
      bstack11ll1l1l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11ll1l1l1_opy_)
      config = Configuration(args)
      bstack1ll1l111l_opy_ = config.paths
    bstack111l1l111_opy_ = [os.path.normpath(item) for item in bstack1ll1l111l_opy_]
    bstack11l1l1lll_opy_ = [os.path.normpath(item) for item in args]
    bstack1111111l1_opy_ = [item for item in bstack11l1l1lll_opy_ if item not in bstack111l1l111_opy_]
    import platform as pf
    if pf.system().lower() == bstack1lll11l_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩ౫"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111l1l111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll1l1ll1l_opy_)))
                    for bstack1ll1l1ll1l_opy_ in bstack111l1l111_opy_]
    bstack1ll1l1l11_opy_ = []
    for spec in bstack111l1l111_opy_:
      bstack11111ll1_opy_ = []
      bstack11111ll1_opy_ += bstack1111111l1_opy_
      bstack11111ll1_opy_.append(spec)
      bstack1ll1l1l11_opy_.append(bstack11111ll1_opy_)
    execution_items = []
    for bstack11111ll1_opy_ in bstack1ll1l1l11_opy_:
      for index, _ in enumerate(CONFIG[bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౬")]):
        item = {}
        item[bstack1lll11l_opy_ (u"ࠪࡥࡷ࡭ࠧ౭")] = bstack1lll11l_opy_ (u"ࠫࠥ࠭౮").join(bstack11111ll1_opy_)
        item[bstack1lll11l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ౯")] = index
        execution_items.append(item)
    bstack1l111llll_opy_ = bstack1l1l1llll_opy_(execution_items, bstack1ll1111l11_opy_)
    for execution_item in bstack1l111llll_opy_:
      bstack1l1l111l_opy_ = []
      for item in execution_item:
        bstack1l1l111l_opy_.append(bstack1lll1l1ll1_opy_(name=str(item[bstack1lll11l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ౰")]),
                                             target=bstack11111111_opy_,
                                             args=(item[bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࠫ౱")],)))
      for t in bstack1l1l111l_opy_:
        t.start()
      for t in bstack1l1l111l_opy_:
        t.join()
  else:
    bstack11l1llll_opy_(bstack1llll1l11_opy_)
  if not bstack11ll1111_opy_:
    bstack1lll1l1ll_opy_()
def browserstack_initialize(bstack1ll111l1l1_opy_=None):
  run_on_browserstack(bstack1ll111l1l1_opy_, None, True)
def bstack1lll1l1ll_opy_():
  global CONFIG
  global bstack1ll11111_opy_
  global bstack111l111l1_opy_
  bstack1l11ll1ll_opy_.stop()
  bstack1l11ll1ll_opy_.bstack1l1ll1l1ll_opy_()
  if bstack111ll11l1_opy_.bstack11111l11_opy_(CONFIG):
    bstack111ll11l1_opy_.bstack1l1llll1ll_opy_()
  [bstack1l1ll11ll1_opy_, bstack11l11llll_opy_] = bstack1l11l1lll_opy_()
  if bstack1l1ll11ll1_opy_ is not None and bstack1ll1l111_opy_() != -1:
    sessions = bstack1ll1l1l1ll_opy_(bstack1l1ll11ll1_opy_)
    bstack1111l1ll1_opy_(sessions, bstack11l11llll_opy_)
  if bstack1ll11111_opy_ == bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ౲") and bstack111l111l1_opy_ != 0:
    sys.exit(bstack111l111l1_opy_)
def bstack1l11l1ll_opy_(bstack11l1l1l11_opy_):
  if bstack11l1l1l11_opy_:
    return bstack11l1l1l11_opy_.capitalize()
  else:
    return bstack1lll11l_opy_ (u"ࠩࠪ౳")
def bstack1l1l111ll_opy_(bstack1lll11l11l_opy_):
  if bstack1lll11l_opy_ (u"ࠪࡲࡦࡳࡥࠨ౴") in bstack1lll11l11l_opy_ and bstack1lll11l11l_opy_[bstack1lll11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ౵")] != bstack1lll11l_opy_ (u"ࠬ࠭౶"):
    return bstack1lll11l11l_opy_[bstack1lll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ౷")]
  else:
    bstack1ll11l1l1_opy_ = bstack1lll11l_opy_ (u"ࠢࠣ౸")
    if bstack1lll11l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ౹") in bstack1lll11l11l_opy_ and bstack1lll11l11l_opy_[bstack1lll11l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ౺")] != None:
      bstack1ll11l1l1_opy_ += bstack1lll11l11l_opy_[bstack1lll11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ౻")] + bstack1lll11l_opy_ (u"ࠦ࠱ࠦࠢ౼")
      if bstack1lll11l11l_opy_[bstack1lll11l_opy_ (u"ࠬࡵࡳࠨ౽")] == bstack1lll11l_opy_ (u"ࠨࡩࡰࡵࠥ౾"):
        bstack1ll11l1l1_opy_ += bstack1lll11l_opy_ (u"ࠢࡪࡑࡖࠤࠧ౿")
      bstack1ll11l1l1_opy_ += (bstack1lll11l11l_opy_[bstack1lll11l_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬಀ")] or bstack1lll11l_opy_ (u"ࠩࠪಁ"))
      return bstack1ll11l1l1_opy_
    else:
      bstack1ll11l1l1_opy_ += bstack1l11l1ll_opy_(bstack1lll11l11l_opy_[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫಂ")]) + bstack1lll11l_opy_ (u"ࠦࠥࠨಃ") + (
              bstack1lll11l11l_opy_[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ಄")] or bstack1lll11l_opy_ (u"࠭ࠧಅ")) + bstack1lll11l_opy_ (u"ࠢ࠭ࠢࠥಆ")
      if bstack1lll11l11l_opy_[bstack1lll11l_opy_ (u"ࠨࡱࡶࠫಇ")] == bstack1lll11l_opy_ (u"ࠤ࡚࡭ࡳࡪ࡯ࡸࡵࠥಈ"):
        bstack1ll11l1l1_opy_ += bstack1lll11l_opy_ (u"࡛ࠥ࡮ࡴࠠࠣಉ")
      bstack1ll11l1l1_opy_ += bstack1lll11l11l_opy_[bstack1lll11l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨಊ")] or bstack1lll11l_opy_ (u"ࠬ࠭ಋ")
      return bstack1ll11l1l1_opy_
def bstack1l11lll11_opy_(bstack1lll11l1ll_opy_):
  if bstack1lll11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠨࡤࡰࡰࡨࠦಌ"):
    return bstack1lll11l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ಍")
  elif bstack1lll11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣಎ"):
    return bstack1lll11l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡇࡣ࡬ࡰࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಏ")
  elif bstack1lll11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥಐ"):
    return bstack1lll11l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡐࡢࡵࡶࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ಑")
  elif bstack1lll11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦಒ"):
    return bstack1lll11l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡊࡸࡲࡰࡴ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨಓ")
  elif bstack1lll11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣಔ"):
    return bstack1lll11l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࠧࡪ࡫ࡡ࠴࠴࠹࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࠩࡥࡦࡣ࠶࠶࠻ࠨ࠾ࡕ࡫ࡰࡩࡴࡻࡴ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಕ")
  elif bstack1lll11l1ll_opy_ == bstack1lll11l_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠥಖ"):
    return bstack1lll11l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃࡘࡵ࡯ࡰ࡬ࡲ࡬ࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಗ")
  else:
    return bstack1lll11l_opy_ (u"ࠫࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࠨಘ") + bstack1l11l1ll_opy_(
      bstack1lll11l1ll_opy_) + bstack1lll11l_opy_ (u"ࠬࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಙ")
def bstack1lllllll1l_opy_(session):
  return bstack1lll11l_opy_ (u"࠭࠼ࡵࡴࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡶࡴࡽࠢ࠿࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠣࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠤࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧࢁࡽࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࢀࢃ࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࡽࢀࡿࢂࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽࠱ࡷࡶࡃ࠭ಚ").format(
    session[bstack1lll11l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫಛ")], bstack1l1l111ll_opy_(session), bstack1l11lll11_opy_(session[bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡶࡤࡸࡺࡹࠧಜ")]),
    bstack1l11lll11_opy_(session[bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩಝ")]),
    bstack1l11l1ll_opy_(session[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫಞ")] or session[bstack1lll11l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫಟ")] or bstack1lll11l_opy_ (u"ࠬ࠭ಠ")) + bstack1lll11l_opy_ (u"ࠨࠠࠣಡ") + (session[bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಢ")] or bstack1lll11l_opy_ (u"ࠨࠩಣ")),
    session[bstack1lll11l_opy_ (u"ࠩࡲࡷࠬತ")] + bstack1lll11l_opy_ (u"ࠥࠤࠧಥ") + session[bstack1lll11l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨದ")], session[bstack1lll11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧಧ")] or bstack1lll11l_opy_ (u"࠭ࠧನ"),
    session[bstack1lll11l_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫ಩")] if session[bstack1lll11l_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬಪ")] else bstack1lll11l_opy_ (u"ࠩࠪಫ"))
def bstack1111l1ll1_opy_(sessions, bstack11l11llll_opy_):
  try:
    bstack111ll1ll_opy_ = bstack1lll11l_opy_ (u"ࠥࠦಬ")
    if not os.path.exists(bstack11ll1l1l_opy_):
      os.mkdir(bstack11ll1l1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll11l_opy_ (u"ࠫࡦࡹࡳࡦࡶࡶ࠳ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩಭ")), bstack1lll11l_opy_ (u"ࠬࡸࠧಮ")) as f:
      bstack111ll1ll_opy_ = f.read()
    bstack111ll1ll_opy_ = bstack111ll1ll_opy_.replace(bstack1lll11l_opy_ (u"࠭ࡻࠦࡔࡈࡗ࡚ࡒࡔࡔࡡࡆࡓ࡚ࡔࡔࠦࡿࠪಯ"), str(len(sessions)))
    bstack111ll1ll_opy_ = bstack111ll1ll_opy_.replace(bstack1lll11l_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠪࢃࠧರ"), bstack11l11llll_opy_)
    bstack111ll1ll_opy_ = bstack111ll1ll_opy_.replace(bstack1lll11l_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠥࡾࠩಱ"),
                                              sessions[0].get(bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡤࡱࡪ࠭ಲ")) if sessions[0] else bstack1lll11l_opy_ (u"ࠪࠫಳ"))
    with open(os.path.join(bstack11ll1l1l_opy_, bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨ಴")), bstack1lll11l_opy_ (u"ࠬࡽࠧವ")) as stream:
      stream.write(bstack111ll1ll_opy_.split(bstack1lll11l_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪಶ"))[0])
      for session in sessions:
        stream.write(bstack1lllllll1l_opy_(session))
      stream.write(bstack111ll1ll_opy_.split(bstack1lll11l_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫಷ"))[1])
    logger.info(bstack1lll11l_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡦࡺ࡯࡬ࡥࠢࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠥࡧࡴࠡࡽࢀࠫಸ").format(bstack11ll1l1l_opy_));
  except Exception as e:
    logger.debug(bstack1llll1lll_opy_.format(str(e)))
def bstack1ll1l1l1ll_opy_(bstack1l1ll11ll1_opy_):
  global CONFIG
  try:
    host = bstack1lll11l_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬಹ") if bstack1lll11l_opy_ (u"ࠪࡥࡵࡶࠧ಺") in CONFIG else bstack1lll11l_opy_ (u"ࠫࡦࡶࡩࠨ಻")
    user = CONFIG[bstack1lll11l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫಼ࠧ")]
    key = CONFIG[bstack1lll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩಽ")]
    bstack1l1ll111_opy_ = bstack1lll11l_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ಾ") if bstack1lll11l_opy_ (u"ࠨࡣࡳࡴࠬಿ") in CONFIG else bstack1lll11l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫೀ")
    url = bstack1lll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨು").format(user, key, host, bstack1l1ll111_opy_,
                                                                                bstack1l1ll11ll1_opy_)
    headers = {
      bstack1lll11l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪೂ"): bstack1lll11l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨೃ"),
    }
    proxies = bstack1111l1l11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1lll11l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫೄ")], response.json()))
  except Exception as e:
    logger.debug(bstack111lll11l_opy_.format(str(e)))
def bstack1l11l1lll_opy_():
  global CONFIG
  global bstack1llll1llll_opy_
  try:
    if bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೅") in CONFIG:
      host = bstack1lll11l_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫೆ") if bstack1lll11l_opy_ (u"ࠩࡤࡴࡵ࠭ೇ") in CONFIG else bstack1lll11l_opy_ (u"ࠪࡥࡵ࡯ࠧೈ")
      user = CONFIG[bstack1lll11l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭೉")]
      key = CONFIG[bstack1lll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨೊ")]
      bstack1l1ll111_opy_ = bstack1lll11l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬೋ") if bstack1lll11l_opy_ (u"ࠧࡢࡲࡳࠫೌ") in CONFIG else bstack1lll11l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧ್ࠪ")
      url = bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩ೎").format(user, key, host, bstack1l1ll111_opy_)
      headers = {
        bstack1lll11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ೏"): bstack1lll11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ೐"),
      }
      if bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೑") in CONFIG:
        params = {bstack1lll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೒"): CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೓")], bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೔"): CONFIG[bstack1lll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫೕ")]}
      else:
        params = {bstack1lll11l_opy_ (u"ࠪࡲࡦࡳࡥࠨೖ"): CONFIG[bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೗")]}
      proxies = bstack1111l1l11_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1l1ll111ll_opy_ = response.json()[0][bstack1lll11l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ೘")]
        if bstack1l1ll111ll_opy_:
          bstack11l11llll_opy_ = bstack1l1ll111ll_opy_[bstack1lll11l_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ೙")].split(bstack1lll11l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭೚"))[0] + bstack1lll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩ೛") + bstack1l1ll111ll_opy_[
            bstack1lll11l_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ೜")]
          logger.info(bstack11llll1l1_opy_.format(bstack11l11llll_opy_))
          bstack1llll1llll_opy_ = bstack1l1ll111ll_opy_[bstack1lll11l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ೝ")]
          bstack1111l11l_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧೞ")]
          if bstack1lll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೟") in CONFIG:
            bstack1111l11l_opy_ += bstack1lll11l_opy_ (u"࠭ࠠࠨೠ") + CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩೡ")]
          if bstack1111l11l_opy_ != bstack1l1ll111ll_opy_[bstack1lll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ೢ")]:
            logger.debug(bstack1ll11l1lll_opy_.format(bstack1l1ll111ll_opy_[bstack1lll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧೣ")], bstack1111l11l_opy_))
          return [bstack1l1ll111ll_opy_[bstack1lll11l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭೤")], bstack11l11llll_opy_]
    else:
      logger.warn(bstack11lll11l1_opy_)
  except Exception as e:
    logger.debug(bstack11lllll1_opy_.format(str(e)))
  return [None, None]
def bstack11llll11_opy_(url, bstack1l1llll11_opy_=False):
  global CONFIG
  global bstack111ll11ll_opy_
  if not bstack111ll11ll_opy_:
    hostname = bstack1l1llll1l1_opy_(url)
    is_private = bstack1lllll11l1_opy_(hostname)
    if (bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ೥") in CONFIG and not bstack1l1l1ll11_opy_(CONFIG[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ೦")])) and (is_private or bstack1l1llll11_opy_):
      bstack111ll11ll_opy_ = hostname
def bstack1l1llll1l1_opy_(url):
  return urlparse(url).hostname
def bstack1lllll11l1_opy_(hostname):
  for bstack11ll11l1l_opy_ in bstack11ll11l1_opy_:
    regex = re.compile(bstack11ll11l1l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11l11ll1l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1ll1l1l111_opy_
  if not bstack111ll11l1_opy_.bstack1lll1l11ll_opy_(CONFIG, bstack1ll1l1l111_opy_):
    logger.warning(bstack1lll11l_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ೧"))
    return {}
  try:
    results = driver.execute_script(bstack1lll11l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡳ࡫ࡷࠡࡒࡵࡳࡲ࡯ࡳࡦࠪࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡧࡹࡩࡳࡺࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡘࡆࡖ࡟ࡈࡇࡗࡣࡗࡋࡓࡖࡎࡗࡗࠬ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡩࡲࠥࡃࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫࡩࡻ࡫࡮ࡵࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡷ࡫࡭ࡰࡸࡨࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡳࡰ࡮ࡹࡩ࠭࡫ࡶࡦࡰࡷ࠲ࡩ࡫ࡴࡢ࡫࡯࠲ࡩࡧࡴࡢࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡦࡪࡤࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡓࡇࡖࡔࡔࡔࡓࡆࠩ࠯ࠤ࡫ࡴࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪࡼࡥ࡯ࡶࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨ࡮ࡪࡩࡴࠩࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࢃࠩ࠼ࠌࠣࠤࠥࠦࠢࠣࠤ೨"))
    return results
  except Exception:
    logger.error(bstack1lll11l_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥ೩"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1ll1l1l111_opy_
  if not bstack111ll11l1_opy_.bstack1lll1l11ll_opy_(CONFIG, bstack1ll1l1l111_opy_):
    logger.warning(bstack1lll11l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨ೪"))
    return {}
  try:
    bstack1ll1l1ll_opy_ = driver.execute_script(bstack1lll11l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡁࠥࡴࡥࡸࠢࡆࡹࡸࡺ࡯࡮ࡇࡹࡩࡳࡺࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡋࡊ࡚࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࠩࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡦ࡯ࠢࡀࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨࡦࡸࡨࡲࡹ࠯ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡴࡨࡱࡴࡼࡥࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡔࡗࡐࡑࡆࡘ࡙ࡠࡔࡈࡗࡕࡕࡎࡔࡇࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡸࡵ࡬ࡷࡧࠫࡩࡻ࡫࡮ࡵ࠰ࡧࡩࡹࡧࡩ࡭࠰ࡶࡹࡲࡳࡡࡳࡻࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡤࡪࡵࡳࡥࡹࡩࡨࡆࡸࡨࡲࡹ࠮ࡥࡷࡧࡱࡸ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠠࡤࡣࡷࡧ࡭ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡰࡥࡤࡶࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠫ࠾ࠎࠥࠦࠠࠡࠤࠥࠦ೫"))
    return bstack1ll1l1ll_opy_
  except Exception:
    logger.error(bstack1lll11l_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡷࡰࡱࡦࡸࡹࠡࡹࡤࡷࠥ࡬࡯ࡶࡰࡧ࠲ࠧ೬"))
    return {}