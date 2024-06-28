from org_info.completer import OrgInfoCompleter
from org_info.papatto import Papatto

class OrgInfoGenerator:

    @staticmethod
    def generate(corp_number):
        org_infos = Papatto.get_org_infos(corp_number)
        completer = OrgInfoCompleter(org_infos)
        return completer.complete_org_infos(org_infos)
