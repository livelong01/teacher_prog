import tkinter as tk
import webbrowser
import json
import os
import shutil
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

# Configurações de arquivo
ARQUIVO = "alunos.json"
PASTA_FOTOS = "fotos"
FOTO_PADRAO = "fotos/padrao.png"

# Garantir que a pasta de fotos exista
if not os.path.exists(PASTA_FOTOS):
    os.makedirs(PASTA_FOTOS)

# --- FUNÇÕES DE DADOS ---

def carregar_alunos():
    if not os.path.exists(ARQUIVO):
        return []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def salvar_alunos():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(alunos, f, ensure_ascii=False, indent=2)

def abrir_reuniao(link):
    if link.startswith("http"):
        webbrowser.open(link)
    else:
        messagebox.showerror("Erro", "Link inválido! \n"
        "Precisa começar com 'http'")

# --- FUNÇÕES DE INTERFACE ---

def filtrar_alunos(event=None):
    canvas.yview_moveto(0) # Leva o scroll para o topo ao pesquisar
    termo = campo_busca.get().lower()
    
    # Deleta todos os widgets que estão dentro do container
    for widget in container.winfo_children():
        widget.destroy()
    
    # Reconstrói os cards apenas para os nomes que contém o termo
    for aluno in alunos:
        if termo in aluno["nome"].lower():
            criar_card_aluno(container, aluno)

def excluir_aluno(frame_aluno, aluno):
    if messagebox.askyesno("Confirmar", f"Deseja excluir {aluno['nome']}?"):
        global alunos # Garante que estamos mexendo na lista certa
        
        # Remove da lista global
        alunos = [a for a in alunos if a != aluno]
        salvar_alunos()
        
        # Remove a foto
        if aluno["foto"] != FOTO_PADRAO and os.path.exists(aluno["foto"]):
            try:
                os.remove(aluno["foto"])
            except:
                pass
        
        # IMPORTANTE: Em vez de só destruir o frame, chame o filtro
        # para atualizar a visualização baseada na lista nova
        filtrar_alunos()

def criar_card_aluno(pai, aluno):
    frame = tk.Frame(pai, bd=1, relief="solid", padx=5, pady=5)
    frame.pack(fill="x", pady=5, padx=10)

    # Lógica de imagem
    try:
        caminho = aluno.get("foto", FOTO_PADRAO)
        if not os.path.exists(caminho):
            caminho = FOTO_PADRAO
        img = Image.open(caminho).resize((50, 50))
        foto = ImageTk.PhotoImage(img)
    except:
        img = Image.open(FOTO_PADRAO).resize((50, 50))
        foto = ImageTk.PhotoImage(img)

    btn = tk.Button(
        frame, image=foto, text=aluno["nome"], compound="left",
        command=lambda: abrir_reuniao(aluno["link"]),
        anchor="w", padx=10, relief="flat", font=("Arial", 10, "bold")
    )
    btn.image = foto # Referência para o lixo do Python não apagar a imagem
    btn.pack(side="left", fill="x", expand=True)
    
    btn_excluir = tk.Button(
        frame, text="✖", fg="white", bg="#ff4444",
        font=("Arial", 8), command=lambda: excluir_aluno(frame, aluno)
    )
    btn_excluir.pack(side="right", padx=5)
    
        # Botão de Editar (Adicione isso dentro da função criar_card_aluno)
    btn_editar = tk.Button(
        frame, text="Editar", fg="black", bg="#FFD700", # Cor amarela/ouro
        font=("Arial", 8), command=lambda: abrir_janela_edicao(aluno)
    )
    btn_editar.pack(side="right", padx=2)

def abrir_janela_cadastro():
    cadastro = tk.Toplevel(janela)
    cadastro.title("Novo Aluno")
    cadastro.geometry("350x450")
    cadastro.grab_set() # Torna a janela modal (foca nela)
    
    foto_temp = {"caminho": FOTO_PADRAO}

    tk.Label(cadastro, text="Nome do Aluno:", font=("Arial", 10, "bold")).pack(pady=10)
    campo_nome = tk.Entry(cadastro, width=35)
    campo_nome.pack()

    tk.Label(cadastro, text="Link do Google Meet:", font=("Arial", 10, "bold")).pack(pady=10)
    campo_link = tk.Entry(cadastro, width=35)
    campo_link.pack()

    label_foto = tk.Label(cadastro, text="Nenhuma foto selecionada", fg="gray")
    
    def selecionar_foto():
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png")])
        if caminho:
            foto_temp["caminho"] = caminho
            label_foto.config(text=f"Selecionado: {os.path.basename(caminho)}", fg="green")
        cadastro.lift() # Garante que a janela de cadastro volte para frente

    tk.Button(cadastro, text="Selecionar Foto", command=selecionar_foto).pack(pady=10)
    label_foto.pack()

    def salvar():
        nome = campo_nome.get().strip()
        link = campo_link.get().strip()

        if not nome or not link:
            messagebox.showwarning("Erro", "Preencha nome e link!")
            return

        # Processar Foto
        caminho_final = FOTO_PADRAO
        if foto_temp["caminho"] != FOTO_PADRAO:
            ext = os.path.splitext(foto_temp["caminho"])[1]
            nome_arq = f"{nome.lower().replace(' ', '_')}{ext}"
            caminho_final = os.path.join(PASTA_FOTOS, nome_arq)
            shutil.copy(foto_temp["caminho"], caminho_final)

        novo_aluno = {"nome": nome, "link": link, "foto": caminho_final}
        alunos.append(novo_aluno)
        alunos.sort(key=lambda x: x["nome"].lower()) # Ordenar
        
        salvar_alunos()
        campo_busca.delete(0, tk.END) # Reseta busca
        filtrar_alunos() # Atualiza lista na tela
        cadastro.destroy()

    tk.Button(cadastro, text="SALVAR", bg="#4CAF50", fg="white", 
              font=("Arial", 10, "bold"), command=salvar, width=10).pack(pady=15)

