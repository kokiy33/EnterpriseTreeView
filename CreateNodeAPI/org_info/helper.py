from org_info.model import OrgInfo

def remove_duplicates(items: list[OrgInfo]):
    """
    階層構造の重複を削除する
    """
    def is_subset(dic1, dic2):
        s1 = set([v for v in dic1.values() if v])
        s2 = set([v for v in dic2.values() if v])
        return s1 < s2

    new_items = []
    s = set()
    for item in items:
        if any(is_subset(item, tmp) for tmp in items):
            continue

        v = tuple(item.values())
        if v in s:
            continue

        s.add(v)
        new_items.append(item)

    return new_items