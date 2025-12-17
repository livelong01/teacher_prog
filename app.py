import tkinter as tk
import webbrowser
import json
import os
from PIL import Image, ImageTk

ARQUIVO = "alunos.json"

def carregar_alunos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_alunos():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(alunos, f, ensure_ascii=False, indent=2)

def abrir_reuniao(link):
    webbrowser.open(link)

def criar_card_aluno(pai, aluno):
    frame = tk.Frame(pai, bd=1, relief="solid", padx=5, pady=5)
    frame.pack(fill="x", pady=5, padx=10)

    caminho_foto = aluno.get("foto", "fotos/padrao.png")
    img = Image.open(caminho_foto).resize((50, 50))
    foto = ImageTk.PhotoImage(img)

    btn = tk.Button(
        frame,
        image=foto,
        text=aluno["nome"],
        compound="left",
        command=lambda: abrir_reuniao(aluno["link"]),
        anchor="w",
        padx=10
    )
    btn.image = foto
    btn.pack(fill="x")

def abrir_janela_cadastro():
    cadastro = tk.Toplevel(janela)
    cadastro.title("Adicionar aluno")
    cadastro.geometry("350x300")

    tk.Label(cadastro, text="Nome").pack(pady=5)
    campo_nome = tk.Entry(cadastro, width=40)
    campo_nome.pack(pady=5)

    tk.Label(cadastro, text="Link").pack(pady=5)
    campo_link = tk.Entry(cadastro, width=40)
    campo_link.pack(pady=5)

    def salvar():
        aluno = {
            "nome": campo_nome.get().strip(),
            "link": campo_link.get().strip(),
            "foto": "fotos/padrao.png"
        }
        if not aluno["nome"] or not aluno["link"]:
            return

        alunos.append(aluno)
        salvar_alunos()
        criar_card_aluno(container, aluno)
        cadastro.destroy()

    tk.Button(cadastro, text="Salvar", command=salvar).pack(pady=20)

# Carregar alunos
alunos = carregar_alunos()

# Janela principal
janela = tk.Tk()
janela.title("Acesso rápido aos Meets")
janela.geometry("500x500")

tk.Label(
    janela,
    text="Alunos",
    font=("Arial", 16, "bold")
).pack(pady=10)

container = tk.Frame(janela)
container.pack(fill="both", expand=True)

for aluno in alunos:
    criar_card_aluno(container, aluno)

tk.Button(
    janela,
    text="Adicionar aluno",
    command=abrir_janela_cadastro
).pack(pady=10)

janela.mainloop()
