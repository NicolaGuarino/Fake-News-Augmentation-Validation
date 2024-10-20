import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Definisci il percorso base (la directory iniziale contenente le cartelle Q4TEMP, Q5TEMP, ecc.)
base_dir = 'D:/Universita/Magistrale/Tesi/Progetto/2. Confronto con LLM'
results_dir = os.path.join(base_dir, 'results')

# Crea la cartella results se non esiste
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Crea un DataFrame per riepilogare le terne forti e deboli
summary_data = []

# Trova tutte le cartelle "QxTEMP..." e all'interno le sottocartelle e i file Excel
for temp_folder in os.listdir(base_dir):
    if os.path.isdir(os.path.join(base_dir, temp_folder)):
        for sub_folder in ['Coronavirus and vaccines in America', 'Vaccines and illnesses fake news1', 'Viral Fake Election News1']:
            full_sub_folder_path = os.path.join(base_dir, temp_folder, sub_folder)
            for file_name in ['SimilarityResults1.xlsx', 'SimilarityResults2.xlsx', 'SimilarityResults3.xlsx']:
                file_path = os.path.join(full_sub_folder_path, file_name)
                
                if os.path.exists(file_path):
                    print(f"Processing file: {temp_folder}_{sub_folder}_{file_name}")
                    
                    # Qui inizia il tuo codice, lasciato intatto
                    data = pd.read_excel(file_path)

                    # Funzione per estrarre il sottografo di appartenenza dall'articolo
                    def get_subgraph_type(article):
                        if "generated" in article.lower():
                            return "generated"
                        elif "train" in article.lower():
                            return "train set"
                        elif "test" in article.lower():
                            return "test set"
                        return None

                    # Creiamo un grafo vuoto
                    G = nx.Graph()

                    # Aggiunta dei nodi e degli archi
                    for _, row in data.iterrows():
                        comparison = row['Comparison']
                        article1 = row['Article 1'].split('\n')[0]
                        article2 = row['Article 2'].split('\n')[0]
                        similarity = row['Similarity']

                        # Determina i sottografi in base al tipo di confronto
                        subgraph1 = get_subgraph_type(comparison.split(' - ')[0])
                        subgraph2 = get_subgraph_type(comparison.split(' - ')[1])

                        # Aggiungi i nodi al grafo
                        G.add_node(article1, subgraph=subgraph1)
                        G.add_node(article2, subgraph=subgraph2)

                        # Aggiungi un arco colorato se la similarità è MID o HIGH
                        if similarity == 'MID':
                            G.add_edge(article1, article2, color='orange', weight=1, similarity='MID')
                        elif similarity == 'HIGH':
                            G.add_edge(article1, article2, color='green', weight=2, similarity='HIGH')

                    # Funzione per trovare le terne X-Y-Z
                    def find_ternary_relationships(G, generated, train_set, test_set):
                        ternary_relationships = []
                        for x in generated:
                            # Trova i nodi Y a cui X è collegato
                            y_nodes = G.neighbors(x)
                            for y in y_nodes:
                                if y in train_set:
                                    # Trova i nodi Z a cui Y è collegato
                                    z_nodes = G.neighbors(y)
                                    for z in z_nodes:
                                        if z in test_set and z in G.neighbors(x):
                                            ternary_relationships.append((x, y, z))
                        return ternary_relationships

                    # Definiamo i colori degli archi e gli spessori
                    edges = G.edges()
                    colors = [G[u][v]['color'] for u, v in edges]
                    weights = [G[u][v]['weight'] for u, v in edges]

                    # Layout personalizzato per il grafo
                    pos = {}
                    generated_nodes = [n for n, d in G.nodes(data=True) if d['subgraph'] == 'generated']
                    train_nodes = [n for n, d in G.nodes(data=True) if d['subgraph'] == 'train set']
                    test_nodes = [n for n, d in G.nodes(data=True) if d['subgraph'] == 'test set']

                    # Definiamo la posizione dei nodi in righe ordinate
                    y_generated = np.linspace(1, 0, num=len(generated_nodes))
                    y_train = np.linspace(1, 0, num=len(train_nodes))
                    y_test = np.linspace(1, 0, num=len(test_nodes))

                    # Assegna le posizioni dei nodi
                    for i, node in enumerate(generated_nodes):
                        pos[node] = (-0.5, y_generated[i])
                    for i, node in enumerate(train_nodes):
                        pos[node] = (0.0, y_train[i])
                    for i, node in enumerate(test_nodes):
                        pos[node] = (0.5, y_test[i])

                    # Trova e stampa le terne che rispettano la proprietà
                    ternary_relationships = find_ternary_relationships(G, generated_nodes, train_nodes, test_nodes)

                    data = []
                    strong_count = 0
                    weak_count = 0
                    for triplet in ternary_relationships:
                        x, y, z = triplet
                        mid_xy = G[x][y]['similarity']
                        mid_yz = G[y][z]['similarity']
                        mid_xz = G[x][z]['similarity']
                        data.append((x, mid_xy, y, mid_yz, z, mid_xz))
                        #print((x, mid_xy, y, mid_yz, z, mid_xz))

                        # Conta le terne forti e deboli
                        similarities = [mid_xy, mid_yz, mid_xz]
                        mid_count = similarities.count('MID')

                        if mid_count < 2:
                            strong_count += 1  # 0 o 1 MID nella terna
                        else:
                            weak_count += 1  # 2 o più MID nella terna

                    # Crea un DataFrame con i risultati delle terne
                    df = pd.DataFrame(data, columns=['Generated', 'Link Generated - Train', 'Train', 'Link Train - Test', 'Test', 'Link Generated - Test'])

                    # Aggiungi le nuove colonne per Strong e Weak e inserisci i conteggi
                    df['Strong Ternaries'] = ''
                    df['Weak Ternaries'] = ''

                    # Aggiungi la riga con i conteggi di Strong e Weak
                    summary_row = pd.DataFrame({
                        'Generated': [''],
                        'Link Generated - Train': [''],
                        'Train': [''],
                        'Link Train - Test': [''],
                        'Test': [''],
                        'Link Generated - Test': [''],
                        'Strong Ternaries': [strong_count],
                        'Weak Ternaries': [weak_count]
                    })

                    # Usa pd.concat per aggiungere la riga riepilogativa al DataFrame
                    df = pd.concat([summary_row, df], ignore_index=True)

                    # Salva il DataFrame nella cartella 'results'
                    result_file_path = os.path.join(results_dir, f'result_{temp_folder}_{sub_folder}_{file_name}')
                    df.to_excel(result_file_path, index=False)
                    
                    # Aggiungi i dati per il riepilogo
                    summary_data.append({
                        'Model': f'{temp_folder}',
                        'Campaign': f'{sub_folder}',
                        'Trial N.': f'{file_name}',
                        'Strong Ternaries': strong_count,
                        'Weak Ternaries': weak_count
                    })

                    # Stampa il conteggio delle terne forti e deboli
                    print(f'Numero di terne forti: {strong_count}')
                    print(f'Numero di terne deboli: {weak_count}')

                    # Colori distinti per ogni gruppo
                    node_colors = []
                    for node in G.nodes(data=True):
                        if node[1]['subgraph'] == 'generated':
                            node_colors.append('lightcoral')
                        elif node[1]['subgraph'] == 'train set':
                            node_colors.append('lightgreen')
                        elif node[1]['subgraph'] == 'test set':
                            node_colors.append('lightblue')

                    # Disegniamo il grafo
                    plt.figure(figsize=(16, 12))
                    nx.draw(G, pos, with_labels=True, edge_color=colors, width=weights, node_color=node_colors, node_size=500, font_size=8, font_weight='bold')

                    # Aggiungere linee tratteggiate per separare le sezioni
                    plt.axvline(x=-0.2, color='black', linestyle='--', linewidth=2)
                    plt.axvline(x=0.2, color='black', linestyle='--', linewidth=2)

                    # Aggiungere i nomi delle sottosezioni
                    plt.text(-0.5, 1.05, 'Generated', fontsize=14, fontweight='bold', ha='center', color='darkred')
                    plt.text(0.0, 1.05, 'Train Set', fontsize=14, fontweight='bold', ha='center', color='darkgreen')
                    plt.text(0.5, 1.05, 'Test Set', fontsize=14, fontweight='bold', ha='center', color='darkblue')

                    plt.title("Graph with Train Set, Test Set, and Generated Articles")
                    plt.show()

# Crea un DataFrame per il riepilogo finale
summary_df = pd.DataFrame(summary_data)

# Salva il riepilogo in un file Excel separato
summary_file_path = os.path.join(results_dir, 'ternary_summary.xlsx')
summary_df.to_excel(summary_file_path, index=False)

print(f"Riepilogo delle terne forti e deboli salvato in: {summary_file_path}")