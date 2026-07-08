import customtkinter as ctk

from cadastro import abrir_tela_cadastro
from atualizar import abrir_tela_atualizar
import listar as listar_mod
from listar import (
    CORES,
    abrir_tela_consulta,
    buscar_resumo,
    buscar_usuarios,
    criar_linha_usuario,
    criar_mensagem_lista,
    limpar_frame,
)
from remover import abrir_tela_excluir


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")



def carregar_icone(caminho, tamanho=(28, 28)):
    try:
        from PIL import Image

        return ctk.CTkImage(Image.open(caminho), size=tamanho)
    except Exception:
        return None


def abrirNovaTelaSistema(app):
    app.withdraw()

    tela_sistema = ctk.CTkToplevel(app)
    tela_sistema.title("Sistema - Cadastro Base")
    tela_sistema.configure(fg_color=CORES["fundo"])

    try:
        tela_sistema.state("zoomed")
    except Exception:
        tela_sistema.geometry("1100x700")

    tela_sistema.lift()
    tela_sistema.focus_force()

    tela_sistema.grid_columnconfigure(1, weight=1)
    tela_sistema.grid_rowconfigure(1, weight=1)

    contexto = {"conteudo": None, "pesquisa": None}

    criar_topo(tela_sistema, app, contexto)
    criar_sidebar(tela_sistema, app, contexto)
    criar_conteudo(tela_sistema, app, contexto)


def criar_topo(tela, app, contexto):
    frame_topo = ctk.CTkFrame(
        tela,
        height=78,
        fg_color=CORES["painel"],
        corner_radius=0,
        border_width=1,
        border_color=CORES["linha"],
    )
    frame_topo.grid(row=0, column=0, columnspan=2, sticky="ew")
    frame_topo.grid_columnconfigure(1, weight=1)
    frame_topo.grid_propagate(False)

    bloco_titulo = ctk.CTkFrame(frame_topo, fg_color="transparent")
    bloco_titulo.grid(row=0, column=0, padx=26, pady=13, sticky="w")

    ctk.CTkLabel(
        bloco_titulo,
        text="Cadastro Base",
        font=("Segoe UI", 24, "bold"),
        text_color=CORES["texto"],
    ).pack(anchor="w")

    ctk.CTkLabel(
        bloco_titulo,
        text="Painel administrativo de usuarios",
        font=("Segoe UI", 13),
        text_color=CORES["texto_suave"],
    ).pack(anchor="w")

    area_pesquisa = ctk.CTkFrame(frame_topo, fg_color="transparent")
    area_pesquisa.grid(row=0, column=1, padx=20, pady=18, sticky="e")

    pesquisa = ctk.CTkEntry(
        area_pesquisa,
        placeholder_text="Pesquisar usuario, CPF ou identidade...",
        width=340,
        height=40,
        border_width=1,
        border_color=CORES["linha"],
        fg_color=CORES["painel_claro"],
        text_color=CORES["texto"],
        placeholder_text_color=CORES["texto_suave"],
    )
    pesquisa.pack(side="left", padx=(0, 10))
    contexto["pesquisa"] = pesquisa

    def pesquisar():
        abrir_tela_consulta(app, pesquisa.get())

    pesquisa.bind("<Return>", lambda event: pesquisar())

    ctk.CTkButton(
        area_pesquisa,
        text="Pesquisar",
        width=112,
        height=40,
        corner_radius=8,
        fg_color=CORES["azul"],
        hover_color=CORES["azul_hover"],
        command=pesquisar,
    ).pack(side="left")

    def voltar():
        tela.destroy()
        app.deiconify()

    ctk.CTkButton(
        frame_topo,
        text="Logout",
        width=108,
        height=40,
        corner_radius=8,
        fg_color=CORES["vermelho"],
        hover_color=CORES["vermelho_hover"],
        command=voltar,
    ).grid(row=0, column=2, padx=(0, 26), pady=18)


