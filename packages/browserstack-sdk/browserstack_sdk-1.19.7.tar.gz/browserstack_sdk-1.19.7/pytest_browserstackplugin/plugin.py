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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack111111l1l_opy_, bstack11l1lllll_opy_, update, bstack1ll1l1ll11_opy_,
                                       bstack1ll11l1l1_opy_, bstack1l11l11ll_opy_, bstack1ll1111l1_opy_, bstack1lll1l1l1l_opy_,
                                       bstack1llll11111_opy_, bstack1lll11l111_opy_, bstack1l1111l11_opy_, bstack1l11l1ll1_opy_,
                                       bstack1ll1lll1_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l1l111l1l_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1l1ll11l_opy_, bstack1ll1l1l1_opy_, bstack1ll1111111_opy_, bstack1lll1lll1_opy_, \
    bstack1ll1ll1l11_opy_
from bstack_utils.helper import bstack1ll1ll1ll_opy_, bstack1111l111l_opy_, bstack11l1ll11ll_opy_, bstack111l11ll1_opy_, \
    bstack11l1ll1l11_opy_, \
    bstack11ll111111_opy_, bstack1llll11ll1_opy_, bstack1l11ll1l1_opy_, bstack11l1lllll1_opy_, bstack1ll11l1l1l_opy_, Notset, \
    bstack1ll111111_opy_, bstack11l1l1l11l_opy_, bstack11l1llllll_opy_, Result, bstack11l1ll1l1l_opy_, bstack11l1l11ll1_opy_, bstack1l11lll1ll_opy_, \
    bstack1ll1l1l1ll_opy_, bstack1l1ll1111_opy_, bstack1llll11l1_opy_, bstack11ll111l1l_opy_
from bstack_utils.bstack11l11l111l_opy_ import bstack11l111ll11_opy_
from bstack_utils.messages import bstack1l1lllll1l_opy_, bstack111l1ll11_opy_, bstack1lll11ll1l_opy_, bstack11l1l11l1_opy_, bstack111l111ll_opy_, \
    bstack1l11ll11_opy_, bstack1lllllll1_opy_, bstack1llll1lll1_opy_, bstack1l1l1l1111_opy_, bstack1l1llll111_opy_, \
    bstack11llll1l1_opy_, bstack11lllll1_opy_
from bstack_utils.proxy import bstack11111ll1l_opy_, bstack1ll1l1l1l1_opy_
from bstack_utils.bstack1l1ll1ll1_opy_ import bstack1111l1ll11_opy_, bstack1111ll1ll1_opy_, bstack1111ll11l1_opy_, bstack1111l1lll1_opy_, \
    bstack1111ll1111_opy_, bstack1111ll111l_opy_, bstack1111l1ll1l_opy_, bstack11ll1l11l_opy_, bstack1111l1l1ll_opy_
from bstack_utils.bstack11lll11ll_opy_ import bstack1ll1lll111_opy_
from bstack_utils.bstack1lll111ll_opy_ import bstack11l1ll1ll_opy_, bstack1l1ll1lll1_opy_, bstack1ll1l11l1_opy_, \
    bstack11llll11_opy_, bstack111llll1l_opy_
from bstack_utils.bstack1l11l111ll_opy_ import bstack1l11lllll1_opy_
from bstack_utils.bstack1l1l1ll111_opy_ import bstack1ll1l1llll_opy_
import bstack_utils.bstack11llllll_opy_ as bstack1llll111ll_opy_
bstack1ll11l111_opy_ = None
bstack1111l11l_opy_ = None
bstack1llll11l_opy_ = None
bstack111111111_opy_ = None
bstack1l1lll1l_opy_ = None
bstack11l1l111_opy_ = None
bstack1llll1ll1l_opy_ = None
bstack1lll11l1_opy_ = None
bstack1ll1lll1ll_opy_ = None
bstack1lllll1l11_opy_ = None
bstack1l1llll11l_opy_ = None
bstack11l1ll111_opy_ = None
bstack111l1lll1_opy_ = None
bstack1lll11l11_opy_ = bstack111ll11_opy_ (u"࠭ࠧᔰ")
CONFIG = {}
bstack11l1l11l_opy_ = False
bstack1l1lll1l1l_opy_ = bstack111ll11_opy_ (u"ࠧࠨᔱ")
bstack1l1l1l1ll1_opy_ = bstack111ll11_opy_ (u"ࠨࠩᔲ")
bstack1ll1l11l_opy_ = False
bstack1111l1l1l_opy_ = []
bstack1ll11111l1_opy_ = bstack1ll1l1l1_opy_
bstack1lllll1l11l_opy_ = bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᔳ")
bstack1llll1l1lll_opy_ = False
bstack1l11lll1_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll11111l1_opy_,
                    format=bstack111ll11_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᔴ"),
                    datefmt=bstack111ll11_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ᔵ"),
                    stream=sys.stdout)
