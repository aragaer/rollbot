from random import randint

class Die(object):

    def __init__(self, sides):
        self._sides = sides

    def roll(self, times):
        return tuple(randint(1, self._sides) for _ in range(times))


def roll(tokens):
    result = []
    for token in tokens:
        if 'd' in token:
            count, sides = token.split('d')
            count = int(count) if count else 1
            result.append(tuple(Die(int(sides)).roll(count)))
        else:
            try:
                result.append(int(token))
            except:
                result.append(token)

    return result


def _count1(token):
    if type(token) is tuple:
        return sum(token)
    else:
        return token


def count(tokens):
    if not tokens:
        return 0

    result = _count1(tokens[0])
    for op, token in zip(tokens[1::2], tokens[2::2]):
        if op == '+':
            result += _count1(token)
        else:
            result -= _count1(token)
    return result
