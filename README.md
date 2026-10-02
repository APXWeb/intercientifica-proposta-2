# Intercientifica · Proposta 2 (APX Web)

Segunda proposta de site para a Intercientifica, independente da primeira.

## As duas propostas

| | Proposta 1 | Proposta 2 |
|---|---|---|
| Pasta local | `portfolio-projects/intercientifica/` | `portfolio-projects/intercientifica-proposta-2/` |
| Repositório | github.com/APXWeb/intercientifica (branch `master`) | github.com/APXWeb/intercientifica-proposta-2 (branch `main`) |
| Endereço | https://apxweb.github.io/intercientifica/ | https://apxweb.github.io/intercientifica-proposta-2/ |
| Conceito | Base clara e clínica, cartões arredondados, página única | O rótulo do kit: caixa vermelha, células de rótulo, REF e Σ como tipografia; exploração 3D de uma estação Opentrons® Flex controlada pelo scroll |

São dois repositórios git separados. Nada desta pasta é publicado no repositório da Proposta 1, e vice-versa.

## Estrutura

```
index.html                  Home: caixa, automação 3D (scroll), leitura multiplex, dados, linhas, qualidade, publicações
produtos/                   Catálogo com filtros (linha, formato) e busca (doença, marcador, REF)
produtos/<kit>/             Ficha de cada um dos 9 kits
empresa/                    Quem somos, missão, valores, trajetória, equipe, compromisso, sede
publicacoes/                25 artigos e 14 notícias, com filtro e busca; uma página por publicação
contato/                    Formulário que abre o WhatsApp oficial com a mensagem pronta
404.html                    Página de erro do GitHub Pages
assets/css/site.css         Design system completo (tokens no topo do arquivo)
assets/js/site.js           Navegação, revelações, filtros, formulário, narrativa por scroll
assets/js/flex.js           Opentrons Flex em Three.js, controlado pelo scroll (só na home, sob demanda)
assets/js/multiplex.js      Mapa de classificação das microesferas (a antiga etapa 4)
assets/img/flex/            Quadros estáticos da cena: herói e fallback sem WebGL ou com movimento reduzido
_tools/                     Gerador das páginas e dados transcritos do site oficial
```

## Como ver localmente

Sirva a pasta-mãe para que o caminho seja igual ao do GitHub Pages:

```bash
cd portfolio-projects
python -m http.server 8722
# abra http://127.0.0.1:8722/intercientifica-proposta-2/
```

A Proposta 1 fica no mesmo servidor em http://127.0.0.1:8722/intercientifica/.

## Como editar

As páginas HTML são geradas. Para mudar textos, produtos, cabeçalho ou rodapé, edite `_tools/data_site.py`, `_tools/build.py` ou `_tools/pages.py` e rode, a partir desta pasta:

```bash
python _tools/pages.py
```

Requer Python 3 com Pillow. O CSS e o JS são editados diretamente.

## Como publicar sem afetar a Proposta 1

Este repositório tem o próprio remoto e o próprio GitHub Pages (branch `main`, pasta raiz). Um `git push` aqui só atualiza https://apxweb.github.io/intercientifica-proposta-2/. Não altere o remoto nem copie arquivos para `portfolio-projects/intercientifica/`.

## Comportamentos importantes

- **Formulário:** não existe servidor. Ao enviar, o site abre o WhatsApp oficial (+55 12 99108-7550, do Linktree da empresa) com a mensagem montada e diz claramente que ela ainda precisa ser enviada lá.
- **Automação, de perto (3D principal):** o scroll controla a cena. Cada texto com `data-pose` é uma âncora; entre duas âncoras a pose (câmera, porta, pórtico, deck, tela) é interpolada com platôs para leitura, a mesma lógica do projeto NOIR. Ir, parar e voltar funcionam. As poses estão no topo de `assets/js/flex.js`.
- **Sem WebGL, com movimento reduzido ou economia de dados:** a seção mostra quadros estáticos da própria cena, trocados conforme a etapa; todo o texto fica fora do canvas. O trilho de etapas é navegável pelo teclado.
- **Leitura multiplex:** o mapa das microesferas se forma conforme a seção passa pela tela; nada se move sem o scroll. Sem WebGL aparece a figura SVG equivalente.
- **Mapa:** o Google Maps só carrega quando o visitante pede.

