"""Silnik generowania PDF: style, flowable'e, nagłówek/stopka.

Dokument: odpowiedzi na pytania kontrolne do ćwiczenia T2.
"""
import os
import hashlib

import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties
from PIL import Image as PILImage

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, Image, Flowable,
                                NextPageTemplate, PageBreak, KeepTogether)
from reportlab.pdfgen import canvas as canvas_module

rcParams['mathtext.fontset'] = 'dejavuserif'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, 'build')
FIGDIR = os.path.join(BUILD, 'figs')
MATHDIR = os.path.join(BUILD, 'math')
os.makedirs(MATHDIR, exist_ok=True)

NAVY = colors.HexColor('#12335c')
ACCENT = colors.HexColor('#1a5fb4')
GREY = colors.HexColor('#5c6773')
RULE = colors.HexColor('#b8c6d9')
LIGHT = colors.HexColor('#eef3f9')
LIGHT2 = colors.HexColor('#f7f9fc')

PAGE_W, PAGE_H = A4
LM, RM, TM, BM = 2.05 * cm, 2.05 * cm, 2.30 * cm, 2.05 * cm
CONTENT_W = PAGE_W - LM - RM

# ------------------------------------------------------------------ fonty
MPL_FONTS = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')


def _reg(name, fname):
    pdfmetrics.registerFont(TTFont(name, os.path.join(MPL_FONTS, fname)))


_reg('Serif', 'DejaVuSerif.ttf')
_reg('Serif-Bold', 'DejaVuSerif-Bold.ttf')
_reg('Serif-Italic', 'DejaVuSerif-Italic.ttf')
_reg('Serif-BoldItalic', 'DejaVuSerif-BoldItalic.ttf')
_reg('Sans', 'DejaVuSans.ttf')
_reg('Sans-Bold', 'DejaVuSans-Bold.ttf')
_reg('Sans-Italic', 'DejaVuSans-Oblique.ttf')
_reg('Sans-BoldItalic', 'DejaVuSans-BoldOblique.ttf')
pdfmetrics.registerFontFamily('Serif', normal='Serif', bold='Serif-Bold',
                              italic='Serif-Italic', boldItalic='Serif-BoldItalic')
pdfmetrics.registerFontFamily('Sans', normal='Sans', bold='Sans-Bold',
                              italic='Sans-Italic', boldItalic='Sans-BoldItalic')

BODY = 9.55
LEAD = 14.1

S = {}
S['body'] = ParagraphStyle('body', fontName='Serif', fontSize=BODY, leading=LEAD,
                           alignment=TA_JUSTIFY, hyphenationLang='pl_PL',
                           embeddedHyphenation=1, splitLongWords=1,
                           spaceBefore=0, spaceAfter=5.2, textColor=colors.HexColor('#14181d'))
S['body_c'] = ParagraphStyle('body_c', parent=S['body'], alignment=TA_CENTER,
                             hyphenationLang='')
S['q'] = ParagraphStyle('q', fontName='Sans-Bold', fontSize=10.1, leading=14.2,
                        textColor=NAVY, alignment=TA_LEFT, hyphenationLang='pl_PL',
                        embeddedHyphenation=1, spaceBefore=0, spaceAfter=0)
S['part'] = ParagraphStyle('part', fontName='Sans-Bold', fontSize=11.6, leading=15,
                           textColor=NAVY, spaceBefore=0, spaceAfter=2,
                           hyphenationLang='pl_PL')
S['part_sub'] = ParagraphStyle('part_sub', fontName='Sans', fontSize=8.6, leading=12,
                               textColor=GREY, spaceBefore=0, spaceAfter=6)
S['bullet'] = ParagraphStyle('bullet', parent=S['body'], leftIndent=12.5,
                             bulletIndent=3.0, spaceAfter=2.6,
                             bulletFontName='Serif', bulletFontSize=BODY)
