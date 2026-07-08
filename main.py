import customtkinter as ctk

from sistema import abrirNovaTelaSistema


CORES = {
    "fundo": "#898989",
    "painel": "#bcbcbc",
    "painel_claro": "#eeeeee",
    "linha": "#334155",
    "texto": "#1F2937",
    "texto_suave": "#1F2937",
    "azul": "#2563EB",
    "azul_hover": "#1D4ED8",
    "verde": "#16A34A",
    "vermelho": "#DC2626",
}


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)

    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def carregar_icone(caminho, tamanho=(28, 28)):
    try:
        from PIL import Image

        return ctk.CTkImage(Image.open(caminho), size=tamanho)
    except Exception:
        return None


def validar_login():
    usuario = campo_usuario.get().strip()
    senha = campo_senha.get().strip()

    if usuario == "1" and senha == "1":
        resultado_login.configure(text="")
        abrirNovaTelaSistema(app)
    else:
        resultado_login.configure(text="Usuario ou senha incorretos.", text_color=CORES["vermelho"])
        campo_senha.delete(0, "end")
        campo_usuario.focus()


def alternar_senha():
    if mostrar_senha.get():
        campo_senha.configure(show="")
    else:
        campo_senha.configure(show="*")


app = ctk.CTk()
app.title("Login - Cadastro Base")
app.configure(fg_color=CORES["fundo"])
app.resizable(False, False)

largura = 460
altura = 460
centralizar_janela(app, largura, altura)

container = ctk.CTkFrame(app, fg_color=CORES["painel"], corner_radius=12)
container.pack(fill="both", expand=True, padx=28, pady=28)

icone = carregar_icone("img/icone.png", (42, 42))

if icone:
    ctk.CTkLabel(container, text="", image=icone).pack(pady=(28, 10))

ctk.CTkLabel(
    container,
    text="Cadastro Base",
    font=("Segoe UI", 26, "bold"),
    text_color=CORES["texto"],
).pack(pady=(0, 4))

ctk.CTkLabel(
    container,
    text="Acesse o painel administrativo",
    font=("Segoe UI", 13),
    text_color=CORES["texto_suave"],
).pack(pady=(0, 26))

campo_usuario = ctk.CTkEntry(
    container,
    placeholder_text="Usuario",
    width=320,
    height=42,
    fg_color=CORES["painel_claro"],
    border_color=CORES["linha"],
    text_color=CORES["linha"],
)
campo_usuario.pack(pady=(0, 12))

campo_senha = ctk.CTkEntry(
    container,
    placeholder_text="Senha",
    width=320,
    height=42,
    show="*",
    fg_color=CORES["painel_claro"],
    border_color=CORES["linha"],
    text_color=CORES["linha"],
)
campo_senha.pack(pady=(0, 8))

mostrar_senha = ctk.BooleanVar(value=False)

ctk.CTkCheckBox(
    container,
    text="Mostrar senha",
    variable=mostrar_senha,
    command=alternar_senha,
    font=("Segoe UI", 12),
    text_color=CORES["texto_suave"],
    checkbox_width=17,
    checkbox_height=17,
).pack(anchor="w", padx=50, pady=(8, 18))

botao_login = ctk.CTkButton(
    container,
    text="Entrar",
    width=320,
    height=44,
    fg_color=CORES["azul"],
    hover_color=CORES["azul_hover"],
    font=("Segoe UI", 15, "bold"),
    command=validar_login,
)
botao_login.pack(pady=(0, 14))

resultado_login = ctk.CTkLabel(
    container,
    text="",
    height=24,
    font=("Segoe UI", 13),
)
resultado_login.pack()

ctk.CTkLabel(
    container,
    text="Use 1 / 1 para acessar",
    font=("Segoe UI", 11),
    text_color=CORES["texto_suave"],
).pack(side="bottom", pady=18)

campo_usuario.bind("<Return>", lambda event: campo_senha.focus())
campo_senha.bind("<Return>", lambda event: validar_login())
campo_usuario.focus()

app.mainloop()