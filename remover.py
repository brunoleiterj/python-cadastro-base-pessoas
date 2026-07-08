import customtkinter as ctk

from listar import (
    CORES,
    buscar_usuarios,
    centralizar_janela,
    criar_area_busca,
    criar_janela_base,
    criar_linha_usuario,
    criar_mensagem_lista,
    executar_comando,
    limpar_frame,
    mostrar_mensagem,
)


def abrir_tela_excluir(app):
    janela = criar_janela_base(app, "Excluir usuario")

    ctk.CTkLabel(
        janela,
        text="Excluir usuario",
        font=("Segoe UI", 24, "bold"),
        text_color=CORES["texto"],
    ).pack(anchor="w", padx=22, pady=(20, 14))

    lista = ctk.CTkScrollableFrame(janela, fg_color=CORES["painel"], corner_radius=10)
    lista.pack(fill="both", expand=True, padx=22, pady=(0, 22))
    lista.grid_columnconfigure(0, weight=1)

    def pesquisar(termo):
        limpar_frame(lista)
        try:
            usuarios = buscar_usuarios(termo)
        except Exception as e:
            criar_mensagem_lista(lista, 0, f"Erro ao consultar:\n{e}")
            return

        if not usuarios:
            criar_mensagem_lista(lista, 0, "Nenhum usuario encontrado.")
            return

        for indice, usuario in enumerate(usuarios):
            criar_linha_usuario(lista, indice, usuario, excluir, "Excluir")

    def excluir(usuario):
        nome = f"{usuario['nome'] or ''} {usuario['sobrenome'] or ''}".strip()
        confirmar = ctk.CTkToplevel(app)
        confirmar.title("Confirmar exclusao")
        confirmar.geometry("380x180")
        confirmar.configure(fg_color=CORES["fundo"])
        confirmar.transient(janela)
        confirmar.grab_set()
        centralizar_janela(confirmar, 380, 180)

        ctk.CTkLabel(
            confirmar,
            text=f"Deseja excluir {nome or 'este usuario'}?",
            font=("Segoe UI", 14),
            text_color=CORES["texto"],
            wraplength=320,
        ).pack(expand=True, padx=20, pady=18)

        botoes = ctk.CTkFrame(confirmar, fg_color="transparent")
        botoes.pack(pady=(0, 18))

        def confirmar_exclusao():
            try:
                executar_comando(
                    "DELETE FROM usuarios WHERE ROWID = CHARTOROWID(:rid)",
                    {"rid": usuario["rid"]},
                )
                confirmar.destroy()
                mostrar_mensagem(app, "Sucesso", "Usuario excluido com sucesso.", "sucesso")
                pesquisar("")
            except Exception as e:
                confirmar.destroy()
                mostrar_mensagem(app, "Erro", f"Erro ao excluir:\n{e}", "erro")

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            width=110,
            fg_color=CORES["linha"],
            command=confirmar.destroy,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            botoes,
            text="Excluir",
            width=110,
            fg_color=CORES["vermelho"],
            hover_color="#B91C1C",
            command=confirmar_exclusao,
        ).pack(side="left", padx=8)

    criar_area_busca(janela, "Pesquise o usuario que deseja excluir", pesquisar)
    pesquisar("")
