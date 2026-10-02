---
name: Intercientifica · Proposta 2
description: O rótulo do kit como sistema visual; caixa vermelha, células de rótulo, REF e Σ como tipografia de primeira linha.
colors:
  box-red: "#DE1E18"
  red-deep: "#B3130E"
  ink: "#101215"
  ink-2: "#353A41"
  ink-3: "#5B626B"
  paper: "#FFFFFF"
  paper-2: "#F0F2F3"
  paper-3: "#E3E7EA"
  rule-soft: "#CDD3D8"
  chamber: "#0A0C0F"
  chamber-rule: "rgba(236, 239, 242, 0.14)"
  on-dark: "#ECEFF2"
  on-dark-2: "#A3ACB6"
  on-dark-3: "#808994"
  on-red-rule: "rgba(255, 255, 255, 0.42)"
  bead-1: "#FF5A47"
  bead-2: "#FFB547"
  bead-3: "#5FD3C2"
  bead-4: "#9DAAFF"
  ok: "#0F7A3D"
typography:
  display:
    fontFamily: "Archivo, 'Arial Narrow', system-ui, sans-serif"
    fontSize: "clamp(2.6rem, 1.2rem + 5.2vw, 5.75rem)"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "-0.04em"
    fontVariation: "'wdth' 116"
  hero:
    fontFamily: "Archivo, 'Arial Narrow', system-ui, sans-serif"
    fontSize: "clamp(2.4rem, 0.7rem + 3.5vw, 4.4rem)"
    fontWeight: 800
    lineHeight: 0.96
    letterSpacing: "-0.035em"
    fontVariation: "'wdth' 106"
  headline:
    fontFamily: "Archivo, 'Arial Narrow', system-ui, sans-serif"
    fontSize: "clamp(2.3rem, 1.3rem + 3.6vw, 4.5rem)"
    fontWeight: 800
    lineHeight: 0.98
    letterSpacing: "-0.035em"
    fontVariation: "'wdth' 116"
  title:
    fontFamily: "Archivo, 'Arial Narrow', system-ui, sans-serif"
    fontSize: "clamp(1.9rem, 1.2rem + 2.6vw, 3.4rem)"
    fontWeight: 750
    lineHeight: 1.04
    letterSpacing: "-0.03em"
    fontVariation: "'wdth' 116"
  subtitle:
    fontFamily: "Archivo, 'Arial Narrow', system-ui, sans-serif"
    fontSize: "clamp(1.25rem, 1.1rem + 0.5vw, 1.55rem)"
    fontWeight: 700
    lineHeight: 1.04
    letterSpacing: "-0.018em"
    fontVariation: "'wdth' 108"
  lead:
    fontFamily: "Archivo, 'Arial Narrow', system-ui, sans-serif"
    fontSize: "clamp(1.1rem, 1.02rem + 0.35vw, 1.3rem)"
    fontWeight: 400
    lineHeight: 1.5
  body:
    fontFamily: "Archivo, 'Arial Narrow', system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
  small:
    fontFamily: "Archivo, 'Arial Narrow', system-ui, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "'Martian Mono', ui-monospace, 'Cascadia Mono', monospace"
    fontSize: "0.72rem"
    fontWeight: 500
    letterSpacing: "0.06em"
    fontVariation: "'wdth' 87.5"
  code:
    fontFamily: "'Martian Mono', ui-monospace, 'Cascadia Mono', monospace"
    fontSize: "0.78rem"
    fontWeight: 500
    letterSpacing: "0"
    fontFeature: "'tnum' 1"
    fontVariation: "'wdth' 87.5"
  figure:
    fontFamily: "'Martian Mono', ui-monospace, 'Cascadia Mono', monospace"
    fontSize: "clamp(2rem, 1.2rem + 2.6vw, 3.6rem)"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "-0.04em"
    fontFeature: "'tnum' 1"
    fontVariation: "'wdth' 87.5"
rounded:
  none: "0px"
