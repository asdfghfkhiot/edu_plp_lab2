"""Wersja skrócona: „ściąga” z ćwiczenia T2 na 4 strony A4.

Uruchomienie:  .venv/bin/python scripts/build_cheatsheet.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pdfkit as K
from pdfkit import (S, Eq, MathImg, data_table, CONTENT_W, NAVY, ACCENT, GREY,
                    RULE, LIGHT, LIGHT2, PAGE_W, PAGE_H)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle, Flowable,
                                Frame, PageTemplate, BaseDocTemplate, PageBreak)

ROOT = K.ROOT
FIG = K.FIGDIR
OUT = os.path.join(ROOT, 'Cwiczenie_T2_-_sciaga.pdf')

HEAD_H = 1.28 * cm      # wysokość paska nagłówka
FOOT_H = 0.95 * cm
LM = RM = 1.35 * cm
TM = HEAD_H + 0.42 * cm
BM = FOOT_H + 0.36 * cm
CW = PAGE_W - LM - RM

BODY = 7.9
LEAD = 10.4

ST = {}
ST['b'] = ParagraphStyle('b', fontName='Serif', fontSize=BODY, leading=LEAD,
                         alignment=TA_JUSTIFY, textColor=colors.HexColor('#14181d'),
                         spaceAfter=2.4, hyphenationLang='pl_PL',
                         embeddedHyphenation=1, splitLongWords=1)
ST['bl'] = ParagraphStyle('bl', parent=ST['b'], alignment=TA_LEFT)
ST['bullet'] = ParagraphStyle('bullet', parent=ST['b'], leftIndent=9.5,
                              bulletIndent=1.5, spaceAfter=1.4,
                              bulletFontSize=BODY)
ST['q'] = ParagraphStyle('q', fontName='Sans-Bold', fontSize=8.5, leading=10.6,
                         textColor=colors.white, alignment=TA_LEFT)
ST['n'] = ParagraphStyle('n', fontName='Sans-Bold', fontSize=8.6, leading=10.6,
                         textColor=colors.white, alignment=TA_CENTER)
ST['sec'] = ParagraphStyle('sec', fontName='Sans-Bold', fontSize=8.9, leading=11,
                           textColor=NAVY, alignment=TA_LEFT)
ST['th'] = ParagraphStyle('th', fontName='Sans-Bold', fontSize=7.4, leading=9.2,
                          textColor=colors.white, alignment=TA_LEFT)
ST['thc'] = ParagraphStyle('thc', parent=ST['th'], alignment=TA_CENTER)
ST['td'] = ParagraphStyle('td', fontName='Serif', fontSize=7.5, leading=9.6,
                          alignment=TA_LEFT, textColor=colors.HexColor('#14181d'))
ST['tdc'] = ParagraphStyle('tdc', parent=ST['td'], alignment=TA_CENTER)
ST['cap'] = ParagraphStyle('cap', fontName='Sans', fontSize=6.7, leading=8.4,
                           textColor=GREY, alignment=TA_LEFT, spaceAfter=3)


def P(t, st='b'):
    return Paragraph(t, ST[st])


def bullets(items):
    return [Paragraph(t, ST['bullet'], bulletText='\u2022') for t in items]


class SectionBar(Flowable):
    """Pasek nagłówka sekcji z numerem rzymskim."""

    def __init__(self, rzym, title, h=0.52 * cm):
        super().__init__()
        self.rzym = rzym
        self.title = title
        self.hh = h
        self.p = Paragraph(title, ParagraphStyle(
            'sech', fontName='Sans-Bold', fontSize=8.6, leading=10.4,
            textColor=colors.white, alignment=TA_LEFT))

    def wrap(self, aw, ah):
        self.p.wrap(CW - 1.3 * cm, ah)
        return CW, self.hh + 4

    def draw(self):
        c = self.canv
        h = self.hh
        c.setFillColor(NAVY)
        c.rect(0, 4, CW, h, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont('Sans-Bold', 8.6)
        c.drawString(0.18 * cm, 4 + h / 2 - 2.9, f'{self.rzym}.')
        self.p.drawOn(c, 1.08 * cm, 4 + h / 2 - 2.9 - 0.7)


def QBox(pairs, widths, header):
    """Siatka: kolumna numerów pytań + treść. Zwraca listę flowable."""
    rows = []
    for num, cell in pairs:
        head = [Paragraph(str(num), ST['n'])]
        rows.append([head, cell])
    data = [[Paragraph(header, ST['thc']), Paragraph(
        'Pytanie \u2192 odpowiedź / wzór', ST['th'])]]
    # wiersze z numerami w nagłówkowej kolumnie
    out = []
    nw = widths[0]
    tw = widths[1]
    body = []
    for num, cell in pairs:
        body.append([Paragraph(str(num), ParagraphStyle(
            f'nn{num}', fontName='Sans-Bold', fontSize=8.4, leading=10,
            textColor=colors.white, alignment=TA_CENTER)), cell])
    t = Table(body, colWidths=[nw, tw], hAlign='LEFT')
    style = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, -1), NAVY),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('LEFTPADDING', (0, 0), (0, -1), 2),
        ('RIGHTPADDING', (0, 0), (0, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2.6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.6),
        ('LEFTPADDING', (1, 0), (1, -1), 5),
        ('RIGHTPADDING', (1, 0), (1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor('#ccd7e4')),
        ('BOX', (0, 0), (-1, -1), 0.4, NAVY),
        ('LINEAFTER', (0, 0), (0, -1), 0.4, NAVY),
    ]
    for i in range(len(body)):
        if i % 2 == 1:
            style.append(('BACKGROUND', (1, i), (1, i), LIGHT2))
    t.setStyle(TableStyle(style))
    out.append(t)
    return out


def qtable(rows, widths, align=None, header=True):
    data = []
    for r_i, row in enumerate(rows):
        cells = []
        for c_i, cell in enumerate(row):
            if isinstance(cell, str):
                if header and r_i == 0:
                    cells.append(Paragraph(
                        cell, ST['thc'] if (align and align[c_i] == 'c') else ST['th']))
                else:
                    cells.append(Paragraph(
                        cell, ST['tdc'] if (align and align[c_i] == 'c') else ST['td']))
            else:
                cells.append(cell)
        data.append(cells)
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign='LEFT')
    style = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3.2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3.2),
        ('TOPPADDING', (0, 0), (-1, -1), 1.9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.9),
        ('LINEBELOW', (0, 0), (-1, -1), 0.28, colors.HexColor('#d2dbe6')),
        ('BOX', (0, 0), (-1, -1), 0.4, colors.HexColor('#c3cedc')),
    ]
    if header:
        style += [('BACKGROUND', (0, 0), (-1, 0), NAVY)]
    n0 = 1 if header else 0
    for i in range(n0, len(data)):
        if (i - n0) % 2 == 1:
            style.append(('BACKGROUND', (0, i), (-1, i), LIGHT2))
    t.setStyle(TableStyle(style))
    return t


# --------------------------------------------------------------- szablon strony
class SheetCanvas(K.NumberedCanvas):
    pass


def draw_headfoot(c, total_pages, section_label):
    c.saveState()
    # ---- pasek nagłówka
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - HEAD_H, PAGE_W, HEAD_H, stroke=0, fill=1)
    c.setFillColor(colors.HexColor('#2c6cb0'))
    c.rect(0, PAGE_H - HEAD_H, PAGE_W, 0.075 * cm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont('Sans-Bold', 11.2)
    c.drawString(LM, PAGE_H - 0.60 * cm, '\u0106wiczenie T2 \u00b7 \u015aci\u0105ga')
    c.setFont('Sans', 7.3)
    c.setFillColor(colors.HexColor('#b9d0ea'))
    c.drawString(LM, PAGE_H - 0.95 * cm,
                 'Pomiary napi\u0119\u0107 i pr\u0105d\u00f3w sta\u0142ych \u00b7 szybka powt\u00f3rka przed zaliczeniem')
    if section_label:
        c.setFillColor(colors.white)
        c.setFont('Sans-Bold', 7.0)
        c.drawRightString(PAGE_W - RM, PAGE_H - 0.60 * cm, section_label)
    c.setFillColor(colors.HexColor('#b9d0ea'))
    c.setFont('Sans', 6.9)
    c.drawRightString(PAGE_W - RM, PAGE_H - 0.95 * cm,
                      'wersja skr\u00f3cona \u00b7 pe\u0142ne wyprowadzenia: dokument 21-stronicowy')
    # ---- stopka
    c.setStrokeColor(RULE)
    c.setLineWidth(0.45)
    c.line(LM, FOOT_H, PAGE_W - RM, FOOT_H)
    c.setFillColor(GREY)
    c.setFont('Sans', 6.6)
    c.drawString(LM, 0.55 * cm, 'Laboratorium Podstaw Pomiar\u00f3w \u00b7 ISE WEiTI PW')
    c.drawRightString(PAGE_W - RM, 0.55 * cm, f'str. {c._pageNumber} z {total_pages}')
    c.restoreState()


SECTIONS = {}


class SheetCanvas2(K.NumberedCanvas):
    """Canvas, który zna etykietę sekcji dla każdej strony."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._pagemarks = []

    def showPage(self):
        self._pagemarks.append(getattr(self, '_cur_section', ''))
        super().showPage()

    def save(self):
        total = len(self._saved)
        for i, st in enumerate(self._saved):
            self.__dict__.update(st)
            if self._pageNumber > 1:
                lbl = self._pagemarks[i] if i < len(self._pagemarks) else ''
                draw_headfoot(self, total, lbl)
            K.canvas_module.Canvas.showPage(self)
        K.canvas_module.Canvas.save(self)


