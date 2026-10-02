"""Gera todas as páginas HTML da Proposta 2 a partir de data_site.py e dos
dados coletados do site oficial (_tools/data). Rode da raiz do projeto:

    python _tools/pages.py

Cabeçalho, rodapé, ícones e metadados vivem só aqui; as páginas geradas são
HTML estático, prontas para o GitHub Pages, sem etapa de build no servidor."""
import html, io, json, math, os, random, re, sys, unicodedata

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from data_site import *  # noqa

SITE_URL = "https://apxweb.github.io/intercientifica-proposta-2/"
BASE_PATH = "/intercientifica-proposta-2/"
YEAR = 2026
esc = lambda t: html.escape(t or "", quote=True)


def reg(t):
    """Marca ® com o estilo tipográfico do sistema (sem mudar o texto)."""
    return esc(t).replace("®", '<span class="reg">®</span>')


def slugify(t, limit=72):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()[:limit].rstrip("-")


def clean(t):
    return re.sub(r"\s+", " ", (t or "").replace("​", "")).strip()


def excerpt(t, n=160):
    t = clean(t)
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(",;:–-") + "…"


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="\n").write(content)


# ---------------------------------------------------------------- ícones
SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M3 12h17M14 6l6 6-6 6"/></symbol>
  <symbol id="i-back" viewBox="0 0 24 24"><path d="M21 12H4M10 6l-6 6 6 6"/></symbol>
  <symbol id="i-down" viewBox="0 0 24 24"><path d="M12 3v17M6 14l6 6 6-6"/></symbol>
  <symbol id="i-ext" viewBox="0 0 24 24"><path d="M7 17 17 7M8 7h9v9"/></symbol>
  <symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 3h4l2 5-3 2a12 12 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2"/></symbol>
  <symbol id="i-mail" viewBox="0 0 24 24"><path d="M3 5h18v14H3zM3 6l9 7 9-7"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><path d="M12 11.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24"><path d="M10.5 18a7.5 7.5 0 1 0 0-15 7.5 7.5 0 0 0 0 15zM16 16l5 5"/></symbol>
  <symbol id="i-close" viewBox="0 0 24 24"><path d="M5 5l14 14M19 5 5 19"/></symbol>
  <symbol id="i-file" viewBox="0 0 24 24"><path d="M6 2h9l5 5v15H6zM14 2v6h6M9 13h8M9 17h8"/></symbol>
  <symbol id="i-sigma" viewBox="0 0 24 24"><path d="M18 4H6l7 8-7 8h12"/></symbol>
  <symbol id="i-factory" viewBox="0 0 24 24"><path class="icon-fill" d="M2 21V9.5l5.5 3.2V9.5l5.5 3.2V9.5l5.5 3.2V3H22v18z"/></symbol>
  <symbol id="i-wa" viewBox="0 0 24 24"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35M12.05 21.5h-.01a9.43 9.43 0 0 1-4.8-1.32l-.35-.2-3.57.93.96-3.48-.23-.36A9.4 9.4 0 0 1 2.6 12.04C2.6 6.84 6.84 2.6 12.06 2.6c2.52 0 4.9.99 6.68 2.77a9.37 9.37 0 0 1 2.76 6.68c0 5.2-4.24 9.45-9.45 9.45M20.1 4c-2.15-2.15-5-3.34-8.05-3.34C5.78.66.67 5.77.67 12.04c0 2 .52 3.96 1.52 5.69L.57 23.7l6.1-1.6a11.36 11.36 0 0 0 5.37 1.37h.01c6.27 0 11.38-5.11 11.38-11.38 0-3.04-1.18-5.9-3.33-8.05"/></symbol>
  <symbol id="i-ig" viewBox="0 0 24 24"><path d="M4 4h16v16H4z"/><path d="M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM17 7h.01"/></symbol>
  <symbol id="i-fb" viewBox="0 0 24 24"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8.5A.5.5 0 0 1 14 8z"/></symbol>
