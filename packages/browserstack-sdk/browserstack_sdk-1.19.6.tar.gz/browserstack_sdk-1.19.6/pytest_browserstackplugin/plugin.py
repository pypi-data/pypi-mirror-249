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
from browserstack_sdk.__init__ import (bstack1l11ll1l_opy_, bstack1lll1ll11_opy_, update, bstack1lll1lll1_opy_,
                                       bstack1l1ll11lll_opy_, bstack1ll111ll1_opy_, bstack1ll1ll111l_opy_, bstack1ll11ll1l1_opy_,
                                       bstack1lll11111_opy_, bstack11llllll1_opy_, bstack1l11ll11_opy_, bstack1l11l1l1l_opy_,
                                       bstack1l1ll1llll_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l11lll1ll_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack111lll11_opy_, bstack1ll11ll11_opy_, bstack1lll1l111l_opy_, bstack11ll1ll1_opy_, \
    bstack1111ll1l_opy_
from bstack_utils.helper import bstack11l1l1ll1_opy_, bstack1lll11lll1_opy_, bstack11ll11l1ll_opy_, bstack1ll11ll1l_opy_, \
    bstack11ll111l1l_opy_, \
    bstack11l1l11111_opy_, bstack1lll1ll1l_opy_, bstack11lll1l1l_opy_, bstack11ll11l1l1_opy_, bstack1111l111_opy_, Notset, \
    bstack11ll1ll11_opy_, bstack11l1l1l111_opy_, bstack11l1l1llll_opy_, Result, bstack11l1lll111_opy_, bstack11l11lll1l_opy_, bstack1l1111l111_opy_, \
    bstack1l1lll1l11_opy_, bstack1llll1l11l_opy_, bstack1l1l1ll11_opy_
from bstack_utils.bstack11l11l1lll_opy_ import bstack11l111llll_opy_
from bstack_utils.messages import bstack1l11l1l1_opy_, bstack1111ll11_opy_, bstack1lll11ll1_opy_, bstack111l1l1l_opy_, bstack11111l1l1_opy_, \
    bstack1111lll1_opy_, bstack11l11l1l_opy_, bstack11ll1l11_opy_, bstack1llll1ll1l_opy_, bstack1l11ll111_opy_, \
    bstack11l1111l_opy_, bstack1ll11lll1_opy_
from bstack_utils.proxy import bstack1ll1ll1l11_opy_, bstack1l1l11ll11_opy_
from bstack_utils.bstack1ll111lll1_opy_ import bstack1111ll1l11_opy_, bstack1111ll111l_opy_, bstack1111ll1lll_opy_, bstack1111ll11l1_opy_, \
    bstack1111l1ll11_opy_, bstack1111l1lll1_opy_, bstack1111ll11ll_opy_, bstack11ll1l111_opy_, bstack1111l1llll_opy_
from bstack_utils.bstack1l1l1l111_opy_ import bstack1l1ll1l1_opy_
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1l1l1l11ll_opy_, bstack11llll11_opy_, bstack1ll11l11l1_opy_, \
    bstack1l1111l1_opy_, bstack1llllll1ll_opy_
from bstack_utils.bstack1l11lllll1_opy_ import bstack1l11l1l111_opy_
from bstack_utils.bstack1l1llll111_opy_ import bstack1l11ll1ll_opy_
import bstack_utils.bstack1ll1lll1l_opy_ as bstack111ll11l1_opy_
bstack1llll11l_opy_ = None
bstack1l1l11ll_opy_ = None
bstack1ll1111l_opy_ = None
bstack1l1lll111_opy_ = None
bstack1lllll1111_opy_ = None
bstack1ll1ll11ll_opy_ = None
bstack1l1l11llll_opy_ = None
bstack1llll11l1l_opy_ = None
bstack1ll1ll111_opy_ = None
bstack1l1l1l1l1l_opy_ = None
bstack11llll1ll_opy_ = None
bstack1l111l1ll_opy_ = None
bstack11111llll_opy_ = None
bstack11l1111l1_opy_ = bstack1lll11l_opy_ (u"ࠬ࠭ᔯ")
CONFIG = {}
bstack111l1ll1_opy_ = False
bstack1l1l1l11_opy_ = bstack1lll11l_opy_ (u"࠭ࠧᔰ")
bstack1l1lllll11_opy_ = bstack1lll11l_opy_ (u"ࠧࠨᔱ")
bstack1l111l1l_opy_ = False
bstack11l1ll1ll_opy_ = []
bstack11l111ll_opy_ = bstack1ll11ll11_opy_
bstack1lllll111ll_opy_ = bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᔲ")
bstack1llll11llll_opy_ = False
bstack11l11ll1_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l111ll_opy_,
                    format=bstack1lll11l_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᔳ"),
                    datefmt=bstack1lll11l_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬᔴ"),
                    stream=sys.stdout)
