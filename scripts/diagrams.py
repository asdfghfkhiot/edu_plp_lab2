"""Rysunki schematów do dokumentu z odpowiedziami (ćw. T2).

Rysunki rysowane są bezpośrednio prymitywami matplotlib, dzięki czemu
każdy element ma ustalone położenie.
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import rcParams

rcParams['font.family'] = 'DejaVu Sans'
rcParams['mathtext.fontset'] = 'dejavusans'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'build', 'figs')
os.makedirs(OUT, exist_ok=True)

INK = '#101010'
LW = 1.6
FS = 11.5


def new_ax(xlim, ylim):
    w = (xlim[1] - xlim[0]) * 0.42
    h = (ylim[1] - ylim[0]) * 0.42
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=320, facecolor='white', bbox_inches='tight', pad_inches=0.04)
    plt.close(fig)
    return path


def wire(ax, *pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=INK, lw=LW, solid_capstyle='round',
            solid_joinstyle='round', zorder=2)


def dot(ax, x, y, r=0.055):
    ax.add_patch(Circle((x, y), r, facecolor=INK, edgecolor='none', zorder=5))


def txt(ax, x, y, s, ha='center', va='center', fs=FS, weight='normal'):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=INK, zorder=7,
            fontweight=weight)


def resistor(ax, p0, p1, amp=0.10, n=6):
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    d = p1 - p0
    L = np.linalg.norm(d)
    u = d / L
    perp = np.array([-u[1], u[0]])
    a = p0 + u * (0.16 * L)
    b = p1 - u * (0.16 * L)
    pts = [p0, a]
    for i in range(n):
        t = (i + 0.5) / n
        s = 1.0 if i % 2 == 0 else -1.0
        pts.append(a + (b - a) * t + perp * amp * s)
    pts += [b, p1]
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=INK, lw=LW,
            solid_capstyle='round', solid_joinstyle='round', zorder=3)


def circle(ax, x, y, r=0.40, label=None, fs=FS - 1):
    ax.add_patch(Circle((x, y), r, facecolor='white', edgecolor=INK,
                        lw=LW, zorder=4))
    if label:
        txt(ax, x, y, label, fs=fs, weight='bold')


def source(ax, x, y, r=0.40, lab='$E$', side='left'):
    circle(ax, x, y, r)
    txt(ax, x, y + 0.155, '+', fs=13)
    txt(ax, x, y - 0.175, '–', fs=13)
    if side == 'left':
        txt(ax, x - r - 0.12, y, lab, ha='right')
    elif side == 'right':
        txt(ax, x + r + 0.12, y, lab, ha='left')
    elif side == 'below':
        txt(ax, x, y - r - 0.22, lab, va='top')
    else:
        txt(ax, x, y + r + 0.22, lab, va='bottom')


def darrow(ax, p0, p1, lab=None, side='right', fs=FS):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle='<|-|>', lw=1.0, color=INK,
                                shrinkA=0, shrinkB=0, mutation_scale=9),
                zorder=6)
    if lab:
        x = max(p0[0], p1[0])
        y = (p0[1] + p1[1]) / 2
        if side == 'right':
            txt(ax, x + 0.10, y, lab, ha='left')
        else:
            txt(ax, x - 0.10, y, lab, ha='right')


def iarrow(ax, x0, x1, y, lab, above=True):
    ax.annotate('', xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle='-|>', lw=1.0, color=INK,
                                shrinkA=0, shrinkB=0, mutation_scale=9),
                zorder=6)
    txt(ax, (x0 + x1) / 2, y + (0.24 if above else -0.24), lab,
        va='bottom' if above else 'top')


# ------------------------------------------------------------------ Rys. 1
def fig_source():
    fig, ax = new_ax((-0.75, 5.6), (-0.30, 3.35))
    source(ax, 0, 1.15)
    wire(ax, (0, 0), (0, 0.75))
    wire(ax, (0, 1.55), (0, 3.1))
    wire(ax, (0, 3.1), (0.5, 3.1))
    resistor(ax, (0.5, 3.1), (1.85, 3.1))
    txt(ax, 1.17, 3.42, '$R_w$')
    wire(ax, (1.85, 3.1), (4.2, 3.1))
    wire(ax, (0, 0), (4.2, 0))
    dot(ax, 4.2, 3.1)
    dot(ax, 4.2, 0)
    txt(ax, 4.40, 3.1, '$A$', ha='left')
    txt(ax, 4.40, 0.0, '$B$', ha='left')
    darrow(ax, (4.78, 0.08), (4.78, 3.02), '$U_{AB}$', side='right')
    txt(ax, 0.52, 1.15, '', ha='left')
    return save(fig, 'fig02_zrodlo.png')


# ------------------------------------------------------------------ Rys. 2
def fig_voltmeter():
    fig, ax = new_ax((-0.75, 5.55), (-0.30, 3.35))
    source(ax, 0, 1.15)
    wire(ax, (0, 0), (0, 0.75))
    wire(ax, (0, 1.55), (0, 3.1))
    wire(ax, (0, 3.1), (0.5, 3.1))
    resistor(ax, (0.5, 3.1), (1.85, 3.1))
    txt(ax, 1.17, 3.42, '$R_w$')
    wire(ax, (1.85, 3.1), (3.35, 3.1))
    dot(ax, 3.35, 3.1)
    wire(ax, (3.35, 3.1), (3.35, 2.62))
    circle(ax, 3.35, 2.22, 0.40, '$V$')
    wire(ax, (3.35, 1.82), (3.35, 0))
    dot(ax, 3.35, 0)
    wire(ax, (0, 0), (3.35, 0))
    txt(ax, 3.90, 2.22, '$R_V$', ha='left')
    iarrow(ax, 2.45, 3.05, 3.1, '$I_V$')
    darrow(ax, (4.62, 0.08), (4.62, 3.02), '$U_V$', side='right')
    return save(fig, 'fig04_woltomierz.png')


def source_with_meter(ax, mv, rv, uv, ref):
    source(ax, 0, 1.15)
    wire(ax, (0, 0), (0, 0.75))
    wire(ax, (0, 1.55), (0, 3.1))
    wire(ax, (0, 3.1), (0.5, 3.1))
    resistor(ax, (0.5, 3.1), (1.85, 3.1))
    txt(ax, 1.17, 3.42, '$R_w$')
    wire(ax, (1.85, 3.1), (3.05, 3.1))
    dot(ax, 3.05, 3.1)
    wire(ax, (3.05, 3.1), (3.05, 2.62))
    circle(ax, 3.05, 2.22, 0.40, mv)
    wire(ax, (3.05, 1.82), (3.05, 0))
    dot(ax, 3.05, 0)
    wire(ax, (0, 0), (3.05, 0))
    txt(ax, 3.80, 2.22, rv, ha='left')
    darrow(ax, (4.55, 0.08), (4.55, 3.02), uv, side='right')
    txt(ax, 1.55, 0.0, ref, va='top')


# ------------------------------------------------------------------ Rys. 3
def fig_meters():
    fig, ax = new_ax((-0.75, 5.6), (-0.30, 3.35))
    source(ax, 0, 1.15)
    wire(ax, (0, 0), (0, 0.75))
    wire(ax, (0, 1.55), (0, 3.1))
    wire(ax, (0, 3.1), (0.85, 3.1))
    circle(ax, 1.25, 3.1, 0.40, '$A$')
    wire(ax, (1.65, 3.1), (2.85, 3.1))
    txt(ax, 1.25, 3.82, '$R_A$')
    dot(ax, 2.85, 3.1)
    wire(ax, (2.85, 3.1), (4.45, 3.1))
    wire(ax, (4.45, 3.1), (4.45, 2.62))
    resistor(ax, (4.45, 2.62), (4.45, 1.35))
    txt(ax, 4.72, 2.0, '$R$', ha='left')
    wire(ax, (4.45, 1.35), (4.45, 0))
    wire(ax, (0, 0), (4.45, 0))
    wire(ax, (2.85, 3.1), (2.85, 2.62))
    circle(ax, 2.85, 2.22, 0.40, '$V$')
    wire(ax, (2.85, 1.82), (2.85, 0))
    txt(ax, 2.36, 2.22, '$R_V$', ha='right')
    dot(ax, 2.85, 0)
    iarrow(ax, 3.15, 3.75, 3.1, '$I$')
    return save(fig, 'fig03_mierniki.png')


# ------------------------------------------------------------------ Rys. 4
def fig_compensation():
    fig, ax = new_ax((-0.75, 7.35), (-0.30, 3.80))
    source(ax, 0, 1.15)
    wire(ax, (0, 0), (0, 0.75))
    wire(ax, (0, 1.55), (0, 3.1))
    wire(ax, (0, 3.1), (0.45, 3.1))
    resistor(ax, (0.45, 3.1), (1.75, 3.1))
    txt(ax, 1.05, 3.60, '$R_w$')
    wire(ax, (1.75, 3.1), (2.30, 3.1))
    dot(ax, 2.30, 3.1)
    circle(ax, 2.80, 3.1, 0.40, '$W$')
    wire(ax, (3.20, 3.1), (4.10, 3.1))
    dot(ax, 4.10, 3.1)
    wire(ax, (4.10, 3.1), (4.10, 2.62))
    circle(ax, 4.10, 2.22, 0.40, '$V$')
    wire(ax, (4.10, 1.82), (4.10, 0))
    dot(ax, 4.10, 0)
    wire(ax, (4.10, 3.1), (6.10, 3.1))
    wire(ax, (6.10, 3.1), (6.10, 2.62))
    resistor(ax, (6.10, 2.62), (6.10, 1.62))
    txt(ax, 6.37, 2.12, '$R_{wz}$', ha='left')
    wire(ax, (6.10, 1.62), (6.10, 1.55))
    source(ax, 6.10, 1.15, lab='', side='none')
    txt(ax, 6.72, 1.15, '$E_{wz}$', ha='left')
    wire(ax, (6.10, 0.75), (6.10, 0))
    wire(ax, (6.10, 0), (0, 0))
    darrow(ax, (4.75, 0.08), (4.75, 3.02), '$U_{wz}$', side='right')
    return save(fig, 'fig06_kompensacja.png')


# ------------------------------------------------------------------ Rys. 5
def fig_characteristic():
    fig, ax = plt.subplots(figsize=(5.4, 3.15))
    E, Rw = 10.0, 2.0
    Ik = E / Rw
    ax.plot([0, Ik + 1.2], [E, E], lw=2.0, color='#1a5fb4',
            label=r'źródło idealne ($R_w = 0$)')
    ax.plot([0, Ik], [E, 0], lw=2.0, color='#c01c28',
            label=r'źródło rzeczywiste ($R_w > 0$)')
    ax.plot([0, Ik], [E, E], ls=':', lw=1.1, color='0.45')
    ax.plot([Ik, Ik], [0, E], ls=':', lw=1.1, color='0.45')
    ax.plot([0], [E], 'o', ms=4.5, color='0.15')
    ax.plot([Ik], [0], 'o', ms=4.5, color='0.15')
    ax.annotate(r'$I_k = E/R_w$', xy=(Ik, 0), xytext=(Ik - 0.30, 1.55),
                arrowprops=dict(arrowstyle='->', lw=1.0, color='0.35'),
                fontsize=10)
    ax.annotate(r'$\Delta U = I\,R_w$', xy=(3.0, 4.0), xytext=(3.55, 1.75),
                arrowprops=dict(arrowstyle='->', lw=1.0, color='0.35'),
                fontsize=10)
    ax.annotate(r'$E$', xy=(0, E), xytext=(-0.62, E - 0.1), fontsize=11)
    ax.set_xlim(0, Ik + 1.2)
    ax.set_ylim(0, E * 1.14)
    ax.set_xlabel('prąd obciążenia $I$  [A]', fontsize=9.5)
    ax.set_ylabel('napięcie $U$  [V]', fontsize=9.5)
    ax.grid(alpha=0.25, lw=0.6)
    ax.legend(fontsize=8.8, loc='lower left', framealpha=1.0,
              borderpad=0.6, handlelength=2.2)
    ax.tick_params(labelsize=9)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    path = os.path.join(OUT, 'fig01_charakterystyka.png')
    fig.savefig(path, dpi=320, facecolor='white')
    plt.close(fig)
    return path


# ------------------------------------------------------------------ Rys. 6
def fig_two_voltmeters():
    fig, axs = plt.subplots(1, 2, figsize=(8.6, 2.5))
    for ax, (mv, rv, uv, ref) in zip(
            axs,
            [('$V_1$', '$R_{V1}$', '$U_1$', '(a)'),
             ('$V_2$', '$R_{V2}$', '$U_2$', '(b)')]):
        ax.set_xlim(-0.75, 5.25)
        ax.set_ylim(-0.50, 3.35)
        ax.set_aspect('equal')
        ax.axis('off')
        source_with_meter(ax, mv, rv, uv, ref)
    fig.subplots_adjust(0.01, 0.01, 0.99, 0.99, wspace=0.06)
    path = os.path.join(OUT, 'fig05_dwa_woltomierze.png')
    fig.savefig(path, dpi=320, facecolor='white', bbox_inches='tight',
                pad_inches=0.05)
    plt.close(fig)
    return path


# ------------------------------------------------------------------ Rys. 7
def fig_rv_influence():
    """U/E w funkcji stosunku RV/Rw - ilustracja do pytania 16."""
    fig, ax = plt.subplots(figsize=(5.2, 2.85))
    x = np.logspace(-1.2, 3.2, 400)
    y = 1.0 / (1.0 + 1.0 / x)
    ax.semilogx(x, y * 100, lw=2.0, color='#1a5fb4')
    for xv, lab in ((1.0, '50 %'), (10.0, '90,9 %'), (100.0, '99,0 %')):
        ax.plot([xv], [100.0 / (1 + 1 / xv)], 'o', ms=4.5, color='#c01c28', zorder=5)
        ax.annotate(lab, xy=(xv, 100.0 / (1 + 1 / xv)),
                    xytext=(xv * 1.30, 100.0 / (1 + 1 / xv) - 11),
                    fontsize=8.6, color='#7a1220')
    ax.axhline(100, color='0.55', lw=0.9, ls=':')
    ax.text(0.14, 101.5, 'wartość poprawna (E)', fontsize=8.2, color='0.35')
    ax.set_xlim(0.06, 1600)
    ax.set_ylim(0, 112)
    ax.set_xlabel(r'stosunek rezystancji $R_V/R_w$', fontsize=9)
    ax.set_ylabel(r'wynik pomiaru $U_V/E$  [%]', fontsize=9)
    ax.grid(alpha=0.25, lw=0.6, which='major')
    ax.tick_params(labelsize=8.5)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    path = os.path.join(OUT, 'fig07_wplyw_rv.png')
    fig.savefig(path, dpi=320, facecolor='white')
    plt.close(fig)
    return path


if __name__ == '__main__':
    for f in (fig_source, fig_voltmeter, fig_meters, fig_compensation,
              fig_characteristic, fig_two_voltmeters, fig_rv_influence):
        print(f())