</svg>"""


def icon(name, cls="icon"):
    fill = name in ("wa", "factory")
    return '<svg class="%s%s" aria-hidden="true"><use href="#i-%s"/></svg>' % (cls, " icon-fill" if fill else "", name)


def ref_sym():
    return '<span class="sym" aria-hidden="true">REF</span>'


# ---------------------------------------------------------------- moldura
NAV = [("empresa/", "Empresa", "empresa"), ("produtos/", "Produtos", "produtos"),
       ("produtos/#automacao", "Automação", None), ("publicacoes/", "Publicações", "publicacoes"),
       ("contato/", "Contato", "contato")]

FONTS = "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..900&family=Martian+Mono:wdth,wght@75..112.5,400..600&display=swap"


def page(rel, title, desc, body, section=None, home=False, extra_head="", scripts="", og_type="website", base=None):
    depth = rel.count("/")
    p = base if base is not None else "../" * depth
    url = SITE_URL + re.sub(r"index\.html$", "", rel)
    nav = "".join(
        '<a href="%s%s"%s>%s</a>' % (p, href, ' aria-current="page"' if key and key == section else "", label)
        for href, label, key in NAV)
    sheet_nav = "".join('<a href="%s%s">%s<span>%02d</span></a>' % (p, href, label, i + 1) for i, (href, label, _) in enumerate(NAV))
    full_title = title if home else "%s | Intercientifica" % title
    mast_cls = "mast is-on-red" if home else "mast"
    base_tag = '<base href="%s">\n' % BASE_PATH if base == "" and rel == "404.html" else ""
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
%s<script>document.documentElement.classList.add('js')</script>
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="theme-color" content="#DE1E18">
<meta property="og:type" content="%s">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Intercientifica">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%sassets/img/og-share.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="%sassets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="%sassets/img/favicon-192.png">
<link rel="apple-touch-icon" href="%sassets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="%s">
<link rel="stylesheet" href="%sassets/css/site.css">
%s</head>
<body>
%s
<a class="skip" href="#conteudo">Pular para o conteúdo</a>

<header class="%s" id="mast">
  <div class="wrap mast__in">
    <a class="mast__logo" href="%s" aria-label="Intercientifica, página inicial">
      <img class="logo-c" src="%sassets/img/logo.png" width="633" height="309" alt="">
      <img class="logo-w" src="%sassets/img/logo-white.png" width="633" height="309" alt="">
    </a>
    <nav class="mast__nav" aria-label="Principal">%s</nav>
    <div class="mast__end">
      <a class="mast__tel" href="tel:%s">%s<span>%s</span></a>
      <a class="btn btn--red mast__cta" href="%scontato/">Falar com a equipe</a>
    </div>
    <button class="mast__menu" type="button" aria-expanded="false" aria-controls="sheet"><i aria-hidden="true"></i>Menu</button>
  </div>
</header>

<div class="sheet on-red" id="sheet" role="dialog" aria-modal="true" aria-label="Menu" hidden>
  <div class="sheet__top">
    <img src="%sassets/img/logo-white.png" width="633" height="309" alt="Intercientifica">
    <button class="sheet__close" type="button">%sFechar</button>
  </div>
  <nav class="sheet__nav" aria-label="Menu principal"><a href="%s">Início<span>00</span></a>%s</nav>
  <div class="sheet__foot">
    <a href="tel:%s">%s</a>
    <a href="https://wa.me/%s" target="_blank" rel="noopener">WhatsApp %s</a>
    <a href="mailto:ic@intercientifica.com.br">ic@intercientifica.com.br</a>
  </div>
</div>

<main id="conteudo">
%s
</main>

%s

<div class="peek" id="peek" aria-hidden="true"><img alt="" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" width="300" height="225"></div>
<script src="%sassets/js/site.js" defer></script>
%s
</body>
</html>
""" % (base_tag, esc(full_title), esc(desc), url, og_type, esc(full_title), esc(desc), url, SITE_URL, p, p, p, FONTS, p, extra_head,
       SPRITE, mast_cls, p or "./", p, p, nav, PHONE, icon("phone"), PHONE_LABEL[4:], p,
       p, icon("close"), p or "./", sheet_nav, PHONE, PHONE_LABEL, WHATSAPP, WHATSAPP_LABEL,
       body, colophon(p), p, scripts)


