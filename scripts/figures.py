"""Rysunki do dokumentu 'Odpowiedzi na pytania kontrolne' (ćw. T2 - Pomiary napięć i prądów stałych)."""
import os
import matplotlib
matplotlib.use('Agg')
import schemdraw
import schemdraw.elements as elm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'build', 'figs')
os.makedirs(OUT, exist_ok=True)

BASE = dict(unit=1.6, fontsize=11, lw=1.7, color='black')


def save(d, name):
    path = os.path.join(OUT, name)
    d.save(path, dpi=300)
    return path


def source_branch(d, x=0.0, ytop=3.0, ybot=0.0, rw=(0.75, 2.55)):
    """Gałąź: źródło E + rezystancja Rw (górna gałąź); wraca przez (x, ybot)."""
    d += elm.SourceV().at((x, ybot + 0.6)).to((x, ytop - 0.4)).label('$E$', loc='left', ofst=0.14)
    d += elm.Line().at((x, ybot + 0.6)).to((x, ybot))
    d += elm.Line().at((x, ytop - 0.4)).to((x, ytop))
    d += elm.Resistor().at((rw[0], ytop)).to((rw[1], ytop)).label('$R_w$', loc='top', ofst=0.14)


# ------------------------------------------------------------------ Rys. 1
# Schemat zastępczy rzeczywistego źródła napięcia z zaciskami A i B
def fig_source():
    with schemdraw.Drawing(show=False) as d:
        d.config(**BASE)
        source_branch(d)
        d += elm.Line().at((0, 3.0)).to((0.75, 3.0))
        d += elm.Line().at((2.55, 3.0)).to((4.4, 3.0))
        d += elm.Line().at((0, 0)).to((4.4, 0))
        d += elm.Dot().at((4.4, 3.0))
        d += elm.Dot().at((4.4, 0))
        d += elm.Label().at((4.55, 3.0)).label('$A$', loc='right')
        d += elm.Label().at((4.55, 0.0)).label('$B$', loc='right')
        d += elm.Arrow(double=True).at((5.25, 0.1)).to((5.25, 2.9))
        d += elm.Label().at((5.32, 1.5)).label(r'$U_{AB}$', loc='right')
    return save(d, 'rys1_zrodlo.png')


# ------------------------------------------------------------------ Rys. 2
# Błąd metody: woltomierz o skończonej rezystancji RV dołączony do źródła
def fig_voltmeter():
    with schemdraw.Drawing(show=False) as d:
        d.config(**BASE)
        source_branch(d)
        d += elm.Line().at((0, 3.0)).to((0.75, 3.0))
        d += elm.Line().at((2.55, 3.0)).to((3.6, 3.0))
        d += elm.Dot().at((3.6, 3.0))
        d += elm.Line().at((3.6, 3.0)).to((3.6, 2.6))
        d += elm.MeterV().at((3.6, 2.6)).to((3.6, 0.4)).label('$R_V$', loc='right', ofst=0.22)
        d += elm.Line().at((3.6, 0.4)).to((3.6, 0))
        d += elm.Dot().at((3.6, 0))
        d += elm.Line().at((0, 0)).to((3.6, 0))
        d += elm.CurrentLabel(top=True).at((3.6, 1.9)).label('$I_V$', ofst=0.55)
        d += elm.Arrow(double=True).at((4.35, 0.1)).to((4.35, 2.9))
        d += elm.Label().at((4.42, 1.5)).label('$U_V$', loc='right')
    return save(d, 'rys2_woltomierz.png')


# ------------------------------------------------------------------ Rys. 3
# Amperomierz szeregowo, woltomierz równolegle
def fig_meters():
    with schemdraw.Drawing(show=False) as d:
        d.config(**BASE)
        d += elm.SourceV().at((0, 0.6)).to((0, 2.6)).label('$E$', loc='left', ofst=0.14)
        d += elm.Line().at((0, 0.6)).to((0, 0))
        d += elm.Line().at((0, 2.6)).to((0, 3.0))
        d += elm.Line().at((0, 3.0)).to((0.9, 3.0))
        d += elm.MeterA().at((0.9, 3.0)).to((1.9, 3.0)).label('$R_A$', loc='top', ofst=0.14)
        d += elm.Line().at((1.9, 3.0)).to((3.7, 3.0))
        d += elm.Dot().at((3.7, 3.0))
        d += elm.Line().at((3.7, 3.0)).to((4.8, 3.0))
        d += elm.Resistor().at((4.8, 3.0)).to((4.8, 1.3)).label('$R$', loc='right', ofst=0.2)
        d += elm.Line().at((4.8, 1.3)).to((4.8, 0))
        d += elm.Dot().at((4.8, 1.3))
        d += elm.Line().at((0, 0)).to((4.8, 0))
        d += elm.Line().at((3.7, 3.0)).to((3.7, 2.5))
        d += elm.MeterV().at((3.7, 2.5)).to((3.7, 0.5)).label('$R_V$', loc='left', ofst=0.22)
        d += elm.Line().at((3.7, 0.5)).to((3.7, 0))
        d += elm.Dot().at((3.7, 0))
    return save(d, 'rys3_mierniki.png')


