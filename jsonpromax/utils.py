import re


def rm_ascii(s):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    return ''.join(pattern.findall(s))


def camel_to_snake(s):
    up_index = []
    for i, c in enumerate(s):
        if c.isupper():
            up_index.append(i)  # 获取大写字符索引位置
    ls = s.lower()  # 原字符串转小写
    # print(ls)
    list_ls = list(ls)  # 转列表
    if up_index:
        addi = 0
        for g in up_index:
            list_ls.insert(g + addi, '_')  # 插入_
            addi += 1
    last_ls = ''.join(list_ls)  # 转回字符
    # print(last_ls)
    return last_ls


def unstructurize_dict(d, preserved=None, start_level=0, end_level=0):
    output = {}
    for k, v in d.items():
        if preserved and k in preserved:
            output[k] = v
            continue
        temp = output
        k_split = camel_to_snake(k).split('_')[start_level:]
        if len(k_split) < end_level + 1:
            continue
        for kk in k_split[:-(end_level+1)]:
            if kk not in temp:
                temp[kk] = {}
            temp = temp[kk]
        temp[k_split[-(end_level+1)]] = v
    return output


def get_json_depth(obj, depth=0):
    if isinstance(obj, list):
        if len(obj) > 0:
            return max(get_json_depth(item, depth+1) for item in obj)
        else:
            return depth
    elif isinstance(obj, dict):
        if len(obj) > 0:
            return max(get_json_depth(item, depth+1) for item in obj.values())
        else:
            return depth
    else:
        return depth
