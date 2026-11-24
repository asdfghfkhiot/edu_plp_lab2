"""Zeszyt ćwiczeń T2 — protokół laboratoryjny, wyprowadzenia i zadania domowe.

Buduje Cwiczenie_T2_-_zeszyt_cwiczen.pdf
"""
import os
import sys

from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle, KeepTogether,
                                PageBreak, Flowable, NextPageTemplate)
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pdfkit as K
from pdfkit import (S, Eq, Badge, PartHeading, note_box, data_table, CONTENT_W,
                    NAVY, ACCENT, GREY, RULE, LIGHT, LIGHT2, PAGE_W, PAGE_H,
                    LM, RM, build_with, NumberedCanvas, Doc, build)

OUT = 'Cwiczenie_T2_-_zeszyt_cwiczen.pdf'
ROW_H = 0.86 * cm


# --------------------------------------------------------------- style własne
S['h2'] = ParagraphStyle('h2', fontName='Sans-Bold', fontSize=12.0, leading=15.5,
                         textColor=NAVY, spaceBefore=10, spaceAfter=4.5,
                         hyphenationLang='pl_PL')
S['h3'] = ParagraphStyle('h3', fontName='Sans-Bold', fontSize=9.6, leading=13,
                         textColor=NAVY, spaceBefore=7, spaceAfter=3)
S['wzor'] = ParagraphStyle('wzor', fontName='Serif', fontSize=9.0, leading=13.0,
                           alignment=TA_CENTER, textColor=colors.HexColor('#1d2b3a'),
                           spaceBefore=2, spaceAfter=2)
S['fill'] = ParagraphStyle('fill', fontName='Sans', fontSize=7.4, leading=10,
                           textColor=GREY, alignment=TA_CENTER)
S['cell_s'] = ParagraphStyle('cell_s', fontName='Serif', fontSize=7.9, leading=10.6,
                             alignment=TA_CENTER)


# --------------------------------------------------------------- pomocnicze


def blank_table(header, widths, nrows, row_h=ROW_H, footer=False):
    """Tabela protokołu z pustymi wierszami do wpisania odręcznego.

    Wysokość wiersza wymuszamy przez leading pustego akapitu — atrybut
    ROWHEIGHTS jest nadpisywany przez Table._calc podczas łamania.
    """
    lead = row_h / 1.0 - 7.2          # 3,6 pt paddingu góra + dół
    blank = ParagraphStyle('blank', fontName='Serif', fontSize=8.0,
                           leading=max(lead, 10.0), alignment=TA_CENTER)
    rows = [[Paragraph('&nbsp;', blank) for _ in header] for _ in range(nrows)]
    t = data_table([header] + rows, widths, header=True, zebra=False)
    t.setStyle(TableStyle([
        ('LINEBELOW', (0, 1), (-1, -1), 0.55, colors.HexColor('#9fb2c9')),
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
    ]))
    return t


def wypelnij(*txt):
    return Paragraph(' '.join(txt), S['fill'])


def sekcja(num, tytul, podtytul):
    return PartHeading(num, tytul, podtytul)


def lh(txt, size=7.4, color=GREY):
    """Mała etykieta pomocnicza pod tabelą."""
    return Paragraph(txt, ParagraphStyle('lh', fontName='Sans', fontSize=size,
                                         leading=size * 1.45, textColor=color,
                                         spaceBefore=2.5, spaceAfter=6))


class Ruler(Flowable):
    """Linia punktowana do wpisania odpowiedzi (miejsce na odręczne notatki)."""

    def __init__(self, n=1, w=None, h=0.72 * cm):
        super().__init__()
        self.n = n
        self.w = w
        self.height = h * n
        self.width = w or CONTENT_W

    def wrap(self, aw, ah):
        self.width = self.w or aw
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(colors.HexColor('#a8b8cb'))
        c.setDash(1.6, 2.6)
        c.setLineWidth(0.5)
        step = self.height / self.n
        for i in range(self.n):
            y = self.height - (i + 1) * step + 0.16 * cm
            c.line(0, y, self.width, y)
        c.restoreState()