spacing:
  s-4: "16px"
  s-5: "24px"
  s-6: "32px"
  s-7: "48px"
  s-8: "64px"
  s-9: "96px"
  gutter: "clamp(16px, 4vw, 48px)"
  section: "clamp(88px, 11vw, 168px)"
  mast-h: "68px"
  max: "1440px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0 20px 0 22px"
    height: "54px"
  button-primary-hover:
    backgroundColor: "{colors.box-red}"
    textColor: "{colors.paper}"
  button-red:
    backgroundColor: "{colors.box-red}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0 20px 0 22px"
    height: "54px"
  button-red-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  button-white:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 20px 0 22px"
    height: "54px"
  button-white-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  button-line:
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 20px 0 22px"
    height: "54px"
  button-line-hover:
    backgroundColor: "{colors.box-red}"
    textColor: "{colors.paper}"
  field-key:
    textColor: "{colors.ink-3}"
    typography: "{typography.label}"
  sym-ref:
    textColor: "{colors.ink}"
    typography: "{typography.code}"
    rounded: "{rounded.none}"
    padding: "0 0.3em"
    height: "1.55em"
  chip:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 14px"
    height: "40px"
  chip-selected:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  input-search:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 40px 0 14px"
    height: "44px"
  mast:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    height: "{spacing.mast-h}"
  mast-on-red:
    backgroundColor: "{colors.box-red}"
    textColor: "{colors.paper}"
    height: "{spacing.mast-h}"
  close-band:
    backgroundColor: "{colors.box-red}"
    textColor: "{colors.paper}"
    padding: "{spacing.section} 0 0"
  colophon:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-dark}"
---

# Design System: Intercientifica · Proposta 2

## Overview

**Creative North Star: "A Caixa e a Bula"**

O site é a própria documentação do kit Intercientifica ampliada a escala de monumento: a caixa vermelha vira campo inteiro, o rótulo branco vira painel registrado sobre linhas-guia, e a bula (instruções de uso) vira o idioma de tabelas regradas, células com nome de campo e valor, e símbolos no estilo ISO 15223. REF e Σ (determinações) são tipografia de primeira linha, não ornamento. O sistema é impresso, plano e preciso: tinta preta, papel revestido frio, quinas retas e fios de 1px.

A densidade é a de um rótulo técnico: muita informação em células pequenas, mas com hierarquia brutal entre o display expandido em Archivo e o mono condensado de códigos. Há exatamente um capítulo escuro, a câmara de leitura (`--chamber`), onde vive a única cor espectral do site, a das microesferas. Fora dela, todo campo de texto é acromático, e o vermelho da caixa é a única cor de marca.

O movimento segue a gramática do registro gráfico: primeiro as linhas-guia se desenham, depois a chapa (vermelha ou de imagem) entra por recorte, depois o texto é impresso linha a linha, tudo num único relógio expo-out. O sistema recusa a página clínica branca de cartões arredondados com bebê de banco de imagens, e a página navy/neon de DNA de ficção científica.

**Key Characteristics:**
- Vermelho da caixa ocupando campos inteiros (topo da home, fechamentos, menu móvel, topos de página vermelhos, 404), nunca salpicado.
- Células de rótulo: nome do campo em mono maiúsculo e valor logo abaixo, separados por fios de 1px.
- Archivo variável com eixo de largura: expandido para display, normal para texto; Martian Mono condensado só para códigos, referências e medidas.
- Quinas retas em tudo; os únicos círculos são as microesferas e os pontos de analito.
- Uma câmara escura por página no máximo, e é lá que a cor espectral fica confinada.
- Registro como movimento: fio, chapa, tipo, com o mesmo `--ease`.

## Colors

Paleta de impressão: um vermelho de caixa comprometido, tinta preta, papel frio e uma câmara escura; o espectro existe só dentro das microesferas.

