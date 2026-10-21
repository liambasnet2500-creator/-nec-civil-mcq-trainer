"""Build the final question bank (bank.json) from raw_bank.json."""
import json, re, collections, importlib, sys
import tex
import overrides as O

FIELDS_OPT = 'ABCD'


def clean(s):
    if not s:
        return s
    s = re.sub(r'(?<=[A-Za-z0-9])– (?=[A-Za-z0-9])', '–', s)
    # opening quotes extracted as closing glyphs
    s = re.sub(r'(^|[\s(\[])’', r'\1‘', s)
    s = re.sub(r'(^|[\s(\[])”', r'\1“', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


R_MAP = {'R7': 7, 'R6': 6, 'R5': 5, 'R4': 4, 'R3': 3, 'R2': 2, 'R1': 1, 'OLD': 0}
TAG_MAP = {'NEC': ['NEC'], '2080 M': ['2080M'], '2080 C': ['2080C'], '2080 M+C': ['2080M', '2080C'],
           'NEC model': ['model']}


def build():
    raw = json.load(open('raw_bank.json'))
    subs = raw['subs']
    out = []
    for q in raw['questions']:
        qid = q['id']
        r = None
        tags = []
        for b in q['badges']:
            if b in R_MAP:
                r = R_MAP[b]
            elif b in TAG_MAP:
                tags += TAG_MAP[b]
            else:
                raise ValueError((qid, b))
        if r is None:
            r = 0.5
        f = {'stem': clean(q['stem']), 'reason': clean(q['reason']), 'note': clean(q['note'])}
        for k in FIELDS_OPT:
            f[k] = clean(q['options'][k])
        # plain-text repairs before LaTeX
        for field, pairs in O.TEXT.get(qid, {}).items():
            for old, new in pairs:
                assert old in f[field], (qid, field, old, f[field])
                f[field] = f[field].replace(old, new)
        # LaTeX
        g = {}
        for k, val in f.items():
            if k in FIELDS_OPT:
                g[k] = tex.latexify(val, whole_frac=True)
            else:
                g[k] = tex.latexify(val)
        for field, val in O.TEX.get(qid, {}).items():
            if isinstance(val, list):
                for old, new in val:
                    assert old in g[field], (qid, field, old, g[field])
                    g[field] = g[field].replace(old, new)
            else:
                g[field] = val
        out.append(dict(
            id=qid, ch=q['ch'], sub=q['sub'], subName=subs[q['sub']]['name'], r=r, tags=tags,
            wording=q['wording'], conceptId=None, stem=g['stem'],
            options={k: g[k] for k in FIELDS_OPT}, ans=q['check'], reason=g['reason'], note=g['note'],
        ))
    # concept ids: default = own id; groups from overrides
    by_id = {q['id']: q for q in out}
    for q in out:
        q['conceptId'] = 'c%d' % q['id']
    for grp in O.CONCEPTS:
        cid = 'c' + '-'.join(str(x) for x in grp)
        for x in grp:
            by_id[x]['conceptId'] = cid
    return out, raw


if __name__ == '__main__':
    out, raw = build()
    json.dump(out, open('bank.json', 'w'), ensure_ascii=False, indent=1)
    print('built', len(out))
