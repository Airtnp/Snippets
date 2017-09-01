import re

rules = [
    ('bold', re.compile(r'\*\*')),
    ('link', re.compile(r'\[\[(.*?)\]\]')),
]

def tokenize(string):
    pos = 0
    last_end = 0
    while 1:
        if pos >= len(string):
            break
        for tok, rule in rules:
            match = rule.match(string, pos)
            if match is not None:
                start, end = match.span()
                if start > last_end:
                    yield 'text', string[last_end:start]
                yield tok, match.group()
                last_end = pos = match.end()
                break
        else:
            pos += 1
    if last_end < len(string):
        yield 'text', string[last_end:]