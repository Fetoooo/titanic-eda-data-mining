import nbformat
from nbclient import NotebookClient

print("Reading Assignment1_Data_Mining.ipynb...")
with open('Assignment1_Data_Mining.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

client = NotebookClient(nb, timeout=600, kernel_name='python3')
print("Executing notebook cells...")
client.execute()

print("Saving executed notebook...")
with open('Assignment1_Data_Mining.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Notebook successfully executed and saved with all outputs and figures!")
