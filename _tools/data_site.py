"""Conteúdo factual do site, transcrito do site oficial (intercientifica.com.br).
Nada aqui é inventado: cada texto tem origem no site oficial ou nas publicações
da própria empresa. Ao alterar, confira a fonte."""

WHATSAPP = "5512991087550"          # Linktree oficial da empresa
WHATSAPP_LABEL = "+55 (12) 99108-7550"
PHONE = "+551239499700"
PHONE_LABEL = "+55 (12) 3949-9700"
HOURS = "Seg a Sex, 8:00 às 17:00"
EMAILS = [
    ("Equipe científica", "ic@intercientifica.com.br"),
    ("Equipe comercial", "b2c@intercientifica.com.br"),
    ("Assessoria científica", "a.cientifica@intercientifica.com.br"),
    ("Contato geral", "contato@intercientifica.com.br"),
]
ADDRESS_LINES = ["Av. Shishima Hifumi, 2911, Mod. 306-309", "Urbanova, Parque Tecnológico UNIVAP", "São José dos Campos, SP, CEP 12244-000", "Brasil"]
MAPS_EMBED = "https://www.google.com/maps?q=Av.+Shishima+Hifumi,+2911,+S%C3%A3o+Jos%C3%A9+dos+Campos+-+SP,+12244-000&output=embed"
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=Av.+Shishima+Hifumi,+2911,+S%C3%A3o+Jos%C3%A9+dos+Campos+-+SP,+12244-000"
INSTAGRAM = "https://www.instagram.com/intercientifica/"
FACEBOOK = "https://www.facebook.com/intercientifica.oficial"

LINES = {
    "neomap": {
        "name": "NeoMAP", "method": "Ensaios multiplex",
        "desc": "Kits para ensaios múltiplos simultâneos, utilizando a plataforma xMAP®, da Luminex®. Vários analitos de uma mesma amostra são analisados em um único ensaio.",
        "diseases": ["Hipotireoidismo Congênito", "Hiperplasia Adrenal Congênita", "Fibrose Cística", "Toxoplasmose", "Rubéola", "Citomegalovírus"],
    },
    "neolisa": {
        "name": "NeoLISA", "method": "Ensaios enzimáticos e colorimétricos",
        "desc": "Kits em ensaios enzimáticos e colorimétricos para triagem de doenças em recém-nascidos, com opções de ensaio manual, semiautomatizado e automatizado, conforme o produto.",
        "diseases": ["Fenilcetonúria", "Galactosemia", "Doença do Xarope de Bordo", "Deficiência de G6PD", "Deficiência de Biotinidase"],
    },
}

