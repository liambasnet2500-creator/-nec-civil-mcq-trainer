"""Convert formula segments in plain question text into $...$ LaTeX."""
import re

GREEK = {'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma', 'δ': r'\delta', 'ε': r'\varepsilon',
         'θ': r'\theta', 'κ': r'\kappa', 'λ': r'\lambda', 'μ': r'\mu', 'ν': r'\nu', 'ρ': r'\rho',
         'σ': r'\sigma', 'τ': r'\tau', 'φ': r'\phi', 'ψ': r'\psi', 'ω': r'\omega', 'η': r'\eta',
         'ξ': r'\xi', 'ζ': r'\zeta', 'χ': r'\chi', 'Δ': r'\Delta', '∆': r'\Delta', 'Σ': r'\Sigma',
         'Φ': r'\Phi', 'Ω': r'\Omega', 'π': r'\pi', 'Γ': r'\Gamma', 'Ψ': r'\Psi'}
SYM = {'×': r'\times', '·': r'\cdot', '−': '-', '–': '-', '≤': r'\le', '≥': r'\ge', '≈': r'\approx',
       '∝': r'\propto', '∞': r'\infty', '∫': r'\int', '∇': r'\nabla', '∂': r'\partial', '⟂': r'\perp',
       '∥': r'\parallel', '°': r'^\circ', '′': "'", '″': "''", '%': r'\%', '≠': r'\ne', '±': r'\pm',
       '÷': r'\div', '→': r'\to', '’': "'", '<': '<', '>': '>', '|': '|'}
FRAC = {'½': '1/2', '⅓': '1/3', '⅔': '2/3', '¼': '1/4', '¾': '3/4', '⅕': '1/5', '⅛': '1/8'}
SUP = dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁽⁾ⁿ', '0123456789-+()n'))
SUB = dict(zip('₀₁₂₃₄₅₆₇₈₉', '0123456789'))
FUNCS = ['sin', 'cos', 'tan', 'cot', 'log', 'ln', 'exp', 'max', 'min']
GREEK_CH = ''.join(GREEK)

# symbol vocabulary: token -> latex (applied to whole alnum runs)
VOCAB = {}


def v(**kw):
    VOCAB.update(kw)


STRONG_CH = set(GREEK_CH) | set(SUP) | set(SUB) | set('√∫∇∂∝⟂∥^_½⅓⅔¼¾⅕⅛')
OPS = {'=', '+', '−', '-', '–', '×', '÷', '·', '<', '>', '≤', '≥', '≈', '∝', '≠', '±', '/'}

UNIT_STEMS = ['mm', 'cm', 'km', 'm', 'kN', 'MN', 'N', 'kg', 'g', 't', 'Pa', 'kPa', 'MPa', 'GPa', 's',
              'h', 'L', 'l', 'ha', 'day', 'd', 'yr', 'W', 'kW', 'MW', 'GW', 'kWh', 'MWh', 'GWh', 'min',
              'lpcd', 'year', 'Mm', 'mg', 'µg', 'μg', 'μm', 'µm', 'cumec', 'cumecs', 'litre', 'litres', 'sec', 'hr', 'mL', 'ml',
              'Rs', 'cusec', 'veh', 'pcu', 'PCU', 'person', 'cap', 'capita', 'ppm']
UNIT_RE = re.compile(r'^(?:%s)[²³]?(?:[/·](?:%s)[²³]?)*$' % ('|'.join(UNIT_STEMS), '|'.join(UNIT_STEMS)))


def is_unit(tok):
    return bool(UNIT_RE.match(tok))


_VOCAB_RE = None


def protect(s):
    global _VOCAB_RE
    if not VOCAB:
        return s, []
    keys = sorted(VOCAB, key=len, reverse=True)
    rx = re.compile(r'(?<![A-Za-z])(%s)(?![A-Za-z0-9])' % ('|'.join(map(re.escape, keys))))
    saved = []

    def rep(m):
        saved.append(VOCAB[m.group(1)])
        return '\x01%d\x02' % (len(saved) - 1)
    return rx.sub(rep, s), saved