### Primary
- **Vermelho da Caixa** (`box-red`): a cor do logotipo e da caixa do kit. Ocupa campos inteiros com texto branco por cima: `.box` (topo da home), `.close` (fechamento de cada página), `.sheet` (menu móvel), `.ptop--red`, `.nf` (404), `.mast.is-on-red`. Também é a chapa que entra no hover dos botões, o sublinhado da navegação ativa, a seleção de texto, o cursor dos campos e o fundo do selo ANVISA em `.registry__badge`.
- **Vermelho Profundo** (`red-deep`): vermelho para texto sobre branco em tamanho de corpo ou menor (6.6:1). Usado em `.line__method`, hover de títulos de `.index-list`, `.related` e `.pager`, links do corpo de posts, rótulo de corte em `.bar__cut` e o asterisco de obrigatório nos formulários. Também é o token `--error`.

### Tertiary
- **Espectro das Microesferas** (`bead-1` coral, `bead-2` âmbar, `bead-3` verde-água, `bead-4` lavanda): as quatro cores dos conjuntos de analitos. Vivem só no canvas Three.js, nas figuras SVG de fallback e nos pontos `.analytes i` da câmara.

### Neutral
- **Tinta** (`ink`): texto principal, fios fortes (`--rule` tem o mesmo valor), fundo do botão primário, chip selecionado e fundo do rodapé `.colophon`.
- **Tinta Secundária** (`ink-2`): leads, parágrafos de apoio, descrições (11:1 sobre branco).
- **Tinta de Metadado** (`ink-3`): nomes de campo, cabeçalhos de tabela, fontes de dados, datas (6.1:1 sobre branco).
- **Papel do Rótulo** (`paper`): fundo padrão, painel do rótulo, células e miniaturas.
- **Papel Revestido Frio** (`paper-2`): o único fundo de seção alternativo (`.lines`, contendo o índice de kits), hover de chips e fundo do mapa.
- **Papel de Espera** (`paper-3`): fundo de imagens enquanto carregam (`.solution__img`, `.gallery figure`).
- **Fio Suave** (`rule-soft`): divisórias entre linhas de tabelas e listas, abaixo de um fio forte de cabeçalho.
- **Câmara** (`chamber`): fundo da câmara de leitura (`.chamber`, `.window`), com `chamber-rule` para fios, `on-dark` para texto, `on-dark-2` para texto secundário (8.4:1) e `on-dark-3` para etapas inativas (5.4:1).
- **Fio sobre Vermelho** (`on-red-rule`): linhas-guia e divisórias sobre o campo vermelho.
- **Confirmação** (`ok`): só a borda de `.form__status.is-ok`.

### Named Rules
**The Box Face Rule.** O vermelho entra como campo inteiro, de borda a borda, com texto branco por cima; ou como chapa de estado (hover, ativo, seleção). Nunca como fundo de cartão, ícone colorido ou destaque espalhado.

**The Spectral Confinement Rule.** As quatro cores `bead-*` só existem dentro da câmara escura e das microesferas. Texto, fios, botões e fundos permanecem acromáticos ou vermelhos.

**The Red-Deep Text Rule.** Texto vermelho em tamanho de corpo ou menor sobre branco usa `red-deep`. O `box-red` sobre branco só aparece em tamanho de display (a palavra destacada no H1 do rótulo).

## Typography

**Display Font:** Archivo variável (eixos `wdth` 62 a 125 e `wght` 300 a 900), com fallback 'Arial Narrow', system-ui
**Body Font:** Archivo, mesma família, largura normal
**Label/Mono Font:** Martian Mono variável (`wdth` 75 a 112.5), com fallback ui-monospace, 'Cascadia Mono'

**Character:** Uma sans grotesca que se alarga para gritar como a face da caixa, e um mono condensado que fala como o texto impresso do rótulo: código, lote, referência. A largura é a hierarquia, mais do que o tamanho.

