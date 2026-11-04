# Frequencia de temas - ENEM
O projeto foi criado para ajudar meu irmão na reta final de estudos para o ENEM (Exame Nacional do Ensino Médio). A ideia é conseguir elencar os cinco temas de cada matéria que caíram com maior frequência nos últimos 6 anos e permitir concentrar as últimas horas de estudo nos conteúdos com maior probabilidade de aparecer.
Indo um pouco além dessa ideia inicial, o projeto ainda fez o link entre o material do cursinho, os temas que mais caem e as questões do ENEM relacionadas para que o tempo seja gasto estudando, e não organizando o estudo.

Confira o resultado [aqui](Resultados/Humanas/Guia-de-Estudo.md).

## Tech
___
- Python 3.13
- JSONL (banco)
- JSON (saídas detalhadas)
- TXT (métricas)
- Heurística de substring em listas de palavras-chave para a classificação de questões
- PyMuPDF / pypdf / Word COM / OCR

## Funcionalidades
___
- Extração de texto de questões via Python para economizar tokens
- Dados armazenados de forma simples em JSONL
- Separação de questões por Macro-Temas e Sub-Temas por IA
- Cruzamento de dados entre divisão de questões do ENEM por tema e capítulos do cursinho

## Próximos passos
___
A principal melhoria no projeto seria uma definição padronizada de temas. No projeto atual a IA definiu sub-temas para cada questão e como resultado houveram 684 etiquetas de sub-tema distintas para 270 questões (201 em História, 215 em Geografia, 145 em Sociologia, 123 em Filosofia). Temas como 'terra', 'cultura', 'arte', 'império', 'sociedade', 'costumes' acabam convivendo com 'lei aberdeen', 'Balfour' e 'Chiquinha Gonzaga'.

Depois, quando houve mapeamento de sub-temas em capítulos do cursinho por substring, ocorreram falsos positivos como ("cemitério" → Segundo Reinado).