def conv_inner(s):
    """Convert a formula string (no $) into LaTeX."""
    s, saved = protect(s)
    r = _conv(s)
    r = re.sub('\x01(\\d+)\x02', lambda m: saved[int(m.group(1))], r)
    cmds = sorted({c[1:] for c in list(SYM.values()) + list(GREEK.values()) if c.startswith('\\')} | set(FUNCS) | {'circ'}, key=len, reverse=True)
    r = re.sub(r'(\\(?:%s))(?=[A-Za-z])' % '|'.join(cmds), r'\1 ', r)
    r = r.replace('^\\circ ', '^\\circ\\,') if False else r
    return r


def _conv(s):
    out = []
    i = 0
    n = len(s)

    def read_group(j, open_ch, close_ch):
        depth = 0
        k = j
        while k < n:
            if s[k] == open_ch:
                depth += 1
            elif s[k] == close_ch:
                depth -= 1
                if depth == 0:
                    return s[j + 1:k], k + 1
            k += 1
        return s[j + 1:], n

    while i < n:
        c = s[i]
        if c == '√':
            j = i + 1
            if j < n and s[j] in '([':
                inner, k = read_group(j, s[j], ')' if s[j] == '(' else ']')
            elif j < n and s[j] == '\x01':
                k = s.index('\x02', j) + 1
                inner = s[j:k]
            else:
                m = re.match(r'[0-9.]+|[A-Za-z%s][₀-₉A-Za-z0-9]*' % GREEK_CH, s[j:])
                inner = m.group(0)
                k = j + len(inner)
            out.append(r'\sqrt{' + _conv(inner) + '}')
            i = k
            continue
        if c in SUP:
            j = i
            while j < n and s[j] in SUP:
                j += 1
            out.append('^{' + ''.join(SUP[x] for x in s[i:j]) + '}')
            i = j
            continue
        if c in SUB:
            j = i
            while j < n and s[j] in SUB:
                j += 1
            out.append('_{' + ''.join(SUB[x] for x in s[i:j]) + '}')
            i = j
            continue
        if c == '^':
            j = i + 1
            if j < n and s[j] == '(':
                inner, k = read_group(j, '(', ')')
            elif j < n and s[j] in FRAC:
                inner, k = FRAC[s[j]], j + 1
            else:
                m = re.match(r'-?[0-9.]+|[A-Za-z]', s[j:])
                inner = m.group(0) if m else ''
                k = j + len(inner)
            out.append('^{' + _conv(inner) + '}')
            i = k
            continue
        if c in FRAC:
            a, b = FRAC[c].split('/')
            out.append(r'\tfrac{%s}{%s}' % (a, b))
            i += 1
            continue
        if c in GREEK:
            m = re.match(r'\d+', s[i + 1:])
            if m:
                out.append(GREEK[c] + '_{' + m.group(0) + '}')
                i += 1 + len(m.group(0))
            else:
                out.append(GREEK[c] + ' ')
                i += 1
            continue
        if c == '\x01':
            k = s.index('\x02', i)
            out.append(s[i:k + 1])
            i = k + 1
            continue
        if c in SYM:
            out.append(SYM[c] + (' ' if SYM[c].startswith('\\') and SYM[c][-1].isalpha() else ''))
            i += 1
            continue
        if c.isalpha():
            # alnum run (letters + digits + greek handled separately)
            m = re.match(r'[A-Za-z][A-Za-z0-9]*', s[i:])
            run = m.group(0)
            out.append(conv_word(run))
            i += len(run)
            continue
        if c == ' ':
            out.append(' ')
            i += 1
            continue
        out.append(c)
        i += 1
    r = ''.join(out)
    r = re.sub(r' +', ' ', r).strip()
    r = re.sub(r' ([_^])', r'\1', r)
    r = re.sub(r'(\\[a-zA-Z]+) (?=[^a-zA-Z])', r'\1', r)
    r = r.replace('\\% ', '\\%')
    return r


