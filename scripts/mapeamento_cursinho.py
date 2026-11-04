# mapeamento_cursinho.py - mapeia temas do banco para capítulos do cursinho
# Cada tema individual do banco pode mapear para múltiplos capítulos
MAPA_CURSINHO = {
    "geografia": {
        # GEOGRAFIA I - Frente A
        "Capítulo 01 - Geomorfologia 1: Unidades de relevo": [
            "relevo", "placas tectônicas", "tectônica", "vulcões", "fenda tectônica",
            "crosta terrestre", "geomorfologia", "escudos cristalinos", "mineração",
            "amazônia", "cerrado", "solos", "degradação", "feição fisiográfica",
            "rochas ígneas", "calcário", "intemperismo químico", "desmoronamento de solo",
        ],
        "Capítulo 02 - Geomorfologia II: Classificação do relevo brasileiro": [
            "relevo brasileiro", "unidades de relevo", "planalto", "depressão",
            "planície", "maciço", "amazônia", "cerrado", "caatinga", "pampa",
        ],
        "Capítulo 03 - Introdução à climatologia": [
            "clima", "climatologia", "temperatura", "umidade", "precipitação",
            "massa de ar", "frente", "ciclone", "anticiclone",
        ],
        "Capítulo 04 - Climatologia I: Circulação atmosférica e marinha": [
            "circulação atmosférica", "circulação marinha", "vento", "corrente marinha",
            "alísios", "monsão", "corrente do brasil", "corrente das falklands",
            "massa de ar", "frente", "zona de convergência",
        ],
        "Capítulo 05 - Climatologia II: Classificação climática e climogramas brasileiros": [
            "classificação climática", "climograma", "clima equatorial", "clima tropical",
            "clima semiárido", "clima de altitude", "clima subtropical",
            "semiárido", "caatinga", "amazônia",
        ],
        "Capítulo 06 - Mudanças climáticas locais e regionais": [
            "mudanças climáticas locais", "ilha de calor", "poluição do ar",
            "inversão térmica", "smog", "chuva ácida", "cidade", "rio tietê",
        ],
        "Capítulo 07 - Mudanças climáticas globais": [
            "mudanças climáticas globais", "aquecimento global", "effecto estufa",
            "co₂", "queimadas", "desmatamento", "crise climática", "protocolo de kyoto",
            "acordo de paris", "cop", "mitigação", "sustentabilidade",
        ],
        "Capítulo 08 - Desenvolvimento sustentável e acordos ambientais": [
            "desenvolvimento sustentável", "acordos ambientais", "rio-92", "cop",
            "agenda 21", "objetivos de desenvolvimento sustentável", "ods",
            "energia renovável", "matriz energética", "energia hidrelétrica",
            "energia eólica", "energia solar", "biocombustíveis",
        ],
        # GEOGRAFIA I - Frente B
        "Capítulo 09 - Introdução à geografia urbana": [
            "cidade", "urbanização", "espaço urbano", "uso do solo urbano",
            "zoneamento", "plano diretor", "estatuto da cidade",
        ],
        "Capítulo 10 - Urbanização acelerada: problemas urbanos": [
            "urbanização acelerada", "favela", "mocambo", "periferia", "conurbação",
            "região metropolitana", "macrocefalia urbana", "exclusão urbana",
            "habitação", "saneamento", "transporte urbano", "mobilidade urbana",
        ],
        "Capítulo 11 - Geografia das redes: transporte, energia e telecomunicações": [
            "rede de transporte", "rodovia", "ferrovia", "porto", "aeroporto",
            "rede de energia", "telecomunicações", "logística", "transporte",
            "navegação fluvial", "rio reno",
        ],
        "Capítulo 12 - Regiões metropolitanas e megalópoles": [
            "região metropolitana", "megalópole", "conurbação", "macrometrópole",
            "metrópole", "área metropolitana", "região metropolitana de são paulo",
            "região metropolitana do rio de janeiro",
        ],
        "Capítulo 13 - Industrialização: Revoluções industriais": [
            "industrialização", "revolução industrial", "primeira revolução industrial",
            "segunda revolução industrial", "vapor", "fábrica", "trabalho fabril",
            "capitalismo industrial",
        ],
        "Capítulo 14 - Industrialização tardia: economias emergentes": [
            "industrialização tardia", "economias emergentes", "brics", "china",
            "índia", "brasil industrial", "desenvolvimento desigual",
        ],
        "Capítulo 15 - Nova DIT e Modelo organizacional toyotista": [
            "nova dit", "divisão internacional do trabalho", "toyotismo",
            "modelo toyotista", "flexibilização", "lean production", "just in time",
            "cadence", "indústria 4.0",
        ],
        "Capítulo 16 - Evolução do capitalismo no século XX": [
            "capitalismo", "evolução do capitalismo", "século XX", "crise de 1929",
            "nova economia", "globalização", "neoliberalismo", "financeirização",
        ],
        # GEOGRAFIA II - Frente A
        "Capítulo 01 - Cartografia I: Introdução à Cartografia": [
            "cartografia", "mapa", "escala", "legenda", "símbolos cartográficos",
            "projeção cartográfica", "sistema de coordenadas", "latitude", "longitude",
        ],
        "Capítulo 02 - Cartografia II: Movimentos da Terra": [
            "movimentos da terra", "rotação", "translação", "fuso horário",
            "solstício", "equinócio", "sombra", "orientação", "dia e noite",
        ],
        "Capítulo 03 - Cartografia III: Representação cartográfica": [
            "representação cartográfica", "mapa temático", "mapa de coroplese",
            "mapa de símbolos", "mapa de isolinhas", "cartograma",
            "informação geográfica", "sensoriamento remoto", "sig",
        ],
        "Capítulo 04 - Dinámica interna da Terra e agentes endógenos": [
            "dinâmica interna da terra", "placas tectônicas", "movimentos endógenos",
            "vulcanismo", "sismicismo", "orogênese", "placa continental",
            "placa oceânica", "subducção", "fenda", "falha",
        ],
        "Capítulo 05 - Estrutura e tempo geológicos": [
            "estrutura geológica", "tempo geológico", "era geológica",
            "período geológico", "época geológica", "fóssil", "datação radiométrica",
        ],
        "Capítulo 06 - Pedogénese e processos erosivos": [
            "pedogênese", "formação do solo", "solo", "horizonte do solo",
            "processos erosivos", "erosão hídrica", "erosão eólica", "desmatamento",
            "conservação do solo", "uso do solo",
        ],
        "Capítulo 07 - Técnicas conservativas e degradativas do solo": [
            "técnicas conservativas", "agricultura conservacionista",
            "plantio direto", "rotação de culturas", "curva de nível",
            "técnicas degradativas", "queimada", "desmatamento", "sobrepastagem",
        ],
        # GEOGRAFIA II - Frente B
        "Capítulo 08 - Demografia I: Conceitos e teorias demográficos": [
            "demografia", "população", "densidade demográfica", "natalidade",
            "mortalidade", "crescimento populacional", "taxa de fecundidade",
            "pirâmide etária", "expectativa de vida", "migratório",
        ],
        "Capítulo 09 - Demografia II: Fases demográficas e transição etária": [
            "transição demográfica", "fases demográficas", "estacionário",
            "expansivo", "constante", "diminuente", "envelhecimento populacional",
            "janela demográfica",
        ],
        "Capítulo 10 - Migrações internacionais": [
            "migrações internacionais", "migração", "imigração", "emigração",
            "refugiados", "fronteiras", "deslocamento", "fluxo migratório",
            "saldo migratório",
        ],
        "Capítulo 11 - Migrações brasileiras": [
            "migrações brasileiras", "migração interna", "migração rural-urbana",
            "êxodo rural", "marcha para o oeste", "migração nordeste-sudeste",
            "itinerários afetivos", "deslocamento populacional",
        ],
    },
    "historia": {
        # HISTÓRIA I - Frente A
        "Capítulo 01 - Mundo Antigo: Grécia": [
            "grécia", "grego", "cidade-estado", "polis", "atenas", "esparta",
            "democracia ateniense", "filosofia grega", "mitologia grega",
            "guerras médicas", "peloponeso",
        ],
        "Capítulo 02 - Mundo Antigo: Roma": [
            "roma", "romano", "república romana", "império romano", "julius caesar",
            "augusto", "pax romana", "lei das doze tábuas", "cristianismo primitivo",
            "queda do império romano do ocidente",
        ],
        "Capítulo 03 - Alta Idade Média": [
            "alta idade média", "idade média", "feudalismo", "vassalo",
            "senhorio", "cristianismo medieval", "império carolíngio",
            "invasões bárbaras", "monasticismo",
        ],
        "Capítulo 04 - Baixa Idade Média": [
            "baixa idade média", "crise do feudalismo", "peste negra",
            "guerra dos cem anos", "comuna", "burguesia", "feira medieval",
            "universidades medievais", "catedral gótica",
        ],
        "Capítulo 05 - Monarquia absolutistas": [
            "monarquia absoluta", "absolutismo", "luís xiv", "estado absoluto",
            "divino direito dos reis", "versalhes", "centralização estatal",
        ],
        "Capítulo 06 - Teorias políticas da Idade Moderna": [
            "teorias políticas idade moderna", "maquiavel", "hobbes", "locke",
            "montesquieu", "contrato social", "separação dos poderes",
            "soberania", "estado moderno",
        ],
        "Capítulo 07 - Expansão marítima e comercial": [
            "expansão marítima", "expansão comercial", "descobrimentos",
            "cristóvão colombo", "vasco da gama", "magalhães", "tordesilhas",
            "carrera de indias", "nau da índia",
        ],
        "Capítulo 08 - Renascimento": [
            "renascimento", "humanismo", "leonardo da vinci", "michelangelo",
            "arte renascentista", "perspectiva", "imprensa de gutenberg",
        ],
        "Capítulo 09 - Reforma Protestante e Contrarreforma": [
            "reforma protestante", "martinho lutero", "calvino", "contrarreforma",
            "concílio de trento", "igreja católica", "igreja protestante",
            "anglicanismo", "inquisição",
        ],
        # HISTÓRIA I - Frente B
        "Capítulo 10 - América Castelhana": [
            "américa castelhana", "nova espanha", "vice-reino do peru",
            "conquista do méxico", "conquista do peru", "cortes", "pizarro",
            "encomenda", "mita", "potosi", "prata", "ouro",
        ],
        "Capítulo 11 - América Portuguesa: aspectos políticos e econômicos": [
            "américa portuguesa", "brasil colônia", "capitanias hereditárias",
            "governo-geral", "salvador", "rio de janeiro", "economia colonial",
            "comércio colonial", "pacto colonial",
        ],
        "Capítulo 12 - América Portuguesa: sociedade escravocrata e cultura colonial": [
            "sociedade escravocrata", "escravidão", "escravidão africana",
            "trabalho escravo", "cultura colonial", "senhor de engenho",
            "senzala", "quilombo", "resistência escrava",
        ],
        "Capítulo 13 - América Portuguesa: invasões estrangeiras": [
            "invasões estrangeiras", "invasão francesa", "invasão holandesa",
            "frança antártica", "frança equinocial", "nova holanda",
            "batalha dos guararapes", "john maurice de nassau",
        ],
        "Capítulo 14 - América Portuguesa - Expansão territorial e bandeirantismo": [
            "expansão territorial", "bandeirantismo", "bandeirantes",
            "expansão para o oeste", "tratado de madri", "limites do brasil",
        ],
        "Capítulo 15 - América Portuguesa - Mineração e Revoltas separatistas": [
            "mineração", "ciclo do ouro", "minas gerais", "ouro", "diamante",
            "revolta separatista", "conjuração mineira", "tiradentes",
            "revolta de vila rica", "inconfidência mineira",
        ],
        # HISTÓRIA II - Frente A
        "Capítulo 01 - Revolução Inglesa": [
            "revolução inglesa", "cromwell", "revolução puritana",
            "revolução gloriosa", "carlos i", "carlos ii", "james ii",
            "declaração de direitos", "parlamento inglês",
        ],
        "Capítulo 02 - Revolução Industrial": [
            "revolução industrial", "máquina a vapor", "james watt",
            "fábrica", "trabalho fabril", "proletariado", "burguesia industrial",
            "tear mecânico", "carvão", "ferro",
        ],
        "Capítulo 03 - Iluminismo": [
            "iluminismo", "voltaire", "rousseau", "montesquieu", "diderot",
            "razão", "crítica", "tolerância", "enciclopédia", "despotismo esclarecido",
        ],
        "Capítulo 04 - Revolução Francesa": [
            "revolução francesa", "1789", "bastilha", "declaração dos direitos do homem",
            "terceiro estado", "luís xvi", "marat", "robespierre", "terror",
            "direito", "liberdade", "igualdade", "fraternidade",
        ],
        "Capítulo 05 - Era Napoleónica e Congresso de Viena": [
            "napoleão", "era napoleônica", "congresso de viena",
            "código napoleônico", "campanhas de napoleão", "exílio de napoleão",
            "concerto europeu", "metternich",
        ],
        "Capítulo 06 - Revoluções burguesas e unificações": [
            "revoluções burguesas", "revolução de 1830", "revolução de 1848",
            "primavera dos povos", "unificação da itália", "unificação da alemanha",
            "garibaldi", "cavour", "bismarck",
        ],
        "Capítulo 07 - Ideário político do século XIX": [
            "ideário político século XIX", "liberalismo", "conservadorismo",
            "socialismo", "marxismo", "anarquismo", "nacionalismo",
            "sucesso", "democracia",
        ],
        "Capítulo 08 - Imperialismo e Neocolonialismo": [
            "imperialismo", "neocolonialismo", "corrida pela áfrica",
            "conferência de berlim", "império britânico", "império francês",
            "domínio colonial", "exploração de colônias",
        ],
        "Capítulo 09 - Estados Unidos no século XIX": [
            "estados unidos século XIX", "guerra de secessão", "abraham lincoln",
            "abolição da escravidão", "expansão para o oeste", "monroe doctrine",
            "destino manifesto",
        ],
        # HISTÓRIA II - Frente B
        "Capítulo 10 - América Inglesa": [
            "améria inglesa", "treze colônias", "nova inglaterra",
            "virginia", "massachusetts", "peregrinos", "mayflower",
        ],
        "Capítulo 11- Emancipação da América inglesa": [
            "emancipação da américa inglesa", "revolução americana",
            "declaração de independência dos estados unidos", "george washington",
            "guerra da independência americana", "constituição americana",
        ],
        "Capítulo 12 - Emancipação da América espanhola": [
            "emancipação da américa espanhola", "guerras de independência",
            "simón bolívar", "jose de san martín", "miguel hidalgo",
            "independência da américa latina",
        ],
        "Capítulo 13 - Brasil Império: Período Joanino (1808-1822)": [
            "período joanino", "dom joão vi", "transferência da família real",
            "abertura dos portos", "fundação de instituições no brasil",
            "elevar o brasil a reino unido",
        ],
        "Capítulo 14 - Brasil Império: Primeiro Reinado (1822-1831)": [
            "primeiro reinado", "dom pedro i", "independência do brasil",
            "7 de setembro de 1822", "constituição de 1824", "dissolução da assembleia",
            "abdicação de dom pedro i",
        ],
        "Capítulo 15 - Brasil Império: Período Regencial (1831-1840)": [
            "período regencial", "regência trina", "regência de um único",
            "revolta dos malês", "cabanagem", "balaiada", "revolta farroupilha",
            "revolta da praia",
        ],
        "Capítulo 16 - Brasil Império: Segundo Reinado (1840-1889)": [
            "segundo reinado", "dom pedro ii", "idade de ouro do brasil",
            "guerra do paraguai", "questão religiosa", "abolição da escravidão",
            "lei áurea", "republicanismo", "golpe de 1889",
        ],
    },
}

print("Mapeamento do cursinho carregado:")
for mat, caps in MAPA_CURSINHO.items():
    print(f"  {mat}: {len(caps)} capítulos")
