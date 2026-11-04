import json
from pathlib import Path

BASE = Path(r'C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA')
DADOS = BASE / 'dados'
summary_dir = BASE / 'Markdowns'

matters = ['historia', 'geografia', 'filosofia', 'sociologia']
tipos_lists = {
    'historia': ['interpretar-fonte', 'processo-politico', 'comparar-processos', 'transformacao-permanencia', 'agrario-trabalho'],
    'geografia': ['socioambiental', 'producao-espaco', 'redes-globalizacao', 'populacao', 'leitura-cartografica'],
    'filosofia': ['interpretar-fragmento', 'aplicar-conceito', 'comparar-autores', 'questao-eticamente-julgada', 'ciencia-filosofia'],
    'sociologia': ['identidade-cultura', 'desigualdade', 'cotidiano', 'mundo-trabalho', 'movimentos-sociais'],
}

check_defs = {
    'historia': {
        'Titulo': '# interpretar-fonte',
        'Classificacao': 'Classificacao',
        'Intro': '1. Introducao',
        'Fundamentos': '2. Fundamentos',
        'Referencia': '3. Referencia comparativa',
        'Passo a passo': '4. Passo a passo',
        'Exemplo': '5. Exemplo diferente',
        'Instancias': '6. Todas as instancias',
        'Checklist': '7. Checklist',
    },
    'geografia': {
        'Titulo': '# socioambiental',
        'Classificacao': 'Classificacao',
        'Intro': '1. Introducao',
        'Fundamentos': '2. Fundamentos',
        'Referencia': '3. Referencia comparativa',
        'Passo a passo': '4. Passo a passo',
        'Exemplo': '5. Exemplo diferente',
        'Instancias': '6. Todas as instancias',
        'Checklist': '7. Checklist',
    },
    'filosofia': {
        'Titulo': '# interpretar-fragmento',
        'Classificacao': 'Classificacao',
        'Intro': '1. Introducao',
        'Fundamentos': '2. Fundamentos',
        'Referencia': '3. Referencia comparativa',
        'Passo a passo': '4. Passo a passo',
        'Exemplo': '5. Exemplo diferente',
        'Instancias': '6. Todas as instancias',
        'Checklist': '7. Checklist',
    },
    'sociologia': {
        'Titulo': '# identidade-cultura',
        'Classificacao': 'Classificacao',
        'Intro': '1. Introducao',
        'Fundamentos': '2. Fundamentos',
        'Referencia': '3. Referencia comparativa',
        'Passo a passo': '4. Passo a passo',
        'Exemplo': '5. Exemplo diferente',
        'Instancias': '6. Todas as instancias',
        'Checklist': '7. Checklist',
    },
}

count = 0
for mat in matters:
    tipos = tipos_lists[mat]
    check_def = check_defs[mat]
    for tipo in tipos:
        filepath = summary_dir / mat / f'{tipo}.md'
        if filepath.exists():
            count += 1
            with open(filepath, encoding='utf-8') as f:
                content = f.read()
            missing = [label for label, search in check_def.items() if search not in content]
            if missing:
                print(f'MISSING in {mat}/{tipo}: {missing}')

print(f'Validated {count}/20 summary files')