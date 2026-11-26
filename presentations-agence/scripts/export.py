#!/usr/bin/env python3
"""Export HTML autonome d'un deck : un seul fichier, rien à charger, s'ouvre hors ligne.

  python export.py deck.html --out deck-autonome.html [--qualite 80] [--max 1920]

- feuilles de style locales intégrées, url() des CSS résolues ;
- images converties en WebP (1920 px max) et intégrées en base64 ;
- polices intégrées en base64 ;
- scripts locaux et externes intégrés ;
- navigation : flèches, espace, Page suivante/précédente, clic (droite avance, gauche recule),
  N notes, O vue d'ensemble, P vue présentateur (minuteur, slide suivante, notes, synchronisée),
  F plein écran, Début/Fin ;
- mise en scène : morphing des éléments qui portent le même view-transition-name d'une slide
  à l'autre, sous-étapes data-etape, titres data-anim="mots", sens du retour (.deck-back),
  barre de progression par partie si <body data-progression> ;
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
.deck-live .slide{position:absolute;inset:0;display:none}
.deck-live .slide.is-active{display:block}
.deck-live .pageno::after{content:attr(data-page)}
/* éléments qui persistent d'une slide à l'autre (même view-transition-name) : pas de seconde entrée */
.deck-live .slide.is-active .persiste[data-anim]{animation:none!important;opacity:1!important}
/* mots animés un par un */
.deck-live .slide [data-anim=mots]{opacity:1!important;animation:none!important}
.deck-live .slide [data-anim=mots] .w{display:inline-block;opacity:0}
.deck-live .slide.is-active [data-anim=mots] .w{animation:rise .7s cubic-bezier(.16,1,.3,1) both;animation-delay:calc(var(--i,0) * 120ms + var(--j) * 55ms)}
/* sous-étapes : révélées une à une avant de passer à la slide suivante */
.deck-live [data-etape]{opacity:0;transform:translateY(16px);transition:opacity .45s cubic-bezier(.2,0,0,1),transform .55s cubic-bezier(.2,0,0,1)}
.deck-live [data-etape].vu{opacity:1;transform:none}
::view-transition-group(*){animation-duration:.7s;animation-timing-function:cubic-bezier(.65,0,.35,1)}
.deck-notes{position:fixed;left:0;right:0;bottom:0;max-height:38vh;overflow:auto;background:rgba(15,15,15,.94);color:#eee;font:16px/1.5 system-ui,sans-serif;padding:18px 28px;display:none;z-index:10;white-space:pre-wrap}
.deck-notes.on{display:block}
.deck-count{position:fixed;right:14px;bottom:10px;color:#777;font:12px system-ui,sans-serif;z-index:11}
.deck-prog{position:fixed;left:0;right:0;bottom:0;height:4px;display:flex;gap:3px;z-index:11}
.deck-prog i{flex:var(--n);background:rgba(255,255,255,.18);position:relative;cursor:pointer}
.deck-prog i b{position:absolute;inset:0 auto 0 0;width:var(--p,0%);background:rgba(255,255,255,.75);transition:width .5s}
.deck-ov{position:fixed;inset:0;background:rgba(12,12,12,.96);color:#ddd;font:15px/1.4 system-ui,sans-serif;padding:40px 56px;overflow:auto;display:none;z-index:20;columns:3 320px}
.deck-ov.on{display:block}
.deck-ov b{display:block;color:#fff;margin:18px 0 6px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;break-after:avoid}
.deck-ov a{display:block;color:inherit;text-decoration:none;padding:4px 0;cursor:pointer}
.deck-ov a.now{color:#fff;font-weight:600}
.deck-ov a small{color:#777;margin-right:10px;font-variant-numeric:tabular-nums}
body.presentateur .stage{left:24px;top:84px;transform-origin:0 0}
body.presentateur .deck-pv{display:grid}
.deck-pv{display:none;position:fixed;inset:0;pointer-events:none;grid-template-columns:62% 1fr;grid-template-rows:60px 1fr;color:#eee;font:16px/1.5 system-ui,sans-serif;z-index:12}
.deck-pv header{grid-column:1/3;display:flex;gap:24px;align-items:center;padding:0 24px;border-bottom:1px solid #333;pointer-events:auto}
.deck-pv header b{font-size:28px;font-variant-numeric:tabular-nums}
.deck-pv aside{grid-column:2;padding:20px 28px;overflow:auto;pointer-events:auto;white-space:pre-wrap}
.deck-pv aside h4{margin:0 0 6px;color:#999;font-size:12px;letter-spacing:.14em;text-transform:uppercase}
.deck-pv .suiv{color:#fff;font-size:20px;margin-bottom:28px}
.deck-pv .notes-pv{font-size:22px;line-height:1.5}
.deck-pv button{font:inherit;background:#222;color:#eee;border:1px solid #444;padding:4px 12px;cursor:pointer}
"""
NAV_JS = """
(function(){
  var P=new URLSearchParams(location.search), PV=P.get('presentateur')==='1';
  document.body.classList.add('deck-live'); if(PV) document.body.classList.add('presentateur');
  var slides=[].slice.call(document.querySelectorAll('section.slide'));
  var stage=document.createElement('div');stage.className='stage';
  slides[0].parentNode.insertBefore(stage,slides[0]);
  var titre=function(s){var h=s.querySelector('h1,h2,.title,.titre,.headline,.masthead');return h?h.textContent.replace(/\\s+/g,' ').trim():'';};
  slides.forEach(function(s,i){stage.appendChild(s);var n=String(i+1).padStart(2,'0');
    s.querySelectorAll('.pageno').forEach(function(p){p.setAttribute('data-page',n)});
    // mots : chaque mot devient un span animé (--j = rang du mot)
    s.querySelectorAll('[data-anim=mots]').forEach(function(el){var j=0,w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),t,ts=[];
      while(t=w.nextNode())ts.push(t);
      ts.forEach(function(t){var f=document.createDocumentFragment();t.textContent.split(/(\\s+)/).forEach(function(m){
        if(!m)return; if(/^\\s+$/.test(m)){f.appendChild(document.createTextNode(m));return;}
        var sp=document.createElement('span');sp.className='w';sp.style.setProperty('--j',j++);sp.textContent=m;f.appendChild(sp);});
        t.parentNode.replaceChild(f,t);});});});
  var noms=function(s){return [].slice.call(s.querySelectorAll('[style*="view-transition-name"]')).map(function(e){return e.style.viewTransitionName});};
  var etapes=function(s){return [].slice.call(s.querySelectorAll('[data-etape]')).sort(function(a,b){return a.dataset.etape-b.dataset.etape});};
  var notes=document.createElement('div');notes.className='deck-notes';document.body.appendChild(notes);
  var count=document.createElement('div');count.className='deck-count';document.body.appendChild(count);
  // progression par partie (data-section), si <body data-progression>
  var parts=[];slides.forEach(function(s,i){var n=s.dataset.section||'';if(!parts.length||parts[parts.length-1].n!==n)parts.push({n:n,a:i,b:i});else parts[parts.length-1].b=i;});
  var prog=null;if(document.body.hasAttribute('data-progression')){prog=document.createElement('div');prog.className='deck-prog';
    parts.forEach(function(p){var i=document.createElement('i');i.style.setProperty('--n',p.b-p.a+1);i.title=p.n;i.innerHTML='<b></b>';i.onclick=function(){show(p.a)};prog.appendChild(i);p.el=i;});
    document.body.appendChild(prog);}
  // vue d'ensemble (O)
  var ov=document.createElement('div');ov.className='deck-ov';document.body.appendChild(ov);
  function buildOv(){var h='',last=null;slides.forEach(function(s,i){var n=s.dataset.section||'';if(n!==last){h+='<b>'+(n||'·')+'</b>';last=n;}
    h+='<a data-i="'+i+'"'+(i===cur?' class="now"':'')+'><small>'+String(i+1).padStart(2,'0')+'</small>'+titre(s).slice(0,90)+'</a>';});
    ov.innerHTML=h;ov.querySelectorAll('a').forEach(function(a){a.onclick=function(){ov.classList.remove('on');show(+a.dataset.i)}});}
  // vue présentateur (P) : même fichier, ?presentateur=1, synchronisé par BroadcastChannel
  var bc=window.BroadcastChannel?new BroadcastChannel('deck-'+location.pathname):null, sync=false;
  var pv=null,t0=null,tick=null;
  if(PV){pv=document.createElement('div');pv.className='deck-pv';
    pv.innerHTML='<header><b id="pv-n"></b><span id="pv-t">00:00</span><button id="pv-go">Démarrer</button><button id="pv-prev">←</button><button id="pv-next">→</button></header><aside><h4>Ensuite</h4><div class="suiv" id="pv-s"></div><h4>Notes</h4><div class="notes-pv" id="pv-notes"></div></aside>';
    document.body.appendChild(pv);
    pv.querySelector('#pv-go').onclick=function(){if(tick){clearInterval(tick);tick=null;this.textContent='Reprendre';return;}t0=t0||Date.now();this.textContent='Pause';
      tick=setInterval(function(){var s=Math.floor((Date.now()-t0)/1000);pv.querySelector('#pv-t').textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');},500);};
    pv.querySelector('#pv-prev').onclick=function(){back()};pv.querySelector('#pv-next').onclick=function(){fwd()};}
  var cur=-1, sub=0;
  function fit(){var W=PV?innerWidth*.62-48:innerWidth,H=PV?innerHeight-108:innerHeight,k=Math.min(W/1920,H/1080);
    stage.style.transform=PV?'scale('+k+')':'scale('+k+') translate(-50%,-50%)';}
  function apply(i,dir){var prevNoms=cur>=0?noms(slides[cur]):[];cur=i;
    document.body.classList.toggle('deck-back',dir<0);
    slides.forEach(function(s,j){s.classList.toggle('is-active',j===cur)});
    var s=slides[cur];s.querySelectorAll('.persiste').forEach(function(e){e.classList.remove('persiste')});
    noms(s).forEach(function(n){if(prevNoms.indexOf(n)>=0)s.querySelectorAll('[style*="view-transition-name"]').forEach(function(e){if(e.style.viewTransitionName===n)e.classList.add('persiste')})});
    var et=etapes(s);sub=dir<0?et.length:0;et.forEach(function(e,k){e.classList.toggle('vu',k<sub)});
    var a=s.querySelector('.notes');notes.textContent=a?a.textContent.trim():'(pas de notes)';
    count.textContent=(cur+1)+' / '+slides.length;history.replaceState(null,'','#'+(cur+1));
    if(prog)parts.forEach(function(p){p.el.style.setProperty('--p',cur>p.b?'100%':cur<p.a?'0%':((cur-p.a+1)/(p.b-p.a+1)*100)+'%')});
    if(pv){pv.querySelector('#pv-n').textContent=(cur+1)+' / '+slides.length;pv.querySelector('#pv-s').textContent=slides[cur+1]?titre(slides[cur+1]):'Fin';pv.querySelector('#pv-notes').textContent=notes.textContent;}
    if(bc&&!sync)bc.postMessage({i:cur,sub:sub});
    emit();}
  // un monde persistant (canvas derrière toutes les slides) écoute cet événement pour déplacer sa caméra
  function emit(){document.dispatchEvent(new CustomEvent('deck:slide',{detail:{i:cur,etape:sub,slide:slides[cur],pose:slides[cur].dataset.pose||null}}));}
  function show(i,dir){i=Math.max(0,Math.min(slides.length-1,i));if(i===cur)return;dir=dir||(i>cur?1:-1);
    var reduit=matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(document.startViewTransition&&!reduit&&cur>=0)document.startViewTransition(function(){apply(i,dir)});else apply(i,dir);}
  function fwd(){var et=etapes(slides[cur]);if(sub<et.length){et[sub++].classList.add('vu');if(bc)bc.postMessage({i:cur,sub:sub});emit();return;}show(cur+1,1);}
  function back(){var et=etapes(slides[cur]);if(sub>0){et[--sub].classList.remove('vu');if(bc)bc.postMessage({i:cur,sub:sub});emit();return;}show(cur-1,-1);}
  if(bc)bc.onmessage=function(e){sync=true;if(e.data.i!==cur)apply(e.data.i,e.data.i>cur?1:-1);var et=etapes(slides[cur]);sub=e.data.sub;et.forEach(function(x,k){x.classList.toggle('vu',k<sub)});sync=false;};
  addEventListener('resize',fit);
  addEventListener('keydown',function(e){if(e.metaKey||e.ctrlKey||e.altKey)return;var k=e.key;
    if(ov.classList.contains('on')){if(k==='Escape'||k==='o'||k==='O')ov.classList.remove('on');return;}
    if(['ArrowRight','ArrowDown',' ','PageDown','Enter'].indexOf(k)>=0){e.preventDefault();fwd();}
    else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].indexOf(k)>=0){e.preventDefault();back();}
    else if(k==='Home')show(0);else if(k==='End')show(slides.length-1);
    else if(k==='n'||k==='N')notes.classList.toggle('on');
    else if(k==='o'||k==='O'||k==='Escape'){buildOv();ov.classList.add('on');}
    else if((k==='p'||k==='P')&&!PV)window.open(location.pathname+'?presentateur=1#'+(cur+1),'presentateur','width=1400,height=860');
    else if(k==='f'||k==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}});
  addEventListener('click',function(e){if(e.target.closest('.deck-notes,.deck-ov,.deck-pv,.deck-prog')||PV)return;e.clientX>innerWidth/3?fwd():back();});
  fit();apply(Math.max(0,Math.min(slides.length-1,(parseInt(location.hash.slice(1))||1)-1)),1);
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
