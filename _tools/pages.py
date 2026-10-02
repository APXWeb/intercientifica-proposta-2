"""Ponto de entrada do gerador. Rode da raiz do projeto:

    python _tools/pages.py
"""
from build import *  # noqa: F401,F403  (moldura, dados e blocos)



# ================================================================ AUTOMAÇÃO 3D (Opentrons Flex)
AUTO_STEPS = [("intro", "Apresentação"), ("estrutura", "Estrutura"), ("deck", "Deck"), ("portico", "Pórtico"), ("interface", "Interface"), ("final", "Composição final")]
IMPORTMAP = """<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.min.js"}}</script>
<link rel="modulepreload" href="https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.min.js" crossorigin>
"""
# Marcadores projetados sobre o modelo: (texto, ponto x,y,z em metros, poses, peça móvel)
AUTO_PINS = [
    ("87 cm", "0,-0.05,0.405", "estrutura", "tag"),
    ("84 cm", "-0.505,0.42,0.345", "estrutura", "tag"),
    ("69 cm", "0.505,-0.05,0", "estrutura", "tag"),
    ("A1", "-0.19,0.16,-0.16", "deck", "tag"),
    ("A3", "0.138,0.16,-0.16", "deck", "tag minor"),
    ("D1", "-0.19,0.16,0.161", "deck", "tag minor"),
    ("D3", "0.138,0.16,0.161", "deck", "tag"),
    ("Coluna 4", "0.302,0.17,-0.053", "deck", "tag"),
    ("Pórtico · X e Y", "-0.3,0.55,0", "portico", "carriage"),
    ("Pipetas · eixo Z", "0,0.32,0.16", "portico", "carriage"),
    ("Tela de 7″", "0.33,0.6,0.37", "interface", ""),
    ("Luz de status", "0.12,0.81,0.35", "interface", ""),
    ("Câmera 2 MP", "-0.385,0.81,0.35", "interface", ""),
]


def pins_html():
    return "".join('<span class="pin%s" data-pin="%s" data-for="%s"%s><i></i><b>%s</b></span>' % (
        (" pin--tag" if part.startswith("tag") else "") + (" pin--minor" if "minor" in part else ""), pt, poses, (' data-part="%s"' % part) if part == "carriage" else "", esc(label)) for label, pt, poses, part in AUTO_PINS)


def rail_html():
    return "".join('<button type="button" data-go="%s" aria-current="%s"><span>%02d</span>%s</button>' % (
        k, "step" if i == 0 else "false", i + 1, esc(l)) for i, (k, l) in enumerate(AUTO_STEPS))


def stills_html():
    alts = {
        "intro": "Opentrons Flex em vista de três quartos, com moldura preta e laterais em alumínio",
        "estrutura": "Opentrons Flex com a porta frontal de policarbonato se abrindo e as cotas de 87, 84 e 69 centímetros",
        "deck": "Vista de cima do deck do Opentrons Flex com as posições de trabalho destacadas",
        "portico": "Pórtico do Opentrons Flex com o carro das pipetas sobre o deck",
        "interface": "Detalhe da tela sensível ao toque e da luz de status do Opentrons Flex",
        "final": "Opentrons Flex em composição final, de frente",
    }
    return "".join('<img data-still="%s" class="%s" src="assets/img/flex/%s-1600.webp" srcset="assets/img/flex/%s-800.webp 800w, assets/img/flex/%s-1600.webp 1600w" sizes="100vw" width="1600" height="1000" alt="%s" loading="%s" decoding="async">' % (
        k, "is-on" if i == 0 else "", k, k, k, alts[k], "eager" if i == 0 else "lazy") for i, (k, _) in enumerate(AUTO_STEPS))


# ================================================================ HOME
def ledger_rows():
    data = [
        ("até", "85%", 15, 85, "menos consumo médio de reagentes", ""),
        ("", "58%", 42, 58, "menos consumo de energia elétrica", ""),
        ("mais de", "75%", 25, 75, "menos plástico, papel, etiquetas e microplacas", "com o NeoMAP® 4PLEX"),
        ("mais de", "50%", 50, 50, "de redução no tempo de processamento", ""),
    ]
    out = []
    for pre, v, keep, cut, label, sub in data:
        spoken = {"até": "até %s de redução" % v, "mais de": "mais de %s de redução" % v, "": "%s de redução" % v}[pre]
        out.append("""<div class="lrow" data-r="up">
        <p class="lrow__v"><small>%s</small>%s</p>
        <p class="lrow__l">%s%s</p>
        <div class="bar-wrap" role="img" aria-label="%s: %s em relação a outras metodologias">
          <div class="bar" style="--keep:%dfr;--cut:%dfr"><span class="bar__keep"></span><span class="bar__cut">−%s</span></div>
          <div class="bar__scale" aria-hidden="true"><span>0</span><span>100 = outras metodologias</span></div>
        </div>
      </div>""" % (pre or "&nbsp;", v, esc(label), ('<span>%s</span>' % esc(sub)) if sub else "", esc(label.capitalize()), spoken, keep, cut, v))
    return "\n      ".join(out)


def build_home():
    p = ""
    recent = [x for x in articles if x["ok"]][:5]
    keys = "".join("<span></span>" for _ in range(12))
    dz = lambda line: "".join("<li>%s</li>" % esc(d) for d in LINES[line]["diseases"])
    analytes = "".join('<li><i style="background:%s"></i>%s</li>' % (c, a) for c, a in zip(BEAD_COLORS, ["TSH", "T4", "17-OH", "IRT"]))
    milestone = next(x for x in news if x["title"].startswith("1.750.300"))
    consumo = next((x for x in articles if x["title"].startswith("Consumo de Reagentes")), None)
    ctx = {
        "keys": keys, "factory": icon("factory", "sym-svg"), "arrow": icon("arrow"), "sigma": icon("sigma"), "down": icon("down"),
        "phone": PHONE_LABEL, "analytes": analytes, "milestone": milestone["slug"],
        "plate3": formation_svg(3).replace('class="plate-svg"', 'class="plate-svg is-on"'),
        "stills": stills_html(), "pins": pins_html(), "rail": rail_html(),
        "c0": BEAD_COLORS[0], "c1": BEAD_COLORS[1], "c2": BEAD_COLORS[2], "c3": BEAD_COLORS[3],
        "ledger": ledger_rows(),
        "consumo": (' Estudo relacionado: <a href="publicacoes/%s/">%s</a>.' % (consumo["slug"], esc(consumo["title"]))) if consumo and consumo["ok"] else "",
        "neomap_desc": reg(LINES["neomap"]["desc"]), "neolisa_desc": reg(LINES["neolisa"]["desc"]),
        "neomap_dz": dz("neomap"), "neolisa_dz": dz("neolisa"),
        "table": kits_table(p, PRODUCTS),
        "qa": "".join('<div class="reg-row" data-r="up" style="--i:%d"><dt>%s</dt><dd>%s</dd><dd class="where">%s</dd></div>' % (i, a, esc(b), c) for i, (a, b, c) in enumerate(QA_PROGRAMS)),
        "n_art": len(articles), "n_news": len(news), "recent": index_rows(p, recent), "close": close_block(p),
        "kit_q": "Informa%C3%A7%C3%B5es%20sobre%20um%20kit",
    }
    body = HOME_TEMPLATE % ctx
    write("index.html", page("index.html", "Intercientifica | Triagem neonatal e pré-natal, feita no Brasil",
                             "Kits NeoMAP® e NeoLISA®, reagentes, softwares e cartões de coleta para triagem neonatal e pré-natal. Fabricação nacional desde 1994, em São José dos Campos, SP.",
                             body, home=True, extra_head=IMPORTMAP,
                             scripts='<script type="module" src="assets/js/flex.js"></script>\n<script type="module" src="assets/js/multiplex.js"></script>'))


