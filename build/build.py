#!/usr/bin/env python3
"""Rebuild questions.json and index.html from the part*.json sources.

    python3 build/build.py

Writes ../questions.json and ../index.html relative to this script.
"""
import json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def load():
    parts = sorted(glob.glob(os.path.join(HERE, 'part*.json')),
                   key=lambda p: int(re.search(r'part(\d+)', p).group(1)))
    qs = []
    for p in parts:
        qs += json.load(open(p, encoding='utf-8'))
    ids = [q['id'] for q in qs]
    assert ids == list(range(1, len(qs) + 1)), 'question ids must be contiguous from 1'
    for q in qs:
        assert 2 <= len(q['opts']) <= 4, q['id']
        assert all(0 <= i < len(q['opts']) for i in q['a']), q['id']
        assert (len(q['a']) > 1) == ('Choose' in q['q']), q['id']
        for k in ('q', 'why', 'wrong', 'ref'):
            assert q.get(k), (q['id'], k)
    return qs

def main():
    qs = load()
    json.dump(qs, open(os.path.join(ROOT, 'questions.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    body = tpl.replace('__DATA__', json.dumps(qs, ensure_ascii=False, separators=(',', ':')))
    title = re.search(r'<title>(.*?)</title>', body).group(1)
    links = re.findall(r'<link [^>]+>', body)
    for l in links:
        body = body.replace(l, '', 1)
    body = body.replace(f'<title>{title}</title>', '', 1)

    html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n' + '\n'.join(links) +
            '\n</head>\n<body>\n' + body.lstrip() + '\n</body>\n</html>\n')
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
    print(f'built {len(qs)} questions -> questions.json, index.html')

if __name__ == '__main__':
    main()
