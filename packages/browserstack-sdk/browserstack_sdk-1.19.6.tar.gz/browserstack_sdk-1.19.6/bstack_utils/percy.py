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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1lll1l1l1l_opy_, bstack1l1llllll1_opy_
class bstack11l111l1l_opy_:
  working_dir = os.getcwd()
  bstack1ll1ll1ll1_opy_ = False
  config = {}
  binary_path = bstack1lll11l_opy_ (u"࠭ࠧጪ")
  bstack111l1l1l11_opy_ = bstack1lll11l_opy_ (u"ࠧࠨጫ")
  bstack11lll11ll_opy_ = False
  bstack111ll1ll11_opy_ = None
  bstack111lllllll_opy_ = {}
  bstack111ll1l11l_opy_ = 300
  bstack111llllll1_opy_ = False
  logger = None
  bstack111ll1l1ll_opy_ = False
  bstack111lll11ll_opy_ = bstack1lll11l_opy_ (u"ࠨࠩጬ")
  bstack11l1111l11_opy_ = {
    bstack1lll11l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩጭ") : 1,
    bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫጮ") : 2,
    bstack1lll11l_opy_ (u"ࠫࡪࡪࡧࡦࠩጯ") : 3,
    bstack1lll11l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬጰ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11l11111ll_opy_(self):
    bstack111lll1lll_opy_ = bstack1lll11l_opy_ (u"࠭ࠧጱ")
    bstack111lll1l11_opy_ = sys.platform
    bstack111ll1l111_opy_ = bstack1lll11l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ጲ")
    if re.match(bstack1lll11l_opy_ (u"ࠣࡦࡤࡶࡼ࡯࡮ࡽ࡯ࡤࡧࠥࡵࡳࠣጳ"), bstack111lll1l11_opy_) != None:
      bstack111lll1lll_opy_ = bstack11ll11lll1_opy_ + bstack1lll11l_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡲࡷࡽ࠴ࡺࡪࡲࠥጴ")
      self.bstack111lll11ll_opy_ = bstack1lll11l_opy_ (u"ࠪࡱࡦࡩࠧጵ")
    elif re.match(bstack1lll11l_opy_ (u"ࠦࡲࡹࡷࡪࡰࡿࡱࡸࡿࡳࡽ࡯࡬ࡲ࡬ࡽࡼࡤࡻࡪࡻ࡮ࡴࡼࡣࡥࡦࡻ࡮ࡴࡼࡸ࡫ࡱࡧࡪࢂࡥ࡮ࡥࡿࡻ࡮ࡴ࠳࠳ࠤጶ"), bstack111lll1l11_opy_) != None:
      bstack111lll1lll_opy_ = bstack11ll11lll1_opy_ + bstack1lll11l_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡽࡩ࡯࠰ࡽ࡭ࡵࠨጷ")
      bstack111ll1l111_opy_ = bstack1lll11l_opy_ (u"ࠨࡰࡦࡴࡦࡽ࠳࡫ࡸࡦࠤጸ")
      self.bstack111lll11ll_opy_ = bstack1lll11l_opy_ (u"ࠧࡸ࡫ࡱࠫጹ")
    else:
      bstack111lll1lll_opy_ = bstack11ll11lll1_opy_ + bstack1lll11l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮࡮࡬ࡲࡺࡾ࠮ࡻ࡫ࡳࠦጺ")
      self.bstack111lll11ll_opy_ = bstack1lll11l_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨጻ")
    return bstack111lll1lll_opy_, bstack111ll1l111_opy_
  def bstack111llll1l1_opy_(self):
    try:
      bstack111l1l111l_opy_ = [os.path.join(expanduser(bstack1lll11l_opy_ (u"ࠥࢂࠧጼ")), bstack1lll11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫጽ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111l1l111l_opy_:
        if(self.bstack111llll11l_opy_(path)):
          return path
      raise bstack1lll11l_opy_ (u"࡛ࠧ࡮ࡢ࡮ࡥࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤጾ")
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠱ࠥࢁࡽࠣጿ").format(e))
  def bstack111llll11l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111ll11l11_opy_(self, bstack111lll1lll_opy_, bstack111ll1l111_opy_):
    try:
      bstack111ll11l1l_opy_ = self.bstack111llll1l1_opy_()
      bstack111l1l1lll_opy_ = os.path.join(bstack111ll11l1l_opy_, bstack1lll11l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪፀ"))
      bstack111lllll1l_opy_ = os.path.join(bstack111ll11l1l_opy_, bstack111ll1l111_opy_)
      if os.path.exists(bstack111lllll1l_opy_):
        self.logger.info(bstack1lll11l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥፁ").format(bstack111lllll1l_opy_))
        return bstack111lllll1l_opy_
      if os.path.exists(bstack111l1l1lll_opy_):
        self.logger.info(bstack1lll11l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢፂ").format(bstack111l1l1lll_opy_))
        return self.bstack111l1ll111_opy_(bstack111l1l1lll_opy_, bstack111ll1l111_opy_)
      self.logger.info(bstack1lll11l_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣፃ").format(bstack111lll1lll_opy_))
      response = bstack1l1llllll1_opy_(bstack1lll11l_opy_ (u"ࠫࡌࡋࡔࠨፄ"), bstack111lll1lll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack111l1l1lll_opy_, bstack1lll11l_opy_ (u"ࠬࡽࡢࠨፅ")) as file:
          file.write(response.content)
        self.logger.info(bstack111l1l11l1_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࡥ࡭ࡳࡧࡲࡺࡡࡽ࡭ࡵࡥࡰࡢࡶ࡫ࢁࠧፆ"))
        return self.bstack111l1ll111_opy_(bstack111l1l1lll_opy_, bstack111ll1l111_opy_)
      else:
        raise(bstack111l1l11l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࡷࡹࡧࡴࡶࡵࡢࡧࡴࡪࡥࡾࠤፇ"))
    except:
      self.logger.error(bstack1lll11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧፈ"))
  def bstack11l111111l_opy_(self, bstack111lll1lll_opy_, bstack111ll1l111_opy_):
    try:
      bstack111lllll1l_opy_ = self.bstack111ll11l11_opy_(bstack111lll1lll_opy_, bstack111ll1l111_opy_)
      bstack111llll111_opy_ = self.bstack111l1l11ll_opy_(bstack111lll1lll_opy_, bstack111ll1l111_opy_, bstack111lllll1l_opy_)
      return bstack111lllll1l_opy_, bstack111llll111_opy_
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨፉ").format(e))
    return bstack111lllll1l_opy_, False
  def bstack111l1l11ll_opy_(self, bstack111lll1lll_opy_, bstack111ll1l111_opy_, bstack111lllll1l_opy_, bstack111ll1111l_opy_ = 0):
    if bstack111ll1111l_opy_ > 1:
      return False
    if bstack111lllll1l_opy_ == None or os.path.exists(bstack111lllll1l_opy_) == False:
      self.logger.warn(bstack1lll11l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣፊ"))
      bstack111lllll1l_opy_ = self.bstack111ll11l11_opy_(bstack111lll1lll_opy_, bstack111ll1l111_opy_)
      self.bstack111l1l11ll_opy_(bstack111lll1lll_opy_, bstack111ll1l111_opy_, bstack111lllll1l_opy_, bstack111ll1111l_opy_+1)
    bstack111lll1l1l_opy_ = bstack1lll11l_opy_ (u"ࠦࡣ࠴ࠪࡁࡲࡨࡶࡨࡿ࡜࠰ࡥ࡯࡭ࠥࡢࡤ࠯࡞ࡧ࠯࠳ࡢࡤࠬࠤፋ")
    command = bstack1lll11l_opy_ (u"ࠬࢁࡽࠡ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫፌ").format(bstack111lllll1l_opy_)
    bstack111ll111ll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111lll1l1l_opy_, bstack111ll111ll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1lll11l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨࠧፍ"))
      bstack111lllll1l_opy_ = self.bstack111ll11l11_opy_(bstack111lll1lll_opy_, bstack111ll1l111_opy_)
      self.bstack111l1l11ll_opy_(bstack111lll1lll_opy_, bstack111ll1l111_opy_, bstack111lllll1l_opy_, bstack111ll1111l_opy_+1)
  def bstack111l1ll111_opy_(self, bstack111l1l1lll_opy_, bstack111ll1l111_opy_):
    try:
      working_dir = os.path.dirname(bstack111l1l1lll_opy_)
      shutil.unpack_archive(bstack111l1l1lll_opy_, working_dir)
      bstack111lllll1l_opy_ = os.path.join(working_dir, bstack111ll1l111_opy_)
      os.chmod(bstack111lllll1l_opy_, 0o755)
      return bstack111lllll1l_opy_
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣፎ"))
  def bstack111l1l1ll1_opy_(self):
    try:
      percy = str(self.config.get(bstack1lll11l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧፏ"), bstack1lll11l_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣፐ"))).lower()
      if percy != bstack1lll11l_opy_ (u"ࠥࡸࡷࡻࡥࠣፑ"):
        return False
      self.bstack11lll11ll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨፒ").format(e))
  def bstack111l1l1111_opy_(self):
    try:
      bstack111l1l1111_opy_ = str(self.config.get(bstack1lll11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨፓ"), bstack1lll11l_opy_ (u"ࠨࡡࡶࡶࡲࠦፔ"))).lower()
      return bstack111l1l1111_opy_
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺࠢࡦࡥࡵࡺࡵࡳࡧࠣࡱࡴࡪࡥ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣፕ").format(e))
  def init(self, bstack1ll1ll1ll1_opy_, config, logger):
    self.bstack1ll1ll1ll1_opy_ = bstack1ll1ll1ll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111l1l1ll1_opy_():
      return
    self.bstack111lllllll_opy_ = config.get(bstack1lll11l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧፖ"), {})
    self.bstack111ll111l1_opy_ = config.get(bstack1lll11l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬፗ"), bstack1lll11l_opy_ (u"ࠥࡥࡺࡺ࡯ࠣፘ"))
    try:
      bstack111lll1lll_opy_, bstack111ll1l111_opy_ = self.bstack11l11111ll_opy_()
      bstack111lllll1l_opy_, bstack111llll111_opy_ = self.bstack11l111111l_opy_(bstack111lll1lll_opy_, bstack111ll1l111_opy_)
      if bstack111llll111_opy_:
        self.binary_path = bstack111lllll1l_opy_
        thread = Thread(target=self.bstack111ll11111_opy_)
        thread.start()
      else:
        self.bstack111ll1l1ll_opy_ = True
        self.logger.error(bstack1lll11l_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡩࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡓࡩࡷࡩࡹࠣፙ").format(bstack111lllll1l_opy_))
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨፚ").format(e))
  def bstack11l11111l1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1lll11l_opy_ (u"࠭࡬ࡰࡩࠪ፛"), bstack1lll11l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴࡬ࡰࡩࠪ፜"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1lll11l_opy_ (u"ࠣࡒࡸࡷ࡭࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࡸࠦࡡࡵࠢࡾࢁࠧ፝").format(logfile))
      self.bstack111l1l1l11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࠥࡶࡡࡵࡪ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ፞").format(e))
  def bstack111ll11111_opy_(self):
    bstack111ll1llll_opy_ = self.bstack111ll1l1l1_opy_()
    if bstack111ll1llll_opy_ == None:
      self.bstack111ll1l1ll_opy_ = True
      self.logger.error(bstack1lll11l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮ࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠨ፟"))
      return False
    command_args = [bstack1lll11l_opy_ (u"ࠦࡦࡶࡰ࠻ࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠧ፠") if self.bstack1ll1ll1ll1_opy_ else bstack1lll11l_opy_ (u"ࠬ࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠩ፡")]
    bstack111l1ll11l_opy_ = self.bstack111l1ll1ll_opy_()
    if bstack111l1ll11l_opy_ != None:
      command_args.append(bstack1lll11l_opy_ (u"ࠨ࠭ࡤࠢࡾࢁࠧ።").format(bstack111l1ll11l_opy_))
    env = os.environ.copy()
    env[bstack1lll11l_opy_ (u"ࠢࡑࡇࡕࡇ࡞ࡥࡔࡐࡍࡈࡒࠧ፣")] = bstack111ll1llll_opy_
    bstack111l1ll1l1_opy_ = [self.binary_path]
    self.bstack11l11111l1_opy_()
    self.bstack111ll1ll11_opy_ = self.bstack111l1lll1l_opy_(bstack111l1ll1l1_opy_ + command_args, env)
    self.logger.debug(bstack1lll11l_opy_ (u"ࠣࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠤ፤"))
    bstack111ll1111l_opy_ = 0
    while self.bstack111ll1ll11_opy_.poll() == None:
      bstack111l1llll1_opy_ = self.bstack111l1l1l1l_opy_()
      if bstack111l1llll1_opy_:
        self.logger.debug(bstack1lll11l_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠧ፥"))
        self.bstack111llllll1_opy_ = True
        return True
      bstack111ll1111l_opy_ += 1
      self.logger.debug(bstack1lll11l_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡕࡩࡹࡸࡹࠡ࠯ࠣࡿࢂࠨ፦").format(bstack111ll1111l_opy_))
      time.sleep(2)
    self.logger.error(bstack1lll11l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡌࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࢀࢃࠠࡢࡶࡷࡩࡲࡶࡴࡴࠤ፧").format(bstack111ll1111l_opy_))
    self.bstack111ll1l1ll_opy_ = True
    return False
  def bstack111l1l1l1l_opy_(self, bstack111ll1111l_opy_ = 0):
    try:
      if bstack111ll1111l_opy_ > 10:
        return False
      bstack111ll1lll1_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡘࡋࡒࡗࡇࡕࡣࡆࡊࡄࡓࡇࡖࡗࠬ፨"), bstack1lll11l_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵ࠼࠸࠷࠸࠾ࠧ፩"))
      bstack111lllll11_opy_ = bstack111ll1lll1_opy_ + bstack11ll1l1l11_opy_
      response = requests.get(bstack111lllll11_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack111ll1l1l1_opy_(self):
    bstack111l1lllll_opy_ = bstack1lll11l_opy_ (u"ࠧࡢࡲࡳࠫ፪") if self.bstack1ll1ll1ll1_opy_ else bstack1lll11l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ፫")
    bstack11l1l1ll11_opy_ = bstack1lll11l_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠣ፬").format(self.config[bstack1lll11l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ፭")], bstack111l1lllll_opy_)
    uri = bstack1lll1l1l1l_opy_(bstack11l1l1ll11_opy_)
    try:
      response = bstack1l1llllll1_opy_(bstack1lll11l_opy_ (u"ࠫࡌࡋࡔࠨ፮"), uri, {}, {bstack1lll11l_opy_ (u"ࠬࡧࡵࡵࡪࠪ፯"): (self.config[bstack1lll11l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ፰")], self.config[bstack1lll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ፱")])})
      if response.status_code == 200:
        bstack111ll11lll_opy_ = response.json()
        if bstack1lll11l_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢ፲") in bstack111ll11lll_opy_:
          return bstack111ll11lll_opy_[bstack1lll11l_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣ፳")]
        else:
          raise bstack1lll11l_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪ፴").format(bstack111ll11lll_opy_)
      else:
        raise bstack1lll11l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦ፵").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨ፶").format(e))
  def bstack111l1ll1ll_opy_(self):
    bstack111lll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll11l_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤ፷"))
    try:
      if bstack1lll11l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ፸") not in self.bstack111lllllll_opy_:
        self.bstack111lllllll_opy_[bstack1lll11l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ፹")] = 2
      with open(bstack111lll1ll1_opy_, bstack1lll11l_opy_ (u"ࠩࡺࠫ፺")) as fp:
        json.dump(self.bstack111lllllll_opy_, fp)
      return bstack111lll1ll1_opy_
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ፻").format(e))
  def bstack111l1lll1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111lll11ll_opy_ == bstack1lll11l_opy_ (u"ࠫࡼ࡯࡮ࠨ፼"):
        bstack111lll1111_opy_ = [bstack1lll11l_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭፽"), bstack1lll11l_opy_ (u"࠭࠯ࡤࠩ፾")]
        cmd = bstack111lll1111_opy_ + cmd
      cmd = bstack1lll11l_opy_ (u"ࠧࠡࠩ፿").join(cmd)
      self.logger.debug(bstack1lll11l_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧᎀ").format(cmd))
      with open(self.bstack111l1l1l11_opy_, bstack1lll11l_opy_ (u"ࠤࡤࠦᎁ")) as bstack111lll111l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111lll111l_opy_, text=True, stderr=bstack111lll111l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111ll1l1ll_opy_ = True
      self.logger.error(bstack1lll11l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᎂ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111llllll1_opy_:
        self.logger.info(bstack1lll11l_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧᎃ"))
        cmd = [self.binary_path, bstack1lll11l_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣᎄ")]
        self.bstack111l1lll1l_opy_(cmd)
        self.bstack111llllll1_opy_ = False
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᎅ").format(cmd, e))
  def bstack11l1l11ll_opy_(self):
    if not self.bstack11lll11ll_opy_:
      return
    try:
      bstack111ll1ll1l_opy_ = 0
      while not self.bstack111llllll1_opy_ and bstack111ll1ll1l_opy_ < self.bstack111ll1l11l_opy_:
        if self.bstack111ll1l1ll_opy_:
          self.logger.info(bstack1lll11l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧᎆ"))
          return
        time.sleep(1)
        bstack111ll1ll1l_opy_ += 1
      os.environ[bstack1lll11l_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧᎇ")] = str(self.bstack111l1lll11_opy_())
      self.logger.info(bstack1lll11l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥᎈ"))
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᎉ").format(e))
  def bstack111l1lll11_opy_(self):
    if self.bstack1ll1ll1ll1_opy_:
      return
    try:
      bstack11l1111111_opy_ = [platform[bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᎊ")].lower() for platform in self.config.get(bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᎋ"), [])]
      bstack111ll11ll1_opy_ = sys.maxsize
      bstack111llll1ll_opy_ = bstack1lll11l_opy_ (u"࠭ࠧᎌ")
      for browser in bstack11l1111111_opy_:
        if browser in self.bstack11l1111l11_opy_:
          bstack111lll11l1_opy_ = self.bstack11l1111l11_opy_[browser]
        if bstack111lll11l1_opy_ < bstack111ll11ll1_opy_:
          bstack111ll11ll1_opy_ = bstack111lll11l1_opy_
          bstack111llll1ll_opy_ = browser
      return bstack111llll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1lll11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᎍ").format(e))