def colophon(p):
    links = "".join('<li><a href="%s%s">%s</a></li>' % (p, h, l) for h, l, _ in NAV)
    kits = "".join('<li><a href="%sprodutos/%s/">%s</a></li>' % (p, x["slug"], esc(x["name"])) for x in PRODUCTS[:5])
    kits += '<li><a href="%sprodutos/">Todos os kits</a></li>' % p
    mails = "".join('<li><a href="mailto:%s">%s</a></li>' % (m, m) for _, m in EMAILS[:3])
    return """<footer class="colophon on-dark">
  <div class="wrap">
    <div class="colophon__grid">
      <div class="maker">
        <svg aria-hidden="true"><use href="#i-factory"/></svg>
        <address>
          <strong>Intercientifica</strong>
          %s<br>
          <a href="tel:%s">%s</a> · %s
        </address>
      </div>
      <nav aria-label="Rodapé"><h2>Navegação</h2><ul>%s</ul></nav>
      <nav aria-label="Kits"><h2>Kits</h2><ul>%s</ul></nav>
      <div class="colophon__contact"><h2>Contato</h2><ul class="mails">%s</ul>
        <div class="social"><a href="%s" target="_blank" rel="noopener" aria-label="Instagram da Intercientifica">%s</a><a href="%s" target="_blank" rel="noopener" aria-label="Facebook da Intercientifica">%s</a></div>
      </div>
    </div>
    <div class="colophon__base">
      <span>© %d Intercientifica. Fabricação nacional desde 1994.</span>
      <span>Proposta de redesign desenvolvida por <a href="https://apxweb.github.io/apex-web/" target="_blank" rel="noopener">Apex Web</a>.</span>
    </div>
  </div>
</footer>""" % ("<br>".join(ADDRESS_LINES[:3]), PHONE, PHONE_LABEL, HOURS, links, kits, mails, INSTAGRAM, icon("ig"), FACEBOOK, icon("fb"), YEAR)


# ---------------------------------------------------------------- publicações
inv = json.load(io.open(os.path.join(HERE, "data/ic_inventory.json"), encoding="utf-8"))
scraped = {x["url"]: x for x in json.load(io.open(os.path.join(HERE, "data/ic_posts_full.json"), encoding="utf-8"))}
POST_LINKS = json.load(io.open(os.path.join(HERE, "data/ic_post_links.json"), encoding="utf-8"))
PDF_MAP = json.load(io.open(os.path.join(HERE, "data/ic_pdf_map.json"), encoding="utf-8"))
BROKEN_TITLES = {
    "c%C3%B3pia-a-import%C3%A2ncia-da-triagem-neona": "Dia Mundial de doenças raras",
    "c%C3%B3pia-a-doen%C3%A7a-da-urina-do-xarope-de": "A importância da Triagem Neonatal para o Hipotiroidismo Congênito (HC)",
}
MONTHS = {"jan": "01", "fev": "02", "mar": "03", "abr": "04", "mai": "05", "jun": "06", "jul": "07", "ago": "08", "set": "09", "out": "10", "nov": "11", "dez": "12"}


def fix_href(href):
    href = (href or "").strip()
    if href in PDF_MAP:
        return "../../" + PDF_MAP[href]
    if re.search(r"intercientifica\.com\.br/wp-content/", href):
        return None
    if re.fullmatch(r"https?://(www\.)?intercientifica\.com\.br/?", href):
        return "../../"
    return href


