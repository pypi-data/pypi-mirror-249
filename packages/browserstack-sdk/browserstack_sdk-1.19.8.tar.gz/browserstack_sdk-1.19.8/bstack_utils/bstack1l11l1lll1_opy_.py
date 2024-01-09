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
from uuid import uuid4
from bstack_utils.helper import bstack111l11lll_opy_, bstack11l1l1l11l_opy_
from bstack_utils.bstack1111lll1_opy_ import bstack1111l1l1ll_opy_
class bstack1l11l1l1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l1l111111_opy_=None, framework=None, tags=[], scope=[], bstack11111l111l_opy_=None, bstack111111l111_opy_=True, bstack11111l1ll1_opy_=None, bstack1ll111ll_opy_=None, result=None, duration=None, bstack1l11lll111_opy_=None, meta={}):
        self.bstack1l11lll111_opy_ = bstack1l11lll111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111111l111_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l1l111111_opy_ = bstack1l1l111111_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11111l111l_opy_ = bstack11111l111l_opy_
        self.bstack11111l1ll1_opy_ = bstack11111l1ll1_opy_
        self.bstack1ll111ll_opy_ = bstack1ll111ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l11l1ll1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111111l1l1_opy_(self):
        bstack11111l11l1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᐟ"): bstack11111l11l1_opy_,
            bstack11lllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᐠ"): bstack11111l11l1_opy_,
            bstack11lllll_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᐡ"): bstack11111l11l1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11lllll_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥᐢ") + key)
            setattr(self, key, val)
    def bstack111111lll1_opy_(self):
        return {
            bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨᐣ"): self.name,
            bstack11lllll_opy_ (u"ࠫࡧࡵࡤࡺࠩᐤ"): {
                bstack11lllll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᐥ"): bstack11lllll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᐦ"),
                bstack11lllll_opy_ (u"ࠧࡤࡱࡧࡩࠬᐧ"): self.code
            },
            bstack11lllll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᐨ"): self.scope,
            bstack11lllll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᐩ"): self.tags,
            bstack11lllll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᐪ"): self.framework,
            bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᐫ"): self.bstack1l1l111111_opy_
        }
    def bstack111111l11l_opy_(self):
        return {
         bstack11lllll_opy_ (u"ࠬࡳࡥࡵࡣࠪᐬ"): self.meta
        }
    def bstack11111l1111_opy_(self):
        return {
            bstack11lllll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᐭ"): {
                bstack11lllll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᐮ"): self.bstack11111l111l_opy_
            }
        }
    def bstack11111l1l1l_opy_(self, bstack1111111ll1_opy_, details):
        step = next(filter(lambda st: st[bstack11lllll_opy_ (u"ࠨ࡫ࡧࠫᐯ")] == bstack1111111ll1_opy_, self.meta[bstack11lllll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐰ")]), None)
        step.update(details)
    def bstack1111111l11_opy_(self, bstack1111111ll1_opy_):
        step = next(filter(lambda st: st[bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭ᐱ")] == bstack1111111ll1_opy_, self.meta[bstack11lllll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐲ")]), None)
        step.update({
            bstack11lllll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᐳ"): bstack111l11lll_opy_()
        })
    def bstack1l1l111l1l_opy_(self, bstack1111111ll1_opy_, result, duration=None):
        bstack11111l1ll1_opy_ = bstack111l11lll_opy_()
        if bstack1111111ll1_opy_ is not None and self.meta.get(bstack11lllll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐴ")):
            step = next(filter(lambda st: st[bstack11lllll_opy_ (u"ࠧࡪࡦࠪᐵ")] == bstack1111111ll1_opy_, self.meta[bstack11lllll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐶ")]), None)
            step.update({
                bstack11lllll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᐷ"): bstack11111l1ll1_opy_,
                bstack11lllll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᐸ"): duration if duration else bstack11l1l1l11l_opy_(step[bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᐹ")], bstack11111l1ll1_opy_),
                bstack11lllll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᐺ"): result.result,
                bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᐻ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111111ll11_opy_):
        if self.meta.get(bstack11lllll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐼ")):
            self.meta[bstack11lllll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐽ")].append(bstack111111ll11_opy_)
        else:
            self.meta[bstack11lllll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐾ")] = [ bstack111111ll11_opy_ ]
    def bstack111111ll1l_opy_(self):
        return {
            bstack11lllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᐿ"): self.bstack1l11l1ll1l_opy_(),
            **self.bstack111111lll1_opy_(),
            **self.bstack111111l1l1_opy_(),
            **self.bstack111111l11l_opy_()
        }
    def bstack11111l11ll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11lllll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᑀ"): self.bstack11111l1ll1_opy_,
            bstack11lllll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᑁ"): self.duration,
            bstack11lllll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᑂ"): self.result.result
        }
        if data[bstack11lllll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᑃ")] == bstack11lllll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᑄ"):
            data[bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᑅ")] = self.result.bstack11llll1l1l_opy_()
            data[bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᑆ")] = [{bstack11lllll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᑇ"): self.result.bstack11l1lll1l1_opy_()}]
        return data
    def bstack11111l1l11_opy_(self):
        return {
            bstack11lllll_opy_ (u"ࠬࡻࡵࡪࡦࠪᑈ"): self.bstack1l11l1ll1l_opy_(),
            **self.bstack111111lll1_opy_(),
            **self.bstack111111l1l1_opy_(),
            **self.bstack11111l11ll_opy_(),
            **self.bstack111111l11l_opy_()
        }
    def bstack1l11l11lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11lllll_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧᑉ") in event:
            return self.bstack111111ll1l_opy_()
        elif bstack11lllll_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᑊ") in event:
            return self.bstack11111l1l11_opy_()
    def bstack1l11l1l111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11111l1ll1_opy_ = time if time else bstack111l11lll_opy_()
        self.duration = duration if duration else bstack11l1l1l11l_opy_(self.bstack1l1l111111_opy_, self.bstack11111l1ll1_opy_)
        if result:
            self.result = result
class bstack1l111l1ll1_opy_(bstack1l11l1l1ll_opy_):
    def __init__(self, hooks=[], bstack1l11l11ll1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11l11ll1_opy_ = bstack1l11l11ll1_opy_
        super().__init__(*args, **kwargs, bstack1ll111ll_opy_=bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᑋ"))
    @classmethod
    def bstack1111111l1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11lllll_opy_ (u"ࠩ࡬ࡨࠬᑌ"): id(step),
                bstack11lllll_opy_ (u"ࠪࡸࡪࡾࡴࠨᑍ"): step.name,
                bstack11lllll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᑎ"): step.keyword,
            })
        return bstack1l111l1ll1_opy_(
            **kwargs,
            meta={
                bstack11lllll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ᑏ"): {
                    bstack11lllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᑐ"): feature.name,
                    bstack11lllll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᑑ"): feature.filename,
                    bstack11lllll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᑒ"): feature.description
                },
                bstack11lllll_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᑓ"): {
                    bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨᑔ"): scenario.name
                },
                bstack11lllll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᑕ"): steps,
                bstack11lllll_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᑖ"): bstack1111l1l1ll_opy_(test)
            }
        )
    def bstack1111111lll_opy_(self):
        return {
            bstack11lllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᑗ"): self.hooks
        }
    def bstack111111l1ll_opy_(self):
        if self.bstack1l11l11ll1_opy_:
            return {
                bstack11lllll_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᑘ"): self.bstack1l11l11ll1_opy_
            }
        return {}
    def bstack11111l1l11_opy_(self):
        return {
            **super().bstack11111l1l11_opy_(),
            **self.bstack1111111lll_opy_()
        }
    def bstack111111ll1l_opy_(self):
        return {
            **super().bstack111111ll1l_opy_(),
            **self.bstack111111l1ll_opy_()
        }
    def bstack1l11l1l111_opy_(self):
        return bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᑙ")
class bstack1l11l111ll_opy_(bstack1l11l1l1ll_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1ll111ll_opy_=bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᑚ"))
    def bstack1l1111l111_opy_(self):
        return self.hook_type
    def bstack111111llll_opy_(self):
        return {
            bstack11lllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᑛ"): self.hook_type
        }
    def bstack11111l1l11_opy_(self):
        return {
            **super().bstack11111l1l11_opy_(),
            **self.bstack111111llll_opy_()
        }
    def bstack111111ll1l_opy_(self):
        return {
            **super().bstack111111ll1l_opy_(),
            **self.bstack111111llll_opy_()
        }
    def bstack1l11l1l111_opy_(self):
        return bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ᑜ")