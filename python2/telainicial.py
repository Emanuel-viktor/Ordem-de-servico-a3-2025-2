import tkinter as tk
from PIL import Image, ImageTk
import sys
import os
import time

# ==== Permite acessar arquivos mesmo se virar EXE ====
def resource_path(rel_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)


# ==== SPLASH SCREEN ====
def show_splash(duration=1.6):
    splash = tk.Toplevel()
    splash.overrideredirect(True)

    w, h = 600, 360
    ws = splash.winfo_screenwidth()
    hs = splash.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    splash.geometry(f"{w}x{h}+{x}+{y}")

    try:
        img_path = resource_path("splash.png")
        img = Image.open(img_path).resize((w, h), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        lbl = tk.Label(splash, image=photo)
        lbl.image = photo
        lbl.pack(fill="both", expand=True)

    except Exception as e:
        print("Erro no splash:", e)
        tk.Label(
            splash,
            text="Carregando...",
            font=("Arial", 22, "bold")
        ).pack(expand=True)

    splash.update()
    time.sleep(duration)
    splash.destroy()


# ==== ABERTURA DO SISTEMA PRINCIPAL ====
def iniciar():
    import gui_gestao_com_excluir
    gui_gestao_com_excluir.App().mainloop()


# ==== TELA INICIAL ====
class TelaInicial(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TDG Monitoramento Eletrônico - Início")
        self.geometry("900x600")
        self.resizable(False, False)

        # Carrega fundo
        try:
            img_path = resource_path("os.png")
            img = Image.open(img_path)

            img_ratio = img.width / img.height
            frame_ratio = 900 / 600

            if img_ratio > frame_ratio:
                new_height = 600
                new_width = int(new_height * img_ratio)
            else:
                new_width = 900
                new_height = int(new_width / img_ratio)

            img = img.resize((new_width, new_height), Image.LANCZOS)
            self.bg = ImageTk.PhotoImage(img)

            bg_label = tk.Label(self, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        except Exception as e:
            print("Erro carregando os.png:", e)

        # Botão iniciar centralizado
        btn = tk.Button(
            self,
            text="INICIAR",
            font=("Arial", 26, "bold"),
            width=12,
            bg="#0077ff",
            fg="white",
            command=self.abrir_sistema,
            bd=0,
            activebackground="#699fe6",
            activeforeground="white"
        )
        btn.place(relx=0.5, rely=0.90, anchor="center")

    def abrir_sistema(self):
        self.destroy()
        iniciar()


# ==== EXECUÇÃO ====
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    show_splash()

    root.destroy()
    app = TelaInicial()
    app.mainloop()
