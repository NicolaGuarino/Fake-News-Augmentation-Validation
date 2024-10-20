import pandas as pd

# Load the Excel file
file_path = 'Ten sample influential Russian trolls.xlsx'
df = pd.read_excel(file_path, sheet_name='tweets_top10', skiprows=3)

# Convert the tweet_id to integer and then to string to avoid scientific notation
df['tweet_id'] = df['tweet_id'].apply(lambda x: '{:.0f}'.format(x))

# Create the final DataFrame with the specified columns
final_df = pd.DataFrame()

# Construct the 'url' column
final_df['url'] = 'https://twitter.com/' + df['user_key'] + '/status/' + df['tweet_id']

# Set the 'titolo' column to the 'tweet_id'
final_df['titolo'] = df['tweet_id']

# Set the 'testo' column to the 'text'
final_df['testo'] = df['text']

# Set the 'campagna' column to the specified text
final_df['campagna'] = 'Russian troll accounts during 2016 U.S. presidential election'

# Set the 'threat actor' column to the 'user_key'
final_df['threat actor'] = df['user_key']

# Save the final DataFrame to a new Excel file
final_df.to_excel('RussianTroll_extract.xlsx', index=False)

print("The data has been successfully transformed and saved to 'RussianTroll_extract.xlsx'")