posts = []
for kind, items in (("noticia", inv["noticias_items"]), ("artigo", inv["artigos_items"])):
    for i, n in enumerate(items):
        post = scraped.get(n["href"], {})
        key = n["href"].rstrip("/").rsplit("/", 1)[-1]
        if kind == "noticia":
            ok = bool(post) and "404" not in (post.get("meta", {}).get("title") or "") and len(post.get("blocks", [])) > 2
            title = None
            if ok:
                heads = [clean(b["text"]) for b in post["blocks"] if b["t"] in ("h1", "h2") and clean(b.get("text"))]
                title = heads[0] if heads else None
            title = title or BROKEN_TITLES.get(key) or clean(n["block"]).replace("Ler mais", "").split(". ")[0]
            listing = clean(n["block"]).replace("Ler mais", "").strip()
        else:
            title = clean(n["title"])
            ok = bool(post) and len(post.get("bodyText", "")) > 80
            listing = clean(n["block"])
        if listing.startswith(title):
            listing = listing[len(title):].strip()
        date = clean(post.get("meta", {}).get("date")) if post else ""
        iso = ""
        m = re.match(r"(\d+) de (\w{3})\.? de (\d{4})", date)
        if m:
            iso = "%s-%s-%02d" % (m.group(3), MONTHS.get(m.group(2), "01"), int(m.group(1)))
        img = None
        if kind == "noticia" and os.path.exists(os.path.join(ROOT, "assets/img/noticias/%d-640.webp" % i)):
            img = "assets/img/noticias/%d-640.webp" % i
        posts.append({"kind": kind, "i": i, "title": title, "slug": slugify(title), "ok": ok, "post": post,
                      "listing": listing, "date": date, "iso": iso, "img": img})

seen = {}
for it in posts:
    base, k = it["slug"], 2
    while it["slug"] in seen:
        it["slug"] = "%s-%d" % (base, k); k += 1
    seen[it["slug"]] = 1


DASH_FIXES = [
    ("carreira — e a saúde", "carreira, e a saúde"),
    ("Microlab Nimbus —, incluindo", "Microlab Nimbus (incluindo"),
    ("amostras medianas, e corte flutuante — com capacidade", "amostras medianas e corte flutuante), com capacidade"),
]


def no_dashes(t):
    for a, b in DASH_FIXES:
        t = t.replace(a, b)
    return t


