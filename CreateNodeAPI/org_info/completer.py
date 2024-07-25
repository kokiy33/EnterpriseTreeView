from org_info.model import OrgInfo
from typing import List

class OrgInfoCompleter:

    def __init__(self, items: list[OrgInfo]):
        self.items: list[OrgInfo] = items
        self.set_map()

    def set_div2hq(self):
        self.div2hq = {}
        for item in self.items:
            hq = item["headquarter"]
            div = item["division"]

            if div and hq:
                self.div2hq[div] = hq

    def set_dep2hq_div(self):
        self.dep2hq_div = {}
        for item in self.items:
            hq = item["headquarter"]
            div = item["division"]
            dep = item["department"]

            if dep and (hq or div):
                self.dep2hq_div[dep] = (hq, div)

    def set_hq_dep2div(self):
        self.hq_dep2div = {}
        for item in self.items:
            hq = item["headquarter"]
            div = item["division"]
            dep = item["department"]

            if hq and dep and div:
                self.hq_dep2div[(hq, dep)] = div

    def set_map(self):
        self.set_div2hq()
        self.items = [self.complete_hq(item) for item in self.items]

        self.set_dep2hq_div()
        self.items = [self.comlete_hq_and_div(item) for item in self.items]

        self.set_hq_dep2div()
        self.items = [self.complete_div(item) for item in self.items]

    def complete_hq(self, dic: OrgInfo):
        hq = dic["headquarter"]
        div = dic["division"]

        hq = self.div2hq.get(div, hq)
        dic["headquarter"] = hq

        return dic

    def comlete_hq_and_div(self, dic: OrgInfo):
        hq = dic["headquarter"]
        div = dic["division"]
        dep = dic["department"]

        if hq or div:
            return dic

        hq, div = self.dep2hq_div.get(dep, (hq, div)) if dep else (hq, div)
        dic["headquarter"] = hq
        dic["division"] = div

        return dic

    def complete_div(self, dic: OrgInfo):
        hq = dic["headquarter"]
        div = dic["division"]
        dep = dic["department"]

        if div:
            return dic

        div = self.hq_dep2div.get((hq, dep), div)
        dic["division"] = div

        return dic

    def complete_org_info(self, dic: OrgInfo):
        dic = self.complete_hq(dic)
        dic = self.comlete_hq_and_div(dic)
        dic = self.complete_div(dic)
        return dic

    def complete_org_infos(self, items: list[OrgInfo]):
        return [self.complete_org_info(item) for item in items]