## Conteúdo: fontes e pontos a confirmar com o cliente

Todo o conteúdo vem do site oficial (intercientifica.com.br) e das publicações da própria empresa. Nada foi inventado.

A confirmar:
1. **Ano de fundação.** O site oficial diz 1994; a matéria da Luminex republicada no site diz "fundada em 1992". Usamos 1994.
2. **"30 anos de experiência"** no site oficial; usamos "desde 1994" para não envelhecer.
3. **Números do NeoMAP® 4PLEX** (1.750.300 análises, picote de 3,00 mm, 25 leituras por parâmetro, até 8 placas e mais de 3.000 análises por rotina) vêm de uma notícia sem data; confirmar se seguem atuais.
4. **Notícias** não têm data no site oficial e aparecem como "Arquivo". Duas estão fora do ar no site original e ficam listadas sem link.
5. **Linhas de características por kit** seguem a ordem do site oficial, onde a lista aparece antes do nome de cada produto.
6. **Foto do NeoMAP® 3Plex** é a mesma para IgG e IgM, como no site oficial.
7. **Instruções de uso e fichas técnicas** não estão publicadas; as fichas do site direcionam para a equipe científica.

## O modelo do Opentrons Flex

Não há modelo 3D oficial público do Flex. A máquina é construída em código (`buildMachine()` em `assets/js/flex.js`) a partir de fontes oficiais da Opentrons:

- manual do Flex, seções "System Specifications" e "Robot components" (docs.opentrons.com/flex): 87 × 69 × 84 cm, aço e alumínio usinado, porta frontal e janelas laterais de policarbonato, tela de 7" na frente à direita, luz de status no topo, câmera de 2 MP, deck de alumínio, pórtico X/Y com precisão de 0,1 mm;
- definição de deck do código aberto (repositório Opentrons/opentrons, `shared-data/deck/definitions/5/ot3_standard.json`): posições de 128 × 86 mm com passo de 164 × 107 mm.

Formas internas (carro das pipetas, trilhos) são aproximações visuais das fotos oficiais, e o material de laboratório no deck é ilustrativo. Se a Opentrons ou o cliente fornecerem um GLB oficial, troque `buildMachine()` mantendo os nomes dos grupos (porta, pórtico, carro, pipetas, posições, tela, status) e as poses continuam valendo.

### Para regerar os quadros estáticos

Com o site servido localmente, abra a home com `window.__forcePose = '<pose>'` definido antes do carregamento (por exemplo, com `addInitScript` do Playwright), esconda `.mast`, `.auto__pins`, `.auto__rail`, `.auto__cap` e `.auto__steps`, e capture `.auto__stage` em 1600 × 1000. Para o herói, use também `window.__noShift = true` em 1140 × 1350. Converta para WebP (1600 e 800 px).

## A confirmar com o cliente (automação)

8. **Qual equipamento Opentrons a Intercientifica usa.** O site oficial cita só "sistema da Hamilton® Robotics e Opentrons®". A cena mostra um **Opentrons Flex** por decisão da APX; os textos não afirmam que é o equipamento da Intercientifica. Se for o OT-2, a Opentrons publica um modelo de referência oficial (repositório Opentrons/ot2, sem arquivo de licença formal; verificar antes de usar).
9. **Automação com o NeoMAP® 4PLEX:** os dados de "até 8 placas" e "mais de 3.000 análises por rotina" referem-se ao NIMBUS (Hamilton®), segundo a notícia da empresa.
10. **Foto do topo da home** (`assets/img/lab/99eb321d-*.webp`): quadro de capa de um vídeo do site oficial (mídia `92fb3b_99eb321d…` da conta Wix da Intercientifica), legendado "Laboratório da Intercientifica". Se houver foto original em alta resolução, vale substituir.