def render_blocks(it):
    post = it["post"]
    blocks = post.get("blocks", [])
    title_c = clean(it["title"]).lower()
    pdf_texts = {clean(b.get("text")) for b in blocks if b["t"] == "pdf"}
    items = []
    for b in blocks:
        t = b["t"]
        if t in ("h1", "h2", "h3", "h4", "p", "li", "blockquote"):
            txt = clean(b.get("text"))
            if not txt or txt.lower() == title_c or txt in pdf_texts or txt.lower() in ("ler mais", "ver tudo", "posts recentes", "compartilhar"):
                continue
            items.append({"t": t, "text": no_dashes(txt), "links": b.get("links") or []})
        elif t in ("img", "pdf", "iframe"):
            items.append(b)
    merged = []
    for x in items:
        prev = merged[-1] if merged else None
        if prev and prev["t"] == "p" and x["t"] == "p" and not re.search(r"[.!?:;)\]\"”…]$", prev["text"]) and re.match(r"^[a-zà-ú0-9(]", x["text"]):
            prev["text"] += " " + x["text"]; prev["links"] = prev["links"] + x["links"]
        else:
            merged.append(dict(x))
    out, cover, n_img, in_list = [], None, 0, False
    for x in merged:
        t = x["t"]
        if t != "li" and in_list:
            out.append("</ul>"); in_list = False
        if t == "img":
            n_img += 1
            path = "assets/img/posts/%s-%d.webp" % (it["slug_p1"], n_img)
            if not os.path.exists(os.path.join(ROOT, path)):
                continue
            from PIL import Image
            w, h = Image.open(os.path.join(ROOT, path)).size
            alt = "Imagem da publicação: %s" % it["title"] if n_img == 1 else "Imagem %d da publicação: %s" % (n_img, it["title"])
            tag = '<img src="../../%s" width="%d" height="%d" alt="%s"%s>' % (path, w, h, esc(alt), "" if cover is None and n_img == 1 else ' loading="lazy"')
            if cover is None and n_img == 1 and len(out) <= 1:
                cover = '<figure class="post__cover">%s</figure>' % tag
            else:
                out.append("<figure>%s</figure>" % tag)
        elif t == "pdf":
            href = fix_href(x.get("href"))
            if not href:
                continue
            label = x.get("text") or ""
            if re.match(r"https?://", label):
                label = "Documento em " + re.sub(r"^www\.", "", re.match(r"https?://([^/]+)", label).group(1))
            label = "Ver o artigo completo (PDF)" if label.lower() in ("ver o artigo completo", ".pdf") or len(label) < 4 else label + " (PDF)"
            out.append('<p class="post__dl"><a class="btn btn--line" href="%s" target="_blank" rel="noopener">%s%s</a></p>' % (esc(href), esc(label), icon("file")))
        elif t == "iframe":
            src = x.get("src") or ""
            if "youtube" in src:
                out.append('<div class="video"><iframe src="%s" title="Vídeo da publicação" loading="lazy" allowfullscreen></iframe></div>' % esc(src))
        else:
            body = esc(x["text"])
            for link in x["links"]:
                lt, href = clean(link.get("text")), fix_href(link.get("href"))
                if not lt or not href:
                    continue
                ext = "" if href.startswith(("mailto:", "../")) and not href.endswith(".pdf") else ' target="_blank" rel="noopener"'
                body = body.replace(esc(lt), '<a href="%s"%s>%s</a>' % (esc(href), ext, esc(lt)), 1)
            if t == "li":
                if not in_list:
                    out.append("<ul>"); in_list = True
                out.append("<li>%s</li>" % body)
            elif t in ("h1", "h2"):
                out.append("<h2>%s</h2>" % body)
            elif t in ("h3", "h4"):
                out.append("<h3>%s</h3>" % body)
            elif t == "blockquote":
                out.append("<blockquote><p>%s</p></blockquote>" % body)
            else:
                out.append("<p>%s</p>" % body)
    if in_list:
        out.append("</ul>")
    known = {b.get("href") for b in blocks if b["t"] == "pdf"}
    for b in blocks:
        for lk in b.get("links") or []:
            known.add(lk.get("href"))
    added = set()
    for lk in POST_LINKS.get(post.get("url"), []):
        href = (lk.get("href") or "").strip()
        text = clean(lk.get("text"))
        if not href or href in known or href in added or href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        mapped = fix_href(href)
        if not mapped or mapped == "../../" or re.search(r"^https?://(www\.)?intercientifica\.com\.br", mapped):
            continue
        added.add(href)
        is_pdf = mapped.lower().split("?")[0].endswith(".pdf") or "usrfiles.com/ugd/" in mapped
        label = text if text and text.lower() != title_c and len(text) >= 4 else "Ver o artigo completo"
        if re.match(r"https?://", label):
            label = "Abrir a fonte em " + re.sub(r"^www\.", "", re.match(r"https?://([^/]+)", label).group(1))
        if is_pdf and "(PDF)" not in label:
            label += " (PDF)"
        out.append('<p class="post__dl"><a class="btn btn--line" href="%s" target="_blank" rel="noopener">%s%s</a></p>' % (esc(mapped), esc(label), icon("file" if is_pdf else "ext")))
    return cover, "\n        ".join(out)


# As imagens dos posts foram baixadas pela ferramenta da Proposta 1 com o slug dela.
for it in posts:
    t = it["title"]
    it["slug_p1"] = "teste-do-pezinho-ampliado" if t.startswith("Teste do Pezinho será ampliado") else slugify(t)

news = [x for x in posts if x["kind"] == "noticia"]
articles = [x for x in posts if x["kind"] == "artigo"]


def post_desc(it, body_html):
    paras = [html.unescape(re.sub(r"<[^>]+>", "", m)) for m in re.findall(r"<p>(.*?)</p>", body_html, re.S)]
    good = [t for t in paras if len(clean(t)) >= 80]
    return excerpt(good[0] if good else html.unescape(it["listing"]) or it["title"], 155)


rendered = {}
for it in posts:
    if it["ok"]:
        cover, body = render_blocks(it)
        rendered[it["slug"]] = (cover, body)
        it["excerpt"] = post_desc(it, body)
    else:
        it["excerpt"] = excerpt(html.unescape(it["listing"]), 160)


def related_posts(keywords, limit=5):
    out = []
    for it in posts:
        hay = (it["title"] + " " + it.get("excerpt", "")).lower()
        if it["ok"] and any(k in hay for k in keywords):
            out.append(it)
    return out[:limit]


