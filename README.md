# Intercientifica · Proposta 2 (APX Web)

Segunda proposta de site para a Intercientifica, independente da primeira.

## As duas propostas

| | Proposta 1 | Proposta 2 |
|---|---|---|
| Pasta local | `portfolio-projects/intercientifica/` | `portfolio-projects/intercientifica-proposta-2/` |
| Repositório | github.com/APXWeb/intercientifica (branch `master`) | github.com/APXWeb/intercientifica-proposta-2 (branch `main`) |
| Endereço | https://apxweb.github.io/intercientifica/ | https://apxweb.github.io/intercientifica-proposta-2/ |
| Conceito | Base clara e clínica, cartões arredondados, página única | O rótulo do kit: caixa vermelha, células de rótulo, REF e Σ como tipografia, câmara escura com microesferas em 3D |

São dois repositórios git separados. Nada desta pasta é publicado no repositório da Proposta 1, e vice-versa.

## Estrutura

```
index.html                  Home: caixa, princípio (scroll + WebGL), dados, linhas, automação, qualidade, publicações
produtos/                   Catálogo com filtros (linha, formato) e busca (doença, marcador, REF)
produtos/<kit>/             Ficha de cada um dos 9 kits
empresa/                    Quem somos, missão, valores, trajetória, equipe, compromisso, sede
publicacoes/                25 artigos e 14 notícias, com filtro e busca; uma página por publicação
contato/                    Formulário que abre o WhatsApp oficial com a mensagem pronta
404.html                    Página de erro do GitHub Pages
assets/css/site.css         Design system completo (tokens no topo do arquivo)
assets/js/site.js           Navegação, revelações, filtros, formulário, narrativa por scroll
assets/js/beads.js          Microesferas em Three.js (carregado sob demanda, só na home)
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
- **3D:** ilustrativo e rotulado como tal. Não carrega com movimento reduzido, economia de dados ou sem WebGL; nesses casos aparecem figuras SVG equivalentes. Tem botão de pausa.
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
