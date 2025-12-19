import os
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

from app.data import carregar_alunos, salvar_alunos, PASTA_FOTOS, FOTO_PADRAO, copy_photo
from app.utils import abrir_reuniao, obter_cor_status


def run_app():
    alunos = carregar_alunos()
    alunos.sort(key=lambda x: x["nome"].lower())

    janela = tk.Tk()
    janela.title("Meets dos Alunos")
    janela.geometry("500x650")

    project_root = Path(__file__).resolve().parent.parent
    icon_path = project_root / "icon.ico"
    if icon_path.exists():
        try:
            janela.iconbitmap(str(icon_path))
        except Exception:
            pass
        try:
            # Also set a PhotoImage icon (works better on some platforms)
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            janela.iconphoto(False, photo)
            janela._icon_photo = photo
        except Exception:
            pass

    # --- variáveis que serão fechadas nas funções internas ---
    container = None
    canvas = None
    campo_busca = None

    def filtrar_alunos(event=None):
        canvas.yview_moveto(0)
        termo = campo_busca.get().lower()
        for widget in container.winfo_children():
            widget.destroy()
        for aluno in alunos:
            if termo in aluno["nome"].lower():
                criar_card_aluno(container, aluno)

    def excluir_aluno(frame_aluno, aluno):
        if messagebox.askyesno("Confirmar", f"Deseja excluir {aluno['nome']}?"):
            nonlocal alunos
            alunos = [a for a in alunos if a != aluno]
            salvar_alunos(alunos)
            if aluno["foto"] != FOTO_PADRAO and os.path.exists(aluno["foto"]):
                try:
                    os.remove(aluno["foto"])
                except Exception:
                    pass
            filtrar_alunos()

    def criar_card_aluno(pai, aluno):
        frame = tk.Frame(pai, bd=1, relief="solid", padx=5, pady=5)
        frame.pack(fill="x", pady=5, padx=10)
        try:
            caminho = aluno.get("foto", FOTO_PADRAO)
            if not os.path.exists(caminho):
                caminho = FOTO_PADRAO
            img = Image.open(caminho).resize((50, 50))
            foto = ImageTk.PhotoImage(img)
        except Exception:
            img = Image.open(FOTO_PADRAO).resize((50, 50))
            foto = ImageTk.PhotoImage(img)

        btn = tk.Button(
            frame, image=foto, text=aluno["nome"], compound="left",
            command=lambda: abrir_reuniao(aluno["link"]),
            anchor="w", padx=10, relief="flat", font=("Arial", 10, "bold")
        )
        btn.image = foto
        btn.pack(side="left", fill="x", expand=True)

        cor = obter_cor_status(aluno["link"])
        status_dot = tk.Canvas(frame, width=12, height=12, highlightthickness=0)
        status_dot.create_oval(2, 2, 10, 10, fill=cor, outline="black")
        status_dot.pack(side="left", padx=5)

        btn_excluir = tk.Button(
            frame, text="Excluir", fg="white", bg="#ff4444",
            font=("Arial", 8, "bold"), command=lambda: excluir_aluno(frame, aluno),
            width=6
        )
        btn_excluir.pack(side="right", padx=5)

        btn_editar = tk.Button(
            frame, text="Editar", fg="black", bg="#FFD700",
            font=("Arial", 8, "bold"), command=lambda: abrir_janela_edicao(aluno),
            width=6
        )
        btn_editar.pack(side="right", padx=2)

    def abrir_janela_cadastro():
        cadastro = tk.Toplevel(janela)
        cadastro.title("Novo Aluno")
        cadastro.geometry("350x450")
        cadastro.grab_set()
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
            cadastro.lift()

        tk.Button(cadastro, text="Selecionar Foto", command=selecionar_foto).pack(pady=10)
        label_foto.pack()

        def salvar():
            nome = campo_nome.get().strip()
            link = campo_link.get().strip()
            if not nome or not link:
                messagebox.showwarning("Erro", "Preencha nome e link!")
                return
            caminho_final = FOTO_PADRAO
            if foto_temp["caminho"] != FOTO_PADRAO:
                ext = Path(foto_temp["caminho"]).suffix
                nome_arq = f"{nome.lower().replace(' ', '_')}{ext}"
                caminho_final = copy_photo(foto_temp["caminho"], nome_arq)
            novo_aluno = {"nome": nome, "link": link, "foto": caminho_final}
            alunos.append(novo_aluno)
            alunos.sort(key=lambda x: x["nome"].lower())
            salvar_alunos(alunos)
            campo_busca.delete(0, tk.END)
            filtrar_alunos()
            cadastro.destroy()

        tk.Button(cadastro, text="SALVAR", bg="#4CAF50", fg="white",
                  font=("Arial", 10, "bold"), command=salvar, width=10).pack(pady=15)

    def abrir_janela_edicao(aluno_antigo):
        edicao = tk.Toplevel(janela)
        edicao.title(f"Editando: {aluno_antigo['nome']}")
        edicao.geometry("350x450")
        edicao.grab_set()
        foto_temp = {"caminho": aluno_antigo["foto"]}

        tk.Label(edicao, text="Nome do Aluno:", font=("Arial", 10, "bold")).pack(pady=10)
        campo_nome = tk.Entry(edicao, width=35)
        campo_nome.insert(0, aluno_antigo["nome"])
        campo_nome.pack()

        tk.Label(edicao, text="Link do Google Meet:", font=("Arial", 10, "bold")).pack(pady=10)
        campo_link = tk.Entry(edicao, width=35)
        campo_link.insert(0, aluno_antigo["link"])
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
            caminho_final = foto_temp["caminho"]
            if foto_temp["caminho"] != aluno_antigo["foto"]:
                ext = Path(foto_temp["caminho"]).suffix
                nome_arq = f"{nome.lower().replace(' ', '_')}_edit{ext}"
                caminho_final = copy_photo(foto_temp["caminho"], nome_arq)
            aluno_antigo["nome"] = nome
            aluno_antigo["link"] = link
            aluno_antigo["foto"] = caminho_final
            alunos.sort(key=lambda x: x["nome"].lower())
            salvar_alunos(alunos)
            filtrar_alunos()
            edicao.destroy()

        tk.Button(edicao, text="SALVAR ALTERAÇÕES", bg="#FF9800", fg="white",
                  font=("Arial", 10, "bold"), command=salvar_alteracoes).pack(pady=30)

    # --- Construção da UI ---
    tk.Label(janela, text="Controle de Acessos", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(janela, text="Buscar aluno:").pack()
    campo_busca = tk.Entry(janela, font=("Arial", 12), width=35)
    campo_busca.pack(pady=5)
    campo_busca.bind("<KeyRelease>", filtrar_alunos)

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
        altura_visivel = canvas.winfo_height()
        altura_total = container.winfo_height()
        if altura_total > altura_visivel:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    for a in alunos:
        criar_card_aluno(container, a)

    tk.Button(
        janela, text="+ Adicionar Novo Aluno", bg="#2196F3", fg="white",
        font=("Arial", 11, "bold"), command=abrir_janela_cadastro, pady=10
    ).pack(fill="x", padx=20, pady=15)

    janela.mainloop()
