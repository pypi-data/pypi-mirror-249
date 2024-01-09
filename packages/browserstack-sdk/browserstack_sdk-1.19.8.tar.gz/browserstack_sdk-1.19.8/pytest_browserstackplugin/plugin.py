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
from browserstack_sdk.__init__ import (bstack1l11111ll_opy_, bstack1l111111_opy_, update, bstack1111l11l1_opy_,
                                       bstack1llllll1ll_opy_, bstack11llll111_opy_, bstack1llll1l111_opy_, bstack1l11l1l1l_opy_,
                                       bstack11ll1l1ll_opy_, bstack1l1l1l1l11_opy_, bstack1ll111llll_opy_, bstack11l1111l1_opy_,
                                       bstack1llll11lll_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l11lll1ll_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1lllll111_opy_, bstack1llllllll1_opy_, bstack1111ll11_opy_, bstack111lll1ll_opy_, \
    bstack11ll1ll11_opy_
from bstack_utils.helper import bstack1lllll1l11_opy_, bstack1111l1lll_opy_, bstack11ll111l1l_opy_, bstack111l11lll_opy_, \
    bstack11l1l1ll11_opy_, \
    bstack11l1llll1l_opy_, bstack1l1l11lll1_opy_, bstack1l111ll1_opy_, bstack11ll11l111_opy_, bstack1ll1l111l1_opy_, Notset, \
    bstack1l1l11l11l_opy_, bstack11l1l1l11l_opy_, bstack11l1ll1l11_opy_, Result, bstack11ll111111_opy_, bstack11ll11111l_opy_, bstack1l11111lll_opy_, \
    bstack1ll1111ll_opy_, bstack1l1ll1l1_opy_, bstack11l1l11l1_opy_, bstack11l1l1l111_opy_
from bstack_utils.bstack11l111ll1l_opy_ import bstack11l11l11l1_opy_
from bstack_utils.messages import bstack11ll1ll1l_opy_, bstack1l1111ll1_opy_, bstack1ll1l1l1l_opy_, bstack1111llll_opy_, bstack11l11lll_opy_, \
    bstack1ll11l1111_opy_, bstack11ll11ll1_opy_, bstack1llll11l1_opy_, bstack1lll1lll_opy_, bstack111ll11ll_opy_, \
    bstack111l11111_opy_, bstack11l1llll1_opy_
from bstack_utils.proxy import bstack1l1ll11l1l_opy_, bstack1ll111111_opy_
from bstack_utils.bstack1111lll1_opy_ import bstack1111lll111_opy_, bstack1111ll1lll_opy_, bstack1111ll1l11_opy_, bstack1111l1llll_opy_, \
    bstack1111ll111l_opy_, bstack1111l1lll1_opy_, bstack1111l1ll1l_opy_, bstack1ll1111l1_opy_, bstack1111l1ll11_opy_
from bstack_utils.bstack111111l1_opy_ import bstack1l1ll1l11_opy_
from bstack_utils.bstack1ll11ll11l_opy_ import bstack11lll111_opy_, bstack1llll1l1l1_opy_, bstack11l1ll1ll_opy_, \
    bstack1lll1l11l1_opy_, bstack1lll11l1l_opy_
from bstack_utils.bstack1l11l1lll1_opy_ import bstack1l111l1ll1_opy_
from bstack_utils.bstack11l1ll11l_opy_ import bstack1ll1llll1l_opy_
import bstack_utils.bstack1lll1llll1_opy_ as bstack1111ll111_opy_
bstack11l1ll1l_opy_ = None
bstack1ll1lll111_opy_ = None
bstack1l1ll1lll1_opy_ = None
bstack1ll11ll111_opy_ = None
bstack11l11l11_opy_ = None
bstack1llll11ll1_opy_ = None
bstack1llllll11l_opy_ = None
bstack1llll1ll1l_opy_ = None
bstack1l1l1l1ll_opy_ = None
bstack1l1lll111l_opy_ = None
bstack1lll1lll1_opy_ = None
bstack11ll11l1_opy_ = None
bstack1lll1l11ll_opy_ = None
bstack1l1ll1ll11_opy_ = bstack11lllll_opy_ (u"ࠧࠨᔱ")
CONFIG = {}
bstack1ll11ll11_opy_ = False
bstack111ll1l1_opy_ = bstack11lllll_opy_ (u"ࠨࠩᔲ")
bstack1ll11111l_opy_ = bstack11lllll_opy_ (u"ࠩࠪᔳ")
bstack1ll1l11ll_opy_ = False
bstack1lll11l1ll_opy_ = []
bstack1lllll11_opy_ = bstack1llllllll1_opy_
bstack1lllll111ll_opy_ = bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᔴ")
bstack1lllll1ll1l_opy_ = False
bstack1l1l11l1l1_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1lllll11_opy_,
                    format=bstack11lllll_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩᔵ"),
                    datefmt=bstack11lllll_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧᔶ"),
                    stream=sys.stdout)