class MarkSection(Flowable):
    """Niewidoczny znacznik: ustawia etykietę sekcji dla bieżącej strony."""

    def __init__(self, label):
        super().__init__()
        self.label = label

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        self.canv._cur_section = self.label

# =================================================================== TREŚĆ
def banner():
    """Kompaktowy pasek tytułowy na początku strony 1 (zamiast osobnej okładki)."""
    st = []
    H = 2.55 * cm

    class _Draw(Flowable):
        def wrap(self, aw, ah):
            return CW, H

        def draw(self):
            cv = self.canv
            cv.setFillColor(NAVY)
            cv.rect(0, 0, CW, H, stroke=0, fill=1)
            cv.setFillColor(colors.HexColor('#2c6cb0'))
            cv.rect(0, H - 0.07 * cm, CW, 0.07 * cm, stroke=0, fill=1)

            cv.setFillColor(colors.HexColor('#8fb3d9'))
            cv.setFont('Sans', 6.6)
            cv.drawString(0.45 * cm, H - 0.58 * cm,
                          'LABORATORIUM PODSTAW POMIARÓW \u00b7 ISE WEiTI PW \u00b7 '
                          'INSTRUKCJA v. 2.4')

            cv.setFillColor(colors.white)
            cv.setFont('Sans-Bold', 21)
            cv.drawString(0.42 * cm, H - 1.42 * cm, '\u0106wiczenie T2 \u00b7 \u015aci\u0105ga')

            cv.setFillColor(colors.HexColor('#dce8f7'))
            cv.setFont('Sans', 9.6)
            cv.drawString(0.45 * cm, H - 1.95 * cm,
                          'Pomiary napięć i prądów stałych \u2013 22 pytania kontrolne')
            cv.drawString(0.45 * cm, H - 2.22 * cm,
                          'wzory \u00b7 liczby \u00b7 schematy \u00b7 pułapki na zaliczeniu')

            # ramka z informacją po prawej
            cv.setFillColor(colors.HexColor('#1b4470'))
            cv.rect(CW - 5.35 * cm, 0.32 * cm, 5.0 * cm, H - 0.86 * cm,
                    stroke=0, fill=1)
            cv.setFillColor(colors.HexColor('#a8c6e8'))
            cv.setFont('Sans', 6.5)
            cv.drawString(CW - 5.12 * cm, H - 1.02 * cm, 'WERSJA SKR\u00d3CONA')
            cv.setFillColor(colors.white)
            cv.setFont('Sans-Bold', 7.6)
            cv.drawString(CW - 5.12 * cm, H - 1.36 * cm, '4 strony A4 \u00b7 do druku')
            cv.setFillColor(colors.HexColor('#a8c6e8'))
            cv.setFont('Sans', 6.5)
            cv.drawString(CW - 5.12 * cm, H - 1.66 * cm, 'pe\u0142ne wyprowadzenia:')
            cv.drawString(CW - 5.12 * cm, H - 1.90 * cm, 'dokument 21-stronicowy')
    st.append(_Draw())
    st.append(Spacer(1, 5))
    return st


