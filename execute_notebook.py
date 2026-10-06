import nbformat
from nbclient import NotebookClient

with open('notebooks/SAIFA_Quant_Edge_1_0_Research.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

client = NotebookClient(nb, timeout=600, kernel_name='python3')
client.execute()

with open('notebooks/SAIFA_Quant_Edge_1_0_Research.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Notebook executed successfully.")
