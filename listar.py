import customtkinter as ctk
from db import conectar


CORES = {
    "fundo": "#E5E7EB",
    "painel": "#F3F4F6",
    "sidebar": "#EDEFF3",
    "painel_claro": "#DDE3EA",
    "hover_menu": "#D1D9E6",
    "linha": "#C5CCD6",
    "texto": "#111827",
    "texto_suave": "#64748B",
    "azul": "#2563EB",
    "azul_hover": "#1D4ED8",
    "verde": "#16A34A",
    "vermelho": "#DC2626",
    "vermelho_hover": "#B91C1C",
    "amarelo": "#D97706",
}


CAMPOS_USUARIO = (
    "rid",
    "nome",
    "sobrenome",
    "identidade",
    "cpf",
    "uf",
    "cidade",
    "data_nasc",
    "sexo",
)


def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def mostrar_mensagem(app, titulo, mensagem, tipo="info"):
    popup = ctk.CTkToplevel(app)
    popup.title(titulo)
    popup.geometry("380x180")
    popup.resizable(False, False)
    popup.configure(fg_color=CORES["fundo"])
    popup.transient(app)
    popup.grab_set()
    popup.focus_force()
    centralizar_janela(popup, 380, 180)

    cor = CORES["verde"] if tipo == "sucesso" else CORES["vermelho"] if tipo == "erro" else CORES["azul"]

    ctk.CTkLabel(
        popup,
        text=mensagem,
        wraplength=320,
        text_color=cor,
        font=("Segoe UI", 14),
    ).pack(expand=True, padx=24, pady=18)

    ctk.CTkButton(popup, text="OK", width=120, command=popup.destroy).pack(pady=(0, 18))


def executar_consulta(sql, parametros=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(sql, parametros or {})
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados


def executar_comando(sql, parametros=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(sql, parametros or {})
    afetados = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return afetados


def buscar_usuarios(termo="", limite=100):
    sql = """
        SELECT *
        FROM (
            SELECT
                ROWIDTOCHAR(ROWID) AS rid,
                nome,
                sobrenome,
                identidade,
                cpf,
                uf,
                cidade,
                TO_CHAR(data_nasc, 'YYYY-MM-DD') AS data_nasc,
                sexo
            FROM usuarios
            WHERE
                :termo IS NULL
                OR LOWER(nome) LIKE LOWER(:busca)
                OR LOWER(sobrenome) LIKE LOWER(:busca)
                OR cpf LIKE :busca
                OR identidade LIKE :busca
                OR LOWER(cidade) LIKE LOWER(:busca)
                OR LOWER(uf) LIKE LOWER(:busca)
            ORDER BY ROWID DESC
        )
        WHERE ROWNUM <= :limite
    """
    termo = termo.strip()
    parametros = {
        "termo": termo or None,
        "busca": f"%{termo}%",
        "limite": limite,
    }
    return [dict(zip(CAMPOS_USUARIO, linha)) for linha in executar_consulta(sql, parametros)]


def buscar_resumo():
    sql = """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN sexo = 'M' THEN 1 ELSE 0 END) AS masculino,
            SUM(CASE WHEN sexo = 'F' THEN 1 ELSE 0 END) AS feminino,
            COUNT(DISTINCT uf) AS estados
        FROM usuarios
    """
    total, masculino, feminino, estados = executar_consulta(sql)[0]
    return {
        "total": total or 0,
        "masculino": masculino or 0,
        "feminino": feminino or 0,
        "estados": estados or 0,
    }


def limpar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def criar_janela_base(app, titulo, largura=900, altura=620):
    janela = ctk.CTkToplevel(app)
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    janela.configure(fg_color=CORES["fundo"])
    janela.transient(app)
    janela.grab_set()
    janela.focus_force()
    centralizar_janela(janela, largura, altura)
    return janela


def criar_mensagem_lista(pai, linha, texto):
    ctk.CTkLabel(
        pai,
        text=texto,
        font=("Segoe UI", 14),
        text_color=CORES["texto_suave"],
        wraplength=420,
    ).grid(row=linha, column=0, padx=20, pady=20)


def criar_linha_usuario(pai, linha, usuario, comando=None, texto_botao="Selecionar"):
    item = ctk.CTkFrame(pai, fg_color=CORES["painel_claro"], corner_radius=8)
    item.grid(row=linha, column=0, sticky="ew", padx=18, pady=6)
    item.grid_columnconfigure(0, weight=1)

    textos = ctk.CTkFrame(item, fg_color="transparent")
    textos.grid(row=0, column=0, padx=14, pady=10, sticky="w")

    nome_completo = f"{usuario['nome'] or ''} {usuario['sobrenome'] or ''}".strip()
    detalhe = f"CPF: {usuario['cpf'] or '-'} | ID: {usuario['identidade'] or '-'} | Data Nascimento: {usuario['data_nasc'] or '-'} | Local: {usuario['cidade'] or '-'}-{usuario['uf'] or '-'}"

    ctk.CTkLabel(
        textos,
        text=nome_completo or "Sem nome",
        font=("Segoe UI", 14, "bold"),
        text_color=CORES["texto"],
    ).pack(anchor="w")

    ctk.CTkLabel(
        textos,
        text=detalhe,
        font=("Segoe UI", 12),
        text_color=CORES["texto_suave"],
    ).pack(anchor="w")

    ctk.CTkLabel(
        item,
        text=usuario["sexo"] or "-",
        width=48,
        height=26,
        corner_radius=13,
        fg_color=CORES["azul"] if usuario["sexo"] == "M" else CORES["amarelo"],
        text_color="#FFFFFF",
        font=("Segoe UI", 12, "bold"),
    ).grid(row=0, column=1, padx=14, pady=10)

    if comando:
        ctk.CTkButton(
            item,
            text=texto_botao,
            width=100,
            height=30,
            command=lambda: comando(usuario),
        ).grid(row=0, column=2, padx=(0, 14), pady=10)


def criar_area_busca(pai, placeholder, comando):
    area = ctk.CTkFrame(pai, fg_color="transparent")
    area.pack(fill="x", padx=22, pady=(0, 14))

    entrada = ctk.CTkEntry(
        area,
        placeholder_text=placeholder,
        height=38,
        fg_color=CORES["painel_claro"],
        border_color=CORES["linha"],
    )
    entrada.pack(side="left", fill="x", expand=True, padx=(0, 10))
    entrada.bind("<Return>", lambda event: comando(entrada.get()))

    ctk.CTkButton(
        area,
        text="Pesquisar",
        width=120,
        height=38,
        command=lambda: comando(entrada.get()),
    ).pack(side="left")
    return entrada


def abrir_tela_consulta(app, termo_inicial=""):
    janela = criar_janela_base(app, "Consultar usuarios")

    ctk.CTkLabel(
        janela,
        text="Consultar usuarios",
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
            criar_linha_usuario(lista, indice, usuario)

    entrada = criar_area_busca(janela, "Digite nome, CPF, identidade, cidade ou UF", pesquisar)
    entrada.insert(0, termo_inicial)
    pesquisar(termo_inicial)