store = {
    bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᔶ"): []
}
bstack1llll1l1l11_opy_ = False
def bstack1l111ll1l_opy_():
    global CONFIG
    global bstack1ll11111l1_opy_
    if bstack111ll11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᔷ") in CONFIG:
        bstack1ll11111l1_opy_ = bstack1l1ll11l_opy_[CONFIG[bstack111ll11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᔸ")]]
        logging.getLogger().setLevel(bstack1ll11111l1_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l11l1ll1l_opy_ = {}
current_test_uuid = None
def bstack1111l1ll_opy_(page, bstack1ll1ll11l_opy_):
    try:
        page.evaluate(bstack111ll11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᔹ"),
                      bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ᔺ") + json.dumps(
                          bstack1ll1ll11l_opy_) + bstack111ll11_opy_ (u"ࠥࢁࢂࠨᔻ"))
    except Exception as e:
        print(bstack111ll11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤᔼ"), e)
def bstack1ll11lll1l_opy_(page, message, level):
    try:
        page.evaluate(bstack111ll11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᔽ"), bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫᔾ") + json.dumps(
            message) + bstack111ll11_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪᔿ") + json.dumps(level) + bstack111ll11_opy_ (u"ࠨࡿࢀࠫᕀ"))
    except Exception as e:
        print(bstack111ll11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧᕁ"), e)
def pytest_configure(config):
    bstack11ll1l1l_opy_ = Config.get_instance()
    config.args = bstack1ll1l1llll_opy_.bstack1lllllll11l_opy_(config.args)
    bstack11ll1l1l_opy_.bstack1l1lll1l11_opy_(bstack1llll11l1_opy_(config.getoption(bstack111ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᕂ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lllll1llll_opy_ = item.config.getoption(bstack111ll11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᕃ"))
    plugins = item.config.getoption(bstack111ll11_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨᕄ"))
    report = outcome.get_result()
    bstack1lllll1111l_opy_(item, call, report)
    if bstack111ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦᕅ") not in plugins or bstack1ll11l1l1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack111ll11_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣᕆ"), None)
    page = getattr(item, bstack111ll11_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢᕇ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1llll1lllll_opy_(item, report, summary, bstack1lllll1llll_opy_)
    if (page is not None):
        bstack1llll1ll1ll_opy_(item, report, summary, bstack1lllll1llll_opy_)
def bstack1llll1lllll_opy_(item, report, summary, bstack1lllll1llll_opy_):
    if report.when == bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᕈ") and report.skipped:
        bstack1111l1l1ll_opy_(report)
    if report.when in [bstack111ll11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᕉ"), bstack111ll11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᕊ")]:
        return
    if not bstack11l1ll11ll_opy_():
        return
    try:
        if (str(bstack1lllll1llll_opy_).lower() != bstack111ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪᕋ")):
            item._driver.execute_script(
                bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫᕌ") + json.dumps(
                    report.nodeid) + bstack111ll11_opy_ (u"ࠧࡾࡿࠪᕍ"))
        os.environ[bstack111ll11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᕎ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack111ll11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤᕏ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111ll11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᕐ")))
    bstack11lll1ll1_opy_ = bstack111ll11_opy_ (u"ࠦࠧᕑ")
    bstack1111l1l1ll_opy_(report)
    if not passed:
        try:
            bstack11lll1ll1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack111ll11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᕒ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11lll1ll1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack111ll11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᕓ")))
        bstack11lll1ll1_opy_ = bstack111ll11_opy_ (u"ࠢࠣᕔ")
        if not passed:
            try:
                bstack11lll1ll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111ll11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᕕ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11lll1ll1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ᕖ")
                    + json.dumps(bstack111ll11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦᕗ"))
                    + bstack111ll11_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᕘ")
                )
            else:
                item._driver.execute_script(
                    bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᕙ")
                    + json.dumps(str(bstack11lll1ll1_opy_))
                    + bstack111ll11_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤᕚ")
                )
        except Exception as e:
            summary.append(bstack111ll11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧᕛ").format(e))
def bstack1llll1l111l_opy_(test_name, error_message):
    try:
        bstack1llll1l1ll1_opy_ = []
        bstack1ll1l1ll_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᕜ"), bstack111ll11_opy_ (u"ࠩ࠳ࠫᕝ"))
        bstack11ll11l1_opy_ = {bstack111ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨᕞ"): test_name, bstack111ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᕟ"): error_message, bstack111ll11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᕠ"): bstack1ll1l1ll_opy_}
        bstack1llll1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᕡ"))
        if os.path.exists(bstack1llll1l1111_opy_):
            with open(bstack1llll1l1111_opy_) as f:
                bstack1llll1l1ll1_opy_ = json.load(f)
        bstack1llll1l1ll1_opy_.append(bstack11ll11l1_opy_)
        with open(bstack1llll1l1111_opy_, bstack111ll11_opy_ (u"ࠧࡸࠩᕢ")) as f:
            json.dump(bstack1llll1l1ll1_opy_, f)
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ᕣ") + str(e))
def bstack1llll1ll1ll_opy_(item, report, summary, bstack1lllll1llll_opy_):
    if report.when in [bstack111ll11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᕤ"), bstack111ll11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᕥ")]:
        return
    if (str(bstack1lllll1llll_opy_).lower() != bstack111ll11_opy_ (u"ࠫࡹࡸࡵࡦࠩᕦ")):
        bstack1111l1ll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111ll11_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᕧ")))
    bstack11lll1ll1_opy_ = bstack111ll11_opy_ (u"ࠨࠢᕨ")
    bstack1111l1l1ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11lll1ll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111ll11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᕩ").format(e)
                )
        try:
            if passed:
                bstack111llll1l_opy_(getattr(item, bstack111ll11_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᕪ"), None), bstack111ll11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᕫ"))
            else:
                error_message = bstack111ll11_opy_ (u"ࠪࠫᕬ")
                if bstack11lll1ll1_opy_:
                    bstack1ll11lll1l_opy_(item._page, str(bstack11lll1ll1_opy_), bstack111ll11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᕭ"))
                    bstack111llll1l_opy_(getattr(item, bstack111ll11_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᕮ"), None), bstack111ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᕯ"), str(bstack11lll1ll1_opy_))
                    error_message = str(bstack11lll1ll1_opy_)
                else:
                    bstack111llll1l_opy_(getattr(item, bstack111ll11_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᕰ"), None), bstack111ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᕱ"))
                bstack1llll1l111l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack111ll11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨᕲ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack111ll11_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᕳ"), default=bstack111ll11_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᕴ"), help=bstack111ll11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᕵ"))
    parser.addoption(bstack111ll11_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᕶ"), default=bstack111ll11_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨᕷ"), help=bstack111ll11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢᕸ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack111ll11_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦᕹ"), action=bstack111ll11_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤᕺ"), default=bstack111ll11_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦᕻ"),
                         help=bstack111ll11_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦᕼ"))
def bstack1l11l1lll1_opy_(log):
    if not (log[bstack111ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕽ")] and log[bstack111ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᕾ")].strip()):
        return
    active = bstack1l11111ll1_opy_()
    log = {
        bstack111ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᕿ"): log[bstack111ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᖀ")],
        bstack111ll11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᖁ"): datetime.datetime.utcnow().isoformat() + bstack111ll11_opy_ (u"ࠫ࡟࠭ᖂ"),
        bstack111ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖃ"): log[bstack111ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖄ")],
    }
    if active:
        if active[bstack111ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬᖅ")] == bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᖆ"):
            log[bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖇ")] = active[bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖈ")]
        elif active[bstack111ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩᖉ")] == bstack111ll11_opy_ (u"ࠬࡺࡥࡴࡶࠪᖊ"):
            log[bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖋ")] = active[bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖌ")]
    bstack1ll1l1llll_opy_.bstack1l111lllll_opy_([log])
def bstack1l11111ll1_opy_():
    if len(store[bstack111ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᖍ")]) > 0 and store[bstack111ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᖎ")][-1]:
        return {
            bstack111ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨᖏ"): bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᖐ"),
            bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖑ"): store[bstack111ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᖒ")][-1]
        }
    if store.get(bstack111ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᖓ"), None):
        return {
            bstack111ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᖔ"): bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺࠧᖕ"),
            bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖖ"): store[bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᖗ")]
        }
    return None
