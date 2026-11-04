# mapeamento_cursinho_pt2.py - Filosofia e Sociologia
MAPA_CURSINHO_PT2 = {
    "filosofia": {
        "Capítulo 01 - Renascença": [
            "renascença", "humanismo", "leonardo da vinci", "michelangelo",
            "arte renascentista", "perspectiva", "imprensa de gutenberg",
        ],
        "Capítulo 02 - Revolução científica": [
            "revolução científica", "copérnico", "galileu", "newton",
            "kepler", "método científico", "heliocentrismo", "geocentrismo",
        ],
        "Capítulo 03 - Racionalismo": [
            "racionalismo", "descartes", "spinoza", "leibniz", "razão",
            "ideias inatas", "dedução", "cogito ergo sum",
        ],
        "Capítulo 04 - Empirismo": [
            "empirismo", "locke", "berkeley", "hum", "experiência",
            "tábula rasa", "indução", "impressões e ideias",
        ],
        "Capítulo 05 - Kant: teoria do conhecimento": [
            "kant", "teoria do conhecimento", "crítica da razão pura",
            "sintéticos a priori", "categorias do entendimento",
            "fenômeno e númeno",
        ],
        "Capítulo 06 - Ética kantiana e utilitarista": [
            "ética kantiana", "imperativo categórico", "dever",
            "utilitarismo", "bentham", "mill", "maior felicidade para o maior número",
        ],
        "Capítulo 07 - Teorias políticas da modernidade": [
            "teorias políticas modernidade", "maquiavel", "hobbes", "locke",
            "rousseau", "contrato social", "soberania", "estado moderno",
            "separação dos poderes",
        ],
    },
    "sociologia": {
        "Capítulo 01 - Antropologia cultural": [
            "antropologia cultural", "cultura", "etnocentrismo", "relativismo cultural",
            "rituais", "mitos", "símbolos", "parentesco", "tribo",
        ],
        "Capítulo 02 - Esferas da cultura de massas": [
            "cultura de massa", "indústria cultural", "meios de comunicação",
            "televisão", "rádio", "cinema", "cultura popular",
        ],
        "Capítulo 03 - Meios de comunicação e Sociedade": [
            "meios de comunicação", "sociedade", "opinião pública",
            "agenda setting", "framing", "redes sociais", "internet",
        ],
        "Capítulo 04 - Sociologia brasileira": [
            "sociologia brasileira", "brasil", "raízes do brasil",
            "sérgio buarque de holanda", "gilberto freyre", "darcy ribeiro",
            "casa grande e senzala", "formação do brasil",
        ],
        "Capítulo 05 - Estado e Governo": [
            "estado", "governo", "soberania", "nação", "cidadania",
            "poder político", "legitimidade", "autoridade",
        ],
        "Capítulo 06 - Democracia e Participação": [
            "democracia", "participação", "voto", "eleições",
            "partidos políticos", "movimentos sociais", "cidadania ativa",
        ],
        "Capítulo 07 - Cidadania e Direitos": [
            "cidadania", "direitos", "direitos humanos", "direitos sociais",
            "declaração universal dos direitos humanos", "igualdade",
            "liberdade", "justiça",
        ],
    },
}

print("Mapeamento pt2 carregado:")
for mat, caps in MAPA_CURSINHO_PT2.items():
    print(f"  {mat}: {len(caps)} capítulos")
