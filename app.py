import tkinter as tk
import webbrowser

# Lista de alunos com links
alunos = [
    {
        "nome": "Ana",
        "link": "https://meet.google.com/ana-link"
    },
    {
        "nome": "Bruno",
        "link": "https://meet.google.com/bruno-link"
    },
    {
        "nome": "Carlos",
        "link": "https://meet.google.com/carlos-link"
    }
]

def entrar_na_reuniao():
    selecionado = lista.curselection()
    if not selecionado:
        return

    indice = selecionado[0]
    link = alunos[indice]["link"]
    webbrowser.open(link)

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

# Inserir alunos
for aluno in alunos:
    lista.insert(tk.END, aluno["nome"])

# Botão para entrar no Meet
botao = tk.Button(
    janela,
    text="Entrar na reunião",
    command=entrar_na_reuniao
)
botao.pack(pady=10)

# Loop
janela.mainloop()