### Hierarchy
- **Display** (800, `--t-display`, 0.95, largura 116%, -0.04em): títulos dos fechamentos vermelhos e da 404, limitados a 14ch.
- **Hero** (800, até 4.4rem, 0.96, largura 106%, -0.035em): o H1 dentro do painel do rótulo na home, quebrado em linhas `.ln`.
- **Headline** (800, `--t-h1`, 0.98, largura 116%): H1 das páginas internas (`.ptop h1`, até 18ch) e, num degrau próprio de até 5rem, o nome do kit em `.spec h1`.
- **Title** (750, `--t-h2`, 1.04, largura 116%, -0.03em): títulos de seção em `.head h2`, `.split h2` e títulos das etapas da câmara.
- **Subtitle** (700, `--t-h3`, largura 108%): títulos de bloco da bula (`.leaflet h2`), missão e visão, nomes de kit na tabela (até 1.4rem).
- **Line Name** (800, até 6rem, 0.9, largura 125%, -0.05em): só os nomes das duas linhas, NeoMAP e NeoLISA, em `.line__name`.
- **Lead** (400, `--t-lead`, 1.5): parágrafos de abertura, até 46 a 58ch.
- **Body** (400, 1.0625rem, 1.6): texto corrido; posts sobem para 1.1rem e 1.75.
- **Label** (mono 500, 0.72rem, 0.06em, maiúsculas, largura 87.5%, `ink-3`): nomes de campo (`.field__k`), cabeçalhos de tabela, legendas de filtros e formulários, títulos do rodapé.
- **Code** (mono 500, 0.78 a 0.92rem, números tabulares, largura 87.5%): REF, determinações, telefones, e-mails, datas, legendas de imagem.
- **Figure** (mono 500, até 3.6rem, 1, -0.04em): números grandes com fonte em `.lrow__v`, `.prod-cells .big` e anos de `.timeline`.

### Named Rules
**The Two Voices Rule.** Archivo carrega palavras; Martian Mono carrega apenas códigos, referências, medidas, datas, contatos e nomes de campo. Prosa nunca vai em mono.

**The Width Is Hierarchy Rule.** Títulos sobem de largura (106%, 108%, 116%, 125%) com tracking negativo; texto fica em 100%; o mono fica sempre condensado em 87.5%. Não use o eixo de largura em corpo de texto.

**The Registered Mark Rule.** Todo ® de marca (NeoMAP, NeoLISA, xMAP, Luminex, Hamilton, Opentrons) vai em `.reg`: 0.55em, elevado, peso 500.

## Layout

Grade de 12 colunas (`.grid`, `repeat(12, minmax(0, 1fr))`) dentro de `.wrap` com máximo de 1440px e gutter fluido de 16 a 48px. A grade é visível no topo da home: `.box__keys` desenha as 12 linhas-guia verticais sobre o vermelho, e o rótulo (7 colunas) e a janela da câmara (5 colunas) se registram nelas. Seções usam `--section` (88 a 168px) de respiro vertical; `.section--tight` usa 64 a 112px. O cabeçalho `.mast` é fixo com 68px, e todo deslocamento sticky (filtros, palco da câmara, meta de posts) parte de `--mast-h`.

Os cabeçalhos de seção (`.head`) colocam o título em 7 colunas e o lead nas colunas 9 a 12, alinhados pela base. Dados com fonte usam linhas regradas de três colunas proporcionais (3/4/5 em `.lrow` e `.timeline`, 4/3/5 em `.facts__row`). A escala de espaço é base 8 (`s-4` a `s-9`: 16, 24, 32, 48, 64, 96px).

