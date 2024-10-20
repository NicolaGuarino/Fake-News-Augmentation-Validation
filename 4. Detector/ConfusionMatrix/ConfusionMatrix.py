import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Definisci la matrice di confusione con i numeri forniti
cm = np.array([[5, 0], [7, 16]])

# Crea il plot della matrice di confusione
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['FAKE', 'REAL'], yticklabels=['FAKE', 'REAL'])
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.title('Confusion Matrix')
plt.show()