store = {
    bstack1lll11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᔵ"): []
}
bstack1lllll1l1ll_opy_ = False
def bstack1lll1l11l1_opy_():
    global CONFIG
    global bstack11l111ll_opy_
    if bstack1lll11l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᔶ") in CONFIG:
        bstack11l111ll_opy_ = bstack111lll11_opy_[CONFIG[bstack1lll11l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᔷ")]]
        logging.getLogger().setLevel(bstack11l111ll_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l1111l11l_opy_ = {}
current_test_uuid = None
def bstack1llllll111_opy_(page, bstack1lll1l1lll_opy_):
    try:
        page.evaluate(bstack1lll11l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᔸ"),
                      bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬᔹ") + json.dumps(
                          bstack1lll1l1lll_opy_) + bstack1lll11l_opy_ (u"ࠤࢀࢁࠧᔺ"))
    except Exception as e:
        print(bstack1lll11l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣᔻ"), e)
def bstack11lllll1l_opy_(page, message, level):
    try:
        page.evaluate(bstack1lll11l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᔼ"), bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪᔽ") + json.dumps(
            message) + bstack1lll11l_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩᔾ") + json.dumps(level) + bstack1lll11l_opy_ (u"ࠧࡾࡿࠪᔿ"))
    except Exception as e:
        print(bstack1lll11l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦᕀ"), e)
def pytest_configure(config):
    bstack1l1l1ll1ll_opy_ = Config.get_instance()
    config.args = bstack1l11ll1ll_opy_.bstack1llllll1lll_opy_(config.args)
    bstack1l1l1ll1ll_opy_.bstack1lllll11ll_opy_(bstack1l1l1ll11_opy_(config.getoption(bstack1lll11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᕁ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lllll1ll11_opy_ = item.config.getoption(bstack1lll11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᕂ"))
    plugins = item.config.getoption(bstack1lll11l_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧᕃ"))
    report = outcome.get_result()
    bstack1llllll1111_opy_(item, call, report)
    if bstack1lll11l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥᕄ") not in plugins or bstack1111l111_opy_():
        return
    summary = []
    driver = getattr(item, bstack1lll11l_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢᕅ"), None)
    page = getattr(item, bstack1lll11l_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨᕆ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1llll1lll11_opy_(item, report, summary, bstack1lllll1ll11_opy_)
    if (page is not None):
        bstack1llll1ll1l1_opy_(item, report, summary, bstack1lllll1ll11_opy_)
def bstack1llll1lll11_opy_(item, report, summary, bstack1lllll1ll11_opy_):
    if report.when == bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᕇ") and report.skipped:
        bstack1111l1llll_opy_(report)
    if report.when in [bstack1lll11l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᕈ"), bstack1lll11l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᕉ")]:
        return
    if not bstack11ll11l1ll_opy_():
        return
    try:
        if (str(bstack1lllll1ll11_opy_).lower() != bstack1lll11l_opy_ (u"ࠫࡹࡸࡵࡦࠩᕊ")):
            item._driver.execute_script(
                bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪᕋ") + json.dumps(
                    report.nodeid) + bstack1lll11l_opy_ (u"࠭ࡽࡾࠩᕌ"))
        os.environ[bstack1lll11l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᕍ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1lll11l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣᕎ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1lll11l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᕏ")))
    bstack1ll111111l_opy_ = bstack1lll11l_opy_ (u"ࠥࠦᕐ")
    bstack1111l1llll_opy_(report)
    if not passed:
        try:
            bstack1ll111111l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1lll11l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᕑ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll111111l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1lll11l_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᕒ")))
        bstack1ll111111l_opy_ = bstack1lll11l_opy_ (u"ࠨࠢᕓ")
        if not passed:
            try:
                bstack1ll111111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1lll11l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᕔ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll111111l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬᕕ")
                    + json.dumps(bstack1lll11l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥᕖ"))
                    + bstack1lll11l_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᕗ")
                )
            else:
                item._driver.execute_script(
                    bstack1lll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᕘ")
                    + json.dumps(str(bstack1ll111111l_opy_))
                    + bstack1lll11l_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᕙ")
                )
        except Exception as e:
            summary.append(bstack1lll11l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦᕚ").format(e))
def bstack1llll1l1ll1_opy_(test_name, error_message):
    try:
        bstack1lllll11l11_opy_ = []
        bstack1l1lll1l1l_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᕛ"), bstack1lll11l_opy_ (u"ࠨ࠲ࠪᕜ"))
        bstack1l11l1111_opy_ = {bstack1lll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᕝ"): test_name, bstack1lll11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᕞ"): error_message, bstack1lll11l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᕟ"): bstack1l1lll1l1l_opy_}
        bstack1lllll11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll11l_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᕠ"))
        if os.path.exists(bstack1lllll11lll_opy_):
            with open(bstack1lllll11lll_opy_) as f:
                bstack1lllll11l11_opy_ = json.load(f)
        bstack1lllll11l11_opy_.append(bstack1l11l1111_opy_)
        with open(bstack1lllll11lll_opy_, bstack1lll11l_opy_ (u"࠭ࡷࠨᕡ")) as f:
            json.dump(bstack1lllll11l11_opy_, f)
    except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬᕢ") + str(e))
def bstack1llll1ll1l1_opy_(item, report, summary, bstack1lllll1ll11_opy_):
    if report.when in [bstack1lll11l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᕣ"), bstack1lll11l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᕤ")]:
        return
    if (str(bstack1lllll1ll11_opy_).lower() != bstack1lll11l_opy_ (u"ࠪࡸࡷࡻࡥࠨᕥ")):
        bstack1llllll111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1lll11l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᕦ")))
    bstack1ll111111l_opy_ = bstack1lll11l_opy_ (u"ࠧࠨᕧ")
    bstack1111l1llll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll111111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1lll11l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᕨ").format(e)
                )
        try:
            if passed:
                bstack1llllll1ll_opy_(getattr(item, bstack1lll11l_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᕩ"), None), bstack1lll11l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᕪ"))
            else:
                error_message = bstack1lll11l_opy_ (u"ࠩࠪᕫ")
                if bstack1ll111111l_opy_:
                    bstack11lllll1l_opy_(item._page, str(bstack1ll111111l_opy_), bstack1lll11l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᕬ"))
                    bstack1llllll1ll_opy_(getattr(item, bstack1lll11l_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᕭ"), None), bstack1lll11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᕮ"), str(bstack1ll111111l_opy_))
                    error_message = str(bstack1ll111111l_opy_)
                else:
                    bstack1llllll1ll_opy_(getattr(item, bstack1lll11l_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᕯ"), None), bstack1lll11l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᕰ"))
                bstack1llll1l1ll1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1lll11l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧᕱ").format(e))
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
    parser.addoption(bstack1lll11l_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᕲ"), default=bstack1lll11l_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᕳ"), help=bstack1lll11l_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᕴ"))
    parser.addoption(bstack1lll11l_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᕵ"), default=bstack1lll11l_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧᕶ"), help=bstack1lll11l_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨᕷ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1lll11l_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥᕸ"), action=bstack1lll11l_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣᕹ"), default=bstack1lll11l_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥᕺ"),
                         help=bstack1lll11l_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥᕻ"))
def bstack1l111l1ll1_opy_(log):
    if not (log[bstack1lll11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕼ")] and log[bstack1lll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕽ")].strip()):
        return
    active = bstack1l11ll1l1l_opy_()
    log = {
        bstack1lll11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᕾ"): log[bstack1lll11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᕿ")],
        bstack1lll11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᖀ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"ࠪ࡞ࠬᖁ"),
        bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᖂ"): log[bstack1lll11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖃ")],
    }
    if active:
        if active[bstack1lll11l_opy_ (u"࠭ࡴࡺࡲࡨࠫᖄ")] == bstack1lll11l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᖅ"):
            log[bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖆ")] = active[bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖇ")]
        elif active[bstack1lll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨᖈ")] == bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᖉ"):
            log[bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖊ")] = active[bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖋ")]
    bstack1l11ll1ll_opy_.bstack1l11ll11l1_opy_([log])
def bstack1l11ll1l1l_opy_():
    if len(store[bstack1lll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖌ")]) > 0 and store[bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᖍ")][-1]:
        return {
            bstack1lll11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᖎ"): bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᖏ"),
            bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖐ"): store[bstack1lll11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᖑ")][-1]
        }
    if store.get(bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᖒ"), None):
        return {
            bstack1lll11l_opy_ (u"ࠧࡵࡻࡳࡩࠬᖓ"): bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᖔ"),
            bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖕ"): store[bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᖖ")]
        }
    return None
bstack1l11111lll_opy_ = bstack1l11lll1ll_opy_(bstack1l111l1ll1_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1llll11llll_opy_
        if bstack1llll11llll_opy_:
            driver = getattr(item, bstack1lll11l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᖗ"), None)
            bstack11ll11l11_opy_ = bstack111ll11l1_opy_.bstack111ll11l_opy_(CONFIG, bstack11l1l11111_opy_(item.own_markers))
            item._a11y_started = bstack111ll11l1_opy_.bstack111l1lll_opy_(driver, bstack11ll11l11_opy_)
        if not bstack1l11ll1ll_opy_.on() or bstack1lllll111ll_opy_ != bstack1lll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᖘ"):
            return
        global current_test_uuid, bstack1l11111lll_opy_
        bstack1l11111lll_opy_.start()
        bstack1l11l1llll_opy_ = {
            bstack1lll11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᖙ"): uuid4().__str__(),
            bstack1lll11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᖚ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"ࠨ࡜ࠪᖛ")
        }
        current_test_uuid = bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᖜ")]
        store[bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᖝ")] = bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᖞ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l1111l11l_opy_[item.nodeid] = {**_1l1111l11l_opy_[item.nodeid], **bstack1l11l1llll_opy_}
        bstack1llll1lll1l_opy_(item, _1l1111l11l_opy_[item.nodeid], bstack1lll11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᖟ"))
    except Exception as err:
        print(bstack1lll11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨᖠ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lllll1l1ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11ll11l1l1_opy_():
        atexit.register(bstack111llll1_opy_)
        if not bstack1lllll1l1ll_opy_:
            bstack1llll1ll1ll_opy_ = [signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT]
            for s in bstack1llll1ll1ll_opy_:
                signal.signal(s, bstack1lllll1llll_opy_)
            bstack1lllll1l1ll_opy_ = True
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1111ll1l11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1lll11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᖡ")
    try:
        if not bstack1l11ll1ll_opy_.on():
            return
        bstack1l11111lll_opy_.start()
        uuid = uuid4().__str__()
        bstack1l11l1llll_opy_ = {
            bstack1lll11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᖢ"): uuid,
            bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᖣ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"ࠪ࡞ࠬᖤ"),
            bstack1lll11l_opy_ (u"ࠫࡹࡿࡰࡦࠩᖥ"): bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᖦ"),
            bstack1lll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᖧ"): bstack1lll11l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᖨ"),
            bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᖩ"): bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᖪ")
        }
        threading.current_thread().current_hook_uuid = uuid
        store[bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᖫ")] = item
        store[bstack1lll11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᖬ")] = [uuid]
        if not _1l1111l11l_opy_.get(item.nodeid, None):
            _1l1111l11l_opy_[item.nodeid] = {bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᖭ"): [], bstack1lll11l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᖮ"): []}
        _1l1111l11l_opy_[item.nodeid][bstack1lll11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᖯ")].append(bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᖰ")])
        _1l1111l11l_opy_[item.nodeid + bstack1lll11l_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩᖱ")] = bstack1l11l1llll_opy_
        bstack1lllll11l1l_opy_(item, bstack1l11l1llll_opy_, bstack1lll11l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᖲ"))
    except Exception as err:
        print(bstack1lll11l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧᖳ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack11l11ll1_opy_
        if CONFIG.get(bstack1lll11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᖴ"), False):
            if CONFIG.get(bstack1lll11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᖵ"), bstack1lll11l_opy_ (u"ࠢࡢࡷࡷࡳࠧᖶ")) == bstack1lll11l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᖷ"):
                bstack1llll1l111l_opy_ = bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᖸ"), None)
                bstack1111111l_opy_ = bstack1llll1l111l_opy_ + bstack1lll11l_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᖹ")
                driver = getattr(item, bstack1lll11l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᖺ"), None)
                PercySDK.screenshot(driver, bstack1111111l_opy_)
        if getattr(item, bstack1lll11l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬᖻ"), False):
            logger.info(bstack1lll11l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠥࠨᖼ"))
            driver = getattr(item, bstack1lll11l_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᖽ"), None)
            bstack11lll11lll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack111ll11l1_opy_.bstack11l11111_opy_(driver, bstack11lll11lll_opy_, item.name, item.module.__name__, item.path, bstack11l11ll1_opy_)
        if not bstack1l11ll1ll_opy_.on():
            return
        bstack1l11l1llll_opy_ = {
            bstack1lll11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᖾ"): uuid4().__str__(),
            bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᖿ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"ࠪ࡞ࠬᗀ"),
            bstack1lll11l_opy_ (u"ࠫࡹࡿࡰࡦࠩᗁ"): bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᗂ"),
            bstack1lll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᗃ"): bstack1lll11l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᗄ"),
            bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᗅ"): bstack1lll11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᗆ")
        }
        _1l1111l11l_opy_[item.nodeid + bstack1lll11l_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᗇ")] = bstack1l11l1llll_opy_
        bstack1lllll11l1l_opy_(item, bstack1l11l1llll_opy_, bstack1lll11l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᗈ"))
    except Exception as err:
        print(bstack1lll11l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫᗉ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l11ll1ll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1111ll11l1_opy_(fixturedef.argname):
        store[bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬᗊ")] = request.node
    elif bstack1111l1ll11_opy_(fixturedef.argname):
        store[bstack1lll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬᗋ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1lll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᗌ"): fixturedef.argname,
            bstack1lll11l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᗍ"): bstack11ll111l1l_opy_(outcome),
            bstack1lll11l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᗎ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack1lllll1l111_opy_ = store[bstack1lll11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᗏ")]
        if not _1l1111l11l_opy_.get(bstack1lllll1l111_opy_.nodeid, None):
            _1l1111l11l_opy_[bstack1lllll1l111_opy_.nodeid] = {bstack1lll11l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᗐ"): []}
        _1l1111l11l_opy_[bstack1lllll1l111_opy_.nodeid][bstack1lll11l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᗑ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1lll11l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᗒ"), str(err))
if bstack1111l111_opy_() and bstack1l11ll1ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l1111l11l_opy_[request.node.nodeid][bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᗓ")].bstack111111llll_opy_(id(step))
        except Exception as err:
            print(bstack1lll11l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧᗔ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l1111l11l_opy_[request.node.nodeid][bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᗕ")].bstack1l11l11111_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1lll11l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᗖ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l11lllll1_opy_: bstack1l11l1l111_opy_ = _1l1111l11l_opy_[request.node.nodeid][bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᗗ")]
            bstack1l11lllll1_opy_.bstack1l11l11111_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1lll11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᗘ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lllll111ll_opy_
        try:
            if not bstack1l11ll1ll_opy_.on() or bstack1lllll111ll_opy_ != bstack1lll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᗙ"):
                return
            global bstack1l11111lll_opy_
            bstack1l11111lll_opy_.start()
            if not _1l1111l11l_opy_.get(request.node.nodeid, None):
                _1l1111l11l_opy_[request.node.nodeid] = {}
            bstack1l11lllll1_opy_ = bstack1l11l1l111_opy_.bstack111111l11l_opy_(
                scenario, feature, request.node,
                name=bstack1111l1lll1_opy_(request.node, scenario),
                bstack1l1l111l1l_opy_=bstack1ll11ll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1lll11l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᗚ"),
                tags=bstack1111ll11ll_opy_(feature, scenario)
            )
            _1l1111l11l_opy_[request.node.nodeid][bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᗛ")] = bstack1l11lllll1_opy_
            bstack1lllll11ll1_opy_(bstack1l11lllll1_opy_.uuid)
            bstack1l11ll1ll_opy_.bstack1l111l1lll_opy_(bstack1lll11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᗜ"), bstack1l11lllll1_opy_)
        except Exception as err:
            print(bstack1lll11l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ᗝ"), str(err))
def bstack1lllll111l1_opy_(bstack1lllll1l11l_opy_):
    if bstack1lllll1l11l_opy_ in store[bstack1lll11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᗞ")]:
        store[bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᗟ")].remove(bstack1lllll1l11l_opy_)
def bstack1lllll11ll1_opy_(bstack1llll1l1111_opy_):
    store[bstack1lll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᗠ")] = bstack1llll1l1111_opy_
    threading.current_thread().current_test_uuid = bstack1llll1l1111_opy_
@bstack1l11ll1ll_opy_.bstack1llllll1l1l_opy_
def bstack1llllll1111_opy_(item, call, report):
    global bstack1lllll111ll_opy_
    bstack1ll1111ll_opy_ = bstack1ll11ll1l_opy_()
    if hasattr(report, bstack1lll11l_opy_ (u"ࠨࡵࡷࡳࡵ࠭ᗡ")):
        bstack1ll1111ll_opy_ = bstack11l1lll111_opy_(report.stop)
    if hasattr(report, bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨᗢ")):
        bstack1ll1111ll_opy_ = bstack11l1lll111_opy_(report.start)
    try:
        if getattr(report, bstack1lll11l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᗣ"), bstack1lll11l_opy_ (u"ࠫࠬᗤ")) == bstack1lll11l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᗥ"):
            bstack1l11111lll_opy_.reset()
        if getattr(report, bstack1lll11l_opy_ (u"࠭ࡷࡩࡧࡱࠫᗦ"), bstack1lll11l_opy_ (u"ࠧࠨᗧ")) == bstack1lll11l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᗨ"):
            if bstack1lllll111ll_opy_ == bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᗩ"):
                _1l1111l11l_opy_[item.nodeid][bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᗪ")] = bstack1ll1111ll_opy_
                bstack1llll1lll1l_opy_(item, _1l1111l11l_opy_[item.nodeid], bstack1lll11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᗫ"), report, call)
                store[bstack1lll11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᗬ")] = None
            elif bstack1lllll111ll_opy_ == bstack1lll11l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᗭ"):
                bstack1l11lllll1_opy_ = _1l1111l11l_opy_[item.nodeid][bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᗮ")]
                bstack1l11lllll1_opy_.set(hooks=_1l1111l11l_opy_[item.nodeid].get(bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᗯ"), []))
                exception, bstack1l1l111l11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1l111l11_opy_ = [call.excinfo.exconly(), getattr(report, bstack1lll11l_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨᗰ"), bstack1lll11l_opy_ (u"ࠪࠫᗱ"))]
                bstack1l11lllll1_opy_.stop(time=bstack1ll1111ll_opy_, result=Result(result=getattr(report, bstack1lll11l_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᗲ"), bstack1lll11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᗳ")), exception=exception, bstack1l1l111l11_opy_=bstack1l1l111l11_opy_))
                bstack1l11ll1ll_opy_.bstack1l111l1lll_opy_(bstack1lll11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᗴ"), _1l1111l11l_opy_[item.nodeid][bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᗵ")])
        elif getattr(report, bstack1lll11l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᗶ"), bstack1lll11l_opy_ (u"ࠩࠪᗷ")) in [bstack1lll11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᗸ"), bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᗹ")]:
            bstack1l11llllll_opy_ = item.nodeid + bstack1lll11l_opy_ (u"ࠬ࠳ࠧᗺ") + getattr(report, bstack1lll11l_opy_ (u"࠭ࡷࡩࡧࡱࠫᗻ"), bstack1lll11l_opy_ (u"ࠧࠨᗼ"))
            if getattr(report, bstack1lll11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᗽ"), False):
                hook_type = bstack1lll11l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᗾ") if getattr(report, bstack1lll11l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᗿ"), bstack1lll11l_opy_ (u"ࠫࠬᘀ")) == bstack1lll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᘁ") else bstack1lll11l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᘂ")
                _1l1111l11l_opy_[bstack1l11llllll_opy_] = {
                    bstack1lll11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᘃ"): uuid4().__str__(),
                    bstack1lll11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᘄ"): bstack1ll1111ll_opy_,
                    bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᘅ"): hook_type
                }
            _1l1111l11l_opy_[bstack1l11llllll_opy_][bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘆ")] = bstack1ll1111ll_opy_
            bstack1lllll111l1_opy_(_1l1111l11l_opy_[bstack1l11llllll_opy_][bstack1lll11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᘇ")])
            bstack1lllll11l1l_opy_(item, _1l1111l11l_opy_[bstack1l11llllll_opy_], bstack1lll11l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᘈ"), report, call)
            if getattr(report, bstack1lll11l_opy_ (u"࠭ࡷࡩࡧࡱࠫᘉ"), bstack1lll11l_opy_ (u"ࠧࠨᘊ")) == bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᘋ"):
                if getattr(report, bstack1lll11l_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᘌ"), bstack1lll11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᘍ")) == bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᘎ"):
                    bstack1l11l1llll_opy_ = {
                        bstack1lll11l_opy_ (u"ࠬࡻࡵࡪࡦࠪᘏ"): uuid4().__str__(),
                        bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᘐ"): bstack1ll11ll1l_opy_(),
                        bstack1lll11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᘑ"): bstack1ll11ll1l_opy_()
                    }
                    _1l1111l11l_opy_[item.nodeid] = {**_1l1111l11l_opy_[item.nodeid], **bstack1l11l1llll_opy_}
                    bstack1llll1lll1l_opy_(item, _1l1111l11l_opy_[item.nodeid], bstack1lll11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᘒ"))
                    bstack1llll1lll1l_opy_(item, _1l1111l11l_opy_[item.nodeid], bstack1lll11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᘓ"), report, call)
    except Exception as err:
        print(bstack1lll11l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨᘔ"), str(err))
def bstack1llll1l11l1_opy_(test, bstack1l11l1llll_opy_, result=None, call=None, bstack1ll1ll1111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l11lllll1_opy_ = {
        bstack1lll11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᘕ"): bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠬࡻࡵࡪࡦࠪᘖ")],
        bstack1lll11l_opy_ (u"࠭ࡴࡺࡲࡨࠫᘗ"): bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࠬᘘ"),
        bstack1lll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᘙ"): test.name,
        bstack1lll11l_opy_ (u"ࠩࡥࡳࡩࡿࠧᘚ"): {
            bstack1lll11l_opy_ (u"ࠪࡰࡦࡴࡧࠨᘛ"): bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᘜ"),
            bstack1lll11l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᘝ"): inspect.getsource(test.obj)
        },
        bstack1lll11l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᘞ"): test.name,
        bstack1lll11l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᘟ"): test.name,
        bstack1lll11l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᘠ"): bstack1l11ll1ll_opy_.bstack1l11l1l11l_opy_(test),
        bstack1lll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᘡ"): file_path,
        bstack1lll11l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᘢ"): file_path,
        bstack1lll11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᘣ"): bstack1lll11l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᘤ"),
        bstack1lll11l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᘥ"): file_path,
        bstack1lll11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᘦ"): bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᘧ")],
        bstack1lll11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᘨ"): bstack1lll11l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᘩ"),
        bstack1lll11l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᘪ"): {
            bstack1lll11l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᘫ"): test.nodeid
        },
        bstack1lll11l_opy_ (u"࠭ࡴࡢࡩࡶࠫᘬ"): bstack11l1l11111_opy_(test.own_markers)
    }
    if bstack1ll1ll1111_opy_ in [bstack1lll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᘭ"), bstack1lll11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᘮ")]:
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠩࡰࡩࡹࡧࠧᘯ")] = {
            bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᘰ"): bstack1l11l1llll_opy_.get(bstack1lll11l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᘱ"), [])
        }
    if bstack1ll1ll1111_opy_ == bstack1lll11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᘲ"):
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᘳ")] = bstack1lll11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᘴ")
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᘵ")] = bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᘶ")]
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘷ")] = bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᘸ")]
    if result:
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᘹ")] = result.outcome
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᘺ")] = result.duration * 1000
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᘻ")] = bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᘼ")]
        if result.failed:
            bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᘽ")] = bstack1l11ll1ll_opy_.bstack11llll1l11_opy_(call.excinfo.typename)
            bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᘾ")] = bstack1l11ll1ll_opy_.bstack1lllllll1ll_opy_(call.excinfo, result)
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᘿ")] = bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᙀ")]
    if outcome:
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᙁ")] = bstack11ll111l1l_opy_(outcome)
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᙂ")] = 0
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᙃ")] = bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᙄ")]
        if bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᙅ")] == bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᙆ"):
            bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᙇ")] = bstack1lll11l_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᙈ")  # bstack1llll1l1l11_opy_
            bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᙉ")] = [{bstack1lll11l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᙊ"): [bstack1lll11l_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᙋ")]}]
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᙌ")] = bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᙍ")]
    return bstack1l11lllll1_opy_
def bstack1llll1ll11l_opy_(test, bstack1l11l111l1_opy_, bstack1ll1ll1111_opy_, result, call, outcome, bstack1lllll1ll1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l11l111l1_opy_[bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᙎ")]
    hook_name = bstack1l11l111l1_opy_[bstack1lll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᙏ")]
    hook_data = {
        bstack1lll11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙐ"): bstack1l11l111l1_opy_[bstack1lll11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᙑ")],
        bstack1lll11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᙒ"): bstack1lll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᙓ"),
        bstack1lll11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᙔ"): bstack1lll11l_opy_ (u"ࠬࢁࡽࠨᙕ").format(bstack1111ll111l_opy_(hook_name)),
        bstack1lll11l_opy_ (u"࠭ࡢࡰࡦࡼࠫᙖ"): {
            bstack1lll11l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᙗ"): bstack1lll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᙘ"),
            bstack1lll11l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᙙ"): None
        },
        bstack1lll11l_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᙚ"): test.name,
        bstack1lll11l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᙛ"): bstack1l11ll1ll_opy_.bstack1l11l1l11l_opy_(test, hook_name),
        bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᙜ"): file_path,
        bstack1lll11l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᙝ"): file_path,
        bstack1lll11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᙞ"): bstack1lll11l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᙟ"),
        bstack1lll11l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᙠ"): file_path,
        bstack1lll11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᙡ"): bstack1l11l111l1_opy_[bstack1lll11l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᙢ")],
        bstack1lll11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᙣ"): bstack1lll11l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨᙤ") if bstack1lllll111ll_opy_ == bstack1lll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᙥ") else bstack1lll11l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᙦ"),
        bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᙧ"): hook_type
    }
    bstack1llll1llll1_opy_ = bstack1l11l11lll_opy_(_1l1111l11l_opy_.get(test.nodeid, None))
    if bstack1llll1llll1_opy_:
        hook_data[bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨᙨ")] = bstack1llll1llll1_opy_
    if result:
        hook_data[bstack1lll11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᙩ")] = result.outcome
        hook_data[bstack1lll11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᙪ")] = result.duration * 1000
        hook_data[bstack1lll11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᙫ")] = bstack1l11l111l1_opy_[bstack1lll11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᙬ")]
        if result.failed:
            hook_data[bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ᙭")] = bstack1l11ll1ll_opy_.bstack11llll1l11_opy_(call.excinfo.typename)
            hook_data[bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ᙮")] = bstack1l11ll1ll_opy_.bstack1lllllll1ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1lll11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᙯ")] = bstack11ll111l1l_opy_(outcome)
        hook_data[bstack1lll11l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᙰ")] = 100
        hook_data[bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᙱ")] = bstack1l11l111l1_opy_[bstack1lll11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᙲ")]
        if hook_data[bstack1lll11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᙳ")] == bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᙴ"):
            hook_data[bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᙵ")] = bstack1lll11l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫᙶ")  # bstack1llll1l1l11_opy_
            hook_data[bstack1lll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᙷ")] = [{bstack1lll11l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᙸ"): [bstack1lll11l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᙹ")]}]
    if bstack1lllll1ll1l_opy_:
        hook_data[bstack1lll11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᙺ")] = bstack1lllll1ll1l_opy_.result
        hook_data[bstack1lll11l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᙻ")] = bstack11l1l1l111_opy_(bstack1l11l111l1_opy_[bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᙼ")], bstack1l11l111l1_opy_[bstack1lll11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᙽ")])
        hook_data[bstack1lll11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᙾ")] = bstack1l11l111l1_opy_[bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᙿ")]
        if hook_data[bstack1lll11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ ")] == bstack1lll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᚁ"):
            hook_data[bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᚂ")] = bstack1l11ll1ll_opy_.bstack11llll1l11_opy_(bstack1lllll1ll1l_opy_.exception_type)
            hook_data[bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᚃ")] = [{bstack1lll11l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᚄ"): bstack11l1l1llll_opy_(bstack1lllll1ll1l_opy_.exception)}]
    return hook_data
def bstack1llll1lll1l_opy_(test, bstack1l11l1llll_opy_, bstack1ll1ll1111_opy_, result=None, call=None, outcome=None):
    bstack1l11lllll1_opy_ = bstack1llll1l11l1_opy_(test, bstack1l11l1llll_opy_, result, call, bstack1ll1ll1111_opy_, outcome)
    driver = getattr(test, bstack1lll11l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᚅ"), None)
    if bstack1ll1ll1111_opy_ == bstack1lll11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᚆ") and driver:
        bstack1l11lllll1_opy_[bstack1lll11l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᚇ")] = bstack1l11ll1ll_opy_.bstack1l11llll11_opy_(driver)
    if bstack1ll1ll1111_opy_ == bstack1lll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᚈ"):
        bstack1ll1ll1111_opy_ = bstack1lll11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᚉ")
    bstack1l1l11111l_opy_ = {
        bstack1lll11l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᚊ"): bstack1ll1ll1111_opy_,
        bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᚋ"): bstack1l11lllll1_opy_
    }
    bstack1l11ll1ll_opy_.bstack1l1111lll1_opy_(bstack1l1l11111l_opy_)
def bstack1lllll11l1l_opy_(test, bstack1l11l1llll_opy_, bstack1ll1ll1111_opy_, result=None, call=None, outcome=None, bstack1lllll1ll1l_opy_=None):
    hook_data = bstack1llll1ll11l_opy_(test, bstack1l11l1llll_opy_, bstack1ll1ll1111_opy_, result, call, outcome, bstack1lllll1ll1l_opy_)
    bstack1l1l11111l_opy_ = {
        bstack1lll11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᚌ"): bstack1ll1ll1111_opy_,
        bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᚍ"): hook_data
    }
    bstack1l11ll1ll_opy_.bstack1l1111lll1_opy_(bstack1l1l11111l_opy_)
def bstack1l11l11lll_opy_(bstack1l11l1llll_opy_):
    if not bstack1l11l1llll_opy_:
        return None
    if bstack1l11l1llll_opy_.get(bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᚎ"), None):
        return getattr(bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᚏ")], bstack1lll11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᚐ"), None)
    return bstack1l11l1llll_opy_.get(bstack1lll11l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᚑ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l11ll1ll_opy_.on():
            return
        places = [bstack1lll11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᚒ"), bstack1lll11l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᚓ"), bstack1lll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᚔ")]
        bstack1l11ll1ll1_opy_ = []
        for bstack1llll1l1l1l_opy_ in places:
            records = caplog.get_records(bstack1llll1l1l1l_opy_)
            bstack1llll1l11ll_opy_ = bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᚕ") if bstack1llll1l1l1l_opy_ == bstack1lll11l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᚖ") else bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᚗ")
            bstack1lllll1111l_opy_ = request.node.nodeid + (bstack1lll11l_opy_ (u"ࠩࠪᚘ") if bstack1llll1l1l1l_opy_ == bstack1lll11l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᚙ") else bstack1lll11l_opy_ (u"ࠫ࠲࠭ᚚ") + bstack1llll1l1l1l_opy_)
            bstack1llll1l1111_opy_ = bstack1l11l11lll_opy_(_1l1111l11l_opy_.get(bstack1lllll1111l_opy_, None))
            if not bstack1llll1l1111_opy_:
                continue
            for record in records:
                if bstack11l11lll1l_opy_(record.message):
                    continue
                bstack1l11ll1ll1_opy_.append({
                    bstack1lll11l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ᚛"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1lll11l_opy_ (u"࡚࠭ࠨ᚜"),
                    bstack1lll11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭᚝"): record.levelname,
                    bstack1lll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᚞"): record.message,
                    bstack1llll1l11ll_opy_: bstack1llll1l1111_opy_
                })
        if len(bstack1l11ll1ll1_opy_) > 0:
            bstack1l11ll1ll_opy_.bstack1l11ll11l1_opy_(bstack1l11ll1ll1_opy_)
    except Exception as err:
        print(bstack1lll11l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭᚟"), str(err))
def bstack111ll111l_opy_(sequence, driver_command, response=None):
    if sequence == bstack1lll11l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᚠ"):
        if driver_command == bstack1lll11l_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᚡ"):
            bstack1l11ll1ll_opy_.bstack111ll1l1l_opy_({
                bstack1lll11l_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᚢ"): response[bstack1lll11l_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬᚣ")],
                bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᚤ"): store[bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᚥ")]
            })
def bstack111llll1_opy_():
    global bstack11l1ll1ll_opy_
    bstack1l11ll1ll_opy_.bstack1l11ll111l_opy_()
    for driver in bstack11l1ll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lllll1llll_opy_(*args):
    global bstack11l1ll1ll_opy_
    bstack1l11ll1ll_opy_.bstack1l11ll111l_opy_()
    for driver in bstack11l1ll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1l111_opy_(self, *args, **kwargs):
    bstack1l111l1l1_opy_ = bstack1llll11l_opy_(self, *args, **kwargs)
    bstack1l11ll1ll_opy_.bstack11111111l_opy_(self)
    return bstack1l111l1l1_opy_
def bstack1lllll1ll1_opy_(framework_name):
    global bstack11l1111l1_opy_
    global bstack11l11l11_opy_
    bstack11l1111l1_opy_ = framework_name
    logger.info(bstack1ll11lll1_opy_.format(bstack11l1111l1_opy_.split(bstack1lll11l_opy_ (u"ࠩ࠰ࠫᚦ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11ll11l1ll_opy_():
            Service.start = bstack1ll1ll111l_opy_
            Service.stop = bstack1ll11ll1l1_opy_
            webdriver.Remote.__init__ = bstack1ll111l11_opy_
            webdriver.Remote.get = bstack1llll11l11_opy_
            if not isinstance(os.getenv(bstack1lll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫᚧ")), str):
                return
            WebDriver.close = bstack1lll11111_opy_
            WebDriver.quit = bstack11111l11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1ll1lll11_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1l1l11l11l_opy_ = getAccessibilityResultsSummary
        if not bstack11ll11l1ll_opy_() and bstack1l11ll1ll_opy_.on():
            webdriver.Remote.__init__ = bstack1llll1l111_opy_
        bstack11l11l11_opy_ = True
    except Exception as e:
        pass
    bstack1ll1l1l1l1_opy_()
    if os.environ.get(bstack1lll11l_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩᚨ")):
        bstack11l11l11_opy_ = eval(os.environ.get(bstack1lll11l_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᚩ")))
    if not bstack11l11l11_opy_:
        bstack1l11ll11_opy_(bstack1lll11l_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣᚪ"), bstack11l1111l_opy_)
    if bstack11l11ll11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1llll11ll_opy_
        except Exception as e:
            logger.error(bstack1111lll1_opy_.format(str(e)))
    if bstack1lll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᚫ") in str(framework_name).lower():
        if not bstack11ll11l1ll_opy_():
            return
        try:
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
def bstack11111l11l_opy_(self):
    global bstack11l1111l1_opy_
    global bstack1l1lllll1l_opy_
    global bstack1l1l11ll_opy_
    try:
        if bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᚬ") in bstack11l1111l1_opy_ and self.session_id != None and bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ᚭ"), bstack1lll11l_opy_ (u"ࠪࠫᚮ")) != bstack1lll11l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᚯ"):
            bstack1l1l11lll_opy_ = bstack1lll11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᚰ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1lll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᚱ")
            bstack1llll1l11l_opy_(logger, True)
            if self != None:
                bstack1l1111l1_opy_(self, bstack1l1l11lll_opy_, bstack1lll11l_opy_ (u"ࠧ࠭ࠢࠪᚲ").join(threading.current_thread().bstackTestErrorMessages))
        threading.current_thread().testStatus = bstack1lll11l_opy_ (u"ࠨࠩᚳ")
    except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥᚴ") + str(e))
    bstack1l1l11ll_opy_(self)
    self.session_id = None
def bstack1ll111l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1lllll1l_opy_
    global bstack1l1ll1ll1_opy_
    global bstack1l111l1l_opy_
    global bstack11l1111l1_opy_
    global bstack1llll11l_opy_
    global bstack11l1ll1ll_opy_
    global bstack1l1l1l11_opy_
    global bstack1l1lllll11_opy_
    global bstack1llll11llll_opy_
    global bstack11l11ll1_opy_
    CONFIG[bstack1lll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᚵ")] = str(bstack11l1111l1_opy_) + str(__version__)
    command_executor = bstack11lll1l1l_opy_(bstack1l1l1l11_opy_)
    logger.debug(bstack111l1l1l_opy_.format(command_executor))
    proxy = bstack1l1ll1llll_opy_(CONFIG, proxy)
    bstack1l1lll1l1l_opy_ = 0
    try:
        if bstack1l111l1l_opy_ is True:
            bstack1l1lll1l1l_opy_ = int(os.environ.get(bstack1lll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᚶ")))
    except:
        bstack1l1lll1l1l_opy_ = 0
    bstack1ll11lll1l_opy_ = bstack1l11ll1l_opy_(CONFIG, bstack1l1lll1l1l_opy_)
    logger.debug(bstack11ll1l11_opy_.format(str(bstack1ll11lll1l_opy_)))
    bstack11l11ll1_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᚷ"))[bstack1l1lll1l1l_opy_]
    if bstack1lll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᚸ") in CONFIG and CONFIG[bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᚹ")]:
        bstack1ll11l11l1_opy_(bstack1ll11lll1l_opy_, bstack1l1lllll11_opy_)
    if desired_capabilities:
        bstack1l11lll1l_opy_ = bstack1lll1ll11_opy_(desired_capabilities)
        bstack1l11lll1l_opy_[bstack1lll11l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᚺ")] = bstack11ll1ll11_opy_(CONFIG)
        bstack1l1111l1l_opy_ = bstack1l11ll1l_opy_(bstack1l11lll1l_opy_)
        if bstack1l1111l1l_opy_:
            bstack1ll11lll1l_opy_ = update(bstack1l1111l1l_opy_, bstack1ll11lll1l_opy_)
        desired_capabilities = None
    if options:
        bstack11llllll1_opy_(options, bstack1ll11lll1l_opy_)
    if not options:
        options = bstack1lll1lll1_opy_(bstack1ll11lll1l_opy_)
    if bstack111ll11l1_opy_.bstack1lll1l11ll_opy_(CONFIG, bstack1l1lll1l1l_opy_) and bstack111ll11l1_opy_.bstack1lll1l11l_opy_(bstack1ll11lll1l_opy_, options):
        bstack1llll11llll_opy_ = True
        bstack111ll11l1_opy_.set_capabilities(bstack1ll11lll1l_opy_, CONFIG)
    if proxy and bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᚻ")):
        options.proxy(proxy)
    if options and bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᚼ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lll1ll1l_opy_() < version.parse(bstack1lll11l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᚽ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll11lll1l_opy_)
    logger.info(bstack1lll11ll1_opy_)
    if bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᚾ")):
        bstack1llll11l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᚿ")):
        bstack1llll11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧᛀ")):
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
        bstack1lll1ll11l_opy_ = bstack1lll11l_opy_ (u"ࠨࠩᛁ")
        if bstack1lll1ll1l_opy_() >= version.parse(bstack1lll11l_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪᛂ")):
            bstack1lll1ll11l_opy_ = self.caps.get(bstack1lll11l_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥᛃ"))
        else:
            bstack1lll1ll11l_opy_ = self.capabilities.get(bstack1lll11l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦᛄ"))
        if bstack1lll1ll11l_opy_:
            bstack1l1lll1l11_opy_(bstack1lll1ll11l_opy_)
            if bstack1lll1ll1l_opy_() <= version.parse(bstack1lll11l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬᛅ")):
                self.command_executor._url = bstack1lll11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᛆ") + bstack1l1l1l11_opy_ + bstack1lll11l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦᛇ")
            else:
                self.command_executor._url = bstack1lll11l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᛈ") + bstack1lll1ll11l_opy_ + bstack1lll11l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥᛉ")
            logger.debug(bstack1111ll11_opy_.format(bstack1lll1ll11l_opy_))
        else:
            logger.debug(bstack1l11l1l1_opy_.format(bstack1lll11l_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦᛊ")))
    except Exception as e:
        logger.debug(bstack1l11l1l1_opy_.format(e))
    bstack1l1lllll1l_opy_ = self.session_id
    if bstack1lll11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᛋ") in bstack11l1111l1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1l11ll1ll_opy_.bstack11111111l_opy_(self)
    bstack11l1ll1ll_opy_.append(self)
    if bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᛌ") in CONFIG and bstack1lll11l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᛍ") in CONFIG[bstack1lll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᛎ")][bstack1l1lll1l1l_opy_]:
        bstack1l1ll1ll1_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᛏ")][bstack1l1lll1l1l_opy_][bstack1lll11l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᛐ")]
    logger.debug(bstack1l11ll111_opy_.format(bstack1l1lllll1l_opy_))
def bstack1llll11l11_opy_(self, url):
    global bstack1ll1ll111_opy_
    global CONFIG
    try:
        bstack11llll11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1llll1ll1l_opy_.format(str(err)))
    try:
        bstack1ll1ll111_opy_(self, url)
    except Exception as e:
        try:
            bstack1lll1llll_opy_ = str(e)
            if any(err_msg in bstack1lll1llll_opy_ for err_msg in bstack11ll1ll1_opy_):
                bstack11llll11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1llll1ll1l_opy_.format(str(err)))
        raise e
def bstack111111lll_opy_(item, when):
    global bstack1l111l1ll_opy_
    try:
        bstack1l111l1ll_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll1llll_opy_(item, call, rep):
    global bstack11111llll_opy_
    global bstack11l1ll1ll_opy_
    name = bstack1lll11l_opy_ (u"ࠪࠫᛑ")
    try:
        if rep.when == bstack1lll11l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᛒ"):
            bstack1l1lllll1l_opy_ = threading.current_thread().bstackSessionId
            bstack1lllll1ll11_opy_ = item.config.getoption(bstack1lll11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᛓ"))
            try:
                if (str(bstack1lllll1ll11_opy_).lower() != bstack1lll11l_opy_ (u"࠭ࡴࡳࡷࡨࠫᛔ")):
                    name = str(rep.nodeid)
                    bstack1lll11lll_opy_ = bstack1l1l1l11ll_opy_(bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᛕ"), name, bstack1lll11l_opy_ (u"ࠨࠩᛖ"), bstack1lll11l_opy_ (u"ࠩࠪᛗ"), bstack1lll11l_opy_ (u"ࠪࠫᛘ"), bstack1lll11l_opy_ (u"ࠫࠬᛙ"))
                    os.environ[bstack1lll11l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᛚ")] = name
                    for driver in bstack11l1ll1ll_opy_:
                        if bstack1l1lllll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll11lll_opy_)
            except Exception as e:
                logger.debug(bstack1lll11l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ᛛ").format(str(e)))
            try:
                bstack11ll1l111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1lll11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᛜ"):
                    status = bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᛝ") if rep.outcome.lower() == bstack1lll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᛞ") else bstack1lll11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᛟ")
                    reason = bstack1lll11l_opy_ (u"ࠫࠬᛠ")
                    if status == bstack1lll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᛡ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1lll11l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᛢ") if status == bstack1lll11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᛣ") else bstack1lll11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᛤ")
                    data = name + bstack1lll11l_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫᛥ") if status == bstack1lll11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᛦ") else name + bstack1lll11l_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧᛧ") + reason
                    bstack11l111l11_opy_ = bstack1l1l1l11ll_opy_(bstack1lll11l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᛨ"), bstack1lll11l_opy_ (u"࠭ࠧᛩ"), bstack1lll11l_opy_ (u"ࠧࠨᛪ"), bstack1lll11l_opy_ (u"ࠨࠩ᛫"), level, data)
                    for driver in bstack11l1ll1ll_opy_:
                        if bstack1l1lllll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack11l111l11_opy_)
            except Exception as e:
                logger.debug(bstack1lll11l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭᛬").format(str(e)))
    except Exception as e:
        logger.debug(bstack1lll11l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧ᛭").format(str(e)))
    bstack11111llll_opy_(item, call, rep)
notset = Notset()
def bstack1llllll1l1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11llll1ll_opy_
    if str(name).lower() == bstack1lll11l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫᛮ"):
        return bstack1lll11l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦᛯ")
    else:
        return bstack11llll1ll_opy_(self, name, default, skip)
def bstack1llll11ll_opy_(self):
    global CONFIG
    global bstack1l1l11llll_opy_
    try:
        proxy = bstack1ll1ll1l11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1lll11l_opy_ (u"࠭࠮ࡱࡣࡦࠫᛰ")):
                proxies = bstack1l1l11ll11_opy_(proxy, bstack11lll1l1l_opy_())
                if len(proxies) > 0:
                    protocol, bstack111l1llll_opy_ = proxies.popitem()
                    if bstack1lll11l_opy_ (u"ࠢ࠻࠱࠲ࠦᛱ") in bstack111l1llll_opy_:
                        return bstack111l1llll_opy_
                    else:
                        return bstack1lll11l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᛲ") + bstack111l1llll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1lll11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨᛳ").format(str(e)))
    return bstack1l1l11llll_opy_(self)
def bstack11l11ll11_opy_():
    return (bstack1lll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᛴ") in CONFIG or bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᛵ") in CONFIG) and bstack1lll11lll1_opy_() and bstack1lll1ll1l_opy_() >= version.parse(
        bstack1lll1l111l_opy_)
def bstack1ll1111l1l_opy_(self,
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
    global bstack1l1ll1ll1_opy_
    global bstack1l111l1l_opy_
    global bstack11l1111l1_opy_
    CONFIG[bstack1lll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᛶ")] = str(bstack11l1111l1_opy_) + str(__version__)
    bstack1l1lll1l1l_opy_ = 0
    try:
        if bstack1l111l1l_opy_ is True:
            bstack1l1lll1l1l_opy_ = int(os.environ.get(bstack1lll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᛷ")))
    except:
        bstack1l1lll1l1l_opy_ = 0
    CONFIG[bstack1lll11l_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᛸ")] = True
    bstack1ll11lll1l_opy_ = bstack1l11ll1l_opy_(CONFIG, bstack1l1lll1l1l_opy_)
    logger.debug(bstack11ll1l11_opy_.format(str(bstack1ll11lll1l_opy_)))
    if CONFIG.get(bstack1lll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᛹")):
        bstack1ll11l11l1_opy_(bstack1ll11lll1l_opy_, bstack1l1lllll11_opy_)
    if bstack1lll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᛺") in CONFIG and bstack1lll11l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᛻") in CONFIG[bstack1lll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᛼")][bstack1l1lll1l1l_opy_]:
        bstack1l1ll1ll1_opy_ = CONFIG[bstack1lll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᛽")][bstack1l1lll1l1l_opy_][bstack1lll11l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᛾")]
    import urllib
    import json
    bstack111l1111l_opy_ = bstack1lll11l_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩ᛿") + urllib.parse.quote(json.dumps(bstack1ll11lll1l_opy_))
    browser = self.connect(bstack111l1111l_opy_)
    return browser
def bstack1ll1l1l1l1_opy_():
    global bstack11l11l11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1111l1l_opy_
        bstack11l11l11_opy_ = True
    except Exception as e:
        pass
def bstack1lllll1l1l1_opy_():
    global CONFIG
    global bstack111l1ll1_opy_
    global bstack1l1l1l11_opy_
    global bstack1l1lllll11_opy_
    global bstack1l111l1l_opy_
    CONFIG = json.loads(os.environ.get(bstack1lll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧᜀ")))
    bstack111l1ll1_opy_ = eval(os.environ.get(bstack1lll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪᜁ")))
    bstack1l1l1l11_opy_ = os.environ.get(bstack1lll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪᜂ"))
    bstack1l11l1l1l_opy_(CONFIG, bstack111l1ll1_opy_)
    bstack1lll1l11l1_opy_()
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
    if (bstack1lll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᜃ") in CONFIG or bstack1lll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᜄ") in CONFIG) and bstack1lll11lll1_opy_():
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
        logger.debug(bstack1lll11l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧᜅ"))
    bstack1l1lllll11_opy_ = CONFIG.get(bstack1lll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᜆ"), {}).get(bstack1lll11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᜇ"))
    bstack1l111l1l_opy_ = True
    bstack1lllll1ll1_opy_(bstack1111ll1l_opy_)
if (bstack11ll11l1l1_opy_()):
    bstack1lllll1l1l1_opy_()
@bstack1l1111l111_opy_(class_method=False)
def bstack1lllll11111_opy_(hook_name, event, bstack1llll1l1lll_opy_=None):
    if hook_name not in [bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᜈ"), bstack1lll11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᜉ"), bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᜊ"), bstack1lll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᜋ"), bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᜌ"), bstack1lll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᜍ"), bstack1lll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᜎ"), bstack1lll11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᜏ")]:
        return
    node = store[bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᜐ")]
    if hook_name in [bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᜑ"), bstack1lll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᜒ")]:
        node = store[bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬᜓ")]
    elif hook_name in [bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷ᜔ࠬ"), bstack1lll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴ᜕ࠩ")]:
        node = store[bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ᜖")]
    if event == bstack1lll11l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ᜗"):
        hook_type = bstack1111ll1lll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l11l111l1_opy_ = {
            bstack1lll11l_opy_ (u"ࠫࡺࡻࡩࡥࠩ᜘"): uuid,
            bstack1lll11l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ᜙"): bstack1ll11ll1l_opy_(),
            bstack1lll11l_opy_ (u"࠭ࡴࡺࡲࡨࠫ᜚"): bstack1lll11l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ᜛"),
            bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ᜜"): hook_type,
            bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ᜝"): hook_name
        }
        store[bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ᜞")].append(uuid)
        bstack1llll1lllll_opy_ = node.nodeid
        if hook_type == bstack1lll11l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᜟ"):
            if not _1l1111l11l_opy_.get(bstack1llll1lllll_opy_, None):
                _1l1111l11l_opy_[bstack1llll1lllll_opy_] = {bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᜠ"): []}
            _1l1111l11l_opy_[bstack1llll1lllll_opy_][bstack1lll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᜡ")].append(bstack1l11l111l1_opy_[bstack1lll11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᜢ")])
        _1l1111l11l_opy_[bstack1llll1lllll_opy_ + bstack1lll11l_opy_ (u"ࠨ࠯ࠪᜣ") + hook_name] = bstack1l11l111l1_opy_
        bstack1lllll11l1l_opy_(node, bstack1l11l111l1_opy_, bstack1lll11l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᜤ"))
    elif event == bstack1lll11l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᜥ"):
        bstack1l11llllll_opy_ = node.nodeid + bstack1lll11l_opy_ (u"ࠫ࠲࠭ᜦ") + hook_name
        _1l1111l11l_opy_[bstack1l11llllll_opy_][bstack1lll11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᜧ")] = bstack1ll11ll1l_opy_()
        bstack1lllll111l1_opy_(_1l1111l11l_opy_[bstack1l11llllll_opy_][bstack1lll11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᜨ")])
        bstack1lllll11l1l_opy_(node, _1l1111l11l_opy_[bstack1l11llllll_opy_], bstack1lll11l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᜩ"), bstack1lllll1ll1l_opy_=bstack1llll1l1lll_opy_)
def bstack1lllll1lll1_opy_():
    global bstack1lllll111ll_opy_
    if bstack1111l111_opy_():
        bstack1lllll111ll_opy_ = bstack1lll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᜪ")
    else:
        bstack1lllll111ll_opy_ = bstack1lll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᜫ")
@bstack1l11ll1ll_opy_.bstack1llllll1l1l_opy_
def bstack1llll1ll111_opy_():
    bstack1lllll1lll1_opy_()
    if bstack1lll11lll1_opy_():
        bstack1l1ll1l1_opy_(bstack111ll111l_opy_)
    bstack11l11l1lll_opy_ = bstack11l111llll_opy_(bstack1lllll11111_opy_)
bstack1llll1ll111_opy_()