import pandas as pd
import requests
from bs4 import BeautifulSoup

def extract_post_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Cerca il div con il testo del post usando il selettore specifico
            post_div = soup.find('div', {'dir': 'auto', 'style': 'text-align: start;'})
            if post_div:
                post_text = post_div.get_text(separator=' ', strip=True)
                return post_text
            else:
                # Prova a cercare in altri punti del DOM
                post_text = soup.get_text(separator=' ', strip=True)
                if len(post_text) > 0:
                    return post_text
                else:
                    return "Post text not found"
        else:
            return "Failed to retrieve content"
    except Exception as e:
        return str(e)

# Carica il file CSV
file_path = 'facebook-fact-check.csv'  # Percorso originale mantenuto
df = pd.read_csv(file_path)

# Filtra solo le notizie false basandosi sulla colonna 'Rating'
df_false_news = df[df['Rating'].isin(['mostly false', 'mixture of true and false'])].copy()

# Estrai il testo del post dagli URL
df_false_news.loc[:, 'testo'] = df_false_news['Post URL'].apply(extract_post_text)

# Crea un nuovo DataFrame con le colonne richieste
extracted_data = pd.DataFrame({
    'url': df_false_news['Post URL'],
    'titolo': df_false_news['post_id'],
    'testo': df_false_news['testo'],
    'campagna': 'Hyperpartisan Facebook pages in 2016 American Politic Elections',
    'threat actor': df_false_news['account_id']
})

# Salva i dati estratti in un nuovo file CSV
output_path = 'facebook_extract.csv'  # Percorso originale mantenuto
extracted_data.to_csv(output_path, index=False)

print(f"I dati estratti sono stati salvati in {output_path}")