def conv_word(run):
    if run in VOCAB:
        return VOCAB[run]
    for f in FUNCS:
        if run == f:
            return '\\' + f + ' '
    m = re.fullmatch(r'([A-Za-z])(\d+)', run)
    if m:
        return '%s_{%s}' % m.groups()
    m = re.fullmatch(r'(sin|cos|tan)([A-Za-z])', run)
    if m:
        return '\\%s %s' % m.groups()
    if len(run) >= 3 and run.isalpha() and run.lower() == run and run not in ('dx', 'dy', 'dz', 'ds', 'du', 'dv'):
        return r'\text{%s}' % run
    if re.fullmatch(r'[A-Z]{3,}', run):
        return r'\text{%s}' % run
    return run


def strong(tok):
    t = tok.strip('(),;:.[]‘’“”\'"')
    if not t or not re.search(r'[A-Za-z0-9%s√∫∇]' % GREEK_CH, t):
        return False
    if re.fullmatch(r'[0-9]*[A-Za-z]+(?:-[A-Za-z]+)+', t) or re.fullmatch(r'\d+(st|nd|rd|th)', t) \
            or re.fullmatch(r'[0-9.]+-[A-Za-z]+(?:-[A-Za-z]+)*', t):
        return False
    if is_unit(re.sub(r'^[0-9.,]+/?', '', t)) and re.match(r'[0-9]', t):
        return False
    if any(ch in STRONG_CH for ch in t):
        return not is_unit(t)
    if re.fullmatch(r'[0-9.]*[A-Za-z][A-Za-z]?\d*/[0-9.]+', t):
        return True
    if re.fullmatch(r'[0-9.]+/[A-Za-z]{1,2}', t):
        return True
    if re.match(r'^[0-9.]*[A-Za-z]{1,2}\([A-Za-z0-9]', t) and not re.match(r'^(?:Rs|No|Fig|Eq)\(', t):
        return True
    core = re.sub(r'[()\[\]]', '', t)
    core2 = re.sub(r'^[0-9.]+', '', core)
    if (core in VOCAB and core not in WEAK) or (core2 in VOCAB and core2 not in WEAK and core2 != core):
        return True
    # contains operator between symbols, e.g. bd/12, 2M/T, (1+e), h(a+2b)
    if re.search(r'[A-Za-z0-9)\]][/+=×·−-][A-Za-z(\[]', t) and re.search(r'[A-Za-z]', t) and not is_unit(t) \
            and not re.fullmatch(r'[A-Za-z]+(?:-[A-Za-z]+)+', t):
        if re.fullmatch(r'[A-Za-z]+(?:[/-][A-Za-z]+)+', t):
            parts = re.split(r'[/-]', t)
            if any(len(p) >= 3 and p not in VOCAB for p in parts):
                return False
        return True
    return False


def is_op(tok):
    return tok in OPS


def is_num(tok):
    return bool(re.fullmatch(r'[(\[]*[-−]?[0-9][0-9,./()\[\]×·+−°′″-]*[°′″%²³]*[)\]]*', tok))


from wordfreq import zipf_frequency
UNIT1 = set('msShNtgLldWJK')


def is_var(tok):
    t = re.sub(r'[()\[\]]', '', tok)
    if re.fullmatch(r'[A-Za-z]', t):
        return True
    if re.fullmatch(r'[0-9.]+[A-Za-z]{1,2}', t) and not re.fullmatch(r'\d+(st|nd|rd|th)', t) \
            and not is_unit(re.sub(r'^[0-9.]+', '', t)):
        return True
    if re.fullmatch(r'[A-Za-z]{2,3}', t) and not t.isupper() and not is_unit(t) and zipf_frequency(t.lower(), 'en') < 3.0:
        return True
    return False