def page1():
    st = [MarkSection('I\u2013III \u00b7 \u017ar\u00f3d\u0142o, mierniki, b\u0142\u0105d metody')]
    st += [SectionBar('I', '\u0179R\u00d3D\u0141O NAPI\u0118CIA: IDEALNE vs RZECZYWISTE  (pyt. 1\u20133)')]
    st += [Spacer(1, 2)]

    rows = [
        ['', 'Źródło idealne', 'Źródło rzeczywiste'],
        ['Rezystancja wewn. <i>R</i><sub>w</sub>', '= 0', '&gt; 0 (od ułamka mΩ do kilku kΩ)'],
        ['Napięcie zaciskowe', '<i>U</i> = <i>E</i> = const',
         '<i>U</i> = <i>E</i> − <i>I</i>·<i>R</i><sub>w</sub>'],
        ['Prąd zwarcia', 'teoretycznie ∞', '<i>I</i><sub>k</sub> = <i>E</i>/<i>R</i><sub>w</sub>'],
        ['Gdzie <i>R</i><sub>w</sub>', '—',
         'zasilacz: mΩ \u00b7 akumulator: kilka mΩ \u00b7 ogniwo AA: 0,1\u20131 Ω \u00b7 bateria zegarka: kΩ'],
    ]
    st.append(qtable(rows, [3.05 * cm, 3.55 * cm, 11.65 * cm], align=['l', 'c', 'l']))
    st.append(Spacer(1, 3))
    st += [P('<b>Model zastępczy:</b> źródło <i>E</i> + szeregowa rezystancja '
             '<i>R</i><sub>w</sub> między zaciskami <i>A</i>, <i>B</i> (tw. Thevenina dla każdego '
             'obwodu liniowego). <b>Uwaga:</b> każde realne źródło jest rzeczywiste; model '
             'idealny stosujemy tylko gdy <i>R</i><sub>w</sub> &lt;&lt; <i>R</i><sub>obc</sub>.')]
    st += [Eq(r'$U_{AB} = E - I\,R_w = E\,\dfrac{R_{obc}}{R_w + R_{obc}}$', size=8.6, space=1.2)]

    st += [Spacer(1, 4), SectionBar('II', 'WOLTOMIERZE I MIERNIKI  (pyt. 4\u20136)')]
    st += [Spacer(1, 2)]
    rows = [
        ['Typ woltomierza', '<i>R</i><sub>V</sub>'],
        ['Magnetoelektryczny (LM-3)', '<i>R</i><sub>V</sub> = κ·<i>U</i><sub>z</sub>, κ = 1 kΩ/V '
                                      '(np. 15 kΩ na 15 V)'],
        ['Cyfrowy ręczny / stołowy', '10 MΩ (U1252B, 34450A)'],
        ['Profesjonalny stacjonarny', 'do 10 GΩ'],
        ['Idealny', '∞'],
    ]
    st.append(qtable(rows, [5.6 * cm, 12.65 * cm], align=['l', 'l']))
    st.append(Spacer(1, 3))
    st += [P('<b>Włączanie:</b> amperomierz <b>szeregowo</b> (ma <i>R</i><sub>A</sub> → 0, nie zmienia '
             'prądu), woltomierz <b>równolegle</b> (ma <i>R</i><sub>V</sub> → ∞, nie pobiera prądu). '
             'Idealny: <i>R</i><sub>A</sub> = 0, <i>R</i><sub>V</sub> = ∞.')]
    st += bullets([
        'parametry woltomierza: <i>R</i><sub>V</sub>, zakres <i>U</i><sub>z</sub>, klasa '
        '<i>k</i><sub>l</sub> (analog) / δ<sub>g</sub><i>U</i> (cyfrowy), rozdzielczość, czułość κ',
        'amperomierz szeregowo wymaga przerwania obwodu; woltomierz szeregowo lub amperomierz '
        'równolegle = błąd gruby (zwarcie / brak wskazania)',
    ])

    st += [Spacer(1, 4), SectionBar('III', 'B\u0141\u0104D METODY  (pyt. 7\u20138)')]
    st += [Spacer(1, 2)]
    st += [P('<b>Błąd metody</b> = błąd <b>systematyczny</b> i <b>korygowalny</b>: przyrząd zmienia '
             'warunki pracy obwodu. Dla woltomierza na zaciskach źródła:')]
    st += [Eq(r'$I_V = \dfrac{E}{R_w + R_V}$', tag='(2-1)', size=8.6, space=1.2)]
    st += [Eq(r'$U_V = E\,\dfrac{R_V}{R_w + R_V} = \dfrac{E}{\dfrac{R_w}{R_V}+1}$', tag='(2-2)',
              size=8.6, space=1.2)]
    st += [Eq(r'$\Delta_m E = U_V - E = -E\,\dfrac{R_w}{R_w+R_V} = -\dfrac{E}{1+R_V/R_w}'
              r' \;\approx\; -U_V\,\dfrac{R_w}{R_V}$', tag='(2-3)/(2-4)', size=8.6, space=1.2)]
    st += [Eq(r'$E = U_V - \Delta_m E = U_V\left(1 + \dfrac{R_w}{R_V}\right)$', tag='(2-5)',
              size=8.6, space=1.2)]
    st += [P('Błąd jest <b>zawsze ujemny</b> (woltomierz wskazuje mniej niż SEM). Znika, gdy '
             '<i>R</i><sub>V</sub> &gt;&gt; <i>R</i><sub>w</sub>: dla <i>R</i><sub>V</sub> '
             '≥ 100·<i>R</i><sub>w</sub> błąd ≤ 1 %. Uśrednianie go nie usuwa \u2013 trzeba '
             'skorygować albo dobrać przyrząd.')]

    # --- ŚCIĄGA WZORÓW
    st += [Spacer(1, 4), SectionBar('III-b', 'ŚCIĄGA WZORÓW – WSZYSTKO, CO TRZEBA PAMIĘTAĆ')]
    st += [Spacer(1, 2)]
    rows = [
        ['Wielkość', 'Wzór', 'Uwaga'],
        ['Napięcie zaciskowe', '<i>U</i> = <i>E</i> − <i>I</i>·<i>R</i><sub>w</sub>',
         'spadek na rezystancji wewnętrznej'],
        ['Napięcie na woltomierzu', '<i>U</i><sub>V</sub> = <i>E</i>·<i>R</i><sub>V</sub>/(<i>R</i><sub>w</sub>+<i>R</i><sub>V</sub>)',
         'zawsze &lt; <i>E</i> dla <i>R</i><sub>w</sub> &gt; 0'],
        ['Błąd metody + korekcja',
         'Δ<sub>m</sub><i>E</i> = −<i>U</i><sub>V</sub>·<i>R</i><sub>w</sub>/<i>R</i><sub>V</sub>; '
         '<i>E</i> = <i>U</i><sub>V</sub>(1+<i>R</i><sub>w</sub>/<i>R</i><sub>V</sub>)',
         'ujemny, korygowalny'],
        ['Błąd graniczny (klasa)', 'Δ<sub>kl</sub><i>U</i> = <i>k</i><sub>l</sub>·<i>U</i><sub>z</sub>/100',
         'odniesiony do <b>zakresu</b>'],
        ['Niepewność – przyrząd', '<i>u</i>(<i>U</i>) = Δ<sub>kl</sub><i>U</i>/√3',
         'rozkład jednostajny'],
        ['Niepewność – wzorzec', '<i>u</i>(<i>R</i>) = Δ<sub>g</sub><i>R</i>/3',
         'rozkład normalny: dzielnik <b>3</b>'],
        ['Niepewność wzgl. (klasa)', '<i>u</i><sub>rel</sub> = (<i>k</i><sub>l</sub>/√3)·(<i>U</i><sub>z</sub>/<i>U</i>)',
         'min. = <i>k</i><sub>l</sub>/√3 przy <i>U</i> = <i>U</i><sub>z</sub>'],
        ['LM-3: rezystancja', '<i>R</i><sub>V</sub> = κ·<i>U</i><sub>z</sub>, κ = 1 kΩ/V',
         'zależy od zakresu – nie zmieniać!'],
        ['Metoda kompensacyjna', '<i>E</i> = <i>U</i><sub>wz</sub> przy <i>U</i><sub>W</sub> = 0',
         'prąd nie płynie → brak błędu metody'],
        ['Niepewność kompensacji', '<i>u</i>(<i>E</i>) = ⎷(Δ<sub>g</sub><i>U</i><sub>wz</sub>² + Δ<i>U</i>² + Δ<i>U</i><sub>min</sub>²)/3',
         '3 składniki'],
    ]
    st.append(qtable(rows, [3.55 * cm, 8.55 * cm, 6.15 * cm], align=['l', 'l', 'l']))
    return st


