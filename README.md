# Ćwiczenie T2 – odpowiedzi na pytania kontrolne

Opracowanie odpowiedzi na 22 pytania kontrolne do ćwiczenia **T2 „Pomiary napięć i prądów stałych”**
(Laboratorium Podstaw Pomiarów, ISE WEiTI PW; instrukcja v. 2.4 z 20.10.2023).

## Pliki wynikowe

| Plik | Strony | Do czego |
|---|---|---|
| `Cwiczenie_T2_-_odpowiedzi_na_pytania_kontrolne.pdf` | 21 | pełne opracowanie: wyprowadzenia, schematy, wszystkie rachunki |
| `Cwiczenie_T2_-_sciaga.pdf` | 4 | wersja skrócona – szybka powtórka przed zaliczeniem |
| `Cwiczenie_T2_-_zeszyt_cwiczen.pdf` | 12 | zeszyt ćwiczeń: gotowy protokół na zajęcia + zadania domowe |
| `kalkulator.html` | — | interaktywny kalkulator niepewności (HTML, bez zależności) |

Dokument zawiera:

- stronę tytułową ze spisem części,
- wprowadzenie z tabelą oznaczeń i opisem sposobu wyznaczania niepewności,
- odpowiedzi na wszystkie 22 pytania, pogrupowane w 8 części tematycznych,
- 7 rysunków autorskich (schematy układów pomiarowych, charakterystyki, wykres wpływu
  rezystancji woltomierza),
- pełne wyprowadzenia wzorów oraz rozwiązania zadań rachunkowych z analizą niepewności,
- tabelę zbiorczą wyników zadań 17 oraz 19–22,
- zakładki PDF (panel spisu treści) dla każdego pytania.

Numery wzorów w nawiasach, np. (2-2) lub (2-17), odpowiadają numeracji z instrukcji
do ćwiczenia. Wzory oznaczone (W-*n*) są zależnościami pomocniczymi wyprowadzonymi
w opracowaniu.

## Wersja skrócona (ściąga, 4 strony)

`Cwiczenie_T2_-_sciaga.pdf` – gęsty układ dwukolumnowy do wydruku:

1. **s. 1** – źródło napięcia (idealne vs rzeczywiste), woltomierze, błąd metody
   z pełnym wyprowadzeniem + zbiorcza „ściąga wzorów” (13 wzorów w jednej tabeli),
2. **s. 2** – niepewność (klasa przyrządu, tabela dla zakresu 15 V), dwa woltomierze,
   metoda kompensacyjna, rząd wielkości *R*<sub>w</sub> w praktyce + reguła decyzyjna,
3. **s. 3** – wpływ *R*<sub>V</sub> na wynik (tabela + wykresy), komplet obliczeń
   zadań 17 i 19–22, tabela wyników,
4. **s. 4** – autotest (10 pytań), liczby do zapamiętania, najczęstsze pułapki.

## Zeszyt ćwiczeń (12 stron)

`Cwiczenie_T2_-_zeszyt_cwiczen.pdf` – dokument do zabrania na zajęcia i wypełnienia:

1. **s. 1** – strona tytułowa z danymi identyfikacyjnymi i mapą dokumentu,
2. **s. 2–3** – Zadanie 1: ustawienia układu, tabela 5 pomiarów (U, I, I<sub>obl</sub>,
   niepewności), przykład rachunkowy, miejsce na wykres z aplikacji `Porównywanie wyników`,
3. **s. 4–5** – Zadanie 2: dobór zakresu LM-3, tabela napięć na trzech źródłach,
   ocena jakościowa źródeł, wyznaczenie *R*<sub>w</sub> i korekcja wzorem (2-5),
4. **s. 6–7** – Zadanie 3: uzasadnienie doboru przyrządów, tabela kolejnych *U*<sub>wz</sub>
   przy równoważeniu, wynik z niepewnością (2-17)/(2-18), porównanie z metodą bezpośrednią,
5. **s. 8** – pełne wyprowadzenie wzorów (2-15) i (2-16) z dyskusją założeń,
6. **s. 9** – analiza niepewności metody dwóch woltomierzy: czułości ∂*R*<sub>w</sub>/∂ln*x*,
   budżet niepewności, wnioski o dominacji *U*<sub>2</sub> (2,1 % — patrz niżej),
7. **s. 10–11** – zadania domowe 1 i 2 z rozwiązaniami wzorcowymi i tabelami wyników
   dla kolejnych wartości *E*,
8. **s. 12** – lista kontrolna przed oddaniem protokołu (10 punktów).

Każda tabela protokołu ma **puste wiersze o wysokości 0,86 cm** (do wpisu odręcznego)
i z góry rozplanowane kolumny obliczeniowe, żeby dało się je wypełniać po kolei na
zajęciach. Komentarze pod tabelami podają, czego prowadzący szuka w danym miejscu.

## Kalkulator (`kalkulator.html`)

Samodzielny plik HTML (bez zależności zewnętrznych) – otwiera się podwójnym kliknięciem.
Pięć zakładek:

| Zakładka | Co liczy |
|---|---|
| 1 · Niepewność przyrządu | δ<sub>g</sub>, Δ<sub>g</sub>, *u*, *u*<sub>rel</sub> dla klasy, multimetru cyfrowego (a % + b %·U<sub>z</sub>/U) i elementu wzorcowego; tabela dla 10…100 % zakresu |
| 2 · Błąd metody / SEM | *U*<sub>V</sub>, Δ<sub>m</sub>*E*, korekcja *E* = *U*<sub>V</sub>(1 + *R*<sub>w</sub>/*R*<sub>V</sub>), tabela 8 wartości *R*<sub>V</sub>/*R*<sub>w</sub> |
| 3 · Dwa woltomierze | *E* i *R*<sub>w</sub> z (2-15)/(2-16) + **budżet niepewności z pochodnymi analitycznymi** |
| 4 · Kompensacja | (2-17)/(2-18) z rozpadem na trzy składniki i udziałami procentowymi |
| 5 · Dobór zakresu LM-3 | porównanie wszystkich 7 zakresów: δ, *u*, *R*<sub>V</sub>, błąd metody, rekomendacja |

Zakładka 3 odtwarza wynik z §„Niepewność metody dwóch woltomierzy”: dla *E* = 10 V,
*R*<sub>w</sub> = 10 kΩ, *R*<sub>V1</sub> = 10 MΩ, *R*<sub>V2</sub> = 15 kΩ daje
**u(*R*<sub>w</sub>) ≈ 206 Ω (2,1 %)** — budżet zdominowany przez *U*<sub>2</sub> (76 %)
i *R*<sub>V2</sub> (24 %), przy znikomym wkładzie *R*<sub>V1</sub> (0,06 %).
Zakładka 5 ujawnia konflikt, o którym instrukcja milczy: mniejszy zakres daje mniejszy
błąd graniczny, ale mniejsze *R*<sub>V</sub> = ϰ·*U*<sub>z</sub>, czyli większy błąd metody.

## Struktura repozytorium

```
Cwiczenie_T2_-_instrukcja_do_cwiczenia_-_v_2_4.pdf   instrukcja źródłowa
Cwiczenie_T2_-_cwiczenie.pdf                         skrót ćwiczenia (zadania)
Cwiczenie_T2_-_odpowiedzi_na_pytania_kontrolne.pdf   dokument wynikowy
scripts/
  diagrams.py         generowanie rysunków (matplotlib, schematy rysowane prymitywami)
  pdfkit.py           silnik PDF: style, fonty DejaVu, render formuł (matplotlib mathtext),
                      szablon strony z nagłówkiem/stopką i numeracją
  build_answers.py    treść dokumentu pełnego + złożenie całości
  cheatsheet_kit.py   wersja skrócona (ściąga 4-stronicowa): układ, tabele, sekcje
  zeszyt_kit.py       zeszyt ćwiczeń (12 stron): protokoły, wyprowadzenia, zadania domowe
kalkulator.html       interaktywny kalkulator niepewności (HTML + JS, bez zależności)
build/                katalog roboczy (rysunki PNG, wyrenderowane formuły) – nie wersjonowany
```

## Ponowne złożenie dokumentu

Wymagania: Python 3.11+ oraz pakiety `reportlab`, `matplotlib`, `pymupdf`, `pillow`, `pyphen`.

```bash
python3 -m venv .venv
.venv/bin/pip install reportlab matplotlib pillow pyphen pymupdf

.venv/bin/python scripts/diagrams.py        # rysunki -> build/figs/
.venv/bin/python scripts/build_answers.py   # PDF pełny (21 stron)
.venv/bin/python scripts/cheatsheet_kit.py  # PDF skrócony (4 strony)
.venv/bin/python scripts/zeszyt_kit.py      # zeszyt ćwiczeń (12 stron)
```

Skrypt `build_answers.py` samodzielnie wyrenderuje też wszystkie formuły (matplotlib
mathtext, font DejaVu Serif) i zapisze je w `build/math/` – katalog jest odtwarzany
przy każdym uruchomieniu, więc nie trzeba go wersjonować.

## Uwagi

- Wszystkie wielkości liczbowe w zadaniach rachunkowych (17, 19–22) obliczono dla danych
  podanych w treści pytań; niepewności podano dla współczynnika rozszerzenia *k* = 1.
- Znak `≪` / `≫` nie występuje w foncie DejaVu Serif – w tekście jest renderowany
  z DejaVu Sans (znacznik `<font name="Sans">`).
- `mathtext` (matplotlib) nie obsługuje środowiska `cases` ani `\xrightarrow` – złożone
  układy równań są w zeszycie podane jako tabele, nie jako jedna formuła.
- Analiza niepewności *R*<sub>w</sub> w zeszycie i w kalkulatorze używa pochodnych
  analitycznych; różniczkowanie numeryczne daje katastrofę odejmowania (mianownik (2-16)
  jest różnicą bliskich sobie iloczynów).
