import re

from org_info.completer import OrgInfoCompleter
from org_info.model import OrgInfo
from org_info.pattern import ORG_INFO_PATTERNS
from org_info.text_nomalizer import TextNormalizer

class BusyoParser:

    def __init__(self, completer: OrgInfoCompleter=None):
        self.completer = completer
        self.normalizer = TextNormalizer()

    @staticmethod
    def _preprocess_busyo(busyo):
        busyo = re.sub(r"長$", "", busyo)
        busyo = re.sub(r"兼", "部", busyo)
        busyo = re.sub(r"副工場", "工場", busyo)
        busyo = re.sub(r"(理事|執行職|役員)", r"\1;", busyo)

        for pattern in ORG_INFO_PATTERNS.values():
            busyo = re.sub(f"({pattern})", r"\1;", busyo)

        return busyo

    def parse_busyo(self, busyo) -> OrgInfo:
        busyo = self._preprocess_busyo(busyo)

        org_info = OrgInfo({hierarchy: "" for hierarchy in ORG_INFO_PATTERNS})
        for hierarchy in ORG_INFO_PATTERNS:
            pattern = ORG_INFO_PATTERNS[hierarchy]
            match = re.search(f"\w[\w&＆・]*({pattern})", busyo)
            if match:
                org_info[hierarchy] = self.normalizer.normalize(match.group(0))

        if self.completer:
            return self.completer.complete_org_info(org_info)

        return org_info