def page2():
    st = [MarkSection('IV\u2013V \u00b7 niepewno\u015b\u0107, wyznaczanie Rw')]
    st += [SectionBar('IV', 'NIEPEWNO\u015a\u0106 POMIARU  (pyt. 9\u201311)')]
    st += [Spacer(1, 2)]
    st += [P('<b>Klasa <i>k</i><sub>l</sub></b> woltomierza elektromechanicznego określa '
             '<b>błąd bezwzględny odniesiony do ZAKRESU</b> (a nie do wskazania):')]
    st += [Eq(r'$\Delta_{kl}U = \dfrac{k_l\,U_z}{100} \qquad u(U) = \dfrac{\Delta_{kl}U}{\sqrt{3}}'
              r' \qquad u_{rel}(U) = \dfrac{k_l\,U_z}{U\sqrt{3}}\,[\%]$',
              tag='(2-8)(2-9)(2-10)', size=8.6, space=1.4)]
    st += [Spacer(1, 2)]
    rows = [
        ['Wskazanie (zakres 15 V, klasa 0,5)', '1,5 V (10 %)', '7,5 V (50 %)', '15 V (100 %)'],
        ['Δ<sub>kl</sub><i>U</i>', '75 mV', '75 mV', '75 mV'],
        ['δ<i>U</i>', '5,00 %', '1,00 %', '0,50 %'],
        ['<i>u</i>(<i>U</i>)', '43,3 mV', '43,3 mV', '43,3 mV'],
        ['<i>u</i><sub>rel</sub>(<i>U</i>)', '2,89 %', '0,58 %', '0,29 %'],
    ]
    st.append(qtable(rows, [5.9 * cm, 3.3 * cm, 3.3 * cm, 3.3 * cm],
                     align=['l', 'c', 'c', 'c']))
    st += [Spacer(1, 3)]
    st += [Eq(r'$u_{rel,min}(U) = \dfrac{k_l}{\sqrt{3}}\,[\%] \;\;\Rightarrow\;\;'
              r' k_l = 0{,}5: \;\; u_{rel,min} \approx 0{,}289\,\%$', tag='(W-8)',
              size=8.6, space=1.2)]
    st += bullets([
        '<b>minimum przy wskazaniu = koniec zakresu</b>: dlatego zakres dobiera się tuż powyżej '
        'mierzonej wartości (wskazanie w górnej części skali)',
        'elementy wzorcowe (opornik dekadowy, rezystor o tolerancji) \u2013 rozkład normalny: '
        '<i>u</i>(<i>x</i>) = Δ<sub>g</sub><i>x</i>/3, czyli δ/3, a nie δ/√3  (2-11), (2-12)',
        'multimetry cyfrowe: δ<sub>g</sub><i>U</i> = <i>a</i>% + <i>b</i>%·<i>U</i><sub>z</sub>/<i>U</i> '
        '(tab. 2.1\u20132.2 instrukcji); 34450A ma <i>R</i><sub>V</sub> = 10 MΩ',
    ])

    st += [Spacer(1, 4), SectionBar('V', 'REZYSTANCJA WEWN\u0118TRZNA Z DW\u00d3CH WOLTOMIERZY  (pyt. 12)')]
    st += [Spacer(1, 2)]
    st += [P('Dwa woltomierze o <b>znacz\u0105co r\u00f3\u017cnych</b> <i>R</i><sub>V</sub> daj\u0105 '
             'uk\u0142ad dw\u00f3ch r\u00f3wna\u0144 (2-13), (2-14), a po rozwi\u0105zaniu:')]
    st += [Eq(r'$E = U_1U_2\,\dfrac{R_{V1}-R_{V2}}{R_{V1}U_2-R_{V2}U_1} \qquad'
              r' R_w = R_{V1}R_{V2}\,\dfrac{U_1-U_2}{R_{V1}U_2-R_{V2}U_1}$',
              tag='(2-15)(2-16)', size=8.6, space=1.4)]
    st += [P('<b>Warunki wiarygodno\u015bci:</b> wskazania r\u00f3\u017cni\u0105 si\u0119 znacz\u0105co '
             '(wi\u0119cej ni\u017c wynosz\u0105 niepewno\u015bci); du\u017ca r\u00f3\u017cnica '
             '<i>R</i><sub>V1</sub>/<i>R</i><sub>V2</sub>; znane <i>R</i><sub>V1</sub>, '
             '<i>R</i><sub>V2</sub>; sta\u0142e <i>E</i> i <i>R</i><sub>w</sub>; przy LM-3 '
             '<b>nie zmienia\u0107 zakresu</b> mi\u0119dzy pomiarami.')]
    st += [P('W \u0107wiczeniu: 34450A (10 M\u03a9) + LM-3 (κ·<i>U</i><sub>z</sub>), '
             'wspomagane aplikacj\u0105 Demo_02 \u2013 <i>metoda ekstrapolacji liniowej</i>: '
             '<i>U</i> = <i>E</i> − <i>E</i>·<i>R</i><sub>w</sub>/(<i>R</i><sub>V</sub>+<i>R</i><sub>w</sub>), '
             'wi\u0119c <i>U</i>(\u03b5 = 1/<i>R</i><sub>V</sub>) jest liniowa; wyraz wolny = <i>E</i>, '
             'nachylenie = <i>R</i><sub>w</sub>.')]

    st += [SectionBar('VI', 'METODA KOMPENSACYJNA POMIARU SEM  (pyt. 13\u201315)')]
    st += [Spacer(1, 2)]
    st += [P('<b>Metoda zerowa:</b> SEM badanego \u017ar\u00f3d\u0142a r\u00f3wnowa\u017cy si\u0119 '
             'napi\u0119ciem regulowanego \u017ar\u00f3d\u0142a wzorcowego. W r\u00f3wnowadze '
             'przez wska\u017anik nie p\u0142ynie pr\u0105d, wi\u0119c na <i>R</i><sub>w</sub> '
             'nie ma spadku napi\u0119cia:')]
    st += [Eq(r'$E = U_{wz} \qquad U_W \approx 0$', tag='(W-10)', size=8.6, space=1.2)]
    rows = [
        ['', 'Metoda bezpo\u015brednia', 'Metoda kompensacyjna'],
        ['B\u0142\u0105d metody', 'jest (ujemny), zale\u017cy od <i>R</i><sub>w</sub>/<i>R</i><sub>V</sub>',
         '<b>brak</b> \u2013 w r\u00f3wnowadze pr\u0105d nie p\u0142ynie'],
        ['Wp\u0142yw <i>R</i><sub>w</sub> \u017ar\u00f3d\u0142a', 'wynik zale\u017cy od <i>R</i><sub>w</sub>',
         'wynik <b>nie zale\u017cy</b> od <i>R</i><sub>w</sub>'],
        ['Dok\u0142adno\u015b\u0107', 'klasa woltomierza i <i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>',
         'dok\u0142adno\u015b\u0107 <i>U</i><sub>wz</sub> + rozdzielczo\u015b\u0107 regulacji'],
        ['Z\u0142o\u017cono\u015b\u0107 / czas', 'prosta, szybka, 1 przyrz\u0105d',
         'z\u0142o\u017cona, wolna, wra\u017cliwa na warunki'],
        ['Kiedy stosowa\u0107', 'zwyk\u0142e pomiary, <i>R</i><sub>w</sub> ma\u0142e',
         'du\u017ce <i>R</i><sub>w</sub>, wymagana du\u017ca dok\u0142adno\u015b\u0107 SEM'],
    ]
    st.append(Spacer(1, 2))
    st.append(qtable(rows, [3.55 * cm, 6.9 * cm, 6.9 * cm], align=['l', 'l', 'l']))

    # --- rząd wielkości Rw w praktyce
    st += [Spacer(1, 4), SectionBar('V-b', 'RZĄD WIELKOŚCI <i>R</i><sub>w</sub> – CO Z TEGO WYNIKA')]
    st += [Spacer(1, 2)]
    rows = [
        ['Źródło', '<i>R</i><sub>w</sub>', 'Co to oznacza dla pomiaru'],
        ['Zasilacz stabilizowany / E3646A', 'ułamek mΩ – kilka mΩ',
         'zachowuje się jak źródło idealne; woltomierz 10 MΩ w pełni wystarcza'],
        ['Akumulator', 'kilka mΩ', 'mały spadek napięcia nawet przy dużych prądach'],
        ['Ogniwo AA / Li-Ion', '0,1–1 Ω / kilkadziesiąt mΩ',
         'rośnie przy rozładowaniu i w niskiej temperaturze'],
        ['Bateria zegarka, ogniwa małe', 'kilka Ω – kilka kΩ',
         'woltomierz 10 MΩ OK; LM-3 (15 kΩ) daje już wyraźny błąd'],
        ['Czujnik / dzielnik / obwód o dużej impedancji', 'kΩ – MΩ',
         '<b>tylko metoda kompensacyjna</b> lub woltomierz o <i>R</i><sub>V</sub> <font name="Sans">≫</font> <i>R</i><sub>w</sub>'],
    ]
    st.append(qtable(rows, [5.75 * cm, 3.45 * cm, 9.05 * cm], align=['l', 'c', 'l']))
    st += [Spacer(1, 3)]
    st += [P('<b>Reguła decyzyjna:</b> policz stosunek <i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>. '
             'Jeśli ≥ 100 → metoda bezpośrednia (błąd ≤ 1 %, '
             'do pominięcia). Jeśli mniejszy → albo koryguj wzorem (2-5), albo '
             'przejdź na <b>metodę kompensacyjną</b>.')]
    return st


