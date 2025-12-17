import tkinter as tk
import webbrowser


def abrir_meet():
    link = entry_link.get()
    if link:
        webbrowser.open(link)


janela = tk.Tk()
janela.title("Meet dos Alunos")
janela.geometry("400x200")

tk.Label(janela, text="Link da reunião:").pack(pady=5)

entry_link = tk.Entry(janela, width=50)
entry_link.pack(pady=5)

btn = tk.Button(janela, text="Entrar na reunião", command=abrir_meet)
btn.pack(pady=20)

janela.mainloop()