def abrir_janela_edicao(aluno_antigo):
    edicao = tk.Toplevel(janela)
    edicao.title(f"Editando: {aluno_antigo['nome']}")
    edicao.geometry("350x450")
    edicao.grab_set()
    
    # Variável para a foto (começa com a foto que o aluno já tem)
    foto_temp = {"caminho": aluno_antigo["foto"]}

    tk.Label(edicao, text="Nome do Aluno:", font=("Arial", 10, "bold")).pack(pady=10)
    campo_nome = tk.Entry(edicao, width=35)
    campo_nome.insert(0, aluno_antigo["nome"]) # Preenche com o nome atual
    campo_nome.pack()

    tk.Label(edicao, text="Link do Google Meet:", font=("Arial", 10, "bold")).pack(pady=10)
    campo_link = tk.Entry(edicao, width=35)
    campo_link.insert(0, aluno_antigo["link"]) # Preenche com o link atual
    campo_link.pack()

    label_foto = tk.Label(edicao, text=f"Foto atual: {os.path.basename(aluno_antigo['foto'])}", fg="blue")
    
    def selecionar_nova_foto():
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png")])
        if caminho:
            foto_temp["caminho"] = caminho
            label_foto.config(text=f"Nova: {os.path.basename(caminho)}", fg="green")
        edicao.lift()

    tk.Button(edicao, text="Trocar Foto", command=selecionar_nova_foto).pack(pady=10)
    label_foto.pack()

    def salvar_alteracoes():
        nome = campo_nome.get().strip()
        link = campo_link.get().strip()

        if not nome or not link:
            messagebox.showwarning("Erro", "Nome e link não podem ficar vazios!")
            return

        # Se a foto mudou, processamos o novo arquivo
        caminho_final = foto_temp["caminho"]
        if foto_temp["caminho"] != aluno_antigo["foto"]:
            ext = os.path.splitext(foto_temp["caminho"])[1]
            nome_arq = f"{nome.lower().replace(' ', '_')}_edit{ext}"
            caminho_final = os.path.join(PASTA_FOTOS, nome_arq)
            shutil.copy(foto_temp["caminho"], caminho_final)

        # Atualiza o objeto na lista original
        aluno_antigo["nome"] = nome
        aluno_antigo["link"] = link
        aluno_antigo["foto"] = caminho_final

        alunos.sort(key=lambda x: x["nome"].lower()) # Reordenar caso o nome mude
        salvar_alunos()
        filtrar_alunos() # Atualiza a tela principal
        edicao.destroy()

    tk.Button(edicao, text="SALVAR ALTERAÇÕES", bg="#FF9800", fg="white", 
              font=("Arial", 10, "bold"), command=salvar_alteracoes).pack(pady=30)

# --- INICIALIZAÇÃO DA JANELA PRINCIPAL ---

alunos = carregar_alunos()
alunos.sort(key=lambda x: x["nome"].lower())

janela = tk.Tk()
janela.title("Meets dos Alunos")
janela.geometry("500x650")

# Título e Busca
tk.Label(janela, text="Controle de Acessos", font=("Arial", 16, "bold")).pack(pady=10)
tk.Label(janela, text="Buscar aluno:").pack()
campo_busca = tk.Entry(janela, font=("Arial", 12), width=35)
campo_busca.pack(pady=5)
campo_busca.bind("<KeyRelease>", filtrar_alunos)

# --- ESTRUTURA DE SCROLL ---
frame_scroll = tk.Frame(janela)
frame_scroll.pack(fill="both", expand=True, padx=5, pady=5)

canvas = tk.Canvas(frame_scroll)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
container = tk.Frame(canvas)
canvas_frame = canvas.create_window((0, 0), window=container, anchor="nw")

def ajustar_largura(event):
    canvas.itemconfig(canvas_frame, width=event.width)
canvas.bind("<Configure>", ajustar_largura)

def configurar_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
container.bind("<Configure>", configurar_scroll)

def _on_mousewheel(event):
    # Obtém a altura atual do Canvas (o que aparece na tela)
    altura_visivel = canvas.winfo_height()
    # Obtém a altura total de todos os cards somados
    altura_total = container.winfo_height()

    # Só permite o scroll se o conteúdo for maior que a janela
    if altura_total > altura_visivel:
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        
canvas.bind_all("<MouseWheel>", _on_mousewheel)

# --- CARGA INICIAL ---
for a in alunos:
    criar_card_aluno(container, a)

# Botão de Adicionar (Fixo no rodapé)
tk.Button(
    janela, text="+ Adicionar Novo Aluno", bg="#2196F3", fg="white",
    font=("Arial", 11, "bold"), command=abrir_janela_cadastro, pady=10
).pack(fill="x", padx=20, pady=15)

janela.mainloop()