Pontos de quebra observados, todos `max-width`:
- **1100px:** rótulo e janela da home empilham em 12 colunas; o número de telefone do cabeçalho some, fica o ícone.
- **960px:** a navegação vira o botão Menu e a folha vermelha `.sheet`; ficha de produto, post e contato empilham.
- **900px:** cabeçalhos de seção, câmara (palco sticky em 46svh acima das etapas), ledger, linhas, soluções, registro, filtros (deixam de ser sticky) e rodapé empilham; canais caem para 2 colunas.
- **760px:** a tabela de kits vira grade de duas linhas por kit, com o nome de cada coluna repetido via `data-k`; índice de publicações, fatos, missão e visão, linha do tempo e galeria passam a uma coluna.
- **640px:** linhas do rótulo se reorganizam e os botões do rótulo ocupam a largura toda.
- **600px:** paginação e linhas de formulário passam a uma coluna; botão de envio em largura total.
- **520px:** canais e células da ficha passam a uma coluna.

### Named Rules
**The Fixed Columns Rule.** O índice de kits é uma tabela regrada cujas colunas (Kit, Linha, REF, Σ Determinações) nunca se movem nem reordenam; filtrar esconde linhas, não reorganiza colunas.

**The Registered Grid Rule.** Elementos de destaque se alinham às 12 colunas e aos fios; nada flutua fora da grade com deslocamento decorativo.

## Elevation & Depth

O sistema é plano como papel impresso. Profundidade vem de chapas sobrepostas (rótulo branco sobre a caixa vermelha, janela escura recortada na caixa) e de fios, não de sombras. Existem exatamente duas sombras, ambas suaves e com deslocamento só vertical, e ambas para objetos que de fato flutuam sobre outro plano.

### Shadow Vocabulary
- **Sombra do Rótulo** (`box-shadow: 0 30px 60px -30px rgba(60, 4, 2, 0.55)`): só o painel `.label` sobre o vermelho da home, tingida de vermelho escuro.
- **Sombra da Espiada** (`box-shadow: 0 24px 50px -24px rgba(16,18,21,0.45)`): a prévia `.peek` da imagem do kit que segue o cursor na tabela (só ponteiro fino).

### Named Rules
**The Printed Flat Rule.** Cartões, botões, chips, células e tabelas não têm sombra. Se algo precisa se destacar, ganha um fio de 1px de tinta ou muda de chapa (fundo), nunca uma sombra.

## Shapes

Quinas retas em tudo (raio 0, inclusive `border-radius: 0` explícito em inputs). A forma é feita de fios: 1px (`--line`) para divisórias de células, linhas de tabela e molduras; 1.5px para bordas de botões, do símbolo REF, do menu e para o fio de topo de tabelas e listas (`.kits table`, `.index-list`, `.form`, `.facts`, `.values`, `.mv`). Fios fortes usam `ink`; divisórias internas de listas usam `rule-soft`; na câmara, `chamber-rule`; sobre o vermelho, `on-red-rule`.

Os únicos círculos do sistema são as microesferas e os pontos `.analytes i` (9px). A janela da câmara tem cantoneiras de registro (`.window__corner`, 14px, fio de 1.5px) como marcas de corte. Legendas de imagem (`.img-cap`) são etiquetas brancas presas ao canto inferior esquerdo com fio no topo e à direita. Os ícones são SVG de traço 1.6, terminação quadrada e junção em quina.

### Named Rules
**The Square Corner Rule.** Raio zero em todo elemento de interface. Arredondar um botão, chip ou campo quebra o rótulo.

**The Keyline Rule.** Células se dividem por fios de 1px que tocam as bordas; o espaço entre células é feito de padding, não de gaps com fundo à mostra.

## Components