HOME_TEMPLATE = """
<section class="box on-red" aria-labelledby="hero-title">
  <div class="box__keys" aria-hidden="true"><div class="wrap"><div class="grid">%(keys)s</div></div></div>
  <div class="wrap box__in">
    <div class="label">
      <div class="label__row label__row--head">
        <div class="label__maker">%(factory)s<span>Intercientifica<br><span class="muted">São José dos Campos, SP</span></span></div>
        <div class="field"><span class="field__k">Desde</span><span class="field__v code">1994</span></div>
        <div class="field"><span class="field__k">Certificação</span><span class="field__v">Boas Práticas de Fabricação ANVISA</span></div>
      </div>
      <div class="label__body">
        <h1 id="hero-title"><span class="ln"><span>Triagem neonatal</span></span><span class="ln"><span>e pré-natal,</span></span><span class="ln"><span class="red">feita no Brasil.</span></span></h1>
        <p class="label__lead label__fade">Desde 1994, a Intercientifica pesquisa, desenvolve e fabrica kits, reagentes, softwares e cartões de coleta personalizados para laboratórios.</p>
        <div class="label__actions label__fade">
          <a class="btn" href="produtos/">Ver catálogo de kits%(arrow)s</a>
          <a class="btn btn--line" href="contato/">Falar com a equipe científica</a>
        </div>
      </div>
      <div class="label__row label__row--foot">
        <div class="field"><span class="field__k">Linhas</span><span class="field__v">NeoMAP® · NeoLISA®</span></div>
        <div class="field"><span class="field__k">%(sigma)s Kits no catálogo</span><span class="field__v code">9</span></div>
        <div class="field"><span class="field__k">Fabricação</span><span class="field__v">100%% nacional</span></div>
      </div>
    </div>
    <figure class="window window--photo on-dark">
      <img src="assets/img/lab/99eb321d-1080.webp" srcset="assets/img/lab/99eb321d-540.webp 540w, assets/img/lab/99eb321d-1080.webp 1080w" sizes="(max-width: 1100px) 100vw, 40vw" width="1080" height="882" alt="Pipeta multicanal dispensando reagente em uma microplaca no laboratório da Intercientifica" fetchpriority="high">
      <span class="window__corner window__corner--tl" aria-hidden="true"></span>
      <span class="window__corner window__corner--tr" aria-hidden="true"></span>
      <figcaption class="window__cap"><span>Laboratório da Intercientifica</span><a class="window__go" href="#automacao-3d">Automação, de perto%(down)s</a></figcaption>
    </figure>
  </div>
  <div class="box__foot">
    <div class="wrap"><a href="#automacao-3d">%(down)sAutomação, de perto</a><span>%(phone)s · ic@intercientifica.com.br</span></div>
  </div>
</section>

<section class="auto on-dark" id="automacao-3d" aria-labelledby="auto3d-title">
  <div class="auto__stage">
    <div class="auto__still" aria-hidden="true">%(stills)s</div>
    <canvas aria-hidden="true"></canvas>
    <div class="auto__pins" aria-hidden="true">%(pins)s</div>
    <nav class="auto__rail" aria-label="Etapas da exploração do equipamento">%(rail)s</nav>
  </div>
  <div class="auto__steps">
    <article class="auto__step" data-pose="intro">
      <div class="auto__card">
        <h2 id="auto3d-title">Automação, de perto.</h2>
        <p>A Intercientifica oferece soluções de automação completa para as linhas NeoLISA® e NeoMAP®, com sistemas Hamilton® Robotics e Opentrons®. O equipamento mostrado é um Opentrons® Flex, como exemplo de plataforma.</p>
        <p class="auto__note">Representação 3D ilustrativa, baseada nas especificações publicadas pela Opentrons.</p>
        <p class="auto__hint">%(down)sRole para explorar o equipamento</p>
      </div>
    </article>
    <article class="auto__step" data-pose="estrutura">
      <div class="auto__card">
        <h3>Uma estação fechada.</h3>
        <p>Estrutura rígida de aço e alumínio usinado, com 87 × 69 × 84 cm. A porta frontal e as janelas laterais são de policarbonato, removíveis, e a porta se abre para dar acesso ao interior.</p>
      </div>
    </article>
    <article class="auto__step" data-pose="deck">
      <div class="auto__card">
        <h3>Doze posições de trabalho.</h3>
        <p>O deck de alumínio usinado tem 12 posições no padrão ANSI/SLAS, de A1, no fundo à esquerda, a D3, na frente à direita. A coluna 4 é uma área de apoio que só a garra alcança.</p>
      </div>
    </article>
    <article class="auto__step" data-pose="portico">
      <div class="auto__card">
        <h3>Movimento nos três eixos.</h3>
        <p>O pórtico se desloca nos eixos X e Y com precisão de 0,1 mm e leva as montagens das pipetas e da garra. Motores de passo controlam o eixo Z.</p>
      </div>
    </article>
    <article class="auto__step" data-pose="interface">
      <div class="auto__card">
        <h3>Operação na própria máquina.</h3>
        <p>Tela sensível ao toque de 7 polegadas na frente, à direita, faixa de luz de status no topo e câmera de 2 MP para fotos e vídeos.</p>
      </div>
    </article>
    <article class="auto__step" data-pose="final">
      <div class="auto__card">
        <h3>Automação para a rotina do seu laboratório.</h3>
        <p>A solução de automação para cada laboratório é definida com a equipe da Intercientifica, de acordo com os kits NeoLISA® e NeoMAP® e o fluxo de trabalho.</p>
        <div class="auto__actions"><a class="btn btn--red" href="contato/?assunto=Equipamentos%%20e%%20automa%%C3%%A7%%C3%%A3o">Consultar automação%(arrow)s</a></div>
        <p class="auto__src">Especificações do equipamento: <a href="https://docs.opentrons.com/flex/" target="_blank" rel="noopener">manual do Opentrons Flex</a>.</p>
      </div>
    </article>
  </div>
</section>


<section class="section ledger" aria-labelledby="ledger-title">
  <div class="wrap">
    <div class="head">
      <h2 id="ledger-title" data-r="print">Menos insumos por resultado.</h2>
      <p data-r="up">Kits NeoMAP® comparados a outras metodologias disponíveis no mercado, segundo dados divulgados pela Intercientifica.</p>
    </div>
    <div class="ledger__rows">
      %(ledger)s
    </div>
    <p class="ledger__src">A barra escura mostra o consumo restante em relação a outras metodologias (100). Onde a fonte diz “até” ou “mais de”, a barra marca esse limite, não um valor medido. Fontes: textos “Nosso compromisso” e “Nossos produtos” do site oficial e a publicação <a href="publicacoes/%(milestone)s/">1.750.300 análises já realizadas com o Kit NeoMAP® 4PLEX</a>.%(consumo)s</p>
    <dl class="facts">
      <div class="facts__row" data-r="up"><dt>Análises produzidas desde 1994</dt><dd class="facts__v">mais de 48 milhões</dd><dd class="facts__src">Informado pela Intercientifica no site oficial.</dd></div>
      <div class="facts__row" data-r="up"><dt>Análises com o NeoMAP® 4PLEX</dt><dd class="facts__v">1.750.300</dd><dd class="facts__src">Marco divulgado em <a href="publicacoes/%(milestone)s/">publicação da empresa</a>.</dd></div>
      <div class="facts__row" data-r="up"><dt>Precisão dos kits NeoMAP®</dt><dd class="facts__v">50 a 100 vezes maior</dd><dd class="facts__src">que os métodos fluorimétricos ELISA tradicionais, segundo a ficha dos kits.</dd></div>
    </dl>
  </div>
</section>

<section class="mplex on-dark" id="leitura" aria-labelledby="leitura-title">
  <div class="wrap mplex__grid">
    <div class="mplex__txt">
      <h2 id="leitura-title" data-r="print">Uma leitura, quatro marcadores.</h2>
      <p data-r="up">Nos kits NeoMAP®, na plataforma xMAP®, da Luminex®, os ensaios ocorrem <strong>dentro do mesmo orifício, em suspensão</strong>. Conjuntos de microesferas identificados por cor permitem ler vários analitos de uma mesma amostra.</p>
      <p data-r="up">Segundo a Intercientifica, com o NeoMAP® 4PLEX um único picote de 3,00 mm basta para os quatro marcadores, e o ensaio realiza <strong>25 leituras para cada parâmetro</strong>; o resultado final é a média dessas 25 réplicas.</p>
      <ul class="analytes" aria-label="Marcadores do NeoMAP® 4Plex">%(analytes)s</ul>
      <p class="mplex__src">Fonte: <a href="publicacoes/%(milestone)s/">1.750.300 análises já realizadas com o Kit NeoMAP® 4PLEX</a>, publicação da Intercientifica.</p>
    </div>
    <figure class="mplex__fig">
      <div class="stage mplex__stage" id="multiplex-stage" data-step="3">
        %(plate3)s
        <canvas aria-hidden="true"></canvas>
        <div class="stage__axes" aria-hidden="true"><div class="ax-x"></div><div class="ax-y"></div><span class="lx">classificação por cor</span><span class="ly">sinal</span></div>
        <div class="stage__tags" aria-hidden="true"><span data-tag="0" style="background:%(c0)s;left:32.5%%;top:66.7%%">TSH</span><span data-tag="1" style="background:%(c1)s;left:50%%;top:43.3%%">T4</span><span data-tag="2" style="background:%(c2)s;left:67.5%%;top:55%%">17-OH</span><span data-tag="3" style="background:%(c3)s;left:77.5%%;top:31.7%%">IRT</span></div>
      </div>
      <figcaption class="stage__cap mplex__cap">Mapa de classificação das microesferas. Representação ilustrativa, fora de escala; não reproduz um procedimento validado.</figcaption>
    </figure>
  </div>
</section>

<section class="section lines" id="linhas" aria-labelledby="linhas-title">
  <div class="wrap">
    <div class="head">
      <h2 id="linhas-title" data-r="print">Duas linhas, nove kits.</h2>
      <p data-r="up">Kits para triagem pré-natal e neonatal, desenvolvidos e fabricados no Brasil. Cada linha da tabela abre a ficha completa do kit.</p>
    </div>
    <div class="lines__pair">
      <div class="line">
        <figure class="line__box" data-r="plate"><img src="assets/img/produtos/neomap-4plex-900.webp" srcset="assets/img/produtos/neomap-4plex-480.webp 480w, assets/img/produtos/neomap-4plex-900.webp 900w" sizes="(max-width: 900px) 100vw, 45vw" width="900" height="532" alt="Caixa vermelha e frascos de reagentes do kit NeoMAP® 4Plex" loading="lazy"><figcaption class="img-cap">NeoMAP® 4Plex · REF. 16635-230</figcaption></figure>
        <h3 class="line__name">NeoMAP<span class="reg">®</span></h3>
        <p class="line__method">Ensaios multiplex</p>
        <p class="line__desc">%(neomap_desc)s</p>
        <ul class="line__dz" aria-label="Triagens atendidas pela linha NeoMAP">%(neomap_dz)s</ul>
      </div>
      <div class="line">
        <figure class="line__box" data-r="plate"><img src="assets/img/produtos/neolisa-msud-900.webp" srcset="assets/img/produtos/neolisa-msud-480.webp 480w, assets/img/produtos/neolisa-msud-900.webp 900w" sizes="(max-width: 900px) 100vw, 45vw" width="900" height="611" alt="Caixa vermelha e frascos de reagentes do kit NeoLISA® MSUD" loading="lazy"><figcaption class="img-cap">NeoLISA® MSUD · REF. 4570-200</figcaption></figure>
        <h3 class="line__name">NeoLISA<span class="reg">®</span></h3>
        <p class="line__method">Ensaios enzimáticos e colorimétricos</p>
        <p class="line__desc">%(neolisa_desc)s</p>
        <ul class="line__dz" aria-label="Triagens atendidas pela linha NeoLISA">%(neolisa_dz)s</ul>
      </div>
    </div>
    <div class="kits" data-peek>
      %(table)s
    </div>
    <p style="margin-top:32px"><a class="link" href="produtos/">Abrir o catálogo com filtros e busca%(arrow)s</a></p>
  </div>
</section>

<section class="section" id="automacao" aria-labelledby="sol-title">
  <div class="wrap">
    <h2 id="sol-title" class="sr-only">Automação e cartões de coleta</h2>
    <div class="solution">
      <figure class="solution__img" data-r="plate">
        <img src="assets/img/automacao-hamilton-1400.webp" srcset="assets/img/automacao-hamilton-700.webp 700w, assets/img/automacao-hamilton-1400.webp 1400w" sizes="(max-width: 900px) 100vw, 66vw" width="1400" height="1145" alt="Sistema automatizado de pipetagem em operação no laboratório" loading="lazy">
        <figcaption class="img-cap">Automação Hamilton®</figcaption>
      </figure>
      <div class="solution__txt">
        <h3 data-r="print">NIMBUS e NeoMAP® 4PLEX.</h3>
        <p data-r="up">O NeoMAP® 4PLEX e a automação utilizada com ele, o NIMBUS, da Hamilton® Robotics, estão registrados na ANVISA, segundo a Intercientifica.</p>
        <div class="field-row" data-r="up" style="--i:1">
          <div class="field"><span class="field__k">Placas ao mesmo tempo</span><span class="field__v code">até 8</span></div>
          <div class="field"><span class="field__k">Análises por rotina</span><span class="field__v code">mais de 3.000</span></div>
        </div>
        <p class="muted" style="font-size:var(--t-small)">Dados do equipamento automatizado oferecido com o NeoMAP® 4PLEX, segundo a Intercientifica.</p>
        <a class="link" href="produtos/#automacao">Automação no catálogo%(arrow)s</a>
      </div>
    </div>
    <div class="solution solution--flip">
      <figure class="solution__img" data-r="plate">
        <img src="assets/img/cartoes-coleta-1000.webp" srcset="assets/img/cartoes-coleta-600.webp 600w, assets/img/cartoes-coleta-1000.webp 1000w" sizes="(max-width: 900px) 100vw, 58vw" width="1000" height="1003" alt="Mãos com luvas picotando uma amostra de sangue seco em um cartão de coleta" loading="lazy">
        <figcaption class="img-cap">Cartões de coleta</figcaption>
      </figure>
      <div class="solution__txt">
        <h3 data-r="print">Cartões de coleta personalizados.</h3>
        <p data-r="up">Cartões de coleta de sangue personalizados para laboratórios, fabricados pela Intercientifica.</p>
        <a class="link" href="contato/?assunto=Assuntos%%20comerciais">Solicitar cartões para o seu laboratório%(arrow)s</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="qualidade" style="background:var(--paper-2)" aria-labelledby="qual-title">
  <div class="wrap">
    <div class="head head--stack">
      <h2 id="qual-title" data-r="print">Inspecionada por dentro, avaliada por fora.</h2>
    </div>
    <div class="registry">
      <div class="registry__lead" data-r="up">
        <p class="stmt">Laboratório, processos, procedimentos e registros atendem à certificação de <strong>Boas Práticas de Fabricação e Controle de Produtos para a Saúde, In Vitro Classes III e IV</strong>, por meio de inspeções periódicas da ANVISA.</p>
        <div class="registry__badge"><b>SBTEIM</b><span>Sócia fundadora da Sociedade Brasileira de Triagem Neonatal e Erros Inatos do Metabolismo.</span></div>
      </div>
      <div class="registry__table">
        <h3>Programas de controle externo de qualidade</h3>
        <dl>%(qa)s</dl>
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="pub-title">
  <div class="wrap">
    <div class="head">
      <h2 id="pub-title" data-r="print">Ciência publicada.</h2>
      <p data-r="up">%(n_art)d artigos científicos e %(n_news)d notícias publicados pela Intercientifica, com os PDFs originais quando disponíveis.</p>
    </div>
    %(recent)s
    <p style="margin-top:32px"><a class="link" href="publicacoes/">Todas as publicações%(arrow)s</a></p>
  </div>
</section>

%(close)s
"""