def page3():
    st = [MarkSection('VII\u2013VIII \u00b7 wp\u0142yw RV, zadania')]
    st += [Spacer(1, 1), SectionBar('VII', 'WP\u0141YW <i>R</i><sub>V</sub> NA WYNIK  (pyt. 16\u201318)')]
    st += [Spacer(1, 2)]
    st += [P('<b>Źródło idealne</b> (<i>R</i><sub>w</sub> = 0): <i>U</i><sub>V</sub> = <i>E</i> '
             'niezale\u017cnie od <i>R</i><sub>V</sub> \u2013 woltomierz zawsze wska\u017ce SEM. '
             '<b>Źródło rzeczywiste</b>: <i>U</i><sub>V</sub> ro\u015bnie z '
             '<i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>; dla <i>R</i><sub>V</sub> = '
             '<i>R</i><sub>w</sub> wska\u017ce tylko 50 % SEM.')]
    rows = [
        ['<i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>', '0,01', '0,1', '1', '10', '100', '1000'],
        ['<i>U</i><sub>V</sub>/<i>E</i>', '1,0 %', '9,1 %', '50,0 %', '90,9 %', '99,0 %', '99,9 %'],
        ['Δ<sub>m</sub><i>E</i>/<i>E</i>', '−99,0 %', '−90,9 %', '−50,0 %', '−9,1 %', '−1,0 %', '−0,1 %'],
    ]
    st.append(qtable(rows, [3.5 * cm, 2.28 * cm, 2.28 * cm, 2.28 * cm, 2.28 * cm,
                            2.28 * cm, 2.28 * cm], align=['l', 'c', 'c', 'c', 'c', 'c', 'c']))
    st += [Spacer(1, 2)]
    st += [P('<b>Wniosek:</b> do pomiaru SEM \u017ar\u00f3d\u0142a rzeczywistego potrzeba '
             '<i>R</i><sub>V</sub> &gt;&gt; <i>R</i><sub>w</sub>; inaczej korygowa\u0107 '
             '(2-5) lub u\u017cy\u0107 metody kompensacyjnej. Analogicznie amperomierz: '
             '<i>R</i><sub>A</sub> &lt;&lt; <i>R</i><sub>obc</sub>.')]

    st += [Spacer(1, 2)]
    from reportlab.platypus import Image as RLImage
    from PIL import Image as PILImage

    def imgf(name, w_cm):
        pth = os.path.join(FIG, name)
        im = PILImage.open(pth)
        w = w_cm * cm
        h = w * im.size[1] / float(im.size[0])
        i = RLImage(pth, width=w, height=h)
        i.hAlign = 'LEFT'
        return i

    i1 = imgf('fig06_kompensacja.png', 8.7)
    i2 = imgf('fig07_wplyw_rv.png', 8.4)
    t = Table([[i1, i2]], colWidths=[9.1 * cm, 8.9 * cm])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    st.append(t)
    st.append(Paragraph(
        'Schemat kompensacyjny: <b>W</b> \u2013 wska\u017anik r\u00f3wnowagi (du\u017ca '
        'czu\u0142o\u015b\u0107), <b>V</b> \u2013 woltomierz napi\u0119cia wzorcowego '
        '(du\u017ca dok\u0142adno\u015b\u0107). Obok: wynik <i>U</i><sub>V</sub>/<i>E</i> '
        'w funkcji <i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>.', ST['cap']))
    st += [Eq(r'$u(E) = \sqrt{\dfrac{\Delta_g U_{wz}^2 + \Delta U^2 + \Delta U_{min}^2}{3}}'
              r' \qquad u_{rel}(E) = \dfrac{u(E)}{U_{wz}}\cdot 100\%$',
              tag='(2-17)(2-18)', size=8.6, space=1.4)]
    st += [P('Δ<i>U</i> = 10 mV (zasilacz E3646A); Δ<i>U</i><sub>min</sub> = napi\u0119cie cyfry '
             '\u201e1\u201d na najmniej znacz\u0105cym miejscu wska\u017anika r\u00f3wnowagi. '
             '<b>Decyduje dok\u0142adno\u015b\u0107 <i>U</i><sub>wz</sub></b> \u2013 to on '
             'wyznacza dok\u0142adno\u015b\u0107 ca\u0142ej metody.')]

    st += [Spacer(1, 4), SectionBar('VIII', 'ZADANIA RACHUNKOWE \u2013 KOMPLET OBLICZE\u0143')]
    st += [Spacer(1, 2)]

    def block(num, title, lines, results):
        out = []
        out.append(Paragraph(
            f'<font color="#ffffff" backColor="#12335c"> <b>{num}</b> </font> <b>{title}</b>',
            ParagraphStyle('bh', fontName='Sans', fontSize=8.0, leading=10.2,
                           textColor=colors.HexColor('#12335c'), spaceBefore=3,
                           spaceAfter=1)))
        out += lines
        for r in results:
            out.append(r)
        return out

    # --- 17
    st += [Paragraph('<font color="#ffffff" backColor="#12335c"> <b>17</b> </font> '
                     '<b>Woltomierz 10 kΩ na źródle z <i>E</i> = 10 V i <i>R</i><sub>w</sub> = 10 kΩ</b>',
                     ParagraphStyle('bh', fontName='Sans', fontSize=8.0, leading=10.2,
                                    textColor=NAVY, spaceBefore=3, spaceAfter=1))]
    st += [Eq(r'$U_V = E\,\dfrac{R_V}{R_w+R_V} = 10\cdot\dfrac{10}{10+10} = \mathbf{5{,}00\ V}'
              r' \qquad \Delta_m E = -5{,}00\ \mathrm{V}\ (50\%)'
              r' \qquad E = U_V\left(1+\dfrac{R_w}{R_V}\right) = 10{,}0\ \mathrm{V}$',
              size=8.4, space=1.2)]

    # --- 19
    st += [Paragraph('<font color="#ffffff" backColor="#12335c"> <b>19</b> </font> '
                     '<b><i>E</i> = 5 V, <i>U</i> = 2,500 V, <i>R</i><sub>V</sub> = 100 kΩ → <i>R</i><sub>w</sub>?</b>',
                     ParagraphStyle('bh2', fontName='Sans', fontSize=8.0, leading=10.2,
                                    textColor=NAVY, spaceBefore=3, spaceAfter=1))]
    st += [Eq(r'$\dfrac{E-U}{R_w} = \dfrac{U}{R_V} \;\;\Rightarrow\;\; '
              r'R_w = R_V\dfrac{E-U}{U} = R_V\left(\dfrac{E}{U}-1\right) = 100\,\mathrm{k}\Omega'
              r'\cdot\dfrac{5-2{,}5}{2{,}5} = \mathbf{100\ k\Omega}$', size=8.4, space=1.2)]
    st += [P('Spr.: <i>I</i><sub>V</sub> = 25 µA → 25 µA·100 kΩ = 2,500 V; '
             '2,500 + 2,500 = 5,000 V ✓')]

    # --- 20
    st += [Paragraph('<font color="#ffffff" backColor="#12335c"> <b>20</b> </font> '
                     '<b><i>I</i> = 10,000 mA, <i>I</i><sub>z</sub> = 50 mA, '
                     'δ<sub>g</sub> = 0,05 % + 0,02 %·<i>I</i><sub>z</sub>/<i>I</i></b>',
                     ParagraphStyle('bh3', fontName='Sans', fontSize=8.0, leading=10.2,
                                    textColor=NAVY, spaceBefore=3, spaceAfter=1))]
    st += [Eq(r'$\delta_{gI} = 0{,}05\% + 0{,}02\%\cdot\dfrac{50}{10} = 0{,}05 + 0{,}10 = 0{,}15\%'
              r' \qquad u_{rel}(I) = \dfrac{0{,}15\%}{\sqrt{3}} \approx \mathbf{0{,}087\%}$',
              size=8.4, space=1.2)]
    st += [P('<i>u</i>(<i>I</i>) ≈ 0,0087 mA → <i>I</i> = (10,000 ± 0,009) mA. Sk\u0142adnik '
             'zakresowy (0,10 %) > sta\u0142y (0,05 %).')]

    # --- 21
    st += [Paragraph('<font color="#ffffff" backColor="#12335c"> <b>21</b> </font> '
                     '<b><i>R</i> = 10 kΩ (0,1 %), <i>U</i> = 10,000 V, <i>U</i><sub>z</sub> = 20 V, '
                     'δ<sub>g</sub> = 0,05 % + 0,01 %·<i>U</i><sub>z</sub>/<i>U</i></b>',
                     ParagraphStyle('bh4', fontName='Sans', fontSize=8.0, leading=10.2,
                                    textColor=NAVY, spaceBefore=3, spaceAfter=1))]
    st += [Eq(r'$I = \dfrac{U}{R} = \dfrac{10{,}000}{10\,\mathrm{k}\Omega} = \mathbf{1{,}0000\ mA}'
              r' \qquad \delta_{gU} = 0{,}05 + 0{,}01\cdot\dfrac{20}{10} = 0{,}07\%$',
              size=8.4, space=1.2)]
    st += [Eq(r'$u_{rel}(U) = \dfrac{0{,}07\%}{\sqrt{3}} \approx 0{,}0404\%,\;\;'
              r'u_{rel}(R) = \dfrac{0{,}1\%}{3} = 0{,}0333\%$', size=8.4, space=1.2)]
    st += [Eq(r'$u_{rel}(I) = \sqrt{0{,}0404^2 + 0{,}0333^2} \approx \mathbf{0{,}052\%}'
              r' \;\Rightarrow\; u(I) \approx 0{,}00052\ \mathrm{mA} = 0{,}52\ \mu\mathrm{A}$',
              size=8.4, space=1.2)]

    # --- 22
    st += [Paragraph('<font color="#ffffff" backColor="#12335c"> <b>22</b> </font> '
                     '<b><i>U</i> = 10,000 V, <i>U</i><sub>z</sub> = 30 V, '
                     'δ<sub>g</sub> = 0,01 % + 0,01 %·<i>U</i><sub>z</sub>/<i>U</i>, '
                     'Δ<i>U</i> = 0,1 mV, Δ<i>U</i><sub>min</sub> = 0,01 mV</b>',
                     ParagraphStyle('bh5', fontName='Sans', fontSize=8.0, leading=10.2,
                                    textColor=NAVY, spaceBefore=3, spaceAfter=1))]
    st += [Eq(r'$\delta_{gU_{wz}} = 0{,}01 + 0{,}01\cdot\dfrac{30}{10} = 0{,}04\%'
              r' \;\Rightarrow\; \Delta_g U_{wz} = 4\ \mathrm{mV}$', size=8.4, space=1.2)]
    st += [Eq(r'$u(E) = \dfrac{1}{\sqrt{3}}\sqrt{4^2 + 0{,}1^2 + 0{,}01^2}\ \mathrm{mV}'
              r' = \sqrt{16{,}0101/3}\ \mathrm{mV} \approx \mathbf{2{,}31\ mV}'
              r' \;\; (0{,}023\%)$', size=8.4, space=1.2)]
    st += [P('Decyduje sk\u0142adnik <i>U</i><sub>wz</sub>; rozdzielczo\u015b\u0107 i '
             'nieczu\u0142o\u015b\u0107 wska\u017anika s\u0105 >20× mniejsze.')]

    st += [Spacer(1, 5), SectionBar('IX', 'TABELA WYNIK\u00d3W \u2013 SZYBKA POWT\u00d3RKA')]
    st += [Spacer(1, 2)]
    rows = [
        ['Pyt.', 'Szukane', 'Wz\u00f3r', 'Wynik'],
        ['17', '<i>U</i><sub>V</sub>', '<i>E</i>·<i>R</i><sub>V</sub>/(<i>R</i><sub>w</sub>+<i>R</i><sub>V</sub>)', '5,00 V'],
        ['19', '<i>R</i><sub>w</sub>', '<i>R</i><sub>V</sub>(<i>E</i>/<i>U</i> − 1)', '100 kΩ'],
        ['20', '<i>u</i><sub>rel</sub>(<i>I</i>)', 'δ<sub>g</sub>/<font name="Sans">√</font>3', '0,087 %'],
        ['21', '<i>I</i>', '<i>U</i>/<i>R</i>', '1,0000 mA'],
        ['21', '<i>u</i><sub>rel</sub>(<i>I</i>)', '<font name="Sans">√</font>(<i>u</i><sub>U</sub>²+<i>u</i><sub>R</sub>²)', '0,052 %'],
        ['22', '<i>u</i>(<i>E</i>)', 'wz\u00f3r (2-17)', '2,31 mV'],
    ]
    st.append(qtable(rows, [1.15 * cm, 2.30 * cm, 8.55 * cm, 6.75 * cm],
                     align=['c', 'c', 'l', 'c']))

    return st


