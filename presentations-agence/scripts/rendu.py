#!/usr/bin/env python3
"""Rend chaque slide d'un deck en PNG, assemble une planche contact et signale les défauts.

  python rendu.py deck.html --out renders/ [--slides 1,4] [--cols 4] [--attente 800] [--no-js]

Sorties : renders/slide-01.png ..., renders/planche.png, renders/rapport.txt
Prérequis : pip install playwright pillow ; Chrome installé, ou `playwright install chromium`.

Le rendu se fait animations coupées (chaque élément dans son état final) et avec
?print=1 dans l'URL, pour que les scènes 3D se figent. Les éléments volontairement
coupés par le bord portent la classe .bleed et ne sont pas signalés.
"""
import argparse
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

KILL_ANIM = "*,*::before,*::after{animation-delay:0s!important;animation-duration:0s!important;transition:none!important;caret-color:transparent!important}"

CHECK_JS = r"""
() => {
  const generic = new Set(['serif','sans-serif','monospace','cursive','fantasy','system-ui','ui-monospace','ui-serif','ui-sans-serif']);
  const declared = new Set([...document.fonts].map(f => f.family.replace(/["']/g,'').toLowerCase()));
  const errors = [...document.fonts].filter(f => f.status === 'error').map(f => f.family);
  const desc = el => {
    let s = el.tagName.toLowerCase();
    if (el.className && typeof el.className === 'string') s += '.' + el.className.trim().split(/\s+/).join('.');
    const t = (el.textContent || '').trim().replace(/\s+/g,' ').slice(0, 40);
    return t ? `${s} « ${t} »` : s;
  };
  const textOf = el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
  return [...document.querySelectorAll('section.slide')].map(s => {
    const issues = [];
    const R = s.getBoundingClientRect();
    const stamps = [...s.querySelectorAll('.stamp,.tampon')];
    const missingFonts = new Set();
    s.querySelectorAll('*').forEach(el => {
      if (el.closest('.notes')) return;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      const bleed = el.closest('.bleed,.bg,[data-bleed]');
      if (!bleed && el.parentElement === s &&
          (r.left < R.left - 3 || r.top < R.top - 3 || r.right > R.right + 3 || r.bottom > R.bottom + 3))
        issues.push('sort de la slide : ' + desc(el));
      if (el.matches('h1,h2,.title,.giant,.titre') && !el.hasAttribute('data-lignes-ok')) {
        const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2;
        const lines = Math.round(el.offsetHeight / lh);
        if (lines >= 3) issues.push(`titre sur ${lines} lignes : ` + desc(el));
      }
      if ((cs.overflowY === 'hidden' || cs.overflow === 'hidden') && el !== s &&
          el.scrollHeight > el.clientHeight + 3 && (el.textContent || '').trim() && !bleed)
        issues.push('texte coupé dans sa boîte : ' + desc(el));
      if (textOf(el)) {
        const fs = parseFloat(cs.fontSize);
        if (fs < 16 && !el.closest('.source,.credit,.legende,.small-ok'))
          issues.push(`texte de ${fs}px (illisible projeté) : ` + desc(el));
        const fam = cs.fontFamily.split(',')[0].replace(/["']/g,'').trim().toLowerCase();
        if (!generic.has(fam) && !declared.has(fam)) missingFonts.add(fam);
        for (const st of stamps) {
          if (st === el || st.contains(el) || el.contains(st)) continue;
          const q = st.getBoundingClientRect();
          const ix = Math.max(0, Math.min(r.right, q.right) - Math.max(r.left, q.left));
          const iy = Math.max(0, Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top));
          if (ix * iy > 0.25 * r.width * r.height) issues.push('texte sous un tampon (à vérifier) : ' + desc(el));
        }
      }
      if (el.tagName === 'IMG' && !(el.complete && el.naturalWidth)) issues.push('image manquante : ' + el.getAttribute('src'));
    });
    missingFonts.forEach(f => issues.push(`police non déclarée, repli système : ${f}`));
    errors.forEach(f => issues.push(`police en erreur : ${f}`));
    return issues;
  });
}
"""


def planche(paths, out, cols=4, tw=480):
    th = int(tw * 9 / 16)
    gap, lab = 24, 30
    rows = (len(paths) + cols - 1) // cols
    W = cols * tw + (cols + 1) * gap
    H = rows * (th + lab) + (rows + 1) * gap
    sheet = Image.new("RGB", (W, H), (28, 28, 28))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default(size=18)
    except TypeError:
        font = ImageFont.load_default()
    for k, (num, p) in enumerate(paths):
        r, c = divmod(k, cols)
        x = gap + c * (tw + gap)
        y = gap + r * (th + lab + gap)
        im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (x, y))
        d.text((x, y + th + 6), f"{num:02d}", fill=(200, 200, 200), font=font)
    sheet.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--out", default="renders")
    ap.add_argument("--slides", default="")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--attente", type=int, default=800, help="ms d'attente après chargement (3D, images)")
    ap.add_argument("--no-js", action="store_true")
    a = ap.parse_args()

    src = pathlib.Path(a.html).resolve()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    wanted = {int(x) for x in a.slides.split(",") if x.strip()}

    with sync_playwright() as p:
        args = ["--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--allow-file-access-from-files"]
        try:
            b = p.chromium.launch(channel="chrome", args=args)
        except Exception:
            b = p.chromium.launch(args=args)
        ctx = b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1, java_script_enabled=not a.no_js)
        page = ctx.new_page()
        console = []
        page.on("console", lambda m: console.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: console.append(f"erreur JS : {e}"))
        page.goto(src.as_uri() + "?print=1", wait_until="load")
        page.add_style_tag(content=KILL_ANIM)
        if not a.no_js:
            page.evaluate("document.fonts.ready")
        page.wait_for_timeout(a.attente)

        slides = page.locator("section.slide")
        n = slides.count()
        issues = page.evaluate(CHECK_JS) if not a.no_js else [[] for _ in range(n)]
        rendus = []
        for i in range(n):
            num = i + 1
            if wanted and num not in wanted:
                continue
            f = out / f"slide-{num:02d}.png"
            slides.nth(i).screenshot(path=str(f))
            rendus.append((num, f))
        b.close()

    if rendus:
        planche(rendus, out / "planche.png", a.cols)

    lignes = []
    for i, iss in enumerate(issues):
        if (wanted and i + 1 not in wanted) or not iss:
            continue
        lignes.append(f"Slide {i + 1:02d}")
        lignes += [f"  - {x}" for x in dict.fromkeys(iss)]
    if console:
        lignes.append("Console")
        lignes += [f"  - {x}" for x in console[:20]]
    rapport = "\n".join(lignes) if lignes else "Aucun problème détecté. Regarder quand même la planche et chaque slide modifiée."
    (out / "rapport.txt").write_text(rapport + "\n")
    print(f"{len(rendus)} slides rendues dans {out}/")
    print(rapport)


if __name__ == "__main__":
    sys.exit(main())