# ---------------------------------------------------------------- figuras estáticas das microesferas
# Mesmas formações que o WebGL desenha; servem sem JavaScript, sem WebGL e com
# movimento reduzido. Representação ilustrativa, não um dado real.
BEAD_COLORS = ["#FF5A47", "#FFB547", "#5FD3C2", "#9DAAFF"]


def formation_svg(step, n=260, seed=7):
    rnd = random.Random(seed)
    W, H = 800, 600
    pts = []
    for i in range(n):
        g = i % 4
        if step == 0:      # coleta: mancha no papel-filtro
            a, r = rnd.random() * math.tau, math.sqrt(rnd.random()) * 150
            pts.append((400 + math.cos(a) * r * 1.05, 290 + math.sin(a) * r, 3.4 + rnd.random() * 2.6, "#7A1712", 0.55 + rnd.random() * 0.4))
        elif step == 1:    # picote: um disco
            a, r = rnd.random() * math.tau, math.sqrt(rnd.random()) * 70
            pts.append((400 + math.cos(a) * r, 290 + math.sin(a) * r * 0.45, 3 + rnd.random() * 2.2, "#B8BFC7", 0.6 + rnd.random() * 0.4))
        elif step == 2:    # ensaio: nuvem com quatro conjuntos
            a, r = rnd.random() * math.tau, math.sqrt(rnd.random()) * 230
            pts.append((400 + math.cos(a) * r * 1.3, 290 + math.sin(a) * r * 0.9, 3 + rnd.random() * 3.5, BEAD_COLORS[g], 0.5 + rnd.random() * 0.5))
        else:              # leitura: mapa de classificação
            cx, cy = [(260, 400), (400, 260), (540, 330), (620, 190)][g]
            a, r = rnd.random() * math.tau, abs(rnd.gauss(0, 1)) * 26
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r, 3 + rnd.random() * 1.8, BEAD_COLORS[g], 0.65 + rnd.random() * 0.35))
    circles = "".join('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity="%.2f"/>' % p for p in pts)
    return '<svg class="plate-svg%s" data-plate="%d" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" aria-hidden="true">%s</svg>' % (" is-on" if step == 0 else "", step, W, H, circles)


def hero_svg():
    rnd = random.Random(3)
    out = []
    for i in range(220):
        a, r = rnd.random() * math.tau, math.sqrt(rnd.random()) * 300
        z = rnd.random()
        col = BEAD_COLORS[i % 4] if i % 5 == 0 else "#C9CFD6"
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity="%.2f"/>' % (300 + math.cos(a) * r, 340 + math.sin(a) * r * 1.2, 2 + z * 6, col, 0.25 + z * 0.65))
    return '<svg class="plate-svg" viewBox="0 0 600 680" preserveAspectRatio="xMidYMid slice" aria-hidden="true">%s</svg>' % "".join(out)


