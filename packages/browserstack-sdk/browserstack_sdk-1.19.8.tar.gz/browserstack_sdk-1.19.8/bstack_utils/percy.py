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
from bstack_utils.helper import bstack1ll1111l1l_opy_, bstack1llll11ll_opy_
class bstack11l1l1ll1_opy_:
  working_dir = os.getcwd()
  bstack11lll111l_opy_ = False
  config = {}
  binary_path = bstack11lllll_opy_ (u"ࠨࠩጬ")
  bstack111llll11l_opy_ = bstack11lllll_opy_ (u"ࠩࠪጭ")
  bstack111llll1_opy_ = False
  bstack111lll1l11_opy_ = None
  bstack111lll11ll_opy_ = {}
  bstack111ll11l1l_opy_ = 300
  bstack111l1ll11l_opy_ = False
  logger = None
  bstack111lllll1l_opy_ = False
  bstack111ll11ll1_opy_ = bstack11lllll_opy_ (u"ࠪࠫጮ")
  bstack111l1lll11_opy_ = {
    bstack11lllll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫጯ") : 1,
    bstack11lllll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ጰ") : 2,
    bstack11lllll_opy_ (u"࠭ࡥࡥࡩࡨࠫጱ") : 3,
    bstack11lllll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧጲ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111lllll11_opy_(self):
    bstack111l1lll1l_opy_ = bstack11lllll_opy_ (u"ࠨࠩጳ")
    bstack11l11111ll_opy_ = sys.platform
    bstack111l11llll_opy_ = bstack11lllll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨጴ")
    if re.match(bstack11lllll_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥጵ"), bstack11l11111ll_opy_) != None:
      bstack111l1lll1l_opy_ = bstack11ll11ll11_opy_ + bstack11lllll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧጶ")
      self.bstack111ll11ll1_opy_ = bstack11lllll_opy_ (u"ࠬࡳࡡࡤࠩጷ")
    elif re.match(bstack11lllll_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦጸ"), bstack11l11111ll_opy_) != None:
      bstack111l1lll1l_opy_ = bstack11ll11ll11_opy_ + bstack11lllll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣጹ")
      bstack111l11llll_opy_ = bstack11lllll_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦጺ")
      self.bstack111ll11ll1_opy_ = bstack11lllll_opy_ (u"ࠩࡺ࡭ࡳ࠭ጻ")
    else:
      bstack111l1lll1l_opy_ = bstack11ll11ll11_opy_ + bstack11lllll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨጼ")
      self.bstack111ll11ll1_opy_ = bstack11lllll_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪጽ")
    return bstack111l1lll1l_opy_, bstack111l11llll_opy_
  def bstack111l1llll1_opy_(self):
    try:
      bstack111ll1l1ll_opy_ = [os.path.join(expanduser(bstack11lllll_opy_ (u"ࠧࢄࠢጾ")), bstack11lllll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ጿ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111ll1l1ll_opy_:
        if(self.bstack111ll1ll1l_opy_(path)):
          return path
      raise bstack11lllll_opy_ (u"ࠢࡖࡰࡤࡰࡧ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦፀ")
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥፁ").format(e))
  def bstack111ll1ll1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111lll1111_opy_(self, bstack111l1lll1l_opy_, bstack111l11llll_opy_):
    try:
      bstack111lllllll_opy_ = self.bstack111l1llll1_opy_()
      bstack111ll1l111_opy_ = os.path.join(bstack111lllllll_opy_, bstack11lllll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬፂ"))
      bstack111ll11lll_opy_ = os.path.join(bstack111lllllll_opy_, bstack111l11llll_opy_)
      if os.path.exists(bstack111ll11lll_opy_):
        self.logger.info(bstack11lllll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧፃ").format(bstack111ll11lll_opy_))
        return bstack111ll11lll_opy_
      if os.path.exists(bstack111ll1l111_opy_):
        self.logger.info(bstack11lllll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤፄ").format(bstack111ll1l111_opy_))
        return self.bstack111l1ll1ll_opy_(bstack111ll1l111_opy_, bstack111l11llll_opy_)
      self.logger.info(bstack11lllll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥፅ").format(bstack111l1lll1l_opy_))
      response = bstack1llll11ll_opy_(bstack11lllll_opy_ (u"࠭ࡇࡆࡖࠪፆ"), bstack111l1lll1l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack111ll1l111_opy_, bstack11lllll_opy_ (u"ࠧࡸࡤࠪፇ")) as file:
          file.write(response.content)
        self.logger.info(bstack111l1l11ll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࡧ࡯࡮ࡢࡴࡼࡣࡿ࡯ࡰࡠࡲࡤࡸ࡭ࢃࠢፈ"))
        return self.bstack111l1ll1ll_opy_(bstack111ll1l111_opy_, bstack111l11llll_opy_)
      else:
        raise(bstack111l1l11ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࡶࡪࡹࡰࡰࡰࡶࡩ࠳ࡹࡴࡢࡶࡸࡷࡤࡩ࡯ࡥࡧࢀࠦፉ"))
    except:
      self.logger.error(bstack11lllll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢፊ"))
  def bstack111ll11111_opy_(self, bstack111l1lll1l_opy_, bstack111l11llll_opy_):
    try:
      bstack111ll11lll_opy_ = self.bstack111lll1111_opy_(bstack111l1lll1l_opy_, bstack111l11llll_opy_)
      bstack111l1l11l1_opy_ = self.bstack111l1lllll_opy_(bstack111l1lll1l_opy_, bstack111l11llll_opy_, bstack111ll11lll_opy_)
      return bstack111ll11lll_opy_, bstack111l1l11l1_opy_
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣፋ").format(e))
    return bstack111ll11lll_opy_, False
  def bstack111l1lllll_opy_(self, bstack111l1lll1l_opy_, bstack111l11llll_opy_, bstack111ll11lll_opy_, bstack111ll1l11l_opy_ = 0):
    if bstack111ll1l11l_opy_ > 1:
      return False
    if bstack111ll11lll_opy_ == None or os.path.exists(bstack111ll11lll_opy_) == False:
      self.logger.warn(bstack11lllll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥፌ"))
      bstack111ll11lll_opy_ = self.bstack111lll1111_opy_(bstack111l1lll1l_opy_, bstack111l11llll_opy_)
      self.bstack111l1lllll_opy_(bstack111l1lll1l_opy_, bstack111l11llll_opy_, bstack111ll11lll_opy_, bstack111ll1l11l_opy_+1)
    bstack111lll1l1l_opy_ = bstack11lllll_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦፍ")
    command = bstack11lllll_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ፎ").format(bstack111ll11lll_opy_)
    bstack111l1ll1l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111lll1l1l_opy_, bstack111l1ll1l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack11lllll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢፏ"))
      bstack111ll11lll_opy_ = self.bstack111lll1111_opy_(bstack111l1lll1l_opy_, bstack111l11llll_opy_)
      self.bstack111l1lllll_opy_(bstack111l1lll1l_opy_, bstack111l11llll_opy_, bstack111ll11lll_opy_, bstack111ll1l11l_opy_+1)
  def bstack111l1ll1ll_opy_(self, bstack111ll1l111_opy_, bstack111l11llll_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll1l111_opy_)
      shutil.unpack_archive(bstack111ll1l111_opy_, working_dir)
      bstack111ll11lll_opy_ = os.path.join(working_dir, bstack111l11llll_opy_)
      os.chmod(bstack111ll11lll_opy_, 0o755)
      return bstack111ll11lll_opy_
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥፐ"))
  def bstack111ll1llll_opy_(self):
    try:
      percy = str(self.config.get(bstack11lllll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩፑ"), bstack11lllll_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥፒ"))).lower()
      if percy != bstack11lllll_opy_ (u"ࠧࡺࡲࡶࡧࠥፓ"):
        return False
      self.bstack111llll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣፔ").format(e))
  def bstack11l111111l_opy_(self):
    try:
      bstack11l111111l_opy_ = str(self.config.get(bstack11lllll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪፕ"), bstack11lllll_opy_ (u"ࠣࡣࡸࡸࡴࠨፖ"))).lower()
      return bstack11l111111l_opy_
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥࡳ࡯ࡥࡧ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥፗ").format(e))
  def init(self, bstack11lll111l_opy_, config, logger):
    self.bstack11lll111l_opy_ = bstack11lll111l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111ll1llll_opy_():
      return
    self.bstack111lll11ll_opy_ = config.get(bstack11lllll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩፘ"), {})
    self.bstack111ll1ll11_opy_ = config.get(bstack11lllll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧፙ"), bstack11lllll_opy_ (u"ࠧࡧࡵࡵࡱࠥፚ"))
    try:
      bstack111l1lll1l_opy_, bstack111l11llll_opy_ = self.bstack111lllll11_opy_()
      bstack111ll11lll_opy_, bstack111l1l11l1_opy_ = self.bstack111ll11111_opy_(bstack111l1lll1l_opy_, bstack111l11llll_opy_)
      if bstack111l1l11l1_opy_:
        self.binary_path = bstack111ll11lll_opy_
        thread = Thread(target=self.bstack111ll111ll_opy_)
        thread.start()
      else:
        self.bstack111lllll1l_opy_ = True
        self.logger.error(bstack11lllll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥ፛").format(bstack111ll11lll_opy_))
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ፜").format(e))
  def bstack111ll1lll1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11lllll_opy_ (u"ࠨ࡮ࡲ࡫ࠬ፝"), bstack11lllll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬ፞"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11lllll_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢ፟").format(logfile))
      self.bstack111llll11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ፠").format(e))
  def bstack111ll111ll_opy_(self):
    bstack111llllll1_opy_ = self.bstack111llll1l1_opy_()
    if bstack111llllll1_opy_ == None:
      self.bstack111lllll1l_opy_ = True
      self.logger.error(bstack11lllll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣ፡"))
      return False
    command_args = [bstack11lllll_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢ።") if self.bstack11lll111l_opy_ else bstack11lllll_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫ፣")]
    bstack111lll1ll1_opy_ = self.bstack11l1111111_opy_()
    if bstack111lll1ll1_opy_ != None:
      command_args.append(bstack11lllll_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢ፤").format(bstack111lll1ll1_opy_))
    env = os.environ.copy()
    env[bstack11lllll_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢ፥")] = bstack111llllll1_opy_
    bstack111llll1ll_opy_ = [self.binary_path]
    self.bstack111ll1lll1_opy_()
    self.bstack111lll1l11_opy_ = self.bstack111lll1lll_opy_(bstack111llll1ll_opy_ + command_args, env)
    self.logger.debug(bstack11lllll_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦ፦"))
    bstack111ll1l11l_opy_ = 0
    while self.bstack111lll1l11_opy_.poll() == None:
      bstack111lll111l_opy_ = self.bstack111l1l111l_opy_()
      if bstack111lll111l_opy_:
        self.logger.debug(bstack11lllll_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢ፧"))
        self.bstack111l1ll11l_opy_ = True
        return True
      bstack111ll1l11l_opy_ += 1
      self.logger.debug(bstack11lllll_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣ፨").format(bstack111ll1l11l_opy_))
      time.sleep(2)
    self.logger.error(bstack11lllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦ፩").format(bstack111ll1l11l_opy_))
    self.bstack111lllll1l_opy_ = True
    return False
  def bstack111l1l111l_opy_(self, bstack111ll1l11l_opy_ = 0):
    try:
      if bstack111ll1l11l_opy_ > 10:
        return False
      bstack111l1l1l11_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧ፪"), bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩ፫"))
      bstack111l1ll111_opy_ = bstack111l1l1l11_opy_ + bstack11ll11lll1_opy_
      response = requests.get(bstack111l1ll111_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack111llll1l1_opy_(self):
    bstack111ll111l1_opy_ = bstack11lllll_opy_ (u"ࠩࡤࡴࡵ࠭፬") if self.bstack11lll111l_opy_ else bstack11lllll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ፭")
    bstack11l11lll1l_opy_ = bstack11lllll_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠥ፮").format(self.config[bstack11lllll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ፯")], bstack111ll111l1_opy_)
    uri = bstack1ll1111l1l_opy_(bstack11l11lll1l_opy_)
    try:
      response = bstack1llll11ll_opy_(bstack11lllll_opy_ (u"࠭ࡇࡆࡖࠪ፰"), uri, {}, {bstack11lllll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ፱"): (self.config[bstack11lllll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ፲")], self.config[bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ፳")])})
      if response.status_code == 200:
        bstack111l1l1ll1_opy_ = response.json()
        if bstack11lllll_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤ፴") in bstack111l1l1ll1_opy_:
          return bstack111l1l1ll1_opy_[bstack11lllll_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥ፵")]
        else:
          raise bstack11lllll_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬ፶").format(bstack111l1l1ll1_opy_)
      else:
        raise bstack11lllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨ፷").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣ፸").format(e))
  def bstack11l1111111_opy_(self):
    bstack111ll11l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦ፹"))
    try:
      if bstack11lllll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ፺") not in self.bstack111lll11ll_opy_:
        self.bstack111lll11ll_opy_[bstack11lllll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ፻")] = 2
      with open(bstack111ll11l11_opy_, bstack11lllll_opy_ (u"ࠫࡼ࠭፼")) as fp:
        json.dump(self.bstack111lll11ll_opy_, fp)
      return bstack111ll11l11_opy_
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ፽").format(e))
  def bstack111lll1lll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111ll11ll1_opy_ == bstack11lllll_opy_ (u"࠭ࡷࡪࡰࠪ፾"):
        bstack111ll1111l_opy_ = [bstack11lllll_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨ፿"), bstack11lllll_opy_ (u"ࠨ࠱ࡦࠫᎀ")]
        cmd = bstack111ll1111l_opy_ + cmd
      cmd = bstack11lllll_opy_ (u"ࠩࠣࠫᎁ").join(cmd)
      self.logger.debug(bstack11lllll_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃࠢᎂ").format(cmd))
      with open(self.bstack111llll11l_opy_, bstack11lllll_opy_ (u"ࠦࡦࠨᎃ")) as bstack111l1l1lll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111l1l1lll_opy_, text=True, stderr=bstack111l1l1lll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111lllll1l_opy_ = True
      self.logger.error(bstack11lllll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᎄ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111l1ll11l_opy_:
        self.logger.info(bstack11lllll_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿࠢᎅ"))
        cmd = [self.binary_path, bstack11lllll_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲࠥᎆ")]
        self.bstack111lll1lll_opy_(cmd)
        self.bstack111l1ll11l_opy_ = False
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᎇ").format(cmd, e))
  def bstack111ll1lll_opy_(self):
    if not self.bstack111llll1_opy_:
      return
    try:
      bstack111llll111_opy_ = 0
      while not self.bstack111l1ll11l_opy_ and bstack111llll111_opy_ < self.bstack111ll11l1l_opy_:
        if self.bstack111lllll1l_opy_:
          self.logger.info(bstack11lllll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢᎈ"))
          return
        time.sleep(1)
        bstack111llll111_opy_ += 1
      os.environ[bstack11lllll_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩᎉ")] = str(self.bstack11l11111l1_opy_())
      self.logger.info(bstack11lllll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠧᎊ"))
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᎋ").format(e))
  def bstack11l11111l1_opy_(self):
    if self.bstack11lll111l_opy_:
      return
    try:
      bstack111ll1l1l1_opy_ = [platform[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᎌ")].lower() for platform in self.config.get(bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᎍ"), [])]
      bstack111l1l1111_opy_ = sys.maxsize
      bstack111lll11l1_opy_ = bstack11lllll_opy_ (u"ࠨࠩᎎ")
      for browser in bstack111ll1l1l1_opy_:
        if browser in self.bstack111l1lll11_opy_:
          bstack111l1l1l1l_opy_ = self.bstack111l1lll11_opy_[browser]
        if bstack111l1l1l1l_opy_ < bstack111l1l1111_opy_:
          bstack111l1l1111_opy_ = bstack111l1l1l1l_opy_
          bstack111lll11l1_opy_ = browser
      return bstack111lll11l1_opy_
    except Exception as e:
      self.logger.error(bstack11lllll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᎏ").format(e))