def criar_sidebar(tela, app, contexto):
    sidebar = ctk.CTkFrame(
        tela,
        width=250,
        fg_color=CORES["sidebar"],
        corner_radius=0,
        border_width=1,
        border_color=CORES["linha"],
    )
    sidebar.grid(row=1, column=0, sticky="nsw")
    sidebar.grid_propagate(False)

    ctk.CTkLabel(
        sidebar,
        text="Menu",
        font=("Segoe UI", 13, "bold"),
        text_color=CORES["texto_suave"],
    ).pack(anchor="w", padx=22, pady=(24, 12))

    botoes = [
        ("Dashboard", None, lambda: recarregar_dashboard(app, contexto)),
        ("Cadastrar usuario", "img/cadastro.png", lambda: abrir_tela_cadastro(app)),
        ("Atualizar cadastro", "img/atualizar.png", lambda: abrir_tela_atualizar(app)),
        ("Excluir usuario", "img/remover.png", lambda: abrir_tela_excluir(app)),
        ("Consultar usuarios", "img/listar.png", lambda: abrir_tela_consulta(app)),
    ]

    for texto, icone, comando in botoes:
        criar_botao_menu(sidebar, texto, icone, comando)

    rodape = ctk.CTkFrame(
        sidebar,
        fg_color=CORES["painel_claro"],
        corner_radius=8,
        border_width=1,
        border_color=CORES["linha"],
    )
    rodape.pack(side="bottom", fill="x", padx=16, pady=18)

    ctk.CTkLabel(
        rodape,
        text="Usuario logado",
        font=("Segoe UI", 12),
        text_color=CORES["texto_suave"],
    ).pack(anchor="w", padx=14, pady=(12, 0))

    ctk.CTkLabel(
        rodape,
        text="Administrador",
        font=("Segoe UI", 14, "bold"),
        text_color=CORES["texto"],
    ).pack(anchor="w", padx=14, pady=(0, 12))


def criar_conteudo(tela, app, contexto):
    conteudo = ctk.CTkScrollableFrame(tela, fg_color=CORES["fundo"], corner_radius=0)
    conteudo.grid(row=1, column=1, sticky="nsew", padx=24, pady=24)
    conteudo.grid_columnconfigure((0, 1, 2, 3), weight=1)
    contexto["conteudo"] = conteudo

    montar_dashboard(app, contexto)


def recarregar_dashboard(app, contexto):
    limpar_frame(contexto["conteudo"])
    montar_dashboard(app, contexto)


