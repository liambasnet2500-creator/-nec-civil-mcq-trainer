"""Parse NEC Civil Chapterwise Repeated MCQs PDF into a raw JSON question bank."""
import json, re, sys, collections
import pymupdf as fitz
from wordfreq import zipf_frequency

PDF = 'nec.pdf'
PUA = {
    '': '(', '': ')', '': ':', '': '[', '': ']',
    '': '+', '': '×', '': '≈', '': '–', '': '≥',
}
TEAL, GREEN, GREY, RED, WHITE = 0x0b5563, 0x1f6f3f, 0x5f6b73, 0xb3261e, 0xffffff
MID_X = 297.6


def fix(s):
    for k, v in PUA.items():
        s = s.replace(k, v)
    return s


def span_text(s):
    """Rebuild span text from chars, inserting spaces where glyphs are visibly separated."""
    out = ''
    prev = None
    for c in s['chars']:
        ch = c['c']
        if prev is not None and ch != ' ' and not out.endswith(' '):
            gap = c['bbox'][0] - prev['bbox'][2]
            if gap > 0.18 * s['size']:
                out += ' '
        out += ch
        prev = c
    return fix(out)


def spans_of(page):
    out = []
    d = page.get_text('rawdict')
    for b in d['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                if not s['chars']:
                    continue
                t = span_text(s)
                x0, y0, x1, y1 = s['bbox']
                out.append(dict(t=t, x0=x0, y0=y0, x1=x1, y1=y1,
                                font=s['font'], size=round(s['size'], 1), color=s['color'],
                                base=round(s['origin'][1], 1)))
    return out


def classify(s):
    f, z, c = s['font'], s['size'], s['color']
    if z == 9.3 and c == WHITE:
        return 'chapter'
    if f.endswith('Medium') and c == WHITE:
        return 'chapter_code'
    if z == 5.6 and c == GREY:
        return 'meta'
    if f.endswith('ExtraBold') and z == 8.3 and c == TEAL:
        return 'num'
    if f.endswith('ExtraBold') and z == 5.2 and c == WHITE:
        return 'badge'
    if f.endswith('ExtraBold') and z == 5.2 and c == RED:
        return 'wording'
    if f.endswith('ExtraBold') and z == 7.4 and c == TEAL:
        return 'optletter'
    if f.endswith('ExtraBold') and z == 7.4 and c == GREEN:
        return 'check'
    if c == GREEN:
        return 'anstext'
    if z == 5.6 and c == RED:
        return 'note'
    if c == GREY and z <= 7.6:
        return 'reason'
    if z == 8.3 and c == 0:
        return 'stem'
    if c == 0 and z in (7.4, 7.6):
        return 'opt'
    if 'DejaVu' in f and c == 0:
        return 'opt'
    return 'other'


def build_stream(doc):
    stream = []
    for pn in range(1, 30):
        page = doc[pn]
        sp = [s for s in spans_of(page) if 25 < s['y0'] < 812]
        for s in sp:
            s['k'] = classify(s)
            s['page'] = pn + 1
        banners = sorted({round(s['y0']) for s in sp if s['k'] == 'chapter'})
        cuts = [0] + [b - 8 for b in banners] + [10000]
        for i in range(len(cuts) - 1):
            lo, hi = cuts[i], cuts[i + 1]
            band = [s for s in sp if lo <= s['y0'] < hi]
            ban = [s for s in band if s['k'] in ('chapter', 'chapter_code')]
            rest = [s for s in band if s['k'] not in ('chapter', 'chapter_code')]
            stream.extend(sorted(ban, key=lambda s: s['x0']))
            for col in (0, 1):
                cs = [s for s in rest if (s['x0'] >= MID_X - 2) == bool(col)]
                for s in cs:
                    s['col'] = col
                # badges sit ~3pt below the text baseline; snap them to their line
                for s in cs:
                    s['line'] = s['base']
                for l in lines_of(cs):
                    stream.extend(l)
    return stream


def lines_of(spans, tol=1.6):
    """Group spans into visual lines (list of lists) preserving order."""
    lines = []
    for s in sorted(spans, key=lambda s: (s['line'], s['x0'])):
        if lines and abs(lines[-1][0]['line'] - s['line']) <= tol:
            lines[-1].append(s)
        else:
            lines.append([s])
    for l in lines:
        l.sort(key=lambda s: s['x0'])
    return lines


def lines_in_order(spans, tol=1.6):
    """Group spans into lines keeping stream (reading) order; a new line starts on page/column/baseline change."""
    lines = []
    for s in spans:
        if lines:
            last = lines[-1][-1]
            if last['page'] == s['page'] and last.get('col') == s.get('col') and abs(lines[-1][0]['line'] - s['line']) <= tol:
                lines[-1].append(s)
                continue
        lines.append([s])
    for l in lines:
        l.sort(key=lambda s: s['x0'])
    return lines


def join_line(spans):
    out = ''
    prev = None
    for s in spans:
        t = s['t']
        if prev is not None and out and not out.endswith(' ') and not t.startswith(' '):
            if s['x0'] - prev['x1'] > 1.2:
                out += ' '
        out += t
        prev = s
    return re.sub(r'\s+', ' ', out).strip()


HYPH_LOG = []


def join_lines(texts):
    out = ''
    for t in texts:
        t = t.strip()
        if not t:
            continue
        if not out:
            out = t
            continue
        m = re.search(r'([A-Za-z]+)-$', out)
        if m and re.match(r'[a-z]', t):
            left = m.group(1)
            right = re.match(r'[A-Za-z]+', t).group(0)
            joined = (left + right).lower()
            zj = zipf_frequency(joined, 'en')
            zl, zr = zipf_frequency(left.lower(), 'en'), zipf_frequency(right.lower(), 'en')
            keep = False
            if zj < 1.8 and zl > 2.5 and zr > 2.5 and len(left) > 1 and len(right) > 2:
                keep = True
            HYPH_LOG.append((left, right, 'KEEP' if keep else 'JOIN', zj))
            out = out + t if keep else out[:-1] + t
        elif out[-1] in '-–—/' and len(out) > 1 and out[-2] != ' ':
            out = out + t
        else:
            out = out + ' ' + t
    return out


def parse(stream):
    qs = []
    cur = None
    ch = None
    sub = None
    subs = {}
    chapters = {}
    i = 0
    n = len(stream)
    while i < n:
        s = stream[i]
        k = s['k']
        if k == 'chapter':
            if re.fullmatch(r'\s*\d+\s*', s['t']):
                ch = int(s['t'])
                chapters[ch] = ''
            else:
                chapters[ch] = (chapters.get(ch, '') + s['t']).strip()
            cur = None
            i += 1
            continue
        if k == 'num' and re.fullmatch(r'\d+\.\d+', s['t'].strip()):
            sub = s['t'].strip()
            title = ''
            j = i + 1
            while j < n and stream[j]['k'] == 'num' and abs(stream[j]['base'] - s['base']) < 1:
                title += stream[j]['t']
                j += 1
            info = ''
            while j < n and stream[j]['k'] == 'meta' and abs(stream[j]['base'] - s['base']) < 4:
                info += stream[j]['t']
                j += 1
            subs[sub] = dict(name=title.strip(), info=info.strip(), ch=ch)
            cur = None
            i = j
            continue
        if k == 'num' and re.fullmatch(r'\s*\d+\s*', s['t']):
            cur = dict(id=int(s['t']), ch=ch, sub=sub, spans=[], page=s['page'], col=s['col'])
            qs.append(cur)
            i += 1
            continue
        if k == 'num' and s['t'].strip() == '':
            i += 1
            continue
        if cur is not None and k not in ('meta', 'chapter_code'):
            cur['spans'].append(s)
        elif k not in ('meta', 'chapter_code') and s['t'].strip():
            print('ORPHAN', s['page'], k, repr(s['t']), file=sys.stderr)
        i += 1
    return qs, subs, chapters


def assemble(q):
    sp = q['spans']
    badges = [s['t'].strip() for s in sp if s['k'] == 'badge' and s['t'].strip()]
    wording = any(s['k'] == 'wording' and 'WORDING' in s['t'] for s in sp)
    # split regions
    check_i = next((i for i, s in enumerate(sp) if s['k'] == 'check'), None)
    pre = sp[:check_i] if check_i is not None else sp
    post = sp[check_i:] if check_i is not None else []
    stem_sp = [s for s in pre if s['k'] == 'stem']
    stem = join_lines([join_line(l) for l in lines_in_order(stem_sp)])
    # options
    letters = [s for s in pre if s['k'] == 'optletter' and s['t'].strip() in 'ABCD' and s['t'].strip()]
    opt_sp = [s for s in pre if s['k'] == 'opt']
    cells = collections.OrderedDict()
    for L in letters:
        cells[L['t'].strip()] = dict(L=L, lines=collections.OrderedDict())
    letter_lines = sorted({round(L['line'], 1) for L in letters})
    issues = []
    for s in opt_sp:
        # most recent letter line at or above this span
        cand_lines = [y for y in letter_lines if y <= s['line'] + 1.6]
        if not cand_lines:
            issues.append('opt-before-letters:' + s['t'])
            continue
        y = cand_lines[-1]
        row = [L for L in letters if abs(round(L['line'], 1) - y) <= 1.6]
        row_ok = [L for L in row if L['x0'] <= s['x0'] + 2]
        if not row_ok:
            issues.append('opt-unplaced:' + s['t'])
            continue
        L = max(row_ok, key=lambda L: L['x0'])
        cell = cells[L['t'].strip()]
        key = round(s['line'])
        cell['lines'].setdefault(key, []).append(s)
    options = {}
    for letter, cell in cells.items():
        texts = [join_line(v) for kk, v in sorted(cell['lines'].items())]
        options[letter] = join_lines(texts)
    # answer
    ans = None
    anstext = ''
    reason = ''
    note = ''
    if post:
        ans = post[0]['t'].replace('✓', '').strip()
        rest = post[1:]
        green = [s for s in rest if s['k'] == 'anstext']
        grey = [s for s in rest if s['k'] in ('reason',)]
        notes = [s for s in rest if s['k'] == 'note']
        other = [s for s in rest if s['k'] not in ('anstext', 'reason', 'note', 'wording', 'badge')]
        if other:
            issues.append('post-other:' + '|'.join(s['k'] + ':' + s['t'] for s in other))
        # anstext + reason share lines; rebuild line by line keeping colour segments
        comb = [s for s in rest if s['k'] in ('anstext', 'reason')]
        segs = []
        for l in lines_in_order(comb):
            # split line into green-run then grey-run
            g = [s for s in l if s['k'] == 'anstext']
            r = [s for s in l if s['k'] == 'reason']
            segs.append((join_line(g), join_line(r)))
        gtexts = [a for a, b in segs if a]
        rtexts = [b for a, b in segs if b]
        anstext = join_lines(gtexts)
        reason = join_lines(rtexts)
        reason = re.sub(r'^[–-]\s*', '', reason.strip())
        if notes:
            nt = join_lines([join_line(l) for l in lines_in_order(notes)])
            note = re.sub(r'^NOTE\s*', '', nt).strip()
    if any(s['k'] == 'other' for s in sp):
        issues.append('other-span')
    return dict(id=q['id'], ch=q['ch'], sub=q['sub'], badges=badges, wording=wording,
                stem=stem, options=options, check=ans, anstext=anstext, reason=reason,
                note=note, page=q['page'], issues=issues)


def answer_key(doc):
    t = ''
    for pn in (30,):
        t += fix(doc[pn].get_text())
    key = {}
    for m in re.finditer(r'(?<![\d.])(\d{1,3})\s*([ABCD])\b', t):
        key[int(m.group(1))] = m.group(2)
    return key


if __name__ == '__main__':
    doc = fitz.open(PDF)
    stream = build_stream(doc)
    qs, subs, chapters = parse(stream)
    out = [assemble(q) for q in qs]
    key = answer_key(doc)
    json.dump(dict(questions=out, subs=subs, chapters=chapters, key=key),
              open('raw_bank.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(HYPH_LOG, open('hyph_log.json', 'w'), ensure_ascii=False)
    print('questions', len(out), 'key', len(key), 'subs', len(subs))
    print(chapters)
    ids = [q['id'] for q in out]
    print('missing ids', sorted(set(range(1, 647)) - set(ids)), 'dups', [x for x, c in collections.Counter(ids).items() if c > 1])
    for q in out:
        if q['issues'] or len(q['options']) != 4 or not q['check'] or not q['stem']:
            print('ISSUE', q['id'], q['issues'], list(q['options'].keys()), q['check'], q['stem'][:50])
