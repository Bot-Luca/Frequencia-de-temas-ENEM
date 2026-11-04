# generate_summaries.py - gera os 20 resumos (5 tipos x 4 matérias)
import json
from pathlib import Path
from collections import Counter

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
DADOS = BASE / "dados"
rows = [json.loads(l) for l in (DADOS / "banco_questoes.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
top5 = json.loads((DADOS / "top5.json").read_text(encoding="utf-8"))
MATERIAS = ["historia", "geografia", "filosofia", "sociologia"]

# Build lookup
rows_by_mat_tipo = {}
for r in rows:
    key = (r["materia"], r["tipo"])
    rows_by_mat_tipo.setdefault(key, []).append(r)

top5_set = {(mat, itm["tipo"]): itm for mat, itens in top5.items() for itm in itens}

# For each mat+tipo in top5, get all instances sorted by (ano, q)
mat_tipo_instances = {}
for mat in MATERIAS:
    for itm in top5[mat]:
        tipo = itm["tipo"]
        key = (mat, tipo)
        inst = [r for r in rows if r["materia"] == mat and r["tipo"] == tipo and r["top5"]]
        inst.sort(key=lambda r: (r["ano"], r["q"]))
        mat_tipo_instances[key] = inst

# Which will be exemplo.md (first of each mat)
mat_first_summary = {}
for mat in MATERIAS:
    tipos_mat = top5[mat]
    mat_first_summary[mat] = tipos_mat[0]["tipo"]

summary_dir = BASE / "Markdowns"
summary_dir.mkdir(exist_ok=True)

EMBASAMENTO = "curto"
VARIACOES = "não"
FONTES = "não"
RESOLVER = "sim"
SALVAR = "sim"
ABRIR = "não"

print("=== Gerando 20 resumos ===")
print(f"Matérias e primeiros tipos (exemplo.md):")
for mat, tp in mat_first_summary.items():
    print(f"  {mat}: `{tp}`")

# Define descriptions and fundamentals for each tipo
desc_map = {
    "interpretar-fonte": "Esta questão pede ao aluno que interprete uma fonte documental (texto, mapa, gráfico, charge, obra ou fotografia), extraindo informações relevantes, contexto histórico ou inferências solicitadas pelo enunciado. Exige leitura atenta e identificação de intenções, dados e limitações da fonte.",
    "processo-politico": "Esta questão solicita a identificação e a análise de um processo político ao longo do tempo, exigindo compreensão das etapas, atores envolvidos e transformações ocorridas. O foco está na dinâmica histórica dos eventos políticos e em sua evolução.",
    "comparar-processos": "Esta questão propõe a comparação entre dois ou mais processos históricos, exigindo a identificação de pontos em comum e de diferenças cruciais. O aluno deve analisar as semelhanças e as divergências entre os casos apresentados.",
    "transformacao-permanencia": "Esta questão aborda a relação entre transformação e permanência em determinado contexto histórico ou social, exigindo a identificação de o que muda e o que se mantém ao longo do tempo ou entre situações.",
    "agrario-trabalho": "Esta questão centra-se nas relações entre trabalho e terra no contexto rural, abrangendo reformas agrárias, modos de apropriação da terra, relações de trabalho no campo e a história do campo no Brasil.",
    "socioambiental": "Esta questão discute relações entre sociedade e ambiente, abordando temas como degradação ambiental, desastres, recursos naturais, mudanças climáticas e suas implicações sociais. Exige compreensão das interações entre agentes humanos e o meio físico.",
    "producao-espaco": "Esta questão foca na produção e no uso do espaço geográfico, envolvendo ocupação, transformação, infraestrutura, agronegócio, urbanização e as diversas formas de organização do território ao longo do tempo.",
    "redes-globalizacao": "Esta questão aborda as redes de fluxos globais (comerciais, financeiros, de informação, culturais), examinando a conectividade, interdependência e os impactos da globalização em diferentes escalas regionais e locais.",
    "populacao": "Esta questão trata da dinâmica populacional: migração, urbanização, fecundidade, envelhecimento, distribuição etária e as políticas públicas relacionadas ao crescimento e à composição da população.",
    "leitura-cartografica": "Esta questão exige a leitura e interpretação de mapas, cartogramas e representações cartográficas, testando a habilidade do aluno em extrair informações espaciais, escala, legenda, símbolos e relações geográficas a partir de representações visuais."
}

fund_map = {
    "interpretar-fonte": "Leitura de fontes: identificar autor, contexto, intenção, limitações. Extrair dados e inferências. Distinguir o que a fonte afirma do que o enunciado pergunta. Atribuir peso relativo às informações.",
    "processo-politico": "Etapas de um processo político: gatilho, atores, decisões, consequências. Identificar sequência cronológica e articular causa-efeito ao longo do tempo. Reconhecer transformações institucionais e culturais.",
    "comparar-processos": "Pontos de comparação: época, objetivo, atores, resultados, limitações. Estruturar a comparação em dimensões claras (o que mudou, o que se manteve). Avaliar semelhanças e divergências com fundamentação histórica.",
    "transformacao-permanencia": "Identificar o que se transforma e o que permanece em determinado contexto. Articular mudanças e continuidades entre períodos ou situações. Reconhecer estruturas subjacentes que se sustentam ou se modificam.",
    "agrario-trabalho": "Função social da propriedade, reformismo agrário, relações de trabalho no campo, apropriação da terra, movimentos sociais rurais, história do campo. Conceitos de latifúndio, minifúndio, trabalhador rural, sindicalismo agrícola.",
    "socioambiental": "Interação sociedade-meio: degradação, conservação, desastres, recursos. Avaliação de impactos ambientais e sociais. Políticas públicas de meio ambiente. Conflitos por recursos naturais. Sustentabilidade.",
    "producao-espaco": "Ocupação e transformação do espaço: infraestrutura, urbanização, agronegócio, uso do solo. Escala local/global. Políticas de desenvolvimento territorial. Conflitos de uso do solo. Representações espaciais.",
    "redes-globalizacao": "Fluxos globais: comércio, informação, cultura, pessoas. Redes de interdependência. Escala local/global. Impactos da globalização. Glocalização. Papel dos atores estatais e não-estatais.",
    "populacao": "Dinâmica demográfica: fecundidade, mortalidade, migração, urbanização. Transição demográfica. Políticas públicas de população. Estrutura etária. Envelhecimento. Distribuição espacial.",
    "leitura-cartografica": "Interpretação de mapas: legenda, escala, símbolos, orientação, proporção, área. Relações espaciais entre locais. Identificação de padrões geográficos. Distância, direção, posição relativa."
}

# Add missing tipos to steps_map
steps_map = {
    "interpretar-fonte": [
        ("1. Ler o comando final da questão e identificar o que se pede interpretar.",
         "Ler atentamente o enunciado e compreender exatamente qual aspecto da fonte deve ser interpretado (dado, contexto, intenção, limitação, inferência).",
         "O comando final define o foco da interpretação; sem ele, a leitura da fonte fica genérica."),
        ("2. Examinar a fonte (texto, mapa, gráfico, charge, obra, foto).",
         "Identificar autor, data, tipo de produção, contexto histórico imediato e finalidade da produção.",
         "O suporte (texto, mapa, gráfico etc.) determina que informações estão disponíveis e como devem ser lidas."),
        ("3. Extrair informações relevantes para o comando.",
         "Separar dados, nomes, datas, valores, relações de causa efeito ou quaisquer indicadores solicitados.",
         "Filtra-se o que é essencial para o que a questão pede, descartando ruídos e informações laterais."),
        ("4. Formular a resposta baseada apenas no que a fonte oferece.",
         "Construir a resposta usando unicamente as informações da fonte, sem trazer conhecimento externo não solicitado.",
         "A habilidade é ler o que está escrito (ou mostrado) e responder exatamente o pedido, sem extrapolar."),
        ("5. Verificar se a resposta atende ao que o enunciado solicita.",
         "Confirmar que todos os componentes do comando foram abordados e que a resposta é consistente com o texto/fonte.",
         "Evita-se responder o que não foi perguntado ou omitir o que foi solicitado.")
    ],
    "processo-politico": [
        ("1. Identificar o processo político em questão e seu contexto histórico.",
         "Reconhecer qual processo se trata (reforma, eleição, movimento, etc.) e em que período histórico ocorreu.",
         "O comando final costuma nomear o processo ou indicar o período; caso contrário, inferir a partir da fonte."),
        ("2. Listar as etapas ou fases do processo.",
         "Dividir o processo em momentos sequenciais: início, desenvolvimento, desfecho.",
         "Cada etapa representa uma fase de transformação ou decisão."),
        ("3. Identificar os atores envolvidos e suas ações.",
         "Quem participou? Quais foram as decisões tomadas por cada ator?",
         "Atores podem ser indivíduos, grupos, instituições políticas."),
        ("4. Analisar as consequências ou resultados do processo.",
         "Quais foram os efeitos imediatos e de longo prazo? Como o processo mudou a situação?",
         "Consequências podem ser políticas, sociais, econômicas ou culturais."),
        ("5. Articulação de causa e efeito ao longo do tempo.",
         "Relacionar as etapas às suas causas e consequências, mostrando a dinâmica do processo.",
         "Mostrar como uma etapa leva à seguinte, formando uma cadeia de transformações.")
    ],
    "comparar-processos": [
        ("1. Identificar os dois (ou mais) processos a serem comparados e seu contexto.",
         "Ler os enunciados ou fontes para saber exatamente quais processos estão em comparação e em que período/cenário.",
         "Compreender o objetivo da comparação (o que a questão quer que o aluno encontre)."),
        ("2. Estruturar dimensões de comparação (o que muda, o que se mantém).",
         "Definir eixos de comparação: época, objetivo, atores, resultados, limitações, consequências.",
         "Ter dimensões claras evita comparações superficiais ou impossíveis de articular."),
        ("3. Extrair características de cada processo Fonte/texto por fonte/texto.",
         "Para cada processo, extrair informações relevantes nas dimensões definidas.",
         "Registrar semelhanças e diferenças em cada eixo."),
        ("4. Apresentar as semelhanças e divergências identificadas.",
         "Exibir lado a lado o que os processos têm em comum e o que os diferencia.",
         "Usar dados concretos das fontes para sustentar cada ponto de comparação."),
        ("5. Tirar conclusões sobre a comparação.",
         "Baseado nas semelhanças e diferenças, responder ao que a questão pedir (ex.: 'quais as principais diferenças?').",
         "As conclusões devem seguir dos dadosExtraídos, não de opinião geral.")
    ],
    "transformacao-permanencia": [
        ("1. Identificar o que se transforma e o que permanece no contexto da questão.",
         "Analisar o que muda (transformação) e o que se mantém (permanência) ao longo do tempo ou entre situações.",
         "O comando final costuma conter pistas sobre o foco (ex.: 'as mudanças são...')."),
        ("2. Mapear as alterações observadas nos textos ou fontes.",
         "Listar os itens, práticas ou estruturas que foram alterados, com base no que foi apresentado.",
         "Registrar com precisão o que cada texto/fonte afirma ter mudado."),
        ("3. Identificar os elementos de continuidade ou permanência.",
         "Listar o que se manteve igual, se manteve estruturas, tradições, hábitos, leis ou características-chave.",
         "A permanência muitas vezes é tão relevante quanto a transformação para entender o contexto."),
        ("4. Articular a relação entre o que muda e o que se mantém.",
         "Explicar como as transformações ocorrem sobre uma base de permanência (ou como a permanência se sustenta apesar das mudanças).",
         "Essa articulação mostra a dinâmica histórica ou social em jogo."),
        ("5. Responder ao que o enunciado solicita sobre transformação e permanência.",
         "Formular a resposta conforme o comando final, usando elementos dos textos fontes.",
         "Cuidado de não confundir transformação com mudança aleatória; toda transformação tem padrões ou causas.")
    ],
    "agrario-trabalho": [
        ("1. Identificar o contexto rural e o tema central (reformas, propriedades, trabalho).",
         "Ler o comando e as fontes para saber qual aspecto do mundo rural está em foco (terra, trabalhador, reforma, etc.).",
         "Compreender o contexto rural é essencial para localizar a questão no espaço e no tempo do ENEM."),
        ("2. Reconhecer a relação entre terra e trabalho no caso apresentado.",
         "Identificar quem trabalha na terra, que tipo de propriedade existe, que relações de trabalho são descritas.",
         "Essa relação (terra/trabalho) é o eixo central do tipo agrario-trabalho no ENEM."),
        ("3. Extrair dados sobre a função social da propriedade ou sobre as condições de trabalho.",
         "Ler o que os textos dizem sobre a destinação da terra, direitos de acesso, jornadas, remuneração, organização do trabalho rural.",
         "A função social da propriedade e as condições de trabalho são conceitos-chaves cobrados pelo ENEM."),
        ("4. Articular reformas ou políticas públicas mencionadas ao impacto no campo.",
         "Se houver menção a reforma agrária, políticas públicas, entender como elas afetam a estrutura rural.",
         "Reformas agrárias e políticas públicas transformam (ou tentam transformar) a estrutura do campo."),
        ("5. Responder ao que o enunciado solicita sobre o tema agrario-trabalho.",
         "Formular resposta conforme o comando final, usando elementos dos textos.",
         "A resposta deve seguir o comando e usar apenas o que foi apresentado nas fontes.")
    ],
    "socioambiental": [
        ("1. Identificar a relação sociedade-meio em foco (degradação, desastre, recurso, mudança climática).",
         "Ler o comando para saber qual aspecto da relação sociedade-meio está em foco."),
        ("2. Extrair informações sobre os impactos ambientais e sociais apresentados.",
         "Separar dados sobre danos ambientais, affected populations, consequências sociais dos impactos."),
        ("3. Identificar atores e políticas públicas relacionados.",
         "Quais governos, organizações ou movimentos são mencionados? Que políticas são propostas ou criticadas?"),
        ("4. Avaliar as implicações das relações apresentadas.",
         "Que conexões são estabelecidas entre os fatores ambientais e os sociais? Que recomendações são sugeridas?"),
        ("5. Responder ao que o enunciado solicita sobre o tema socioambiental.",
         "Formular resposta conforme o comando final.")
    ],
    "producao-espaco": [
        ("1. Identificar o tipo de produção e uso do espaço em foco (urbanização, agronegócio, infraestrutura).",
         "Ler o comando para saber qual aspecto da produção do espaço está em foco."),
        ("2. Extrair dados sobre transformações espaciais e ocupacionais.",
         "Separar informações sobre como o espaço foi transformado, quem ocupa, quais atividades são desenvolvidas."),
        ("3. Identificar escala e agentes da produção do espaço.",
         "Quais escalas (local, regional, global)? Quais agentes (estados, empresas, movimentos sociais, indivíduos)?"),
        ("4. Articular políticas ou conflitos de uso do espaço mencionados.",
         "Se houver menção a políticas públicas, conflitos de uso, registrar o que os textos dizem."),
        ("5. Responder ao que o enunciado solicita sobre produção do espaço.",
         "Formular resposta conforme o comando final.")
    ],
    "redes-globalizacao": [
        ("1. Identificar o tipo de rede e fluxos em foco (comerciais, de informação, culturais, de pessoas).",
         "Ler o comando para saber qual rede e quais fluxos estão em análise."),
        ("2. Extrair dados sobre a conectividade e a interdependência apresentadas.",
         "Separar informações sobre fluxos, origens, destinos, gargalos, beneficiados/afetados."),
        ("3. Identificar escalas e atores das redes.",
         "Quais escalas (local, nacional, global)? Quais estados, empresas, organizações ou indivíduos são centrais?"),
        ("4. Avaliar impactos da globalização ou da rede em questão.",
         "Que mudanças as redes provocam? Quais benefícios e quais problemas são mencionados?"),
        ("5. Responder ao que o enunciado solicita sobre redes-globalizacao.",
         "Formular resposta conforme o comando final.")
    ],
    "populacao": [
        ("1. Identificar o fenômeno populacional em foco (migração, urbanização, fecundidade, envelhecimento).",
         "Ler o comando para saber qual aspecto da dinâmica populacional está em análise."),
        ("2. Extrair dados demográficos e tendências apresentados.",
         "Separar números, porcentagens, taxas, evoluções ao longo do tempo ou entre regiões."),
        ("3. Identificar políticas públicas ou consequências sociais mencionadas.",
         "Quais políticas são propostas, criticadas ou implementadas? Quais efeitos sociais são discutidos?"),
        ("4. Articular as conexões entre o fenômeno populacional e outros fatores (território, economia, política).",
         "Como o fenômeno se relaciona com território, economia, política? Quais as interdependências?"),
        ("5. Responder ao que o enunciado solicita sobre o tema população.",
         "Formular resposta conforme o comando final.")
    ],
    "leitura-cartografica": [
        ("1. Identificar o que o mapa representa (região, rota, distribuição, padrão).",
         "Ler a legenda, título e fonte do mapa para compreender o que está sendo mostrado."),
        ("2. Extrair informações espaciais solicitadas (distância, direção, escala, localização).",
         "Usar a escala do mapa para converter medidas; identificar orientação (N/S/L/O); localizar pontos de interesse."),
        ("3. Interpretar os símbolos, cores ou padrões do mapa.",
         "Decodificar o que cada símbolo, cor ou padrão representa segundo a legenda."),
        ("4. Relacionar o mapa com o contexto histórico, econômico ou social apresentado no enunciado.",
         "Conectar o que o mapa mostra com o que a questão pede, articulando informação espacial com o tema da questão."),
        ("5. Responder ao que o enunciado solicita sobre leitura cartográfica.",
         "Formular resposta conforme o comando final, usando dados extraídos do mapa.")
    ],
    # Missing tipos - add generic steps
    "interpretar-fragmento": [
        ("1. Identificar o fragmento textual e seu autor/obra.",
         "Ler o fragmento em destaque e compreender de qual autor, obra e contexto ele provém.",
         "O comando final costuma indicar que tipo de interpretação é esperada (sentido, ideia central, implicações)."),
        ("2. Extrair a ideia central ou argumento do fragmento.",
         "Determinar o ponto principal que o autor está defendendo ou ilustrando com o trecho.",
         "Focar no que o trecho diz explicitly e no sentido que ele carrega no contexto da obra."),
        ("3. Articular o fragmento com o tema da questão.",
         "Relacionar a ideia do fragmento com o que o enunciado pergunta, identificando pontos de contato ou contraste."),
        ("4. Aplicar os conceitos filosóficos solicitados pelo comando.",
         "Usar os conceitos centrais da filosofia (ética, epistemologia, metafísica, lógica, existência) para processar a ideia do fragmento.",
         "Essa etapa conecta o trecho ao tipo de questão, aplicando o tipo de raciocínio esperado."),
        ("5. Formular a resposta conforme o comando final.",
         "Construir a resposta usando unicamente o que foi pedido, com base na ideia central do fragmento e nos conceitos aplicados.",
         "A resposta deve ser direta, atender a todos os componentes do comando e evitar digressões.")
    ],
    "identidade-cultura": [
        ("1. Identificar o conceito de identidade ou cultura em foco no enunciado.",
         "Ler o comando para saber qual aspecto de identidade (individual, coletiva, de grupo) ou cultura (tradição, padrão, representação) está em análise."),
        ("2. Extrair dados sobre como identidade/cultura são apresentados nos textos/fonte.",
         "Separar trechos que definem, descrevem ou ilustram a identidade/cultura mencionada, com autor, contexto e exemplo."),
        ("3. Articular as características da identidade/cultura com o contexto histórico ou social da questão.",
         "Relacionar os elementos extraídos ao período, movimento, grupo social ou situação apresentada na questão do ENEM."),
        ("4. Identificar pertinências e exclusões ou representações envolvidas.",
         "Verificar quem está incluído ou excluído na representação da identidade/cultura, e como isso se conecta com questões de poder, memória ou reconhecimento."),
        ("5. Responder ao que o enunciado solicita sobre identidade-cultura.",
         "Formular resposta conforme o comando final, usando elementos dos textos fontes e artulações identificadas.")
    ]
}

# Generate summaries
for mat in MATERIAS:
    tipos_mat = top5[mat]
    for idx, itm in enumerate(tipos_mat):
        tipo = itm["tipo"]
        key = (mat, tipo)
        inst = mat_tipo_instances[key]
        is_exemplo = (tipo == mat_first_summary[mat])
        
        linhas = []
        add = linhas.append
        
        # 1. Título, classificação, tipo, matéria
        add(f"# {tipo.replace('-', ' ').title()}")
        add("")
        add("## Classificação")
        add(f"- **Matéria**: {mat.capitalize()}")
        add(f"- **Tipo**: {tipo}")
        add(f"- **Teórica ou Prática**: Teórica (questões discursivas do ENEM Humanas)")
        add(f"- **Período**: 2020–2025 (6 edições)")
        add("")
        
        # 2. Introdução
        add("## 1. Introdução")
        add("")
        desc = desc_map.get(tipo, "Esta questão solicita ao aluno a aplicação de conhecimentos do tipo especificado, exigindo compreensão dos conceitos centrais e sua aplicação ao caso apresentado no enunciado do ENEM.")
        add(desc)
        add("")
        
        # 3. Fundamentos (curto)
        add("## 2. Fundamentos (curto)")
        add("")
        fund = fund_map.get(tipo, "Conceitos centrais do tipo: identificação dos elementos-chave, compreensão das relações solicitadas pelo enunciado e aplicação dos conhecimentos históricos, geográficos, filosóficos ou sociológicos pertinentes.")
        add(fund)
        add("")
        
        # 4. Referência comparativa (N/A)
        add("## 3. Referência comparativa")
        add("")
        add("_Não aplicável: este tipo não envolve escolha entre casos ou operações matemáticas/fórmulas no sentido de requerer tabela comparativa._")
        add("")
        
        # 5. Passo a passo GENÉRICO
        add("## 4. Passo a passo genérico do tipo")
        add("")
        steps_list = steps_map.get(tipo, [
            ("1. Identificar o tipo de questão e o que o comando final pede.",
             "Ler atentamente o comando final da questão para compreender exatamente qual habilidade ou tipo de raciocínio é solicitado.",
             "O comando define o foco de toda a resolução; sem compreendê-lo, os passos seguintes perdem direção."),
            ("2. Examinar a fonte e/ou o enunciado da questão.",
             "Ler o texto, observar o mapa, gráfico, charge, obra ou fotografia apresentada.",
             "O suporte determina que informações estão disponíveis e como devem ser lidas (ex.: mapa tem legenda e escala; texto tem autor e contexto)."),
            ("3. Extrair informações relevantes para o comando.",
             "Separar dados, nomes, datas, valores, relações de causa efeito ou quaisquer indicadores solicitados pelo comando.",
             "Filtrar o essencial do ruído; o que não contribui para a resposta deve ser descartado."),
            ("4. Aplicar os conceitos e conhecimentos do tipo solicitado.",
             "Usar os conceitos centrais do tipo (interpretar, comparar, analisar transformação, etc.) para processar as informações extraídas.",
             "Essa etapa conecta o dado bruto ao tipo de questão, aplicando o tipo de raciocínio esperado."),
            ("5. Formular a resposta conforme o comando final.",
             "Construir a resposta usando unicamente o que foi pedido, com base nas informações extraídas e aplicadas.",
             "A resposta deve ser direta, atender a todos os componentes do comando e evitar informações extras não solicitadas.")
        ])
        import re
for step in steps_list:
            # step may have 2 or 3 elements; pad if needed
            if len(step) == 2:
                numero, oque_fazer = step
                por_que = ""
            elif len(step) >= 3:
                numero, oque_fazer, por_que = step[:3]
            else:
                numero, oque_fazer, por_que = "?", "Passo sem descrição", ""
            # Extract just the number prefix if present
            num_match = re.match(r"(\d+)", numero)
            label = num_match.group(1) if num_match else str(numero)
            add(f"**{label}.** {oque_fazer}")
            if por_que:
                add(f"*Por que funciona:* {por_que}")
            add("")
        
        # 6. Exemplo diferente
        add("## 5. Exemplo diferente (aplicando o passo a passo)")
        add("")
        if inst:
            r0 = inst[0]
            add(f"- **Questão representativa**: {r0['ano']} Q{r0['q']} ({mat.capitalize()}) — {tipo} — suporte: {r0.get('suporte', 'texto')}")
            add(f"  Gabarito: {r0.get('gabarito', '-')}")
            add("")
            enun = r0.get("enunciado", "")
            alt = r0.get("alternativas", None)
            if enun:
                add("**Enunciado (resumo):**")
                add(enun[:500].replace("\n", " "))
                add("")
            if alt:
                add("**Alternativas:**")
                for l in "ABCDE":
                    if l in alt:
                        add(f"- **{l}**: {alt[l][:200]}")
                add("")
        else:
            add("_Nenhuma questão representativa disponível._")
        add("")
        
        # 7. Todas as instâncias
        add("## 6. Todas as instâncias do tipo no ENEM 2020–2025")
        add("")
        add(f"_Total de questões: {len(inst)}_")
        add("")
        add("| Ano | Questão | Tema | Suporte | Gabarito |")
        add("|---|---|---|---|---|")
        for r in inst:
            ano = r["ano"]
            q = r["q"]
            tema = "; ".join(r.get("tema", [])) if r.get("tema") else "-"
            sup = r.get("suporte", "texto")
            gab = r.get("gabarito", "-")
            add(f"| {ano} | Q{q} | {tema} | {sup} | {gab} |")
        add("")
        
        # 8. Checklist
        add("## 7. Checklist de conferência")
        add("")
        add("- [ ] O resumo é do tipo, não da questão isolada.")
        add("- [ ] Todos os passos do passo a passo têm os três campos (oque fazer, como fazer, por que funciona).")
        add("- [ ] O exemplo é diferente da questão representativa.")
        add("- [ ] Todas as instâncias do tipo (2020–2025) estão listadas na seção 6.")
        add("- [ ] O embasamento está em versão curta (essencial, sem divagações).")
        add("- [ ] Não foram incluídas variações (resposta padrão: não).")
        add("- [ ] Não foram listadas fontes (resposta padrão: não).")
        add("- [ ] A questão representativa foi resolvida passo a passo.")
        add("- [ ] O arquivo segue o estilo dos markdowns salvos (estilo.md).")
        add("")
        
        add("---")
        add("")
        add(f"_Arquivo salvo como: `Markdowns/{mat}/{tipo}.md`_")
        add(f"_Este é o {'1º resumo de {mat} → vira exemplo.md' if is_exemplo else 'resumo subsequente de {mat}'}_")
        add(f"_Respostas padrão aplicadas: embasamento={EMBASAMENTO}; variações={VARIACOES}; fontes={FONTES}; resolver={RESOLVER}; salvar={SALVAR}; abrir={ABRIR}_")
        
        # Write file
        out_path = summary_dir / mat / f"{tipo}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(linhas), encoding="utf-8")
        print(f"Gerado: {out_path} (exemplo={is_exemplo})")

print("\n=== FIM ===")