# ================================================================ PRODUTOS
def build_catalog():
    p = "../"
    n_map = sum(1 for x in PRODUCTS if x["line"] == "neomap")
    n_lisa = len(PRODUCTS) - n_map
    fmt_count = lambda f: sum(1 for x in PRODUCTS if f in x["formats"])
    body = """
<section class="ptop ptop--red on-red">
  <div class="wrap">
    <ol class="crumbs"><li><a href="../">Início</a></li><li aria-current="page">Produtos</li></ol>
    <h1 data-r="print">Catálogo de kits.</h1>
    <p class="ptop__lead">Nove kits em duas linhas: NeoMAP®, para ensaios multiplex na plataforma xMAP®, e NeoLISA®, para ensaios enzimáticos e colorimétricos. Filtre por linha ou formato de ensaio, ou busque por doença, marcador ou referência.</p>
  </div>
</section>

<div class="wrap">
  <form class="filters" id="filters" role="search" aria-label="Filtrar kits">
    <div class="filters__groups">
      <fieldset class="fgroup">
        <legend>Linha</legend>
        <div class="chips">
          <label class="chip"><input type="radio" name="line" value="" checked><span>Todas <small>%d</small></span></label>
          <label class="chip"><input type="radio" name="line" value="neomap"><span>NeoMAP® <small>%d</small></span></label>
          <label class="chip"><input type="radio" name="line" value="neolisa"><span>NeoLISA® <small>%d</small></span></label>
        </div>
      </fieldset>
      <fieldset class="fgroup">
        <legend>Formato do ensaio</legend>
        <div class="chips">
          <label class="chip"><input type="radio" name="format" value="" checked><span>Qualquer</span></label>
          <label class="chip"><input type="radio" name="format" value="manual"><span>Manual <small>%d</small></span></label>
          <label class="chip"><input type="radio" name="format" value="semiautomatizado"><span>Semiautomatizado <small>%d</small></span></label>
          <label class="chip"><input type="radio" name="format" value="automatizado"><span>Automatizado <small>%d</small></span></label>
        </div>
      </fieldset>
    </div>
    <div class="search">
      <label for="q">Buscar</label>
      <input id="q" name="q" type="search" placeholder="Doença, marcador, REF" autocomplete="off" enterkeyhint="search">
      %s
    </div>
  </form>
  <div class="results-bar"><p id="count" aria-live="polite" style="margin:0">9 kits</p><button type="button" id="reset" hidden>Limpar filtros</button></div>
  <div class="kits kits--catalog" data-peek>
    %s
  </div>
  <div class="empty" id="empty" hidden>
    <p>Nenhum kit corresponde a esses filtros. Tente outra palavra ou <button type="button" class="link" id="reset2" style="border:0;background:none;padding:0;cursor:pointer;font:inherit">limpe os filtros</button>. Se procura algo fora do catálogo, <a href="../contato/">fale com a equipe científica</a>.</p>
  </div>
</div>

<section class="section" id="automacao" aria-labelledby="auto-title">
  <div class="wrap">
    <div class="solution">
      <figure class="solution__img" data-r="plate">
        <img src="../assets/img/automacao-hamilton-1400.webp" srcset="../assets/img/automacao-hamilton-700.webp 700w, ../assets/img/automacao-hamilton-1400.webp 1400w" sizes="(max-width: 900px) 100vw, 66vw" width="1400" height="1145" alt="Sistema automatizado de pipetagem em operação no laboratório" loading="lazy">
        <figcaption class="img-cap">Automação</figcaption>
      </figure>
      <div class="solution__txt">
        <h2 id="auto-title" class="sr-only">Automação</h2>
        <h3 data-r="print">Automação completa.</h3>
        <p>Soluções de automação completa para as linhas NeoLISA® e NeoMAP®, utilizando o sistema da Hamilton® Robotics e Opentrons®.</p>
        <p>Segundo a Intercientifica, o equipamento automatizado oferecido com o NeoMAP® 4PLEX é compacto, de fácil operação, e permite realizar <strong>até oito placas ao mesmo tempo</strong>, com mais de 3.000 análises por rotina. O kit e a automação utilizada (NIMBUS) estão registrados na ANVISA.</p>
        <a class="btn" href="../contato/?assunto=Equipamentos%%20e%%20automa%%C3%%A7%%C3%%A3o">Consultar automação%s</a>
      </div>
    </div>
    <div class="solution solution--flip" id="cartoes">
      <figure class="solution__img" data-r="plate">
        <img src="../assets/img/cartoes-coleta-1000.webp" srcset="../assets/img/cartoes-coleta-600.webp 600w, ../assets/img/cartoes-coleta-1000.webp 1000w" sizes="(max-width: 900px) 100vw, 58vw" width="1000" height="1003" alt="Mãos com luvas picotando uma amostra de sangue seco em um cartão de coleta" loading="lazy">
        <figcaption class="img-cap">Cartões de coleta</figcaption>
      </figure>
      <div class="solution__txt">
        <h3 data-r="print">Cartões de coleta.</h3>
        <p>Cartões de coleta de sangue personalizados para laboratórios.</p>
        <a class="btn btn--line" href="../contato/?assunto=Assuntos%%20comerciais">Solicitar cartões%s</a>
      </div>
    </div>
  </div>
</section>
%s
""" % (len(PRODUCTS), n_map, n_lisa, fmt_count("manual"), fmt_count("semiautomatizado"), fmt_count("automatizado"),
       icon("search"), kits_table(p, PRODUCTS, catalog=True), icon("arrow"), icon("arrow"), close_block(p))
    write("produtos/index.html", page("produtos/index.html", "Catálogo de kits NeoMAP® e NeoLISA®",
                                      "Kits NeoMAP® (multiplex, xMAP®) e NeoLISA® (enzimáticos e colorimétricos) para triagem neonatal e pré-natal, com referências, apresentações, automação e cartões de coleta.",
                                      body, section="produtos"))


