#!/usr/bin/env python3
import re


_DICE_EXPR = re.compile(r'^\s*(\d*[dдк]?\d+)', re.UNICODE)
_OP_EXPR = re.compile(r'^\s*([-+])', re.UNICODE)
_DIE_SUB = re.compile(r'[дк]', re.UNICODE)


def parse(expression):
    result = []
    first_dice_match = _DICE_EXPR.search(expression)
    if first_dice_match is not None:
        result.append(_DIE_SUB.sub('d', first_dice_match.group(1)))
        anchor = first_dice_match.end()
    else:
        result.append('2d6')
        anchor = 0
    while True:
        op_match = _OP_EXPR.search(expression[anchor:])
        if op_match is None:
            break
        dice_anchor = anchor + op_match.end()
        dice_match = _DICE_EXPR.search(expression[dice_anchor:])
        if dice_match is None:
            break
        result.append(op_match.group(1))
        result.append(_DIE_SUB.sub('d', dice_match.group(1)))
        anchor = dice_anchor + dice_match.end()
    return result, expression[anchor:].strip()


if __name__ == '__main__':
    for test in ["3d6", ' 3d6', ' +1', '+1огонь', '+2test 2d6 + 2!', '+лов', 'd4 test', 'd2 d3']:
        print("[%s]\t" % test, parse(test))
