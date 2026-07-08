import customtkinter as ctk

from listar import (
    CORES,
    buscar_usuarios,
    criar_area_busca,
    criar_janela_base,
    criar_linha_usuario,
    criar_mensagem_lista,
    executar_comando,
    limpar_frame,
    mostrar_mensagem,
)


def criar_formulario_usuario(pai):
    frame = ctk.CTkFrame(pai, fg_color=CORES["painel"], corner_radius=10)
    frame.pack(fill="x", padx=22, pady=(0, 16))
    frame.grid_columnconfigure((0, 1), weight=1)

    campos = {}
    definicoes = [
        ("nome", "Nome"),
        ("sobrenome", "Sobrenome"),
        ("identidade", "Identidade"),
        ("cpf", "CPF"),
        ("uf", "UF"),
        ("cidade", "Cidade"),
        ("data_nasc", "Data nascimento YYYY-MM-DD"),
    ]

    for indice, (chave, placeholder) in enumerate(definicoes):
        entrada = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            height=38,
            fg_color=CORES["painel_claro"],
            border_color=CORES["linha"],
        )
        entrada.grid(row=indice // 2, column=indice % 2, sticky="ew", padx=14, pady=10)
        campos[chave] = entrada

    sexo = ctk.StringVar(value="M")
    area_sexo = ctk.CTkFrame(frame, fg_color="transparent")
    area_sexo.grid(row=4, column=0, columnspan=2, sticky="w", padx=14, pady=(8, 14))

    ctk.CTkRadioButton(
        area_sexo,
        text="Masculino",
        variable=sexo,
        value="M",
    ).pack(side="left", padx=(0, 20))

    ctk.CTkRadioButton(
        area_sexo,
        text="Feminino",
        variable=sexo,
        value="F",
    ).pack(side="left")

    campos["sexo"] = sexo
    return campos


def preencher_formulario(campos, usuario):
    for chave, entrada in campos.items():
        if chave == "sexo":
            entrada.set(usuario.get(chave) or "M")
        else:
            entrada.delete(0, "end")
            entrada.insert(0, usuario.get(chave) or "")


def ler_formulario(campos):
    return {
        "nome": campos["nome"].get(),
        "sobrenome": campos["sobrenome"].get(),
        "identidade": campos["identidade"].get(),
        "cpf": campos["cpf"].get(),
        "uf": campos["uf"].get().upper(),
        "cidade": campos["cidade"].get(),
        "data_nasc": campos["data_nasc"].get(),
        "sexo": campos["sexo"].get(),
    }


def abrir_tela_atualizar(app):
    janela = criar_janela_base(app, "Atualizar cadastro", 920, 720)
    selecionado = {"usuario": None}

    ctk.CTkLabel(
        janela,
        text="Atualizar cadastro",
        font=("Segoe UI", 24, "bold"),
        text_color=CORES["texto"],
    ).pack(anchor="w", padx=22, pady=(20, 14))

    campos = criar_formulario_usuario(janela)

    def salvar():
        usuario = selecionado["usuario"]

        if not usuario:
            mostrar_mensagem(app, "Aviso", "Pesquise e selecione um usuario antes de salvar.", "erro")
            return

        dados = ler_formulario(campos)
        dados["rid"] = usuario["rid"]

        sql = """
            UPDATE usuarios
            SET
                nome = :nome,
                sobrenome = :sobrenome,
                identidade = :identidade,
                cpf = :cpf,
                uf = :uf,
                cidade = :cidade,
                data_nasc = TO_DATE(:data_nasc, 'YYYY-MM-DD'),
                sexo = :sexo
            WHERE ROWID = CHARTOROWID(:rid)
        """

        try:
            afetados = executar_comando(sql, dados)

            if afetados:
                mostrar_mensagem(app, "Sucesso", "Cadastro atualizado com sucesso.", "sucesso")
            else:
                mostrar_mensagem(app, "Aviso", "Nenhum cadastro foi atualizado.", "erro")

        except Exception as e:
            mostrar_mensagem(app, "Erro", f"Erro ao atualizar:\n{e}", "erro")

    ctk.CTkButton(
        janela,
        text="Salvar alteracoes",
        height=42,
        fg_color=CORES["verde"],
        hover_color="#15803D",
        command=salvar,
    ).pack(fill="x", padx=22, pady=(0, 16))

    lista = ctk.CTkScrollableFrame(janela, fg_color=CORES["painel"], corner_radius=10)
    lista.pack(fill="both", expand=True, padx=22, pady=(0, 22))
    lista.grid_columnconfigure(0, weight=1)

    def selecionar(usuario):
        selecionado["usuario"] = usuario
        preencher_formulario(campos, usuario)

    def pesquisar(termo):
        limpar_frame(lista)

        try:
            usuarios = buscar_usuarios(termo, limite=50)
        except Exception as e:
            criar_mensagem_lista(lista, 0, f"Erro ao consultar:\n{e}")
            return

        if not usuarios:
            criar_mensagem_lista(lista, 0, "Nenhum usuario encontrado.")
            return

        for indice, usuario in enumerate(usuarios):
            criar_linha_usuario(lista, indice, usuario, selecionar)

    criar_area_busca(janela, "Pesquise para selecionar o cadastro", pesquisar)
    pesquisar("")