def build_product(i):
    x = PRODUCTS[i]
    p = "../../"
    line = LINES[x["line"]]
    pres = "".join('<li><span>%s %s</span><span>%s %s determinações</span></li>' % (ref_sym(), esc(r), icon("sigma"), esc(d)) for d, r in x["pres"])
    feats = "".join("<li>%s</li>" % reg(f) for f in x["feat"])
    rel = related_posts(x["kw"])
    rel_html = "".join('<li><a href="%spublicacoes/%s/"><span>%s<small>%s</small></span>%s</a></li>' % (
        p, r["slug"], esc(r["title"]), "Artigo" + (" · " + esc(r["date"]) if r["date"] else "") if r["kind"] == "artigo" else "Notícia", icon("arrow")) for r in rel)
    if not rel_html:
        rel_html = '<li><p class="leaflet__note" style="padding:14px 0;margin:0">Ainda não há publicações associadas a este kit no site. <a href="%spublicacoes/">Ver todas as publicações</a>.</p></li>' % p
    siblings = [y for y in PRODUCTS if y["line"] == x["line"] and y is not x]
    prev_x = PRODUCTS[i - 1] if i > 0 else None
    next_x = PRODUCTS[i + 1] if i + 1 < len(PRODUCTS) else None
    pager = ""
    if prev_x:
        pager += '<a href="%sprodutos/%s/"><span>Kit anterior</span><strong>%s</strong></a>' % (p, prev_x["slug"], reg(prev_x["name"]))
    if next_x:
        pager += '<a href="%sprodutos/%s/"><span>Próximo kit</span><strong>%s</strong></a>' % (p, next_x["slug"], reg(next_x["name"]))
    q = "assunto=Informa%C3%A7%C3%B5es%20sobre%20um%20kit&kit=" + x["slug"]
    shared = '<figcaption class="img-cap">Embalagem da linha NeoMAP® 3Plex</figcaption>' if x.get("img_shared") else '<figcaption class="img-cap">%s</figcaption>' % reg(x["name"])
    body = """
<article>
  <header class="sheet-top">
    <div class="wrap spec">
      <figure class="spec__img">
        <img src="%sassets/img/produtos/%s-900.webp" srcset="%sassets/img/produtos/%s-480.webp 480w, %sassets/img/produtos/%s-900.webp 900w" sizes="(max-width: 960px) 100vw, 50vw" width="%d" height="%d" alt="Embalagem e frascos de reagentes do kit %s">
        %s
      </figure>
      <div class="spec__txt">
        <ol class="crumbs"><li><a href="%s">Início</a></li><li><a href="%sprodutos/">Produtos</a></li><li aria-current="page">%s</li></ol>
        <h1>%s</h1>
        <p class="spec__ind">%s</p>
        <div class="cells">
          <div class="field"><span class="field__k">Linha</span><span class="field__v">%s</span></div>
          <div class="field"><span class="field__k">Tipo de ensaio</span><span class="field__v">%s</span></div>
          <div class="field wide-cell"><span class="field__k">Analito ou marcador</span><span class="field__v">%s</span></div>
          <div class="field wide-cell"><span class="field__k">Apresentação e referência</span><ul class="pres">%s</ul></div>
          <div class="field wide-cell"><span class="field__k">Formato</span><span class="field__v">%s</span></div>
        </div>
        <div class="spec__actions">
          <a class="btn btn--red" href="%scontato/?%s">Solicitar informações técnicas%s</a>
          <a class="btn btn--line" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">%sWhatsApp</a>
        </div>
      </div>
    </div>
  </header>

  <section class="section--tight">
    <div class="wrap leaflet">
      <div class="leaflet__col">
        <h2>Características <span>Ficha do fabricante</span></h2>
        <ul class="feat">%s</ul>
        <p class="leaflet__note">Características conforme publicadas pela Intercientifica. Para instruções de uso, validação e condições comerciais, consulte a equipe científica.</p>
      </div>
      <div class="leaflet__col">
        <h2>Triagem relacionada <span>%d</span></h2>
        <ul class="line__dz" style="margin:16px 0 40px">%s</ul>
        <h2>Publicações relacionadas <span>%d</span></h2>
        <ul class="related">%s</ul>
        <h2 style="margin-top:40px">Outros kits %s <span>%d</span></h2>
        <ul class="related">%s</ul>
      </div>
    </div>
  </section>
  <nav class="wrap" aria-label="Navegar entre kits" style="padding-bottom:var(--section)"><div class="pager">%s</div></nav>
</article>
%s
""" % (p, x["img"], p, x["img"], p, x["img"], x["img_w"], x["img_h"], esc(x["name"]), shared,
       p, p, esc(x["short"]),
       reg(x["name"]), esc(x["ind"]),
       reg(line["name"] + "®"), esc(x["assay"]), esc(x["targets"]), pres, esc(", ".join(f.capitalize() for f in x["formats"])),
       p, q, icon("arrow"), WHATSAPP, ("Ol%C3%A1!%20Gostaria%20de%20informa%C3%A7%C3%B5es%20sobre%20o%20kit%20" + x["name"].replace("®", "%C2%AE").replace(" ", "%20") + "%20(REF.%20" + x["pres"][0][1] + ")."), icon("wa"),
       feats, len(x["diseases"]), "".join("<li>%s</li>" % esc(d) for d in x["diseases"]), len(rel), rel_html,
       esc(line["name"] + "®"), len(siblings),
       "".join('<li><a href="%sprodutos/%s/"><span>%s<small>REF. %s</small></span>%s</a></li>' % (p, y["slug"], reg(y["name"]), " · ".join(r for _, r in y["pres"]), icon("arrow")) for y in siblings),
       pager, close_block(p, "Dúvidas sobre o %s?" % reg(x["name"]), "Fale com a equipe científica para fichas técnicas, validação, cotação ou demonstração."))
    write("produtos/%s/index.html" % x["slug"], page("produtos/%s/index.html" % x["slug"], "%s · REF. %s" % (x["name"], " · ".join(r for _, r in x["pres"])),
                                                     excerpt("%s %s" % (x["name"] + ":", x["ind"]), 155), body, section="produtos", og_type="product"))


