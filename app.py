import tkinter as tk
import webbrowser

def entrar_na_reuniao():
    link = campo_link.get()
    if link.strip():
        webbrowser.open(link)

# Janela principal
janela = tk.Tk()
janela.title("Acesso rápido aos Meets")
janela.geometry("500x400")

# Título
titulo = tk.Label(
    janela,
    text="Meet dos Alunos",
    font=("Arial", 16, "bold")
)
titulo.pack(pady=20)

# Campo de texto
campo_link = tk.Entry(janela, width=50)
campo_link.pack(pady=10)

# Botão
botao = tk.Button(
    janela,
    text="Entrar na reunião",
    command=entrar_na_reuniao
)
botao.pack(pady=20)

# Loop da janela
janela.mainloop()