S['num'] = ParagraphStyle('num', parent=S['body'], leftIndent=15.5,
                          bulletIndent=2.0, spaceAfter=2.6)
S['caption'] = ParagraphStyle('caption', fontName='Sans', fontSize=8.0, leading=11.4,
                              alignment=TA_CENTER, textColor=GREY,
                              spaceBefore=3.5, spaceAfter=8,
                              hyphenationLang='pl_PL')
S['cell'] = ParagraphStyle('cell', fontName='Serif', fontSize=8.5, leading=11.6,
                           alignment=TA_LEFT)
S['cell_c'] = ParagraphStyle('cell_c', parent=S['cell'], alignment=TA_CENTER)
S['cell_h'] = ParagraphStyle('cell_h', fontName='Sans-Bold', fontSize=8.3,
                             leading=11.2, textColor=colors.white,
                             alignment=TA_LEFT)
S['cell_hc'] = ParagraphStyle('cell_hc', parent=S['cell_h'], alignment=TA_CENTER)
S['note'] = ParagraphStyle('note', fontName='Serif', fontSize=8.9, leading=12.9,
                           alignment=TA_JUSTIFY, hyphenationLang='pl_PL',
                           embeddedHyphenation=1, textColor=colors.HexColor('#1d2b3a'))
S['tag'] = ParagraphStyle('tag', fontName='Serif', fontSize=9.0, leading=13,
                          alignment=TA_LEFT, textColor=colors.HexColor('#33404f'))
S['small'] = ParagraphStyle('small', fontName='Sans', fontSize=7.9, leading=11,
                            textColor=GREY, alignment=TA_LEFT,
                            hyphenationLang='pl_PL')

# ------------------------------------------------------------------ wzory


def _sanitize(tex):
    """Usuwa wewnętrzne znaki $ (formuła zawsze trafia do jednego środowiska math)."""
    t = tex.strip()
    core = t[1:-1] if (t.startswith('$') and t.endswith('$')) else t
    core = core.replace('$', '')
    return '$' + core + '$'