def convert_text(text, whole_frac=False):
    """Return text with formula segments wrapped in $...$."""
    if not text or not text.strip():
        return text
    toks = re.split(r'( +)', text)
    words = [t for t in toks if not t.startswith(' ')]
    # classify
    kinds = []
    for w0 in words:
        w = w0 if re.search(r'\d\.$', w0) else w0.rstrip(',;:.?!')
        if not w:
            kinds.append('t')
            continue
        if re.fullmatch(r'\(?(sin|cos|tan|cot|log|ln)\)?', w):
            kinds.append('m')
        elif is_op(w):
            kinds.append('op')
        elif strong(w):
            kinds.append('m')
        elif is_num(w):
            kinds.append('n')
        elif is_var(w) or re.sub(r'[()\[\]]', '', w) in WEAK:
            kinds.append('v')
        else:
            kinds.append('t')
    for k in range(1, len(words)):
        w = words[k].rstrip(',;:.')
        if kinds[k] == 'v' and kinds[k - 1] == 'n' and w in UNIT1:
            kinds[k] = 't'
    # build segments: runs of m/n/v/op ; trailing punctuation splits
    segs = []
    i = 0
    N = len(words)
    while i < N:
        if kinds[i] in ('m', 'op', 'n', 'v'):
            j = i
            while j < N and kinds[j] in ('m', 'op', 'n', 'v'):
                if j > i and re.search(r'[,;:.]$', words[j - 1]) and not re.search(r'\d\.$', words[j - 1]):
                    break
                if j > i and re.search(r'[,;]$', words[j - 1]):
                    break
                if j > i and words[j].startswith('(') and words[j].count('(') > words[j].count(')') \
                        and kinds[j - 1] != 'op':
                    prev = ' '.join(words[i:j])
                    if prev.count('(') == prev.count(')'):
                        break
                j += 1
            segs.append((i, j))
            i = j
        else:
            i += 1
    keep = []
    for a, b in segs:
        ks = kinds[a:b]
        # trim leading/trailing ops
        while a < b and kinds[a] == 'op' and words[a] not in ('−', '-'):
            a += 1
        while b > a and kinds[b - 1] == 'op':
            b -= 1
        if a >= b:
            continue
        ks = kinds[a:b]
        has_m = 'm' in ks
        has_op = 'op' in ks
        has_v = 'v' in ks
        if has_m or (has_v and has_op and any(words[k] in OPS for k in range(a, b))):
            # single bare var with op must be adjacent to op
            if not has_m:
                ok = any(kinds[k] == 'v' and ((k + 1 < b and kinds[k + 1] == 'op') or (k - 1 >= a and kinds[k - 1] == 'op'))
                         for k in range(a, b))
                if not ok:
                    continue
            # do not wrap if the only strong thing is a stray letter word like 'A' at sentence start
            keep.append((a, b))
    # trim trailing/leading punctuation from segment words
    res_words = list(words)
    for a, b in keep:
        seg = ' '.join(words[a:b])
        pre = ''
        post = ''
        m = re.match(r'^([(\[]*)(.*?)([,;:.?!]*)$', seg, re.S)
        lead, body, trail = m.groups()
        # balance: move unmatched leading '(' / trailing ')' outside
        if lead and body.count(')') + body.count(']') <= body.count('(') + body.count('['):
            pre = lead
        else:
            body = lead + body
        while body.endswith(')') and body.count(')') > body.count('('):
            body = body[:-1]
            trail = ')' + trail
        while body.endswith(']') and body.count(']') > body.count('['):
            body = body[:-1]
            trail = ']' + trail
        if body.endswith('.') and not re.search(r'\d\.$', body):
            body = body[:-1]
            trail = '.' + trail
        latex = conv_inner(body)
        if whole_frac and a == 0 and b == len(words):
            latex = frac_top(body) or latex
        res_words[a] = pre + '$' + latex + '$' + trail
        for k in range(a + 1, b):
            res_words[k] = None
    out = []
    wi = 0
    for t in toks:
        if t.startswith(' '):
            out.append(t)
        else:
            w = res_words[wi]
            wi += 1
            if w is not None:
                out.append(w)
            else:
                out.append('\x00')
    s = ''.join(out)
    s = re.sub(r' *\x00', '', s)
    return s


def split_atom_left(s, end):
    """Return start index of the atom ending at s[end-1]."""
    i = end
    while i > 0:
        c = s[i - 1]
        if c in ')]':
            close = c
            open_ = '(' if c == ')' else '['
            depth = 0
            j = i - 1
            while j >= 0:
                if s[j] == close:
                    depth += 1
                elif s[j] == open_:
                    depth -= 1
                    if depth == 0:
                        break
                j -= 1
            i = j
            continue
        if c.isalnum() or c in GREEK_CH or c in SUP or c in SUB or c in '√.^·' or c in FRAC:
            i -= 1
            continue
        break
    return i