# ---------------------------------------------------------------- blocos reutilizáveis
def kits_table(p, products, catalog=False):
    rows = []
    for x in products:
        pres = "<br>".join(r for _, r in x["pres"])
        sig = "<br>".join(d for d, _ in x["pres"])
        search = " ".join([x["name"], x["short"], x["targets"], " ".join(x["diseases"]), " ".join(r for _, r in x["pres"]), LINES[x["line"]]["name"], x["assay"]])
        thumb = ""
        fmt = ""
        if catalog:
            thumb = '<td class="kit-thumb" aria-hidden="true"><span><img src="%sassets/img/produtos/%s-480.webp" width="80" height="60" alt="" loading="lazy"></span></td>' % (p, x["img"])
            fmt = '<td class="c-fmt"><span class="kit-fmt">%s</span></td>' % esc(", ".join(f.capitalize() for f in x["formats"]))
        rows.append("""<tr data-line="%s" data-formats="%s" data-search="%s" data-img="%sassets/img/produtos/%s-480.webp">
  %s<td class="c-name"><a class="row-link" href="%sprodutos/%s/"><span class="kit-name">%s<small>%s</small></span></a></td>
  <td class="c-line"><span class="kit-line">%s</span></td>
  %s<td class="c-ref" data-k="Referência"><span class="kit-ref">%s</span></td>
  <td class="c-sig" data-k="Determinações"><span class="kit-sig">%s</span></td>
  <td class="c-go kit-go"><span>%s</span></td>
</tr>""" % (x["line"], " ".join(x["formats"]), esc(search), p, x["img"], thumb, p, x["slug"], reg(x["name"]), esc(x["ind"] if catalog else x["targets"]),
            reg(LINES[x["line"]]["name"] + "®"), fmt, pres, sig, icon("arrow")))
    head_extra = '<th scope="col" class="kit-thumb"><span class="sr-only">Imagem</span></th>' if catalog else ""
    fmt_head = '<th scope="col" class="c-fmt">Formato</th>' if catalog else ""
    return """<table>
  <caption class="sr-only">Kits Intercientifica: nome, linha, referência e número de determinações</caption>
  <thead><tr>%s<th scope="col">Kit</th><th scope="col" class="c-line">Linha</th>%s<th scope="col" class="c-sym">%s Referência</th><th scope="col" class="c-sym">%s Determinações</th><th scope="col"><span class="sr-only">Abrir</span></th></tr></thead>
  <tbody>
%s
  </tbody>
</table>""" % (head_extra, fmt_head, ref_sym(), icon("sigma"), "\n".join(rows))


def close_block(p, title="Fale com a equipe científica.", lead="Para saber mais sobre nossos produtos, solicitar informações técnicas ou comerciais, entre em contato com nossa equipe."):
    return """<section class="close on-red" aria-labelledby="close-title">
  <div class="wrap">
    <h2 id="close-title" data-r="print">%s</h2>
    <p class="close__lead" data-r="up">%s</p>
    <div class="close__actions" data-r="up" style="--i:1">
      <a class="btn btn--white" href="%scontato/">Enviar mensagem%s</a>
      <a class="btn btn--line-light" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">%sWhatsApp</a>
    </div>
    <div class="channels">
      <a href="tel:%s"><span class="field__k">%sTelefone</span><span class="field__v">%s</span><span class="field__k">%s</span></a>
      <a href="mailto:ic@intercientifica.com.br"><span class="field__k">%sEquipe científica</span><span class="field__v">ic@intercientifica.com.br</span></a>
      <a href="mailto:b2c@intercientifica.com.br"><span class="field__k">%sEquipe comercial</span><span class="field__v">b2c@intercientifica.com.br</span></a>
      <a href="%s" target="_blank" rel="noopener"><span class="field__k">%sEndereço</span><span class="field__v field__v--text">Parque Tecnológico UNIVAP, São José dos Campos, SP</span></a>
    </div>
  </div>
</section>""" % (title, lead, p, icon("arrow"), WHATSAPP, "Ol%C3%A1!%20Vim%20pelo%20site%20da%20Intercientifica.", icon("wa"),
             PHONE, icon("phone"), PHONE_LABEL, HOURS, icon("mail"), icon("mail"), MAPS_LINK, icon("pin"))


def index_rows(p, items, show_kind=False):
    rows = []
    for it in items:
        when = it["date"] or ("Notícia" if it["kind"] == "noticia" else "Artigo")
        kind = "Artigo" if it["kind"] == "artigo" else "Notícia"
        inner = '<span class="when">%s</span><span class="t">%s<small>%s</small></span><span class="kind">%s%s</span>' % (
            esc(when) if it["kind"] == "artigo" else "Arquivo", esc(it["title"]), esc(excerpt(it.get("excerpt", ""), 150)),
            kind if show_kind else "", icon("arrow") if it["ok"] else "")
        if it["ok"]:
            rows.append('<li data-kind="%s" data-search="%s"><a href="%spublicacoes/%s/">%s</a></li>' % (it["kind"], esc(it["title"] + " " + it.get("excerpt", "")), p, it["slug"], inner))
        else:
            rows.append('<li data-kind="%s" data-search="%s"><div class="noref">%s</div></li>' % (it["kind"], esc(it["title"] + " " + it.get("excerpt", "")), inner))
    return '<ol class="index-list">%s</ol>' % "".join(rows)
