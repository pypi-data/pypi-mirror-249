import re


def camel_to_underline(name):
    # 名称驼峰变成下划线
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def underline_to_camel(name):
    parts = name.split('_')
    return parts[0] + ''.join(v.title() for v in parts[1:])