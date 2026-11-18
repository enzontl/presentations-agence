#!/usr/bin/env python3
"""Export HTML autonome d'un deck : un seul fichier, rien à charger, s'ouvre hors ligne.

  python export.py deck.html --out deck-autonome.html [--qualite 80] [--max 1920]

- feuilles de style locales intégrées, url() des CSS résolues ;
- images converties en WebP (1920 px max) et intégrées en base64 ;
- polices intégrées en base64 ;
- scripts locaux et externes intégrés ;
- navigation : flèches, espace, Page suivante/précédente, clic (droite avance, gauche recule),
  N affiche les notes, F plein écran, Début/Fin ;
- mise à l'échelle à la fenêtre ; numéros de page écrits en dur (data-page).
"""
import argparse
import base64
import io
import mimetypes
import pathlib
import re
import sys
import urllib.request

from PIL import Image

RASTER = (".jpg", ".jpeg", ".png", ".webp", ".gif")
FONT_MIME = {".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".otf": "font/otf"}


def b64(data, mime):
    return f"data:{mime};base64," + base64.b64encode(data).decode()


class Inliner:
    def __init__(self, qualite, maxw, usage=""):
        self.q, self.maxw, self.cache, self.usage = qualite, maxw, {}, usage

    def image(self, path):
        if path in self.cache:
            return self.cache[path]
        if path.suffix.lower() == ".svg":
            uri = b64(path.read_bytes(), "image/svg+xml")
        elif path.suffix.lower() in RASTER:
            im = Image.open(path)
            if im.width > self.maxw:
                im = im.resize((self.maxw, round(im.height * self.maxw / im.width)), Image.LANCZOS)
            buf = io.BytesIO()
            mode = "RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB"
            im.convert(mode).save(buf, "WEBP", quality=self.q, method=6)
            uri = b64(buf.getvalue(), "image/webp")
        else:
            uri = b64(path.read_bytes(), mimetypes.guess_type(path.name)[0] or "application/octet-stream")
        self.cache[path] = uri
        return uri

    def asset(self, ref, base):
        if ref.startswith(("data:", "#", "%23")):
            return ref
        if ref.startswith(("http://", "https://")):
            data = urllib.request.urlopen(urllib.request.Request(ref, headers={"User-Agent": "deck-export"}), timeout=30).read()
            ext = pathlib.Path(ref.split("?")[0]).suffix.lower()
            return b64(data, FONT_MIME.get(ext) or mimetypes.guess_type(ref.split("?")[0])[0] or "application/octet-stream")
        p = (base / ref.split("?")[0].split("#")[0]).resolve()
        if not p.exists():
            print(f"  manquant : {ref}")
            return ref
        if p.suffix.lower() in FONT_MIME:
            return b64(p.read_bytes(), FONT_MIME[p.suffix.lower()])
        return self.image(p)

    def css(self, text, base):
        def imp(m):
            ref = m.group(1)
            p = (base / ref).resolve()
            return self.css(p.read_text(), p.parent) if p.exists() else m.group(0)
        text = re.sub(r"@import\s+(?:url\()?['\"]?([^'\")]+)['\"]?\)?\s*;", imp, text)
        # polices : on n'intègre que les familles réellement citées par le deck
        def face(m):
            fam = re.search(r"font-family:\s*['\"]?([^;'\"]+)", m.group(0))
            return m.group(0) if not self.usage or not fam or fam.group(1).strip() in self.usage else ""
        text = re.sub(r"@font-face\s*{[^}]*}", face, text)
        return re.sub(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", lambda m: f"url('{self.asset(m.group(1), base)}')", text)


NAV_CSS = """
html,body{height:100%;overflow:hidden}
body.deck-live{background:#000;display:block;padding:0;margin:0}
.deck-live .stage{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform-origin:0 0}
.deck-live .slide{position:absolute;inset:0;visibility:hidden}
.deck-live .slide.is-active{visibility:visible}
.deck-live .pageno::after{content:attr(data-page)}
.deck-notes{position:fixed;left:0;right:0;bottom:0;max-height:38vh;overflow:auto;background:rgba(15,15,15,.94);color:#eee;font:16px/1.5 system-ui,sans-serif;padding:18px 28px;display:none;z-index:10;white-space:pre-wrap}
.deck-notes.on{display:block}
.deck-count{position:fixed;right:14px;bottom:10px;color:#777;font:12px system-ui,sans-serif;z-index:11}
"""

NAV_JS = """
(function(){
  document.body.classList.add('deck-live');
  var slides=[].slice.call(document.querySelectorAll('section.slide'));
  var stage=document.createElement('div');stage.className='stage';
  slides[0].parentNode.insertBefore(stage,slides[0]);
  slides.forEach(function(s,i){stage.appendChild(s);var n=String(i+1).padStart(2,'0');
    s.querySelectorAll('.pageno').forEach(function(p){p.setAttribute('data-page',n)});});
  var notes=document.createElement('div');notes.className='deck-notes';document.body.appendChild(notes);
  var count=document.createElement('div');count.className='deck-count';document.body.appendChild(count);
  var cur=Math.max(0,Math.min(slides.length-1,(parseInt(location.hash.slice(1))||1)-1));
  function fit(){var k=Math.min(innerWidth/1920,innerHeight/1080);
    stage.style.transform='scale('+k+') translate(-50%,-50%)';}
  function show(i){cur=Math.max(0,Math.min(slides.length-1,i));
    slides.forEach(function(s,j){s.classList.toggle('is-active',j===cur)});
    var a=slides[cur].querySelector('.notes');notes.textContent=a?a.textContent.trim():'(pas de notes)';
    count.textContent=(cur+1)+' / '+slides.length;history.replaceState(null,'','#'+(cur+1));}
  addEventListener('resize',fit);
  addEventListener('keydown',function(e){var k=e.key;
    if(['ArrowRight','ArrowDown',' ','PageDown','Enter'].indexOf(k)>=0){e.preventDefault();show(cur+1);}
    else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].indexOf(k)>=0){e.preventDefault();show(cur-1);}
    else if(k==='Home')show(0);else if(k==='End')show(slides.length-1);
    else if(k==='n'||k==='N')notes.classList.toggle('on');
    else if(k==='f'||k==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}});
  addEventListener('click',function(e){if(e.target.closest('.deck-notes'))return;show(e.clientX>innerWidth/3?cur+1:cur-1);});
  fit();show(cur);
})();
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--out", default=None)
    ap.add_argument("--qualite", type=int, default=80)
    ap.add_argument("--max", type=int, default=1920)
    a = ap.parse_args()

    src = pathlib.Path(a.html).resolve()
    base = src.parent
    out = pathlib.Path(a.out) if a.out else base / (src.stem + "-autonome.html")
    html = src.read_text()
    # texte qui cite les polices : le HTML et les CSS locales, sauf les blocs @font-face
    usage = html
    for href in re.findall(r"<link\b[^>]*href=['\"]([^'\"]+\.css)['\"]", html):
        p = (base / href).resolve()
        if p.exists():
            usage += re.sub(r"@font-face\s*{[^}]*}", "", p.read_text())
    inl = Inliner(a.qualite, a.max, usage)

    def link(m):
        tag = m.group(0)
        if "stylesheet" not in tag:
            return tag
        href = re.search(r"href=['\"]([^'\"]+)['\"]", tag).group(1)
        if href.startswith("http"):
            css = urllib.request.urlopen(urllib.request.Request(href, headers={"User-Agent": "Mozilla/5.0 Chrome/124"}), timeout=30).read().decode()
            return f"<style>{inl.css(css, base)}</style>"
        p = (base / href).resolve()
        return f"<style>{inl.css(p.read_text(), p.parent)}</style>"
    html = re.sub(r"<link\b[^>]*>", link, html)
    html = re.sub(r"(<style[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + inl.css(m.group(2), base) + m.group(3), html, flags=re.S)

    def script(m):
        src_ = m.group(2)
        if src_.startswith("http"):
            code = urllib.request.urlopen(urllib.request.Request(src_, headers={"User-Agent": "deck-export"}), timeout=60).read().decode()
        else:
            code = (base / src_).read_text()
        attrs = re.sub(r"\ssrc=['\"][^'\"]+['\"]", "", m.group(1))
        code = code.replace("</script", "<\\/script")
        return f"<script{attrs}>{code}</script>"
    html = re.sub(r"<script([^>]*\ssrc=['\"]([^'\"]+)['\"][^>]*)>\s*</script>", script, html)

    html = re.sub(r"(<(?:img|source)\b[^>]*?\ssrc=)(['\"])([^'\"]+)\2", lambda m: f"{m.group(1)}{m.group(2)}{inl.asset(m.group(3), base)}{m.group(2)}", html)
    html = re.sub(r"(style=)(['\"])(.*?)\2", lambda m: m.group(1) + m.group(2) + inl.css(m.group(3), base).replace(m.group(2), "&quot;" if m.group(2) == '"' else "&#39;") + m.group(2), html, flags=re.S)

    html = html.replace("</head>", f"<style>{NAV_CSS}</style></head>", 1)
    html = html.replace("</body>", f"<script>{NAV_JS}</script></body>", 1)
    out.write_text(html)
    n = len(re.findall(r"<section[^>]*class=['\"][^'\"]*\bslide\b", html))
    print(f"ok {out} : {n} slides, {out.stat().st_size / 1e6:.1f} Mo")


if __name__ == "__main__":
    sys.exit(main())