def split_atom_right(s, start):
    i = start
    n = len(s)
    if i < n and s[i] == '√':
        return split_atom_right(s, i + 1)
    if i < n and s[i] in '([':
        open_, close = s[i], (')' if s[i] == '(' else ']')
        depth = 0
        j = i
        while j < n:
            if s[j] == open_:
                depth += 1
            elif s[j] == close:
                depth -= 1
                if depth == 0:
                    break
            j += 1
        return j + 1
    while i < n and (s[i].isalnum() or s[i] in GREEK_CH or s[i] in SUP or s[i] in SUB or s[i] in '√.'):
        i += 1
    return i


def strip_outer(x):
    if len(x) >= 2 and x[0] in '([' and x[-1] == {'(': ')', '[': ']'}[x[0]]:
        depth = 0
        for k, ch in enumerate(x):
            if ch in '([':
                depth += 1
            elif ch in ')]':
                depth -= 1
                if depth == 0 and k != len(x) - 1:
                    return x
        return x[1:-1]
    return x


def frac_top(body):
    """Convert the first top-level a/b in body into \\dfrac{a}{b}; None if not applicable."""
    depth = 0
    slash = [k for k, ch in enumerate(body) if ch == '/' and depth_at(body, k) == 0]
    if len(slash) != 1:
        return None
    k = slash[0]
    if k == 0 or k == len(body) - 1 or body[k - 1] == ' ' or body[k + 1] == ' ':
        return None
    a0 = split_atom_left(body, k)
    b1 = split_atom_right(body, k + 1)
    num = strip_outer(body[a0:k])
    den = strip_outer(body[k + 1:b1])
    return conv_inner(body[:a0]) + r'\dfrac{' + conv_inner(num) + '}{' + conv_inner(den) + '}' + conv_inner(body[b1:])


def depth_at(s, k):
    d = 0
    for ch in s[:k]:
        if ch in '([':
            d += 1
        elif ch in ')]':
            d -= 1
    return d


# ---------------------------------------------------------------- vocabulary
v(Ar='A_r', av='a_v', C0='C_0', Cc='C_c', Cu='C_u', cu='c_u', cv='c_v', D10='D_{10}', D30='D_{30}',
  D60='D_{60}', De='D_e', Df='D_f', Di='D_i', Do='D_o', Dr='D_r', Dw='D_w', Ec='E_c', e0='e_0',
  emax=r'e_{\max}', emin=r'e_{\min}', Fr=r'\mathrm{Fr}', Fr1=r'\mathrm{Fr}_1', fy='f_y', fck='f_{ck}',
  fcr='f_{cr}', Gs='G_s', hf='h_f', Ix='I_x', Iy='I_y', Iz='I_z', Jz='J_z', Ka='K_a', Kp='K_p',
  Ld='L_d', Le='L_e', Lw='L_w', Lx='L_x', Ly='L_y', m1='m_1', m2='m_2', Mp='M_p', Mu='M_u',
  mv='m_v', Nc='N_c', Nd='N_d', Nf='N_f', Nq='N_q', Ns='N_s', pa='p_a', Pn='P_n', qf='q_f',
  qu='q_u', Re=r'\mathrm{Re}', Rw2='R_{w2}', S0='S_0', Tv='T_v', Vs='V_s', Vv='V_v',
  Vw='V_w', Ww='W_w', Ws='W_s', wc='w_c', ymax=r'y_{\max}', Vmax=r'V_{\max}', Vmean=r'V_{\text{mean}}',
  y1='y_1', y2='y_2', V1='V_1', V2='V_2', V3='V_3', A1V1='A_1V_1', A2V2='A_2V_2', P1A1='P_1A_1',
  P2A2='P_2A_2', V1V2='V_1V_2', cNc='cN_c', qNq='qN_q', k_member=r'k_{\text{member}}',
  C_HW=r'C_{\text{HW}}', S_final=r'S_{\text{final}}', p_abs=r'p_{\text{abs}}', p_atm=r'p_{\text{atm}}',
  p_gauge=r'p_{\text{gauge}}', I_base=r'I_{\text{base}}', i_c='i_c', S_t='S_t', I_G='I_G',
  D60D10='D_{60}D_{10}', D10D60='D_{10}D_{60}', IxIy='I_xI_y', kNfNd='kN_fN_d', kH='kH', d0='d_0', CLH='CLH', CL=r'\text{CL}', CH=r'\text{CH}', te='t_e', Lag=r'\text{Lag}')
