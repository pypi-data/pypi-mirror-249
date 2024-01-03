

import datetime

from register import FunctionRegister


def make_pt(dt):
    return dt


def phone_mask(name):
    import re

    # @output(names=[name], types=["string"])
    def h(r):
        if r is None or len(r.strip()) == 0:
            return "-"

        t = re.sub(r'\D', '', r)

        return t[:3] + '*' * 4 + t[-4:]
    return h


FunctionRegister.add("make_pt", make_pt)
FunctionRegister.add("datetime", datetime)
FunctionRegister.add("phone_mask", phone_mask)