### Buttons
Retangulares como uma etiqueta; o preenchimento entra como uma chapa.
- **Shape:** quinas retas (0px), altura mínima de 54px, padding `0 20px 0 22px`, borda de 1.5px na cor do fundo, Archivo 600 a 1rem, rótulo à esquerda e ícone de seta à direita (`justify-content: space-between`, gap 18px).
- **Primary (`.btn`):** fundo `ink`, texto `paper`, chapa `box-red`.
- **Hover:** um pseudo-elemento com a cor da chapa cresce da esquerda (`scaleX` 0 a 1 em `--d-3`, 700ms, `--ease`); a borda assume a cor da chapa e a seta anda 4px. Só em `hover: hover`. **Active:** desce 1px. **Focus:** contorno de 3px em `ink` com offset de 3px (branco sobre vermelho ou câmara).
- **Red (`.btn--red`):** fundo `box-red`, chapa `ink`; usado no rótulo e em ações primárias sobre branco.
- **White (`.btn--white`):** fundo `paper`, chapa `ink`; ação primária sobre o vermelho.
- **Line (`.btn--line`, `.btn--line-light`):** transparente com borda de 1.5px em tinta ou branco; secundária. A versão clara usa chapa branca.
- **Compact:** no cabeçalho (`.mast__cta`) cai para 42px e 0.9rem.
- **Disabled / Loading:** opacidade 0.5 sem ponteiro; o ícone gira em 900ms enquanto carrega.
- **Link de texto (`.link`):** sublinhado de 1.5px que se desenha da esquerda no hover, com a seta andando 4px.

### Label Cells (`.field`)
A unidade básica do sistema. Nome do campo em mono maiúsculo `ink-3` (`.field__k`, com ícone ou símbolo opcional à esquerda) e valor logo abaixo em Archivo 600 (`.field__v`), ou em mono quando é código. Agrupadas em linhas com fios (`.label__row`, `.cells` em duas colunas na ficha do kit, `.channels` em quatro colunas no fechamento). Sobre o vermelho, o nome do campo fica branco; na câmara, `on-dark-2`.

### Símbolos ISO 15223 (`.sym`, `.sym-svg`)
- **REF:** caixa com borda de 1.5px em `currentColor`, quinas retas, altura 1.55em, Martian Mono 600 a 0.7rem; precede toda referência de kit e o cabeçalho de coluna de referências.
- **Σ (determinações):** ícone SVG `#i-sigma` de traço, precede toda contagem de determinações.
- **Fabricante:** ícone de fábrica preenchido (`.sym-svg.icon-fill`) ao lado do nome e cidade, no rótulo e no bloco `.maker` do rodapé.

### Kits Index (`.kits`)
Tabela regrada com fio de topo de 1.5px em tinta, cabeçalhos em mono maiúsculo `ink-3`, linhas divididas por `rule-soft` com 18px de padding vertical. Colunas: nome do kit (Archivo 700, largura 108%, com analitos em `small`), linha, REF e Σ em mono, e uma seta. A linha inteira é clicável (`.row-link::after` cobre a linha); no hover o fundo passa a `paper` e a seta anda 6px e fica vermelha. Em ponteiro fino, `.peek` mostra a foto da caixa seguindo o cursor. A versão de catálogo (`.kits--catalog`) acrescenta miniatura de 144×100px e formato. Os filtros (`.filters`) ficam sticky abaixo do cabeçalho.

### Chips (`.chip`)
- **Style:** fundo `paper`, fio de 1px em tinta, altura 40px, padding 0 14px, Archivo 500 a 0.92rem, contagem em mono `ink-3`. Chips adjacentes compartilham o fio (margem -1px), formando uma régua.
- **State:** selecionado inverte para fundo `ink` e texto `paper`; hover em `paper-2`; foco com contorno vermelho de 3px.

### Inputs / Fields
- **Busca (`.search`):** caixa de 44px com fio de 1px, quinas retas, rótulo mono acima, ícone de lupa à direita; foco com contorno de 3px em `box-red`.
- **Formulário (`.form`, `.f`):** campos sem caixa, empilhados como linhas de uma ficha. Rótulo mono maiúsculo, valor em Archivo 500 a 1.1rem, fio `rule-soft` abaixo. No foco, um fio de 2px em tinta se desenha da esquerda (`scaleX`, 700ms) e o rótulo escurece para `ink`. Inválido: o fio fica em `--error` (igual a `red-deep`) com mensagem abaixo. O status (`.form__status`) é uma caixa regrada; borda verde no sucesso, vermelha no erro.