# ================================================================ EMPRESA
def build_company():
    p = "../"
    values = "".join('<li data-r="up" style="--i:%d"><h3>%s</h3><p>%s</p></li>' % (i % 3, esc(a), esc(b)) for i, (a, b) in enumerate(VALUES))
    tl = []
    for y, t, d, key in TIMELINE:
        link = ""
        if key:
            hit = next((n for n in news if key.lower() in n["title"].lower() and n["ok"]), None)
            if hit:
                link = ' <a href="%spublicacoes/%s/">Ler a notícia</a>' % (p, hit["slug"])
        tl.append('<li data-r="up"><span class="y">%s</span><h3>%s</h3><p>%s%s</p></li>' % (y, reg(t), esc(d), link))
    lab = ["095e8e35", "bb2b69d6", "f2e31294", "99eb321d", "b24ce512", "f7f4e7c5"]
    alts = ["Pesquisadora pipetando reagentes no laboratório da Intercientifica", "Pesquisadora preparando reagentes na bancada",
            "Pesquisadora trabalhando no laboratório", "Pipeta multicanal dispensando em microplaca", "Ponteiras de pipeta sobre microplaca", "Colaboradora carregando um kit no laboratório"]
    gallery = "".join('<figure class="g%d" data-r="plate"><img src="%sassets/img/lab/%s-1080.webp" srcset="%sassets/img/lab/%s-540.webp 540w, %sassets/img/lab/%s-1080.webp 1080w" sizes="(max-width: 760px) 100vw, %s" width="1080" height="882" alt="%s" loading="lazy"></figure>' % (
        i + 1, p, h, p, h, p, h, "58vw" if i == 0 else "34vw", alts[i]) for i, h in enumerate(lab))
    body = """
<section class="ptop">
  <div class="wrap">
    <ol class="crumbs"><li><a href="../">Início</a></li><li aria-current="page">Empresa</li></ol>
    <h1 data-r="print">Pioneira em triagem neonatal e pré-natal.</h1>
    <p class="ptop__lead">Fabricação 100%% nacional de kits, reagentes, softwares e cartões de coleta personalizados para laboratórios, em São José dos Campos, SP.</p>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="split__a"><h2 data-r="print">Quem somos.</h2></div>
    <div class="split__b" data-r="up">
      <p>A Intercientifica é uma empresa pioneira e inovadora, especializada em triagem neonatal e pré-natal, com fabricação 100%% nacional de kits, reagentes, softwares e cartões de coleta personalizados para laboratórios.</p>
      <p>Fundada em 1994, com objetivo social de pesquisar, desenvolver produtos e serviços que garantam eficiência e precisão em programas de triagem de doenças neonatais e pré-natais.</p>
      <p>Ao longo de sua trajetória, a Intercientifica já produziu mais de 48 milhões de análises, beneficiando a qualidade de vida de milhares de pacientes e de seus familiares, pois com o diagnóstico precoce foi possível obter acesso aos tratamentos específicos e desenvolver uma vida saudável.</p>
    </div>
  </div>
  <div class="wrap" style="margin-top:var(--s-9)">
    <div class="mv">
      <div data-r="up"><h3>Visão</h3><p>Apresentar novas tecnologias para a medicina diagnóstica, priorizando e melhorando a vida humana.</p></div>
      <div data-r="up" style="--i:1"><h3>Missão</h3><p>Fornecer produtos e serviços de qualidade, através de investimentos constantes na pesquisa, desenvolvimento e aprimoramento de seus produtos, de maneira independente, procurando sempre atender às necessidades do mercado.</p></div>
    </div>
    <p class="muted" style="margin-top:24px;max-width:70ch">A missão inclui ainda buscar continuamente soluções por meio de novas ferramentas, tecnologias e produtos, e disponibilizar suporte constante aos clientes.</p>
  </div>
</section>

<section class="section" style="background:var(--paper-2)" aria-labelledby="val-title">
  <div class="wrap">
    <div class="head"><h2 id="val-title" data-r="print">Nove valores.</h2><p data-r="up">Os princípios que orientam produtos, processos e relações da empresa.</p></div>
    <ul class="values">%s</ul>
  </div>
</section>

<section class="section close on-red" style="padding-bottom:var(--section)" aria-labelledby="tl-title">
  <div class="wrap">
    <div class="head" style="margin-bottom:48px"><h2 id="tl-title" data-r="print" style="color:var(--on-red)">Trajetória.</h2><p data-r="up" style="color:var(--on-red)">Marcos com fonte nas publicações da própria Intercientifica.</p></div>
    <ol class="timeline">%s</ol>
  </div>
</section>

<section class="section" aria-labelledby="eq-title">
  <div class="wrap">
    <div class="split" style="margin-bottom:var(--s-8)">
      <div class="split__a"><h2 id="eq-title" data-r="print">Nossa equipe.</h2></div>
      <div class="split__b" data-r="up">
        <p>A qualidade e a excelência dos nossos produtos se devem ao alto nível de qualificação do nosso time de colaboradores e pesquisadores, formado por doutores, mestres e especialistas em suas respectivas áreas, com experiências em órgãos internacionais de pesquisa e de ensino superior.</p>
        <p>A equipe é composta por biólogos, biomédicos, farmacêuticos, químicos, engenheiros e administradores que prezam pelo aperfeiçoamento continuado, com diversos trabalhos científicos publicados em revistas e jornais nacionais e internacionais.</p>
      </div>
    </div>
    <div class="gallery">%s</div>
  </div>
</section>

<section class="section" style="background:var(--paper-2)" aria-labelledby="comp-title">
  <div class="wrap split">
    <div class="split__a"><h2 id="comp-title" data-r="print">Servir o presente sem comprometer o futuro.</h2></div>
    <div class="split__b" data-r="up">
      <p>O nosso compromisso está sustentado em três pilares: inovação, atendimento de excelência e sustentabilidade.</p>
      <p>Investimos fortemente em pesquisas científicas e no aprimoramento dos nossos produtos e serviços para atender de forma personalizada principalmente o mercado nacional. Estamos comprometidos em desenvolver soluções inovadoras para avançar ainda mais na qualidade da triagem neonatal e pré-natal, com foco na redução de insumos e custos. Para isso, os nossos laboratórios, no Brasil e nos Estados Unidos, estão equipados com instrumentos de última geração.</p>
      <p>Nós entendemos que a nossa saúde e a saúde do nosso planeta estão intrinsecamente ligadas. Por isso, o nosso compromisso é servir o presente, sem comprometer o futuro.</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="sede-title">
  <div class="wrap">
    <div class="head"><h2 id="sede-title" data-r="print">Parque Tecnológico UNIVAP.</h2><p data-r="up">%s</p></div>
    <div class="solution" style="align-items:stretch">
      <figure class="solution__img" data-r="plate"><img src="../assets/img/sede-parque-tecnologico-1600.webp" srcset="../assets/img/sede-parque-tecnologico-800.webp 800w, ../assets/img/sede-parque-tecnologico-1600.webp 1600w" sizes="(max-width: 900px) 100vw, 66vw" width="1600" height="1055" alt="Edifícios do Parque Tecnológico UNIVAP, em São José dos Campos" loading="lazy"><figcaption class="img-cap">São José dos Campos, SP</figcaption></figure>
      <div class="solution__txt" style="display:flex;flex-direction:column;justify-content:flex-end">
        <div class="map" data-map style="aspect-ratio:auto;min-height:280px">
          <div class="map__load"><p>O mapa é carregado do Google Maps apenas quando você pedir.</p><button class="btn btn--line" type="button" data-map-load>Mostrar mapa%s</button><a class="link" href="%s" target="_blank" rel="noopener">Abrir no Google Maps%s</a></div>
        </div>
      </div>
    </div>
  </div>
</section>
%s
""" % (values, "".join(tl), gallery, "<br>".join(esc(a) for a in ADDRESS_LINES[:3]), icon("pin"), MAPS_LINK, icon("ext"), close_block(p))
    write("empresa/index.html", page("empresa/index.html", "Empresa: história, missão e equipe",
                                     "Fundada em 1994 em São José dos Campos, a Intercientifica é pioneira em triagem neonatal e pré-natal, com fabricação 100% nacional, certificação ANVISA e programas de controle de qualidade.",
                                     body, section="empresa", extra_head='<script>window.MAP_SRC=%s</script>\n' % json.dumps(MAPS_EMBED)))


