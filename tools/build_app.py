"""Assemble nec-civil-quiz.html from app_template.html + bank.json + KaTeX JS and CSS (fonts embedded)."""
import json, re, base64, sys
bank = json.load(open('bank.json'))
raw = json.load(open('raw_bank.json'))
codes = ['ACiE01', 'ACiE02', 'ACiE03', 'ACiE04', 'ACiE05', 'ACiE06', 'ACiE07', 'ACiE08', 'ACiE09', 'AALL10']
meta = {'chapters': {str(c): {'name': raw['chapters'][str(c)], 'code': codes[c - 1]} for c in range(1, 11)},
        'subs': {k: v['name'] for k, v in raw['subs'].items()}}
KEYS = ['id', 'ch', 'sub', 'subName', 'r', 'tags', 'wording', 'conceptId', 'stem', 'options', 'ans', 'reason', 'note']
bank = [{k: q[k] for k in KEYS} for q in bank]
def js(o):
    return json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
css = open('node_modules/katex/dist/katex.min.css').read()
EMBED = ['Main-Regular', 'Main-Italic', 'Main-Bold', 'Math-Italic', 'AMS-Regular', 'Size1-Regular', 'Size2-Regular',
         'Size3-Regular', 'Size4-Regular']
def face(m):
    block = m.group(0)
    fam = re.search(r'url\(fonts/KaTeX_([A-Za-z0-9-]+)\.woff2\)', block)
    if not fam or fam.group(1) not in EMBED:
        return ''
    data = base64.b64encode(open('node_modules/katex/dist/fonts/KaTeX_%s.woff2' % fam.group(1), 'rb').read()).decode()
    return re.sub(r'src:[^;}]*', 'src:url(data:font/woff2;base64,%s) format("woff2")' % data, block)
css = re.sub(r'@font-face\{[^}]*\}', face, css)
assert 'url(fonts/' not in css
tpl = open('app_template.html').read()
kjs = open('node_modules/katex/dist/katex.min.js').read()
assert '</script' not in kjs.lower() and '<!--' not in kjs
out = tpl.replace('/*__KATEX_CSS__*/', css).replace('__BANK__', js(bank)).replace('__META__', js(meta))
assert out.count('/*__KATEX_JS__*/') == 1
out = out.replace('/*__KATEX_JS__*/', kjs)
dest = sys.argv[1] if len(sys.argv) > 1 else 'nec-civil-quiz.html'
open(dest, 'w').write(out)
print(dest, len(out.encode()) // 1024, 'KB')