# =========================================================== STRONA 1
def page_tytul():
    st = []
    p = Paragraph('ZESZYT ĆWICZEŃ', ParagraphStyle(
        'z1', fontName='Sans-Bold', fontSize=9.4, leading=12, textColor=ACCENT,
        spaceAfter=3))
    st.append(p)
    st.append(Paragraph('Pomiary napięć i prądów stałych', ParagraphStyle(
        'z2', fontName='Sans-Bold', fontSize=20, leading=24, textColor=NAVY,
        spaceAfter=4)))
    st.append(Paragraph('Ćwiczenie T2 · protokół laboratoryjny, wyprowadzenia i zadania domowe',
                        ParagraphStyle('z3', fontName='Sans', fontSize=10.2, leading=14,
                                       textColor=GREY, spaceAfter=12)))
    st.append(Table([['']], colWidths=[CONTENT_W], rowHeights=[0.12 * cm],
                    style=TableStyle([('BACKGROUND', (0, 0), (-1, -1), ACCENT)])))
    st.append(Spacer(1, 14))

    st.append(Paragraph('Dane identyfikacyjne', S['h2']))
    dane = [
        ['Numer albumu', '', 'Data wykonania', ''],
        ['Imię i nazwisko', '', 'Grupa / zespół', ''],
        ['Prowadzący', '', 'Ocena', ''],
    ]
    t = Table([[Paragraph(c, S['cell']) if j % 2 == 0 and i >= 0 else Paragraph(c, S['cell_s'])
                for j, c in enumerate(r)] for i, r in enumerate(dane)],
              colWidths=[3.25 * cm, 5.35 * cm, 3.55 * cm, 5.05 * cm],
              rowHeights=[0.95 * cm] * 3)
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#c3cedc')),
        ('BACKGROUND', (0, 0), (0, -1), LIGHT),
        ('BACKGROUND', (2, 0), (2, -1), LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    st.append(t)
    st.append(Spacer(1, 12))

    st.append(Paragraph('Struktura zeszytu', S['h2']))
    st.append(Paragraph(
        'Zeszyt prowadzi przez trzy zadania laboratoryjne w kolejności arkusza zadań. '
        'Każde zadanie ma <b>gotowy protokół</b> (tabele do wypełnienia odręcznego na '
        'zajęciach, z góry rozplanowanymi kolumnami obliczeniowymi), <b>wskazówkę '
        'obliczeniową</b> z podstawionym przykładem oraz <b>komentarz</b> — co odróżnia '
        'wynik poprawny od wyniku tylko sformatowanego ładnie. Na końcu: pełne '
        'wyprowadzenie wzorów (2-15) i (2-16), analiza niepewności metody dwóch '
        'woltomierzy (której instrukcja nie podaje) i dwa zadania domowe z rozwiązaniem '
        'wzorcowym.', S['body']))
    st.append(Spacer(1, 6))

    rows = [
        ['1', 'Pomiar U i I metodą bezpośrednią i pośrednią', '25 %',
         's. 2–3', 'Rys. 2.8, wzór I<sub>obl</sub> = U/R<sub>d</sub>'],
        ['2', 'Napięcie na źródle rzeczywistym, R<sub>w</sub> źródła', '50 %',
         's. 4–7', 'wzory (2-1)…(2-5), (2-13)…(2-16)'],
        ['3', 'Pomiar SEM metodą kompensacyjną', '25 %',
         's. 8–9', 'wzory (2-17), (2-18)'],
        ['A', 'Wyprowadzenie (2-15) i (2-16)', '—', 's. 10–11', 'rachunek symboliczny'],
        ['B', 'Niepewność metody dwóch woltomierzy', '—', 's. 12', 'propagacja, budżet'],
        ['C', 'Zadania domowe 1 i 2', '—', 's. 13–15', 'rozwiązania wzorcowe'],
    ]
    st.append(data_table([['#', 'Część', 'Waga', 'Strona', 'Wykorzystane wzory']] + rows,
                         [0.95 * cm, 6.55 * cm, 1.55 * cm, 1.85 * cm, 6.3 * cm],
                         header=True,
                         align=['c', 'l', 'c', 'c', 'l']))
    st.append(Spacer(1, 12))

    st += note_box([Paragraph(
        '<b>Konwencja niepewności.</b> Zgodnie z instrukcją (rozdz. 4.1): '
        'dla przyrządów przyjmuje się rozkład jednostajny, więc <b>u = Δ<sub>g</sub>/√3</b>; '
        'dla elementów wzorcowych rozkład normalny i <b>u = Δ<sub>g</sub>/3</b>. '
        'Wszystkie niepewności w zeszycie podano dla <b>k = 1</b> (niepewność standardowa). '
        'Zapis wyniku: <b>x ± u(x)</b> z jednostką.', S['note'])], fill=LIGHT)
    return st


# =========================================================== ZADANIE 1
def zad1():
    st = []
    st.append(sekcja('1', 'POMIAR NAPIĘCIA I PRĄDU METODĄ BEZPOŚREDNIĄ I POŚREDNIĄ',
                     'Zadanie 1 · 25 % oceny · moduł U01, Rys. 2.8'))
    st.append(Paragraph(
        'Wyjście 1 zasilacza podłączamy do zacisków <b>WE</b> modułu U01. '
        'Napięcie U<sub>zas</sub>, ograniczenie prądowe I<sub>ogr</sub> oraz opornik dekadowy '
        'R<sub>d</sub> ustawiamy według wskazówek prowadzącego. Multimetr <b>34450A</b> mierzy '
        'napięcie, multimetr ręczny <b>U1252B</b> — prąd. Następnie obliczamy prąd ze wzoru '
        'I<sub>obl</sub> = U/R<sub>d</sub> i porównujemy oba wyniki za pomocą aplikacji '
        '<i>Porównywanie wyników</i>.', S['body']))

    st.append(Paragraph('Ustawienia układu', S['h2']))
    st.append(Paragraph(
        'Przepisz wartości narzucone przez prowadzącego — bez nich tabela poniżej nie ma '
        'sensu. Zanotuj także <b>zakresy</b> obu multimetrów: od nich zależy niepewność, '
        'a nie od samego wskazania.', S['body']))
    st.append(Spacer(1, 3))
    st.append(blank_table(
        ['U<sub>zas</sub> [V]', 'I<sub>ogr</sub> [mA]', 'R<sub>d</sub> [Ω]',
         'Zakres U (34450A)', 'Zakres I (U1252B)'],
        [3.55 * cm, 3.45 * cm, 3.55 * cm, 3.45 * cm, 3.4 * cm], 1))
    st.append(lh('U<sub>zas</sub> — napięcie wyjściowe zasilacza (Wyjście 1); I<sub>ogr</sub> — '
                 'ograniczenie prądowe; R<sub>d</sub> — rezystancja na oporniku dekadowym.'))

    st.append(Paragraph('Pomiary i obliczenia', S['h2']))
    st.append(Paragraph(
        'Wykonaj <b>pięć</b> pomiarów przy różnych R<sub>d</sub> (prowadzący poda kolejne '
        'wartości). Kolumny I<sub>obl</sub> oraz δ i u wypełniamy po zajęciach — resztę '
        'na miejscu, żeby móc od razu wychwycić błąd gruby.', S['body']))
    st.append(Spacer(1, 3))
    st.append(blank_table(
        ['Lp.', 'R<sub>d</sub> [Ω]', 'U [V]', 'I [mA]', 'I<sub>obl</sub> = U/R<sub>d</sub> [mA]',
         'δ<sub>g</sub>U [%]', 'δ<sub>g</sub>I [%]', 'u<sub>rel</sub>(U) [%]',
         'u<sub>rel</sub>(I) [%]', 'u<sub>rel</sub>(I<sub>obl</sub>) [%]'],
        [1.0 * cm, 1.95 * cm, 1.5 * cm, 1.5 * cm, 2.35 * cm, 1.65 * cm, 1.65 * cm,
         1.9 * cm, 1.9 * cm, 2.35 * cm], 5))
    st.append(lh('δ<sub>g</sub>U i δ<sub>g</sub>I odczytaj z tabeli 2.1 instrukcji dla użytych '
                 'zakresów. u<sub>rel</sub> = δ<sub>g</sub>/√3 <b>tylko</b> dla przyrządów '
                 'cyfrowych, gdy δ<sub>g</sub> jest stały w całym zakresie; dla 34450A i U1252B '
                 'składnik „b·U<sub>z</sub>/U” zależy od wskazania — licz go dla każdego wiersza osobno.'))

    st.append(Paragraph('Wskazówka obliczeniowa', S['h2']))
    st.append(Paragraph(
        'Dla multimetru cyfrowego błąd graniczny zapisujemy jako sumę dwóch składników: '
        'stałego (od wskazania) i zakresowego. Dla 34450A: δ<sub>g</sub>U = 0,015 % + 0,005 %·U<sub>z</sub>/U. '
        'Dla U1252B prąd: δ<sub>g</sub>I = 0,05 % + 5/(n·100 %) — drugi składnik liczysz jako '
        '5 jednostek ostatniej cyfry odniesionych do wskazania.', S['body']))
    st.append(Spacer(1, 2))

    st.append(Paragraph('Przykład rachunkowy', S['h3']))
    st.append(Paragraph('Niech R<sub>d</sub> = 1,000 kΩ, U = 5,000 V, zakres U<sub>z</sub> = 10 V. '
                        'Wtedy:', S['body']))
    st.append(Eq(r'I_{obl} = \frac{U}{R_d} = \frac{5{,}000\ \mathrm{V}}{1{,}000\ \mathrm{k\Omega}}'
                 r' = 5{,}000\ \mathrm{mA}', tag='(1.1)'))
    st.append(Eq(r'\delta_g U = 0{,}015\,\% + 0{,}005\,\%\cdot\frac{10}{5{,}000}'
                 r' = 0{,}025\,\%', tag='(1.2)'))
    st.append(Eq(r'u_{rel}(U) = \frac{0{,}025\,\%}{\sqrt{3}} = 0{,}0144\,\%', tag='(1.3)'))
    st.append(Paragraph(
        'Niepewność I<sub>obl</sub> składamy z niepewności U i R<sub>d</sub> w postaci '
        'względnej (pierwiastek z sumy kwadratów), bo iloraz: '
        'u<sub>rel</sub>(I<sub>obl</sub>) = √(u<sub>rel</sub>(U)² + u<sub>rel</sub>(R<sub>d</sub>)²). '
        'Opornik dekadowy jest elementem wzorcowym — dla niego dzielimy przez 3, nie przez √3.',
        S['body']))
    st.append(Eq(r'u_{rel}(I_{obl}) = \sqrt{0{,}0144^2 + u_{rel}(R_d)^2}\ \%', tag='(1.4)'))

    st += note_box([Paragraph(
        '<b>Na co uważać.</b> Opornik dekadowy ma własną tolerancję (zwykle 0,1 % lub 0,05 %) — '
        'jeśli pominiesz ten składnik, niepewność I<sub>obl</sub> wyjdzie zaniżona, a wniosek '
        'z porównania „I vs I<sub>obl</sub>” fałszywy. Sprawdź na obudowie opornika klasę '
        'albo tolerancję i wpisz ją do tabeli.', S['note'])], fill=colors.HexColor('#fdf6ea'),
        bar=colors.HexColor('#c9761b'))

    st.append(Paragraph('Porównanie I i I<sub>obl</sub>', S['h2']))
    st.append(Paragraph(
        'Aplikacja <i>Porównywanie wyników</i> liczy wskaźnik zgodności — najczęściej '
        'w postaci |I − I<sub>obl</sub>|/√(u(I)² + u(I<sub>obl</sub>)²). Jeśli wynik jest '
        '<b>mniejszy od 2</b>, uznajemy oba wyniki za zgodne na poziomie ufności ≈ 95 %. '
        'Wklej wykres z aplikacji i skomentuj: czy różnica mieści się w niepewnościach, '
        'czy wskazuje na błąd systematyczny (np. pominiętą rezystancję amperomierza).',
        S['body']))
    st.append(Spacer(1, 4))
    st.append(Paragraph('Szkic / wklejony wykres z aplikacji', S['h3']))
    st.append(Ruler(5))
    st.append(Spacer(1, 4))
    st.append(Paragraph('Wniosek', S['h3']))
    st.append(Ruler(3))
    return st


# =========================================================== ZADANIE 2
def zad2():
    st = []
    st.append(sekcja('2', 'POMIAR NAPIĘCIA NA ŹRÓDLE RZECZYWISTYM',
                     'Zadanie 2 · 50 % oceny · wyznaczenie R<sub>w</sub>'))
    st.append(Paragraph(
        'Wyjście 1 zasilacza łączymy z zaciskami <b>Zas.</b> modułu U01, napięcie i ograniczenie '
        'prądowe bez zmian. Mierzymy napięcie na zaciskach trzech źródeł (Źr.1, Źr.2, Źr.3) '
        'dwoma woltomierzami: multimetrem <b>34450A</b> (R<sub>V</sub> = 10 MΩ) i woltomierzem '
        'magnetoelektrycznym <b>LM-3</b> klasy 0,5 (R<sub>V</sub> = ϰ·U<sub>z</sub>, ϰ = 1 kΩ/V).',
        S['body']))

    st += note_box([Paragraph(
        '<b>Warunek krytyczny (uwaga z arkusza).</b> W LM-3 dobierz zakres przy pomiarze '
        '<b>Źr.1</b> i przy kolejnych źródłach <b>go nie zmieniaj</b>. Zmiana zakresu zmienia '
        'R<sub>V</sub> = ϰ·U<sub>z</sub>, czyli warunki obciążenia źródła — a cała metoda opiera '
        'się na tym, że różnica wskazań wynika <i>wyłącznie</i> z różnych R<sub>V</sub>. '
        'Zmiana zakresu w trakcie serii unieważnia porównanie.', S['note'])],
        fill=colors.HexColor('#fdf6ea'), bar=colors.HexColor('#c9761b'))

    st.append(Paragraph('Dobór zakresu LM-3', S['h2']))
    st.append(Paragraph(
        'Zakresy LM-3: 1,5 · 3 · 7,5 · 15 · 30 · 75 · 150 V. Wybieramy <b>najmniejszy zakres '
        'większy od mierzonego napięcia</b> — ale to nie jedyne kryterium, bo R<sub>V</sub> rośnie '
        'z zakresem. Zapisz wybrany zakres i wynikające z niego R<sub>V</sub>:', S['body']))
    st.append(Spacer(1, 3))
    st.append(blank_table(['Wybrany zakres U<sub>z</sub> [V]', 'R<sub>V,LM3</sub> = ϰ·U<sub>z</sub> [kΩ]',
                           'R<sub>V,34450A</sub> [MΩ]', 'R<sub>V,LM3</sub>/R<sub>V,34450A</sub>'],
                          [5.0 * cm, 6.4 * cm, 4.1 * cm, 4.0 * cm], 1))
    st.append(lh('κ = 1 kΩ/V. Stosunek R<sub>V</sub> obu woltomierzy powinien być duży (rzędu 10³), '
                 'inaczej różnica wskazań jest mała i metoda (2-16) traci dokładność.'))

    st.append(Paragraph('Pomiary napięć na zaciskach źródeł', S['h2']))
    st.append(blank_table(
        ['Źródło', 'U<sub>34450A</sub> [V]', 'U<sub>LM-3</sub> [V]',
         'U<sub>34450A</sub> − U<sub>LM-3</sub> [mV]', 'δ<sub>g</sub>U<sub>34450A</sub> [%]',
         'δ<sub>g</sub>U<sub>LM-3</sub> [%]', 'R<sub>w</sub> (2-16) [Ω]'],
        [1.85 * cm, 2.55 * cm, 2.45 * cm, 3.15 * cm, 2.75 * cm, 2.65 * cm, 2.6 * cm], 3))
    st.append(lh('R<sub>w</sub> liczymy ze wzoru (2-16) dla pary (34450A, LM-3): '
                 'R<sub>w</sub> = R<sub>V1</sub>R<sub>V2</sub>(U₁−U₂)/(R<sub>V1</sub>U₂ − R<sub>V2</sub>U₁). '
                 'Kolejność jest istotna — indeks 1 to woltomierz o większym R<sub>V</sub> (34450A).'))

    st.append(Paragraph('Ocena jakościowa źródeł', S['h2']))
    st.append(Paragraph(
        'Im większa R<sub>w</sub>, tym mocniej woltomierz „ściąga” napięcie z zacisków, czyli tym '
        'większa różnica U<sub>34450A</sub> − U<sub>LM-3</sub>. <b>Największą R<sub>w</sub></b> ma '
        'źródło o największej różnicy wskazań, <b>najmniejszą</b> — o najmniejszej. Uzasadnij to '
        'wzorem (2-2): U<sub>V</sub> = E·R<sub>V</sub>/(R<sub>w</sub>+R<sub>V</sub>) — dla '
        'R<sub>w</sub> → 0 napięcie na zaciskach dąży do E niezależnie od R<sub>V</sub>.', S['body']))
    st.append(Spacer(1, 3))
    st.append(blank_table(['Źródło o najmniejszej R<sub>w</sub>', 'Źródło o największej R<sub>w</sub>',
                           'Uzasadnienie (wzór 2-2)'],
                          [4.6 * cm, 4.6 * cm, 8.3 * cm], 2))
    st.append(Paragraph('Wyznaczenie R<sub>w</sub> źródła Źr.2 i korekcja', S['h2']))
    st.append(Paragraph(
        'Dla Źr.2 liczymy R<sub>w</sub> z (2-16), a następnie <b>błąd metody</b> osobno dla obu '
        'woltomierzy i korygujemy wyniki wzorem (2-5):', S['body']))
    st.append(Eq(r'\Delta_m E = -E\,\frac{R_w}{R_w + R_V} = -U_V\,\frac{R_w}{R_V}'
                 r'\qquad\Longrightarrow\qquad E = U_V\left(1 + \frac{R_w}{R_V}\right)',
                 tag='(2.1)'))
    st.append(Spacer(1, 2))
    st.append(blank_table(
        ['Woltomierz', 'R<sub>V</sub> [Ω]', 'U<sub>V</sub> [V]', 'Δ<sub>m</sub>E [mV]',
         'Δ<sub>m</sub>E/E [%]', 'E po korekcji [V]', 'u<sub>rel</sub>(E) [%]', 'u(E) [mV]'],
        [2.55 * cm, 2.35 * cm, 2.3 * cm, 2.45 * cm, 2.4 * cm, 2.65 * cm, 2.45 * cm, 2.35 * cm], 2))
    st.append(lh('Po korekcji u<sub>rel</sub>(E) = u<sub>rel</sub>(U<sub>V</sub>) — tak każe '
                 'arkusz zadań. To założenie upraszczające: pomija niepewność samej R<sub>w</sub>, '
                 'która po korekcji wchodzi do wyniku.'))

    st.append(Paragraph('Dlaczego różnica wskazań jest tak duża?', S['h2']))
    st.append(Paragraph(
        'Prześledź liczby: dla U = 5 V, R<sub>w</sub> = 10 kΩ i woltomierza o R<sub>V</sub> = 15 kΩ '
        'otrzymujemy U<sub>V</sub> = 5·15/(10+15) = 3,00 V, czyli błąd metody −40 %. Ten sam '
        'pomiar multimetrem o R<sub>V</sub> = 10 MΩ daje 4,995 V (błąd −0,1 %). Wniosek: '
        'woltomierz elektromechaniczny <b>nie nadaje się</b> do pomiaru napięć na źródłach '
        'o R<sub>w</sub> rzędu kiloomów, dopóki nie zastosujemy korekcji.', S['body']))
    st.append(Spacer(1, 3))
    st.append(Paragraph('Porównanie skorygowanych wyników (wykres z aplikacji)', S['h3']))
    st.append(Ruler(4))
    st.append(Paragraph('Komentarz', S['h3']))
    st.append(Ruler(3))
    return st


# =========================================================== ZADANIE 3
def zad3():
    st = []
    st.append(sekcja('3', 'POMIAR SEM METODĄ KOMPENSACYJNĄ',
                     'Zadanie 3 · 25 % oceny · Źr.3, Wyjście 2 jako źródło wzorcowe'))
    st.append(Paragraph(
        'Mierzymy SEM źródła <b>Źr.3</b> metodą zerową: regulujemy napięcie wzorcowe U<sub>wz</sub> '
        'z Wyjścia 2 zasilacza tak długo, aż wskaźnik równowagi W wskaże zero. W równowadze '
        'przez źródło badane nie płynie prąd, więc na jego zaciskach panuje dokładnie E — '
        'spadek na R<sub>w</sub> znika. <b>Przed połączeniem układu</b> ustawiamy na Wyjściu 2 '
        'ograniczenie prądowe <b>I<sub>ogr</sub> = 100 mA</b>.', S['body']))

    st += note_box([Paragraph(
        '<b>Dlaczego I<sub>ogr</sub> = 100 mA before podłączeniem?</b> Wyjście 2 jest źródłem '
        'zasilacza, a nie ogniwem — przy niezerowym napięciu i małej rezystancji obwodu może '
        'popłynąć prąd znacznie przekraczający dopuszczalny dla źródła badanego. Ustawienie '
        'ograniczenia <i>przed</i> podłączeniem chroni zarówno Źr.3, jak i opornik regulacyjny.',
        S['note'])], fill=colors.HexColor('#fdf6ea'), bar=colors.HexColor('#c9761b'))

    st.append(Paragraph('Dobór przyrządów — uzasadnienie', S['h2']))
    st.append(Paragraph(
        'Arkusz wymaga, żeby dobrać przyrządy tak, by niepewność była <b>najmniejsza</b>. '
        'Ze wzoru (2-17) wynika, że o niepewności decyduje <b>pomiar U<sub>wz</sub></b>, a nie '
        'rozdzielczość regulacji ani czułość wskaźnika. Dlatego woltomierz mierzący U<sub>wz</sub> '
        'powinien być najdokładniejszym przyrządem w układzie i pracować na <b>najmniejszym '
        'możliwym zakresie</b> — bo δ<sub>g</sub> = a + b·U<sub>z</sub>/U maleje z U<sub>z</sub>.',
        S['body']))
    st.append(Spacer(1, 3))
    st.append(blank_table(
        ['Funkcja w układzie', 'Przyrząd', 'Zakres', 'δ<sub>g</sub> [%]', 'Uzasadnienie wyboru'],
        [4.15 * cm, 2.85 * cm, 2.35 * cm, 2.35 * cm, 5.8 * cm], 3))
    st.append(lh('W kolumnie „Uzasadnienie” wpisz konkret: np. „najmniejszy zakres obejmujący '
                 'U<sub>wz</sub> ≈ 10 V → δ<sub>g</sub> = 0,02 % zamiast 0,04 % na zakresie 30 V”.'))

    st.append(Paragraph('Przebieg równoważenia', S['h2']))
    st.append(Paragraph(
        'W aplikacji <i>Pomiary automatyczne</i> (zakładka <b>Kompensacyjny pomiar SEM</b>) '
        'uruchamiamy serię. Wykres kolejnych wartości U<sub>wz</sub> powinien <b>zbiegać</b> do '
        'wartości SEM: kolejne kroki maleją, a przy dojściu do równowagi wskaźnik zmienia znak '
        'i amplituda oscylacji spada poniżej nieczułości ΔU<sub>min</sub>. Opisz, czy zbieżność '
        'była monotoniczna, czy wystąpiły przeregulowania.', S['body']))
    st.append(Spacer(1, 3))
    st.append(blank_table(['Krok', 'U<sub>wz</sub> [V]', 'Wskazanie wskaźnika W', 'Znak'],
                          [2.1 * cm, 4.0 * cm, 7.0 * cm, 4.1 * cm], 6))
    st.append(Spacer(1, 3))
    st.append(Paragraph('Wykres U<sub>wz</sub>(krok) — wklej z aplikacji', S['h3']))
    st.append(Ruler(4))

    st.append(Paragraph('Wynik i niepewność', S['h2']))
    st.append(Eq(r'u(E) = \sqrt{\left(\frac{\Delta_g U_{wz}}{\sqrt{3}}\right)^{2}'
                 r' + \left(\frac{\Delta U}{\sqrt{3}}\right)^{2}'
                 r' + \left(\frac{\Delta U_{min}}{\sqrt{3}}\right)^{2}}', tag='(2-17)'))
    st.append(Eq(r'u_{rel}(E) = \frac{u(E)}{U_{wz}}\cdot 100\,\%', tag='(2-18)'))
    st.append(Spacer(1, 2))
    st.append(blank_table(
        ['U<sub>wz</sub> ≈ E [V]', 'δ<sub>g</sub>U<sub>wz</sub> [%]',
         'Δ<sub>g</sub>U<sub>wz</sub> [mV]', 'ΔU [mV]', 'ΔU<sub>min</sub> [mV]',
         'u(E) [mV]', 'u<sub>rel</sub>(E) [%]'],
        [2.85 * cm, 2.75 * cm, 2.85 * cm, 1.95 * cm, 2.55 * cm, 2.35 * cm, 2.55 * cm], 1))
    st.append(lh('ΔU — rozdzielczość regulacji napięcia wzorcowego (dla E3646A: 10 mV na działkę); '
                 'ΔU<sub>min</sub> — najmniejsza odczytywalna zmiana na wskaźniku równowagi. '
                 'Wszystkie trzy składniki mają rozkład jednostajny → dzielimy przez √3.'))

    st.append(Paragraph('Porównanie z metodą bezpośrednią', S['h2']))
    st.append(Paragraph(
        'Zestaw wynik dla Źr.3 uzyskany w Zadaniu 2 (metoda bezpośrednia, po korekcji) z wynikiem '
        'kompensacyjnym. <b>Metoda kompensacyjna powinna dać wartość większą</b> — bo nie obciąża '
        'źródła w ogóle, podczas gdy metoda bezpośrednia zawsze ściąga napięcie przez R<sub>V</sub>, '
        'a korekcja opiera się na <i>oszacowanej</i> R<sub>w</sub>, nie na wartości dokładnej.',
        S['body']))
    st.append(Spacer(1, 3))
    st.append(blank_table(['Metoda', 'E [V]', 'u(E) [mV]', 'u<sub>rel</sub>(E) [%]',
                           'Różnica względem kompensacji [%]'],
                          [4.05 * cm, 3.0 * cm, 2.75 * cm, 3.15 * cm, 4.55 * cm], 2))
    st.append(Spacer(1, 4))
    st.append(Paragraph('Wyjaśnienie rozbieżności', S['h3']))
    st.append(Ruler(4))

    st += note_box([Paragraph(
        '<b>Najczęstszy błąd w tym zadaniu.</b> Studenci porównują wynik kompensacyjny z '
        '<i>nieskorygowanym</i> wynikiem metody bezpośredniej i wnioskują o „błędzie metody '
        'kompensacyjnej”. Tymczasem to metoda bezpośrednia jest obciążona — różnica jest '
        '<b>oczekiwana</b> i jej wielkość powinna zgadzać się z obliczonym Δ<sub>m</sub>E. '
        'Jeśli się nie zgadza, sprawdź, czy w Zadaniu 2 użyłeś właściwego R<sub>w</sub>.',
        S['note'])], fill=LIGHT)
    return st


# =========================================================== A. WYPROWADZENIE
def wyprowadzenie():
    st = []
    st.append(sekcja('A', 'WYPROWADZENIE WZORÓW (2-15) i (2-16)',
                     'Skąd biorą się wzory na E i R<sub>w</sub> z dwóch pomiarów napięcia'))
    st.append(Paragraph(
        'Instrukcja podaje gotowy wynik, ale nie pokazuje drogi. Wyprowadzenie jest krótkie '
        'i warto je znać — na kolokwium pytają o <b>założenia</b>, nie o sam wzór.', S['body']))

    st.append(Paragraph('Punkt wyjścia: dwa równania dzielnika', S['h2']))
    st.append(Paragraph(
        'Woltomierz o rezystancji R<sub>V</sub> podłączony do źródła (E, R<sub>w</sub>) tworzy '
        'dzielnik napięcia. Napięcie na zaciskach źródła to napięcie na R<sub>V</sub>:', S['body']))
    st.append(Eq(r'U_1 = E\,\frac{R_{V1}}{R_w + R_{V1}}', tag='(2-13)'))
    st.append(Eq(r'U_2 = E\,\frac{R_{V2}}{R_w + R_{V2}}', tag='(2-14)'))
    st.append(Paragraph(
        'Dwie niewiadome (E, R<sub>w</sub>), dwa równania. Układ jest liniowy ze względu na '
        'E i R<sub>w</sub>, więc rozwiązanie jest jednoznaczne — o ile równania nie są '
        'liniowo zależne, czyli o ile U₁ ≠ U₂.', S['body']))

    st.append(Paragraph('Krok 1 — rugujemy E', S['h2']))
    st.append(Paragraph('Dzielimy (2-13) przez (2-14), żeby pozbyć się E, i mnożymy na krzyż:',
                        S['body']))
    st.append(Eq(r'\frac{U_1}{U_2} = \frac{R_{V1}}{R_{V2}}\cdot\frac{R_w + R_{V2}}{R_w + R_{V1}}'
                 r'\;\Longrightarrow\; U_1 R_{V2}(R_w + R_{V1}) = U_2 R_{V1}(R_w + R_{V2})',
                 tag='(A.1)'))

    st.append(Paragraph('Krok 2 — rozwiązujemy ze względu na R<sub>w</sub>', S['h2']))
    st.append(Paragraph('Grupujemy wyrazy z R<sub>w</sub> po jednej stronie i dzielimy — '
                        'po zmianie znaku w liczniku i mianowniku dostajemy dokładnie (2-16):',
                        S['body']))
    st.append(Eq(r'R_w\,(U_1 R_{V2} - U_2 R_{V1}) = R_{V1}R_{V2}\,(U_2 - U_1)'
                 r'\;\Longrightarrow\; R_w = R_{V1}R_{V2}\,\frac{U_1 - U_2}{R_{V1}U_2 - R_{V2}U_1}',
                 tag='(2-16)'))

    st.append(Paragraph('Krok 3 — wracamy po E', S['h2']))
    st.append(Paragraph(
        'Wyznaczamy R<sub>w</sub> + R<sub>V1</sub> z (2-13), podstawiamy do (2-14), mnożymy przez '
        'mianownik i porządkujemy wyrazy z E:', S['body']))
    st.append(Eq(r'R_w + R_{V1} = E\,\frac{R_{V1}}{U_1}'
                 r'\;\Longrightarrow\; E\,(R_{V1}U_2 - R_{V2}U_1) = U_1U_2\,(R_{V1} - R_{V2})',
                 tag='(A.2)'))
    st.append(Eq(r'E = U_1U_2\,\frac{R_{V1} - R_{V2}}{R_{V1}U_2 - R_{V2}U_1}', tag='(2-15)'))

    st.append(Paragraph('Założenia — i co się dzieje, gdy je złamiesz', S['h2']))
    rows = [
        ['Różnica U₁ − U₂ wynika <b>wyłącznie</b> z różnych R<sub>V</sub>',
         'Źródło jest stabilne w czasie obu pomiarów',
         'Dryf SEM → różnica zawiera człon dryfu, R<sub>w</sub> wychodzi zafałszowana'],
        ['E i R<sub>w</sub> są <b>stałe</b>',
         'Źródło liniowe (Thevenin)',
         'Źródło nieliniowe (np. ogniwo pod obciążeniem) → model (2-1) nie obowiązuje'],
        ['R<sub>V1</sub>, R<sub>V2</sub> znane dokładnie',
         'Dane z instrukcji przyrządów',
         'Błąd R<sub>V</sub> przenosi się na R<sub>w</sub> — patrz część B'],
        ['U₁ i U₂ różnią się <b>znacząco</b>',
         'Różnica <font name="Sans">≫</font> niepewności wskazań',
         'Mianownik (2-16) bliski zeru → katastrofa numeryczna'],
    ]
    st.append(data_table([['Założenie', 'Kiedy spełnione', 'Skutek złamania']] + rows,
                         [4.9 * cm, 4.5 * cm, 8.1 * cm], fs=8.0))
    st.append(Spacer(1, 6))

    st.append(Spacer(1, 5))
    st.append(Paragraph(
        '<b>Granica stosowalności.</b> Instrukcja: wzory (2-15) i (2-16) stosujemy tylko wtedy, '
        'gdy U₁ i U₂ różnią się znacząco. To warunek matematyczny, nie ostrożnościowy: dla '
        'U₁ → U₂ mianownik R<sub>V1</sub>U₂ − R<sub>V2</sub>U₁ → 0 i R<sub>w</sub> staje się '
        'ilorazem 0/0.', ParagraphStyle('gr', fontName='Serif', fontSize=8.6, leading=12.2,
                                        alignment=TA_JUSTIFY, textColor=colors.HexColor('#1d2b3a'),
                                        spaceBefore=1, spaceAfter=0)))
    return st


# =========================================================== B. NIEPEWNOŚĆ RW
def niepewnosc_rw():
    st = []
    st.append(sekcja('B', 'NIEPEWNOŚĆ METODY DWÓCH WOLTOMIERZY',
                     'Czego instrukcja nie podaje — pełny budżet niepewności (2-16)'))
    st.append(Paragraph(
        'Instrukcja stwierdza tylko, że „nie uwzględnia się faktu, że wartości U₁, U₂, '
        'R<sub>V1</sub>, R<sub>V2</sub> są obarczone niepewnością” i na tym poprzestaje. '
        'Poniżej domykamy tę lukę: różniczkujemy (2-16) i budujemy budżet niepewności. '
        'To zarazem odpowiedź na pytanie, <b>który pomiar warto powtórzyć dokładniej</b>.',
        S['body']))

    st.append(Paragraph('Czułości względne', S['h2']))
    st.append(Paragraph(
        'Dla ilorazu wygodnie liczyć pochodne względem logarytmów, bo natychmiast dają '
        'wzmocnienia względne. Po zróżniczkowaniu (2-16) i uporządkowaniu:', S['body']))
    st.append(Eq(r'\frac{\partial R_w}{\partial \ln U_1} = '
                 r'\frac{R_{V1}R_{V2}\,U_1U_2\,(R_{V1}-R_{V2})}'
                 r'{(R_{V1}U_2 - R_{V2}U_1)^2} = -\,\frac{\partial R_w}{\partial \ln U_2}',
                 tag='(B.1)'))
    st.append(Eq(r'\frac{\partial R_w}{\partial \ln R_{V1}} = -\,'
                 r'\frac{R_{V1}R_{V2}^2\,U_1\,(U_1-U_2)}{(R_{V1}U_2 - R_{V2}U_1)^2}'
                 r'\qquad\frac{\partial R_w}{\partial \ln R_{V2}} = '
                 r'\frac{R_{V1}^2R_{V2}\,U_2\,(U_1-U_2)}{(R_{V1}U_2 - R_{V2}U_1)^2}',
                 tag='(B.2)'))
    st.append(Paragraph(
        'Znak minus w (B.1) mówi, że błędy U₁ i U₂ <b>kompensują się częściowo</b> — to '
        'korzystne. W (B.2) pierwsza pochodna jest ujemna, druga dodatnia: przeszacowanie '
        'R<sub>V1</sub> zaniża R<sub>w</sub>, R<sub>V2</sub> — zawyża.', S['body']))

    st.append(Paragraph('Budżet niepewności — przykład liczbowy', S['h2']))
    st.append(Paragraph(
        'Przyjmijmy: E = 10 V, R<sub>w</sub> = 10 kΩ, R<sub>V1</sub> = 10 MΩ (34450A), '
        'R<sub>V2</sub> = 15 kΩ (LM-3 na zakresie 15 V). Wtedy U₁ = 9,990010 V, U₂ = 6,000000 V. '
        'Czułości z (B.1)–(B.2):', S['body']))
    st.append(Spacer(1, 2))
    rows = [
        ['U₁', '0,0183 %', '2,51', '5,0 Ω', '0,06 %'],
        ['U₂', '0,7217 %', '2,51', '180 Ω', '76,3 %'],
        ['R<sub>V1</sub>', '1,0 %', '2,5·10⁻³', '0,25 Ω', '≈ 0 %'],
        ['R<sub>V2</sub>', '1,0 %', '1,00', '100 Ω', '23,6 %'],
    ]
    st.append(data_table([['Składnik', 'u<sub>rel</sub> wejścia', 'Wzmocnienie |∂R<sub>w</sub>/∂ln x|/R<sub>w</sub>',
                           'Wkład', 'Udział w sumie kwadratów']] + rows,
                         [2.35 * cm, 3.1 * cm, 5.55 * cm, 2.55 * cm, 3.95 * cm],
                         align=['l', 'c', 'c', 'c', 'c']))
    st.append(lh('Wzmocnienie 1,00 oznacza, że niepewność wejściowa przenosi się 1:1 na R<sub>w</sub>; '
                 '2,51 — że jest dwuipółkrotnie wzmacniana.'))
    st.append(Paragraph('Po złożeniu (pierwiastek z sumy kwadratów):', S['body']))
    st.append(Eq(r'u(R_w) = \sqrt{5{,}0^2 + 180^2 + 0{,}25^2 + 100^2}\ \Omega'
                 r' \approx 206\ \Omega \;\approx\; 2{,}1\,\%', tag='(B.5)'))

    st.append(Paragraph('Wnioski, których nie ma w instrukcji', S['h2']))
    wnioski = [
        '<b>Decyduje U₂, czyli woltomierz o małym R<sub>V</sub></b> — największa niepewność '
        'względna (0,72 %) razy wzmocnienie 2,51.',
        '<b>R<sub>V1</sub> praktycznie nie wpływa na wynik</b> (wzmocnienie 2,5·10⁻³) — nie warto '
        'certyfikować multimetru 34450A co do R<sub>V</sub>.',
        '<b>R<sub>V2</sub> wnosi 24 %</b> — nie jest pomijalne; κ = 1 kΩ/V to wartość katalogowa.',
        'Niepewność ≈ <b>2 %</b> jest typowa dla tej pary woltomierzy — metoda ustępuje '
        'kompensacyjnej (0,02 %) o dwa rzędy wielkości.',
    ]
    for i, w in enumerate(wnioski, 1):
        st.append(Paragraph(w, S['num'], bulletText=f'{i}.'))
    st.append(Spacer(1, 4))

    st += note_box([Paragraph(
        '<b>Jak poprawić dokładność?</b> Zwiększyć R<sub>V2</sub> (ale R<sub>V</sub> = κ·U<sub>z</sub>, '
        'więc większy zakres go zwiększa kosztem wskazania) albo użyć dwóch multimetrów 10 MΩ — '
        'tyle że wtedy mianownik (2-16) jest bliski zera. <b>Metoda ma wewnętrzny konflikt</b>: '
        'duże R<sub>V2</sub> mało obciąża, małe daje widoczną różnicę. Kompensacja go nie ma.',
        S['note'])], fill=LIGHT)
    return st


# =========================================================== C. ZADANIA DOMOWE
DOM_ROWS = [
    ['Zakresy LM-3', '1,5 · 3 · 7,5 · 15 · 30 · 75 · 150 V'],
    ['Klasa', 'k<sub>l</sub> = 1'],
    ['Współczynnik', 'ϰ = 1 kΩ/V'],
    ['SEM źródła', 'E = dwie ostatnie cyfry albumu [V] (00 → 10 V)'],
    ['R<sub>w</sub> źródła', '1000 Ω'],
    ['Polecenie', 'Δ<sub>m</sub>E oraz u<sub>rel</sub>(E) dla właściwego zakresu'],
]


def zad_domowe():
    st = []
    st.append(sekcja('C', 'ZADANIA DOMOWE',
                     'Zadania 1 i 2 z instrukcji (str. 16) — rozwiązanie wzorcowe'))

    st.append(Paragraph('Zadanie domowe 1 — woltomierz LM-3', S['h2']))
    st.append(data_table([['Parametr', 'Wartość']] + DOM_ROWS,
                         [4.4 * cm, 12.4 * cm], header=True))
    st.append(Spacer(1, 6))

    st.append(Paragraph('Krok 1 — wybór zakresu', S['h3']))
    st.append(Paragraph(
        'Zakres wybieramy <b>najmniejszy, który obejmuje E</b> — to minimalizuje δ<sub>g</sub> '
        '= k<sub>l</sub>·U<sub>z</sub>/100. Dla E z dwóch ostatnich cyfr albumu (1…99 V, przy 00 → 10 V) '
        'zakres zależy od wartości. Zapisujemy to jako funkcję przedziałami:', S['body']))
    st.append(data_table([
        ['Zakres U<sub>z</sub> [V]', '1,5', '3', '7,5', '15', '30', '75', '150'],
        ['Obejmuje E w granicach', 'E ≤ 1,5', '1,5 &lt; E ≤ 3', '3 &lt; E ≤ 7,5',
         '7,5 &lt; E ≤ 15', '15 &lt; E ≤ 30', '30 &lt; E ≤ 75', '75 &lt; E'],
    ], [3.0 * cm, 1.75 * cm, 2.35 * cm, 2.4 * cm, 2.45 * cm, 2.3 * cm, 2.3 * cm, 2.35 * cm],
        align=['l'] + ['c'] * 7, fs=7.6))
    st.append(Spacer(1, 2))

    st.append(Paragraph('Krok 2 — błąd metody', S['h3']))
    st.append(Paragraph(
        'Woltomierz LM-3 obciąża źródło rezystancją R<sub>V</sub> = ϰ·U<sub>z</sub>. Napięcie na '
        'zaciskach spada zgodnie z (2-2), a błąd metody liczymy z (2-4):', S['body']))
    st.append(Eq(r'R_V = \varkappa\,U_z = 1\,\frac{\mathrm{k\Omega}}{\mathrm{V}}\cdot U_z'
                 r'\quad\Longrightarrow\quad \Delta_m E = -U_V\,\frac{R_w}{R_V}'
                 r' = -E\,\frac{R_w}{R_w + R_V}', tag='(C.2)'))
    st.append(Eq(r'\frac{\Delta_m E}{E} = -\frac{R_w}{R_w + R_V}'
                 r' = -\frac{1}{1 + R_V/R_w}', tag='(C.3)'))
    st.append(Paragraph(
        'Błąd względny zależy <b>wyłącznie</b> od stosunku R<sub>V</sub>/R<sub>w</sub> — nie od E. '
        'Dla R<sub>w</sub> = 1000 Ω i ϰ = 1 kΩ/V mamy R<sub>V</sub>/R<sub>w</sub> = U<sub>z</sub> '
        '(liczbowo w woltach na kiloom).', S['body']))

    st.append(Paragraph('Krok 3 — niepewność względna', S['h3']))
    st.append(Paragraph(
        'Dla przyrządu elektromechanicznego rozkład jest jednostajny, więc u = Δ<sub>g</sub>/√3 '
        'wzorem (2-6). Błąd graniczny: Δ<sub>kl</sub>U = k<sub>l</sub>·U<sub>z</sub>/100 wzorem (2-8). '
        'Niepewność względna wskazania U<sub>V</sub>:', S['body']))
    st.append(Eq(r'u_{rel}(U_V) = \frac{k_l\,U_z}{U_V\sqrt{3}}\cdot 100\,\%'
                 r'\;\geq\; \frac{k_l}{\sqrt{3}}\,\% = 0{,}577\,\%\ \ (\text{dla } k_l = 1)',
                 tag='(C.4)'))
    st.append(Paragraph(
        'Minimum 0,577 % osiągamy przy wskazaniu na końcu zakresu, czyli U<sub>V</sub> ≈ U<sub>z</sub>. '
        'To wymaga, żeby SEM źródła leżała blisko końca skali — dlatego wybór zakresu jest '
        'kompromisem między „mały U<sub>z</sub>” (mały Δ<sub>g</sub>) a „U<sub>V</sub> blisko U<sub>z</sub>”.',
        S['body']))
    st.append(Spacer(1, 4))
    st.append(Spacer(1, 3))
    st.append(Paragraph(
        '<b>Spostrzeżenie.</b> Na zakresie 150 V dla E = 96 V błąd metody (−13,0 %) jest 14× '
        'większy niż niepewność (0,90 %) — korekcja jest obowiązkowa.', ParagraphStyle(
            'sp', fontName='Serif', fontSize=8.4, leading=11.8, alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#1d2b3a'), spaceBefore=2, spaceAfter=0)))

    st.append(Paragraph('Kluczowa różnica względem zadania 1', S['h3']))
    st.append(Paragraph(
        'Tu R<sub>V</sub> jest <b>stała</b> (10 MΩ niezależnie od zakresu), a zmienia się tylko '
        'δ<sub>g</sub> od zakresu. Zatem dobór zakresu nie wpływa na błąd metody — wpływa '
        'wyłącznie na niepewność. To odwrotność sytuacji z LM-3, gdzie zakres zmieniał oba.', S['body']))
    return st


def zad_domowe2():
    st = []
    st.append(Paragraph('Zadanie domowe 2 — multimetr 34450A', S['h2']))
    st.append(data_table([
        ['Parametr', 'Wartość'],
        ['Zakresy 34450A', '100 mV · 1 V · 10 V · 100 V · 1000 V'],
        ['R<sub>V</sub>', '10 MΩ (stała, niezależna od zakresu)'],
        ['SEM źródła', 'E = dwie ostatnie cyfry albumu [V] (00 → 10 V)'],
        ['R<sub>w</sub> źródła', '1 MΩ'],
        ['Polecenie', 'Δ<sub>m</sub>E oraz u<sub>rel</sub>(E) dla właściwego zakresu'],
    ], [4.4 * cm, 12.4 * cm], header=True))
    st.append(Spacer(1, 6))

    st.append(Paragraph('Kluczowa różnica względem zadania 1', S['h3']))
    st.append(Paragraph(
        'Tu R<sub>V</sub> jest <b>stała</b> (10 MΩ niezależnie od zakresu), a zmienia się tylko '
        'δ<sub>g</sub> od zakresu — dobór zakresu nie wpływa na błąd metody, tylko na niepewność. '
        'To odwrotność sytuacji z LM-3.', S['body']))
    st.append(Eq(r'\Delta_m E = -E\,\frac{R_w}{R_w + R_V} = -E\,\frac{1\ \mathrm{M\Omega}}'
                 r'{1\ \mathrm{M\Omega} + 10\ \mathrm{M\Omega}} = -0{,}0909\,E', tag='(C.5)'))
    st.append(Spacer(1, 3))

    st.append(Paragraph('Niepewność', S['h3']))
    st.append(Paragraph(
        'δ<sub>g</sub>U dla 34450A: 0,015 % + 0,005 %·U<sub>z</sub>/U. Rozkład jednostajny → √3. '
        'Ponieważ mnożnik korekcji R<sub>w</sub>/R<sub>V</sub> = 0,1 jest stały i znany '
        'dokładnie, niepewność względna po korekcji równa się niepewności względnej przed nią:', S['body']))
    st.append(Eq(r'u_{rel}(E) = u_{rel}(U_V) = \frac{0{,}015\,\% + 0{,}005\,\%\cdot U_z/U_V}{\sqrt{3}}',
                 tag='(C.7)'))
    st.append(Paragraph(
        'Ponieważ U<sub>V</sub> = 0,9091·E, składnik zakresowy liczymy podstawiając tę wartość — '
        'nie E. Dla E = 10 V i zakresu 10 V: U<sub>V</sub> = 9,091 V, δ<sub>g</sub> = 0,015 % + '
        '0,005 %·10/9,091 = 0,0205 %, a u<sub>rel</sub> = 0,0118 %.', S['body']))

    st.append(Paragraph('Tabela wyników', S['h3']))
    rows = []
    for E in [1.0, 5.0, 10.0, 24.0, 48.0, 96.0]:
        Uz = next(z for z in [0.1, 1, 10, 100, 1000] if E <= z)
        Rv = 10e6
        Uv = E * Rv / (1e6 + Rv)
        dm = -E * 1e6 / (1e6 + Rv)
        dg = 0.015 + 0.005 * Uz / Uv
        urel = dg / 3 ** 0.5
        rows.append([f'{E:g}'.replace('.', ','), f'{Uz:g}'.replace('.', ','),
                     f'{Uv:.3f}'.replace('.', ','),
                     f'{dm*1000:.0f}', f'{-dm/E*100:.2f}'.replace('.', ','),
                     f'{dg:.4f}'.replace('.', ','), f'{urel:.4f}'.replace('.', ',')])
    st.append(data_table(
        [['E [V]', 'U<sub>z</sub> [V]', 'U<sub>V</sub> [V]', 'Δ<sub>m</sub>E [mV]',
          'Δ<sub>m</sub>E/E [%]', 'δ<sub>g</sub>U [%]', 'u<sub>rel</sub>(E) [%]']] + rows,
        [2.0 * cm, 2.1 * cm, 2.7 * cm, 3.1 * cm, 3.2 * cm, 2.6 * cm, 3.1 * cm],
        align=['c'] * 7))
    st.append(lh('Błąd metody jest <b>identyczny</b> w każdym wierszu (−9,09 %) — bo R<sub>V</sub> '
                 'jest stała. Zmienia się tylko niepewność, i to przez składnik zakresowy: na '
                 'zakresie 1000 V dla E = 96 V δ<sub>g</sub> rośnie do 0,067 %.'))

    st.append(Spacer(1, 4))
    st.append(Paragraph(
        '<b>Porównanie obu zadań.</b> LM-3: błąd metody zależy od zakresu i jest ogromny, '
        'ale niepewność stała (0,577 %). 34450A: błąd metody stały (−9,09 %), niepewność zależy '
        'od zakresu. „Dobry przyrząd” nie jest pojęciem absolutnym — zależy od tego, czy '
        'dominuje obciążenie źródła, czy rozdzielczość.', ParagraphStyle(
            'por', fontName='Serif', fontSize=8.6, leading=12.2, alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#1d2b3a'))))
    return st


# =========================================================== KONIEC / BUILD
def zakonczenie():
    st = []
    st.append(sekcja('D', 'LISTA KONTROLNA PRZED ODDANIEM',
                     'Co prowadzący sprawdza w protokole — i czego brakuje najczęściej'))
    st.append(Paragraph(
        'Protokół ocenia się nie za „ładne tabele”, ale za to, czy widać w nim <b>rozumowanie</b>. '
        'Poniżej lista w kolejności, w jakiej prowadzący zwykle czyta protokół.', S['body']))
    st.append(Spacer(1, 4))

    rows = [
        ['1', 'Dane identyfikacyjne i ustawienia układu', 'U<sub>zas</sub>, I<sub>ogr</sub>, '
         'R<sub>d</sub>, <b>zakresy obu multimetrów</b>', 'Brak zakresów → nie da się policzyć δ<sub>g</sub>'],
        ['2', 'Zad. 1: tabela pięciu pomiarów', 'U, I, I<sub>obl</sub>, niepewności względne',
         'Pominięta tolerancja opornika dekadowego'],
        ['3', 'Zad. 1: wskaźnik zgodności', 'Wykres z aplikacji + komentarz do wartości wskaźnika',
         'Wykres bez komentarza — najczęstszy brak'],
        ['4', 'Zad. 2: zakres LM-3 i R<sub>V</sub>', 'Jeden zakres dla całej serii, R<sub>V</sub> = ϰ·U<sub>z</sub>',
         'Zmiana zakresu w trakcie serii → metoda nieważna'],
        ['5', 'Zad. 2: R<sub>w</sub> Źr.2 z (2-16)', 'Podstawione liczby, nie tylko wynik',
         'Wynik bez jednostki lub z błędnym indeksem R<sub>V</sub>'],
        ['6', 'Zad. 2: korekcja Δ<sub>m</sub>E', 'Osobno dla 34450A i LM-3, z porównaniem',
         'Korekcja tylko jednego woltomierza'],
        ['7', 'Zad. 3: uzasadnienie doboru przyrządów', 'Odniesienie do (2-17): dominuje U<sub>wz</sub>',
         '„Wzięliśmy najlepszy woltomierz” bez uzasadnienia'],
        ['8', 'Zad. 3: wykres równoważenia', 'Kolejne U<sub>wz</sub>, opis zbieżności',
         'Sam wynik końcowy, bez przebiegu'],
        ['9', 'Zad. 3: porównanie z metodą bezpośrednią', 'Wyjaśnienie <b>kierunku</b> różnicy',
         'Uznanie różnicy za błąd metody kompensacyjnej'],
        ['10', 'Niepewności', 'Wzory z numerami, jednostki, k = 1',
         'Niepewności bez wzorów albo z √3 zamiast 3 (i odwrotnie)'],
    ]
    st.append(data_table([['#', 'Element protokołu', 'Co powinno być', 'Czego brakuje najczęściej']] + rows,
                         [0.85 * cm, 4.9 * cm, 6.35 * cm, 5.25 * cm]))
    st.append(Spacer(1, 10))

    st.append(Paragraph('Trzy zdania, które warto umieć na pamięć', S['h2']))
    st += note_box([Paragraph(
        '<b>1.</b> Woltomierz zawsze obciąża źródło — pytanie nie brzmi „czy”, ale „jak bardzo”, '
        'i odpowiada na nie stosunek R<sub>V</sub>/R<sub>w</sub>.<br/>'
        '<b>2.</b> Metoda kompensacyjna jest jedyną, w której przez źródło badane nie płynie prąd '
        'w równowadze — dlatego jej dokładność ogranicza wyłącznie dokładność napięcia wzorcowego.<br/>'
        '<b>3.</b> Błąd metody i niepewność to dwie różne rzeczy: pierwszy korygujemy obliczeniowo, '
        'drugiej nie da się „odkorygować” — można ją tylko zmniejszyć lepszym przyrządem lub lepszym zakresem.',
        S['note'])], fill=LIGHT)
    st.append(Spacer(1, 12))

    st.append(Paragraph('Odnośniki', S['h2']))
    st.append(Paragraph(
        'Wzory i tabele przywołane w zeszycie pochodzą z instrukcji <i>Ćwiczenie T2. Pomiary napięć '
        'i prądów stałych</i>, wersja 2.4, ISE WEiTI PW: rozdz. 4.1 (niepewność, wzory 2-1…2-12), '
        'rozdz. 4.2 (dwa woltomierze, 2-13…2-16), rozdz. 4.3 (kompensacja, 2-17, 2-18), tabela 2.1 '
        '(błędy graniczne multimetrów), tabela 2.2 (parametry źródeł), str. 16 (zadania domowe). '
        'Pełne omówienie 22 pytań kontrolnych znajduje się w osobnym dokumencie '
        '<i>Odpowiedzi na pytania kontrolne</i> (21 stron), a wersja skrócona — w czterostronicowej '
        '<i>Ściągi</i>.', S['body']))
    return st


class ZeszytDoc(Doc):
    """Dokument bez strony okładkowej — pierwsza strona to zwykła strona tytułowa."""

    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        self.pageTemplates = []
        cw = K.PAGE_W - K.LM - K.RM
        ch = K.PAGE_H - K.TM - K.BM
        self.addPageTemplates([
            K.PageTemplate(id='body', frames=[
                K.Frame(K.LM, K.BM, cw, ch, id='body',
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0)]),
        ])


def main():
    K.NumberedCanvas.header_right = 'Zeszyt ćwiczeń'
    K.NumberedCanvas.footer_left = 'Laboratorium Podstaw Pomiarów · ISE WEiTI PW'
    K.Doc.cover_draw = None

    story = []
    story += page_tytul()
    story.append(PageBreak())
    story += zad1()
    story.append(PageBreak())
    story += zad2()
    story.append(PageBreak())
    story += zad3()
    story.append(PageBreak())
    story += wyprowadzenie()
    story.append(PageBreak())
    story += niepewnosc_rw()
    story.append(PageBreak())
    story += zad_domowe()
    story.append(PageBreak())
    story += zad_domowe2()
    story.append(PageBreak())
    story += zakonczenie()

    out = os.path.join(K.ROOT, OUT)
    K.build_with(story, out, doc_cls=ZeszytDoc)
    print('OK ->', out, os.path.getsize(out), 'B')


if __name__ == '__main__':
    main()
