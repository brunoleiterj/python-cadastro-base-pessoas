import customtkinter as ctk

from db import conectar
from listar import CORES, centralizar_janela, mostrar_mensagem


def somente_numeros(valor):
    return "".join(caractere for caractere in valor if caractere.isdigit())


def formatar_cpf(valor):
    numeros = somente_numeros(valor)[:11]

    if len(numeros) <= 3:
        return numeros
    if len(numeros) <= 6:
        return f"{numeros[:3]}.{numeros[3:]}"
    if len(numeros) <= 9:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"


def formatar_identidade(valor):
    numeros = somente_numeros(valor)[:9]

    if len(numeros) <= 2:
        return numeros
    if len(numeros) <= 5:
        return f"{numeros[:2]}.{numeros[2:]}"
    if len(numeros) <= 8:
        return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:]}"
    return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}-{numeros[8:]}"


def formatar_data(valor):
    numeros = somente_numeros(valor)[:8]

    if len(numeros) <= 4:
        return numeros
    if len(numeros) <= 6:
        return f"{numeros[:4]}-{numeros[4:]}"
    return f"{numeros[:4]}-{numeros[4:6]}-{numeros[6:]}"


def aplicar_mascara(entrada, formatador):
    valor_formatado = formatador(entrada.get())
    entrada.delete(0, "end")
    entrada.insert(0, valor_formatado)
    entrada.icursor("end")


def abrir_tela_cadastro(app):
    tela_cadastro = ctk.CTkToplevel(app)
    tela_cadastro.title("Cadastro de Usuario")
    tela_cadastro.configure(fg_color=CORES["fundo"])

    largura = 760
    altura = 560
    centralizar_janela(tela_cadastro, largura, altura)

    tela_cadastro.transient(app)
    tela_cadastro.grab_set()
    tela_cadastro.focus_force()

    tela_cadastro.grid_columnconfigure(0, weight=1)
    tela_cadastro.grid_rowconfigure(1, weight=1)

    cabecalho = ctk.CTkFrame(tela_cadastro, fg_color="transparent")
    cabecalho.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 14))
    cabecalho.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        cabecalho,
        text="Cadastro de usuario",
        font=("Segoe UI", 26, "bold"),
        text_color=CORES["texto"],
    ).grid(row=0, column=0, sticky="w")

    ctk.CTkLabel(
        cabecalho,
        text="Preencha os dados para incluir um novo usuario na base",
        font=("Segoe UI", 13),
        text_color=CORES["texto_suave"],
    ).grid(row=1, column=0, sticky="w", pady=(2, 0))

    formulario = ctk.CTkFrame(
        tela_cadastro,
        fg_color=CORES["painel"],
        corner_radius=10,
        border_width=1,
        border_color=CORES["linha"],
    )
    formulario.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 18))
    formulario.grid_columnconfigure((0, 1), weight=1)

    campos = {}

    definicoes = [
        ("nome", "Nome"),
        ("sobrenome", "Sobrenome"),
        ("identidade", "Identidade"),
        ("cpf", "CPF"),
        ("uf", "UF (ex: RJ)"),
        ("cidade", "Cidade"),
        ("data_nasc", "Data de nascimento (YYYY-MM-DD)"),
    ]

    for indice, (chave, placeholder) in enumerate(definicoes):
        entrada = ctk.CTkEntry(
            formulario,
            placeholder_text=placeholder,
            height=40,
            fg_color=CORES["painel_claro"],
            border_color=CORES["linha"],
            text_color=CORES["texto"],
            placeholder_text_color=CORES["texto_suave"],
        )
        entrada.grid(
            row=indice // 2,
            column=indice % 2,
            sticky="ew",
            padx=16,
            pady=(16 if indice < 2 else 8, 8),
        )
        campos[chave] = entrada

    campos["cpf"].bind("<KeyRelease>", lambda event: aplicar_mascara(campos["cpf"], formatar_cpf))
    campos["identidade"].bind("<KeyRelease>", lambda event: aplicar_mascara(campos["identidade"], formatar_identidade))
    campos["data_nasc"].bind("<KeyRelease>", lambda event: aplicar_mascara(campos["data_nasc"], formatar_data))

    sexo_var = ctk.StringVar(value="M")

    area_sexo = ctk.CTkFrame(formulario, fg_color="transparent")
    area_sexo.grid(row=4, column=0, columnspan=2, sticky="w", padx=16, pady=(12, 8))

    ctk.CTkLabel(
        area_sexo,
        text="Sexo:",
        font=("Segoe UI", 13, "bold"),
        text_color=CORES["texto"],
    ).pack(side="left", padx=(0, 16))

    ctk.CTkRadioButton(
        area_sexo,
        text="Masculino",
        variable=sexo_var,
        value="M",
        text_color=CORES["texto"],
    ).pack(side="left", padx=(0, 20))

    ctk.CTkRadioButton(
        area_sexo,
        text="Feminino",
        variable=sexo_var,
        value="F",
        text_color=CORES["texto"],
    ).pack(side="left")

    resultado = ctk.CTkLabel(
        formulario,
        text="",
        height=24,
        font=("Segoe UI", 13),
        text_color=CORES["texto_suave"],
    )
    resultado.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=(4, 0))

    def limpar_campos():
        for entrada in campos.values():
            entrada.delete(0, "end")
        sexo_var.set("M")
        campos["nome"].focus()

    def salvar():
        try:
            conn = conectar()
            cursor = conn.cursor()

            sql = """
                INSERT INTO usuarios (
                    nome, sobrenome, identidade, cpf, uf, cidade, data_nasc, sexo
                ) VALUES (
                    :1, :2, :3, :4, :5, :6, TO_DATE(:7, 'YYYY-MM-DD'), :8
                )
            """

            dados = (
                campos["nome"].get(),
                campos["sobrenome"].get(),
                campos["identidade"].get(),
                campos["cpf"].get(),
                campos["uf"].get().upper(),
                campos["cidade"].get(),
                campos["data_nasc"].get(),
                sexo_var.get(),
            )

            cursor.execute(sql, dados)
            conn.commit()
            cursor.close()
            conn.close()

            resultado.configure(text="Usuario salvo com sucesso.", text_color=CORES["verde"])
            mostrar_mensagem(app, "Sucesso", "Usuario salvo com sucesso.", "sucesso")
            limpar_campos()

        except Exception as e:
            resultado.configure(text="Erro ao salvar usuario.", text_color=CORES["vermelho"])
            mostrar_mensagem(app, "Erro", f"Erro ao salvar:\n{e}", "erro")

    botoes = ctk.CTkFrame(formulario, fg_color="transparent")
    botoes.grid(row=6, column=0, columnspan=2, sticky="e", padx=16, pady=(18, 18))

    ctk.CTkButton(
        botoes,
        text="Limpar",
        width=120,
        height=40,
        corner_radius=8,
        fg_color=CORES["painel_claro"],
        hover_color=CORES["hover_menu"],
        text_color=CORES["texto"],
        command=limpar_campos,
    ).pack(side="left", padx=(0, 10))

    ctk.CTkButton(
        botoes,
        text="Salvar cadastro",
        width=160,
        height=40,
        corner_radius=8,
        fg_color=CORES["azul"],
        hover_color=CORES["azul_hover"],
        command=salvar,
    ).pack(side="left")

    campos["nome"].focus()


if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    ctk.set_appearance_mode("light")
    abrir_tela_cadastro(app)
    app.mainloop()
