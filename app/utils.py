import webbrowser
from tkinter import messagebox

def abrir_reuniao(link):
    if link.startswith("http"):
        webbrowser.open(link)
    else:
        messagebox.showerror("Erro", "Link inválido! \nPrecisa começar com 'http'")

def obter_cor_status(link):
    if "meet.google.com" in link.lower():
        return "#28a745"  # Verde (Meet)
    elif link.startswith("http"):
        return "#ffc107"  # Amarelo (Outro link)
    else:
        return "#dc3545"  # Vermelho (Inválido/Incompleto)