store = {
    bstack11lllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᔷ"): []
}
bstack1llll1l1lll_opy_ = False
def bstack111l1lll_opy_():
    global CONFIG
    global bstack1lllll11_opy_
    if bstack11lllll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᔸ") in CONFIG:
        bstack1lllll11_opy_ = bstack1lllll111_opy_[CONFIG[bstack11lllll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᔹ")]]
        logging.getLogger().setLevel(bstack1lllll11_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l1l11111l_opy_ = {}
current_test_uuid = None
def bstack1l1ll1111_opy_(page, bstack1lll11ll1l_opy_):
    try:
        page.evaluate(bstack11lllll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᔺ"),
                      bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧᔻ") + json.dumps(
                          bstack1lll11ll1l_opy_) + bstack11lllll_opy_ (u"ࠦࢂࢃࠢᔼ"))
    except Exception as e:
        print(bstack11lllll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥᔽ"), e)
def bstack1ll11111ll_opy_(page, message, level):
    try:
        page.evaluate(bstack11lllll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᔾ"), bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬᔿ") + json.dumps(
            message) + bstack11lllll_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫᕀ") + json.dumps(level) + bstack11lllll_opy_ (u"ࠩࢀࢁࠬᕁ"))
    except Exception as e:
        print(bstack11lllll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨᕂ"), e)
def pytest_configure(config):
    bstack1lll11111_opy_ = Config.get_instance()
    config.args = bstack1ll1llll1l_opy_.bstack1llllll1l11_opy_(config.args)
    bstack1lll11111_opy_.bstack11l11111l_opy_(bstack11l1l11l1_opy_(config.getoption(bstack11lllll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᕃ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lllll1111l_opy_ = item.config.getoption(bstack11lllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᕄ"))
    plugins = item.config.getoption(bstack11lllll_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢᕅ"))
    report = outcome.get_result()
    bstack1llll11llll_opy_(item, call, report)
    if bstack11lllll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧᕆ") not in plugins or bstack1ll1l111l1_opy_():
        return
    summary = []
    driver = getattr(item, bstack11lllll_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤᕇ"), None)
    page = getattr(item, bstack11lllll_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣᕈ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1llll1l11l1_opy_(item, report, summary, bstack1lllll1111l_opy_)
    if (page is not None):
        bstack1lllll11ll1_opy_(item, report, summary, bstack1lllll1111l_opy_)
def bstack1llll1l11l1_opy_(item, report, summary, bstack1lllll1111l_opy_):
    if report.when == bstack11lllll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᕉ") and report.skipped:
        bstack1111l1ll11_opy_(report)
    if report.when in [bstack11lllll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᕊ"), bstack11lllll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᕋ")]:
        return
    if not bstack11ll111l1l_opy_():
        return
    try:
        if (str(bstack1lllll1111l_opy_).lower() != bstack11lllll_opy_ (u"࠭ࡴࡳࡷࡨࠫᕌ")):
            item._driver.execute_script(
                bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬᕍ") + json.dumps(
                    report.nodeid) + bstack11lllll_opy_ (u"ࠨࡿࢀࠫᕎ"))
        os.environ[bstack11lllll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᕏ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11lllll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥᕐ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11lllll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᕑ")))
    bstack1ll1llll1_opy_ = bstack11lllll_opy_ (u"ࠧࠨᕒ")
    bstack1111l1ll11_opy_(report)
    if not passed:
        try:
            bstack1ll1llll1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11lllll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᕓ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1llll1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11lllll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᕔ")))
        bstack1ll1llll1_opy_ = bstack11lllll_opy_ (u"ࠣࠤᕕ")
        if not passed:
            try:
                bstack1ll1llll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11lllll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᕖ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1llll1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᕗ")
                    + json.dumps(bstack11lllll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧᕘ"))
                    + bstack11lllll_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᕙ")
                )
            else:
                item._driver.execute_script(
                    bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᕚ")
                    + json.dumps(str(bstack1ll1llll1_opy_))
                    + bstack11lllll_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥᕛ")
                )
        except Exception as e:
            summary.append(bstack11lllll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨᕜ").format(e))
def bstack1llll1l111l_opy_(test_name, error_message):
    try:
        bstack1llll11lll1_opy_ = []
        bstack11lllll1l_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᕝ"), bstack11lllll_opy_ (u"ࠪ࠴ࠬᕞ"))
        bstack1l11l11l_opy_ = {bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᕟ"): test_name, bstack11lllll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᕠ"): error_message, bstack11lllll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᕡ"): bstack11lllll1l_opy_}
        bstack1llll1ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᕢ"))
        if os.path.exists(bstack1llll1ll111_opy_):
            with open(bstack1llll1ll111_opy_) as f:
                bstack1llll11lll1_opy_ = json.load(f)
        bstack1llll11lll1_opy_.append(bstack1l11l11l_opy_)
        with open(bstack1llll1ll111_opy_, bstack11lllll_opy_ (u"ࠨࡹࠪᕣ")) as f:
            json.dump(bstack1llll11lll1_opy_, f)
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧᕤ") + str(e))
def bstack1lllll11ll1_opy_(item, report, summary, bstack1lllll1111l_opy_):
    if report.when in [bstack11lllll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᕥ"), bstack11lllll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᕦ")]:
        return
    if (str(bstack1lllll1111l_opy_).lower() != bstack11lllll_opy_ (u"ࠬࡺࡲࡶࡧࠪᕧ")):
        bstack1l1ll1111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11lllll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᕨ")))
    bstack1ll1llll1_opy_ = bstack11lllll_opy_ (u"ࠢࠣᕩ")
    bstack1111l1ll11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll1llll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11lllll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᕪ").format(e)
                )
        try:
            if passed:
                bstack1lll11l1l_opy_(getattr(item, bstack11lllll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᕫ"), None), bstack11lllll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᕬ"))
            else:
                error_message = bstack11lllll_opy_ (u"ࠫࠬᕭ")
                if bstack1ll1llll1_opy_:
                    bstack1ll11111ll_opy_(item._page, str(bstack1ll1llll1_opy_), bstack11lllll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᕮ"))
                    bstack1lll11l1l_opy_(getattr(item, bstack11lllll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᕯ"), None), bstack11lllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᕰ"), str(bstack1ll1llll1_opy_))
                    error_message = str(bstack1ll1llll1_opy_)
                else:
                    bstack1lll11l1l_opy_(getattr(item, bstack11lllll_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᕱ"), None), bstack11lllll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᕲ"))
                bstack1llll1l111l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11lllll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢᕳ").format(e))
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
    parser.addoption(bstack11lllll_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᕴ"), default=bstack11lllll_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᕵ"), help=bstack11lllll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧᕶ"))
    parser.addoption(bstack11lllll_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᕷ"), default=bstack11lllll_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᕸ"), help=bstack11lllll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᕹ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11lllll_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧᕺ"), action=bstack11lllll_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥᕻ"), default=bstack11lllll_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧᕼ"),
                         help=bstack11lllll_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧᕽ"))
def bstack1l11ll11ll_opy_(log):
    if not (log[bstack11lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᕾ")] and log[bstack11lllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᕿ")].strip()):
        return
    active = bstack1l1111llll_opy_()
    log = {
        bstack11lllll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᖀ"): log[bstack11lllll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᖁ")],
        bstack11lllll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᖂ"): datetime.datetime.utcnow().isoformat() + bstack11lllll_opy_ (u"ࠬࡠࠧᖃ"),
        bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖄ"): log[bstack11lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖅ")],
    }
    if active:
        if active[bstack11lllll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᖆ")] == bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᖇ"):
            log[bstack11lllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖈ")] = active[bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖉ")]
        elif active[bstack11lllll_opy_ (u"ࠬࡺࡹࡱࡧࠪᖊ")] == bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࠫᖋ"):
            log[bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖌ")] = active[bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖍ")]
    bstack1ll1llll1l_opy_.bstack1l11ll1111_opy_([log])
def bstack1l1111llll_opy_():
    if len(store[bstack11lllll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᖎ")]) > 0 and store[bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᖏ")][-1]:
        return {
            bstack11lllll_opy_ (u"ࠫࡹࡿࡰࡦࠩᖐ"): bstack11lllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᖑ"),
            bstack11lllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖒ"): store[bstack11lllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖓ")][-1]
        }
    if store.get(bstack11lllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᖔ"), None):
        return {
            bstack11lllll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᖕ"): bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࠨᖖ"),
            bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖗ"): store[bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᖘ")]
        }
    return None
