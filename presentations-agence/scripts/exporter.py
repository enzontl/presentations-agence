#!/usr/bin/env python3
"""Exporte un deck en PDF et en PowerPoint.

  python exporter.py mon-deck/deck.html --pdf --pptx
  python exporter.py mon-deck/deck.html --pptx --out livrables/ --echelle 2

- PDF : une page 1920x1080 par slide, fonds et images inclus, texte sélectionnable.
- PPTX : une slide 16:9 par slide, l'image de la slide en plein cadre, et le script de
  l'orateur (aside.notes) dans les notes PowerPoint. S'ouvre dans PowerPoint, Keynote et
  Google Slides (Fichier, Importer). Le texte n'y est pas modifiable : pour corriger, on
  corrige le HTML et on réexporte.
Prérequis : pip install playwright pillow python-pptx ; Chrome installé, ou playwright install chromium.
"""
import argparse
import io
import pathlib
import sys

from playwright.sync_api import sync_playwright

PRINT_CSS = """
*,*::before,*::after{animation-delay:0s!important;animation-duration:0s!important;transition:none!important}
@page{size:1920px 1080px;margin:0}
html,body.deck{margin:0!important;padding:0!important;background:none!important;display:block!important}
body.deck>*:not(section.slide){display:none!important}
section.slide{break-after:page;page-break-after:always;margin:0!important}
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--pptx", action="store_true")
    ap.add_argument("--out", default=None, help="dossier de sortie (défaut : celui du deck)")
    ap.add_argument("--echelle", type=float, default=1.5, help="netteté des images du PPTX (1 à 2)")
    ap.add_argument("--attente", type=int, default=1500)
    a = ap.parse_args()
    if not (a.pdf or a.pptx):
        ap.error("choisir --pdf, --pptx ou les deux")
    src = pathlib.Path(a.html).resolve()
    out = pathlib.Path(a.out) if a.out else src.parent
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        args = ["--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--allow-file-access-from-files"]
        try:
            b = p.chromium.launch(channel="chrome", args=args)
        except Exception:
            b = p.chromium.launch(args=args)

        if a.pdf:
            pg = b.new_page(viewport={"width": 1920, "height": 1080})
            pg.goto(src.as_uri() + "?print=1", wait_until="load")
            pg.add_style_tag(content=PRINT_CSS)
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(a.attente)
            f = out / (src.stem + ".pdf")
            pg.pdf(path=str(f), width="1920px", height="1080px", print_background=True, prefer_css_page_size=True)
            print(f"ok {f}")
            pg.close()

        if a.pptx:
            from pptx import Presentation
            from pptx.util import Emu
            ctx = b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=a.echelle)
            pg = ctx.new_page()
            pg.goto(src.as_uri() + "?print=1", wait_until="load")
            pg.add_style_tag(content=PRINT_CSS.split("@page")[0])
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(a.attente)
            slides = pg.locator("section.slide")
            notes = pg.evaluate("[...document.querySelectorAll('section.slide')].map(s=>{const n=s.querySelector('.notes');return n?n.textContent.replace(/\\s+\\n/g,'\\n').trim():''})")
            prs = Presentation()
            prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)  # 16:9, 13,333 x 7,5 pouces
            vide = prs.slide_layouts[6]
            for i in range(slides.count()):
                jpg = slides.nth(i).screenshot(type="jpeg", quality=88)  # JPEG : 5 à 10 fois plus léger que PNG
                s = prs.slides.add_slide(vide)
                s.shapes.add_picture(io.BytesIO(jpg), 0, 0, prs.slide_width, prs.slide_height)
                if notes[i]:
                    s.notes_slide.notes_text_frame.text = notes[i]
            f = out / (src.stem + ".pptx")
            prs.save(f)
            print(f"ok {f} : {slides.count()} slides, notes incluses")
        b.close()


if __name__ == "__main__":
    sys.exit(main())