# Listas de características transcritas do site oficial, na ordem em que aparecem.
PRODUCTS = [
    {
        "slug": "neomap-4plex", "line": "neomap", "name": "NeoMAP® 4Plex", "short": "4Plex",
        "assay": "Ensaio multiplex", "formats": ["manual", "automatizado"],
        "ind": "Detecção simultânea dos marcadores TSH, T4, 17-OH e IRT na triagem de Hipotireoidismo Congênito, Hiperplasia Adrenal Congênita e Fibrose Cística.",
        "targets": "TSH, T4, 17-OH, IRT",
        "diseases": ["Hipotireoidismo Congênito", "Hiperplasia Adrenal Congênita", "Fibrose Cística"],
        "pres": [("2.300", "16635-230")],
        "img": "neomap-4plex", "img_w": 900, "img_h": 532,
        "feat": [
            "Ensaio manual e automatizado",
            "Realização simultânea de TSH, T4, 17-OH e IRT",
            "Maior facilidade na integração dos dados",
            "Precisão de 50 a 100 vezes maior que os métodos fluorimétricos ELISA tradicionais",
            "Redução do tempo de processamento em mais de 50%",
            "Redução do volume de água reagente, material para descarte e menor dependência de espaço físico",
            "Diminuição de volume de picotagem e microplacas",
        ],
        "kw": ["4plex", "tsh", "fibrose", "hipertripsinemia", "5plex"],
    },
    {
        "slug": "neomap-3plex-igg", "line": "neomap", "name": "NeoMAP® 3Plex IgG", "short": "3Plex IgG",
        "assay": "Ensaio multiplex", "formats": ["manual"],
        "ind": "Determinação semiquantitativa de anticorpos IgG contra Toxoplasma gondii, Rubéola e Citomegalovírus, através de realização simultânea em formato multiplex.",
        "targets": "Anticorpos IgG: Toxoplasma gondii, Rubéola, Citomegalovírus",
        "diseases": ["Toxoplasmose", "Rubéola", "Citomegalovírus"],
        "pres": [("1.920", "18635-192")],
        "img": "neomap-3plex", "img_w": 900, "img_h": 770, "img_shared": True,
        "feat": [
            "Ensaio manual",
            "Realização simultânea para a análise de anticorpos da classe IgG contra Toxoplasmose, Rubéola e Citomegalovirose",
            "Maior facilidade na integração dos dados",
            "Precisão de 50 a 100 vezes maior que os métodos fluorimétricos ELISA tradicionais",
            "Redução do tempo de processamento em mais de 50%",
            "Redução do volume de água reagente, material para descarte e menor dependência de espaço físico",
            "Diminuição de volume de picotagem e microplacas",
        ],
        "kw": ["torsch", "torch", "infecciosas", "citometria"],
    },
    {
        "slug": "neomap-3plex-igm", "line": "neomap", "name": "NeoMAP® 3Plex IgM", "short": "3Plex IgM",
        "assay": "Ensaio multiplex", "formats": ["manual"],
        "ind": "Determinação semiquantitativa de anticorpos IgM contra Toxoplasma gondii, Rubéola e Citomegalovírus, através de realização simultânea em formato multiplex.",
        "targets": "Anticorpos IgM: Toxoplasma gondii, Rubéola, Citomegalovírus",
        "diseases": ["Toxoplasmose", "Rubéola", "Citomegalovírus"],
        "pres": [("1.920", "19635-192")],
        "img": "neomap-3plex", "img_w": 900, "img_h": 770, "img_shared": True,
        "feat": [
            "Ensaio manual",
            "Realização simultânea para análise de anticorpos da classe IgM contra Toxoplasmose, Rubéola e Citomegalovirose",
            "Maior facilidade na integração dos dados",
            "Precisão de 50 a 100 vezes maior que os métodos fluorimétricos ELISA tradicionais",
            "Redução do tempo de processamento em mais de 50%",
            "Redução do volume de água reagente, material para descarte e menor dependência de espaço físico",
            "Diminuição de volume de picotagem e microplacas",
        ],
        "kw": ["torsch", "torch", "infecciosas", "citometria"],
    },
    {
        "slug": "neolisa-pku", "line": "neolisa", "name": "NeoLISA® PKU", "short": "PKU",
        "assay": "Ensaio enzimático e colorimétrico", "formats": ["manual", "semiautomatizado", "automatizado"],
        "ind": "Quantificação da Fenilalanina na triagem neonatal da Fenilcetonúria.",
        "targets": "Fenilalanina",
        "diseases": ["Fenilcetonúria"],
        "pres": [("2.000", "1570-200")],
        "img": "neolisa-pku", "img_w": 900, "img_h": 588,
        "feat": [
            "Ensaio manual, semiautomatizado e automatizado",
            "Tempo reduzido de ensaio",
            "Não sofre intercorrências de antibióticos ou outros medicamentos",
            "Altamente sensível e específico",
        ],
        "kw": ["fenilceton", "fenilalanina"],
    },
    {
        "slug": "neolisa-gal", "line": "neolisa", "name": "NeoLISA® GAL", "short": "GAL",
        "assay": "Ensaio enzimático e colorimétrico", "formats": ["manual", "automatizado"],
        "ind": "Quantificação da Galactose Total na triagem neonatal da Galactosemia.",
        "targets": "Galactose Total",
        "diseases": ["Galactosemia"],
        "pres": [("2.000", "2570-200")],
        "img": "neolisa-gal", "img_w": 900, "img_h": 565,
        "feat": [
            "Ensaio manual e automatizado",
            "Tempo reduzido de ensaio",
            "Realiza quantificação da Galactose Total",
            "Altamente sensível e específico",
            "Procedimento laboratorial rápido e simplificado",
        ],
        "kw": ["galactosemia"],
    },
    {
        "slug": "neolisa-msud", "line": "neolisa", "name": "NeoLISA® MSUD", "short": "MSUD",
        "assay": "Ensaio enzimático e colorimétrico", "formats": ["manual", "automatizado"],
        "ind": "Quantificação da Leucina, Isoleucina e Valina na triagem da Doença do Xarope de Bordo (MSUD).",
        "targets": "Leucina, Isoleucina, Valina",
        "diseases": ["Doença do Xarope de Bordo"],
        "pres": [("2.000", "4570-200")],
        "img": "neolisa-msud", "img_w": 900, "img_h": 611,
        "feat": [
            "Ensaio manual e automatizado",
            "Tempo reduzido de ensaio",
            "Não sofre interferência de antibióticos ou outros medicamentos",
            "Altamente sensível e específico",
            "Procedimento laboratorial simplificado",
        ],
        "kw": ["xarope de bordo", "leucinose"],
    },
    {
        "slug": "neolisa-g6pd", "line": "neolisa", "name": "NeoLISA® G6PD", "short": "G6PD",
        "assay": "Ensaio enzimático e colorimétrico", "formats": ["manual"],
        "ind": "Avaliação da atividade enzimática da Glicose-6-fosfato Desidrogenase na triagem da Deficiência de G6PD.",
        "targets": "Atividade enzimática da G6PD",
        "diseases": ["Deficiência de G6PD"],
        "pres": [("500", "3570-050"), ("2.000", "3570-200")],
        "img": "neolisa-g6pd", "img_w": 900, "img_h": 549,
        "feat": [
            "Ensaio manual",
            "Tempo reduzido de ensaio",
            "Não sofre interferência de antibióticos ou outros medicamentos",
            "Altamente sensível e específico",
            "Procedimento laboratorial simplificado",
        ],
        "kw": ["g6pd", "g-6-pd", "glicose-6", "metemoglobinemia"],
    },
    {
        "slug": "neolisa-bio-quantitativo", "line": "neolisa", "name": "NeoLISA® BIO Quantitativo", "short": "BIO Quantitativo",
        "assay": "Ensaio quantitativo", "formats": ["manual", "semiautomatizado"],
        "ind": "Avaliação da atividade enzimática da Biotinidase na triagem da Deficiência de Biotinidase.",
        "targets": "Atividade enzimática da Biotinidase",
        "diseases": ["Deficiência de Biotinidase"],
        "pres": [("3.000", "17570-300")],
        "img": "neolisa-bio-quant", "img_w": 900, "img_h": 955,
        "feat": [
            "Ensaio manual e semiautomatizado",
            "Diferenciação precisa entre casos normais, intermediários e deficientes",
            "Reagentes prontos para o uso",
            "Procedimento laboratorial simplificado",
        ],
        "kw": ["biotinidase", "neolisa bio"],
    },
    {
        "slug": "neolisa-bio-qualitativo", "line": "neolisa", "name": "NeoLISA® BIO Qualitativo", "short": "BIO Qualitativo",
        "assay": "Ensaio qualitativo", "formats": ["manual"],
        "ind": "Avaliação da atividade enzimática da Biotinidase na triagem da Deficiência de Biotinidase.",
        "targets": "Atividade enzimática da Biotinidase",
        "diseases": ["Deficiência de Biotinidase"],
        "pres": [("300", "9570-030"), ("3.000", "9570-300")],
        "img": "neolisa-bio-qual", "img_w": 900, "img_h": 771,
        "feat": [
            "Ensaio manual",
            "Diferenciação precisa entre casos normais, intermediários e deficientes",
            "Reagentes prontos para o uso",
            "Procedimento laboratorial simplificado",
        ],
        "kw": ["biotinidase", "neolisa bio"],
    },
]

