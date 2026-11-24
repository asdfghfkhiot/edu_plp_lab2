# Ćwiczenie T2 – odpowiedzi na pytania kontrolne

Opracowanie odpowiedzi na 22 pytania kontrolne do ćwiczenia **T2 „Pomiary napięć i prądów stałych”**
(Laboratorium Podstaw Pomiarów, ISE WEiTI PW; instrukcja v. 2.4 z 20.10.2023).

## Plik wynikowy

```
Cwiczenie_T2_-_odpowiedzi_na_pytania_kontrolne.pdf   (21 stron, A4)
```

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

## Struktura repozytorium

```
Cwiczenie_T2_-_instrukcja_do_cwiczenia_-_v_2_4.pdf   instrukcja źródłowa
Cwiczenie_T2_-_cwiczenie.pdf                         skrót ćwiczenia (zadania)
Cwiczenie_T2_-_odpowiedzi_na_pytania_kontrolne.pdf   dokument wynikowy
scripts/
  diagrams.py         generowanie rysunków (matplotlib, schematy rysowane prymitywami)
  pdfkit.py           silnik PDF: style, fonty DejaVu, render formuł (matplotlib mathtext),
                      szablon strony z nagłówkiem/stopką i numeracją
  build_answers.py    treść dokumentu + złożenie całości
build/                katalog roboczy (rysunki PNG, wyrenderowane formuły) – nie wersjonowany
```

## Ponowne złożenie dokumentu

Wymagania: Python 3.11+ oraz pakiety `reportlab`, `matplotlib`, `pymupdf`, `pillow`, `pyphen`.

```bash
python3 -m venv .venv
.venv/bin/pip install reportlab matplotlib pillow pyphen pymupdf

.venv/bin/python scripts/diagrams.py        # rysunki -> build/figs/
.venv/bin/python scripts/build_answers.py   # PDF wynikowy
```

Skrypt `build_answers.py` samodzielnie wyrenderuje też wszystkie formuły (matplotlib
mathtext, font DejaVu Serif) i zapisze je w `build/math/` – katalog jest odtwarzany
przy każdym uruchomieniu, więc nie trzeba go wersjonować.

## Uwagi

- Wszystkie wielkości liczbowe w zadaniach rachunkowych (17, 19–22) obliczono dla danych
  podanych w treści pytań; niepewności podano dla współczynnika rozszerzenia *k* = 1.
- Znak `≪` / `≫` nie występuje w foncie DejaVu Serif – w tekście jest renderowany
  z DejaVu Sans (znacznik `<font name="Sans">`).