def montar_dashboard(app, contexto):
    conteudo = contexto["conteudo"]

    cabecalho = ctk.CTkFrame(conteudo, fg_color="transparent")
    cabecalho.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 18))
    cabecalho.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        cabecalho,
        text="Visao geral",
        font=("Segoe UI", 28, "bold"),
        text_color=CORES["texto"],
    ).grid(row=0, column=0, sticky="w")

    ctk.CTkButton(
        cabecalho,
        text="Atualizar informacoes",
        width=176,
        height=38,
        corner_radius=8,
        fg_color=CORES["azul"],
        hover_color=CORES["azul_hover"],
        command=lambda: recarregar_dashboard(app, contexto),
    ).grid(row=0, column=1, sticky="e")

    try:
        resumo = buscar_resumo()
        ultimos = buscar_usuarios(limite=6)
        erro = None
    except Exception as e:
        resumo = {"total": 0, "masculino": 0, "feminino": 0, "estados": 0}
        ultimos = []
        erro = str(e)

    criar_card_resumo(conteudo, 0, "Total usuarios", resumo["total"], CORES["azul"])
    criar_card_resumo(conteudo, 1, "Masculino", resumo["masculino"], CORES["verde"])
    criar_card_resumo(conteudo, 2, "Feminino", resumo["feminino"], CORES["amarelo"])
    criar_card_resumo(conteudo, 3, "UFs cadastradas", resumo["estados"], CORES["vermelho"])

    painel_acoes = ctk.CTkFrame(
        conteudo,
        fg_color=CORES["painel"],
        corner_radius=10,
        border_width=1,
        border_color=CORES["linha"],
    )
    painel_acoes.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=22, padx=(0, 11))
    painel_acoes.grid_columnconfigure((0, 1), weight=1)

    ctk.CTkLabel(
        painel_acoes,
        text="Acoes rapidas",
        font=("Segoe UI", 20, "bold"),
        text_color=CORES["texto"],
    ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(18, 10))

    criar_card_acao(painel_acoes, 1, 0, "Cadastrar", "Novo usuario", "img/cadastro.png", lambda: abrir_tela_cadastro(app))
    criar_card_acao(painel_acoes, 1, 1, "Atualizar", "Editar dados", "img/atualizar.png", lambda: abrir_tela_atualizar(app))
    criar_card_acao(painel_acoes, 2, 0, "Excluir", "Remover usuario", "img/remover.png", lambda: abrir_tela_excluir(app))
    criar_card_acao(painel_acoes, 2, 1, "Consultar", "Pesquisar base", "img/listar.png", lambda: abrir_tela_consulta(app))

    painel_tabela = ctk.CTkFrame(
        conteudo,
        fg_color=CORES["painel"],
        corner_radius=10,
        border_width=1,
        border_color=CORES["linha"],
    )
    painel_tabela.grid(row=2, column=2, columnspan=2, sticky="nsew", pady=22, padx=(11, 0))
    painel_tabela.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        painel_tabela,
        text="Ultimos cadastros",
        font=("Segoe UI", 20, "bold"),
        text_color=CORES["texto"],
    ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 12))

    if erro:
        criar_mensagem_lista(painel_tabela, 1, f"Nao foi possivel carregar a base:\n{erro}")
    elif not ultimos:
        criar_mensagem_lista(painel_tabela, 1, "Nenhum usuario cadastrado.")
    else:
        for indice, usuario in enumerate(ultimos, start=1):
            criar_linha_usuario(painel_tabela, indice, usuario)


def criar_botao_menu(pai, texto, caminho_icone, comando):
    ctk.CTkButton(
        pai,
        text=texto,
        image=carregar_icone(caminho_icone) if caminho_icone else None,
        compound="left",
        anchor="w",
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color=CORES["hover_menu"],
        text_color=CORES["texto"],
        font=("Segoe UI", 14),
        command=comando,
    ).pack(fill="x", padx=14, pady=4)


def criar_card_resumo(pai, coluna, titulo, valor, cor):
    card = ctk.CTkFrame(
        pai,
        fg_color=CORES["painel"],
        corner_radius=10,
        border_width=1,
        border_color=CORES["linha"],
    )
    card.grid(row=1, column=coluna, sticky="ew", padx=6)

    ctk.CTkFrame(card, width=4, fg_color=cor, corner_radius=8).pack(side="left", fill="y")

    corpo = ctk.CTkFrame(card, fg_color="transparent")
    corpo.pack(side="left", fill="both", expand=True, padx=16, pady=16)

    ctk.CTkLabel(
        corpo,
        text=titulo,
        font=("Segoe UI", 13),
        text_color=CORES["texto_suave"],
    ).pack(anchor="w")

    ctk.CTkLabel(
        corpo,
        text=str(valor),
        font=("Segoe UI", 28, "bold"),
        text_color=CORES["texto"],
    ).pack(anchor="w")


def criar_card_acao(pai, linha, coluna, titulo, subtitulo, caminho_icone, comando):
    ctk.CTkButton(
        pai,
        text=f"{titulo}\n{subtitulo}",
        image=carregar_icone(caminho_icone, (34, 34)),
        compound="top",
        width=180,
        height=130,
        corner_radius=10,
        border_width=1,
        border_color=CORES["linha"],
        fg_color=CORES["painel_claro"],
        hover_color=CORES["hover_menu"],
        text_color=CORES["texto"],
        font=("Segoe UI", 15, "bold"),
        command=comando,
    ).grid(row=linha, column=coluna, sticky="nsew", padx=12, pady=12)


if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    abrirNovaTelaSistema(app)
    app.mainloop()