### Navigation (`.mast`, `.sheet`)
- **Mast:** faixa fixa de 68px, fundo `paper` com fio inferior; logotipo de 104px, links em Archivo 500 a 0.95rem com sublinhado de 1.5px que se desenha no hover; a página atual fica sublinhada em vermelho. Telefone em mono e botão compacto à direita. Sobre a caixa vermelha (`.is-on-red`), o mast vira vermelho com logotipo branco e botão branco. Preservado entre páginas por view transition.
- **Mobile:** abaixo de 960px, botão Menu com borda de 1.5px; abre `.sheet`, uma chapa vermelha de tela inteira que desce por `clip-path` (700ms), com links em Archivo 700 expandido de até 2.6rem divididos por fios brancos e contatos em mono no pé.
- **Breadcrumbs (`.crumbs`):** mono `ink-3` com barras `/` em `rule-soft`.

### Ledger (`.lrow`, `.bar`)
Linhas de dados com fonte: número grande em mono (Figure) com unidade em `small` acima, rótulo e fonte ao lado, e uma barra de 40px. A barra mostra a parte que fica (`.bar__keep`, bloco `ink`) e a parte cortada (`.bar__cut`, contorno tracejado de 1.5px em `box-red` com hachura diagonal a 8% e a porcentagem em `red-deep`), com escala mono abaixo. As barras crescem da origem quando entram na tela, a parte cortada 350ms depois. A fonte de cada número fica em `.ledger__src` abaixo das linhas.

### Facts Rows (`.facts`)
Lista de definição regrada em três colunas (fato, valor em mono 1.15rem, fonte em `ink-3`), fio de topo de 1.5px e divisórias `rule-soft`. Mesmo idioma do ledger, sem barras. Variações do mesmo padrão: `.reg-row` (programas de qualidade, com código mono à esquerda e procedência à direita) e `.index-list` (publicações, com data mono, título e tipo).

### Story Stage (`.chamber`, `.story`, `.stage`)
O capítulo assinatura, em fundo `chamber`. Etapas (`.step`, cada uma com altura de viewport) à esquerda em 5 colunas; palco sticky à direita em 7 colunas, emoldurado por um fio `chamber-rule`. Um único campo de microesferas Three.js se reorganiza por etapa (`data-step`: nuvem, disco, quatro conjuntos de analitos, leitura); na etapa de leitura aparecem eixos de fio e etiquetas mono. Etapas inativas esmaecem para `on-dark-2` e `on-dark-3`. Contador mono no canto superior e legenda mono na base, sempre com "Representação ilustrativa". Sem WebGL, com economia de dados ou com movimento reduzido, figuras SVG estáticas (`.plate-svg`) assumem cada etapa. Abaixo de 900px o palco fica sticky acima das etapas com 46svh. A janela `.window` do topo da home é a versão compacta da mesma câmara, com cantoneiras, legenda e botão de pausa (`.pause`).

### Close and Channels (`.close`, `.channels`)
Todo percurso termina num campo vermelho: título Display de até 14ch, lead branco, ações (`.btn--white` e `.btn--line-light`) e uma régua de quatro canais (telefone, equipe científica, equipe comercial, endereço) em células `.field` divididas por fios `on-red-rule`, com valores em mono. Canais caem para 2 colunas em 900px e 1 em 520px.

### Colophon (`.colophon`)
O rodapé é o bloco do fabricante, em fundo `ink`. O `.maker` é uma caixa de fio `chamber-rule` com o símbolo de fabricante e o endereço completo, como no verso do rótulo. Títulos de coluna em mono maiúsculo `on-dark-2`; ícones sociais em quadrados de 40px com fio.

### Product Sheet (`.spec`, `.leaflet`)
A página de kit é a ficha: foto da caixa em 6 colunas sobre `paper` com legenda presa ao canto e fio à direita; nome do kit em Headline e grade `.cells` de duas colunas com linha, tipo de ensaio, analitos, apresentação (REF + Σ) e formato. Abaixo, a bula (`.leaflet`) em duas colunas com títulos Subtitle sobre fio de 1.5px e listas regradas; paginação `.pager` entre kits.