def mathpng(tex, size=10.2, dpi=600):
    """Render formuły TeX do PNG; zwraca (ścieżka, szer_pt, wys_pt)."""
    tex = _sanitize(tex)
    key = hashlib.md5(f'{tex}|{size}|{dpi}'.encode()).hexdigest()[:16]
    path = os.path.join(MATHDIR, key + '.png')
    if not os.path.exists(path):
        math_to_image(tex, path, prop=FontProperties(size=size), dpi=dpi,
                      format='png')
        im = PILImage.open(path).convert('RGBA')
        bg = PILImage.new('RGBA', im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        bg.convert('RGB').save(path)
    im = PILImage.open(path)
    return path, im.size[0] * 72.0 / dpi, im.size[1] * 72.0 / dpi


class Eq(Flowable):
    """Wzór: wyśrodkowany obraz formuły + numer po prawej stronie."""

    def __init__(self, tex, tag=None, size=10.2, space=5.0):
        super().__init__()
        self.path, self.w0, self.h0 = mathpng(tex, size)
        self.tag = tag
        self.space = space
        self.scale = 1.0
        maxw = CONTENT_W - (52 if tag else 12)
        if self.w0 > maxw:
            self.scale = maxw / self.w0
        self.width = self.w0 * self.scale
        self.height = self.h0 * self.scale

    def wrap(self, aw, ah):
        return CONTENT_W, self.height + 2 * self.space

    def draw(self):
        c = self.canv
        y = self.space
        c.drawImage(self.path, (CONTENT_W - self.width) / 2.0, y,
                    width=self.width, height=self.height, mask=None)
        if self.tag:
            c.setFont('Serif', 9.0)
            c.setFillColor(colors.HexColor('#33404f'))
            c.drawRightString(CONTENT_W, y + 0.30 * self.height, self.tag)


class Badge(Flowable):
    def __init__(self, num, d=0.80 * cm):
        super().__init__()
        self.num = num
        self.d = d

    def wrap(self, aw, ah):
        return self.d, self.d

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.circle(self.d / 2.0, self.d / 2.0, self.d / 2.0, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont('Sans-Bold', 9.4 if self.num < 10 else 8.6)
        c.drawCentredString(self.d / 2.0, self.d / 2.0 - 3.3, str(self.num))


class PartHeading(Flowable):
    """Nagłówek części z numerem rzymskim i opisem zakresu pytań."""

    def __init__(self, rzym, title, sub):
        super().__init__()
        self.rzym = rzym
        self.title = title
        self.sub = sub
        self.p_title = Paragraph(title, S['part'])
        self.p_sub = Paragraph(sub, S['part_sub'])
        self.keepWithNext = 1

    def wrap(self, aw, ah):
        xt = 1.80 * cm if len(self.rzym) > 2 else 1.15 * cm
        w1, h1 = self.p_title.wrap(CONTENT_W - xt - 0.2 * cm, ah)
        w2, h2 = self.p_sub.wrap(CONTENT_W - xt - 0.2 * cm, ah)
        self.band = max(h1 + h2 + 9, 1.05 * cm)
        self.h = self.band + 12
        return CONTENT_W, self.h

    def draw(self):
        c = self.canv
        h = self.h
        # pasek akcentu
        band = self.band
        c.setFillColor(ACCENT)
        c.rect(0, h - 12 - band, 0.10 * cm, band, stroke=0, fill=1)
        c.setFillColor(LIGHT)
        c.rect(0.10 * cm, h - 12 - band, CONTENT_W - 0.10 * cm, band,
               stroke=0, fill=1)
        x_title = 1.80 * cm if len(self.rzym) > 2 else 1.15 * cm
        c.setFillColor(NAVY)
        c.setFont('Sans-Bold', 12.6 if len(self.rzym) > 2 else 13.2)
        w1, h1 = self.p_title.wrap(CONTENT_W - x_title - 0.2 * cm, 1000)
        w2, h2 = self.p_sub.wrap(CONTENT_W - x_title - 0.2 * cm, 1000)
        top = h - 12 - band
        y_title = top + band - 6 - h1
        y_sub = y_title - h2 - 1
        c.drawString(0.40 * cm, y_title + 1.4, self.rzym)
        self.p_title.drawOn(c, x_title, y_title)
        self.p_sub.drawOn(c, x_title, y_sub)
        # linia pod nagłówkiem
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.line(0, 1, CONTENT_W, 1)


def fig_block(path, width_cm, caption, number):
    """Obraz + podpis. Zwraca listę flowable'ów (strona może się złamać tuż
    przed obrazem, ale obraz nigdy nie zostaje oddzielony od podpisu)."""
    im = PILImage.open(path)
    w = width_cm * cm
    h = w * im.size[1] / float(im.size[0])
    img = Image(path, width=w, height=h)
    img.hAlign = 'CENTER'
    cap = Paragraph(f'<b>Rys. {number}.</b> {caption}', S['caption'])
    cap.keepWithNext = 0
    return [Spacer(1, 3), KeepTogether([img, cap])]


def note_box(flowables, fill=LIGHT, bar=ACCENT):
    t = Table([[flowables]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), fill),
        ('LINEBEFORE', (0, 0), (0, -1), 2.1, bar),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return [Spacer(1, 3), t, Spacer(1, 7)]


def data_table(rows, widths, header=True, fs=8.5, align=None, zebra=True):
    """rows: lista wierszy; komórki: str (Paragraph) lub Flowable."""
    data = []
    for r_i, row in enumerate(rows):
        out = []
        for c_i, cell in enumerate(row):
            if isinstance(cell, str):
                if header and r_i == 0:
                    st = S['cell_hc'] if (align and align[c_i] == 'c') else S['cell_h']
                else:
                    st = S['cell_c'] if (align and align[c_i] == 'c') else S['cell']
                out.append(Paragraph(cell, st))
            else:
                out.append(cell)
        data.append(out)
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign='CENTER')
    style = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.6),
        ('LINEBELOW', (0, 0), (-1, -1), 0.35, colors.HexColor('#d2dbe6')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#c3cedc')),
    ]
    if header:
        style += [('BACKGROUND', (0, 0), (-1, 0), NAVY),
                  ('LINEBELOW', (0, 0), (-1, 0), 0.5, NAVY)]
    if zebra:
        start = 1 if header else 0
        for i in range(start, len(data)):
            if (i - start) % 2 == 1:
                style.append(('BACKGROUND', (0, i), (-1, i), LIGHT2))
    t.setStyle(TableStyle(style))
    return t