VALUES = [
    ("Inovação", "Estimular a equipe na busca constante pela inovação de produtos e processos."),
    ("Independência", "Desenvolvimento visando a reduzir a dependência com outras empresas."),
    ("Imagem", "Elevar e divulgar a imagem da empresa nacional como solução para as necessidades do mercado."),
    ("Qualidade", "Superar as expectativas dos clientes quanto aos nossos produtos e serviços."),
    ("Custos", "Monitorar continuamente e reduzir desperdícios para a obtenção de processos enxutos."),
    ("Entrega", "Atender por ordem de pedidos os clientes no tempo certo."),
    ("Ética", "Garantir que as relações com clientes e funcionários sejam baseadas na ética e conduta dos negócios e na empresa."),
    ("Segurança", "Trabalhar de maneira eficiente, garantindo a segurança dos usuários e apoiando nosso sistema de gestão da qualidade, que tem como base a inovação de processos visando a melhoria contínua."),
    ("Sustentabilidade", "Utilizar de maneira consciente os recursos naturais e buscar a redução e destinação correta de resíduos."),
]

QA_PROGRAMS = [
    ("PNCQ", "Programa Nacional de Controle de Qualidade", "Brasil"),
    ("CDC NSQAP", "Newborn Screening Quality Assurance Program", "EUA"),
    ("SLEIMPN", "Sociedad Latinoamericana de Errores Innatos del Metabolismo y Pesquisa Neonatal", "América Latina"),
    ("ISNS", "International Society for Neonatal Screening", "Internacional"),
    ("PEEC", "Programa de Evaluación Externa de Calidad, Fundación Bioquímica Argentina", "Argentina"),
]

