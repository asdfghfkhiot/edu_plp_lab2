"""Budowa dokumentu PDF: odpowiedzi na pytania kontrolne do ćwiczenia T2.

Uruchomienie:  .venv/bin/python scripts/build_answers.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pdfkit as K
from pdfkit import (S, Eq, Badge, PartHeading, fig_block, note_box, data_table,
                    build, CONTENT_W, NAVY, ACCENT, GREY, RULE, LIGHT, LIGHT2)
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle, Flowable,
                                NextPageTemplate, PageBreak, KeepTogether, Image)

ROOT = K.ROOT
FIG = K.FIGDIR
OUT = os.path.join(ROOT, 'Cwiczenie_T2_-_odpowiedzi_na_pytania_kontrolne.pdf')


# ------------------------------------------------------------------ helpers
def P(txt, style='body'):
    return Paragraph(txt, S[style])


def bullets(items, style='bullet', mark='\u2022'):
    return [Paragraph(t, S[style], bulletText=mark) for t in items]


def gap(h=5):
    return Spacer(1, h)


class KSpacer(Spacer):
    """Odstęp, który 'trzyma się' następnego elementu (łańcuch keepWithNext)."""

    def __init__(self, h):
        super().__init__(1, h)
        self.keepWithNext = 1


class QuestionHead(Flowable):
    """Nagłówek pytania: numer w kółku, treść, linia, zakładka PDF."""

    def __init__(self, num, text):
        super().__init__()
        self.num = num
        self.text = text
        self.p = Paragraph(text, S['q'])
        self.d = 0.80 * cm
        self.gapx = 0.30 * cm
        self.pad_top = 8
        self.keepWithNext = 1

    def wrap(self, aw, ah):
        avail = CONTENT_W - self.d - self.gapx
        w, h = self.p.wrap(avail, ah)
        self.hp = h
        self.h = h + 2 * self.pad_top + 6
        return CONTENT_W, self.h

    def draw(self):
        c = self.canv
        h = self.h
        ytop = h
        c.setFillColor(NAVY)
        c.circle(self.d / 2.0, ytop - self.pad_top - self.hp / 2.0, self.d / 2.0,
                 stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont('Sans-Bold', 9.6 if self.num < 10 else 8.6)
        c.drawCentredString(self.d / 2.0, ytop - self.pad_top - self.hp / 2.0 - 3.4,
                            str(self.num))
        self.p.drawOn(c, self.d + self.gapx, ytop - self.pad_top - self.hp)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.55)
        c.line(0, 2.6, CONTENT_W, 2.6)
        key = f'q{self.num}'
        c.bookmarkPage(key, fit='XYZ', top=self.h)
        c.addOutlineEntry(f'Pytanie {self.num}', key, level=0, closed=0)


def Q(num, text):
    return [KSpacer(9), QuestionHead(num, text), Spacer(1, 5)]


# ------------------------------------------------------------------ okładka
def draw_cover(c):
    from pdfkit import PAGE_W, PAGE_H, LM, RM
    band = 8.9 * cm
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - band, PAGE_W, band, stroke=0, fill=1)
    c.setFillColor(colors.HexColor('#1c4573'))
    c.rect(0, PAGE_H - band, 0.62 * cm, band, stroke=0, fill=1)
    c.setFillColor(colors.HexColor('#2c6cb0'))
    c.rect(0, PAGE_H - band, PAGE_W, 0.11 * cm, stroke=0, fill=1)

    c.setFillColor(colors.HexColor('#a8c6e8'))
    c.setFont('Sans', 8.2)
    c.drawString(LM + 0.2 * cm, PAGE_H - 2.35 * cm,
                 'LABORATORIUM PODSTAW POMIARÓW \u00b7 INSTYTUT SYSTEMÓW ELEKTRONICZNYCH')
    c.drawString(LM + 0.2 * cm, PAGE_H - 2.80 * cm,
                 'WYDZIA\u0141 ELEKTRONIKI I TECHNIK INFORMACYJNYCH \u00b7 POLITECHNIKA WARSZAWSKA')

    c.setFillColor(colors.white)
    c.setFont('Sans-Bold', 30)
    c.drawString(LM + 0.2 * cm, PAGE_H - 5.15 * cm, '\u0106wiczenie T2')
    c.setFont('Sans', 16.5)
    c.setFillColor(colors.HexColor('#e6eefa'))
    c.drawString(LM + 0.2 * cm, PAGE_H - 6.08 * cm, 'Pomiary napięć i prądów stałych')

    c.setStrokeColor(colors.HexColor('#7ea8d8'))
    c.setLineWidth(1.1)
    c.line(LM + 0.2 * cm, PAGE_H - 6.72 * cm, LM + 10.2 * cm, PAGE_H - 6.72 * cm)

    c.setFillColor(colors.white)
    c.setFont('Sans-Bold', 14.4)
    c.drawString(LM + 0.2 * cm, PAGE_H - 7.72 * cm, 'Odpowiedzi na pytania kontrolne')

    c.setFillColor(colors.HexColor('#b9d0ea'))
    c.setFont('Sans', 8.9)
    c.drawString(LM + 0.2 * cm, PAGE_H - 8.32 * cm,
                 'opracowanie na podstawie instrukcji do ćwiczenia, wersja 2.4 (20.10.2023)')

    y = PAGE_H - band - 1.15 * cm
    c.setFillColor(NAVY)
    c.setFont('Sans-Bold', 10.3)
    c.drawString(LM, y, 'Zawartość opracowania')
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(LM, y - 0.17 * cm, PAGE_W - RM, y - 0.17 * cm)

    parts = [
        ('I', 'Wiadomości podstawowe \u2013 źródło napięcia', 'pytania 1\u20133'),
        ('II', 'Woltomierze i sposób ich włączania', 'pytania 4\u20136'),
        ('III', 'Błąd metody pomiaru', 'pytania 7\u20138'),
        ('IV', 'Niepewność pomiaru przyrządem elektromechanicznym', 'pytania 9\u201311'),
        ('V', 'Wyznaczanie rezystancji wewnętrznej źródła', 'pytanie 12'),
        ('VI', 'Metoda kompensacyjna pomiaru SEM', 'pytania 13\u201315'),
        ('VII', 'Wpływ rezystancji wewnętrznej przyrządów', 'pytania 16\u201318'),
        ('VIII', 'Zadania rachunkowe', 'pytania 19\u201322'),
    ]
    yy = y - 1.00 * cm
    for rzym, title, rng in parts:
        c.setFillColor(ACCENT)
        c.setFont('Sans-Bold', 8.8)
        c.drawString(LM, yy, rzym)
        c.setFillColor(colors.HexColor('#1a222c'))
        c.setFont('Sans', 9.2)
        c.drawString(LM + 1.05 * cm, yy, title)
        c.setFillColor(GREY)
        c.setFont('Sans-Italic', 8.2)
        c.drawRightString(PAGE_W - RM, yy, rng)
        yy -= 0.635 * cm

    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(LM, 3.72 * cm, PAGE_W - RM, 3.72 * cm)
    c.setFillColor(GREY)
    c.setFont('Sans', 7.6)
    c.drawString(LM, 3.25 * cm, 'Zakres: 22 pytania kontrolne do ćwiczenia T2 (instrukcja v. 2.4)')
    c.drawString(LM, 2.88 * cm,
                 'Niepewności podano jako niepewności standardowe (współczynnik rozszerzenia k = 1)')
    c.drawString(LM, 2.51 * cm,
                 'Oznaczenia, wzory i wartości liczbowe zgodne z instrukcją do ćwiczenia (rozdz. 4)')
    c.setFillColor(NAVY)
    c.setFont('Sans-Bold', 8.4)
    c.drawRightString(PAGE_W - RM, 3.25 * cm, 'Warszawa \u00b7 wersja 1.0')


# ------------------------------------------------------------------ wstęp
def intro():
    st = [NextPageTemplate('body'), PageBreak(), gap(2)]
    st += [Paragraph('Wprowadzenie', ParagraphStyle(
        'h', fontName='Sans-Bold', fontSize=15.5, leading=19, textColor=NAVY,
        spaceAfter=2))]
    st += [Paragraph('Jak czytać ten dokument', S['part_sub'])]

    st += [P(
        'Opracowanie zawiera odpowiedzi na wszystkie 22 pytania kontrolne zamieszczone na '
        'końcu instrukcji do ćwiczenia T2 \u201ePomiary napięć i prądów stałych\u201d. Pytania '
        'połączono w osiem części tematycznych, a ich kolejność i numeracja odpowiadają '
        'instrukcji. Przy każdym pytaniu przytoczono jego treść, a następnie podano '
        'odpowiedź w postaci zwięzłego wyjaśnienia, wyprowadzenia wzorów, schematu lub '
        'obliczeń.')]
    st += [P(
        'Odpowiedzi na pytania 17 oraz 19\u201322 zawierają pełne rachunki, ponieważ tego typu '
        'zadania najczęściej sprawdzane są na zaliczeniu. Wyniki liczbowe zestawiono '
        'dodatkowo w tabeli zbiorczej na końcu dokumentu.')]

    st += [gap(7)]
    st += [Paragraph('Przyjęte oznaczenia', S['part'])]
    st += [gap(3)]
    sym = [
        ['Symbol', 'Znaczenie', 'Jednostka'],
        ['<i>E</i>', 'siła elektromotoryczna (SEM) źródła, równa napięciu źródła idealnego', 'V'],
        ['<i>R</i><sub>w</sub>', 'rezystancja wewnętrzna rzeczywistego źródła napięcia', 'Ω'],
        ['<i>U</i>, <i>U</i><sub>V</sub>', 'napięcie zmierzone (na zaciskach źródła, na woltomierzu)', 'V'],
        ['<i>I</i>, <i>I</i><sub>V</sub>', 'prąd w obwodzie (prąd pobierany przez woltomierz)', 'A'],
        ['<i>R</i><sub>V</sub>, <i>R</i><sub>A</sub>', 'rezystancja wewnętrzna woltomierza i amperomierza', 'Ω'],
        ['<i>U</i><sub>z</sub>, <i>I</i><sub>z</sub>', 'zakres pomiarowy napięcia i prądu', 'V, A'],
        ['<i>k</i><sub>l</sub>', 'klasa dokładności przyrządu elektromechanicznego', '%'],
        ['δ<sub>g</sub><i>x</i>', 'największy dopuszczalny błąd względny pomiaru wielkości <i>x</i>', '%'],
        ['Δ<sub>m</sub><i>E</i>', 'błąd metody pomiaru siły elektromotorycznej', 'V'],
        ['<i>u</i>(<i>x</i>)', 'niepewność standardowa (bezwzględna) wielkości <i>x</i>', 'V, A, Ω'],
        ['<i>u</i><sub>rel</sub>(<i>x</i>)', 'niepewność standardowa względna wielkości <i>x</i>', '%'],
        ['<i>n</i>', 'wskazanie przyrządu cyfrowego bez kropki dziesiętnej', '\u2013'],
        ['κ', 'czułość napięciowa woltomierza magnetoelektrycznego: <i>R</i><sub>V</sub> = κ·<i>U</i><sub>z</sub>', 'Ω/V'],
    ]
    st += [data_table(sym, [2.55 * cm, 11.35 * cm, 1.70 * cm],
                      align=['c', 'l', 'c'])]
    st += [gap(9)]

    st += [Paragraph('Sposób wyznaczania niepewności', S['part'])]
    st += [gap(3)]
    st += [P(
        'W całym opracowaniu stosuje się konwencję przyjętą w Laboratorium Podstaw Pomiarów '
        'i opisaną w rozdz. 4.1 instrukcji. Największy dopuszczalny błąd pomiaru traktowany '
        'jest jako granica przedziału, w którym błąd może wystąpić z jednakowym '
        'prawdopodobieństwem (rozkład jednostajny), a niepewność standardowa jest '
        'odchyleniem standardowym tego rozkładu:')]
    st += [Eq(r'$u(x) = \dfrac{\Delta_g x}{\sqrt{3}} = \dfrac{x\cdot\delta_g x}{\sqrt{3}\cdot 100\%}$',
              tag='(2-6)')]
    st += [P(
        'Dla elementów wzorcowych \u2013 np. opornika dekadowego lub rezystora o znanej '
        'tolerancji \u2013 instrukcja przyjmuje rozkład normalny i niepewność równą jednej '
        'trzeciej błędu granicznego:')]
    st += [Eq(r'$u(x) = \dfrac{\Delta_g x}{3} = \dfrac{x\cdot\delta_g x}{3\cdot 100\%}$',
              tag='(2-11)')]
    st += [P(
        'Niepewność standardową wielkości wyznaczanej pośrednio <i>y</i> = <i>f</i>(<i>x</i><sub>1</sub>, '
        '<i>x</i><sub>2</sub>, \u2026) oblicza się z prawa propagacji niepewności. Dla iloczynów '
        'i ilorazów wygodnie jest posłużyć się niepewnościami względnymi:')]
    st += [Eq(r'$y = x_1\,x_2^{\pm 1} \;\;\Longrightarrow\;\; u_{rel}(y) = \sqrt{u_{rel}^2(x_1) + u_{rel}^2(x_2)}$',
              tag='(W-1)')]
    st += [P(
        'Podane wartości są niepewnościami standardowymi, czyli odpowiadają współczynnikowi '
        'rozszerzenia <i>k</i> = 1. Niepewność rozszerzoną dla <i>k</i> = 2 otrzymuje się, '
        'mnożąc wynik przez dwa.')]

    st += [gap(7)]
    st += note_box([Paragraph(
        '<b>Uwaga o zgodności z instrukcją.</b> Numery wzorów w nawiasach \u2013 np. (2-2), '
        '(2-15) \u2013 oznaczają numerację z instrukcji do ćwiczenia T2 (wersja 2.4). Wzory '
        'oznaczone symbolem (W-<i>n</i>) są zależnościami pomocniczymi wyprowadzonymi '
        'w tym opracowaniu.', S['note'])],
        fill=colors.HexColor('#f4f7fb'), bar=GREY)
    return st


# ================================================================== CZĘŚĆ I
def part1():
    st = []
    st += [PartHeading('I', 'Wiadomości podstawowe \u2013 źródło napięcia',
                       'pytania 1\u20133')]

    # ---------------------------------------------------------- Q1
    st += Q(1, 'Czym się różni rzeczywiste źródło napięcia od źródła idealnego?')
    st += [P(
        'Źródło idealne charakteryzuje się zerową rezystancją wewnętrzną: napięcie na jego '
        'zaciskach jest zawsze równe sile elektromotorycznej <i>E</i>, niezależnie od tego, '
        'jaki prąd pobiera z niego obciążenie. W źródle rzeczywistym występuje niezerowa '
        'rezystancja wewnętrzna <i>R</i><sub>w</sub>, na której przy poborze prądu <i>I</i> '
        'odkłada się spadek napięcia; napięcie zaciskowe jest więc mniejsze od SEM:')]
    st += [Eq(r'$U = E - I\,R_w$', tag='(W-2)')]
    st += [P(
        'Konsekwencje tej różnicy najłatwiej prześledzić na charakterystyce zewnętrznej '
        '<i>U</i> = <i>f</i>(<i>I</i>). Źródło idealne daje prostą poziomą, a rzeczywiste '
        '\u2013 prostą opadającą o nachyleniu \u2212<i>R</i><sub>w</sub>:')]

    st += fig_block(os.path.join(FIG, 'fig01_charakterystyka.png'), 12.0,
                     'Charakterystyka zewnętrzna źródła napięcia: idealnego (niebieska) '
                     'oraz rzeczywistego (czerwona). Napięcie źródła rzeczywistego maleje '
                     'liniowo wraz z prądem obciążenia, a prąd zwarcia jest ograniczony '
                     'do wartości <i>E</i>/<i>R</i><sub>w</sub>.', 1)

    st += [gap(4)]
    por = [
        ['Cecha', 'Źródło idealne', 'Źródło rzeczywiste'],
        ['Rezystancja wewnętrzna', '<i>R</i><sub>w</sub> = 0', '<i>R</i><sub>w</sub> &gt; 0'],
        ['Napięcie na zaciskach', '<i>U</i> = <i>E</i> = const', '<i>U</i> = <i>E</i> \u2212 <i>I</i>·<i>R</i><sub>w</sub>'],
        ['Zależność od obciążenia', 'brak', 'napięcie maleje ze wzrostem prądu'],
        ['Prąd zwarcia', 'teoretycznie nieskończony', '<i>I</i><sub>k</sub> = <i>E</i>/<i>R</i><sub>w</sub> \u2013 skończony'],
        ['Moc wydzielana w źródle', 'zero', '<i>P</i><sub>str</sub> = <i>I</i><sup>2</sup>·<i>R</i><sub>w</sub>'],
        ['Możliwość realizacji', 'tylko jako model', 'każde realne źródło (bateria, zasilacz)'],
    ]
    st += [data_table(por, [4.55 * cm, 5.35 * cm, 6.90 * cm],
                      align=['l', 'c', 'c'])]
    st += [gap(5)]
    st += [P(
        'W praktyce każde źródło jest więc rzeczywiste, a model idealny stosuje się wtedy, '
        'gdy rezystancja wewnętrzna jest pomijalnie mała w porównaniu z rezystancją '
        'obciążenia (<i>R</i><sub>w</sub> <font name="Sans">\u226a</font> <i>R</i><sub>obc</sub>). Wtedy błąd '
        'wynikający z pominięcia <i>R</i><sub>w</sub> jest mniejszy od niepewności pomiaru.')]

    # ---------------------------------------------------------- Q2
    st += Q(2, 'Narysuj schemat zastępczy rzeczywistego źródła napięcia i oznacz jego elementy.')
    st += [P(
        'Rzeczywiste źródło napięcia stałego można przedstawić jako szeregowe połączenie '
        'źródła idealnego o sile elektromotorycznej <i>E</i> oraz rezystora '
        '<i>R</i><sub>w</sub> reprezentującego rezystancję wewnętrzną. Zaciski wyjściowe '
        'oznaczono literami <i>A</i> i <i>B</i>:')]

    st += fig_block(os.path.join(FIG, 'fig02_zrodlo.png'), 9.6,
                     'Schemat zastępczy rzeczywistego źródła napięcia stałego. '
                     '<i>E</i> \u2013 siła elektromotoryczna (SEM), <i>R</i><sub>w</sub> '
                     '\u2013 rezystancja wewnętrzna, <i>A</i> i <i>B</i> \u2013 zaciski '
                     'wyjściowe, <i>U</i><sub>AB</sub> \u2013 napięcie zaciskowe.', 2)

    st += [gap(2)]
    st += [P('<b>Elementy schematu:</b>')]
    st += bullets([
        '<b><i>E</i></b> \u2013 siła elektromotoryczna źródła: napięcie źródła idealnego '
        'wchodzącego w skład modelu, liczone między jego biegunami przy prądzie równym zeru.',
        '<b><i>R</i><sub>w</sub></b> \u2013 rezystancja wewnętrzna: wypadkowa rezystancja '
        'wszystkich elementów wewnętrznych źródła (opór elektrolitu, rezystancja uzwojeń, '
        'rezystancja wyjściowa stabilizatora itp.).',
        '<b><i>A</i>, <i>B</i></b> \u2013 zaciski wyjściowe źródła, do których dołącza się '
        'obciążenie lub przyrząd pomiarowy.',
        '<b><i>U</i><sub>AB</sub></b> \u2013 napięcie zaciskowe, czyli różnica potencjałów '
        'między zaciskami obciążonego źródła.',
    ])
    st += [gap(3)]
    st += [P(
        'Napięcie zaciskowe zależy od prądu obciążenia zgodnie z II prawem Kirchhoffa:')]
    st += [Eq(r'$U_{AB} = E - I\,R_w = E\,\dfrac{R_{obc}}{R_w + R_{obc}}$', tag='(W-3)')]
    st += [P(
        'gdzie <i>R</i><sub>obc</sub> jest rezystancją obciążenia dołączonego do zacisków. '
        'Szeregowy model źródła (twierdzenie Thevenina) obowiązuje dla dowolnego liniowego '
        'obwodu zawierającego źródła \u2013 każdy taki obwód można sprowadzić do jednego '
        'źródła <i>E</i> i jednej rezystancji <i>R</i><sub>w</sub>, widzianych z wybranych '
        'zacisków.')]

    # ---------------------------------------------------------- Q3
    st += Q(3, 'Jakie wartości przyjmuje rezystancja wewnętrzna rzeczywistych źródeł napięcia?')
    st += [P(
        'Rezystancja wewnętrzna rzeczywistych źródeł waha się w bardzo szerokich granicach '
        '\u2013 od ułamka milioma do kilku kiloomów \u2013 i zależy od rodzaju źródła, jego '
        'stanu oraz warunków pracy (temperatura, stopień naładowania, obciążenie).')]
    st += [gap(3)]
    rw = [
        ['Rodzaj źródła', '<i>R</i><sub>w</sub>', 'Uwagi'],
        ['Zasilacz stabilizowany (profesjonalny)', 'od ułamka mΩ do kilku mΩ', 'bardzo mała, dzięki silnemu ujemmenu sprzężeniu zwrotnemu'],
        ['Zasilacz laboratoryjny E3646A', 'rzędu mΩ\u2013Ω', 'zależna od kanału i zakresu napięcia'],
        ['Akumulator samochodowy', 'kilka mΩ', 'mała, ale duży prąd rozruchowy'],
        ['Ogniwo alkaliczne (AA, 1,5 V)', 'od ok. 0,1 Ω do 1 Ω', 'rośnie wraz z rozładowaniem'],
        ['Bateria ogniw w latarce, zegarku', 'od kilku Ω do kilku kΩ', 'zależnie od typu i stanu'],
        ['Ogniwo Li-Ion', 'kilkadziesiąt mΩ', 'rośnie w niskiej temperaturze'],
        ['Źródło sygnału (czujnik, dzielnik)', 'od kΩ do MΩ', 'wynika z konfiguracji obwodu'],
        ['Wzorcowe źródło napięcia (np. kompensator)', 'bardzo mała lub kontrolowana', 'decyduje o dokładności SEM'],
    ]
    st += [data_table(rw, [6.05 * cm, 4.45 * cm, 6.30 * cm],
                      align=['l', 'c', 'l'])]
    st += [gap(5)]
    st += [P(
        'Instrukcja do ćwiczenia podaje, że rezystancja wewnętrzna profesjonalnych zasilaczy '
        'jest rzędu ułamka mΩ, a rezystancja baterii i akumulatorów służących do zasilania '
        'urządzeń waha się w granicach od kilku mΩ do kilku kΩ. W praktyce oznacza to, że:')]
    st += bullets([
        'źródło o <i>R</i><sub>w</sub> rzędu mΩ zachowuje się prawie jak źródło idealne '
        'i można je tak traktować w większości pomiarów,',
        'źródło o <i>R</i><sub>w</sub> rzędu kΩ silnie \u201ezapada się\u201d pod obciążeniem, '
        'a pomiar jego SEM wymaga metody o małym poborze prądu (np. kompensacyjnej),',
        'rezystancja wewnętrzna ogniw rośnie w miarę rozładowania i spadku temperatury, '
        'dlatego nie jest wielkością stałą.',
    ])
    return st


# ================================================================== CZĘŚĆ II
def part2():
    st = []
    st += [Spacer(1, 6), PartHeading('II', 'Woltomierze i sposób ich włączania',
                                     'pytania 4\u20136')]

    # ---------------------------------------------------------- Q4
    st += Q(4, 'Do czego służy woltomierz i jakimi parametrami można go scharakteryzować?')
    st += [P(
        'Woltomierz służy do pomiaru napięcia, czyli różnicy potencjałów między dwoma '
        'punktami obwodu elektrycznego. Dołącza się go do tych punktów równolegle \u2013 '
        'mierzy napięcie odkładające się na elemencie lub na zaciskach źródła. Podstawowym '
        'parametrem opisującym jego wpływ na obwód jest rezystancja wewnętrzna '
        '<i>R</i><sub>V</sub>; pozostałe parametry decydują o dokładności i wygodzie '
        'pomiaru.')]
    st += [gap(3)]
    par = [
        ['Parametr', 'Znaczenie i rola w pomiarze'],
        ['Rezystancja wewnętrzna <i>R</i><sub>V</sub>',
         'decyduje o prądzie pobieranym z obwodu i o błędzie metody; dla woltomierza '
         'idealnego <i>R</i><sub>V</sub> \u2192 \u221e'],
        ['Zakres pomiarowy <i>U</i><sub>z</sub>',
         'największa wartość napięcia, którą można zmierzyć bez zmiany zakresu; wpływa na '
         'błąd graniczny przyrządu analogowego'],
        ['Klasa dokładności <i>k</i><sub>l</sub>',
         'parametr woltomierza elektromechanicznego (np. 0,5) określający największy '
         'dopuszczalny błąd bezwzględny Δ<sub>kl</sub><i>U</i> = <i>k</i><sub>l</sub>'
         '\u00b7<i>U</i><sub>z</sub>/100'],
        ['Największy dopuszczalny błąd δ<sub>g</sub><i>U</i>',
         'parametr woltomierza cyfrowego, podawany w postaci zależności od zakresu i wskazania'],
        ['Rozdzielczość (liczba cyfr)',
         'najmniejsza zmiana napięcia dająca zmianę wskazania; dla przyrządów cyfrowych '
         'określona liczbą cyfr, np. 4\u00bd lub 5\u00bd'],
        ['Czułość napięciowa κ',
         'dla woltomierzy magnetoelektrycznych κ = <i>R</i><sub>V</sub>/<i>U</i><sub>z</sub> '
         '[\u03a9/V]; np. dla LM-3 κ = 1 k\u03a9/V'],
        ['Rezystancja wejściowa / prąd wejściowy',
         'parametry charakteryzujące obciążenie obwodu przez woltomierz (elektroniczny '
         'o dużej rezystancji wejściowej)'],
        ['Typ przetwornika',
         'magnetoelektryczny, elektromagnetyczny, elektroniczny (cyfrowy), kompensatorowy \u2013 '
         'decyduje o klasie i rezystancji wewnętrznej'],
    ]
    st += [data_table(par, [5.25 * cm, 11.55 * cm], align=['l', 'l'])]
    st += [gap(4)]
    st += [P(
        'Przy wyborze woltomierza kierujemy się przede wszystkim stosunkiem jego rezystancji '
        'wewnętrznej do rezystancji źródła, którego napięcie mierzymy: im większy jest '
        'stosunek <i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>, tym mniejszy błąd metody. '
        'Drugim kryterium jest wymagana dokładność, którą określa klasa przyrządu lub '
        'graniczny błąd przyrządu cyfrowego.')]

    # ---------------------------------------------------------- Q5
    st += Q(5, 'Jaką rezystancją wewnętrzną charakteryzują się spotykane w praktyce '
               'woltomierze?')
    st += [P(
        'Rezystancja wewnętrzna woltomierzy zależy od ich typu i zawiera się w bardzo szerokim '
        'zakresie. Instrukcja do ćwiczenia podaje, że wynosi ona od kilku kiloomów w przypadku '
        'mierników magnetoelektrycznych do nawet 10 G\u03a9 w przypadku stacjonarnych, '
        'profesjonalnych woltomierzy.')]
    st += [gap(3)]
    rv = [
        ['Typ woltomierza', '<i>R</i><sub>V</sub>', 'Przykład / uwagi'],
        ['Magnetoelektryczny (analogowy)', 'od kilku kΩ do kilkuset kΩ',
         'LM-3: <i>R</i><sub>V</sub> = κ·<i>U</i><sub>z</sub>, κ = 1 kΩ/V \u2013 np. 15 kΩ '
         'na zakresie 15 V'],
        ['Cyfrowy ręczny (multimetr)', 'ok. 10 MΩ',
         'U1252B \u2013 typowa wartość wejściowa dla napięcia stałego'],
        ['Cyfrowy laboratoryjny (multimetr stołowy)', '10 MΩ',
         '34450A \u2013 wartość przyjmowana w ćwiczeniu'],
        ['Stacjonarny, profesjonalny woltomierz', 'nawet 10 GΩ',
         'woltomierze elektrometryczne / wzmacniacze pomiarowe'],
        ['Woltomierz idealny (model)', '<i>R</i><sub>V</sub> \u2192 \u221e',
         'nie pobiera prądu z obwodu, nie zmienia warunków pomiaru'],
    ]
    st += [data_table(rv, [5.75 * cm, 4.35 * cm, 6.70 * cm],
                      align=['l', 'c', 'l'])]
    st += [gap(5)]
    st += [P(
        'Z punktu widzenia pomiaru napięcia na zaciskach źródła o rezystancji '
        '<i>R</i><sub>w</sub> istotny jest stosunek <i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>. '
        'Woltomierz o rezystancji 10 MΩ można uznać za \u201eprawie idealny\u201d dla źródeł '
        'o <i>R</i><sub>w</sub> rz\u0119du kiloomów, natomiast woltomierz magnetoelektryczny '
        'o rezystancji 15 kΩ jest obciążeniem znaczącym dla źródła o '
        '<i>R</i><sub>w</sub> = 10 kΩ.')]

    # ---------------------------------------------------------- Q6
    st += Q(6, 'W jaki sposób włącza się w obwód pomiarowy amperomierz, a w jaki woltomierz?')
    st += [P(
        '<b>Amperomierz włącza się szeregowo</b> z elementem, przez który płynie mierzony prąd '
        '\u2013 prąd musi przepłynąć przez przyrząd. <b>Woltomierz włącza się równolegle</b> '
        'do elementu lub zacisków, na których mierzone jest napięcie. Oba sposoby włączenia '
        'pokazano na rysunku:')]

    st += fig_block(os.path.join(FIG, 'fig03_mierniki.png'), 10.3,
                     'Sposób włączania mierników: amperomierz <b>A</b> szeregowo '
                     'z odbiornikiem <i>R</i>, woltomierz <b>V</b> równolegle do odbiornika. '
                     'Strzałką zaznaczono prąd <i>I</i> płynący w obwodzie.', 3)

    st += [gap(3)]
    st += [P('<b>Wynikające stąd wymagania wobec przyrządów:</b>')]
    st += bullets([
        'amperomierz powinien mieć jak najmniejszą rezystancję wewnętrzną '
        '(<i>R</i><sub>A</sub> \u2192 0), aby jego włączenie nie zmieniało prądu w obwodzie; '
        'idealny amperomierz ma <i>R</i><sub>A</sub> = 0,',
        'woltomierz powinien mieć jak największą rezystancję wewnętrzną '
        '(<i>R</i><sub>V</sub> \u2192 \u221e), aby nie pobierał prądu z obwodu; idealny '
        'woltomierz ma <i>R</i><sub>V</sub> = \u221e,',
        'należy zachować właściwą biegunowość: zacisk \u201e+\u201d przyrządu od strony '
        'wyższego potencjału,',
        'amperomierz włącza się po przerwaniu obwodu (szeregowo), a woltomierz dołącza się '
        'do istniejących punktów obwodu \u2013 nigdy nie włącza się woltomierza szeregowo '
        'ani amperomierza równolegle, gdyż prowadzi to do zwarcia lub do błędnego wskazania.',
    ])
    st += [gap(3)]
    st += [P(
        'Niezależnie od sposobu włączenia przyrząd pobiera z obwodu pewną moc, która jest '
        'źródłem błędu metody. W przypadku amperomierza jest to spadek napięcia '
        '<i>I</i>·<i>R</i><sub>A</sub> na jego rezystancji, a w przypadku woltomierza \u2013 '
        'prąd <i>U</i>/<i>R</i><sub>V</sub> pobierany równolegle do mierzonego elementu.')]
    return st


# ================================================================== CZĘŚĆ III
def part3():
    st = []
    st += [Spacer(1, 6), PartHeading('III', 'Błąd metody pomiaru',
                                     'pytania 7\u20138')]

    # ---------------------------------------------------------- Q7
    st += Q(7, 'Co to jest błąd metody? Narysuj odpowiedni schemat i opisz istotę tego '
               'błędu dla bezpośredniego pomiaru napięcia.')
    st += [P(
        '<b>Błąd metody</b> (błąd teoretyczny) to błąd wynikający z samej zasady pomiaru '
        '\u2013 z faktu, że przyrząd pomiarowy, dołączony do obwodu, zmienia warunki, '
        'w których ten obwód pracował przed pomiarem. Jest to błąd <b>systematyczny</b>, '
        'a więc powtarzalny i <b>korygowalny</b>: znając jego wartość, można poprawić wynik '
        'pomiaru.')]
    st += [P(
        'W bezpośrednim pomiarze napięcia na zaciskach rzeczywistego źródła woltomierzem '
        'o skończonej rezystancji wewnętrznej <i>R</i><sub>V</sub> dołączenie woltomierza '
        'zamyka obwód i wymusza przepływ prądu <i>I</i><sub>V</sub>:')]

    st += fig_block(os.path.join(FIG, 'fig04_woltomierz.png'), 10.0,
                     'Błąd metody przy bezpośrednim pomiarze napięcia: woltomierz '
                     'o rezystancji <i>R</i><sub>V</sub> dołączony do zacisków źródła '
                     'pobiera prąd <i>I</i><sub>V</sub>, który wywołuje dodatkowy spadek '
                     'napięcia na rezystancji wewnętrznej <i>R</i><sub>w</sub>.', 4)

    st += [gap(3)]
    st += [P('Prąd pobierany przez woltomierz oraz mierzone napięcie wynoszą:')]
    st += [Eq(r'$I_V = \dfrac{E}{R_w + R_V}$', tag='(2-1)')]
    st += [Eq(r'$U_V = E - I_V R_w = E\,\dfrac{R_V}{R_w + R_V} = \dfrac{E}{\dfrac{R_w}{R_V} + 1}$',
              tag='(2-2)')]
    st += [P(
        'Napięcie zmierzone jest więc mniejsze od siły elektromotorycznej o spadek napięcia '
        'na rezystancji wewnętrznej źródła. Błąd metody definiuje się jako różnicę wyniku '
        'pomiaru i wartości prawdziwej:')]
    st += [Eq(r'$\Delta_m E = U_V - E = -E\,\dfrac{R_w}{R_w + R_V} = -\dfrac{E}{1 + R_V/R_w}$',
              tag='(2-3)')]
    st += [P(
        'Błąd ten jest <b>ujemny</b> \u2013 woltomierz zawsze wskazuje mniej niż SEM źródła. '
        'Ponieważ w praktyce nie znamy wartości <i>E</i>, wygodniej jest wyrazić go przez '
        'wynik pomiaru:')]
    st += [Eq(r'$\Delta_m E = -U_V\,\dfrac{R_w}{R_V}$', tag='(2-4)')]
    st += [P(
        'a następnie skorygować wynik:')]
    st += [Eq(r'$E = U_V - \Delta_m E = U_V\left(1 + \dfrac{R_w}{R_V}\right)$', tag='(2-5)')]

    st += [gap(4)]
    st += note_box([Paragraph(
        '<b>Wniosek praktyczny.</b> Błąd metody jest tym mniejszy, im większy jest stosunek '
        '<i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>. Dla <i>R</i><sub>V</sub> \u2265 100·'
        '<i>R</i><sub>w</sub> błąd nie przekracza 1 % i w wielu pomiarach można go pominąć. '
        'Błąd metody jest systematyczny, więc nie zmniejsza go uśrednianie wielu pomiarów \u2013 '
        'należy go wyznaczyć i skorygować albo dobrać przyrząd tak, aby był pomijalny.',
        S['note'])])
    st += [P(
        'Analogiczny błąd metody występuje woltomierzu włączonym równolegle do odbiornika '
        'w obwodzie zasilanym ze źródła: woltomierz bocznikuje odbiornik i zmienia rozpływ '
        'prądów. W obu przypadkach źródłem błędu jest skończona rezystancja wewnętrzna '
        'przyrządu.')]

    # ---------------------------------------------------------- Q8
    st += Q(8, 'Wyprowadź wyrażenie na błąd metody przy pomiarze siły elektromotorycznej '
               'rzeczywistego źródła napięcia woltomierzem o skończonej rezystancji '
               'wewnętrznej.')
    st += [P(
        'Rozpatrzmy rzeczywiste źródło o SEM <i>E</i> i rezystancji wewnętrznej '
        '<i>R</i><sub>w</sub>, do którego zacisków dołączono woltomierz o rezystancji '
        '<i>R</i><sub>V</sub> (rys. 4). Prąd w obwodzie wyznacza prawo Ohma:')]
    st += [Eq(r'$I_V = \dfrac{E}{R_w + R_V}$', tag='(2-1)')]
    st += [P(
        'Napięcie na zaciskach źródła, a więc i na woltomierzu, jest równe SEM pomniejszonej '
        'o spadek napięcia na rezystancji wewnętrznej:')]
    st += [Eq(r'$U_V = E - I_V R_w = E - E\,\dfrac{R_w}{R_w + R_V} = E\,\dfrac{R_V}{R_w + R_V}$',
              tag='(2-2)')]
    st += [P('Błąd metody to różnica wskazania i wartości prawdziwej:')]
    st += [Eq(r'$\Delta_m E = U_V - E = E\left(\dfrac{R_V}{R_w + R_V} - 1\right) = '
              r'-E\,\dfrac{R_w}{R_w + R_V}$', tag='(W-4)')]
    st += [P('Dzieląc licznik i mianownik przez <i>R</i><sub>w</sub>, otrzymuje się postać:')]
    st += [Eq(r'$\Delta_m E = -E\,\dfrac{1}{1 + \dfrac{R_V}{R_w}} = -\dfrac{E}{1 + \dfrac{R_V}{R_w}}$',
              tag='(2-3)')]
    st += [P(
        'Po podzieleniu przez <i>E</i> otrzymujemy względny błąd metody:')]
    st += [Eq(r'$\delta_m E = \dfrac{\Delta_m E}{E}\cdot 100\% = -\dfrac{100\%}{1 + \dfrac{R_V}{R_w}}$',
              tag='(W-5)')]
    st += [P(
        'Znak minus oznacza, że wskazanie woltomierza jest zawsze mniejsze od SEM. Ponieważ '
        'wartość <i>E</i> nie jest znana, w praktyce błąd wyraża się przez zmierzone napięcie:')]
    st += [Eq(r'$\Delta_m E = -U_V\,\dfrac{R_w}{R_V} = -U_V\,\dfrac{R_w}{R_V}$', tag='(2-4)')]
    st += [P(
        'co wynika z rozwinięcia (2-2) w szereg dla <i>R</i><sub>w</sub>/<i>R</i><sub>V</sub> '
        '<font name="Sans">\u226a</font> 1:')]
    st += [Eq(r'$U_V = \dfrac{E}{1 + R_w/R_V} \approx E\left(1 - \dfrac{R_w}{R_V}\right) '
              r'\;\;\Rightarrow\;\; \Delta_m E \approx -E\,\dfrac{R_w}{R_V} \approx -U_V\,\dfrac{R_w}{R_V}$',
              tag='(W-6)')]
    st += [gap(3)]
    st += [P(
        'Otrzymane wyrażenie jest wystarczająco dokładne, gdy <i>R</i><sub>w</sub> '
        '\u2264 0,1·<i>R</i><sub>V</sub> (błąd przybliżenia jest wtedy mniejszy od 1 % '
        'samego błędu metody). Wynik pomiaru koryguje się, dodając wartość bezwzględną błędu:')]
    st += [Eq(r'$E = U_V - \Delta_m E = U_V\left(1 + \dfrac{R_w}{R_V}\right)$', tag='(W-7)')]
    return st


# ================================================================== CZĘŚĆ IV
def part4():
    st = []
    st += [Spacer(1, 6), PartHeading('IV', 'Niepewność pomiaru przyrządem elektromechanicznym',
                                     'pytania 9\u201311')]

    # ---------------------------------------------------------- Q9
    st += Q(9, 'Jaki parametr woltomierza magnetoelektrycznego określa niepewność pomiaru?')
    st += [P(
        'Niepewność pomiaru woltomierza elektromechanicznego określa jego <b>klasa</b> '
        '(dokładności) <i>k</i><sub>l</sub>, wyrażona w procentach, np. 0,1; 0,2; 0,5; 1. '
        'Klasa określa największy dopuszczalny błąd <b>bezwzględny</b> przyrządu, odniesiony '
        'do <b>zakresu pomiarowego</b>, a nie do wskazania:')]
    st += [Eq(r'$\Delta_{kl}U = \dfrac{k_l\,U_z}{100}$', tag='(2-8)')]
    st += [P(
        'gdzie <i>U</i><sub>z</sub> jest zakresem przyrządu. Klasa 0,5 oznacza więc, że błąd '
        'wskazania nie przekracza 0,5 % górnej wartości zakresu na każdym miejscu skali.')]
    st += [gap(3)]
    st += [P(
        'Bezwzględny błąd graniczny jest stały w całym zakresie, dlatego błąd '
        '<b>względny</b> pomiaru zależy od wskazania: przy małych napięciach jest duży, a przy '
        'wskazaniu bliskim końca zakresu \u2013 najmniejszy. Ilustruje to poniższa tabela '
        '(woltomierz klasy 0,5 o zakresie 15 V):')]
    st += [gap(2)]
    kl = [
        ['Wskazanie <i>U</i>', 'Błąd graniczny Δ<sub>kl</sub><i>U</i>', 'Błąd względny δ<i>U</i>',
         'Niepewność <i>u</i>(<i>U</i>)', 'Niepewność wzgl. <i>u</i><sub>rel</sub>'],
        ['1,5 V (10 % zakresu)', '75 mV', '5,00 %', '43,3 mV', '2,89 %'],
        ['7,5 V (50 % zakresu)', '75 mV', '1,00 %', '43,3 mV', '0,58 %'],
        ['15 V (100 % zakresu)', '75 mV', '0,50 %', '43,3 mV', '0,29 %'],
    ]
    st += [data_table(kl, [3.65 * cm, 3.25 * cm, 2.65 * cm, 3.15 * cm, 3.15 * cm],
                      align=['l', 'c', 'c', 'c', 'c'])]
    st += [gap(4)]
    st += [P(
        'Podobną rolę dla multimetrów cyfrowych odgrywa największy dopuszczalny błąd '
        'względny δ<sub>g</sub><i>U</i>, podawany jako suma składnika zależnego od zakresu '
        'i składnika zależnego od wskazania (tab. 2.1 i 2.2 instrukcji). W praktyce klasa '
        '\u2013 obok zakresu \u2013 jest tym parametrem, który przy danym wskazaniu wprost '
        'wyznacza niepewność pomiaru.')]

    # ---------------------------------------------------------- Q10
    st += Q(10, 'Podaj wzór na niepewność standardową pomiaru napięcia za pomocą woltomierza '
                'magnetoelektrycznego.')
    st += [P(
        'Największy dopuszczalny błąd bezwzględny przyrządu o klasie <i>k</i><sub>l</sub> '
        'i zakresie <i>U</i><sub>z</sub> wynosi:')]
    st += [Eq(r'$\Delta_{kl}U = \dfrac{k_l\,U_z}{100}$', tag='(2-8)')]
    st += [P(
        'Zgodnie z konwencją przyjętą w Laboratorium Podstaw Pomiarów błąd ten traktuje się '
        'jako granicę przedziału o rozkładzie jednostajnym (pomija się przy tym zdolność '
        'rozdzielczą przyrządu). Niepewność standardowa jest więc równa:')]
    st += [Eq(r'$u(U) = \dfrac{\Delta_{kl}U}{\sqrt{3}} = \dfrac{k_l\,U_z}{100\,\sqrt{3}}$',
              tag='(2-9)')]
    st += [P('a niepewność standardowa względna:')]
    st += [Eq(r'$u_{rel}(U) = \dfrac{u(U)}{U}\cdot 100\% = \dfrac{\Delta_{kl}U}{U\sqrt{3}}\cdot 100\% '
              r'= \dfrac{k_l\,U_z}{U\sqrt{3}}\,[\%]$', tag='(2-10)')]
    st += [gap(3)]
    st += [P('<b>Przykład liczbowy.</b> Woltomierz LM-3 klasy 0,5 na zakresie '
             '<i>U</i><sub>z</sub> = 15 V, wskazanie <i>U</i> = 12,00 V:')]
    st += [Eq(r'$\Delta_{kl}U = \dfrac{0{,}5\cdot 15}{100} = 75\,\mathrm{mV}\;\;\Rightarrow\;\;'
              r'u(U) = \dfrac{75}{\sqrt{3}} \approx 43\,\mathrm{mV}$')]
    st += [Eq(r'$u_{rel}(U) = \dfrac{0{,}5\cdot 15}{12{,}00\cdot\sqrt{3}} \approx 0{,}36\%$')]
    st += [P(
        'Zwraca uwagę, że niepewność <i>u</i>(<i>U</i>) nie zależy od wskazania \u2013 jest '
        'taka sama na całej skali \u2013 natomiast niepewność względna maleje ze wzrostem '
        'wskazania. Dlatego pomiar wykonuje się na zakresie możliwie bliskim mierzonej '
        'wartości.')]

    # ---------------------------------------------------------- Q11
    st += Q(11, 'Jak oblicza się niepewność standardową względną pomiaru napięcia na podstawie '
                'klasy woltomierza? Jaką minimalną wartość może mieć ta niepewność dla '
                'woltomierza klasy 0,5?')
    st += [P(
        'Niepewność standardową względną oblicza się z zależności (2-10), dzieląc błąd '
        'graniczny przez wskazanie i przez \u221a3:')]
    st += [Eq(r'$u_{rel}(U) = \dfrac{\Delta_{kl}U}{U\sqrt{3}}\cdot 100\% '
              r'= \dfrac{k_l\,U_z}{100\,U\,\sqrt{3}}\cdot 100\% = \dfrac{k_l}{\sqrt{3}}\cdot\dfrac{U_z}{U}\,[\%]$',
              tag='(2-10)')]
    st += [P(
        'Wyrażenie to osiąga minimum, gdy wskazanie jest równe końcowi zakresu '
        '(<i>U</i> = <i>U</i><sub>z</sub>). Wtedy:')]
    st += [Eq(r'$u_{rel,min}(U) = \dfrac{k_l}{\sqrt{3}}\,[\%]$', tag='(W-8)')]
    st += [P('Dla woltomierza klasy 0,5:')]
    st += [Eq(r'$u_{rel,min} = \dfrac{0{,}5}{\sqrt{3}}\,\% \approx 0{,}289\,\%$')]
    st += [gap(3)]
    st += [P(
        '<b>Odpowiedź:</b> minimalna niepewność standardowa względna woltomierza klasy 0,5 '
        'wynosi ok. <b>0,29 %</b> i występuje przy wskazaniu równym końcowi zakresu. Przy '
        'wskazaniu dwukrotnie mniejszym jest dwa razy większa (0,58 %), a przy wskazaniu '
        '10 % zakresu \u2013 dziesięć razy większa (2,89 %).')]
    st += [gap(4)]
    st += note_box([Paragraph(
        'Ponieważ niepewność względna rośnie odwrotnie proporcjonalnie do wskazania, '
        'przy pomiarach woltomierzem analogowym należy <b>dobierać zakres tak, aby wskazanie '
        'znalazło się w górnej części skali</b> \u2013 najlepiej powyżej jej połowy. '
        'Woltomierz LM-3 w ćwiczeniu obsługuje zakresy 1,5; 3; 7,5; 15; 30; 75; 150 V.',
        S['note'])])
    return st


# ================================================================== CZĘŚĆ V
def part5():
    st = []
    st += [Spacer(1, 6), PartHeading('V', 'Wyznaczanie rezystancji wewnętrznej źródła',
                                     'pytanie 12')]

    st += Q(12, 'Opisz, w jaki sposób można wyznaczyć rezystancję wewnętrzną źródła napięcia '
                'mając do dyspozycji dwa woltomierze. Jakie warunki muszą być spełnione, '
                'aby wynik był wiarygodny?')
    st += [P(
        'Pomiar wykonuje się dwoma woltomierzami o <b>znacznie różniących się</b> '
        'rezystancjach wewnętrznych <i>R</i><sub>V1</sub> i <i>R</i><sub>V2</sub>. Każdy '
        'z nich mierzy napięcie na zaciskach tego samego źródła, ale pobiera inny prąd, '
        'a więc wywołuje inny spadek napięcia na <i>R</i><sub>w</sub>. Uzyskuje się dwa '
        'równania:')]

    st += fig_block(os.path.join(FIG, 'fig05_dwa_woltomierze.png'), 16.4,
                     'Pomiar napięcia na zaciskach źródła dwoma woltomierzami: (a) '
                     'woltomierzem o dużej rezystancji <i>R</i><sub>V1</sub>, (b) '
                     'woltomierzem o małej rezystancji <i>R</i><sub>V2</sub>. Różnica '
                     'wskazań <i>U</i><sub>1</sub> i <i>U</i><sub>2</sub> jest miarą '
                     'rezystancji wewnętrznej źródła.', 5)

    st += [Eq(r'$U_1 = E\,\dfrac{R_{V1}}{R_w + R_{V1}}$', tag='(2-13)')]
    st += [Eq(r'$U_2 = E\,\dfrac{R_{V2}}{R_w + R_{V2}}$', tag='(2-14)')]
    st += [P(
        'Jest to układ dwóch równań z dwiema niewiadomymi <i>E</i> i <i>R</i><sub>w</sub>. '
        'Rozwiązując go, otrzymuje się:')]
    st += [Eq(r'$E = U_1 U_2\,\dfrac{R_{V1} - R_{V2}}{R_{V1}U_2 - R_{V2}U_1}$', tag='(2-15)')]
    st += [Eq(r'$R_w = R_{V1}R_{V2}\,\dfrac{U_1 - U_2}{R_{V1}U_2 - R_{V2}U_1}$', tag='(2-16)')]

    st += [gap(4)]
    st += [P('<b>Warunki wiarygodności wyniku:</b>')]
    st += bullets([
        '<b>Znacząca różnica wskazań.</b> Wartości <i>U</i><sub>1</sub> i <i>U</i><sub>2</sub> '
        'muszą różnić się znacznie więcej, niż wynikałoby to z ich niepewności \u2013 inaczej '
        'iloraz w (2-16) jest ilorazem dwóch małych i niepewnych liczb, a wynik traci sens '
        'fizyczny.',
        '<b>Duża różnica rezystancji woltomierzy.</b> Im większy stosunek '
        '<i>R</i><sub>V1</sub>/<i>R</i><sub>V2</sub>, tym większa różnica napięć '
        '<i>U</i><sub>1</sub> i <i>U</i><sub>2</sub>, a więc i lepsze uwarunkowanie zadania. '
        'W praktyce stosuje się np. woltomierz cyfrowy 10 MΩ i magnetoelektryczny 15 kΩ.',
        '<b>Znajomość rezystancji wewnętrznych.</b> Wartości <i>R</i><sub>V1</sub> i '
        '<i>R</i><sub>V2</sub> muszą być znane z odpowiednią dokładnością \u2013 dla woltomierza '
        'magnetoelektrycznego wyznacza się je z zależności <i>R</i><sub>V</sub> = κ·'
        '<i>U</i><sub>z</sub>.',
        '<b>Stała SEM źródła.</b> Oba pomiary muszą być wykonane przy tej samej wartości '
        '<i>E</i> i <i>R</i><sub>w</sub> \u2013 źródło nie może się rozładowywać ani nagrzewać '
        'między pomiarami.',
        '<b>Zakres woltomierza analogowego.</b> Przy pomiarze kolejnych źródeł nie zmienia się '
        'zakresu, gdyż zmiana zakresu zmienia <i>R</i><sub>V</sub>, a więc warunki pomiaru '
        '(uwaga z Zadania 2 instrukcji).',
        '<b>Pominięcie pozostałych błędów.</b> We wzorach (2-15) i (2-16) zakłada się, że '
        'różnica wskazań wynika wyłącznie z wpływu rezystancji wewnętrznych woltomierzy. '
        'Nie uwzględnia się niepewności <i>U</i><sub>1</sub>, <i>U</i><sub>2</sub>, '
        '<i>R</i><sub>V1</sub> i <i>R</i><sub>V2</sub>.',
    ])

    st += [gap(4)]
    st += [P(
        'W ćwiczeniu wyznacza się <i>R</i><sub>w</sub> źródła Źr.2 z pomiarów multimetrem '
        '34450A (<i>R</i><sub>V1</sub> = 10 MΩ) i woltomierzem LM-3 klasy 0,5 '
        '(<i>R</i><sub>V2</sub> = κ·<i>U</i><sub>z</sub> = 1 kΩ/V · <i>U</i><sub>z</sub>), '
        'korzystając dodatkowo z aplikacji Demo_02 (zakładka <i>Metoda ekstrapolacji '
        'liniowej</i>). Metoda ekstrapolacji polega na tym, że zależność napięcia od '
        'przewodności woltomierza 1/<i>R</i><sub>V</sub> jest liniowa:')]
    st += [Eq(r'$U = E - R_w\,I_V = E - E\,R_w\cdot\dfrac{1}{R_V + R_w}$', tag='(W-9)')]
    st += [P(
        'a po wykreśleniu <i>U</i> w funkcji 1/<i>R</i><sub>V</sub> i ekstrapolacji do '
        '1/<i>R</i><sub>V</sub> = 0 (czyli <i>R</i><sub>V</sub> \u2192 \u221e) wyraz wolny '
        'prostej jest równy SEM, a z nachylenia wyznacza się <i>R</i><sub>w</sub>.')]
    return st


# ================================================================== CZĘŚĆ VI
def part6():
    st = []
    st += [Spacer(1, 6), PartHeading('VI', 'Metoda kompensacyjna pomiaru SEM',
                                     'pytania 13\u201315')]

    # ---------------------------------------------------------- Q13
    st += Q(13, 'Narysuj układ do pomiaru siły elektromotorycznej źródła metodą kompensacyjną. '
                'Jakie wymagania powinny spełniać wykorzystywane w układzie woltomierze, '
                'aby błąd pomiaru był najmniejszy?')
    st += [P(
        'Metoda kompensacyjna należy do grupy <b>metod zerowych</b>. SEM badanego źródła '
        'porównuje się z napięciem znanego, regulowanego źródła wzorcowego. W stanie '
        'równowagi przez wskaźnik nie płynie prąd, więc na rezystancji wewnętrznej badanego '
        'źródła nie występuje spadek napięcia i napięcie wzorcowe jest równe SEM:')]

    st += fig_block(os.path.join(FIG, 'fig06_kompensacja.png'), 14.0,
                     'Układ do pomiaru siły elektromotorycznej źródła metodą kompensacyjną. '
                     '<i>E</i>, <i>R</i><sub>w</sub> \u2013 badane źródło; '
                     '<i>E</i><sub>wz</sub>, <i>R</i><sub>wz</sub> \u2013 regulowane źródło '
                     'wzorcowe; <b>W</b> \u2013 wskaźnik równowagi; <b>V</b> \u2013 woltomierz '
                     'mierzący napięcie wzorcowe <i>U</i><sub>wz</sub>.', 6)

    st += [gap(2)]
    st += [P('<b>Wymagania wobec przyrządów:</b>')]
    st += [gap(2)]
    wym = [
        ['Element układu', 'Wymaganie', 'Uzasadnienie'],
        ['Wskaźnik równowagi <b>W</b>',
         'bardzo duża czułość; rezystancja wewnętrzna możliwie duża',
         'precyzyjne wykrycie stanu zrównania, a po skompensowaniu \u2013 zerowy prąd '
         'i brak spadku napięcia na <i>R</i><sub>w</sub>'],
        ['Woltomierz <b>V</b> (pomiar <i>U</i><sub>wz</sub>)',
         'duża dokładność i duża rezystancja wewnętrzna',
         'dokładność <i>U</i><sub>wz</sub> bezpośrednio przenosi się na dokładność '
         'wyznaczenia <i>E</i>'],
        ['Źródło wzorcowe <i>E</i><sub>wz</sub>',
         'dowolna, ale niezbyt duża rezystancja wewnętrzna; możliwie mała i równomierna '
         'rozdzielczość regulacji',
         'napięcie <i>U</i><sub>wz</sub> powinno stabilnie i precyzyjnie równoważyć '
         '<i>E</i>; skokowa regulacja ogranicza dokładność'],
        ['Zakres woltomierza LM-3',
         'zakres tak dobrany, aby wskazanie <i>U</i><sub>wz</sub> było bliskie górnej '
         'granicy zakresu',
         'minimalna niepewność względna pomiaru napięcia (pytanie 11)'],
    ]
    st += [data_table(wym, [4.35 * cm, 5.35 * cm, 7.10 * cm], align=['l', 'l', 'l'])]
    st += [gap(4)]
    st += [P(
        'W układzie z zasilaczem E3646A rolę źródła wzorcowego pełni Wyjście 2 zasilacza, '
        'a napięcie to mierzy wewnętrzna funkcja zasilacza. Wskazaniem równowagi jest '
        'multimetr 34450A (duża rezystancja wejściowa 10 MΩ i rozdzielczość 5\u00bd cyfry), '
        'dzięki czemu prąd w stanie równowagi jest praktycznie zerowy.')]

    # ---------------------------------------------------------- Q14
    st += Q(14, 'Opisz sposób pomiaru siły elektromotorycznej źródła metodą kompensacyjną. '
                'W jakich warunkach warto stosować tę metodę?')
    st += [P('<b>Przebieg pomiaru:</b>')]
    st += [gap(2)]
    st += [P(
        '<b>1. Połączenie układu.</b> Badane źródło (<i>E</i>, <i>R</i><sub>w</sub>) łączy się '
        'szeregowo ze wskaźnikiem równowagi <b>W</b>, a następnie z regulowanym źródłem '
        'wzorcowym (<i>E</i><sub>wz</sub>, <i>R</i><sub>wz</sub>). Woltomierz <b>V</b> '
        'dołącza się równolegle do źródła wzorcowego w celu pomiaru napięcia '
        '<i>U</i><sub>wz</sub>. Należy zwrócić uwagę na biegunowość \u2013 napięcie wzorcowe '
        'musi przeciwstawiać się SEM badanego źródła.', style='body')]
    st += [gap(4)]
    st += [P(
        '<b>2. Równoważenie.</b> Zmienia się napięcie <i>U</i><sub>wz</sub> tak długo, aż '
        'wskaźnik równowagi wskaże zero. W stanie równowagi:')]
    st += [Eq(r'$E = U_{wz}$', tag='(W-10)')]
    st += [P(
        'W praktyce stan zerowy osiąga się z pewną nieczułością \u2013 przyjmuje się go, gdy '
        'napięcie niezrównoważenia jest mniejsze od założonej wartości progowej. Wartość '
        'SEM odczytuje się wtedy z woltomierza <b>V</b>, a nie z nastawy źródła wzorcowego. '
        'W programie <i>Pomiary automatyczne</i> (zakładka <i>Kompensacyjny pomiar SEM</i>) '
        'proces prowadzony jest automatycznie: do chwili zmiany znaku napięcia '
        'niezrównoważenia napięcie wzorcowe zmieniane jest skokowo, a po każdej zmianie znaku '
        'skok jest redukowany (np. o 50 %), aż do spełnienia warunku \u201edopuszczalna '
        'różnica wyników\u201d.')]
    st += [gap(4)]
    st += [P(
        '<b>3. Opracowanie niepewności.</b> Niepewność standardową pomiaru SEM wyznacza się '
        'z zależności uwzględniającej trzy składniki \u2013 niepewność pomiaru napięcia '
        'wzorcowego, rozdzielczość regulacji oraz nieczułość wskaźnika równowagi:')]
    st += [Eq(r'$u(E) = \sqrt{\left(\dfrac{\Delta_g U_{wz}}{\sqrt{3}}\right)^2 + '
              r'\left(\dfrac{\Delta U}{\sqrt{3}}\right)^2 + \left(\dfrac{\Delta U_{min}}{\sqrt{3}}\right)^2}$',
              tag='(2-17)')]
    st += [P(
        'gdzie Δ<i>U</i> = 10 mV dla zasilacza E3646A, a Δ<i>U</i><sub>min</sub> jest napięciem '
        'odpowiadającym cyfrze \u201e1\u201d na najmniej znaczącym miejscu wskaźnika '
        'równowagi.')]
    st += [gap(4)]
    st += [P('<b>Kiedy warto stosować tę metodę:</b>')]
    st += bullets([
        'gdy mamy do czynienia ze źródłem o <b>dużej rezystancji wewnętrznej</b> \u2013 '
        'metoda bezpośrednia daje wtedy duży błąd metody, a metoda kompensacyjna nie pobiera '
        'prądu w stanie równowagi i mierzy SEM bezbłędnie pod tym względem,',
        'gdy wymagana jest <b>duża dokładność</b> pomiaru SEM, np. w pomiarach ogniw '
        'wzorcowych, termoelementów czy czujników o dużym stosunku <i>R</i><sub>w</sub> do '
        'rezystancji obciążenia,',
        'gdy pomiar metodą bezpośrednią jest niemożliwy lub obarczony zbyt dużym błędem '
        '\u2013 np. dla źródeł, które nie mogą dostarczyć prądu nawet rzędu mikroamperów.',
    ])

    # ---------------------------------------------------------- Q15
    st += Q(15, 'Podaj wady i zalety metody kompensacyjnej w stosunku do metody bezpośredniej.')
    st += [gap(2)]
    zal = [
        ['', 'Metoda bezpośrednia', 'Metoda kompensacyjna'],
        ['Zasada',
         'woltomierz dołączony do zacisków źródła',
         'porównanie z napięciem wzorcowym do chwili zaniku prądu'],
        ['Błąd metody',
         'występuje \u2013 zawsze ujemny, zależny od <i>R</i><sub>w</sub>/<i>R</i><sub>V</sub>',
         'brak w stanie równowagi \u2013 z badanego źródła nie jest pobierany prąd'],
        ['Wpływ rezystancji wewnętrznej źródła',
         'wynik zależy od <i>R</i><sub>w</sub> badanego źródła',
         'wynik nie zależy od <i>R</i><sub>w</sub> badanego źródła'],
        ['Dokładność',
         'ograniczona klasą woltomierza i stosunkiem <i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>',
         'ograniczona dokładnością pomiaru napięcia wzorcowego i rozdzielczością regulacji'],
        ['Trudność i czas pomiaru',
         'prosty, szybki, jeden przyrząd',
         'złożony \u2013 wymaga źródła wzorcowego, wskaźnika równowagi i regulacji; czasochłonny'],
        ['Wrażliwość na warunki',
         'mała',
         'duża \u2013 wymaga stabilnego źródła wzorcowego i czułego wskaźnika'],
        ['Możliwość pomiaru w obwodzie',
         'łatwa, woltomierz można dołączyć do dowolnych punktów',
         'utrudniona \u2013 konieczne przerwanie obwodu i właściwa biegunowość'],
        ['Zastosowanie przy rozładowanym źródle',
         'obciąża źródło prądem woltomierza',
         'nie obciąża źródła w stanie równowagi'],
    ]
    st += [data_table(zal, [4.15 * cm, 6.2 * cm, 6.4 * cm], align=['l', 'l', 'l'])]
    st += [gap(5)]
    st += [P(
        '<b>Podsumowanie.</b> Metoda kompensacyjna jest dokładniejsza, ponieważ eliminuje błąd '
        'metody \u2013 w stanie równowagi przez badane źródło nie płynie prąd, więc mierzona '
        'jest rzeczywiście SEM, a nie napięcie zaciskowe. Jej wadą jest większa złożoność '
        'układu, konieczność stosowania źródła wzorcowego o znanym napięciu, dłuższy czas '
        'pomiaru i wrażliwość na nieczułość wskaźnika równowagi. W metodzie bezpośredniej '
        'błąd metody można wprawdzie obliczyć i skorygować, ale korekcja opiera się na '
        'znajomości <i>R</i><sub>w</sub> i <i>R</i><sub>V</sub>, a więc także wnosi '
        'niepewność.')]
    return st


# ================================================================== CZĘŚĆ VII
def part7():
    st = []
    st += [Spacer(1, 6), PartHeading('VII', 'Wpływ rezystancji wewnętrznej przyrządów',
                                     'pytania 16\u201318')]

    # ---------------------------------------------------------- Q16
    st += Q(16, 'W jaki sposób rezystancja wewnętrzna woltomierza wpływa na wynik pomiaru '
                'w przypadku: \u2013 źródła napięciowego idealnego, \u2013 źródła napięciowego '
                'rzeczywistego?')
    st += [P('<b>a) Źródło napięciowe idealne</b> (<i>R</i><sub>w</sub> = 0)')]
    st += [P(
        'Rezystancja wewnętrzna woltomierza <b>nie wpływa</b> na wynik pomiaru. Prąd pobierany '
        'przez woltomierz płynie wprawdzie przez źródło, ale nie wywołuje na nim żadnego '
        'spadku napięcia, ponieważ <i>R</i><sub>w</sub> = 0:')]
    st += [Eq(r'$U_V = E\,\dfrac{R_V}{R_w + R_V} = E\,\dfrac{R_V}{0 + R_V} = E = \mathrm{const}$')]
    st += [P(
        'Woltomierz o dowolnej rezystancji wskaże więc zawsze SEM źródła. Wartość '
        '<i>R</i><sub>V</sub> decyduje jedynie o prądzie pobieranym ze źródła '
        '(<i>I</i><sub>V</sub> = <i>E</i>/<i>R</i><sub>V</sub>) i o mocy w nim wydzielanej.')]
    st += [gap(4)]
    st += [P('<b>b) Źródło napięciowe rzeczywiste</b> (<i>R</i><sub>w</sub> &gt; 0)')]
    st += [P(
        'Rezystancja woltomierza <b>wpływa na wynik</b>, i to tym silniej, im mniejszy jest '
        'stosunek <i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>. Woltomierz pobiera prąd '
        '<i>I</i><sub>V</sub> = <i>E</i>/(<i>R</i><sub>w</sub> + <i>R</i><sub>V</sub>), który '
        'wywołuje spadek napięcia na rezystancji wewnętrznej źródła:')]
    st += [Eq(r'$U_V = E\,\dfrac{R_V}{R_w + R_V} = E\,\dfrac{1}{1 + \dfrac{R_w}{R_V}}$')]
    st += [P(
        'Wynik jest więc zawsze mniejszy od <i>E</i> (błąd metody ujemny), a jedynie dla '
        '<i>R</i><sub>V</sub> <font name="Sans">\u226b</font> <i>R</i><sub>w</sub> zbliża się do SEM. Zależność '
        'względnego wyniku <i>U</i><sub>V</sub>/<i>E</i> od stosunku '
        '<i>R</i><sub>V</sub>/<i>R</i><sub>w</sub> przedstawiono na rysunku:')]

    st += fig_block(os.path.join(FIG, 'fig07_wplyw_rv.png'), 12.0,
                     'Wpływ rezystancji woltomierza na wynik pomiaru: dla źródła idealnego '
                     'wynik nie zależy od <i>R</i><sub>V</sub>, dla źródła rzeczywistego '
                     'względny wynik rośnie od zera do 100 % wraz ze wzrostem stosunku '
                     '<i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>.', 7)

    st += [gap(2)]
    tabela = [
        ['Stosunek <i>R</i><sub>V</sub>/<i>R</i><sub>w</sub>', '0,01', '0,1', '1', '10', '100', '1000'],
        ['Wynik <i>U</i><sub>V</sub>/<i>E</i>', '1,0 %', '9,1 %', '50,0 %', '90,9 %', '99,0 %', '99,9 %'],
        ['Błąd metody Δ<sub>m</sub><i>E</i>/<i>E</i>', '\u221299,0 %', '\u221290,9 %', '\u221250,0 %',
         '\u22129,1 %', '\u22121,0 %', '\u22120,1 %'],
    ]
    st += [data_table(tabela, [4.65 * cm, 2.03 * cm, 2.03 * cm, 2.03 * cm, 2.03 * cm,
                              2.03 * cm, 2.03 * cm], align=['l', 'c', 'c', 'c', 'c', 'c', 'c'])]
    st += [gap(4)]
    st += [P(
        '<b>Wniosek.</b> Woltomierz o dostatecznie dużej rezystancji wewnętrznej pozwala '
        'zmierzyć SEM źródła rzeczywistego z pomijalnym błędem metody. Jeżeli warunek '
        '<i>R</i><sub>V</sub> <font name="Sans">\u226b</font> <i>R</i><sub>w</sub> nie może być spełniony, błąd metody '
        'należy obliczyć z wzoru (2-3) i skorygować wynik. Dla bardzo dużych <i>R</i><sub>w</sub> '
        '(rzędu megaomów) żaden woltomierz nie zapewni wymaganej dokładności i trzeba '
        'zastosować metodę kompensacyjną.')]

    # ---------------------------------------------------------- Q17
    st += Q(17, 'Jaką wartość wskaże woltomierz o rezystancji wewnętrznej 10 kΩ mierzący '
                'napięcie na zaciskach źródła napięciowego rzeczywistego o rezystancji 10 kΩ, '
                'jeżeli siła elektromotoryczna źródła wynosi 10 V?')
    st += [P('Dane: <i>R</i><sub>V</sub> = 10 kΩ, <i>R</i><sub>w</sub> = 10 kΩ, '
             '<i>E</i> = 10 V.')]
    st += [P(
        'Woltomierz dołączony do zacisków źródła tworzy z jego rezystancją wewnętrzną dzielnik '
        'napięcia. Napięcie mierzone opisuje wzór (2-2):')]
    st += [Eq(r'$U_V = E\,\dfrac{R_V}{R_w + R_V} = 10\,\mathrm{V}\cdot\dfrac{10\,\mathrm{k}\Omega}'
              r'{10\,\mathrm{k}\Omega + 10\,\mathrm{k}\Omega} = 10\,\mathrm{V}\cdot 0{,}5 = 5{,}00\,\mathrm{V}$')]
    st += [P('<b>Odpowiedź: woltomierz wskaże 5,00 V</b>, czyli połowę siły elektromotorycznej.')]
    st += [gap(2)]
    st += [P(
        'Warto zauważyć, że błąd metody jest w tym przypadku ogromny:')]
    st += [Eq(r'$\Delta_m E = U_V - E = 5{,}00 - 10 = -5{,}00\,\mathrm{V}'
              r'\;\;\Rightarrow\;\; \delta_m E = -50\%$')]
    st += [P(
        'Dzieje się tak, ponieważ rezystancja woltomierza jest równa rezystancji wewnętrznej '
        'źródła (<i>R</i><sub>V</sub>/<i>R</i><sub>w</sub> = 1). Po korekcji '
        'z wzoru (2-5) otrzymuje się poprawną wartość:')]
    st += [Eq(r'$E = U_V\left(1 + \dfrac{R_w}{R_V}\right) = 5{,}00\,\mathrm{V}\cdot(1 + 1) = 10{,}0\,\mathrm{V}$')]

    # ---------------------------------------------------------- Q18
    st += Q(18, 'Jaką rezystancją wewnętrzną powinien charakteryzować się woltomierz idealny, '
                'a jaką amperomierz idealny?')
    st += [gap(2)]
    ideal = [
        ['Przyrząd', '<i>R</i><sub>we</sub>', 'Wpływ na obwód', 'Uzasadnienie'],
        ['Woltomierz idealny', '<i>R</i><sub>V</sub> \u2192 \u221e (nieskończenie duża)',
         'nie pobiera prądu z obwodu',
         'woltomierz mierzy napięcie, dołączony równolegle; prąd '
         '<i>I</i><sub>V</sub> = <i>U</i>/<i>R</i><sub>V</sub> \u2192 0, więc jego włączenie '
         'nie zmienia rozpływu prądów'],
        ['Amperomierz idealny', '<i>R</i><sub>A</sub> \u2192 0 (zerowa)',
         'nie wprowadza spadku napięcia',
         'amperomierz mierzy prąd, dołączony szeregowo; spadek napięcia '
         '<i>U</i><sub>A</sub> = <i>I</i>·<i>R</i><sub>A</sub> \u2192 0, więc jego włączenie '
         'nie zmienia prądu w obwodzie'],
    ]
    st += [data_table(ideal, [3.15 * cm, 4.15 * cm, 3.55 * cm, 5.95 * cm],
                      align=['l', 'l', 'l', 'l'])]
    st += [gap(4)]
    st += [P(
        'Takie wartości wynikają z ogólnej zasady: <b>przyrząd pomiarowy powinien w jak '
        'najmniejszym stopniu zmieniać stan obwodu</b>, w którym dokonuje pomiaru. Dla '
        'woltomierza oznacza to minimalny prąd pobierany (maksymalna rezystancja), a dla '
        'amperomierza \u2013 minimalny spadek napięcia (minimalna rezystancja). Oba warunki '
        'są jednocześnie optymalne dla pomiaru mocy: woltomierz o <i>R</i><sub>V</sub> \u2192 \u221e '
        'i amperomierz o <i>R</i><sub>A</sub> \u2192 0 nie pobierają energii z obwodu.')]
    st += [gap(3)]
    st += [P(
        'W rzeczywistych przyrządach rezystancje te mają wartości skończone i niezerowe, '
        'dlatego mówi się o przyrządach \u201eprawie idealnych\u201d: multimetr cyfrowy '
        'o 10 MΩ rezystancji wejściowej jest w większości zastosowań \u201eprawie idealnym\u201d '
        'woltomierzem, a amperomierz o rezystancji kilku omów \u2013 \u201eprawie idealnym\u201d '
        'amperomierzem dla obwodów o rezystancji rzędu kiloomów.')]
    st += [gap(3)]
    st += note_box([Paragraph(
        'Zależność jest symetryczna wobec zasady Thevenina: woltomierz mierzy napięcie na '
        'dzielniku <i>R</i><sub>w</sub>/<i>R</i><sub>V</sub>, więc do pomiaru SEM źródła '
        'rzeczywistego potrzeba <i>R</i><sub>V</sub> <font name="Sans">\u226b</font> <i>R</i><sub>w</sub>; '
        'amperomierz mierzy prąd ograniczony rezystancją <i>R</i><sub>A</sub>, więc do pomiaru '
        'prądu potrzeba <i>R</i><sub>A</sub> <font name="Sans">\u226a</font> <i>R</i><sub>obc</sub>.', S['note'])])
    return st


# ================================================================== CZĘŚĆ VIII
def part8():
    st = []
    st += [Spacer(1, 6), PartHeading('VIII', 'Zadania rachunkowe', 'pytania 19\u201322')]

    # ---------------------------------------------------------- Q19
    st += Q(19, 'Zmierzono napięcie na zaciskach źródła rzeczywistego, którego siła '
                'elektromotoryczna wynosi E = 5 V. Uzyskano wynik U = 2,500 V. Ile wynosi '
                'rezystancja wewnętrzna źródła, jeśli rezystancja woltomierza wynosi 100 kΩ?')
    st += [P('Dane: <i>E</i> = 5 V, <i>U</i> = 2,500 V, <i>R</i><sub>V</sub> = 100 kΩ.')]
    st += [P(
        'Woltomierz dołączony do zacisków źródła tworzy z rezystancją wewnętrzną źródła '
        'dzielnik napięcia. Z prawa Ohma dla obwodu z rys. 4 płynie prąd:')]
    st += [Eq(r'$I_V = \dfrac{E - U}{R_w}$', tag='(W-11)')]
    st += [P('a zarazem przez woltomierz płynie prąd:')]
    st += [Eq(r'$I_V = \dfrac{U}{R_V}$', tag='(W-12)')]
    st += [P('Przyrównując oba wyrażenia, otrzymuje się:')]
    st += [Eq(r'$\dfrac{E - U}{R_w} = \dfrac{U}{R_V}\;\;\Rightarrow\;\; '
              r'$R_w = R_V\,\dfrac{E - U}{U} = R_V\left(\dfrac{E}{U} - 1\right)$', tag='(W-13)')]
    st += [P('Po podstawieniu danych:')]
    st += [Eq(r'$R_w = 100\,\mathrm{k}\Omega\cdot\dfrac{5 - 2{,}500}{2{,}500} = '
              r'$100\,\mathrm{k}\Omega\cdot 1 = 100\,\mathrm{k}\Omega$')]
    st += [P('<b>Odpowiedź: rezystancja wewnętrzna źródła wynosi 100 kΩ.</b>')]
    st += [gap(3)]
    st += [P(
        '<b>Sprawdzenie.</b> Prąd woltomierza <i>I</i><sub>V</sub> = 2,500 V / 100 kΩ = 25 µA. '
        'Spadek napięcia na rezystancji wewnętrznej źródła wynosi '
        '<i>I</i><sub>V</sub>·<i>R</i><sub>w</sub> = 25 µA · 100 kΩ = 2,500 V, a więc '
        '<i>E</i> = <i>U</i> + <i>I</i><sub>V</sub><i>R</i><sub>w</sub> = 2,500 + 2,500 = 5,000 V '
        '\u2013 zgodnie z danymi.')]
    st += [gap(3)]
    st += [P(
        '<b>Uwaga.</b> Wynik jest bardzo czuły na dokładność pomiaru napięcia: dla '
        '<i>U</i> = 2,500 V stosunek <i>E</i>/<i>U</i> = 2, a dla <i>U</i> = 2,55 V wynosi już '
        '1,96, co daje <i>R</i><sub>w</sub> = 96 kΩ. W tego typu zadaniach \
        rezystancja woltomierza musi być znana, a napięcie mierzone z dużą dokładnością.')]
    st += [gap(3)]
    st += note_box([Paragraph(
        '<b>Postać ogólna.</b> Zadanie jest szczególnym przypadkiem zależności (2-2). '
        'Wyznaczona z niej rezystancja wewnętrzna źródła wynosi '
        '<i>R</i><sub>w</sub> = <i>R</i><sub>V</sub>(<i>E</i>/<i>U</i> \u2212 1) i można ją '
        'obliczyć pojedynczym pomiarem, jeżeli znane są <i>E</i> i <i>R</i><sub>V</sub>. '
        'Gdy <i>E</i> nie jest znane, trzeba zastosować metodę dwóch woltomierzy '
        '(pytanie 12).', S['note'])], bar=GREY)

    # ---------------------------------------------------------- Q20
    st += Q(20, 'Zmierzono natężenie prądu za pomocą amperomierza. Uzyskano wynik I = 10,000 mA '
                'na zakresie I<sub>z</sub> = 50 mA. Oblicz niepewność standardową względną '
                'pomiaru, jeśli największy dopuszczalny błąd względny pomiaru jest wyrażony '
                'wzorem δ<sub>gI</sub> = 0,05 % + 0,02 %·I<sub>z</sub>/I.')
    st += [P('Dane: <i>I</i> = 10,000 mA, <i>I</i><sub>z</sub> = 50 mA.')]
    st += [P('Największy dopuszczalny błąd względny pomiaru:')]
    st += [Eq(r'$\delta_{gI} = 0{,}05\% + 0{,}02\%\cdot\dfrac{I_z}{I} = 0{,}05\% + '
              r'$0{,}02\%\cdot\dfrac{50}{10} = 0{,}05\% + 0{,}10\% = 0{,}15\%$')]
    st += [P(
        'Niepewność standardową względną oblicza się, dzieląc błąd graniczny przez \u221a3 '
        '(rozkład jednostajny, wzór 2-7):')]
    st += [Eq(r'$u_{rel}(I) = \dfrac{\delta_{gI}}{\sqrt{3}} = \dfrac{0{,}15\%}{\sqrt{3}} '
              r'\approx 0{,}0866\% \approx 0{,}087\%$', tag='(2-7)')]
    st += [P('<b>Odpowiedź: niepewność standardowa względna wynosi ok. 0,087 %.</b>')]
    st += [gap(3)]
    st += [P(
        'Dla pełności obliczeń można podać niepewność bezwzględną i zapis wyniku:')]
    st += [Eq(r'$u(I) = u_{rel}(I)\cdot I = 0{,}000866\cdot 10{,}000\,\mathrm{mA} '
              r'\approx 0{,}0087\,\mathrm{mA}$')]
    st += [Eq(r'$I = (10{,}000 \pm 0{,}009)\,\mathrm{mA}\;\;\;(k = 1)$')]
    st += [gap(3)]
    st += [P(
        'Zwraca uwagę, że składnik zależny od zakresu (0,02 % · <i>I</i><sub>z</sub>/<i>I</i> '
        '= 0,10 %) jest dwa razy większy od składnika stałego (0,05 %). Wynika to z małego '
        'wykorzystania zakresu \u2013 mierzony prąd stanowi zaledwie 20 % zakresu. Przy '
        'pomiarze na zakresie 50 mA korzystniej byłoby użyć zakresu mniejszego, np. 10 mA, '
        'gdyż wtedy udział składnika zakresowego zmalałby pięciokrotnie.')]
    st += [gap(3)]
    st += note_box([Paragraph(
        '<b>Interpretacja wyniku.</b> Niepewność 0,087 % (dla <i>k</i> = 1) oznacza, że '
        'przedział <i>I</i> \u00b1 0,009 mA obejmuje wartość prawdziwą z prawdopodobieństwem '
        'ok. 68 %, a przedział <i>I</i> \u00b1 0,017 mA (dla <i>k</i> = 2) \u2013 z '
        'prawdopodobieństwem ok. 95 %.', S['note'])], bar=GREY)

    # ---------------------------------------------------------- Q21
    st += Q(21, 'Zmierzono prąd metodą pośrednią poprzez pomiar spadku napięcia na rezystorze '
                'o wartości R = 10 kΩ. Woltomierz wskazał wartość U = 10,000 V na zakresie '
                'U<sub>z</sub> = 20 V. Podaj wartość prądu oraz niepewność standardową względną '
                'wyznaczenia tej wartości, jeśli największy dopuszczalny błąd względny pomiaru '
                'napięcia wyraża się zależnością δ<sub>gU</sub> = 0,05 % + 0,01 %·U<sub>z</sub>/U, '
                'a tolerancja rezystora wynosi 0,1 %.')
    st += [P('Dane: <i>R</i> = 10 kΩ (tolerancja 0,1 %), <i>U</i> = 10,000 V, '
             '<i>U</i><sub>z</sub> = 20 V.')]
    st += [P('<b>1. Wartość prądu</b> \u2013 z prawa Ohma dla metody pośredniej:')]
    st += [Eq(r'$I = \dfrac{U}{R} = \dfrac{10{,}000\,\mathrm{V}}{10\,\mathrm{k}\Omega} = '
              r'$1{,}0000\,\mathrm{mA}$')]
    st += [P('<b>2. Błąd graniczny i niepewność pomiaru napięcia</b>:')]
    st += [Eq(r'$\delta_{gU} = 0{,}05\% + 0{,}01\%\cdot\dfrac{U_z}{U} = 0{,}05\% + '
              r'$0{,}01\%\cdot\dfrac{20}{10} = 0{,}05\% + 0{,}02\% = 0{,}07\%$')]
    st += [Eq(r'$u_{rel}(U) = \dfrac{\delta_{gU}}{\sqrt{3}} = \dfrac{0{,}07\%}{\sqrt{3}} '
              r'\approx 0{,}0404\%$')]
    st += [P(
        '<b>3. Niepewność rezystora.</b> Rezystor jest elementem wzorcowym o znanej tolerancji, '
        'więc zgodnie z instrukcją (rozkład normalny) przyjmuje się:')]
    st += [Eq(r'$\delta_{gR} = 0{,}1\%\;\;\Rightarrow\;\;u_{rel}(R) = \dfrac{0{,}1\%}{3} '
              r'\approx 0{,}0333\%$', tag='(2-12)')]
    st += [P(
        '<b>4. Niepewność złożona prądu.</b> Prąd jest ilorazem napięcia i rezystancji, '
        'więc niepewności względne sumują się geometrycznie:')]
    st += [Eq(r'$u_{rel}(I) = \sqrt{u_{rel}^2(U) + u_{rel}^2(R)} = \sqrt{(0{,}0404\%)^2 + '
              r'$(0{,}0333\%)^2} \approx \sqrt{0{,}00163 + 0{,}00111}\,\% \approx 0{,}052\%$')]
    st += [P('<b>Odpowiedź: <i>I</i> = 1,0000 mA, niepewność standardowa względna ok. 0,052 %.</b>')]
    st += [Eq(r'$u(I) = 0{,}00052\cdot 1{,}0000\,\mathrm{mA} \approx 0{,}00052\,\mathrm{mA} '
              r'\approx 0{,}52\,\mu\mathrm{A}$')]
    st += [Eq(r'$I = (1{,}0000 \pm 0{,}0005)\,\mathrm{mA}\;\;\;(k = 1)$')]
    st += [gap(3)]
    st += [P(
        'Wkład pomiaru napięcia (0,040 %) i tolerancji rezystora (0,033 %) jest porównywalny \u2013 '
        'żaden z nich nie dominuje. O niepewności wyniku decydują więc oba elementy, co jest '
        'sytuacją typową dla metody pośredniej o zrównoważonych składnikach.')]

    # ---------------------------------------------------------- Q22
    st += Q(22, 'Zmierzono siłę elektromotoryczną źródła metodą kompensacyjną. Uzyskano wynik '
                'U = 10,000 V na zakresie U<sub>z</sub> = 30 V. Oblicz niepewność standardową '
                'u(U) tego pomiaru, jeśli napięcie wzorcowe zmierzono woltomierzem, którego '
                'największy dopuszczalny błąd względny pomiaru wyraża się zależnością '
                'δ<sub>gU</sub> = 0,01 % + 0,01 %·U<sub>z</sub>/U, rozdzielczość regulacji '
                'napięcia wzorcowego wynosi ΔU = 0,1 mV, a najmniejsza możliwa do odczytania '
                'wartość napięcia na wskaźniku równowagi jest równa ΔU<sub>min</sub> = 0,01 mV.')
    st += [P('Dane: <i>U</i><sub>wz</sub> \u2248 <i>U</i> = 10,000 V, <i>U</i><sub>z</sub> = 30 V, '
             'Δ<i>U</i> = 0,1 mV, Δ<i>U</i><sub>min</sub> = 0,01 mV.')]
    st += [P(
        '<b>1. Błąd graniczny pomiaru napięcia wzorcowego</b>:')]
    st += [Eq(r'$\delta_{gU_{wz}} = 0{,}01\% + 0{,}01\%\cdot\dfrac{U_z}{U} = 0{,}01\% + '
              r'$0{,}01\%\cdot\dfrac{30}{10} = 0{,}01\% + 0{,}03\% = 0{,}04\%$')]
    st += [Eq(r'$\Delta_g U_{wz} = \delta_{gU_{wz}}\cdot U_{wz} = 0{,}0004\cdot 10\,\mathrm{V} '
              r'= 4\,\mathrm{mV} = 0{,}004\,\mathrm{V}$')]
    st += [P(
        '<b>2. Niepewność standardowa</b> według wzoru (2-17), z trzema składnikami '
        '(wszystkie o rozkładzie jednostajnym):')]
    st += [Eq(r'$u(E) = \sqrt{\left(\dfrac{\Delta_g U_{wz}}{\sqrt{3}}\right)^2 + '
              r'\left(\dfrac{\Delta U}{\sqrt{3}}\right)^2 + \left(\dfrac{\Delta U_{min}}{\sqrt{3}}\right)^2}$',
              tag='(2-17)')]
    st += [Eq(r'$u(E) = \sqrt{\dfrac{(4\,\mathrm{mV})^2 + (0{,}1\,\mathrm{mV})^2 + '
              r'$(0{,}01\,\mathrm{mV})^2}{3}} = \sqrt{\dfrac{16 + 0{,}01 + 0{,}0001}{3}}\,\mathrm{mV}$')]
    st += [Eq(r'$u(E) = \sqrt{5{,}337}\,\mathrm{mV} \approx 2{,}31\,\mathrm{mV}$')]
    st += [P('<b>Odpowiedź: niepewność standardowa pomiaru SEM wynosi ok. 2,31 mV.</b>')]
    st += [Eq(r'$u_{rel}(E) = \dfrac{u(E)}{U_{wz}}\cdot 100\% = \dfrac{2{,}31\,\mathrm{mV}}'
              r'{10{,}000\,\mathrm{V}}\cdot 100\% \approx 0{,}023\%$', tag='(2-18)')]
    st += [Eq(r'$E = (10{,}000 \pm 0{,}002)\,\mathrm{V}\;\;\;(k = 1)$')]
    st += [gap(3)]
    st += [P(
        'Decydujący jest pierwszy składnik \u2013 niepewność pomiaru napięcia wzorcowego. '
        'Składniki związane z rozdzielczością regulacji (0,1 mV) i nieczułością wskaźnika '
        '(0,01 mV) są ponad dwadzieścia razy mniejsze i praktycznie nie wpływają na wynik. '
        'Aby zmniejszyć niepewność pomiaru, należałoby zastosować dokładniejszy woltomierz '
        'do pomiaru napięcia wzorcowego lub mniejszy zakres (przy zakresie 10 V zamiast 30 V '
        'błąd graniczny zmalałby do 0,02 %).')]
    st += [gap(3)]
    st += note_box([Paragraph(
        '<b>Spostrzeżenie.</b> Dobór przyrządów ma tu kluczowe znaczenie (Zadanie 3 '
        'instrukcji: \u201edobrać przyrządy pomiarowe w taki sposób, aby niepewność pomiaru '
        'była najmniejsza\u201d). W metodzie kompensacyjnej dokładność wyniku jest wprost '
        'ograniczona dokładnością pomiaru napięcia wzorcowego, dlatego woltomierz mierzący '
        '<i>U</i><sub>wz</sub> powinien być najdokładniejszym przyrządem w układzie.',
        S['note'])], bar=GREY)
    return st


# ================================================================== ZESTAWIENIE
def summary():
    st = [Spacer(1, 10), PageBreak()]
    st += [Paragraph('Zestawienie wyników zadań rachunkowych', ParagraphStyle(
        'h2', fontName='Sans-Bold', fontSize=13.6, leading=17, textColor=NAVY,
        spaceAfter=2))]
    st += [Paragraph('pytania 17 oraz 19\u201322', S['part_sub'])]
    st += [gap(2)]
    st += [P(
        'W tabeli zestawiono wartości liczbowe otrzymane przy założeniach podanych w treści '
        'zadań. Niepewności podano dla <i>k</i> = 1 (jedno odchylenie standardowe).')]
    st += [gap(4)]

    rows = [
        ['Pyt.', 'Wielkość wyznaczana', 'Związek', 'Wynik'],
        ['17', 'napięcie na zaciskach źródła rzeczywistego',
         '<i>U</i><sub>V</sub> = <i>E</i>·<i>R</i><sub>V</sub>/(<i>R</i><sub>w</sub> + <i>R</i><sub>V</sub>)',
         '<b>5,00 V</b>'],
        ['19', 'rezystancja wewnętrzna źródła',
         '<i>R</i><sub>w</sub> = <i>R</i><sub>V</sub>(<i>E</i>/<i>U</i> \u2212 1)',
         '<b>100 kΩ</b>'],
        ['20', 'niepewność względna pomiaru prądu, δ<sub>g</sub> = 0,15 %',
         '<i>u</i><sub>rel</sub> = δ<sub>g</sub>/√3',
         '<b>0,087 %</b> (0,0087 mA)'],
        ['21', 'prąd wyznaczany metodą pośrednią',
         '<i>I</i> = <i>U</i>/<i>R</i>',
         '<b>1,0000 mA</b>'],
        ['21', 'niepewność względna prądu',
         '\u221a(<i>u</i><sub>rel</sub><sup>2</sup>(<i>U</i>) + <i>u</i><sub>rel</sub><sup>2</sup>(<i>R</i>))',
         '<b>0,052 %</b> (0,00052 mA)'],
        ['22', 'niepewność standardowa SEM',
         'wzór (2-17)',
         '<b>2,31 mV</b> (0,023 %)'],
    ]
    st += [data_table(rows, [1.30 * cm, 5.65 * cm, 5.70 * cm, 4.15 * cm],
                      align=['c', 'l', 'c', 'c'])]
    st += [gap(9)]

    st += [Paragraph('Uwagi końcowe', S['part'])]
    st += [P(
        '<b>1. Błąd metody a niepewność.</b> Błąd metody (pytania 7, 8, 16) jest błędem '
        'systematycznym \u2013 jego wartość można obliczyć i skorygować, np. wzorem (2-5). '
        'Niepewność (pytania 9\u201311, 20\u201322) charakteryzuje rozrzut wyniku i nie '
        'zmniejsza się przez korekcję błędów systematycznych.')]
    st += [P(
        '<b>2. Dobór zakresu.</b> Dla przyrządów o stałym błędzie granicznym odniesionym do '
        'zakresu (woltomierz magnetoelektryczny) niepewność względna jest najmniejsza przy '
        'wskazaniu bliskim końca zakresu \u2013 dlatego zakres dobiera się tuż powyżej '
        'mierzonej wartości.')]
    st += [P(
        '<b>3. Rezystancja wewnętrzna przyrządów.</b> Woltomierz powinien mieć '
        '<i>R</i><sub>V</sub> <font name="Sans">\u226b</font> <i>R</i><sub>w</sub>, a amperomierz <i>R</i><sub>A</sub> '
        '<font name="Sans">\u226a</font> <i>R</i><sub>obc</sub>. Gdy warunek ten nie jest spełniony, wynik obarczony '
        'jest błędem metody, który należy wyznaczyć i skorygować.')]
    st += [P(
        '<b>4. Metoda kompensacyjna.</b> Eliminuje błąd metody związany z poborem prądu, ale '
        'wprowadza własne ograniczenia: dokładność pomiaru napięcia wzorcowego, rozdzielczość '
        'regulacji i nieczułość wskaźnika równowagi \u2013 ujęte wzorem (2-17).')]
    return st


# ================================================================== MAIN
def main():
    from reportlab.platypus import BaseDocTemplate
    story = []

    # okładka
    story += [gap(1)]
    story += [Spacer(1, 18.4 * cm)]
    cover_note = Paragraph(
        'Dokument zawiera komplet odpowiedzi, wyprowadzenia wzorów, schematy układów '
        'pomiarowych oraz rozwiązania zadań rachunkowych wraz z analizą niepewności.',
        ParagraphStyle('cn', fontName='Serif', fontSize=10.2, leading=15.5,
                       textColor=colors.HexColor('#2a3644'),
                       alignment=0))
    cztery = Table([[cover_note]], colWidths=[CONTENT_W])
    cztery.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT),
        ('LINEBEFORE', (0, 0), (0, -1), 2.4, ACCENT),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
    ]))
    story += [cztery]

    story += intro()
    story += part1()
    story += part2()
    story += part3()
    story += part4()
    story += part5()
    story += part6()
    story += part7()
    story += part8()
    story += summary()

    K.Doc.cover_draw = draw_cover
    doc = K.Doc(OUT)
    # okładka rysowana przez onPage szablonu 'cover'
    from pdfkit import NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    return OUT


if __name__ == '__main__':
    p = main()
    print('OK:', p, os.path.getsize(p), 'B')