# ================================================================ PUBLICAÇÕES
def build_publications():
    p = "../"
    ordered = [x for x in articles] + [x for x in news]
    body = """
<section class="ptop">
  <div class="wrap">
    <ol class="crumbs"><li><a href="../">Início</a></li><li aria-current="page">Publicações</li></ol>
    <h1 data-r="print">Publicações.</h1>
    <p class="ptop__lead">Estudos, validações e trabalhos científicos com as tecnologias da Intercientifica, e o arquivo de notícias da empresa. Os PDFs originais estão disponíveis quando a publicação os inclui.</p>
  </div>
</section>
<div class="wrap">
  <form class="filters" id="pubfilters" role="search" aria-label="Filtrar publicações">
    <div class="filters__groups">
      <fieldset class="fgroup">
        <legend>Tipo</legend>
        <div class="chips">
          <label class="chip"><input type="radio" name="kind" value="" checked><span>Tudo <small>%d</small></span></label>
          <label class="chip"><input type="radio" name="kind" value="artigo"><span>Artigos <small>%d</small></span></label>
          <label class="chip"><input type="radio" name="kind" value="noticia"><span>Notícias <small>%d</small></span></label>
        </div>
      </fieldset>
    </div>
    <div class="search">
      <label for="pq">Buscar</label>
      <input id="pq" name="q" type="search" placeholder="Título, doença ou kit" autocomplete="off" enterkeyhint="search">
      %s
    </div>
  </form>
  <div class="results-bar"><p id="pcount" aria-live="polite" style="margin:0"></p></div>
  %s
  <div class="empty" id="pempty" hidden><p>Nenhuma publicação encontrada. Tente outra palavra.</p></div>
  <p class="muted" style="font-size:var(--t-small);padding-block:24px var(--section);max-width:72ch">As datas indicam quando cada artigo foi publicado no site da Intercientifica; o ano original do estudo aparece no título quando informado. As notícias são do arquivo do site oficial e não têm data publicada. Itens sem link estão fora do ar no site original.</p>
</div>
""" % (len(ordered), len(articles), len(news), icon("search"), index_rows(p, ordered, show_kind=True))
    write("publicacoes/index.html", page("publicacoes/index.html", "Publicações: artigos e notícias",
                                         "%d artigos científicos e %d notícias da Intercientifica sobre triagem neonatal e pré-natal, NeoMAP® e NeoLISA®." % (len(articles), len(news)),
                                         body, section="publicacoes"))
    for it in posts:
        if not it["ok"]:
            continue
        cover, content = rendered[it["slug"]]
        kind = "Artigo" if it["kind"] == "artigo" else "Notícia"
        coll = articles if it["kind"] == "artigo" else news
        ok_coll = [x for x in coll if x["ok"]]
        idx = ok_coll.index(it)
        pager = ""
        if idx > 0:
            pager += '<a href="../%s/"><span>Anterior</span><strong style="font-size:1.2rem">%s</strong></a>' % (ok_coll[idx - 1]["slug"], esc(excerpt(ok_coll[idx - 1]["title"], 80)))
        if idx + 1 < len(ok_coll):
            pager += '<a href="../%s/"><span>Próxima</span><strong style="font-size:1.2rem">%s</strong></a>' % (ok_coll[idx + 1]["slug"], esc(excerpt(ok_coll[idx + 1]["title"], 80)))
        meta = '<div class="field"><span class="field__k">Tipo</span><span class="field__v">%s</span></div>' % kind
        if it["date"]:
            meta += '<div class="field"><span class="field__k">Publicado no site em</span><span class="field__v"><time datetime="%s">%s</time></span></div>' % (it["iso"], esc(it["date"]))
        meta += '<div class="field"><span class="field__k">Fonte</span><span class="field__v">Site oficial da Intercientifica</span></div>'
        body = """
<section class="ptop">
  <div class="wrap">
    <ol class="crumbs"><li><a href="../../">Início</a></li><li><a href="../">Publicações</a></li><li aria-current="page">%s</li></ol>
    <h1 style="max-width:26ch;font-size:clamp(2rem,1.3rem + 2.6vw,3.6rem)">%s</h1>
  </div>
</section>
<article class="post">
  <div class="wrap post__grid">
    <aside class="post__meta">%s<a class="link" href="../">%sTodas as publicações</a></aside>
    <div class="post__body">
        %s
        %s
    </div>
  </div>
</article>
<nav class="wrap" aria-label="Navegar entre publicações" style="padding-bottom:var(--section)"><div class="pager">%s</div></nav>
%s
""" % (kind, esc(it["title"]), meta, icon("back"), cover or "", content, pager, close_block("../../", "Quer saber mais?", "Fale com a equipe científica sobre os produtos e estudos da Intercientifica."))
        write("publicacoes/%s/index.html" % it["slug"], page("publicacoes/%s/index.html" % it["slug"], it["title"], it["excerpt"], body, section="publicacoes", og_type="article"))