### Motion
Um relógio só: `--ease` (`cubic-bezier(0.16, 1, 0.3, 1)`, expo-out) em quase tudo, com durações `--d-1` 160ms (chips), `--d-2` 320ms (cor, setas), `--d-3` 700ms (chapas, fios) e `--d-4` 1100ms (linhas-guia). A entrada da home é um registro: as 12 linhas-guia crescem de cima (1100ms), a chapa do rótulo se revela da esquerda (1000ms, atraso 260ms), a janela sobe de baixo (1100ms, atraso 480ms), as linhas do H1 sobem uma a uma a cada 80ms a partir de 560ms. No resto do site, quatro revelações por `data-r`: `print` (título impresso de cima por `clip-path`), `plate` (imagem entra como chapa da esquerda com `--ease-in-out` enquanto desescala de 1.12), `rule` (fio que se desenha) e `up` (texto sobe 18px em cascata de 70ms). Navegação entre páginas usa view transitions de 420ms com o mast fixo.

**Movimento reduzido:** os estados iniciais ocultos só existem sob `html.js` e `prefers-reduced-motion: no-preference`; sem JS ou com movimento reduzido, todo conteúdo aparece pronto. Com `reduce`, transições e animações caem para 0.01ms, o scroll suave é desligado, a folha do menu fecha sem espera, a espiada segue o cursor sem inércia e o Three.js não inicia (ficam as figuras SVG).

### Named Rules
**The Registration Order Rule.** Em toda entrada, o fio vem primeiro, depois a chapa, depois o tipo. O fio, uma vez desenhado, nunca se move.

**The Content-First Motion Rule.** Nenhum conteúdo depende de animação para existir; o estado oculto é uma camada opcional acima do estado final.

## Do's and Don'ts

### Do:
- **Do** dar ao vermelho da caixa campos inteiros com texto branco: topo, fechamento, menu móvel, topos de página de destaque.
- **Do** escrever códigos, REF, determinações, telefones, datas e nomes de campo em Martian Mono condensado (largura 87.5%) com números tabulares.
- **Do** preceder toda referência de kit com o símbolo REF em caixa e toda contagem de determinações com Σ.
- **Do** dividir informação em células e linhas regradas por fios de 1px, com fio de topo de 1.5px em tinta nas tabelas e listas.
- **Do** dar a todo número uma linha de fonte em `ink-3` logo abaixo ou ao lado.
- **Do** usar `red-deep` para qualquer texto vermelho em tamanho de corpo sobre branco.
- **Do** rotular toda imagem científica abstrata como "Representação ilustrativa" e oferecer fallback estático para o WebGL.
- **Do** usar `--ease` e as durações `--d-1` a `--d-4` em qualquer transição nova, e esconder estados iniciais só sob `html.js` com `prefers-reduced-motion: no-preference`.

### Don't:
- **Don't** arredondar quinas de botões, chips, campos, imagens ou painéis; o raio do sistema é 0.
- **Don't** levar as cores `bead-*` para fora da câmara escura e das microesferas.
- **Don't** colocar sombra em cartões, botões, chips ou tabelas; as únicas sombras são a do rótulo sobre o vermelho e a da espiada.
- **Don't** usar mono para prosa nem o eixo de largura expandido em texto corrido.
- **Don't** pôr uma linha mono maiúscula solta acima de um título de seção; nomes de campo vivem dentro de células, junto do valor que nomeiam.
- **Don't** adicionar gradientes decorativos ou brilhos; os únicos gradientes são funcionais (o véu escuro sob as legendas do canvas e a hachura da parte cortada da barra).
- **Don't** reordenar, ocultar ou animar as colunas do índice de kits.
- **Don't** usar fotografia de banco de imagens de bebês ou laboratórios genéricos, nem a estética navy/neon de DNA.