# ------------------------------------------------------------------ szablon


class NumberedCanvas(canvas_module.Canvas):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for st in self._saved:
            self.__dict__.update(st)
            if self._pageNumber > 1:
                self._decorate(total)
            canvas_module.Canvas.showPage(self)
        canvas_module.Canvas.save(self)

    def _decorate(self, total):
        c = self
        c.saveState()
        # nagłówek
        c.setFont('Sans', 7.6)
        c.setFillColor(GREY)
        c.drawString(LM, PAGE_H - 1.36 * cm, 'Ćwiczenie T2 \u00b7 Pomiary napięć i prądów stałych')
        c.drawRightString(PAGE_W - RM, PAGE_H - 1.36 * cm,
                          'Odpowiedzi na pytania kontrolne')
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.line(LM, PAGE_H - 1.52 * cm, PAGE_W - RM, PAGE_H - 1.52 * cm)
        # stopka
        c.line(LM, 1.42 * cm, PAGE_W - RM, 1.42 * cm)
        c.setFont('Sans', 7.5)
        c.setFillColor(GREY)
        c.drawString(LM, 1.05 * cm, 'Laboratorium Podstaw Pomiarów \u00b7 ISE WEiTI PW')
        c.drawRightString(PAGE_W - RM, 1.05 * cm,
                          f'str. {self._pageNumber} z {total}')
        c.restoreState()


class Doc(BaseDocTemplate):
    cover_draw = None

    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=A4,
                         leftMargin=LM, rightMargin=RM,
                         topMargin=TM, bottomMargin=BM,
                         title='Ćwiczenie T2 – odpowiedzi na pytania kontrolne',
                         author='Laboratorium Podstaw Pomiarów',
                         subject='Pomiary napięć i prądów stałych',
                         **kw)
        frame_cover = Frame(LM, BM, CONTENT_W, PAGE_H - TM - BM, id='cover',
                            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        frame_body = Frame(LM, BM, CONTENT_W, PAGE_H - TM - BM, id='body',
                           leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[frame_cover], onPage=self._cover_bg),
            PageTemplate(id='body', frames=[frame_body]),
        ])

    def _cover_bg(self, c, doc):
        if Doc.cover_draw is not None:
            Doc.cover_draw(c)
            return
        c.saveState()
        band_h = 7.05 * cm
        c.setFillColor(NAVY)
        c.rect(0, PAGE_H - band_h, PAGE_W, band_h, stroke=0, fill=1)
        c.setFillColor(colors.HexColor('#1f4b7f'))
        c.rect(0, PAGE_H - band_h, PAGE_W, 0.16 * cm, stroke=0, fill=1)
        # delikatne pasy
        c.setFillColor(colors.HexColor('#183f6c'))
        c.rect(0, PAGE_H - band_h, 0.55 * cm, band_h, stroke=0, fill=1)
        c.setStrokeColor(colors.HexColor('#8fb3d9'))
        c.setLineWidth(0.8)
        c.line(LM, PAGE_H - band_h + 1.05 * cm, PAGE_W - RM, PAGE_H - band_h + 1.05 * cm)
        c.restoreState()


def build(story, out_path):
    doc = Doc(out_path)
    doc.build(story, canvasmaker=NumberedCanvas)
    return out_path
