import tkinter as tk

# Lista de alunos (por enquanto fixa)
alunos = [
    "Ana",
    "Bruno",
    "Carlos",
    "Daniela"
]

# Janela principal
janela = tk.Tk()
janela.title("Acesso rápido aos Meets")
janela.geometry("500x400")

# Título
titulo = tk.Label(
    janela,
    text="Lista de Alunos",
    font=("Arial", 16, "bold")
)
titulo.pack(pady=10)

# Listbox
lista = tk.Listbox(janela, width=40, height=10)
lista.pack(pady=20)

# Inserir alunos na lista
for aluno in alunos:
    lista.insert(tk.END, aluno)

# Loop da janela
janela.mainloop()