# ------------------------------------------------------------------ Rys. 4
# Układ do pomiaru SEM metodą kompensacyjną
def fig_compensation():
    with schemdraw.Drawing(show=False) as d:
        d.config(**BASE)
        source_branch(d, rw=(0.6, 1.9))
        d += elm.Line().at((0, 3.0)).to((0.6, 3.0))
        d += elm.Line().at((1.9, 3.0)).to((2.5, 3.0))
        d += elm.Dot().at((2.5, 3.0))
        d += elm.MeterV().at((2.5, 3.0)).to((3.5, 3.0)).label('$W$', loc='top', ofst=0.18)
        d += elm.Line().at((3.5, 3.0)).to((4.3, 3.0))
        d += elm.Dot().at((4.3, 3.0))
        d += elm.Line().at((4.3, 3.0)).to((4.3, 2.55))
        d += elm.MeterV().at((4.3, 2.55)).to((4.3, 0.45)).label('$V$', loc='left', ofst=0.3)
        d += elm.Line().at((4.3, 0.45)).to((4.3, 0))
        d += elm.Dot().at((4.3, 0))
        d += elm.Line().at((4.3, 3.0)).to((5.9, 3.0))
        d += elm.Resistor().at((5.9, 3.0)).to((5.9, 1.75)).label('$R_{wz}$', loc='right', ofst=0.2)
        d += elm.SourceV().at((5.9, 1.75)).to((5.9, 0.55)).label('$E_{wz}$', loc='right', ofst=0.2)
        d += elm.Line().at((5.9, 0.55)).to((5.9, 0))
        d += elm.Line().at((5.9, 0)).to((4.3, 0))
        d += elm.Line().at((4.3, 0)).to((0, 0))
        d += elm.Arrow(double=True).at((4.9, 0.1)).to((4.9, 2.9))
        d += elm.Label().at((4.97, 1.5)).label('$U_{wz}$', loc='right')
    return save(d, 'rys4_kompensacja.png')


# ------------------------------------------------------------------ Rys. 5
# Charakterystyka zewnętrzna źródła: idealne vs rzeczywiste
def fig_characteristic():
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams['font.family'] = 'DejaVu Sans'
    rcParams['mathtext.fontset'] = 'dejavusans'
    E, Rw = 10.0, 2.0
    Ik = E / Rw
    fig, ax = plt.subplots(figsize=(5.2, 3.1), dpi=300)
    ax.plot([0, Ik + 1], [E, E], lw=2.0, color='#1a5fb4', label=r'źródło idealne ($R_w=0$)')
    ax.plot([0, Ik], [E, 0], lw=2.0, color='#c01c28', label=r'źródło rzeczywiste ($R_w>0$)')
    ax.plot([0, Ik], [E, E], ls=':', lw=1.1, color='0.4')
    ax.plot([Ik, Ik], [0, E], ls=':', lw=1.1, color='0.4')
    ax.plot([0], [E], 'o', ms=4, color='0.2')
    ax.plot([Ik], [0], 'o', ms=4, color='0.2')
    ax.annotate(r'$I_k = E/R_w$', xy=(Ik, 0), xytext=(Ik - 0.35, 1.6),
                arrowprops=dict(arrowstyle='->', lw=1.0, color='0.35'), fontsize=10)
    ax.annotate(r'$\Delta U = I\,R_w$', xy=(3.0, 4.0), xytext=(3.35, 1.3),
                arrowprops=dict(arrowstyle='->', lw=1.0, color='0.35'), fontsize=10)
    ax.annotate(r'$E$', xy=(0, E), xytext=(-0.62, E + 0.2), fontsize=11)
    ax.set_xlim(0, Ik + 1)
    ax.set_ylim(0, E * 1.18)
    ax.set_xlabel('prąd obciążenia $I$  [A]', fontsize=10)
    ax.set_ylabel('napięcie $U$  [V]', fontsize=10)
    ax.grid(alpha=0.25, lw=0.6)
    ax.legend(fontsize=8.5, loc='upper right', framealpha=1.0)
    ax.tick_params(labelsize=9)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    path = os.path.join(OUT, 'rys5_charakterystyka.png')
    fig.savefig(path, dpi=300, facecolor='white')
    plt.close(fig)
    return path


if __name__ == '__main__':
    for f in (fig_source, fig_voltmeter, fig_meters, fig_compensation, fig_characteristic):
        print(f())