# Marcos com fonte nas notícias da própria empresa (chave = trecho do título da notícia).
TIMELINE = [
    ("1994", "Fundação", "Fundada com o objetivo social de pesquisar e desenvolver produtos e serviços para programas de triagem de doenças neonatais e pré-natais.", None),
    ("1999", "Parceria Luminex®", "Torna-se um dos primeiros parceiros de tecnologias licenciadas da Luminex na América Latina.", "destaque como parceiro"),
    ("2009", "Certificação ANVISA", "Recebe da ANVISA o Certificado de Boas Práticas de Fabricação, Classe de Risco III.", "Certificado de Boas Práticas"),
    ("2010", "Prêmio FINEP", "Vence o prêmio FINEP 2010 na Região Sudeste, na categoria Micro e Pequena Empresa.", "FINEP 2010"),
    ("2011", "Prêmio ABIMO Inova Saúde", "Reconhecida pela ABIMO como a empresa do setor da saúde que apresentou o melhor case de inovação.", "Abimo Inova"),
    ("2023", "APHL/ISNS Newborn Screening Symposium", "Participa do simpósio internacional de triagem neonatal em Sacramento, Califórnia, Estados Unidos.", "APHL/ISNS"),
]

SUBJECTS = ["Informações sobre um kit", "Triagem Neonatal", "Triagem Pré-Natal", "Equipamentos e automação", "Assuntos comerciais", "Recursos Humanos", "Reclamações", "Outros"]
COUNTRY_CODES = [("BR", "+55"), ("AR", "+54"), ("BO", "+591"), ("CL", "+56"), ("CO", "+57"), ("EC", "+593"), ("MX", "+52"), ("PY", "+595"), ("PE", "+51"), ("UY", "+598"), ("VE", "+58"), ("US", "+1"), ("PT", "+351"), ("ES", "+34")]
