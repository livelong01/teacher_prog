import tkinter as tk
import webbrowser
import json
import os
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import shutil

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
    # Criamos um frame principal para o card
    frame = tk.Frame(pai, bd=1, relief="solid", padx=5, pady=5)
    frame.pack(fill="x", pady=5, padx=10)

    # Carregar a imagem
    try:
        caminho_foto = aluno.get("foto", "fotos/padrao.png")
        if not os.path.exists(caminho_foto):
            caminho_foto = "fotos/padrao.png"
        img = Image.open(caminho_foto).resize((50, 50))
        foto = ImageTk.PhotoImage(img)
    except:
        # Caso a imagem esteja corrompida ou inacessível
        img = Image.open("fotos/padrao.png").resize((50, 50))
        foto = ImageTk.PhotoImage(img)

    # Botão principal (Nome + Foto) - agora usando 'side' para organizar
    btn = tk.Button(
        frame,
        image=foto,
        text=aluno["nome"],
        compound="left",
        command=lambda: abrir_reuniao(aluno["link"]),
        anchor="w",
        padx=10,
        relief="flat"
    )
    btn.image = foto
    btn.pack(side="left", fill="x", expand=True)

    # Botão de Excluir (Lixeira)
    btn_excluir = tk.Button(
        frame,
        text="✖",
        fg="white",
        bg="#ff4444",
        font=("Arial", 5),
        command=lambda: excluir_aluno(frame, aluno),
        padx=2
    )
    btn_excluir.pack(side="right", padx=5)

def abrir_janela_cadastro():
    cadastro = tk.Toplevel(janela)
    cadastro.title("Adicionar aluno")
    cadastro.geometry("350x400") # Aumentei um pouco a altura

    # Faz com que a janela principal fique "travada" até fechar esta
    cadastro.grab_set() 
    # (Opcional) Garante que ela comece na frente
    cadastro.focus_set()

    # Variável para guardar o caminho da foto selecionada
    # Começa com o padrão caso o usuário não escolha uma
    foto_selecionada = {"caminho": "fotos/padrao.png"}

    tk.Label(cadastro, text="Nome").pack(pady=5)
    campo_nome = tk.Entry(cadastro, width=40)
    campo_nome.pack(pady=5)

    tk.Label(cadastro, text="Link").pack(pady=5)
    campo_link = tk.Entry(cadastro, width=40)
    campo_link.pack(pady=5)

    # Label para mostrar o nome do arquivo selecionado
    label_status_foto = tk.Label(cadastro, text="Nenhuma foto selecionada", fg="gray")
    
    def selecionar_foto():
        caminho = filedialog.askopenfilename(
            title="Selecionar Foto",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")]
        )
        if caminho:
            foto_selecionada["caminho"] = caminho
            nome_arquivo = os.path.basename(caminho)
            label_status_foto.config(text=f"Foto: {nome_arquivo}", fg="green")
            #cadastro.lift()          # Traz a janela para frente das outras
            #cadastro.focus_force()

    tk.Button(cadastro, text="Upload Foto", command=selecionar_foto).pack(pady=5)
    label_status_foto.pack()

    def salvar():
        nome = campo_nome.get().strip()
        link = campo_link.get().strip()
        
        if not nome or not link:
            messagebox.showwarning("Erro", "Nome e Link são obrigatórios!")
            return

        # Lógica para copiar a foto para a pasta 'fotos'
        caminho_final = "fotos/padrao.png"
        if foto_selecionada["caminho"] != "fotos/padrao.png":
            # Garante que a pasta existe
            if not os.path.exists("fotos"):
                os.makedirs("fotos")
            
            # Gera um nome de arquivo baseado no nome do aluno para evitar duplicatas
            extensao = os.path.splitext(foto_selecionada["caminho"])[1]
            nome_arquivo = f"{nome.lower().replace(' ', '_')}{extensao}"
            caminho_final = os.path.join("fotos", nome_arquivo)
            
            # Copia o arquivo original para a pasta do projeto
            shutil.copy(foto_selecionada["caminho"], caminho_final)

        aluno = {
            "nome": nome,
            "link": link,
            "foto": caminho_final
        }

        alunos.append(aluno)
        salvar_alunos()
        criar_card_aluno(container, aluno)
        cadastro.destroy()

    tk.Button(cadastro, text="Salvar Aluno", bg="blue", fg="white", command=salvar).pack(pady=20)
    
def excluir_aluno(frame_aluno, aluno):
    # Pergunta se o usuário tem certeza
    confirmar = messagebox.askyesno("Confirmar", f"Deseja excluir o aluno {aluno['nome']}?")
    
    if confirmar:
        # 1. Remover da lista 'alunos' (variável global)
        global alunos
        alunos = [a for a in alunos if a != aluno]
        
        # 2. Salvar o JSON atualizado
        salvar_alunos()
        
        # 3. Excluir o arquivo de foto (se não for a padrão)
        if aluno["foto"] != "fotos/padrao.png" and os.path.exists(aluno["foto"]):
            try:
                os.remove(aluno["foto"])
            except Exception as e:
                print(f"Erro ao deletar foto: {e}")
        
        # 4. Remover o card da interface
        frame_aluno.destroy()

# Carregar alunos
alunos = carregar_alunos()
# Ordena a lista de dicionários pela chave "nome"
alunos.sort(key=lambda x: x["nome"].lower())

# Janela principal
janela = tk.Tk()
janela.title("Acesso rápido aos Meets")
janela.geometry("500x500")

tk.Label(
    janela,
    text="Alunos",
    font=("Arial", 16, "bold")
).pack(pady=10)

# --- ÁREA DE BUSCA ---
tk.Label(janela, text="Pesquisar aluno:", font=("Arial", 10)).pack()
campo_busca = tk.Entry(janela, font=("Arial", 12), width=35)
campo_busca.pack(pady=5)

def filtrar_alunos(event=None):
    termo = campo_busca.get().lower()
    for widget in container.winfo_children():
        widget.destroy()
    for aluno in alunos:
        if termo in aluno["nome"].lower():
            criar_card_aluno(container, aluno)

campo_busca.bind("<KeyRelease>", filtrar_alunos)

# --- INÍCIO DA ÁREA DE SCROLL ---
# 1. Criar um frame para conter o Canvas e a Scrollbar
frame_principal = tk.Frame(janela)
frame_principal.pack(fill="both", expand=True, padx=5, pady=5)

# 2. Criar o Canvas
canvas = tk.Canvas(frame_principal)
canvas.pack(side="left", fill="both", expand=True)

# 3. Adicionar a Scrollbar lateral
scrollbar = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# 4. Configurar o Canvas para usar a Scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# 5. Criar o Frame INTERNO onde os cards serão colocados
container = tk.Frame(canvas)

# 6. Colocar o container dentro do canvas
canvas_frame = canvas.create_window((0, 0), window=container, anchor="nw")

# Atualiza a largura do container para preencher o canvas
def ajustar_largura(event):
    canvas.itemconfig(canvas_frame, width=event.width)

canvas.bind("<Configure>", ajustar_largura)

# Atualiza a área de rolagem sempre que o tamanho do container mudar
def configurar_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

container.bind("<Configure>", configurar_scroll)

# Suporte para o scroll do mouse
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)
# --- FIM DA ÁREA DE SCROLL ---

# O restante do seu código continua quase igual
for aluno in alunos:
    criar_card_aluno(container, aluno)

tk.Button(
    janela,
    text="Adicionar aluno",
    command=abrir_janela_cadastro
).pack(pady=10)

janela.mainloop()