# ================================================================ CONTATO
def build_contact():
    p = "../"
    subjects = "".join('<option value="%s">%s</option>' % (esc(s), esc(s)) for s in SUBJECTS)
    kits = "".join('<option value="%s" data-ref="%s">%s</option>' % (x["slug"], " · ".join(r for _, r in x["pres"]), esc(x["name"])) for x in PRODUCTS)
    ccs = "".join('<option value="%s"%s>%s %s</option>' % (c, " selected" if k == "BR" else "", k, c) for k, c in COUNTRY_CODES)
    mails = "".join('<li><a href="mailto:%s"><span class="field__k">%s</span><span class="field__v">%s</span></a></li>' % (m, l, m) for l, m in EMAILS)
    body = """
<section class="ptop ptop--red on-red">
  <div class="wrap">
    <ol class="crumbs"><li><a href="../">Início</a></li><li aria-current="page">Contato</li></ol>
    <h1 data-r="print">Fale com a equipe científica.</h1>
    <p class="ptop__lead">Para saber mais sobre nossos produtos, solicitar informações técnicas, cotações ou demonstrações, escreva para a equipe. Respondemos de segunda a sexta, das 8:00 às 17:00.</p>
  </div>
</section>

<section class="section">
  <div class="wrap contact">
    <div class="contact__form">
      <h2 style="font-size:var(--t-h3);margin-bottom:8px">Envie sua mensagem</h2>
      <p class="muted" style="font-size:var(--t-small)">Campos marcados com <b style="color:var(--red-deep)">*</b> são obrigatórios. A mensagem segue pelo WhatsApp oficial da Intercientifica.</p>
      <form class="form" id="contact-form" data-whatsapp="%s" novalidate>
        <div class="form__row">
          <div class="f"><label for="nome">Nome <b>*</b></label><input id="nome" name="nome" autocomplete="given-name" required aria-describedby="nome-err"><span class="f__err" id="nome-err"></span></div>
          <div class="f"><label for="sobrenome">Sobrenome</label><input id="sobrenome" name="sobrenome" autocomplete="family-name"></div>
        </div>
        <div class="form__row">
          <div class="f"><label for="org">Laboratório ou instituição</label><input id="org" name="org" autocomplete="organization"></div>
          <div class="f"><label for="email">E-mail <b>*</b></label><input id="email" name="email" type="email" autocomplete="email" required aria-describedby="email-err" inputmode="email"><span class="f__err" id="email-err"></span></div>
        </div>
        <div class="form__row">
          <div class="f"><label for="tel">Telefone</label><div class="f__phone"><select id="ddi" name="ddi" aria-label="Código do país">%s</select><input id="tel" name="tel" type="tel" autocomplete="tel-national" inputmode="tel" aria-describedby="tel-err"></div><span class="f__err" id="tel-err"></span></div>
          <div class="f"><label for="assunto">Assunto <b>*</b></label><select id="assunto" name="assunto" required aria-describedby="assunto-err"><option value="">Escolha uma opção</option>%s</select><span class="f__err" id="assunto-err"></span></div>
        </div>
        <div class="f" id="kit-field"><label for="kit">Kit de interesse</label><select id="kit" name="kit"><option value="">Nenhum kit específico</option>%s</select></div>
        <div class="f"><label for="msg">Mensagem <b>*</b></label><textarea id="msg" name="msg" required aria-describedby="msg-err" rows="6"></textarea><span class="f__err" id="msg-err"></span></div>
        <div class="form__foot">
          <button class="btn btn--red" type="submit">%sEnviar pelo WhatsApp</button>
          <p class="form__note">Ao enviar, abrimos o WhatsApp da Intercientifica em uma nova aba com a sua mensagem já escrita. Ela só é entregue quando você tocar em enviar lá.</p>
          <div class="form__status" id="form-status" role="status" aria-live="polite"></div>
        </div>
      </form>
    </div>
    <aside class="contact__aside">
      <div class="aside-block">
        <h2>Canais diretos</h2>
        <ul class="ch-list">
          <li><a href="tel:%s"><span class="field__k">Telefone · %s</span><span class="field__v">%s</span></a></li>
          <li><a href="https://wa.me/%s" target="_blank" rel="noopener"><span class="field__k">WhatsApp</span><span class="field__v">%s</span></a></li>
          %s
        </ul>
      </div>
      <div class="aside-block">
        <h2>Endereço</h2>
        <ul class="ch-list">
          <li><a href="%s" target="_blank" rel="noopener"><span class="field__k">Abrir no Google Maps</span><span class="field__v" style="font-family:var(--f-sans);font-stretch:100%%;font-size:1rem;line-height:1.45">%s</span></a></li>
        </ul>
        <div class="social" style="margin-top:20px"><a href="%s" target="_blank" rel="noopener" aria-label="Instagram da Intercientifica" style="border-color:var(--rule)">%s</a><a href="%s" target="_blank" rel="noopener" aria-label="Facebook da Intercientifica" style="border-color:var(--rule)">%s</a></div>
      </div>
    </aside>
  </div>
</section>
""" % (WHATSAPP, ccs, subjects, kits, icon("wa"), PHONE, HOURS, PHONE_LABEL, WHATSAPP, WHATSAPP_LABEL, mails, MAPS_LINK,
       "<br>".join(esc(a) for a in ADDRESS_LINES), INSTAGRAM, icon("ig"), FACEBOOK, icon("fb"))
    write("contato/index.html", page("contato/index.html", "Contato: equipe científica e comercial",
                                     "Fale com a Intercientifica: telefone +55 (12) 3949-9700, WhatsApp, e-mails das equipes científica e comercial e endereço no Parque Tecnológico UNIVAP, São José dos Campos, SP.",
                                     body, section="contato"))


def build_404():
    body = """
<section class="nf on-red">
  <div class="wrap">
    <h1>Esta página não está no catálogo.</h1>
    <p>Erro 404: o endereço pode ter mudado. Volte ao início ou procure o kit pelo catálogo.</p>
    <div class="close__actions"><a class="btn btn--white" href="./">Ir para o início%s</a><a class="btn btn--line-light" href="produtos/">Ver catálogo de kits</a></div>
  </div>
</section>""" % icon("arrow")
    write("404.html", page("404.html", "Página não encontrada", "Página não encontrada.", body, base=""))


if __name__ == "__main__":
    build_home()
    build_catalog()
    for i in range(len(PRODUCTS)):
        build_product(i)
    build_company()
    build_publications()
    build_contact()
    build_404()
    n_ok = sum(1 for x in posts if x["ok"])
    print("ok: home, catálogo, %d kits, empresa, contato, 404, %d publicações (de %d)" % (len(PRODUCTS), n_ok, len(posts)))
    for x in PRODUCTS:
        print("  %-28s relacionadas: %d" % (x["name"], len(related_posts(x["kw"]))))
