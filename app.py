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

def salvar_alunos():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(alunos, f, ensure_ascii=False, indent=2)

def entrar_na_reuniao():
    selecionado = lista.curselection()
    if not selecionado:
        return
    indice = selecionado[0]
    webbrowser.open(alunos[indice]["link"])

def abrir_janela_cadastro():
    cadastro = tk.Toplevel(janela)
    cadastro.title("Adicionar aluno")
    cadastro.geometry("350x250")

    tk.Label(cadastro, text="Nome do aluno").pack(pady=5)
    campo_nome = tk.Entry(cadastro, width=40)
    campo_nome.pack(pady=5)

    tk.Label(cadastro, text="Link da reunião").pack(pady=5)
    campo_link = tk.Entry(cadastro, width=40)
    campo_link.pack(pady=5)

    def salvar():
        nome = campo_nome.get().strip()
        link = campo_link.get().strip()
        if not nome or not link:
            return

        aluno = {"nome": nome, "link": link}
        alunos.append(aluno)
        salvar_alunos()

        lista.insert(tk.END, nome)
        cadastro.destroy()

    tk.Button(cadastro, text="Salvar", command=salvar).pack(pady=20)

# Carregar alunos
alunos = carregar_alunos()

# Janela principal
janela = tk.Tk()
janela.title("Acesso rápido aos Meets")
janela.geometry("500x400")

# Título
tk.Label(
    janela,
    text="Lista de Alunos",
    font=("Arial", 16, "bold")
).pack(pady=10)

# Listbox
lista = tk.Listbox(janela, width=40, height=10)
lista.pack(pady=10)

for aluno in alunos:
    lista.insert(tk.END, aluno["nome"])

# Botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Entrar na reunião", command=entrar_na_reuniao).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botoes, text="Adicionar aluno", command=abrir_janela_cadastro).pack(side=tk.LEFT, padx=5)

# Loop
janela.mainloop()
