import pandas as pd

# File Excel da leggere
files = {
    'BERT_Score': '3. Metriche\\BERT_Score.xlsx',
    'Doc2Vec_Similarity_Scores': '3. Metriche\\Doc2Vec_Similarity_Scores.xlsx',
    'SBERT_Similarity_Scores': '3. Metriche\\SBERT_Similarity_Scores.xlsx',
    'USE_Similarity_Scores': '3. Metriche\\USE_Similarity_Scores.xlsx'
}

# Lista dei dataframe caricati
dataframes = {}

# Carica ciascun file Excel in un dataframe e assegna il nome della metrica alla colonna similarity_score
for metric, file in files.items():
    df = pd.read_excel(file)
    if metric == 'Doc2Vec_Similarity_Scores':
        # Includi la colonna 'Ref Nature' dal file Doc2Vec_Similarity_Scores.xlsx
        df = df[['prediction', 'reference', 'Ref Nature', 'similarity_score']]
    else:
        df = df[['prediction', 'reference', 'similarity_score']]
    df.rename(columns={'similarity_score': f'{metric}_score'}, inplace=True)
    dataframes[metric] = df

# Unione dei dataframe in base a prediction e reference
merged_df = dataframes['BERT_Score']
for metric, df in dataframes.items():
    if metric != 'BERT_Score':
        merged_df = pd.merge(merged_df, df, on=['prediction', 'reference'], how='outer')

# Mantieni solo una colonna per 'Ref Nature' (se esiste)
if 'Ref Nature' in merged_df.columns:
    merged_df['Ref Nature'] = merged_df['Ref Nature'].fillna(method='ffill')

# Salva il risultato finale in un nuovo file Excel
merged_df.to_excel('3. Metriche\\Merged_Similarity_Scores.xlsx', index=False)

print("File combinato salvato come 'Merged_Similarity_Scores.xlsx'.")