bstack1l1111ll1l_opy_ = bstack1l11lll1ll_opy_(bstack1l11ll11ll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lllll1ll1l_opy_
        if bstack1lllll1ll1l_opy_:
            driver = getattr(item, bstack11lllll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᖙ"), None)
            bstack1111llll1_opy_ = bstack1111ll111_opy_.bstack11lll1111_opy_(CONFIG, bstack11l1llll1l_opy_(item.own_markers))
            item._a11y_started = bstack1111ll111_opy_.bstack1111l111l_opy_(driver, bstack1111llll1_opy_)
        if not bstack1ll1llll1l_opy_.on() or bstack1lllll111ll_opy_ != bstack11lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᖚ"):
            return
        global current_test_uuid, bstack1l1111ll1l_opy_
        bstack1l1111ll1l_opy_.start()
        bstack1l111l1l11_opy_ = {
            bstack11lllll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᖛ"): uuid4().__str__(),
            bstack11lllll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᖜ"): datetime.datetime.utcnow().isoformat() + bstack11lllll_opy_ (u"ࠪ࡞ࠬᖝ")
        }
        current_test_uuid = bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠫࡺࡻࡩࡥࠩᖞ")]
        store[bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᖟ")] = bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᖠ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l1l11111l_opy_[item.nodeid] = {**_1l1l11111l_opy_[item.nodeid], **bstack1l111l1l11_opy_}
        bstack1lllll1l1ll_opy_(item, _1l1l11111l_opy_[item.nodeid], bstack11lllll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᖡ"))
    except Exception as err:
        print(bstack11lllll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪᖢ"), str(err))
def pytest_runtest_setup(item):
    global bstack1llll1l1lll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11ll11l111_opy_():
        atexit.register(bstack11ll11l11_opy_)
        if not bstack1llll1l1lll_opy_:
            try:
                bstack1llll1ll11l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1l1l111_opy_():
                    bstack1llll1ll11l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llll1ll11l_opy_:
                    signal.signal(s, bstack1llll1l1ll1_opy_)
                bstack1llll1l1lll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥᖣ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1111lll111_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11lllll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᖤ")
    try:
        if not bstack1ll1llll1l_opy_.on():
            return
        bstack1l1111ll1l_opy_.start()
        uuid = uuid4().__str__()
        bstack1l111l1l11_opy_ = {
            bstack11lllll_opy_ (u"ࠫࡺࡻࡩࡥࠩᖥ"): uuid,
            bstack11lllll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᖦ"): datetime.datetime.utcnow().isoformat() + bstack11lllll_opy_ (u"࡚࠭ࠨᖧ"),
            bstack11lllll_opy_ (u"ࠧࡵࡻࡳࡩࠬᖨ"): bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᖩ"),
            bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᖪ"): bstack11lllll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᖫ"),
            bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᖬ"): bstack11lllll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᖭ")
        }
        threading.current_thread().current_hook_uuid = uuid
        store[bstack11lllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᖮ")] = item
        store[bstack11lllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖯ")] = [uuid]
        if not _1l1l11111l_opy_.get(item.nodeid, None):
            _1l1l11111l_opy_[item.nodeid] = {bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᖰ"): [], bstack11lllll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᖱ"): []}
        _1l1l11111l_opy_[item.nodeid][bstack11lllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᖲ")].append(bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠫࡺࡻࡩࡥࠩᖳ")])
        _1l1l11111l_opy_[item.nodeid + bstack11lllll_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬᖴ")] = bstack1l111l1l11_opy_
        bstack1lllll1lll1_opy_(item, bstack1l111l1l11_opy_, bstack11lllll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᖵ"))
    except Exception as err:
        print(bstack11lllll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᖶ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l1l11l1l1_opy_
        if CONFIG.get(bstack11lllll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᖷ"), False):
            if CONFIG.get(bstack11lllll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᖸ"), bstack11lllll_opy_ (u"ࠥࡥࡺࡺ࡯ࠣᖹ")) == bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᖺ"):
                bstack1lllll11l1l_opy_ = bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᖻ"), None)
                bstack111ll111_opy_ = bstack1lllll11l1l_opy_ + bstack11lllll_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤᖼ")
                driver = getattr(item, bstack11lllll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᖽ"), None)
                PercySDK.screenshot(driver, bstack111ll111_opy_)
        if getattr(item, bstack11lllll_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨᖾ"), False):
            logger.info(bstack11lllll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠡࠤᖿ"))
            driver = getattr(item, bstack11lllll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᗀ"), None)
            bstack11lll1111l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1111ll111_opy_.bstack1lll111l11_opy_(driver, bstack11lll1111l_opy_, item.name, item.module.__name__, item.path, bstack1l1l11l1l1_opy_)
        if not bstack1ll1llll1l_opy_.on():
            return
        bstack1l111l1l11_opy_ = {
            bstack11lllll_opy_ (u"ࠫࡺࡻࡩࡥࠩᗁ"): uuid4().__str__(),
            bstack11lllll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᗂ"): datetime.datetime.utcnow().isoformat() + bstack11lllll_opy_ (u"࡚࠭ࠨᗃ"),
            bstack11lllll_opy_ (u"ࠧࡵࡻࡳࡩࠬᗄ"): bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᗅ"),
            bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᗆ"): bstack11lllll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᗇ"),
            bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᗈ"): bstack11lllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᗉ")
        }
        _1l1l11111l_opy_[item.nodeid + bstack11lllll_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᗊ")] = bstack1l111l1l11_opy_
        bstack1lllll1lll1_opy_(item, bstack1l111l1l11_opy_, bstack11lllll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᗋ"))
    except Exception as err:
        print(bstack11lllll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧᗌ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1ll1llll1l_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1111l1llll_opy_(fixturedef.argname):
        store[bstack11lllll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨᗍ")] = request.node
    elif bstack1111ll111l_opy_(fixturedef.argname):
        store[bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨᗎ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᗏ"): fixturedef.argname,
            bstack11lllll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᗐ"): bstack11l1l1ll11_opy_(outcome),
            bstack11lllll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᗑ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack1lllll1l11l_opy_ = store[bstack11lllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᗒ")]
        if not _1l1l11111l_opy_.get(bstack1lllll1l11l_opy_.nodeid, None):
            _1l1l11111l_opy_[bstack1lllll1l11l_opy_.nodeid] = {bstack11lllll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᗓ"): []}
        _1l1l11111l_opy_[bstack1lllll1l11l_opy_.nodeid][bstack11lllll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᗔ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11lllll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᗕ"), str(err))
if bstack1ll1l111l1_opy_() and bstack1ll1llll1l_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l1l11111l_opy_[request.node.nodeid][bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᗖ")].bstack1111111l11_opy_(id(step))
        except Exception as err:
            print(bstack11lllll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪᗗ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l1l11111l_opy_[request.node.nodeid][bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᗘ")].bstack1l1l111l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11lllll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᗙ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l11l1lll1_opy_: bstack1l111l1ll1_opy_ = _1l1l11111l_opy_[request.node.nodeid][bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᗚ")]
            bstack1l11l1lll1_opy_.bstack1l1l111l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11lllll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭ᗛ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lllll111ll_opy_
        try:
            if not bstack1ll1llll1l_opy_.on() or bstack1lllll111ll_opy_ != bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᗜ"):
                return
            global bstack1l1111ll1l_opy_
            bstack1l1111ll1l_opy_.start()
            if not _1l1l11111l_opy_.get(request.node.nodeid, None):
                _1l1l11111l_opy_[request.node.nodeid] = {}
            bstack1l11l1lll1_opy_ = bstack1l111l1ll1_opy_.bstack1111111l1l_opy_(
                scenario, feature, request.node,
                name=bstack1111l1lll1_opy_(request.node, scenario),
                bstack1l1l111111_opy_=bstack111l11lll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11lllll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ᗝ"),
                tags=bstack1111l1ll1l_opy_(feature, scenario)
            )
            _1l1l11111l_opy_[request.node.nodeid][bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᗞ")] = bstack1l11l1lll1_opy_
            bstack1llll1lll11_opy_(bstack1l11l1lll1_opy_.uuid)
            bstack1ll1llll1l_opy_.bstack1l1111l11l_opy_(bstack11lllll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᗟ"), bstack1l11l1lll1_opy_)
        except Exception as err:
            print(bstack11lllll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩᗠ"), str(err))
def bstack1llll1llll1_opy_(bstack1lllll1llll_opy_):
    if bstack1lllll1llll_opy_ in store[bstack11lllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᗡ")]:
        store[bstack11lllll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᗢ")].remove(bstack1lllll1llll_opy_)
def bstack1llll1lll11_opy_(bstack1lllll11111_opy_):
    store[bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᗣ")] = bstack1lllll11111_opy_
    threading.current_thread().current_test_uuid = bstack1lllll11111_opy_
@bstack1ll1llll1l_opy_.bstack1llllll1111_opy_
def bstack1llll11llll_opy_(item, call, report):
    global bstack1lllll111ll_opy_
    bstack1ll1l1111l_opy_ = bstack111l11lll_opy_()
    if hasattr(report, bstack11lllll_opy_ (u"ࠫࡸࡺ࡯ࡱࠩᗤ")):
        bstack1ll1l1111l_opy_ = bstack11ll111111_opy_(report.stop)
    if hasattr(report, bstack11lllll_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫᗥ")):
        bstack1ll1l1111l_opy_ = bstack11ll111111_opy_(report.start)
    try:
        if getattr(report, bstack11lllll_opy_ (u"࠭ࡷࡩࡧࡱࠫᗦ"), bstack11lllll_opy_ (u"ࠧࠨᗧ")) == bstack11lllll_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᗨ"):
            bstack1l1111ll1l_opy_.reset()
        if getattr(report, bstack11lllll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᗩ"), bstack11lllll_opy_ (u"ࠪࠫᗪ")) == bstack11lllll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᗫ"):
            if bstack1lllll111ll_opy_ == bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᗬ"):
                _1l1l11111l_opy_[item.nodeid][bstack11lllll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᗭ")] = bstack1ll1l1111l_opy_
                bstack1lllll1l1ll_opy_(item, _1l1l11111l_opy_[item.nodeid], bstack11lllll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᗮ"), report, call)
                store[bstack11lllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᗯ")] = None
            elif bstack1lllll111ll_opy_ == bstack11lllll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᗰ"):
                bstack1l11l1lll1_opy_ = _1l1l11111l_opy_[item.nodeid][bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᗱ")]
                bstack1l11l1lll1_opy_.set(hooks=_1l1l11111l_opy_[item.nodeid].get(bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᗲ"), []))
                exception, bstack1l11lllll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11lllll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack11lllll_opy_ (u"ࠬࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠫᗳ"), bstack11lllll_opy_ (u"࠭ࠧᗴ"))]
                bstack1l11l1lll1_opy_.stop(time=bstack1ll1l1111l_opy_, result=Result(result=getattr(report, bstack11lllll_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨᗵ"), bstack11lllll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᗶ")), exception=exception, bstack1l11lllll1_opy_=bstack1l11lllll1_opy_))
                bstack1ll1llll1l_opy_.bstack1l1111l11l_opy_(bstack11lllll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᗷ"), _1l1l11111l_opy_[item.nodeid][bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᗸ")])
        elif getattr(report, bstack11lllll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᗹ"), bstack11lllll_opy_ (u"ࠬ࠭ᗺ")) in [bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᗻ"), bstack11lllll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᗼ")]:
            bstack1l111ll1l1_opy_ = item.nodeid + bstack11lllll_opy_ (u"ࠨ࠯ࠪᗽ") + getattr(report, bstack11lllll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᗾ"), bstack11lllll_opy_ (u"ࠪࠫᗿ"))
            if getattr(report, bstack11lllll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᘀ"), False):
                hook_type = bstack11lllll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᘁ") if getattr(report, bstack11lllll_opy_ (u"࠭ࡷࡩࡧࡱࠫᘂ"), bstack11lllll_opy_ (u"ࠧࠨᘃ")) == bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᘄ") else bstack11lllll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᘅ")
                _1l1l11111l_opy_[bstack1l111ll1l1_opy_] = {
                    bstack11lllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᘆ"): uuid4().__str__(),
                    bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᘇ"): bstack1ll1l1111l_opy_,
                    bstack11lllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᘈ"): hook_type
                }
            _1l1l11111l_opy_[bstack1l111ll1l1_opy_][bstack11lllll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᘉ")] = bstack1ll1l1111l_opy_
            bstack1llll1llll1_opy_(_1l1l11111l_opy_[bstack1l111ll1l1_opy_][bstack11lllll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᘊ")])
            bstack1lllll1lll1_opy_(item, _1l1l11111l_opy_[bstack1l111ll1l1_opy_], bstack11lllll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᘋ"), report, call)
            if getattr(report, bstack11lllll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᘌ"), bstack11lllll_opy_ (u"ࠪࠫᘍ")) == bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᘎ"):
                if getattr(report, bstack11lllll_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭ᘏ"), bstack11lllll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᘐ")) == bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᘑ"):
                    bstack1l111l1l11_opy_ = {
                        bstack11lllll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘒ"): uuid4().__str__(),
                        bstack11lllll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᘓ"): bstack111l11lll_opy_(),
                        bstack11lllll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘔ"): bstack111l11lll_opy_()
                    }
                    _1l1l11111l_opy_[item.nodeid] = {**_1l1l11111l_opy_[item.nodeid], **bstack1l111l1l11_opy_}
                    bstack1lllll1l1ll_opy_(item, _1l1l11111l_opy_[item.nodeid], bstack11lllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᘕ"))
                    bstack1lllll1l1ll_opy_(item, _1l1l11111l_opy_[item.nodeid], bstack11lllll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᘖ"), report, call)
    except Exception as err:
        print(bstack11lllll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫᘗ"), str(err))
def bstack1llll1lllll_opy_(test, bstack1l111l1l11_opy_, result=None, call=None, bstack1ll111ll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l11l1lll1_opy_ = {
        bstack11lllll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᘘ"): bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘙ")],
        bstack11lllll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᘚ"): bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࠨᘛ"),
        bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᘜ"): test.name,
        bstack11lllll_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᘝ"): {
            bstack11lllll_opy_ (u"࠭࡬ࡢࡰࡪࠫᘞ"): bstack11lllll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᘟ"),
            bstack11lllll_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᘠ"): inspect.getsource(test.obj)
        },
        bstack11lllll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᘡ"): test.name,
        bstack11lllll_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᘢ"): test.name,
        bstack11lllll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᘣ"): bstack1ll1llll1l_opy_.bstack1l1111ll11_opy_(test),
        bstack11lllll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᘤ"): file_path,
        bstack11lllll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᘥ"): file_path,
        bstack11lllll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᘦ"): bstack11lllll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᘧ"),
        bstack11lllll_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᘨ"): file_path,
        bstack11lllll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᘩ"): bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᘪ")],
        bstack11lllll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᘫ"): bstack11lllll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᘬ"),
        bstack11lllll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᘭ"): {
            bstack11lllll_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᘮ"): test.nodeid
        },
        bstack11lllll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᘯ"): bstack11l1llll1l_opy_(test.own_markers)
    }
    if bstack1ll111ll_opy_ in [bstack11lllll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᘰ"), bstack11lllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᘱ")]:
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠬࡳࡥࡵࡣࠪᘲ")] = {
            bstack11lllll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᘳ"): bstack1l111l1l11_opy_.get(bstack11lllll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᘴ"), [])
        }
    if bstack1ll111ll_opy_ == bstack11lllll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᘵ"):
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᘶ")] = bstack11lllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᘷ")
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᘸ")] = bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᘹ")]
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᘺ")] = bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᘻ")]
    if result:
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᘼ")] = result.outcome
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᘽ")] = result.duration * 1000
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘾ")] = bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᘿ")]
        if result.failed:
            bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᙀ")] = bstack1ll1llll1l_opy_.bstack11llll1l1l_opy_(call.excinfo.typename)
            bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᙁ")] = bstack1ll1llll1l_opy_.bstack1llllllll1l_opy_(call.excinfo, result)
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᙂ")] = bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᙃ")]
    if outcome:
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᙄ")] = bstack11l1l1ll11_opy_(outcome)
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᙅ")] = 0
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᙆ")] = bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᙇ")]
        if bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᙈ")] == bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᙉ"):
            bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᙊ")] = bstack11lllll_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᙋ")  # bstack1llll1ll1ll_opy_
            bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᙌ")] = [{bstack11lllll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᙍ"): [bstack11lllll_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᙎ")]}]
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᙏ")] = bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᙐ")]
    return bstack1l11l1lll1_opy_
def bstack1lllll11lll_opy_(test, bstack1l11ll1lll_opy_, bstack1ll111ll_opy_, result, call, outcome, bstack1llll1l1111_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l11ll1lll_opy_[bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᙑ")]
    hook_name = bstack1l11ll1lll_opy_[bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᙒ")]
    hook_data = {
        bstack11lllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᙓ"): bstack1l11ll1lll_opy_[bstack11lllll_opy_ (u"ࠫࡺࡻࡩࡥࠩᙔ")],
        bstack11lllll_opy_ (u"ࠬࡺࡹࡱࡧࠪᙕ"): bstack11lllll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᙖ"),
        bstack11lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᙗ"): bstack11lllll_opy_ (u"ࠨࡽࢀࠫᙘ").format(bstack1111ll1lll_opy_(hook_name)),
        bstack11lllll_opy_ (u"ࠩࡥࡳࡩࡿࠧᙙ"): {
            bstack11lllll_opy_ (u"ࠪࡰࡦࡴࡧࠨᙚ"): bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᙛ"),
            bstack11lllll_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᙜ"): None
        },
        bstack11lllll_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᙝ"): test.name,
        bstack11lllll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᙞ"): bstack1ll1llll1l_opy_.bstack1l1111ll11_opy_(test, hook_name),
        bstack11lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᙟ"): file_path,
        bstack11lllll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᙠ"): file_path,
        bstack11lllll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᙡ"): bstack11lllll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᙢ"),
        bstack11lllll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᙣ"): file_path,
        bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᙤ"): bstack1l11ll1lll_opy_[bstack11lllll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᙥ")],
        bstack11lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᙦ"): bstack11lllll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᙧ") if bstack1lllll111ll_opy_ == bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᙨ") else bstack11lllll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᙩ"),
        bstack11lllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᙪ"): hook_type
    }
    bstack1lllll11l11_opy_ = bstack1l1111lll1_opy_(_1l1l11111l_opy_.get(test.nodeid, None))
    if bstack1lllll11l11_opy_:
        hook_data[bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫᙫ")] = bstack1lllll11l11_opy_
    if result:
        hook_data[bstack11lllll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᙬ")] = result.outcome
        hook_data[bstack11lllll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ᙭")] = result.duration * 1000
        hook_data[bstack11lllll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᙮")] = bstack1l11ll1lll_opy_[bstack11lllll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᙯ")]
        if result.failed:
            hook_data[bstack11lllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᙰ")] = bstack1ll1llll1l_opy_.bstack11llll1l1l_opy_(call.excinfo.typename)
            hook_data[bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᙱ")] = bstack1ll1llll1l_opy_.bstack1llllllll1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11lllll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᙲ")] = bstack11l1l1ll11_opy_(outcome)
        hook_data[bstack11lllll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᙳ")] = 100
        hook_data[bstack11lllll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᙴ")] = bstack1l11ll1lll_opy_[bstack11lllll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᙵ")]
        if hook_data[bstack11lllll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᙶ")] == bstack11lllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᙷ"):
            hook_data[bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᙸ")] = bstack11lllll_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᙹ")  # bstack1llll1ll1ll_opy_
            hook_data[bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᙺ")] = [{bstack11lllll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᙻ"): [bstack11lllll_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᙼ")]}]
    if bstack1llll1l1111_opy_:
        hook_data[bstack11lllll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᙽ")] = bstack1llll1l1111_opy_.result
        hook_data[bstack11lllll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᙾ")] = bstack11l1l1l11l_opy_(bstack1l11ll1lll_opy_[bstack11lllll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᙿ")], bstack1l11ll1lll_opy_[bstack11lllll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ ")])
        hook_data[bstack11lllll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᚁ")] = bstack1l11ll1lll_opy_[bstack11lllll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᚂ")]
        if hook_data[bstack11lllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᚃ")] == bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᚄ"):
            hook_data[bstack11lllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᚅ")] = bstack1ll1llll1l_opy_.bstack11llll1l1l_opy_(bstack1llll1l1111_opy_.exception_type)
            hook_data[bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᚆ")] = [{bstack11lllll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᚇ"): bstack11l1ll1l11_opy_(bstack1llll1l1111_opy_.exception)}]
    return hook_data
def bstack1lllll1l1ll_opy_(test, bstack1l111l1l11_opy_, bstack1ll111ll_opy_, result=None, call=None, outcome=None):
    bstack1l11l1lll1_opy_ = bstack1llll1lllll_opy_(test, bstack1l111l1l11_opy_, result, call, bstack1ll111ll_opy_, outcome)
    driver = getattr(test, bstack11lllll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᚈ"), None)
    if bstack1ll111ll_opy_ == bstack11lllll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᚉ") and driver:
        bstack1l11l1lll1_opy_[bstack11lllll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᚊ")] = bstack1ll1llll1l_opy_.bstack1l11l1l1l1_opy_(driver)
    if bstack1ll111ll_opy_ == bstack11lllll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᚋ"):
        bstack1ll111ll_opy_ = bstack11lllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᚌ")
    bstack1l11l1l11l_opy_ = {
        bstack11lllll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᚍ"): bstack1ll111ll_opy_,
        bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᚎ"): bstack1l11l1lll1_opy_
    }
    bstack1ll1llll1l_opy_.bstack1l111l1111_opy_(bstack1l11l1l11l_opy_)
def bstack1lllll1lll1_opy_(test, bstack1l111l1l11_opy_, bstack1ll111ll_opy_, result=None, call=None, outcome=None, bstack1llll1l1111_opy_=None):
    hook_data = bstack1lllll11lll_opy_(test, bstack1l111l1l11_opy_, bstack1ll111ll_opy_, result, call, outcome, bstack1llll1l1111_opy_)
    bstack1l11l1l11l_opy_ = {
        bstack11lllll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᚏ"): bstack1ll111ll_opy_,
        bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᚐ"): hook_data
    }
    bstack1ll1llll1l_opy_.bstack1l111l1111_opy_(bstack1l11l1l11l_opy_)
def bstack1l1111lll1_opy_(bstack1l111l1l11_opy_):
    if not bstack1l111l1l11_opy_:
        return None
    if bstack1l111l1l11_opy_.get(bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᚑ"), None):
        return getattr(bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᚒ")], bstack11lllll_opy_ (u"ࠫࡺࡻࡩࡥࠩᚓ"), None)
    return bstack1l111l1l11_opy_.get(bstack11lllll_opy_ (u"ࠬࡻࡵࡪࡦࠪᚔ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1ll1llll1l_opy_.on():
            return
        places = [bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᚕ"), bstack11lllll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᚖ"), bstack11lllll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᚗ")]
        bstack1l1l1111ll_opy_ = []
        for bstack1llll1l1l1l_opy_ in places:
            records = caplog.get_records(bstack1llll1l1l1l_opy_)
            bstack1llll1l11ll_opy_ = bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᚘ") if bstack1llll1l1l1l_opy_ == bstack11lllll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᚙ") else bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᚚ")
            bstack1llll1lll1l_opy_ = request.node.nodeid + (bstack11lllll_opy_ (u"ࠬ࠭᚛") if bstack1llll1l1l1l_opy_ == bstack11lllll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ᚜") else bstack11lllll_opy_ (u"ࠧ࠮ࠩ᚝") + bstack1llll1l1l1l_opy_)
            bstack1lllll11111_opy_ = bstack1l1111lll1_opy_(_1l1l11111l_opy_.get(bstack1llll1lll1l_opy_, None))
            if not bstack1lllll11111_opy_:
                continue
            for record in records:
                if bstack11ll11111l_opy_(record.message):
                    continue
                bstack1l1l1111ll_opy_.append({
                    bstack11lllll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ᚞"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11lllll_opy_ (u"ࠩ࡝ࠫ᚟"),
                    bstack11lllll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᚠ"): record.levelname,
                    bstack11lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᚡ"): record.message,
                    bstack1llll1l11ll_opy_: bstack1lllll11111_opy_
                })
        if len(bstack1l1l1111ll_opy_) > 0:
            bstack1ll1llll1l_opy_.bstack1l11ll1111_opy_(bstack1l1l1111ll_opy_)
    except Exception as err:
        print(bstack11lllll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩᚢ"), str(err))
def bstack1ll11lllll_opy_(sequence, driver_command, response=None):
    if sequence == bstack11lllll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᚣ"):
        if driver_command == bstack11lllll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫᚤ"):
            bstack1ll1llll1l_opy_.bstack111l1lll1_opy_({
                bstack11lllll_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧᚥ"): response[bstack11lllll_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨᚦ")],
                bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᚧ"): store[bstack11lllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᚨ")]
            })
def bstack11ll11l11_opy_():
    global bstack1lll11l1ll_opy_
    bstack1ll1llll1l_opy_.bstack1l11l1111l_opy_()
    for driver in bstack1lll11l1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1l1ll1_opy_(*args):
    global bstack1lll11l1ll_opy_
    bstack1ll1llll1l_opy_.bstack1l11l1111l_opy_()
    for driver in bstack1lll11l1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1ll1l1l_opy_(self, *args, **kwargs):
    bstack1ll11ll1_opy_ = bstack11l1ll1l_opy_(self, *args, **kwargs)
    bstack1ll1llll1l_opy_.bstack111ll11l1_opy_(self)
    return bstack1ll11ll1_opy_
def bstack1lll11llll_opy_(framework_name):
    global bstack1l1ll1ll11_opy_
    global bstack1ll1llll_opy_
    bstack1l1ll1ll11_opy_ = framework_name
    logger.info(bstack11l1llll1_opy_.format(bstack1l1ll1ll11_opy_.split(bstack11lllll_opy_ (u"ࠬ࠳ࠧᚩ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11ll111l1l_opy_():
            Service.start = bstack1llll1l111_opy_
            Service.stop = bstack1l11l1l1l_opy_
            webdriver.Remote.__init__ = bstack1l11l111l_opy_
            webdriver.Remote.get = bstack1l1l11ll_opy_
            if not isinstance(os.getenv(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧᚪ")), str):
                return
            WebDriver.close = bstack11ll1l1ll_opy_
            WebDriver.quit = bstack11ll11ll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack11l111l1l_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1l1lll1l_opy_ = getAccessibilityResultsSummary
        if not bstack11ll111l1l_opy_() and bstack1ll1llll1l_opy_.on():
            webdriver.Remote.__init__ = bstack1l1ll1l1l_opy_
        bstack1ll1llll_opy_ = True
    except Exception as e:
        pass
    bstack1l1l1l111_opy_()
    if os.environ.get(bstack11lllll_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᚫ")):
        bstack1ll1llll_opy_ = eval(os.environ.get(bstack11lllll_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭ᚬ")))
    if not bstack1ll1llll_opy_:
        bstack1ll111llll_opy_(bstack11lllll_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦᚭ"), bstack111l11111_opy_)
    if bstack1l1ll11111_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1l11l1ll_opy_
        except Exception as e:
            logger.error(bstack1ll11l1111_opy_.format(str(e)))
    if bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᚮ") in str(framework_name).lower():
        if not bstack11ll111l1l_opy_():
            return
        try:
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
def bstack11ll11ll_opy_(self):
    global bstack1l1ll1ll11_opy_
    global bstack1111l1l1_opy_
    global bstack1ll1lll111_opy_
    try:
        if bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᚯ") in bstack1l1ll1ll11_opy_ and self.session_id != None and bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᚰ"), bstack11lllll_opy_ (u"࠭ࠧᚱ")) != bstack11lllll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᚲ"):
            bstack11111l1l1_opy_ = bstack11lllll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᚳ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᚴ")
            bstack1l1ll1l1_opy_(logger, True)
            if self != None:
                bstack1lll1l11l1_opy_(self, bstack11111l1l1_opy_, bstack11lllll_opy_ (u"ࠪ࠰ࠥ࠭ᚵ").join(threading.current_thread().bstackTestErrorMessages))
        threading.current_thread().testStatus = bstack11lllll_opy_ (u"ࠫࠬᚶ")
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨᚷ") + str(e))
    bstack1ll1lll111_opy_(self)
    self.session_id = None
def bstack1l11l111l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1111l1l1_opy_
    global bstack11l1llll_opy_
    global bstack1ll1l11ll_opy_
    global bstack1l1ll1ll11_opy_
    global bstack11l1ll1l_opy_
    global bstack1lll11l1ll_opy_
    global bstack111ll1l1_opy_
    global bstack1ll11111l_opy_
    global bstack1lllll1ll1l_opy_
    global bstack1l1l11l1l1_opy_
    CONFIG[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᚸ")] = str(bstack1l1ll1ll11_opy_) + str(__version__)
    command_executor = bstack1l111ll1_opy_(bstack111ll1l1_opy_)
    logger.debug(bstack1111llll_opy_.format(command_executor))
    proxy = bstack1llll11lll_opy_(CONFIG, proxy)
    bstack11lllll1l_opy_ = 0
    try:
        if bstack1ll1l11ll_opy_ is True:
            bstack11lllll1l_opy_ = int(os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᚹ")))
    except:
        bstack11lllll1l_opy_ = 0
    bstack1l1lll1ll_opy_ = bstack1l11111ll_opy_(CONFIG, bstack11lllll1l_opy_)
    logger.debug(bstack1llll11l1_opy_.format(str(bstack1l1lll1ll_opy_)))
    bstack1l1l11l1l1_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᚺ"))[bstack11lllll1l_opy_]
    if bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᚻ") in CONFIG and CONFIG[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᚼ")]:
        bstack11l1ll1ll_opy_(bstack1l1lll1ll_opy_, bstack1ll11111l_opy_)
    if desired_capabilities:
        bstack1llll111l_opy_ = bstack1l111111_opy_(desired_capabilities)
        bstack1llll111l_opy_[bstack11lllll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᚽ")] = bstack1l1l11l11l_opy_(CONFIG)
        bstack1l1111lll_opy_ = bstack1l11111ll_opy_(bstack1llll111l_opy_)
        if bstack1l1111lll_opy_:
            bstack1l1lll1ll_opy_ = update(bstack1l1111lll_opy_, bstack1l1lll1ll_opy_)
        desired_capabilities = None
    if options:
        bstack1l1l1l1l11_opy_(options, bstack1l1lll1ll_opy_)
    if not options:
        options = bstack1111l11l1_opy_(bstack1l1lll1ll_opy_)
    if bstack1111ll111_opy_.bstack1ll1ll1lll_opy_(CONFIG, bstack11lllll1l_opy_) and bstack1111ll111_opy_.bstack11111lll_opy_(bstack1l1lll1ll_opy_, options):
        bstack1lllll1ll1l_opy_ = True
        bstack1111ll111_opy_.set_capabilities(bstack1l1lll1ll_opy_, CONFIG)
    if proxy and bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᚾ")):
        options.proxy(proxy)
    if options and bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᚿ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1l11lll1_opy_() < version.parse(bstack11lllll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᛀ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1lll1ll_opy_)
    logger.info(bstack1ll1l1l1l_opy_)
    if bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᛁ")):
        bstack11l1ll1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᛂ")):
        bstack11l1ll1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᛃ")):
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
        bstack11l1l11ll_opy_ = bstack11lllll_opy_ (u"ࠫࠬᛄ")
        if bstack1l1l11lll1_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭ᛅ")):
            bstack11l1l11ll_opy_ = self.caps.get(bstack11lllll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᛆ"))
        else:
            bstack11l1l11ll_opy_ = self.capabilities.get(bstack11lllll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢᛇ"))
        if bstack11l1l11ll_opy_:
            bstack1ll1111ll_opy_(bstack11l1l11ll_opy_)
            if bstack1l1l11lll1_opy_() <= version.parse(bstack11lllll_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨᛈ")):
                self.command_executor._url = bstack11lllll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᛉ") + bstack111ll1l1_opy_ + bstack11lllll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢᛊ")
            else:
                self.command_executor._url = bstack11lllll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᛋ") + bstack11l1l11ll_opy_ + bstack11lllll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨᛌ")
            logger.debug(bstack1l1111ll1_opy_.format(bstack11l1l11ll_opy_))
        else:
            logger.debug(bstack11ll1ll1l_opy_.format(bstack11lllll_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᛍ")))
    except Exception as e:
        logger.debug(bstack11ll1ll1l_opy_.format(e))
    bstack1111l1l1_opy_ = self.session_id
    if bstack11lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᛎ") in bstack1l1ll1ll11_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1ll1llll1l_opy_.bstack111ll11l1_opy_(self)
    bstack1lll11l1ll_opy_.append(self)
    if bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᛏ") in CONFIG and bstack11lllll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᛐ") in CONFIG[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᛑ")][bstack11lllll1l_opy_]:
        bstack11l1llll_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᛒ")][bstack11lllll1l_opy_][bstack11lllll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᛓ")]
    logger.debug(bstack111ll11ll_opy_.format(bstack1111l1l1_opy_))
def bstack1l1l11ll_opy_(self, url):
    global bstack1l1l1l1ll_opy_
    global CONFIG
    try:
        bstack1llll1l1l1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1lll1lll_opy_.format(str(err)))
    try:
        bstack1l1l1l1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack1llll1111_opy_ = str(e)
            if any(err_msg in bstack1llll1111_opy_ for err_msg in bstack111lll1ll_opy_):
                bstack1llll1l1l1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1lll1lll_opy_.format(str(err)))
        raise e
def bstack11111ll1_opy_(item, when):
    global bstack11ll11l1_opy_
    try:
        bstack11ll11l1_opy_(item, when)
    except Exception as e:
        pass
def bstack11l11l1ll_opy_(item, call, rep):
    global bstack1lll1l11ll_opy_
    global bstack1lll11l1ll_opy_
    name = bstack11lllll_opy_ (u"࠭ࠧᛔ")
    try:
        if rep.when == bstack11lllll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᛕ"):
            bstack1111l1l1_opy_ = threading.current_thread().bstackSessionId
            bstack1lllll1111l_opy_ = item.config.getoption(bstack11lllll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᛖ"))
            try:
                if (str(bstack1lllll1111l_opy_).lower() != bstack11lllll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᛗ")):
                    name = str(rep.nodeid)
                    bstack1ll11llll1_opy_ = bstack11lll111_opy_(bstack11lllll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᛘ"), name, bstack11lllll_opy_ (u"ࠫࠬᛙ"), bstack11lllll_opy_ (u"ࠬ࠭ᛚ"), bstack11lllll_opy_ (u"࠭ࠧᛛ"), bstack11lllll_opy_ (u"ࠧࠨᛜ"))
                    os.environ[bstack11lllll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᛝ")] = name
                    for driver in bstack1lll11l1ll_opy_:
                        if bstack1111l1l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll11llll1_opy_)
            except Exception as e:
                logger.debug(bstack11lllll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᛞ").format(str(e)))
            try:
                bstack1ll1111l1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11lllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᛟ"):
                    status = bstack11lllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᛠ") if rep.outcome.lower() == bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᛡ") else bstack11lllll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᛢ")
                    reason = bstack11lllll_opy_ (u"ࠧࠨᛣ")
                    if status == bstack11lllll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᛤ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11lllll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᛥ") if status == bstack11lllll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᛦ") else bstack11lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᛧ")
                    data = name + bstack11lllll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧᛨ") if status == bstack11lllll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᛩ") else name + bstack11lllll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪᛪ") + reason
                    bstack11ll1111_opy_ = bstack11lll111_opy_(bstack11lllll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ᛫"), bstack11lllll_opy_ (u"ࠩࠪ᛬"), bstack11lllll_opy_ (u"ࠪࠫ᛭"), bstack11lllll_opy_ (u"ࠫࠬᛮ"), level, data)
                    for driver in bstack1lll11l1ll_opy_:
                        if bstack1111l1l1_opy_ == driver.session_id:
                            driver.execute_script(bstack11ll1111_opy_)
            except Exception as e:
                logger.debug(bstack11lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᛯ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪᛰ").format(str(e)))
    bstack1lll1l11ll_opy_(item, call, rep)
notset = Notset()
def bstack1ll11ll1l1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll1lll1_opy_
    if str(name).lower() == bstack11lllll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧᛱ"):
        return bstack11lllll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᛲ")
    else:
        return bstack1lll1lll1_opy_(self, name, default, skip)
def bstack1l11l1ll_opy_(self):
    global CONFIG
    global bstack1llllll11l_opy_
    try:
        proxy = bstack1l1ll11l1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11lllll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᛳ")):
                proxies = bstack1ll111111_opy_(proxy, bstack1l111ll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1ll11ll_opy_ = proxies.popitem()
                    if bstack11lllll_opy_ (u"ࠥ࠾࠴࠵ࠢᛴ") in bstack1l1ll11ll_opy_:
                        return bstack1l1ll11ll_opy_
                    else:
                        return bstack11lllll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᛵ") + bstack1l1ll11ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤᛶ").format(str(e)))
    return bstack1llllll11l_opy_(self)
def bstack1l1ll11111_opy_():
    return (bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᛷ") in CONFIG or bstack11lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᛸ") in CONFIG) and bstack1111l1lll_opy_() and bstack1l1l11lll1_opy_() >= version.parse(
        bstack1111ll11_opy_)
def bstack1ll1l1l11_opy_(self,
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
    global bstack11l1llll_opy_
    global bstack1ll1l11ll_opy_
    global bstack1l1ll1ll11_opy_
    CONFIG[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᛹")] = str(bstack1l1ll1ll11_opy_) + str(__version__)
    bstack11lllll1l_opy_ = 0
    try:
        if bstack1ll1l11ll_opy_ is True:
            bstack11lllll1l_opy_ = int(os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ᛺")))
    except:
        bstack11lllll1l_opy_ = 0
    CONFIG[bstack11lllll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ᛻")] = True
    bstack1l1lll1ll_opy_ = bstack1l11111ll_opy_(CONFIG, bstack11lllll1l_opy_)
    logger.debug(bstack1llll11l1_opy_.format(str(bstack1l1lll1ll_opy_)))
    if CONFIG.get(bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ᛼")):
        bstack11l1ll1ll_opy_(bstack1l1lll1ll_opy_, bstack1ll11111l_opy_)
    if bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᛽") in CONFIG and bstack11lllll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᛾") in CONFIG[bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᛿")][bstack11lllll1l_opy_]:
        bstack11l1llll_opy_ = CONFIG[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᜀ")][bstack11lllll1l_opy_][bstack11lllll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᜁ")]
    import urllib
    import json
    bstack111l11ll_opy_ = bstack11lllll_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬᜂ") + urllib.parse.quote(json.dumps(bstack1l1lll1ll_opy_))
    browser = self.connect(bstack111l11ll_opy_)
    return browser
def bstack1l1l1l111_opy_():
    global bstack1ll1llll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1l1l11_opy_
        bstack1ll1llll_opy_ = True
    except Exception as e:
        pass
def bstack1lllll1l1l1_opy_():
    global CONFIG
    global bstack1ll11ll11_opy_
    global bstack111ll1l1_opy_
    global bstack1ll11111l_opy_
    global bstack1ll1l11ll_opy_
    CONFIG = json.loads(os.environ.get(bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪᜃ")))
    bstack1ll11ll11_opy_ = eval(os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ᜄ")))
    bstack111ll1l1_opy_ = os.environ.get(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭ᜅ"))
    bstack11l1111l1_opy_(CONFIG, bstack1ll11ll11_opy_)
    bstack111l1lll_opy_()
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
    if (bstack11lllll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᜆ") in CONFIG or bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᜇ") in CONFIG) and bstack1111l1lll_opy_():
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
        logger.debug(bstack11lllll_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪᜈ"))
    bstack1ll11111l_opy_ = CONFIG.get(bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᜉ"), {}).get(bstack11lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᜊ"))
    bstack1ll1l11ll_opy_ = True
    bstack1lll11llll_opy_(bstack11ll1ll11_opy_)
if (bstack11ll11l111_opy_()):
    bstack1lllll1l1l1_opy_()
@bstack1l11111lll_opy_(class_method=False)
def bstack1llll1l1l11_opy_(hook_name, event, bstack1lllll1l111_opy_=None):
    if hook_name not in [bstack11lllll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᜋ"), bstack11lllll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᜌ"), bstack11lllll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᜍ"), bstack11lllll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᜎ"), bstack11lllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᜏ"), bstack11lllll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᜐ"), bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᜑ"), bstack11lllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᜒ")]:
        return
    node = store[bstack11lllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᜓ")]
    if hook_name in [bstack11lllll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ᜔࠭"), bstack11lllll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧ᜕ࠪ")]:
        node = store[bstack11lllll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ᜖")]
    elif hook_name in [bstack11lllll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ᜗"), bstack11lllll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ᜘")]:
        node = store[bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ᜙")]
    if event == bstack11lllll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭᜚"):
        hook_type = bstack1111ll1l11_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l11ll1lll_opy_ = {
            bstack11lllll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᜛"): uuid,
            bstack11lllll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ᜜"): bstack111l11lll_opy_(),
            bstack11lllll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ᜝"): bstack11lllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ᜞"),
            bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᜟ"): hook_type,
            bstack11lllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᜠ"): hook_name
        }
        store[bstack11lllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᜡ")].append(uuid)
        bstack1lllll111l1_opy_ = node.nodeid
        if hook_type == bstack11lllll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᜢ"):
            if not _1l1l11111l_opy_.get(bstack1lllll111l1_opy_, None):
                _1l1l11111l_opy_[bstack1lllll111l1_opy_] = {bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᜣ"): []}
            _1l1l11111l_opy_[bstack1lllll111l1_opy_][bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᜤ")].append(bstack1l11ll1lll_opy_[bstack11lllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᜥ")])
        _1l1l11111l_opy_[bstack1lllll111l1_opy_ + bstack11lllll_opy_ (u"ࠫ࠲࠭ᜦ") + hook_name] = bstack1l11ll1lll_opy_
        bstack1lllll1lll1_opy_(node, bstack1l11ll1lll_opy_, bstack11lllll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᜧ"))
    elif event == bstack11lllll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᜨ"):
        bstack1l111ll1l1_opy_ = node.nodeid + bstack11lllll_opy_ (u"ࠧ࠮ࠩᜩ") + hook_name
        _1l1l11111l_opy_[bstack1l111ll1l1_opy_][bstack11lllll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᜪ")] = bstack111l11lll_opy_()
        bstack1llll1llll1_opy_(_1l1l11111l_opy_[bstack1l111ll1l1_opy_][bstack11lllll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᜫ")])
        bstack1lllll1lll1_opy_(node, _1l1l11111l_opy_[bstack1l111ll1l1_opy_], bstack11lllll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᜬ"), bstack1llll1l1111_opy_=bstack1lllll1l111_opy_)
def bstack1lllll1ll11_opy_():
    global bstack1lllll111ll_opy_
    if bstack1ll1l111l1_opy_():
        bstack1lllll111ll_opy_ = bstack11lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᜭ")
    else:
        bstack1lllll111ll_opy_ = bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᜮ")
@bstack1ll1llll1l_opy_.bstack1llllll1111_opy_
def bstack1llll1ll1l1_opy_():
    bstack1lllll1ll11_opy_()
    if bstack1111l1lll_opy_():
        bstack1l1ll1l11_opy_(bstack1ll11lllll_opy_)
    bstack11l111ll1l_opy_ = bstack11l11l11l1_opy_(bstack1llll1l1l11_opy_)
bstack1llll1ll1l1_opy_()