bstack1l11ll111l_opy_ = bstack1l1l111l1l_opy_(bstack1l11l1lll1_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1llll1l1lll_opy_
        if bstack1llll1l1lll_opy_:
            driver = getattr(item, bstack111ll11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᖘ"), None)
            bstack11l1l1111_opy_ = bstack1llll111ll_opy_.bstack1llll11l1l_opy_(CONFIG, bstack11ll111111_opy_(item.own_markers))
            item._a11y_started = bstack1llll111ll_opy_.bstack1l1l1l11l1_opy_(driver, bstack11l1l1111_opy_)
        if not bstack1ll1l1llll_opy_.on() or bstack1lllll1l11l_opy_ != bstack111ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᖙ"):
            return
        global current_test_uuid, bstack1l11ll111l_opy_
        bstack1l11ll111l_opy_.start()
        bstack1l11l1l1l1_opy_ = {
            bstack111ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᖚ"): uuid4().__str__(),
            bstack111ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᖛ"): datetime.datetime.utcnow().isoformat() + bstack111ll11_opy_ (u"ࠩ࡝ࠫᖜ")
        }
        current_test_uuid = bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖝ")]
        store[bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᖞ")] = bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪᖟ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l11l1ll1l_opy_[item.nodeid] = {**_1l11l1ll1l_opy_[item.nodeid], **bstack1l11l1l1l1_opy_}
        bstack1lllll11lll_opy_(item, _1l11l1ll1l_opy_[item.nodeid], bstack111ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᖠ"))
    except Exception as err:
        print(bstack111ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩᖡ"), str(err))
def pytest_runtest_setup(item):
    global bstack1llll1l1l11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1lllll1_opy_():
        atexit.register(bstack1ll1l111ll_opy_)
        if not bstack1llll1l1l11_opy_:
            try:
                bstack1lllll111l1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11ll111l1l_opy_():
                    bstack1lllll111l1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lllll111l1_opy_:
                    signal.signal(s, bstack1llll1ll111_opy_)
                bstack1llll1l1l11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack111ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤᖢ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1111l1ll11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack111ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᖣ")
    try:
        if not bstack1ll1l1llll_opy_.on():
            return
        bstack1l11ll111l_opy_.start()
        uuid = uuid4().__str__()
        bstack1l11l1l1l1_opy_ = {
            bstack111ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖤ"): uuid,
            bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᖥ"): datetime.datetime.utcnow().isoformat() + bstack111ll11_opy_ (u"ࠬࡠࠧᖦ"),
            bstack111ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫᖧ"): bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᖨ"),
            bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᖩ"): bstack111ll11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᖪ"),
            bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᖫ"): bstack111ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᖬ")
        }
        threading.current_thread().current_hook_uuid = uuid
        store[bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᖭ")] = item
        store[bstack111ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᖮ")] = [uuid]
        if not _1l11l1ll1l_opy_.get(item.nodeid, None):
            _1l11l1ll1l_opy_[item.nodeid] = {bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᖯ"): [], bstack111ll11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᖰ"): []}
        _1l11l1ll1l_opy_[item.nodeid][bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᖱ")].append(bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖲ")])
        _1l11l1ll1l_opy_[item.nodeid + bstack111ll11_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫᖳ")] = bstack1l11l1l1l1_opy_
        bstack1lllll11111_opy_(item, bstack1l11l1l1l1_opy_, bstack111ll11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᖴ"))
    except Exception as err:
        print(bstack111ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᖵ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l11lll1_opy_
        if CONFIG.get(bstack111ll11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᖶ"), False):
            if CONFIG.get(bstack111ll11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᖷ"), bstack111ll11_opy_ (u"ࠤࡤࡹࡹࡵࠢᖸ")) == bstack111ll11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᖹ"):
                bstack1llll1l11l1_opy_ = bstack1ll1ll1ll_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᖺ"), None)
                bstack11lll11l1_opy_ = bstack1llll1l11l1_opy_ + bstack111ll11_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣᖻ")
                driver = getattr(item, bstack111ll11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᖼ"), None)
                PercySDK.screenshot(driver, bstack11lll11l1_opy_)
        if getattr(item, bstack111ll11_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧᖽ"), False):
            logger.info(bstack111ll11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣᖾ"))
            driver = getattr(item, bstack111ll11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᖿ"), None)
            bstack11lll1ll11_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1llll111ll_opy_.bstack1l1l1l1lll_opy_(driver, bstack11lll1ll11_opy_, item.name, item.module.__name__, item.path, bstack1l11lll1_opy_)
        if not bstack1ll1l1llll_opy_.on():
            return
        bstack1l11l1l1l1_opy_ = {
            bstack111ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᗀ"): uuid4().__str__(),
            bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᗁ"): datetime.datetime.utcnow().isoformat() + bstack111ll11_opy_ (u"ࠬࡠࠧᗂ"),
            bstack111ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫᗃ"): bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᗄ"),
            bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᗅ"): bstack111ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᗆ"),
            bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᗇ"): bstack111ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᗈ")
        }
        _1l11l1ll1l_opy_[item.nodeid + bstack111ll11_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᗉ")] = bstack1l11l1l1l1_opy_
        bstack1lllll11111_opy_(item, bstack1l11l1l1l1_opy_, bstack111ll11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᗊ"))
    except Exception as err:
        print(bstack111ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭ᗋ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1ll1l1llll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1111l1lll1_opy_(fixturedef.argname):
        store[bstack111ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧᗌ")] = request.node
    elif bstack1111ll1111_opy_(fixturedef.argname):
        store[bstack111ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧᗍ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack111ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨᗎ"): fixturedef.argname,
            bstack111ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᗏ"): bstack11l1ll1l11_opy_(outcome),
            bstack111ll11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᗐ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack1lllll11l11_opy_ = store[bstack111ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᗑ")]
        if not _1l11l1ll1l_opy_.get(bstack1lllll11l11_opy_.nodeid, None):
            _1l11l1ll1l_opy_[bstack1lllll11l11_opy_.nodeid] = {bstack111ll11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᗒ"): []}
        _1l11l1ll1l_opy_[bstack1lllll11l11_opy_.nodeid][bstack111ll11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᗓ")].append(fixture)
    except Exception as err:
        logger.debug(bstack111ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬᗔ"), str(err))
if bstack1ll11l1l1l_opy_() and bstack1ll1l1llll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l11l1ll1l_opy_[request.node.nodeid][bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᗕ")].bstack111111l1l1_opy_(id(step))
        except Exception as err:
            print(bstack111ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩᗖ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l11l1ll1l_opy_[request.node.nodeid][bstack111ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᗗ")].bstack1l1l111111_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack111ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᗘ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l11l111ll_opy_: bstack1l11lllll1_opy_ = _1l11l1ll1l_opy_[request.node.nodeid][bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᗙ")]
            bstack1l11l111ll_opy_.bstack1l1l111111_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack111ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬᗚ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lllll1l11l_opy_
        try:
            if not bstack1ll1l1llll_opy_.on() or bstack1lllll1l11l_opy_ != bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᗛ"):
                return
            global bstack1l11ll111l_opy_
            bstack1l11ll111l_opy_.start()
            if not _1l11l1ll1l_opy_.get(request.node.nodeid, None):
                _1l11l1ll1l_opy_[request.node.nodeid] = {}
            bstack1l11l111ll_opy_ = bstack1l11lllll1_opy_.bstack11111l1l1l_opy_(
                scenario, feature, request.node,
                name=bstack1111ll111l_opy_(request.node, scenario),
                bstack1l111l111l_opy_=bstack111l11ll1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack111ll11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᗜ"),
                tags=bstack1111l1ll1l_opy_(feature, scenario)
            )
            _1l11l1ll1l_opy_[request.node.nodeid][bstack111ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᗝ")] = bstack1l11l111ll_opy_
            bstack1llll1l11ll_opy_(bstack1l11l111ll_opy_.uuid)
            bstack1ll1l1llll_opy_.bstack1l1l11111l_opy_(bstack111ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᗞ"), bstack1l11l111ll_opy_)
        except Exception as err:
            print(bstack111ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨᗟ"), str(err))
def bstack1lllll1l111_opy_(bstack1llll11lll1_opy_):
    if bstack1llll11lll1_opy_ in store[bstack111ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᗠ")]:
        store[bstack111ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᗡ")].remove(bstack1llll11lll1_opy_)
def bstack1llll1l11ll_opy_(bstack1llll1ll1l1_opy_):
    store[bstack111ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᗢ")] = bstack1llll1ll1l1_opy_
    threading.current_thread().current_test_uuid = bstack1llll1ll1l1_opy_
@bstack1ll1l1llll_opy_.bstack1llllll1lll_opy_
def bstack1lllll1111l_opy_(item, call, report):
    global bstack1lllll1l11l_opy_
    bstack1llllll1l_opy_ = bstack111l11ll1_opy_()
    if hasattr(report, bstack111ll11_opy_ (u"ࠪࡷࡹࡵࡰࠨᗣ")):
        bstack1llllll1l_opy_ = bstack11l1ll1l1l_opy_(report.stop)
    if hasattr(report, bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪᗤ")):
        bstack1llllll1l_opy_ = bstack11l1ll1l1l_opy_(report.start)
    try:
        if getattr(report, bstack111ll11_opy_ (u"ࠬࡽࡨࡦࡰࠪᗥ"), bstack111ll11_opy_ (u"࠭ࠧᗦ")) == bstack111ll11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᗧ"):
            bstack1l11ll111l_opy_.reset()
        if getattr(report, bstack111ll11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᗨ"), bstack111ll11_opy_ (u"ࠩࠪᗩ")) == bstack111ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᗪ"):
            if bstack1lllll1l11l_opy_ == bstack111ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᗫ"):
                _1l11l1ll1l_opy_[item.nodeid][bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᗬ")] = bstack1llllll1l_opy_
                bstack1lllll11lll_opy_(item, _1l11l1ll1l_opy_[item.nodeid], bstack111ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᗭ"), report, call)
                store[bstack111ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᗮ")] = None
            elif bstack1lllll1l11l_opy_ == bstack111ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᗯ"):
                bstack1l11l111ll_opy_ = _1l11l1ll1l_opy_[item.nodeid][bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᗰ")]
                bstack1l11l111ll_opy_.set(hooks=_1l11l1ll1l_opy_[item.nodeid].get(bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᗱ"), []))
                exception, bstack1l1111l1l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1111l1l1_opy_ = [call.excinfo.exconly(), getattr(report, bstack111ll11_opy_ (u"ࠫࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠪᗲ"), bstack111ll11_opy_ (u"ࠬ࠭ᗳ"))]
                bstack1l11l111ll_opy_.stop(time=bstack1llllll1l_opy_, result=Result(result=getattr(report, bstack111ll11_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧᗴ"), bstack111ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᗵ")), exception=exception, bstack1l1111l1l1_opy_=bstack1l1111l1l1_opy_))
                bstack1ll1l1llll_opy_.bstack1l1l11111l_opy_(bstack111ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᗶ"), _1l11l1ll1l_opy_[item.nodeid][bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᗷ")])
        elif getattr(report, bstack111ll11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᗸ"), bstack111ll11_opy_ (u"ࠫࠬᗹ")) in [bstack111ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᗺ"), bstack111ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᗻ")]:
            bstack1l11l1l111_opy_ = item.nodeid + bstack111ll11_opy_ (u"ࠧ࠮ࠩᗼ") + getattr(report, bstack111ll11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᗽ"), bstack111ll11_opy_ (u"ࠩࠪᗾ"))
            if getattr(report, bstack111ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᗿ"), False):
                hook_type = bstack111ll11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᘀ") if getattr(report, bstack111ll11_opy_ (u"ࠬࡽࡨࡦࡰࠪᘁ"), bstack111ll11_opy_ (u"࠭ࠧᘂ")) == bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᘃ") else bstack111ll11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᘄ")
                _1l11l1ll1l_opy_[bstack1l11l1l111_opy_] = {
                    bstack111ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᘅ"): uuid4().__str__(),
                    bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᘆ"): bstack1llllll1l_opy_,
                    bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᘇ"): hook_type
                }
            _1l11l1ll1l_opy_[bstack1l11l1l111_opy_][bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᘈ")] = bstack1llllll1l_opy_
            bstack1lllll1l111_opy_(_1l11l1ll1l_opy_[bstack1l11l1l111_opy_][bstack111ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᘉ")])
            bstack1lllll11111_opy_(item, _1l11l1ll1l_opy_[bstack1l11l1l111_opy_], bstack111ll11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᘊ"), report, call)
            if getattr(report, bstack111ll11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᘋ"), bstack111ll11_opy_ (u"ࠩࠪᘌ")) == bstack111ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᘍ"):
                if getattr(report, bstack111ll11_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᘎ"), bstack111ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᘏ")) == bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᘐ"):
                    bstack1l11l1l1l1_opy_ = {
                        bstack111ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᘑ"): uuid4().__str__(),
                        bstack111ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᘒ"): bstack111l11ll1_opy_(),
                        bstack111ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᘓ"): bstack111l11ll1_opy_()
                    }
                    _1l11l1ll1l_opy_[item.nodeid] = {**_1l11l1ll1l_opy_[item.nodeid], **bstack1l11l1l1l1_opy_}
                    bstack1lllll11lll_opy_(item, _1l11l1ll1l_opy_[item.nodeid], bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᘔ"))
                    bstack1lllll11lll_opy_(item, _1l11l1ll1l_opy_[item.nodeid], bstack111ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᘕ"), report, call)
    except Exception as err:
        print(bstack111ll11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪᘖ"), str(err))
def bstack1llll11llll_opy_(test, bstack1l11l1l1l1_opy_, result=None, call=None, bstack1lll1l111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l11l111ll_opy_ = {
        bstack111ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᘗ"): bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᘘ")],
        bstack111ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᘙ"): bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺࠧᘚ"),
        bstack111ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨᘛ"): test.name,
        bstack111ll11_opy_ (u"ࠫࡧࡵࡤࡺࠩᘜ"): {
            bstack111ll11_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᘝ"): bstack111ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᘞ"),
            bstack111ll11_opy_ (u"ࠧࡤࡱࡧࡩࠬᘟ"): inspect.getsource(test.obj)
        },
        bstack111ll11_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᘠ"): test.name,
        bstack111ll11_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᘡ"): test.name,
        bstack111ll11_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᘢ"): bstack1ll1l1llll_opy_.bstack1l11111lll_opy_(test),
        bstack111ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᘣ"): file_path,
        bstack111ll11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᘤ"): file_path,
        bstack111ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᘥ"): bstack111ll11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᘦ"),
        bstack111ll11_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᘧ"): file_path,
        bstack111ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᘨ"): bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᘩ")],
        bstack111ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᘪ"): bstack111ll11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᘫ"),
        bstack111ll11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᘬ"): {
            bstack111ll11_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᘭ"): test.nodeid
        },
        bstack111ll11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᘮ"): bstack11ll111111_opy_(test.own_markers)
    }
    if bstack1lll1l111_opy_ in [bstack111ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᘯ"), bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᘰ")]:
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᘱ")] = {
            bstack111ll11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᘲ"): bstack1l11l1l1l1_opy_.get(bstack111ll11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᘳ"), [])
        }
    if bstack1lll1l111_opy_ == bstack111ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᘴ"):
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᘵ")] = bstack111ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᘶ")
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᘷ")] = bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᘸ")]
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᘹ")] = bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᘺ")]
    if result:
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᘻ")] = result.outcome
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᘼ")] = result.duration * 1000
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᘽ")] = bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘾ")]
        if result.failed:
            bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᘿ")] = bstack1ll1l1llll_opy_.bstack11llll1l1l_opy_(call.excinfo.typename)
            bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᙀ")] = bstack1ll1l1llll_opy_.bstack1lllllll111_opy_(call.excinfo, result)
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᙁ")] = bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᙂ")]
    if outcome:
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᙃ")] = bstack11l1ll1l11_opy_(outcome)
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᙄ")] = 0
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᙅ")] = bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᙆ")]
        if bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᙇ")] == bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᙈ"):
            bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᙉ")] = bstack111ll11_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩᙊ")  # bstack1lllll1ll11_opy_
            bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᙋ")] = [{bstack111ll11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᙌ"): [bstack111ll11_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨᙍ")]}]
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᙎ")] = bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᙏ")]
    return bstack1l11l111ll_opy_
def bstack1lllll1l1ll_opy_(test, bstack1l1111llll_opy_, bstack1lll1l111_opy_, result, call, outcome, bstack1lllll1ll1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l1111llll_opy_[bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᙐ")]
    hook_name = bstack1l1111llll_opy_[bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᙑ")]
    hook_data = {
        bstack111ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᙒ"): bstack1l1111llll_opy_[bstack111ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᙓ")],
        bstack111ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩᙔ"): bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᙕ"),
        bstack111ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙖ"): bstack111ll11_opy_ (u"ࠧࡼࡿࠪᙗ").format(bstack1111ll1ll1_opy_(hook_name)),
        bstack111ll11_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᙘ"): {
            bstack111ll11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᙙ"): bstack111ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᙚ"),
            bstack111ll11_opy_ (u"ࠫࡨࡵࡤࡦࠩᙛ"): None
        },
        bstack111ll11_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᙜ"): test.name,
        bstack111ll11_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᙝ"): bstack1ll1l1llll_opy_.bstack1l11111lll_opy_(test, hook_name),
        bstack111ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᙞ"): file_path,
        bstack111ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᙟ"): file_path,
        bstack111ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᙠ"): bstack111ll11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᙡ"),
        bstack111ll11_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᙢ"): file_path,
        bstack111ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᙣ"): bstack1l1111llll_opy_[bstack111ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᙤ")],
        bstack111ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᙥ"): bstack111ll11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᙦ") if bstack1lllll1l11l_opy_ == bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᙧ") else bstack111ll11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᙨ"),
        bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᙩ"): hook_type
    }
    bstack1llll1ll11l_opy_ = bstack1l11lll1l1_opy_(_1l11l1ll1l_opy_.get(test.nodeid, None))
    if bstack1llll1ll11l_opy_:
        hook_data[bstack111ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪᙪ")] = bstack1llll1ll11l_opy_
    if result:
        hook_data[bstack111ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᙫ")] = result.outcome
        hook_data[bstack111ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᙬ")] = result.duration * 1000
        hook_data[bstack111ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᙭")] = bstack1l1111llll_opy_[bstack111ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᙮")]
        if result.failed:
            hook_data[bstack111ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᙯ")] = bstack1ll1l1llll_opy_.bstack11llll1l1l_opy_(call.excinfo.typename)
            hook_data[bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᙰ")] = bstack1ll1l1llll_opy_.bstack1lllllll111_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack111ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᙱ")] = bstack11l1ll1l11_opy_(outcome)
        hook_data[bstack111ll11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᙲ")] = 100
        hook_data[bstack111ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᙳ")] = bstack1l1111llll_opy_[bstack111ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᙴ")]
        if hook_data[bstack111ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᙵ")] == bstack111ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᙶ"):
            hook_data[bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᙷ")] = bstack111ll11_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᙸ")  # bstack1lllll1ll11_opy_
            hook_data[bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᙹ")] = [{bstack111ll11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᙺ"): [bstack111ll11_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬᙻ")]}]
    if bstack1lllll1ll1l_opy_:
        hook_data[bstack111ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᙼ")] = bstack1lllll1ll1l_opy_.result
        hook_data[bstack111ll11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᙽ")] = bstack11l1l1l11l_opy_(bstack1l1111llll_opy_[bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᙾ")], bstack1l1111llll_opy_[bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᙿ")])
        hook_data[bstack111ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ ")] = bstack1l1111llll_opy_[bstack111ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᚁ")]
        if hook_data[bstack111ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᚂ")] == bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᚃ"):
            hook_data[bstack111ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᚄ")] = bstack1ll1l1llll_opy_.bstack11llll1l1l_opy_(bstack1lllll1ll1l_opy_.exception_type)
            hook_data[bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᚅ")] = [{bstack111ll11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᚆ"): bstack11l1llllll_opy_(bstack1lllll1ll1l_opy_.exception)}]
    return hook_data
def bstack1lllll11lll_opy_(test, bstack1l11l1l1l1_opy_, bstack1lll1l111_opy_, result=None, call=None, outcome=None):
    bstack1l11l111ll_opy_ = bstack1llll11llll_opy_(test, bstack1l11l1l1l1_opy_, result, call, bstack1lll1l111_opy_, outcome)
    driver = getattr(test, bstack111ll11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᚇ"), None)
    if bstack1lll1l111_opy_ == bstack111ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᚈ") and driver:
        bstack1l11l111ll_opy_[bstack111ll11_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᚉ")] = bstack1ll1l1llll_opy_.bstack1l111l11ll_opy_(driver)
    if bstack1lll1l111_opy_ == bstack111ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᚊ"):
        bstack1lll1l111_opy_ = bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᚋ")
    bstack1l11l1llll_opy_ = {
        bstack111ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᚌ"): bstack1lll1l111_opy_,
        bstack111ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᚍ"): bstack1l11l111ll_opy_
    }
    bstack1ll1l1llll_opy_.bstack1l11ll11l1_opy_(bstack1l11l1llll_opy_)
def bstack1lllll11111_opy_(test, bstack1l11l1l1l1_opy_, bstack1lll1l111_opy_, result=None, call=None, outcome=None, bstack1lllll1ll1l_opy_=None):
    hook_data = bstack1lllll1l1ll_opy_(test, bstack1l11l1l1l1_opy_, bstack1lll1l111_opy_, result, call, outcome, bstack1lllll1ll1l_opy_)
    bstack1l11l1llll_opy_ = {
        bstack111ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᚎ"): bstack1lll1l111_opy_,
        bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᚏ"): hook_data
    }
    bstack1ll1l1llll_opy_.bstack1l11ll11l1_opy_(bstack1l11l1llll_opy_)
def bstack1l11lll1l1_opy_(bstack1l11l1l1l1_opy_):
    if not bstack1l11l1l1l1_opy_:
        return None
    if bstack1l11l1l1l1_opy_.get(bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᚐ"), None):
        return getattr(bstack1l11l1l1l1_opy_[bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᚑ")], bstack111ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᚒ"), None)
    return bstack1l11l1l1l1_opy_.get(bstack111ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩᚓ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1ll1l1llll_opy_.on():
            return
        places = [bstack111ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᚔ"), bstack111ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᚕ"), bstack111ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᚖ")]
        bstack1l11ll1111_opy_ = []
        for bstack1llll1lll1l_opy_ in places:
            records = caplog.get_records(bstack1llll1lll1l_opy_)
            bstack1lllll1l1l1_opy_ = bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᚗ") if bstack1llll1lll1l_opy_ == bstack111ll11_opy_ (u"ࠩࡦࡥࡱࡲࠧᚘ") else bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᚙ")
            bstack1llll1llll1_opy_ = request.node.nodeid + (bstack111ll11_opy_ (u"ࠫࠬᚚ") if bstack1llll1lll1l_opy_ == bstack111ll11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ᚛") else bstack111ll11_opy_ (u"࠭࠭ࠨ᚜") + bstack1llll1lll1l_opy_)
            bstack1llll1ll1l1_opy_ = bstack1l11lll1l1_opy_(_1l11l1ll1l_opy_.get(bstack1llll1llll1_opy_, None))
            if not bstack1llll1ll1l1_opy_:
                continue
            for record in records:
                if bstack11l1l11ll1_opy_(record.message):
                    continue
                bstack1l11ll1111_opy_.append({
                    bstack111ll11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᚝"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack111ll11_opy_ (u"ࠨ࡜ࠪ᚞"),
                    bstack111ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ᚟"): record.levelname,
                    bstack111ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᚠ"): record.message,
                    bstack1lllll1l1l1_opy_: bstack1llll1ll1l1_opy_
                })
        if len(bstack1l11ll1111_opy_) > 0:
            bstack1ll1l1llll_opy_.bstack1l111lllll_opy_(bstack1l11ll1111_opy_)
    except Exception as err:
        print(bstack111ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨᚡ"), str(err))
def bstack1111lllll_opy_(sequence, driver_command, response=None):
    if sequence == bstack111ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᚢ"):
        if driver_command == bstack111ll11_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᚣ"):
            bstack1ll1l1llll_opy_.bstack11lll111_opy_({
                bstack111ll11_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᚤ"): response[bstack111ll11_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧᚥ")],
                bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᚦ"): store[bstack111ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᚧ")]
            })
def bstack1ll1l111ll_opy_():
    global bstack1111l1l1l_opy_
    bstack1ll1l1llll_opy_.bstack1l11111l1l_opy_()
    for driver in bstack1111l1l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1ll111_opy_(*args):
    global bstack1111l1l1l_opy_
    bstack1ll1l1llll_opy_.bstack1l11111l1l_opy_()
    for driver in bstack1111l1l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1l1ll1l1_opy_(self, *args, **kwargs):
    bstack1ll11lllll_opy_ = bstack1ll11l111_opy_(self, *args, **kwargs)
    bstack1ll1l1llll_opy_.bstack1l1ll1l11l_opy_(self)
    return bstack1ll11lllll_opy_
def bstack1lll1lll_opy_(framework_name):
    global bstack1lll11l11_opy_
    global bstack1ll11l11l_opy_
    bstack1lll11l11_opy_ = framework_name
    logger.info(bstack11lllll1_opy_.format(bstack1lll11l11_opy_.split(bstack111ll11_opy_ (u"ࠫ࠲࠭ᚨ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l1ll11ll_opy_():
            Service.start = bstack1ll1111l1_opy_
            Service.stop = bstack1lll1l1l1l_opy_
            webdriver.Remote.__init__ = bstack1llllll11_opy_
            webdriver.Remote.get = bstack1lllll1ll1_opy_
            if not isinstance(os.getenv(bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ᚩ")), str):
                return
            WebDriver.close = bstack1llll11111_opy_
            WebDriver.quit = bstack1lll1l1l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1l1ll1l111_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1llll1ll_opy_ = getAccessibilityResultsSummary
        if not bstack11l1ll11ll_opy_() and bstack1ll1l1llll_opy_.on():
            webdriver.Remote.__init__ = bstack1l1l1ll1l1_opy_
        bstack1ll11l11l_opy_ = True
    except Exception as e:
        pass
    bstack1ll1l1lll1_opy_()
    if os.environ.get(bstack111ll11_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᚪ")):
        bstack1ll11l11l_opy_ = eval(os.environ.get(bstack111ll11_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᚫ")))
    if not bstack1ll11l11l_opy_:
        bstack1l1111l11_opy_(bstack111ll11_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥᚬ"), bstack11llll1l1_opy_)
    if bstack1l1l1lllll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1111111ll_opy_
        except Exception as e:
            logger.error(bstack1l11ll11_opy_.format(str(e)))
    if bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᚭ") in str(framework_name).lower():
        if not bstack11l1ll11ll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll11l1l1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l11l11ll_opy_
            Config.getoption = bstack11ll1111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1lll1l11ll_opy_
        except Exception as e:
            pass
def bstack1lll1l1l1_opy_(self):
    global bstack1lll11l11_opy_
    global bstack1l1l1l1l1l_opy_
    global bstack1111l11l_opy_
    try:
        if bstack111ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᚮ") in bstack1lll11l11_opy_ and self.session_id != None and bstack1ll1ll1ll_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᚯ"), bstack111ll11_opy_ (u"ࠬ࠭ᚰ")) != bstack111ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᚱ"):
            bstack11l11111l_opy_ = bstack111ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᚲ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᚳ")
            bstack1l1ll1111_opy_(logger, True)
            if self != None:
                bstack11llll11_opy_(self, bstack11l11111l_opy_, bstack111ll11_opy_ (u"ࠩ࠯ࠤࠬᚴ").join(threading.current_thread().bstackTestErrorMessages))
        threading.current_thread().testStatus = bstack111ll11_opy_ (u"ࠪࠫᚵ")
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧᚶ") + str(e))
    bstack1111l11l_opy_(self)
    self.session_id = None
def bstack1llllll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1l1l1l1l_opy_
    global bstack1l1l111l_opy_
    global bstack1ll1l11l_opy_
    global bstack1lll11l11_opy_
    global bstack1ll11l111_opy_
    global bstack1111l1l1l_opy_
    global bstack1l1lll1l1l_opy_
    global bstack1l1l1l1ll1_opy_
    global bstack1llll1l1lll_opy_
    global bstack1l11lll1_opy_
    CONFIG[bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᚷ")] = str(bstack1lll11l11_opy_) + str(__version__)
    command_executor = bstack1l11ll1l1_opy_(bstack1l1lll1l1l_opy_)
    logger.debug(bstack11l1l11l1_opy_.format(command_executor))
    proxy = bstack1ll1lll1_opy_(CONFIG, proxy)
    bstack1ll1l1ll_opy_ = 0
    try:
        if bstack1ll1l11l_opy_ is True:
            bstack1ll1l1ll_opy_ = int(os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᚸ")))
    except:
        bstack1ll1l1ll_opy_ = 0
    bstack1ll1llll1_opy_ = bstack111111l1l_opy_(CONFIG, bstack1ll1l1ll_opy_)
    logger.debug(bstack1llll1lll1_opy_.format(str(bstack1ll1llll1_opy_)))
    bstack1l11lll1_opy_ = CONFIG.get(bstack111ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᚹ"))[bstack1ll1l1ll_opy_]
    if bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᚺ") in CONFIG and CONFIG[bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᚻ")]:
        bstack1ll1l11l1_opy_(bstack1ll1llll1_opy_, bstack1l1l1l1ll1_opy_)
    if desired_capabilities:
        bstack1ll111l11l_opy_ = bstack11l1lllll_opy_(desired_capabilities)
        bstack1ll111l11l_opy_[bstack111ll11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᚼ")] = bstack1ll111111_opy_(CONFIG)
        bstack1lll1llll1_opy_ = bstack111111l1l_opy_(bstack1ll111l11l_opy_)
        if bstack1lll1llll1_opy_:
            bstack1ll1llll1_opy_ = update(bstack1lll1llll1_opy_, bstack1ll1llll1_opy_)
        desired_capabilities = None
    if options:
        bstack1lll11l111_opy_(options, bstack1ll1llll1_opy_)
    if not options:
        options = bstack1ll1l1ll11_opy_(bstack1ll1llll1_opy_)
    if bstack1llll111ll_opy_.bstack1ll111l1l_opy_(CONFIG, bstack1ll1l1ll_opy_) and bstack1llll111ll_opy_.bstack1l11lll11_opy_(bstack1ll1llll1_opy_, options):
        bstack1llll1l1lll_opy_ = True
        bstack1llll111ll_opy_.set_capabilities(bstack1ll1llll1_opy_, CONFIG)
    if proxy and bstack1llll11ll1_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᚽ")):
        options.proxy(proxy)
    if options and bstack1llll11ll1_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᚾ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1llll11ll1_opy_() < version.parse(bstack111ll11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᚿ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1llll1_opy_)
    logger.info(bstack1lll11ll1l_opy_)
    if bstack1llll11ll1_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᛀ")):
        bstack1ll11l111_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll11ll1_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᛁ")):
        bstack1ll11l111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll11ll1_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩᛂ")):
        bstack1ll11l111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1ll11l111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1lll11ll11_opy_ = bstack111ll11_opy_ (u"ࠪࠫᛃ")
        if bstack1llll11ll1_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬᛄ")):
            bstack1lll11ll11_opy_ = self.caps.get(bstack111ll11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧᛅ"))
        else:
            bstack1lll11ll11_opy_ = self.capabilities.get(bstack111ll11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᛆ"))
        if bstack1lll11ll11_opy_:
            bstack1ll1l1l1ll_opy_(bstack1lll11ll11_opy_)
            if bstack1llll11ll1_opy_() <= version.parse(bstack111ll11_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᛇ")):
                self.command_executor._url = bstack111ll11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᛈ") + bstack1l1lll1l1l_opy_ + bstack111ll11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᛉ")
            else:
                self.command_executor._url = bstack111ll11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᛊ") + bstack1lll11ll11_opy_ + bstack111ll11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᛋ")
            logger.debug(bstack111l1ll11_opy_.format(bstack1lll11ll11_opy_))
        else:
            logger.debug(bstack1l1lllll1l_opy_.format(bstack111ll11_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨᛌ")))
    except Exception as e:
        logger.debug(bstack1l1lllll1l_opy_.format(e))
    bstack1l1l1l1l1l_opy_ = self.session_id
    if bstack111ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᛍ") in bstack1lll11l11_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1ll1l1llll_opy_.bstack1l1ll1l11l_opy_(self)
    bstack1111l1l1l_opy_.append(self)
    if bstack111ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᛎ") in CONFIG and bstack111ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᛏ") in CONFIG[bstack111ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᛐ")][bstack1ll1l1ll_opy_]:
        bstack1l1l111l_opy_ = CONFIG[bstack111ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᛑ")][bstack1ll1l1ll_opy_][bstack111ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᛒ")]
    logger.debug(bstack1l1llll111_opy_.format(bstack1l1l1l1l1l_opy_))
def bstack1lllll1ll1_opy_(self, url):
    global bstack1ll1lll1ll_opy_
    global CONFIG
    try:
        bstack1l1ll1lll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1l1l1111_opy_.format(str(err)))
    try:
        bstack1ll1lll1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack11ll1111l_opy_ = str(e)
            if any(err_msg in bstack11ll1111l_opy_ for err_msg in bstack1lll1lll1_opy_):
                bstack1l1ll1lll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1l1l1111_opy_.format(str(err)))
        raise e
def bstack1l1lll11l_opy_(item, when):
    global bstack11l1ll111_opy_
    try:
        bstack11l1ll111_opy_(item, when)
    except Exception as e:
        pass
def bstack1lll1l11ll_opy_(item, call, rep):
    global bstack111l1lll1_opy_
    global bstack1111l1l1l_opy_
    name = bstack111ll11_opy_ (u"ࠬ࠭ᛓ")
    try:
        if rep.when == bstack111ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᛔ"):
            bstack1l1l1l1l1l_opy_ = threading.current_thread().bstackSessionId
            bstack1lllll1llll_opy_ = item.config.getoption(bstack111ll11_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᛕ"))
            try:
                if (str(bstack1lllll1llll_opy_).lower() != bstack111ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᛖ")):
                    name = str(rep.nodeid)
                    bstack1llll1l1l_opy_ = bstack11l1ll1ll_opy_(bstack111ll11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᛗ"), name, bstack111ll11_opy_ (u"ࠪࠫᛘ"), bstack111ll11_opy_ (u"ࠫࠬᛙ"), bstack111ll11_opy_ (u"ࠬ࠭ᛚ"), bstack111ll11_opy_ (u"࠭ࠧᛛ"))
                    os.environ[bstack111ll11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᛜ")] = name
                    for driver in bstack1111l1l1l_opy_:
                        if bstack1l1l1l1l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1llll1l1l_opy_)
            except Exception as e:
                logger.debug(bstack111ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨᛝ").format(str(e)))
            try:
                bstack11ll1l11l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack111ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᛞ"):
                    status = bstack111ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᛟ") if rep.outcome.lower() == bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᛠ") else bstack111ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᛡ")
                    reason = bstack111ll11_opy_ (u"࠭ࠧᛢ")
                    if status == bstack111ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᛣ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack111ll11_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᛤ") if status == bstack111ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᛥ") else bstack111ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᛦ")
                    data = name + bstack111ll11_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ᛧ") if status == bstack111ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᛨ") else name + bstack111ll11_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩᛩ") + reason
                    bstack1lllll11_opy_ = bstack11l1ll1ll_opy_(bstack111ll11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᛪ"), bstack111ll11_opy_ (u"ࠨࠩ᛫"), bstack111ll11_opy_ (u"ࠩࠪ᛬"), bstack111ll11_opy_ (u"ࠪࠫ᛭"), level, data)
                    for driver in bstack1111l1l1l_opy_:
                        if bstack1l1l1l1l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1lllll11_opy_)
            except Exception as e:
                logger.debug(bstack111ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨᛮ").format(str(e)))
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩᛯ").format(str(e)))
    bstack111l1lll1_opy_(item, call, rep)
notset = Notset()
def bstack11ll1111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1llll11l_opy_
    if str(name).lower() == bstack111ll11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ᛰ"):
        return bstack111ll11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨᛱ")
    else:
        return bstack1l1llll11l_opy_(self, name, default, skip)
def bstack1111111ll_opy_(self):
    global CONFIG
    global bstack1llll1ll1l_opy_
    try:
        proxy = bstack11111ll1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack111ll11_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ᛲ")):
                proxies = bstack1ll1l1l1l1_opy_(proxy, bstack1l11ll1l1_opy_())
                if len(proxies) > 0:
                    protocol, bstack111l1llll_opy_ = proxies.popitem()
                    if bstack111ll11_opy_ (u"ࠤ࠽࠳࠴ࠨᛳ") in bstack111l1llll_opy_:
                        return bstack111l1llll_opy_
                    else:
                        return bstack111ll11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᛴ") + bstack111l1llll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack111ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣᛵ").format(str(e)))
    return bstack1llll1ll1l_opy_(self)
def bstack1l1l1lllll_opy_():
    return (bstack111ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᛶ") in CONFIG or bstack111ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᛷ") in CONFIG) and bstack1111l111l_opy_() and bstack1llll11ll1_opy_() >= version.parse(
        bstack1ll1111111_opy_)
def bstack1l1l1ll11l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1l111l_opy_
    global bstack1ll1l11l_opy_
    global bstack1lll11l11_opy_
    CONFIG[bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᛸ")] = str(bstack1lll11l11_opy_) + str(__version__)
    bstack1ll1l1ll_opy_ = 0
    try:
        if bstack1ll1l11l_opy_ is True:
            bstack1ll1l1ll_opy_ = int(os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᛹")))
    except:
        bstack1ll1l1ll_opy_ = 0
    CONFIG[bstack111ll11_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ᛺")] = True
    bstack1ll1llll1_opy_ = bstack111111l1l_opy_(CONFIG, bstack1ll1l1ll_opy_)
    logger.debug(bstack1llll1lll1_opy_.format(str(bstack1ll1llll1_opy_)))
    if CONFIG.get(bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ᛻")):
        bstack1ll1l11l1_opy_(bstack1ll1llll1_opy_, bstack1l1l1l1ll1_opy_)
    if bstack111ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᛼") in CONFIG and bstack111ll11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᛽") in CONFIG[bstack111ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᛾")][bstack1ll1l1ll_opy_]:
        bstack1l1l111l_opy_ = CONFIG[bstack111ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᛿")][bstack1ll1l1ll_opy_][bstack111ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᜀ")]
    import urllib
    import json
    bstack1ll11l1l_opy_ = bstack111ll11_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫᜁ") + urllib.parse.quote(json.dumps(bstack1ll1llll1_opy_))
    browser = self.connect(bstack1ll11l1l_opy_)
    return browser
def bstack1ll1l1lll1_opy_():
    global bstack1ll11l11l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1l1ll11l_opy_
        bstack1ll11l11l_opy_ = True
    except Exception as e:
        pass
def bstack1lllll11l1l_opy_():
    global CONFIG
    global bstack11l1l11l_opy_
    global bstack1l1lll1l1l_opy_
    global bstack1l1l1l1ll1_opy_
    global bstack1ll1l11l_opy_
    CONFIG = json.loads(os.environ.get(bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩᜂ")))
    bstack11l1l11l_opy_ = eval(os.environ.get(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᜃ")))
    bstack1l1lll1l1l_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬᜄ"))
    bstack1l11l1ll1_opy_(CONFIG, bstack11l1l11l_opy_)
    bstack1l111ll1l_opy_()
    global bstack1ll11l111_opy_
    global bstack1111l11l_opy_
    global bstack1llll11l_opy_
    global bstack111111111_opy_
    global bstack1l1lll1l_opy_
    global bstack11l1l111_opy_
    global bstack1lll11l1_opy_
    global bstack1ll1lll1ll_opy_
    global bstack1llll1ll1l_opy_
    global bstack1l1llll11l_opy_
    global bstack11l1ll111_opy_
    global bstack111l1lll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1ll11l111_opy_ = webdriver.Remote.__init__
        bstack1111l11l_opy_ = WebDriver.quit
        bstack1lll11l1_opy_ = WebDriver.close
        bstack1ll1lll1ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack111ll11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᜅ") in CONFIG or bstack111ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᜆ") in CONFIG) and bstack1111l111l_opy_():
        if bstack1llll11ll1_opy_() < version.parse(bstack1ll1111111_opy_):
            logger.error(bstack1lllllll1_opy_.format(bstack1llll11ll1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1llll1ll1l_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1l11ll11_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1llll11l_opy_ = Config.getoption
        from _pytest import runner
        bstack11l1ll111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack111l111ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack111l1lll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩᜇ"))
    bstack1l1l1l1ll1_opy_ = CONFIG.get(bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜈ"), {}).get(bstack111ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᜉ"))
    bstack1ll1l11l_opy_ = True
    bstack1lll1lll_opy_(bstack1ll1ll1l11_opy_)
if (bstack11l1lllll1_opy_()):
    bstack1lllll11l1l_opy_()
@bstack1l11lll1ll_opy_(class_method=False)
def bstack1lllll1lll1_opy_(hook_name, event, bstack1llll1lll11_opy_=None):
    if hook_name not in [bstack111ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᜊ"), bstack111ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᜋ"), bstack111ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᜌ"), bstack111ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᜍ"), bstack111ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᜎ"), bstack111ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᜏ"), bstack111ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᜐ"), bstack111ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᜑ")]:
        return
    node = store[bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᜒ")]
    if hook_name in [bstack111ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᜓ"), bstack111ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦ᜔ࠩ")]:
        node = store[bstack111ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳ᜕ࠧ")]
    elif hook_name in [bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ᜖"), bstack111ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ᜗")]:
        node = store[bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ᜘")]
    if event == bstack111ll11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ᜙"):
        hook_type = bstack1111ll11l1_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l1111llll_opy_ = {
            bstack111ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᜚"): uuid,
            bstack111ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᜛"): bstack111l11ll1_opy_(),
            bstack111ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭᜜"): bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ᜝"),
            bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭᜞"): hook_type,
            bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᜟ"): hook_name
        }
        store[bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᜠ")].append(uuid)
        bstack1lllll111ll_opy_ = node.nodeid
        if hook_type == bstack111ll11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᜡ"):
            if not _1l11l1ll1l_opy_.get(bstack1lllll111ll_opy_, None):
                _1l11l1ll1l_opy_[bstack1lllll111ll_opy_] = {bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᜢ"): []}
            _1l11l1ll1l_opy_[bstack1lllll111ll_opy_][bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᜣ")].append(bstack1l1111llll_opy_[bstack111ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᜤ")])
        _1l11l1ll1l_opy_[bstack1lllll111ll_opy_ + bstack111ll11_opy_ (u"ࠪ࠱ࠬᜥ") + hook_name] = bstack1l1111llll_opy_
        bstack1lllll11111_opy_(node, bstack1l1111llll_opy_, bstack111ll11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᜦ"))
    elif event == bstack111ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᜧ"):
        bstack1l11l1l111_opy_ = node.nodeid + bstack111ll11_opy_ (u"࠭࠭ࠨᜨ") + hook_name
        _1l11l1ll1l_opy_[bstack1l11l1l111_opy_][bstack111ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᜩ")] = bstack111l11ll1_opy_()
        bstack1lllll1l111_opy_(_1l11l1ll1l_opy_[bstack1l11l1l111_opy_][bstack111ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᜪ")])
        bstack1lllll11111_opy_(node, _1l11l1ll1l_opy_[bstack1l11l1l111_opy_], bstack111ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᜫ"), bstack1lllll1ll1l_opy_=bstack1llll1lll11_opy_)
def bstack1lllll11ll1_opy_():
    global bstack1lllll1l11l_opy_
    if bstack1ll11l1l1l_opy_():
        bstack1lllll1l11l_opy_ = bstack111ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᜬ")
    else:
        bstack1lllll1l11l_opy_ = bstack111ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᜭ")
@bstack1ll1l1llll_opy_.bstack1llllll1lll_opy_
def bstack1llll1l1l1l_opy_():
    bstack1lllll11ll1_opy_()
    if bstack1111l111l_opy_():
        bstack1ll1lll111_opy_(bstack1111lllll_opy_)
    bstack11l11l111l_opy_ = bstack11l111ll11_opy_(bstack1lllll1lll1_opy_)
bstack1llll1l1l1l_opy_()