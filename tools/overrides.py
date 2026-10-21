"""Manual repairs. TEXT: plain-text (old,new) pairs applied before LaTeX conversion.
TEX: per-field full LaTeX replacement (str) or list of (old,new) applied after conversion.
CONCEPTS: groups of near-duplicate question ids sharing one conceptId."""
TEXT = {}
TEX = {}
CONCEPTS = []

# ---- chapter 1
TEX[23] = {'stem': 'Maximum water absorption of 1st-class brick (NEC key):'}
TEX[34] = {'stem': [('diameter d is', 'diameter $d$ is')]}
TEX[35] = {'stem': [('diameter d about', 'diameter $d$ about')]}
TEX[37] = {'stem': [('outer diameter D and inner diameter d,', 'outer diameter $D$ and inner diameter $d$,')]}
TEX[38] = {'stem': [('height h,', 'height $h$,')]}
TEX[39] = {'stem': [('sides a at the top and b at the base', 'sides $a$ at the top and $b$ at the base'),
                    ('height h.', 'height $h$.'), ('from base b is', 'from base $b$ is')],
           'reason': [('longer base b:', 'longer base $b$:')]}
TEX[40] = {'stem': [('outer diameter D and inner diameter d,', 'outer diameter $D$ and inner diameter $d$,')]}
TEX[41] = {'stem': [('width b and depth d', 'width $b$ and depth $d$')]}
TEX[42] = {'stem': [('width b and depth d', 'width $b$ and depth $d$'), ('parallel to b equal', 'parallel to $b$ equal')],
           'reason': 'Centroidal $I$ of a rectangle about the axis parallel to $b$ $= bd^{3}/12$.'}
TEX[43] = {'stem': [('base b and height h', 'base $b$ and height $h$')]}
TEX[44] = {'stem': [('diameter D about', 'diameter $D$ about')]}
TEX[45] = {'reason': '$I_G = bh^{3}/36$ and $I_{\\text{base}} = bh^{3}/12$, so $I_G : I_{\\text{base}} = 1 : 3$.'}
TEX[46] = {'stem': [('base b and height h', 'base $b$ and height $h$')]}
TEX[47] = {'D': 'Pyramid'}
TEX[50] = {'reason': [(' (An FTEI key says the error ‘lies in NW’ — same geometry.)', '')]}
TEX[51] = {'A': r'$\Sigma\text{BS} + \Sigma\text{FS} = \text{last RL} - \text{first RL}$',
           'B': r'$\Sigma\text{FS} - \Sigma\text{BS} = \text{last RL} - \text{first RL}$',
           'C': r'$\Sigma\text{BS} - \Sigma\text{FS} = \text{first RL} + \text{last RL}$',
           'D': r'$\Sigma\text{BS} - \Sigma\text{FS} = \text{last RL} - \text{first RL}$',
           'reason': r'$\Sigma\text{BS} - \Sigma\text{FS} = \text{last RL} - \text{first RL}$ (also $= \Sigma\text{Rise} - \Sigma\text{Fall}$ in the rise-and-fall method).'}
TEX[59] = {'reason': r"Back bearing of AB = 326°30′; angle ABC = $\text{FB}(\text{BC}) - \text{BB}(\text{AB}) = 68^\circ30' - 326^\circ30' + 360^\circ = 102^\circ$."}
TEX[71] = {'stem': [('formation width B, height y and side slopes s horizontal',
                     'formation width $B$, height $y$ and side slopes $s$ horizontal')],
           'A': '$By$',
           'reason': r'Area = top width × height + two side triangles ($\tfrac{1}{2}\cdot sy\cdot y$ each) $= By + sy^{2}$.'}
# ---- chapter 2
TEX[75] = {'reason': r'USCS well-graded sand: $C_u \ge 6$ and $C_c = 1$–3 (gravel: $C_u \ge 4$).'}
TEX[76] = {'stem': [('Porosity n and void ratio e are', 'Porosity $n$ and void ratio $e$ are')]}
TEX[77] = {'stem': [('water content w is', 'water content $w$ is')],
           'reason': [('with w as a decimal', 'with $w$ as a decimal')]}
