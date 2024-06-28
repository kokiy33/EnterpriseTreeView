from org_info.generator import OrgInfoGenerator

if __name__ == '__main__':
    org_infos = OrgInfoGenerator.generate(corp_number='3180301014273')
    for org_info in org_infos[:10]:
        print(org_info)
