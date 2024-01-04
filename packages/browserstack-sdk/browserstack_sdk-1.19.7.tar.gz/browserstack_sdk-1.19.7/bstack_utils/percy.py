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
from bstack_utils.helper import bstack1l1l1l1l1_opy_, bstack1ll111lll1_opy_
class bstack1llllllll_opy_:
  working_dir = os.getcwd()
  bstack1l1111l1l_opy_ = False
  config = {}
  binary_path = bstack111ll11_opy_ (u"ࠧࠨጫ")
  bstack111ll11ll1_opy_ = bstack111ll11_opy_ (u"ࠨࠩጬ")
  bstack111l11l1_opy_ = False
  bstack111llll111_opy_ = None
  bstack111l1ll111_opy_ = {}
  bstack111lllll11_opy_ = 300
  bstack111llll11l_opy_ = False
  logger = None
  bstack111l1l1ll1_opy_ = False
  bstack111lll111l_opy_ = bstack111ll11_opy_ (u"ࠩࠪጭ")
  bstack111l1lllll_opy_ = {
    bstack111ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪጮ") : 1,
    bstack111ll11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬጯ") : 2,
    bstack111ll11_opy_ (u"ࠬ࡫ࡤࡨࡧࠪጰ") : 3,
    bstack111ll11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ጱ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111l1l1l11_opy_(self):
    bstack111l1ll1l1_opy_ = bstack111ll11_opy_ (u"ࠧࠨጲ")
    bstack111lll1l11_opy_ = sys.platform
    bstack111l1l11ll_opy_ = bstack111ll11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧጳ")
    if re.match(bstack111ll11_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤጴ"), bstack111lll1l11_opy_) != None:
      bstack111l1ll1l1_opy_ = bstack11ll11llll_opy_ + bstack111ll11_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦጵ")
      self.bstack111lll111l_opy_ = bstack111ll11_opy_ (u"ࠫࡲࡧࡣࠨጶ")
    elif re.match(bstack111ll11_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥጷ"), bstack111lll1l11_opy_) != None:
      bstack111l1ll1l1_opy_ = bstack11ll11llll_opy_ + bstack111ll11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢጸ")
      bstack111l1l11ll_opy_ = bstack111ll11_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥጹ")
      self.bstack111lll111l_opy_ = bstack111ll11_opy_ (u"ࠨࡹ࡬ࡲࠬጺ")
    else:
      bstack111l1ll1l1_opy_ = bstack11ll11llll_opy_ + bstack111ll11_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧጻ")
      self.bstack111lll111l_opy_ = bstack111ll11_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩጼ")
    return bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_
  def bstack111l1lll1l_opy_(self):
    try:
      bstack111l1l11l1_opy_ = [os.path.join(expanduser(bstack111ll11_opy_ (u"ࠦࢃࠨጽ")), bstack111ll11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬጾ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111l1l11l1_opy_:
        if(self.bstack111ll11l1l_opy_(path)):
          return path
      raise bstack111ll11_opy_ (u"ࠨࡕ࡯ࡣ࡯ࡦࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥጿ")
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤፀ").format(e))
  def bstack111ll11l1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111l1ll1ll_opy_(self, bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_):
    try:
      bstack111llllll1_opy_ = self.bstack111l1lll1l_opy_()
      bstack111ll11111_opy_ = os.path.join(bstack111llllll1_opy_, bstack111ll11_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫፁ"))
      bstack111lll11l1_opy_ = os.path.join(bstack111llllll1_opy_, bstack111l1l11ll_opy_)
      if os.path.exists(bstack111lll11l1_opy_):
        self.logger.info(bstack111ll11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦፂ").format(bstack111lll11l1_opy_))
        return bstack111lll11l1_opy_
      if os.path.exists(bstack111ll11111_opy_):
        self.logger.info(bstack111ll11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣፃ").format(bstack111ll11111_opy_))
        return self.bstack11l111111l_opy_(bstack111ll11111_opy_, bstack111l1l11ll_opy_)
      self.logger.info(bstack111ll11_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤፄ").format(bstack111l1ll1l1_opy_))
      response = bstack1ll111lll1_opy_(bstack111ll11_opy_ (u"ࠬࡍࡅࡕࠩፅ"), bstack111l1ll1l1_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack111ll11111_opy_, bstack111ll11_opy_ (u"࠭ࡷࡣࠩፆ")) as file:
          file.write(response.content)
        self.logger.info(bstack111ll1l1ll_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡥࡳࡪࠠࡴࡣࡹࡩࡩࠦࡡࡵࠢࡾࡦ࡮ࡴࡡࡳࡻࡢࡾ࡮ࡶ࡟ࡱࡣࡷ࡬ࢂࠨፇ"))
        return self.bstack11l111111l_opy_(bstack111ll11111_opy_, bstack111l1l11ll_opy_)
      else:
        raise(bstack111ll1l1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠢࡖࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠺ࠡࡽࡵࡩࡸࡶ࡯࡯ࡵࡨ࠲ࡸࡺࡡࡵࡷࡶࡣࡨࡵࡤࡦࡿࠥፈ"))
    except:
      self.logger.error(bstack111ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨፉ"))
  def bstack111ll111ll_opy_(self, bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_):
    try:
      bstack111lll11l1_opy_ = self.bstack111l1ll1ll_opy_(bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_)
      bstack111l1ll11l_opy_ = self.bstack111ll111l1_opy_(bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_, bstack111lll11l1_opy_)
      return bstack111lll11l1_opy_, bstack111l1ll11l_opy_
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡳࡥࡹ࡮ࠢፊ").format(e))
    return bstack111lll11l1_opy_, False
  def bstack111ll111l1_opy_(self, bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_, bstack111lll11l1_opy_, bstack111lll1ll1_opy_ = 0):
    if bstack111lll1ll1_opy_ > 1:
      return False
    if bstack111lll11l1_opy_ == None or os.path.exists(bstack111lll11l1_opy_) == False:
      self.logger.warn(bstack111ll11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡸࡥࡵࡴࡼ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤፋ"))
      bstack111lll11l1_opy_ = self.bstack111l1ll1ll_opy_(bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_)
      self.bstack111ll111l1_opy_(bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_, bstack111lll11l1_opy_, bstack111lll1ll1_opy_+1)
    bstack111lll1111_opy_ = bstack111ll11_opy_ (u"ࠧࡤ࠮ࠫࡂࡳࡩࡷࡩࡹ࡝࠱ࡦࡰ࡮ࠦ࡜ࡥ࠰࡟ࡨ࠰࠴࡜ࡥ࠭ࠥፌ")
    command = bstack111ll11_opy_ (u"࠭ࡻࡾࠢ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬፍ").format(bstack111lll11l1_opy_)
    bstack111lll1l1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111lll1111_opy_, bstack111lll1l1l_opy_) != None:
      return True
    else:
      self.logger.error(bstack111ll11_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡤࡪࡨࡧࡰࠦࡦࡢ࡫࡯ࡩࡩࠨፎ"))
      bstack111lll11l1_opy_ = self.bstack111l1ll1ll_opy_(bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_)
      self.bstack111ll111l1_opy_(bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_, bstack111lll11l1_opy_, bstack111lll1ll1_opy_+1)
  def bstack11l111111l_opy_(self, bstack111ll11111_opy_, bstack111l1l11ll_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll11111_opy_)
      shutil.unpack_archive(bstack111ll11111_opy_, working_dir)
      bstack111lll11l1_opy_ = os.path.join(working_dir, bstack111l1l11ll_opy_)
      os.chmod(bstack111lll11l1_opy_, 0o755)
      return bstack111lll11l1_opy_
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡺࡴࡺࡪࡲࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤፏ"))
  def bstack111ll1lll1_opy_(self):
    try:
      percy = str(self.config.get(bstack111ll11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨፐ"), bstack111ll11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤፑ"))).lower()
      if percy != bstack111ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤፒ"):
        return False
      self.bstack111l11l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢፓ").format(e))
  def bstack111lll1lll_opy_(self):
    try:
      bstack111lll1lll_opy_ = str(self.config.get(bstack111ll11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩፔ"), bstack111ll11_opy_ (u"ࠢࡢࡷࡷࡳࠧፕ"))).lower()
      return bstack111lll1lll_opy_
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤፖ").format(e))
  def init(self, bstack1l1111l1l_opy_, config, logger):
    self.bstack1l1111l1l_opy_ = bstack1l1111l1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111ll1lll1_opy_():
      return
    self.bstack111l1ll111_opy_ = config.get(bstack111ll11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨፗ"), {})
    self.bstack111ll1l11l_opy_ = config.get(bstack111ll11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ፘ"), bstack111ll11_opy_ (u"ࠦࡦࡻࡴࡰࠤፙ"))
    try:
      bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_ = self.bstack111l1l1l11_opy_()
      bstack111lll11l1_opy_, bstack111l1ll11l_opy_ = self.bstack111ll111ll_opy_(bstack111l1ll1l1_opy_, bstack111l1l11ll_opy_)
      if bstack111l1ll11l_opy_:
        self.binary_path = bstack111lll11l1_opy_
        thread = Thread(target=self.bstack111ll1111l_opy_)
        thread.start()
      else:
        self.bstack111l1l1ll1_opy_ = True
        self.logger.error(bstack111ll11_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤፚ").format(bstack111lll11l1_opy_))
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ፛").format(e))
  def bstack111l11llll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack111ll11_opy_ (u"ࠧ࡭ࡱࡪࠫ፜"), bstack111ll11_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫ፝"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack111ll11_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨ፞").format(logfile))
      self.bstack111ll11ll1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ፟").format(e))
  def bstack111ll1111l_opy_(self):
    bstack11l11111ll_opy_ = self.bstack111l1l111l_opy_()
    if bstack11l11111ll_opy_ == None:
      self.bstack111l1l1ll1_opy_ = True
      self.logger.error(bstack111ll11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢ፠"))
      return False
    command_args = [bstack111ll11_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨ፡") if self.bstack1l1111l1l_opy_ else bstack111ll11_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪ።")]
    bstack111ll1ll1l_opy_ = self.bstack111llll1ll_opy_()
    if bstack111ll1ll1l_opy_ != None:
      command_args.append(bstack111ll11_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨ፣").format(bstack111ll1ll1l_opy_))
    env = os.environ.copy()
    env[bstack111ll11_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨ፤")] = bstack11l11111ll_opy_
    bstack111ll1l111_opy_ = [self.binary_path]
    self.bstack111l11llll_opy_()
    self.bstack111llll111_opy_ = self.bstack111ll11l11_opy_(bstack111ll1l111_opy_ + command_args, env)
    self.logger.debug(bstack111ll11_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥ፥"))
    bstack111lll1ll1_opy_ = 0
    while self.bstack111llll111_opy_.poll() == None:
      bstack111l1l1l1l_opy_ = self.bstack111l1llll1_opy_()
      if bstack111l1l1l1l_opy_:
        self.logger.debug(bstack111ll11_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨ፦"))
        self.bstack111llll11l_opy_ = True
        return True
      bstack111lll1ll1_opy_ += 1
      self.logger.debug(bstack111ll11_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢ፧").format(bstack111lll1ll1_opy_))
      time.sleep(2)
    self.logger.error(bstack111ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥ፨").format(bstack111lll1ll1_opy_))
    self.bstack111l1l1ll1_opy_ = True
    return False
  def bstack111l1llll1_opy_(self, bstack111lll1ll1_opy_ = 0):
    try:
      if bstack111lll1ll1_opy_ > 10:
        return False
      bstack111l1lll11_opy_ = os.environ.get(bstack111ll11_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭፩"), bstack111ll11_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨ፪"))
      bstack111l1l1111_opy_ = bstack111l1lll11_opy_ + bstack11ll1l11ll_opy_
      response = requests.get(bstack111l1l1111_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack111l1l111l_opy_(self):
    bstack111ll1l1l1_opy_ = bstack111ll11_opy_ (u"ࠨࡣࡳࡴࠬ፫") if self.bstack1l1111l1l_opy_ else bstack111ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ፬")
    bstack11ll11l1ll_opy_ = bstack111ll11_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠤ፭").format(self.config[bstack111ll11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ፮")], bstack111ll1l1l1_opy_)
    uri = bstack1l1l1l1l1_opy_(bstack11ll11l1ll_opy_)
    try:
      response = bstack1ll111lll1_opy_(bstack111ll11_opy_ (u"ࠬࡍࡅࡕࠩ፯"), uri, {}, {bstack111ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ፰"): (self.config[bstack111ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ፱")], self.config[bstack111ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ፲")])})
      if response.status_code == 200:
        bstack111ll11lll_opy_ = response.json()
        if bstack111ll11_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣ፳") in bstack111ll11lll_opy_:
          return bstack111ll11lll_opy_[bstack111ll11_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤ፴")]
        else:
          raise bstack111ll11_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫ፵").format(bstack111ll11lll_opy_)
      else:
        raise bstack111ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧ፶").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺࠢ፷").format(e))
  def bstack111llll1ll_opy_(self):
    bstack111ll1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠥ፸"))
    try:
      if bstack111ll11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ፹") not in self.bstack111l1ll111_opy_:
        self.bstack111l1ll111_opy_[bstack111ll11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ፺")] = 2
      with open(bstack111ll1llll_opy_, bstack111ll11_opy_ (u"ࠪࡻࠬ፻")) as fp:
        json.dump(self.bstack111l1ll111_opy_, fp)
      return bstack111ll1llll_opy_
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ፼").format(e))
  def bstack111ll11l11_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111lll111l_opy_ == bstack111ll11_opy_ (u"ࠬࡽࡩ࡯ࠩ፽"):
        bstack111lll11ll_opy_ = [bstack111ll11_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧ፾"), bstack111ll11_opy_ (u"ࠧ࠰ࡥࠪ፿")]
        cmd = bstack111lll11ll_opy_ + cmd
      cmd = bstack111ll11_opy_ (u"ࠨࠢࠪᎀ").join(cmd)
      self.logger.debug(bstack111ll11_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨᎁ").format(cmd))
      with open(self.bstack111ll11ll1_opy_, bstack111ll11_opy_ (u"ࠥࡥࠧᎂ")) as bstack111ll1ll11_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111ll1ll11_opy_, text=True, stderr=bstack111ll1ll11_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111l1l1ll1_opy_ = True
      self.logger.error(bstack111ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᎃ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111llll11l_opy_:
        self.logger.info(bstack111ll11_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨᎄ"))
        cmd = [self.binary_path, bstack111ll11_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤᎅ")]
        self.bstack111ll11l11_opy_(cmd)
        self.bstack111llll11l_opy_ = False
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᎆ").format(cmd, e))
  def bstack1l11ll111_opy_(self):
    if not self.bstack111l11l1_opy_:
      return
    try:
      bstack111l1l1lll_opy_ = 0
      while not self.bstack111llll11l_opy_ and bstack111l1l1lll_opy_ < self.bstack111lllll11_opy_:
        if self.bstack111l1l1ll1_opy_:
          self.logger.info(bstack111ll11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨᎇ"))
          return
        time.sleep(1)
        bstack111l1l1lll_opy_ += 1
      os.environ[bstack111ll11_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨᎈ")] = str(self.bstack111llll1l1_opy_())
      self.logger.info(bstack111ll11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦᎉ"))
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᎊ").format(e))
  def bstack111llll1l1_opy_(self):
    if self.bstack1l1111l1l_opy_:
      return
    try:
      bstack11l1111111_opy_ = [platform[bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᎋ")].lower() for platform in self.config.get(bstack111ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᎌ"), [])]
      bstack111lllllll_opy_ = sys.maxsize
      bstack111lllll1l_opy_ = bstack111ll11_opy_ (u"ࠧࠨᎍ")
      for browser in bstack11l1111111_opy_:
        if browser in self.bstack111l1lllll_opy_:
          bstack11l11111l1_opy_ = self.bstack111l1lllll_opy_[browser]
        if bstack11l11111l1_opy_ < bstack111lllllll_opy_:
          bstack111lllllll_opy_ = bstack11l11111l1_opy_
          bstack111lllll1l_opy_ = browser
      return bstack111lllll1l_opy_
    except Exception as e:
      self.logger.error(bstack111ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᎎ").format(e))