#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interface principal da TDG Monitoramento Eletrônico
Adiciona logomarca no topo e executa a interface gráfica do sistema de gestão.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import importlib.util

LOGO_FILE = "tdg_logo.jpeg"
GESTAO_FILE = "gestao.py"


def iniciar_interface_tdg():
    """Inicia a interface do sistema com a logo da TDG"""
    root = tk.Tk()
    root.title("TDG Monitoramento Eletrônico - Sistema de Gestão")
    root.geometry("900x600")
    root.resizable(False, False)

    # ----- ÍCONE OPCIONAL -----
    if os.path.exists(LOGO_FILE):
        try:
            root.iconphoto(False, tk.PhotoImage(file=LOGO_FILE))
        except Exception:
            pass

    # ----- LOGO NO TOPO -----
    top_frame = ttk.Frame(root, padding=10)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    if os.path.exists(LOGO_FILE):
        try:
            img = Image.open(LOGO_FILE)
            img = img.resize((260, 110), Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(top_frame, image=logo_img)
            logo_label.image = logo_img
            logo_label.pack()
        except Exception as e:
            ttk.Label(top_frame, text=f"Erro ao carregar logo: {e}", font=("Arial", 14)).pack()
    else:
        ttk.Label(top_frame, text="TDG Monitoramento Eletrônico", font=("Arial", 18, "bold")).pack()

    # ----- EXECUTAR O CÓDIGO ORIGINAL DO SISTEMA -----
    try:
        spec = importlib.util.spec_from_file_location("gestao", GESTAO_FILE)
        gestao_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gestao_module)
    except Exception as e:
        ttk.Label(root, text=f"Erro ao carregar sistema principal: {e}", foreground="red").pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    iniciar_interface_tdg()