VOCAB.update({'Nγ': r'N_\gamma', 'γBNγ': r'\gamma BN_\gamma', 'Kaσv': r'K_a\sigma_v', 'σv': r'\sigma_v',
              'σs': r'\sigma_s', 'τbd': r'\tau_{bd}', 'σb': r'\sigma_b', 'σx': r'\sigma_x', 'σy': r'\sigma_y',
              'τxy': r'\tau_{xy}', 'τmax': r'\tau_{\max}', 'τavg': r'\tau_{\text{avg}}', 'τf': r'\tau_f',
              'φu': r'\phi_u', 'ρd': r'\rho_d', 'ηd': r'\eta_d', 'δmax': r'\delta_{\max}',
              'δpoint': r'\delta_{\text{point}}', 'δUDL': r'\delta_{\text{UDL}}', 'ΣBS': r'\Sigma\text{BS}',
              'ΣFS': r'\Sigma\text{FS}', 'ΣRise': r'\Sigma\text{Rise}', 'ΣFall': r'\Sigma\text{Fall}',
              'ρ1A1V1': r'\rho_1A_1V_1', 'ρ2A2V2': r'\rho_2A_2V_2', 'ρ1V1': r'\rho_1V_1', 'ρ2V2': r'\rho_2V_2',
              'RL': r'\text{RL}', 'BS': r'\text{BS}', 'FS': r'\text{FS}'})
# vocabulary entries that make a bare token count as a formula (others only convert inside formulas)
WEAK = {'CL', 'CH', 'Do', 'De', 'Di', 'Dr', 'Le', 'Re', 'Fr', 'te', 'Lag', 'RL', 'BS', 'FS', 'Ar', 'Et'}

CHEM = {
    'CaSO4·2H2O': r'\mathrm{CaSO_4\cdot 2H_2O}', 'CaSO4·½H2O': r'\mathrm{CaSO_4\cdot \tfrac{1}{2}H_2O}',
    'Al2(SO4)3·18H2O': r'\mathrm{Al_2(SO_4)_3\cdot 18H_2O}', 'C2S': r'\mathrm{C_2S}', 'C3S': r'\mathrm{C_3S}',
    'C3A': r'\mathrm{C_3A}', 'C4AF': r'\mathrm{C_4AF}', 'H2O': r'\mathrm{H_2O}', 'CO2': r'\mathrm{CO_2}',
    'O2': r'\mathrm{O_2}', 'H2S': r'\mathrm{H_2S}', 'NH3': r'\mathrm{NH_3}', 'Na2SO4': r'\mathrm{Na_2SO_4}',
    'MgSO4': r'\mathrm{MgSO_4}', 'BOD5': r'\mathrm{BOD_5}', 'O₂': r'\mathrm{O_2}', 'H₂S': r'\mathrm{H_2S}',
    'CO₂': r'\mathrm{CO_2}',
}


def chem(text):
    keys = sorted(CHEM, key=len, reverse=True)
    rx = re.compile(r'(?<![A-Za-z0-9$])(%s)(?![A-Za-z0-9])' % '|'.join(map(re.escape, keys)))
    return rx.sub(lambda m: '$' + CHEM[m.group(1)] + '$', text)


def latexify(text, whole_frac=False):
    if not text:
        return text
    text = chem(text)
    parts = re.split(r'(\$[^$]*\$)', text)
    out = []
    for p in parts:
        if p.startswith('$') and p.endswith('$') and len(p) > 1:
            out.append(p)
        else:
            out.append(convert_text(p, whole_frac=whole_frac and len(parts) == 1))
    s = ''.join(out)
    s = re.sub(r'_\\text\{([^}]*)\}', r'_{\\text{\1}}', s)
    s = re.sub(r'\$[^$]*\$', lambda m: re.sub(r'(\d),(\d)', r'\1{,}\2', m.group(0)), s)
    return s
