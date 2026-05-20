"""
Genereaza grafurile de flux de control (CFG - Control Flow Graph)
pentru metodele testate din simulation.py:
  - MassSpringDamper.__init__
  - MassSpringDamper.get_damping_type
  - MassSpringDamper.simulate

Imaginile sunt salvate in directorul images/ ca fisiere SVG.
Nu necesita dependente externe - foloseste doar biblioteca standard Python.
"""

import os

os.makedirs('images', exist_ok=True)

# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------

DEFS = '''\
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#333333"/>
    </marker>
    <marker id="arr-red" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#C0392B"/>
    </marker>
    <marker id="arr-green" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#1E8449"/>
    </marker>
  </defs>'''


def make_svg(width, height, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'style="background:#FDFEFE">\n{DEFS}\n{body}</svg>\n'
    )


def title(cx, line1, line2=''):
    s = (f'  <text x="{cx}" y="28" text-anchor="middle" font-size="14" '
         f'font-weight="bold" font-family="Arial" fill="#1a1a1a">{line1}</text>\n')
    if line2:
        s += (f'  <text x="{cx}" y="46" text-anchor="middle" font-size="12" '
              f'font-family="Arial" fill="#555555">{line2}</text>\n')
    return s


def node_rect(cx, cy, lines, w=165, h=44, fill='#D6EAF8', stroke='#2874A6'):
    if isinstance(lines, str):
        lines = [lines]
    x, y = cx - w // 2, cy - h // 2
    s = (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" '
         f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>\n')
    n = len(lines)
    for i, line in enumerate(lines):
        ty = cy + (i - (n - 1) / 2.0) * 15 + 4
        s += (f'  <text x="{cx}" y="{ty:.1f}" text-anchor="middle" '
              f'font-size="11" font-family="monospace" fill="#1a1a1a">{line}</text>\n')
    return s


def node_diamond(cx, cy, text, dw=88, dh=29, fill='#FDEBD0', stroke='#E67E22'):
    pts = f'{cx},{cy - dh} {cx + dw},{cy} {cx},{cy + dh} {cx - dw},{cy}'
    s = (f'  <polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>\n')
    s += (f'  <text x="{cx}" y="{cy + 5}" text-anchor="middle" font-size="12" '
          f'font-weight="bold" font-family="Arial" fill="#1a1a1a">{text}</text>\n')
    return s


def node_rounded(cx, cy, text, w=120, h=36, fill='#D5F5E3', stroke='#1E8449'):
    x, y = cx - w // 2, cy - h // 2
    s = (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" '
         f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>\n')
    s += (f'  <text x="{cx}" y="{cy + 5}" text-anchor="middle" font-size="13" '
          f'font-weight="bold" font-family="Arial" fill="#1a1a1a">{text}</text>\n')
    return s


def node_error(cx, cy, lines, w=198, fill='#FADBD8', stroke='#C0392B'):
    if isinstance(lines, str):
        lines = [lines]
    h = len(lines) * 16 + 18
    x, y = cx - w // 2, cy - h // 2
    s = (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
         f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>\n')
    n = len(lines)
    for i, line in enumerate(lines):
        ty = cy + (i - (n - 1) / 2.0) * 16 + 4
        s += (f'  <text x="{cx}" y="{ty:.1f}" text-anchor="middle" '
              f'font-size="11" font-family="Arial" fill="#922B21">{line}</text>\n')
    return s


def arrow_line(x1, y1, x2, y2, lbl='', lx=None, ly=None,
               marker='arr', color='#333333'):
    s = (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
         f'stroke="{color}" stroke-width="1.5" marker-end="url(#{marker})"/>\n')
    if lbl:
        tx = lx if lx is not None else int((x1 + x2) / 2) + 6
        ty = ly if ly is not None else int((y1 + y2) / 2)
        s += (f'  <text x="{tx}" y="{ty}" font-size="11" font-weight="bold" '
              f'font-family="Arial" fill="#7D3C98">{lbl}</text>\n')
    return s


def arrow_curve(d, marker='arr-red', color='#C0392B'):
    return (f'  <path d="{d}" stroke="{color}" stroke-width="1.3" fill="none" '
            f'stroke-dasharray="5,3" marker-end="url(#{marker})"/>\n')


def lbl(x, y, text, color='#7D3C98'):
    return (f'  <text x="{x}" y="{y}" font-size="11" font-weight="bold" '
            f'font-family="Arial" fill="{color}">{text}</text>\n')


def info_box(x, y, lines, w=440):
    h = len(lines) * 17 + 16
    s = (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
         f'fill="#EBF5FB" stroke="#2874A6" stroke-width="1"/>\n')
    for i, line in enumerate(lines):
        s += (f'  <text x="{x + 8}" y="{y + 15 + i * 17}" font-size="11" '
              f'font-family="monospace" fill="#1a1a1a">{line}</text>\n')
    return s


# ---------------------------------------------------------------------------
# CFG 1: __init__   N=9  E=11  V(G)=4
# ---------------------------------------------------------------------------

def cfg_init():
    W, H = 650, 840
    CX, EX = 200, 475   # center column x, error column x
    DW, DH = 88, 29     # diamond half-width, half-height

    body = title(W // 2,
                 'CFG: MassSpringDamper.__init__(m, c, k)',
                 'N=9  E=11  P=1  \u2192  V(G) = 11 \u2212 9 + 2\u00b71 = 4')

    # node y positions
    N1y, N2y, N4y, N6y, N8y, N9y = 85, 180, 300, 420, 545, 670
    # error nodes at same y as their diamond
    N3y, N5y, N7y = N2y, N4y, N6y

    body += node_rounded(CX, N1y, 'N1: START')
    body += node_diamond(CX, N2y, 'N2: if m &lt;= 0')
    body += node_error(EX, N3y, ['N3: raise ValueError', '"m trebuie &gt; 0"'])
    body += node_diamond(CX, N4y, 'N4: if c &lt; 0')
    body += node_error(EX, N5y, ['N5: raise ValueError', '"c trebuie &gt;= 0"'])
    body += node_diamond(CX, N6y, 'N6: if k &lt;= 0')
    body += node_error(EX, N7y, ['N7: raise ValueError', '"k trebuie &gt; 0"'])
    body += node_rect(CX, N8y, ['N8: self.m = m', 'self.c = c', 'self.k = k'], h=52)
    body += node_rounded(CX, N9y, 'N9: END')

    # N1 -> N2
    body += arrow_line(CX, N1y + 18, CX, N2y - DH)
    # N2 -> N3 (T, right)
    body += arrow_line(CX + DW, N2y, EX - 100, N3y, 'T', lx=CX + DW + 4, ly=N2y - 6)
    # N2 -> N4 (F, down)
    body += arrow_line(CX, N2y + DH, CX, N4y - DH)
    body += lbl(CX + 4, (N2y + DH + N4y - DH) // 2, 'F')
    # N4 -> N5 (T, right)
    body += arrow_line(CX + DW, N4y, EX - 100, N5y, 'T', lx=CX + DW + 4, ly=N4y - 6)
    # N4 -> N6 (F, down)
    body += arrow_line(CX, N4y + DH, CX, N6y - DH)
    body += lbl(CX + 4, (N4y + DH + N6y - DH) // 2, 'F')
    # N6 -> N7 (T, right)
    body += arrow_line(CX + DW, N6y, EX - 100, N7y, 'T', lx=CX + DW + 4, ly=N6y - 6)
    # N6 -> N8 (F, down)
    body += arrow_line(CX, N6y + DH, CX, N8y - 26)
    body += lbl(CX + 4, (N6y + DH + N8y - 26) // 2, 'F')
    # N8 -> N9
    body += arrow_line(CX, N8y + 26, CX, N9y - 18)

    # error nodes -> N9 (dashed curves going right)
    ex_r = EX + 100   # right edge of error box (w=198 -> half=99 ~ 100)
    body += arrow_curve(f'M {ex_r} {N3y} C {ex_r+55} {N3y} {ex_r+55} {N9y} {CX+63} {N9y}')
    body += arrow_curve(f'M {ex_r} {N5y} C {ex_r+45} {N5y} {ex_r+45} {N9y} {CX+63} {N9y}')
    body += arrow_curve(f'M {ex_r} {N7y} C {ex_r+35} {N7y} {ex_r+35} {N9y} {CX+63} {N9y}')

    body += info_box(15, N9y + 28, [
        'Cai independente (baza V(G)=4):',
        '  P1: N1\u2192N2\u2192N3\u2192N9            (m invalid \u2192 ValueError)',
        '  P2: N1\u2192N2\u2192N4\u2192N5\u2192N9         (c invalid \u2192 ValueError)',
        '  P3: N1\u2192N2\u2192N4\u2192N6\u2192N7\u2192N9      (k invalid \u2192 ValueError)',
        '  P4: N1\u2192N2\u2192N4\u2192N6\u2192N8\u2192N9      (toti valizi \u2192 obiect creat)',
    ])

    with open('images/cfg_init.svg', 'w', encoding='utf-8') as f:
        f.write(make_svg(W, H, body))
    print('Salvat: images/cfg_init.svg')


# ---------------------------------------------------------------------------
# CFG 2: get_damping_type   N=8  E=9  V(G)=3
# ---------------------------------------------------------------------------

def cfg_damping_type():
    W, H = 600, 770
    CX, RX = 195, 445   # center, return-node column
    DW, DH = 88, 29

    body = title(W // 2,
                 'CFG: MassSpringDamper.get_damping_type()',
                 'N=8  E=9  P=1  \u2192  V(G) = 9 \u2212 8 + 2\u00b71 = 3')

    N1y = 85
    N2y = 175   # calc zeta
    N3y = 280   # if zeta < 1
    N4y = 280   # return "subdampat" (right)
    N5y = 390   # if zeta == 1
    N6y = 390   # return "critic" (right)
    N7y = 500   # return "supradampat" (center)
    N8y = 625   # END

    body += node_rounded(CX, N1y, 'N1: START')
    body += node_rect(CX, N2y, ['N2: zeta = c / (2 * sqrt(m*k))'], w=230, h=38)
    body += node_diamond(CX, N3y, 'N3: if zeta &lt; 1')
    body += node_rect(RX, N4y, ['N4: return', '"subdampat"'],
                      w=155, h=44, fill='#A9DFBF', stroke='#1E8449')
    body += node_diamond(CX, N5y, 'N5: if zeta == 1')
    body += node_rect(RX, N6y, ['N6: return', '"critic"'],
                      w=140, h=44, fill='#A9DFBF', stroke='#1E8449')
    body += node_rect(CX, N7y, ['N7: return', '"supradampat"'],
                      w=165, h=44, fill='#A9DFBF', stroke='#1E8449')
    body += node_rounded(CX, N8y, 'N8: END')

    # N1 -> N2
    body += arrow_line(CX, N1y + 18, CX, N2y - 19)
    # N2 -> N3
    body += arrow_line(CX, N2y + 19, CX, N3y - DH)
    # N3 -> N4 (T, right)
    body += arrow_line(CX + DW, N3y, RX - 78, N4y, 'T', lx=CX + DW + 4, ly=N3y - 6)
    # N3 -> N5 (F, down)
    body += arrow_line(CX, N3y + DH, CX, N5y - DH)
    body += lbl(CX + 4, (N3y + DH + N5y - DH) // 2, 'F')
    # N5 -> N6 (T, right)
    body += arrow_line(CX + DW, N5y, RX - 71, N6y, 'T', lx=CX + DW + 4, ly=N5y - 6)
    # N5 -> N7 (F, down)
    body += arrow_line(CX, N5y + DH, CX, N7y - 22)
    body += lbl(CX + 4, (N5y + DH + N7y - 22) // 2, 'F')
    # N7 -> N8
    body += arrow_line(CX, N7y + 22, CX, N8y - 18)

    # N4 -> N8 (dashed curve, right side)
    body += arrow_curve(f'M {RX + 78} {N4y} C {RX + 115} {N4y} {RX + 115} {N8y} {CX + 63} {N8y}',
                        marker='arr-green', color='#1E8449')
    # N6 -> N8 (dashed curve, right side)
    body += arrow_curve(f'M {RX + 71} {N6y} C {RX + 105} {N6y} {RX + 105} {N8y} {CX + 63} {N8y}',
                        marker='arr-green', color='#1E8449')

    body += info_box(15, N8y + 28, [
        'Cai independente (baza V(G)=3):',
        '  P1: N1\u2192N2\u2192N3\u2192N4\u2192N8    (zeta &lt; 1  \u2192 "subdampat")',
        '  P2: N1\u2192N2\u2192N3\u2192N5\u2192N6\u2192N8  (zeta = 1  \u2192 "critic")',
        '  P3: N1\u2192N2\u2192N3\u2192N5\u2192N7\u2192N8  (zeta &gt; 1  \u2192 "supradampat")',
    ])

    with open('images/cfg_damping_type.svg', 'w', encoding='utf-8') as f:
        f.write(make_svg(W, H, body))
    print('Salvat: images/cfg_damping_type.svg')


# ---------------------------------------------------------------------------
# CFG 3: simulate   N=9  E=11  V(G)=4
# ---------------------------------------------------------------------------

def cfg_simulate():
    W, H = 650, 840
    CX, EX = 200, 475
    DW, DH = 88, 29

    body = title(W // 2,
                 'CFG: MassSpringDamper.simulate(x0, v0, t_max, dt)',
                 'N=9  E=11  P=1  \u2192  V(G) = 11 \u2212 9 + 2\u00b71 = 4')

    N1y, N2y, N4y, N6y, N8y, N9y = 85, 180, 300, 420, 545, 670
    N3y, N5y, N7y = N2y, N4y, N6y

    body += node_rounded(CX, N1y, 'N1: START')
    body += node_diamond(CX, N2y, 'N2: if t_max &lt;= 0')
    body += node_error(EX, N3y, ['N3: raise ValueError', '"t_max trebuie &gt; 0"'])
    body += node_diamond(CX, N4y, 'N4: if dt &lt;= 0')
    body += node_error(EX, N5y, ['N5: raise ValueError', '"dt trebuie &gt; 0"'])
    body += node_diamond(CX, N6y, 'N6: if dt &gt;= t_max')
    body += node_error(EX, N7y, ['N7: raise ValueError', '"dt &gt;= t_max"'])
    body += node_rect(CX, N8y, ['N8: return', 'simulate_mass_spring_damper(...)'], h=48)
    body += node_rounded(CX, N9y, 'N9: END')

    body += arrow_line(CX, N1y + 18, CX, N2y - DH)
    body += arrow_line(CX + DW, N2y, EX - 100, N3y, 'T', lx=CX + DW + 4, ly=N2y - 6)
    body += arrow_line(CX, N2y + DH, CX, N4y - DH)
    body += lbl(CX + 4, (N2y + DH + N4y - DH) // 2, 'F')
    body += arrow_line(CX + DW, N4y, EX - 100, N5y, 'T', lx=CX + DW + 4, ly=N4y - 6)
    body += arrow_line(CX, N4y + DH, CX, N6y - DH)
    body += lbl(CX + 4, (N4y + DH + N6y - DH) // 2, 'F')
    body += arrow_line(CX + DW, N6y, EX - 100, N7y, 'T', lx=CX + DW + 4, ly=N6y - 6)
    body += arrow_line(CX, N6y + DH, CX, N8y - 24)
    body += lbl(CX + 4, (N6y + DH + N8y - 24) // 2, 'F')
    body += arrow_line(CX, N8y + 24, CX, N9y - 18)

    ex_r = EX + 100
    body += arrow_curve(f'M {ex_r} {N3y} C {ex_r+55} {N3y} {ex_r+55} {N9y} {CX+63} {N9y}')
    body += arrow_curve(f'M {ex_r} {N5y} C {ex_r+45} {N5y} {ex_r+45} {N9y} {CX+63} {N9y}')
    body += arrow_curve(f'M {ex_r} {N7y} C {ex_r+35} {N7y} {ex_r+35} {N9y} {CX+63} {N9y}')

    body += info_box(15, N9y + 28, [
        'Cai independente (baza V(G)=4):',
        '  P1: N1\u2192N2\u2192N3\u2192N9            (t_max invalid \u2192 ValueError)',
        '  P2: N1\u2192N2\u2192N4\u2192N5\u2192N9         (dt invalid \u2192 ValueError)',
        '  P3: N1\u2192N2\u2192N4\u2192N6\u2192N7\u2192N9      (dt &gt;= t_max \u2192 ValueError)',
        '  P4: N1\u2192N2\u2192N4\u2192N6\u2192N8\u2192N9      (toti valizi \u2192 simulare)',
    ])

    with open('images/cfg_simulate.svg', 'w', encoding='utf-8') as f:
        f.write(make_svg(W, H, body))
    print('Salvat: images/cfg_simulate.svg')


if __name__ == '__main__':
    cfg_init()
    cfg_damping_type()
    cfg_simulate()
    print('Toate grafurile CFG au fost generate cu succes.')