def page4():
    """Strona 4: szybka autoweryfikacja + fiszki + pułapki."""
    st = [MarkSection('IX\u2013X \u00b7 autotest, fiszki, pu\u0142apki')]

    st += [SectionBar('X', 'AUTOTEST – 10 PYTA\u0143 W MINUT\u0118')]
    st += [Spacer(1, 2)]
    st += [P('Zakryj prawą kolumnę i odpowiedz. Jeśli nie wiesz – wróć do '
              'odpowiedniej części ściągi.')]
    quiz = [
        ['#', 'Pytanie', 'Odpowiedź'],
        ['1', 'Różnica między źródłem idealnym a rzeczywistym?',
         '<i>R</i><sub>w</sub> = 0 vs <i>R</i><sub>w</sub> &gt; 0; <i>U</i> = <i>E</i> vs '
         '<i>U</i> = <i>E</i> − <i>I</i><i>R</i><sub>w</sub>'],
        ['2', 'Jak włącza się amperomierz, a jak woltomierz?',
         'A – <b>szeregowo</b> (<i>R</i><sub>A</sub>→0); V – <b>równolegle</b> '
         '(<i>R</i><sub>V</sub>→∞)'],
        ['3', 'Do czego odnosi się klasa przyrządu?',
         'Do <b>zakresu</b>: Δ<sub>kl</sub><i>U</i> = <i>k</i><sub>l</sub><i>U</i><sub>z</sub>/100'],
        ['4', 'Dzielnik przy niepewności: przyrząd vs wzorzec?',
         'przyrząd <b>√3</b> (jednostajny), wzorzec <b>3</b> (normalny)'],
        ['5', 'Znak błędu metody przy pomiarze SEM woltomierzem?',
         '<b>ujemny</b> – wskazanie zawsze mniejsze od <i>E</i>'],
        ['6', 'Kiedy stosować metodę kompensacyjną?',
         'duże <i>R</i><sub>w</sub> źródła, wymagana duża dokładność SEM'],
        ['7', 'Jak zmierzyć <i>R</i><sub>w</sub> dwoma woltomierzami?',
         'dwa pomiary, różne <i>R</i><sub>V</sub> → wzory (2-15), (2-16); wskazania '
         'muszą różnić się znacząco'],
        ['8', 'Od czego zależy <i>R</i><sub>V</sub> woltomierza LM-3?',
         'od zakresu: <i>R</i><sub>V</sub> = κ<i>U</i><sub>z</sub>, κ = 1 kΩ/V '
         '– <b>nie zmieniać zakresu</b>'],
        ['9', 'Wzór na niepewność metody kompensacyjnej?',
         '(2-17): trzy składniki – Δ<sub>g</sub><i>U</i><sub>wz</sub>, Δ<i>U</i>, '
         'Δ<i>U</i><sub>min</sub>, każdy dzielony przez √3'],
        ['10', 'Co decyduje o dokładności metody kompensacyjnej?',
         'dokładność pomiaru napięcia <b>wzorcowego</b> <i>U</i><sub>wz</sub>'],
    ]
    st.append(qtable(quiz, [0.75 * cm, 7.15 * cm, 10.35 * cm], align=['c', 'l', 'l']))

    # --- fiszki / liczby do zapamiętania
    st += [Spacer(1, 5), SectionBar('XI', 'LICZBY, KTÓRE MUSISZ ZNAĆ NA PAMIĘĆ')]
    st += [Spacer(1, 2)]
    nums = [
        ['Wielkość', 'Wartość', 'Skąd'],
        ['<i>R</i><sub>V</sub> multimetru 34450A', '10 MΩ', 'instrukcja, Zadanie 2'],
        ['κ woltomierza LM-3', '1 kΩ/V', 'instrukcja, Zadanie 2'],
        ['Klasa LM-3 w ćwiczeniu', '0,5', 'Zadanie 2'],
        ['Δ<i>U</i> zasilacza E3646A', '10 mV', 'wzór (2-17)'],
        ['Zakresy LM-3', '1,5; 3; 7,5; 15; 30; 75; 150 V', 'Zadanie domowe 1'],
        ['Zakresy 34450A', '100 mV; 1; 10; 100; 1000 V', 'Zadanie domowe 2'],
        ['Ograniczenie prądowe w kompensacji', '<i>I</i><sub>ogr</sub> = 100 mA', 'Zadanie 3'],
        ['<i>u</i><sub>rel,min</sub> dla klasy 0,5', '0,289 %', '<i>k</i><sub>l</sub>/√3'],
        ['Błąd metody dla <i>R</i><sub>V</sub>=<i>R</i><sub>w</sub>', '−50 % '
         '(<i>U</i><sub>V</sub> = 0,5<i>E</i>)', 'wzór (2-2)'],
        ['Błąd pomijalny, gdy', '<i>R</i><sub>V</sub> ≥ 100<i>R</i><sub>w</sub> '
         '(≤1 %)', 'wzór (2-3)'],
    ]
    st.append(qtable(nums, [6.55 * cm, 5.55 * cm, 6.15 * cm], align=['l', 'c', 'l']))

    # --- pułapki
    st += [Spacer(1, 5), SectionBar('XII', 'NAJCZĘSTSZE PUŁAPKI NA ZALICZENIU')]
    st += [Spacer(1, 2)]
    box = Table([[Paragraph(
        '<b>Najcz\u0119stsze pu\u0142apki na zaliczeniu</b><br/>'
        '\u2022 b\u0142\u0105d metody jest <b>systematyczny</b> \u2013 nie maleje od '
        'u\u015bredniania, trzeba go <b>skorygowa\u0107</b>;<br/>'
        '\u2022 klasa przyrz\u0105du odnosi si\u0119 do <b>zakresu</b>, nie do wskazania '
        '(\u2013 dlatego niepewno\u015b\u0107 wzgl\u0119dna ro\u015bnie przy ma\u0142ych '
        'wskazaniach);<br/>'
        '\u2022 elementy wzorcowe: dzielnik <b>3</b>, przyrz\u0105dy pomiarowe: dzielnik '
        '<b>\u221a3</b>;<br/>'
        '\u2022 woltomierz <b>r\u00f3wnolegle</b>, amperomierz <b>szeregowo</b> \u2013 '
        'odwrotnie = zwarcie / brak wskazania;<br/>'
        '\u2022 metoda kompensacyjna mierzy <b>SEM</b>, metoda bezpo\u015brednia \u2013 '
        '<b>napi\u0119cie zaciskowe</b> (mniejsze o <i>I</i>·<i>R</i><sub>w</sub>);<br/>'
        '\u2022 niepewno\u015b\u0107 <i>u</i>(<i>x</i>) to <b>k</b> = 1; dla <b>k</b> = 2 '
        'mno\u017cysz przez 2.',
        ParagraphStyle('pk', fontName='Serif', fontSize=7.9, leading=10.6,
                       textColor=colors.HexColor('#1d2b3a'), alignment=TA_LEFT))]],
        colWidths=[CW])
    box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fdf3e3')),
        ('LINEBEFORE', (0, 0), (0, -1), 2.2, colors.HexColor('#c9761b')),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    st.append(box)
    return st


# =================================================================== BUDOWA
def build():
    story = []
    story += banner()
    story += page1()
    story.append(PageBreak())
    story += page2()
    story.append(PageBreak())
    story += page3()
    story.append(PageBreak())
    story += page4()

    class SheetDoc(BaseDocTemplate):
        def __init__(self, filename, **kw):
            super().__init__(filename, pagesize=A4,
                             leftMargin=LM, rightMargin=RM,
                             topMargin=TM, bottomMargin=BM,
                             title='Ćwiczenie T2 – ściąga (wersja skrócona)',
                             author='Laboratorium Podstaw Pomiarów',
                             subject='Pomiary napięć i prądów stałych – powtórka',
                             **kw)
            f = Frame(LM, BM, CW, PAGE_H - TM - BM, id='m',
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
            self.addPageTemplates([PageTemplate(id='m', frames=[f])])

    d = SheetDoc(OUT)
    d.build(story, canvasmaker=SheetCanvas2)
    return OUT


if __name__ == '__main__':
    p = build()
    print('OK:', p, os.path.getsize(p), 'B')