TEX[86] = {'reason': [('pore-water pressure u,', 'pore-water pressure $u$,')]}
TEX[104] = {'stem': [('outer diameter Do and inner diameter Di', 'outer diameter $D_o$ and inner diameter $D_i$')]}
TEX[122] = {'A': '$B$', 'C': '$2B$ below GL'}
TEX[123] = {'D': 'Water table'}
TEX[124] = {'reason': [(r'(c, $\phi$', r'($c$, $\phi$')]}
TEX[126] = {'stem': [('at time t to', 'at time $t$ to')]}
# ---- chapter 3
TEX[130] = {'stem': [('radius R and surface tension T,', 'radius $R$ and surface tension $T$,')]}
TEX[145] = {'B': [(' - ', ' − ')], 'C': [(' - ', ' − ')], 'D': [(' - ', ' − ')]}
TEX[146] = {'reason': 'Stable when metacentre $M$ is above $G$ ($GM > 0$); $M$ below $G$ → unstable.'}
TEX[150] = {'stem': [('area A and velocity V strikes', 'area $A$ and velocity $V$ strikes')],
            'reason': [(r'\rho aV(V - 0)', r'\rho AV(V - 0)')]}
TEX[152] = {'stem': [('velocity vector V,', 'velocity vector $V$,')]}
TEX[153] = {'stem': [('diameter d each carry velocity V into', 'diameter $d$ each carry velocity $V$ into'),
                     ('velocity is 2V, its diameter D is', 'velocity is $2V$, its diameter $D$ is')],
            'A': '$d$', 'C': '$2d$'}
TEX[156] = {'reason': r'The jet spreads out and moves along the plate; force $F = \rho aV^{2}$.'}
TEX[158] = {'stem': [('Manning’s n is', 'Manning’s $n$ is')]}
TEX[163] = {'stem': [('length L and diameter D,', 'length $L$ and diameter $D$,')], 'A': '$2L$', 'C': '$4L$'}
TEX[166] = {'stem': [('diameter D operate', 'diameter $D$ operate')], 'B': '$2D$'}
TEX[169] = {'stem': [('Manning’s n ≈', 'Manning’s $n$ ≈')]}
TEX[170] = {'A': '$V$ in laminar and $V^{2}$ in turbulent flow', 'B': '$V^{2}$ laminar, $V$ turbulent',
            'C': '$V$ in both'}
TEX[171] = {'reason': [('laminar ∝ V.', 'laminar ∝ $V$.'), ('friction factor f is', 'friction factor $f$ is')]}
TEX[176] = {'reason': [('= 0.0025 = 1$ in 400.', '= 0.0025$, i.e. 1 in 400.')]}
TEX[177] = {'stem': [('Manning n,', 'Manning $n$,')], 'reason': [(' %', '%')]}
TEX[178] = {'stem': [('Manning’s n doubles', 'Manning’s $n$ doubles')],
            'reason': [('same V and R,', 'same $V$ and $R$,')]}
TEX[179] = {'reason': [('(T = top width)', '($T$ = top width)')]}
TEX[180] = {'stem': [('water depth y,', 'water depth $y$,')], 'A': '$y$', 'C': '$2y$'}
TEX[183] = {'reason': [('loss EL = $', 'loss $E_L = ')]}
TEX[185] = {'stem': [('bed width b, depth y and side slope z horizontal', 'bed width $b$, depth $y$ and side slope $z$ horizontal')],
            'B': '$b+2zy$', 'D': '$b+2y$'}
TEX[187] = {'B': r'$y_2/y_1 = \sqrt{1 + 8\mathrm{Fr}_1^{2}} - 1$'}
TEX[189] = {'stem': [('water depth y,', 'water depth $y$,')], 'D': '$2y$'}
# ---- chapter 4
TEX[202] = {'reason': [('constant M →', 'constant $M$ →')]}
TEX[203] = {'stem': [('A couple M applied', 'A couple $M$ applied')], 'A': '$2M$', 'D': '$M$',
            'reason': r'A couple $M$ at the free end gives $\text{BM} = M$ at every section and zero shear.'}
TEX[206] = {'stem': [('shear force V is related to bending moment M by', 'shear force $V$ is related to bending moment $M$ by')],
            'D': '$V = Mx$'}
TEX[207] = {'stem': [('couple M at its', 'couple $M$ at its')], 'A': '$M/L$ and $M$', 'C': '0 and $M$',
            'reason': [('fixed-end moment M.', 'fixed-end moment $M$.')]}
TEX[215] = {'stem': [('bending moment M and torque T.', 'bending moment $M$ and torque $T$.')]}
TEX[217] = {'stem': [('material, E, G and', 'material, $E$, $G$ and')]}
TEX[223] = {'stem': [('actual length L with', 'actual length $L$ with')], 'B': '$2L$', 'C': '$L$',
            'reason': [('hinged–hinged L, fixed–free 2L (IS uses 0.65L for', 'hinged–hinged $L$, fixed–free $2L$ (IS uses $0.65L$ for')]}
TEX[224] = {'stem': [('actual length L is', 'actual length $L$ is')], 'C': '$2L$', 'D': '$L$',
            'reason': 'Fixed–free (flagpole) column: $L_e = 2L$.'}
TEX[225] = {'stem': [('length L is equivalent (same Le)', 'length $L$ is equivalent (same $L_e$)')], 'B': '$2L$', 'C': '$4L$',
            'reason': r"$0.5L = 2L'$ → $L' = L/4$."}
TEX[228] = {'stem': [('span L and constant flexural rigidity EI carries a full-span UDL of total load W.',
                      'span $L$ and constant flexural rigidity $EI$ carries a full-span UDL of total load $W$.')],
            'reason': [('UDL total W:', 'UDL total $W$:')]}
TEX[229] = {'stem': [('width B,', 'width $B$,')],
            'A': r'$|e| \le B/2$', 'B': r'$|e| \le B/3$', 'C': r'$|e| \le B/6$', 'D': r'$|e| \le B$'}
TEX[230] = {'stem': [('span L and constant flexural rigidity EI is', 'span $L$ and constant flexural rigidity $EI$ is'),
                     ('central point load W.', 'central point load $W$.')]}
TEX[231] = {'stem': [('span L carries a point load W at', 'span $L$ carries a point load $W$ at')],
            'reason': [('central W:', 'central $W$:')]}
TEX[233] = {'stem': [('length L carries a point load W at', 'length $L$ carries a point load $W$ at')]}
TEX[234] = {'stem': [('central point load W or a full-span UDL of total load W.',
                      'central point load $W$ or a full-span UDL of total load $W$.')]}
TEX[235] = {'stem': [('span, E and central', 'span, $E$ and central')],
            'reason': [('doubling b halves the deflection (doubling d →', 'doubling $b$ halves the deflection (doubling $d$ →')]}
TEX[238] = {'stem': [('span L and constant flexural rigidity EI carries a central point load W.',
                      'span $L$ and constant flexural rigidity $EI$ carries a central point load $W$.')]}
TEX[240] = {'stem': [('point load W:', 'point load $W$:')]}
TEX[242] = {'stem': [('radius R and constant EI, with UDL w per', 'radius $R$ and constant $EI$, with UDL $w$ per')]}
TEX[247] = {'stem': [('Let M be', 'Let $M$ be'),
                     (', y the arch ordinate, EI the flexural rigidity and ds an', ', $y$ the arch ordinate, $EI$ the flexural rigidity and $ds$ an'),
                     ('thrust H is', 'thrust $H$ is')],
            'A': r'$\dfrac{\int (M/EI)\,ds}{\int (y^{2}/EI)\,ds}$',
            'B': r'$\dfrac{\int (My/EI)\,ds}{\int (y^{2}/EI)\,ds}$',
            'C': r'$\dfrac{\int (My/EI)\,ds}{\int (y/EI)\,ds}$',
            'reason': r'Two-hinged arch: $H = \int (My/EI)\,ds \div \int (y^{2}/EI)\,ds$.'}
TEX[248] = {'reason': r'$V_B = 80 \times 6/40 = 12$ kN; moments at the crown from the right: $H \times 8 = 12 \times 20$ → $H = 30$ kN.'}
TEX[250] = {'stem': [('vertical shear V and horizontal thrust H give', 'vertical shear $V$ and horizontal thrust $H$ give')]}
TEX[251] = {'stem': [('length L and flexural rigidity EI.', 'length $L$ and flexural rigidity $EI$.')]}
TEX[252] = {'stem': [('span L has', 'span $L$ has')]}
TEX[254] = {'reason': r'$\text{DF} = k_{\text{member}}/\Sigma k$ at the joint; the carry-over factor (½ for a fixed far end) sends moment to the far end.'}
TEX[255] = {'A': '$0.414L$ from the propped end', 'B': '$0.5L$ from the prop', 'C': '$0.25L$'}
TEX[259] = {'reason': [(' %', '%')]}
# ---- chapter 5
TEX[269] = {'reason': 'Vertical faces 16–24 h; slab soffit 3 days; beam soffit 7 days; props 7–14 days. · Depends on: normal weather, and the concrete must have enough strength.'}
TEX[275] = {'B': '75 µm', 'D': '20 µm', 'reason': [('75 µm;', '75 µm (0.075 mm);')]}
TEX[281] = {'stem': [('width b and overall depth D is', 'width $b$ and overall depth $D$ is')],
            'A': [('of bD', 'of $bD$')], 'B': [('of bD', 'of $bD$')], 'C': [('of bD', 'of $bD$')], 'D': [('of bD', 'of $bD$')],
            'reason': [('4 % of bD', '4% of $bD$')]}
TEX[283] = {'C': 'More than balanced',
            'reason': r'Over-reinforced (WSM): moment of resistance more than balanced, but uneconomical and less ductile. In LSM, $M_u$ of over-reinforced is limited to $M_{u,\text{lim}}$. · Depends on: same section and WSM limits.'}
TEX[285] = {'reason': 'Fe 415: 0.12% (Fe 250: 0.15%).'}
TEX[288] = {'reason': [(r'$12 \times10^{-6}/^\circ C$', r'$12 \times 10^{-6}$/°C')]}
TEX[291] = {'B': 'Columns are far apart',
            'reason': 'Strap footing: columns far apart, one near the property line; unequal close columns → trapezoidal combined. · Depends on: economical when a full combined footing would be too long.'}
TEX[294] = {'reason': 'IS 456: maximum 6% of gross area (keep ≤ 4% where bars are lapped); minimum 0.8%.'}
TEX[297] = {'stem': [('batten thickness t,', 'batten thickness $t$,')],
            'A': '$3t$', 'B': '$4t$', 'C': '$6t$', 'D': '$8t$', 'reason': [('≥ 4t', '≥ $4t$')]}
TEX[299] = {'reason': [('An = (400 − 18) × 10 = 3820 mm²', r'$A_n = (400 - 18) \times 10 = 3820$ mm²')]}
TEX[307] = {'D': 'Buttresses'}
# ---- chapter 6
TEX[308] = {'reason': [(' %', '%')]}
TEX[315] = {'A': 'ppm'}
TEX[323] = {'stem': [('P in thousands', '$P$ in thousands')]}
TEX[325] = {'reason': [('$Ca/Mg$', 'Ca/Mg')]}
TEX[332] = {'C': 'Dead-end',
            'reason': 'Dead-end (tree) suits irregular old cities; grid-iron → planned; ring → well-planned; radial → radial roads. · Depends on: easy for irregular streets; loops are more reliable.'}
TEX[333] = {'D': 'Control supply to elevated tanks/standpipes'}
TEX[335] = {'reason': [('$OCl^{-}$', r'$\mathrm{OCl^{-}}$')]}
TEX[340] = {'reason': [('$Na^{+}$', r'$\mathrm{Na^{+}}$'), ('$Ca^{2+}/Mg^{2+}$', r'$\mathrm{Ca^{2+}/Mg^{2+}}$')]}
TEX[352] = {'reason': [(' %', '%')]}
TEX[353] = {'reason': 'SVI = settled volume (mL/L) ÷ MLSS (g/L) = 27/3.0 = 9 mL/g.'}
TEX[362] = {'D': '1997', 'reason': 'EPA 2053 (1997); replaced by EPA 2076 (2019).'}
# ---- chapters 7-8
TEX[374] = {'reason': r'$Q = \text{CCA} \times \text{intensity}/\text{duty}$, adjusted for time factor and losses.'}
TEX[377] = {'stem': [('with d in mm', 'with $d$ in mm'), ('mm, f is approximately', 'mm, $f$ is approximately')]}
TEX[380] = {'B': 'Increases command area'}
TEX[381] = {'stem': [('side slope 1:S (V:H), depth y, length L.', 'side slope $1:S$ (V:H), depth $y$, length $L$.')],
            'A': [('L_y', 'Ly')], 'C': [('L_y', 'Ly')],
            'reason': [('L_y', 'Ly'), ('over length L give', 'over length $L$ give')]}
TEX[392] = {'C': '2'}
TEX[394] = {'reason': [(' (each cutoff counted on both faces)', '')]}
TEX[412] = {'reason': 'Drain over canal: super passage, canal syphon (canal over drain: aqueduct, syphon aqueduct).'}
TEX[420] = {'reason': r'$E = 84 \times 8760 \times 0.6 = 441{,}504$ GWh ≈ 441 TWh.'}
TEX[421] = {'stem': [('discharge Q, net head H and', 'discharge $Q$, net head $H$ and'), ('acceleration g,', 'acceleration $g$,')],
            'reason': [('with Q in m³/s and H in m', 'with $Q$ in m³/s and $H$ in m')]}
TEX[425] = {'B': 'Continuous power', 'reason': 'Power is not continuous or season-independent: output varies with river flow.'}
TEX[428] = {'reason': 'Coincidence factor = 1/diversity factor (diversity ≥ 1).'}
TEX[434] = {'reason': [(' %', '%')]}
TEX[437] = {'A': 'Strong foundation'}
TEX[438] = {'C': 'Increase shear resistance'}
TEX[439] = {'reason': 'Shear-friction factor 3–5; the friction-only sliding FS ≥ 1 is a separate check. · Depends on: traditional range with cohesion; modern codes vary by load case.'}
TEX[442] = {'stem': [('Q varies with effective head H as', '$Q$ varies with effective head $H$ as')], 'C': '$H$'}
TEX[448] = {'reason': r'Enough submergence prevents air-entraining vortices; Gordon: $S = cV\sqrt{D}$.'}
TEX[450] = {'stem': [('Pa. c ≈', 'Pa. $c$ ≈')]}
TEX[467] = {'A': '10–35',
            'reason': r'$N_s = N\sqrt{P}/H^{1.25} \approx 25.6$, in the Pelton range. · Depends on: metric hp convention gives $N_s \approx 25.6$ (kW gives another number, same range).'}
TEX[469] = {'stem': [('discharge Q through head H is', 'discharge $Q$ through head $H$ is')]}
# ---- chapter 9
TEX[473] = {'reason': [(' %', '%')]}
TEX[474] = {'reason': [(' %', '%')]}
TEX[480] = {'A': [('20 000', '20,000')], 'C': [('20 000', '20,000')], 'D': [('10 000', '10,000')],
            'reason': [(r'$I > 20{,}000$', 'I > 20,000')]}
TEX[489] = {'A': [(' - ', ' → ')], 'B': [(' - ', ' → ')], 'C': [(' - ', ' → ')], 'D': [(' - ', ' → ')]}
TEX[491] = {'C': 'Detailed survey'}
TEX[506] = {'stem': '$f = 0.15$, $e = 1/15$ (1 in 15), $R = 100$ m. Max safe speed ≈'}
TEX[515] = {'C': 'Both A and B'}
TEX[519] = {'stem': [('For n lanes, vehicle wheelbase l and curve radius R,', 'For $n$ lanes, vehicle wheelbase $l$ and curve radius $R$,')],
            'reason': r'Mechanical widening $W_e = nl^{2}/2R$; psychological widening $V/(9.5\sqrt{R})$.'}
TEX[520] = {'D': 'Sight distance'}
TEX[522] = {'reason': r'$N = 1/40 + 1/40 = 0.05$; assuming $L > S$: $L = NS^{2}/4.4 = 55.7$ m, which is less than $S = 70$ m, so use $L < S$: $L = 2S - 4.4/N = 140 - 88 = 52$ m.'}
TEX[523] = {'reason': [(' %', '%')], 'note': [(' %', '%')]}
TEX[534] = {'reason': r'$M_R = 10\cdot\text{CBR}$ (CBR ≤ 5); $M_R = 17.6\cdot\text{CBR}^{0.64}$ above.'}
TEX[536] = {'reason': [(' %', '%')]}
TEX[540] = {'reason': [(' %', '%')]}
TEX[541] = {'reason': [(' %', '%')]}
TEX[542] = {'reason': '90th percentile for > 20 msa; 80th for lower traffic (memory key). · Depends on: means the design CBR exceeded by 90% of samples (a low value).'}
TEX[548] = {'reason': [(' %', '%')]}
TEX[553] = {'stem': [('lost time L per cycle and sum of critical flow ratios Y,', 'lost time $L$ per cycle and sum of critical flow ratios $Y$,')],
            'reason': r'Webster: $C_0 = (1.5L + 5)/(1 - Y)$; $L$ 10 s, $Y$ 0.6 → 50 s.'}
TEX[560] = {'reason': [('PHF = $V/(4V_{15})$', r'$\text{PHF} = V/(4V_{15})$')]}
# ---- chapter 10
TEX[598] = {'stem': [('cost is a and it rises by b each year. The undiscounted total for n years',
                      'cost is $a$ and it rises by $b$ each year. The undiscounted total for $n$ years')],
            'A': r'$na + n(n-1)b/2$',
            'reason': r'Total $= \Sigma[a + (k - 1)b]$ for $k = 1, \ldots, n$, $= na + n(n - 1)b/2$.'}
TEX[600] = {'stem': [('interest rate i per period for n equal', 'interest rate $i$ per period for $n$ equal')],
            'C': r'$\dfrac{1}{(1+i)^{n}}$'}
TEX[622] = {'reason': r'PERT activity times follow a $\beta$-distribution; the project duration is taken as normal.'}
TEX[634] = {'reason': '8 h/day and 48 h/week; rest of 30 min after 5 h of continuous work.'}
# ---- plain-text repairs
TEXT[121] = {'reason': [('shattered rock-/hard shale', 'shattered rock/hard shale')]}
TEXT[347] = {'stem': [('out-falls', 'outfalls')]}
TEXT[385] = {'reason': [('under-sluice', 'undersluice')]}
TEXT[484] = {'reason': [('structural/-material', 'structural/material')]}
TEXT[623] = {'reason': [('Sub-contracting', 'Subcontracting')]}

CONCEPTS = [
    [96, 97],     # undrained strength of saturated clay = cohesion (c_u = q_u/2)
    [238, 240],   # strain energy, SS beam with central point load
    [623, 625],   # subcontracting
    [636, 637],   # NEC chair / vice-chair nominated by GoN
    [170, 171],   # friction ∝ V (laminar), V² (turbulent)
    [289, 293],   # helical column strength = 1.05 × tied
    [451, 456],   # surge tank protects against water hammer
    [158, 178],   # Manning n doubled → slope × 4
    [174, 450],   # water-hammer wave speed, same data (≈ 1025 m/s)
    [32, 269],    # vertical formwork removal 16–24 h (IS 456)
    [192, 444],   # bed load definition
    [413, 414],   # tile drains ineffective in low-permeability strata
    [595, 596],   # risk vs volatility (variability of returns)
    [624, 626],   # risk mitigation
]
