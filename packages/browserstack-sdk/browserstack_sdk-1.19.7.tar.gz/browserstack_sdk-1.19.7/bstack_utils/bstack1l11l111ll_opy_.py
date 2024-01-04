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
from uuid import uuid4
from bstack_utils.helper import bstack111l11ll1_opy_, bstack11l1l1l11l_opy_
from bstack_utils.bstack1l1ll1ll1_opy_ import bstack1111ll11ll_opy_
class bstack1l11l1ll11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111l111l_opy_=None, framework=None, tags=[], scope=[], bstack1111111l11_opy_=None, bstack11111l111l_opy_=True, bstack11111l1111_opy_=None, bstack1lll1l111_opy_=None, result=None, duration=None, bstack1l111lll1l_opy_=None, meta={}):
        self.bstack1l111lll1l_opy_ = bstack1l111lll1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack11111l111l_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111l111l_opy_ = bstack1l111l111l_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111111l11_opy_ = bstack1111111l11_opy_
        self.bstack11111l1111_opy_ = bstack11111l1111_opy_
        self.bstack1lll1l111_opy_ = bstack1lll1l111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l11lll111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111111l1ll_opy_(self):
        bstack111111ll1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᐞ"): bstack111111ll1l_opy_,
            bstack111ll11_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᐟ"): bstack111111ll1l_opy_,
            bstack111ll11_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᐠ"): bstack111111ll1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111ll11_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᐡ") + key)
            setattr(self, key, val)
    def bstack1111111ll1_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᐢ"): self.name,
            bstack111ll11_opy_ (u"ࠪࡦࡴࡪࡹࠨᐣ"): {
                bstack111ll11_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᐤ"): bstack111ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᐥ"),
                bstack111ll11_opy_ (u"࠭ࡣࡰࡦࡨࠫᐦ"): self.code
            },
            bstack111ll11_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᐧ"): self.scope,
            bstack111ll11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᐨ"): self.tags,
            bstack111ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᐩ"): self.framework,
            bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᐪ"): self.bstack1l111l111l_opy_
        }
    def bstack11111l1l11_opy_(self):
        return {
         bstack111ll11_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᐫ"): self.meta
        }
    def bstack1111111lll_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᐬ"): {
                bstack111ll11_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᐭ"): self.bstack1111111l11_opy_
            }
        }
    def bstack11111l1ll1_opy_(self, bstack111111ll11_opy_, details):
        step = next(filter(lambda st: st[bstack111ll11_opy_ (u"ࠧࡪࡦࠪᐮ")] == bstack111111ll11_opy_, self.meta[bstack111ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐯ")]), None)
        step.update(details)
    def bstack111111l1l1_opy_(self, bstack111111ll11_opy_):
        step = next(filter(lambda st: st[bstack111ll11_opy_ (u"ࠩ࡬ࡨࠬᐰ")] == bstack111111ll11_opy_, self.meta[bstack111ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐱ")]), None)
        step.update({
            bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᐲ"): bstack111l11ll1_opy_()
        })
    def bstack1l1l111111_opy_(self, bstack111111ll11_opy_, result, duration=None):
        bstack11111l1111_opy_ = bstack111l11ll1_opy_()
        if bstack111111ll11_opy_ is not None and self.meta.get(bstack111ll11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐳ")):
            step = next(filter(lambda st: st[bstack111ll11_opy_ (u"࠭ࡩࡥࠩᐴ")] == bstack111111ll11_opy_, self.meta[bstack111ll11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐵ")]), None)
            step.update({
                bstack111ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᐶ"): bstack11111l1111_opy_,
                bstack111ll11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᐷ"): duration if duration else bstack11l1l1l11l_opy_(step[bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᐸ")], bstack11111l1111_opy_),
                bstack111ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᐹ"): result.result,
                bstack111ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᐺ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111111l1l_opy_):
        if self.meta.get(bstack111ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐻ")):
            self.meta[bstack111ll11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐼ")].append(bstack1111111l1l_opy_)
        else:
            self.meta[bstack111ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐽ")] = [ bstack1111111l1l_opy_ ]
    def bstack111111lll1_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᐾ"): self.bstack1l11lll111_opy_(),
            **self.bstack1111111ll1_opy_(),
            **self.bstack111111l1ll_opy_(),
            **self.bstack11111l1l11_opy_()
        }
    def bstack111111l11l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᐿ"): self.bstack11111l1111_opy_,
            bstack111ll11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᑀ"): self.duration,
            bstack111ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᑁ"): self.result.result
        }
        if data[bstack111ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᑂ")] == bstack111ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᑃ"):
            data[bstack111ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᑄ")] = self.result.bstack11llll1l1l_opy_()
            data[bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᑅ")] = [{bstack111ll11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᑆ"): self.result.bstack11l1l1ll11_opy_()}]
        return data
    def bstack111111llll_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩᑇ"): self.bstack1l11lll111_opy_(),
            **self.bstack1111111ll1_opy_(),
            **self.bstack111111l1ll_opy_(),
            **self.bstack111111l11l_opy_(),
            **self.bstack11111l1l11_opy_()
        }
    def bstack1l111llll1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111ll11_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᑈ") in event:
            return self.bstack111111lll1_opy_()
        elif bstack111ll11_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᑉ") in event:
            return self.bstack111111llll_opy_()
    def bstack1l11l1l11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11111l1111_opy_ = time if time else bstack111l11ll1_opy_()
        self.duration = duration if duration else bstack11l1l1l11l_opy_(self.bstack1l111l111l_opy_, self.bstack11111l1111_opy_)
        if result:
            self.result = result
class bstack1l11lllll1_opy_(bstack1l11l1ll11_opy_):
    def __init__(self, hooks=[], bstack1l11l1l1ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11l1l1ll_opy_ = bstack1l11l1l1ll_opy_
        super().__init__(*args, **kwargs, bstack1lll1l111_opy_=bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࠬᑊ"))
    @classmethod
    def bstack11111l1l1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111ll11_opy_ (u"ࠨ࡫ࡧࠫᑋ"): id(step),
                bstack111ll11_opy_ (u"ࠩࡷࡩࡽࡺࠧᑌ"): step.name,
                bstack111ll11_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᑍ"): step.keyword,
            })
        return bstack1l11lllll1_opy_(
            **kwargs,
            meta={
                bstack111ll11_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᑎ"): {
                    bstack111ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᑏ"): feature.name,
                    bstack111ll11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᑐ"): feature.filename,
                    bstack111ll11_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᑑ"): feature.description
                },
                bstack111ll11_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᑒ"): {
                    bstack111ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᑓ"): scenario.name
                },
                bstack111ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᑔ"): steps,
                bstack111ll11_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᑕ"): bstack1111ll11ll_opy_(test)
            }
        )
    def bstack111111l111_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᑖ"): self.hooks
        }
    def bstack11111l11ll_opy_(self):
        if self.bstack1l11l1l1ll_opy_:
            return {
                bstack111ll11_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᑗ"): self.bstack1l11l1l1ll_opy_
            }
        return {}
    def bstack111111llll_opy_(self):
        return {
            **super().bstack111111llll_opy_(),
            **self.bstack111111l111_opy_()
        }
    def bstack111111lll1_opy_(self):
        return {
            **super().bstack111111lll1_opy_(),
            **self.bstack11111l11ll_opy_()
        }
    def bstack1l11l1l11l_opy_(self):
        return bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᑘ")
class bstack1l1111ll1l_opy_(bstack1l11l1ll11_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1lll1l111_opy_=bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᑙ"))
    def bstack1l11llll1l_opy_(self):
        return self.hook_type
    def bstack11111l11l1_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᑚ"): self.hook_type
        }
    def bstack111111llll_opy_(self):
        return {
            **super().bstack111111llll_opy_(),
            **self.bstack11111l11l1_opy_()
        }
    def bstack111111lll1_opy_(self):
        return {
            **super().bstack111111lll1_opy_(),
            **self.bstack11111l11l1_opy_()
        }
    def bstack1l11l1l11l_opy_(self):
        return bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬᑛ")