import tkinter as tk
import webbrowser
import json
import os

ARQUIVO = "alunos.json"

def carregar_alunos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def entrar_na_reuniao():
    selecionado = lista.curselection()
    if not selecionado:
        return

    indice = selecionado[0]
    link = alunos[indice]["link"]
    webbrowser.open(link)

# Carregar alunos
alunos = carregar_alunos()

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
    lista.insert(tk.END, aluno["nome"])

# Botão
botao = tk.Button(
    janela,
    text="Entrar na reunião",
    command=entrar_na_reuniao
)
botao.pack(pady=10)

# Loop
janela.mainloop()
