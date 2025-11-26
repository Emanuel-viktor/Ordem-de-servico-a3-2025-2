#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Versão GUI do Sistema de Gestão (Clientes / Técnicos / Ordens de Serviço)
Interface simples e funcional usando Tkinter + SQLite (arquivo: gestao.db)
Salve como `gui_gestao.py` e execute: python gui_gestao.py

Observações:
- Interface propositalmente simples (foco em funcionalidade)
- Persistência via SQLite (mesmo esquema do CLI)
- Funcionalidades: cadastrar/listar clientes e técnicos, abrir/listar O.S., atualizar status,
  exportar CSV básico e visualizar histórico.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv
import os

# Image support (Pillow). If Pillow not installed, logo will be skipped gracefully.
try:
    from PIL import Image, ImageTk
except Exception:
    Image = None
    ImageTk = None

DB_FILE = "gestao.db"
DATE_FMT = "%Y-%m-%d %H:%M:%S"


def get_conn():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo_pessoa TEXT NOT NULL,
        documento TEXT NOT NULL,
        cep TEXT,
        rua TEXT,
        numero TEXT,
        bairro TEXT,
        cidade TEXT,
        estado TEXT,
        ponto_referencia TEXT,
        email TEXT,
        telefone_principal TEXT,
        telefone_secundario TEXT,
        nome_responsavel TEXT,
        cpf_responsavel TEXT,
        tel_responsavel TEXT,
        tel_zelador TEXT,
        observacoes TEXT,
        data_cadastro TEXT,
        status TEXT,
        modalidade_atendimento TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS technicians (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT,
        rg TEXT,
        telefone TEXT,
        email TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        tipo_os TEXT,
        data_abertura TEXT,
        data_agendamento TEXT,
        horario_previsto TEXT,
        endereco_execucao TEXT,
        titulo TEXT,
        descricao TEXT,
        tecnico_id INTEGER,
        prioridade TEXT,
        canal_origem TEXT,
        equipamentos TEXT,
        status TEXT,
        checklist TEXT,
        tempo_estimado TEXT,
        materiais TEXT,
        fotos TEXT,
        assinatura_cliente TEXT,
        assinatura_tecnico TEXT,
        observacoes_finais TEXT,
        data_encerramento TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clients(id),
        FOREIGN KEY(tecnico_id) REFERENCES technicians(id)
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        timestamp TEXT,
        evento TEXT,
        responsavel TEXT,
        detalhes TEXT,
        FOREIGN KEY(order_id) REFERENCES orders(id)
    )
    """)
    conn.commit()
    conn.close()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TDG Portaria Remota / Virtual")
        self.geometry("1000x650")

        init_db()

        # ----- Carregar logomarca TDG (uma vez) -----
        # Coloque o arquivo da logo na mesma pasta, nome exato abaixo:
        self._logo_path = "WhatsApp Image 2025-10-16 at 10.13.19.jpeg"
        self.logo_img = None
        self._load_logo_if_available()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.frame_clients = ttk.Frame(self.notebook)
        self.frame_techs = ttk.Frame(self.notebook)
        self.frame_orders = ttk.Frame(self.notebook)
        self.frame_reports = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_clients, text="Clientes")
        self.notebook.add(self.frame_techs, text="Técnicos")
        self.notebook.add(self.frame_orders, text="Ordens de Serviço")
        self.notebook.add(self.frame_reports, text="Relatórios")

        self.build_clients_tab()
        self.build_techs_tab()
        self.build_orders_tab()
        self.build_reports_tab()

    # ---------------- Logo helpers ----------------
    def _load_logo_if_available(self):
        """
        Tenta carregar e redimensionar a logo. Se Pillow não estiver disponível
        ou arquivo não existir, logo_img fica None e é ignorada.
        """
        if Image is None or ImageTk is None:
            print("Pillow não encontrado: a logomarca não será exibida. (pip install pillow para ativar)")
            return
        if not os.path.exists(self._logo_path):
            print(f"Logomarca não encontrada: {self._logo_path}")
            return
        try:
            img = Image.open(self._logo_path)
            # ajuste de tamanho - se quiser mudar, altere aqui
            img = img.resize((120, 80), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
        except Exception as e:
            print("Erro ao carregar logomarca:", e)
            self.logo_img = None

    def add_logo_to_frame(self, frame, x_offset=-10, y_offset=-10):
        """
        Adiciona a logomarca no canto inferior direito do frame passado.
        Usamos place com relx/rely para fixar no canto.
        x_offset e y_offset ajustam deslocamento a partir da borda.
        """
        if not self.logo_img:
            return
        logo_label = tk.Label(frame, image=self.logo_img, bd=0)
        logo_label.image = self.logo_img  # referência para evitar GC
        # place com anchor 'se' (southeast) => canto inferior direito
        logo_label.place(relx=1.0, rely=1.0, anchor='se', x=x_offset, y=y_offset)

    # ------------------ Clientes ------------------
    def build_clients_tab(self):
        top = ttk.Frame(self.frame_clients, padding=8)
        top.pack(side=tk.TOP, fill=tk.X)

        # Form fields (left)
        form = ttk.Frame(top)
        form.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.client_fields = {}
        labels = [
            ("Nome / Razão Social", "nome"),
            ("Tipo (Física/Jurídica)", "tipo_pessoa"),
            ("CNPJ/CPF", "documento"),
            ("CEP", "cep"),
            ("Rua", "rua"),
            ("Número", "numero"),
            ("Bairro", "bairro"),
            ("Cidade", "cidade"),
            ("Estado", "estado"),
            ("Ponto de Referência", "ponto_referencia"),
            ("E-mail", "email"),
            ("Telefone principal", "telefone_principal"),
            ("Telefone secundário", "telefone_secundario"),
            ("Nome do responsável", "nome_responsavel"),
            ("CPF do responsável", "cpf_responsavel"),
            ("Tel. do responsável", "tel_responsavel"),
            ("Tel. Zelador/Porteiro", "tel_zelador"),
            ("Observações", "observacoes"),
            ("Modalidade (opcional)", "modalidade_atendimento"),
        ]

        for i, (lab, key) in enumerate(labels):
            ttk.Label(form, text=lab).grid(row=i, column=0, sticky=tk.W, pady=2)
            e = ttk.Entry(form)
            e.grid(row=i, column=1, sticky=tk.EW, padx=4, pady=2)
            self.client_fields[key] = e

        form.columnconfigure(1, weight=1)

        # Status combobox and buttons (right)
        side = ttk.Frame(top)
        side.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Label(side, text="Status").pack(anchor=tk.W)
        self.client_status = ttk.Combobox(side, values=["Ativo", "Inativo", "Bloqueado"], state="readonly")
        self.client_status.current(0)
        self.client_status.pack(fill=tk.X, pady=4)

        ttk.Button(side, text="Cadastrar Cliente", command=self.gui_cadastrar_cliente).pack(fill=tk.X, pady=4)
        ttk.Button(side, text="Limpar Formulário", command=self.gui_limpar_form_cliente).pack(fill=tk.X, pady=4)
        ttk.Button(side, text="Exportar clientes (CSV)", command=self.gui_export_clients).pack(fill=tk.X, pady=4)

        # Treeview de listagem
        bottom = ttk.Frame(self.frame_clients, padding=8)
        bottom.pack(fill=tk.BOTH, expand=True)
        cols = ("id", "nome", "documento", "cidade", "status")
        self.tree_clients = ttk.Treeview(bottom, columns=cols, show="headings")
        for c in cols:
            self.tree_clients.heading(c, text=c.title())
            self.tree_clients.column(c, width=120)
        self.tree_clients.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.tree_clients.bind('<Double-1>', self.on_client_double)

        scrollbar = ttk.Scrollbar(bottom, orient=tk.VERTICAL, command=self.tree_clients.yview)
        self.tree_clients.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_clients()

        # adiciona logo nesta aba (sem remover nada)
        self.add_logo_to_frame(self.frame_clients)

    def gui_cadastrar_cliente(self):
        data = {k: e.get().strip() for k, e in self.client_fields.items()}
        data['status'] = self.client_status.get()
        # validação simples
        if not data['nome'] or not data['tipo_pessoa'] or not data['documento']:
            messagebox.showwarning("Atenção", "Preencha Nome, Tipo e Documento (obrigatórios).")
            return
        conn = get_conn()
        cur = conn.cursor()
        data_cad = datetime.now().strftime(DATE_FMT)
        cur.execute(
            """INSERT INTO clients (
                nome, tipo_pessoa, documento, cep, rua, numero, bairro, cidade, estado,
                ponto_referencia, email, telefone_principal, telefone_secundario,
                nome_responsavel, cpf_responsavel, tel_responsavel, tel_zelador,
                observacoes, data_cadastro, status, modalidade_atendimento
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                data['nome'], data['tipo_pessoa'], data['documento'], data['cep'], data['rua'], data['numero'],
                data['bairro'], data['cidade'], data['estado'], data['ponto_referencia'], data['email'],
                data['telefone_principal'], data['telefone_secundario'], data['nome_responsavel'],
                data['cpf_responsavel'], data['tel_responsavel'], data['tel_zelador'], data['observacoes'],
                data_cad, data['status'], data['modalidade_atendimento']
            )
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso.")
        self.refresh_clients()
        self.gui_limpar_form_cliente()

    def gui_limpar_form_cliente(self):
        for e in self.client_fields.values():
            e.delete(0, tk.END)
        self.client_status.current(0)

    def refresh_clients(self):
        for r in self.tree_clients.get_children():
            self.tree_clients.delete(r)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, documento, cidade, status FROM clients ORDER BY id DESC LIMIT 200")
        for row in cur.fetchall():
            self.tree_clients.insert('', tk.END, values=row)
        conn.close()

    def on_client_double(self, event):
        sel = self.tree_clients.selection()
        if not sel:
            return
        item = self.tree_clients.item(sel[0])
        cid = item['values'][0]
        self.show_client_detail(cid)

    def show_client_detail(self, cid):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clients WHERE id = ?", (cid,))
        row = cur.fetchone()
        conn.close()
        if not row:
            messagebox.showerror("Erro", "Cliente não encontrado.")
            return
        cols = [d[0] for d in get_conn().cursor().execute("PRAGMA table_info(clients)").fetchall()]
        text = "\n".join([f"{cols[i]}: {row[i]}" for i in range(len(row))])
        detail_win = tk.Toplevel(self)
        detail_win.title(f"Cliente {cid}")
        txt = tk.Text(detail_win, wrap=tk.WORD)
        txt.insert(tk.END, text)
        txt.config(state=tk.DISABLED)
        txt.pack(fill=tk.BOTH, expand=True)

    def gui_export_clients(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files','*.csv')], title='Salvar clientes como')
        if not path:
            return
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clients")
        rows = cur.fetchall()
        headers = [d[0] for d in cur.execute("PRAGMA table_info(clients)").fetchall()]
        conn.close()
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        messagebox.showinfo("Exportado", f"{len(rows)} clientes exportados para:\n{path}")

    # ------------------ Técnicos ------------------
    def build_techs_tab(self):
        top = ttk.Frame(self.frame_techs, padding=8)
        top.pack(side=tk.TOP, fill=tk.X)

        self.tech_fields = {}
        labels = [("Nome", "nome"), ("CPF", "cpf"), ("RG", "rg"), ("Telefone/WhatsApp", "telefone"), ("E-mail", "email")]
        for i, (lab, key) in enumerate(labels):
            ttk.Label(top, text=lab).grid(row=i, column=0, sticky=tk.W, pady=2)
            e = ttk.Entry(top)
            e.grid(row=i, column=1, sticky=tk.EW, padx=4, pady=2)
            self.tech_fields[key] = e
        top.columnconfigure(1, weight=1)
        ttk.Button(top, text="Cadastrar Técnico", command=self.gui_cadastrar_tecnico).grid(row=0, column=2, padx=8)
        ttk.Button(top, text="Limpar", command=self.gui_limpar_form_tech).grid(row=1, column=2, padx=8)

        # listagem
        bottom = ttk.Frame(self.frame_techs, padding=8)
        bottom.pack(fill=tk.BOTH, expand=True)
        cols = ("id", "nome", "cpf", "telefone")
        self.tree_techs = ttk.Treeview(bottom, columns=cols, show="headings")
        for c in cols:
            self.tree_techs.heading(c, text=c.title())
            self.tree_techs.column(c, width=150)
        self.tree_techs.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(bottom, orient=tk.VERTICAL, command=self.tree_techs.yview)
        self.tree_techs.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.refresh_techs()

        # adiciona logo nesta aba (sem remover nada)
        self.add_logo_to_frame(self.frame_techs)

    def gui_cadastrar_tecnico(self):
        data = {k: e.get().strip() for k, e in self.tech_fields.items()}
        if not data['nome']:
            messagebox.showwarning("Atenção", "Nome é obrigatório.")
            return
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO technicians (nome, cpf, rg, telefone, email) VALUES (?,?,?,?,?)",
                    (data['nome'], data['cpf'], data['rg'], data['telefone'], data['email']))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Técnico cadastrado.")
        self.gui_limpar_form_tech()
        self.refresh_techs()

    def gui_limpar_form_tech(self):
        for e in self.tech_fields.values():
            e.delete(0, tk.END)

    def refresh_techs(self):
        for r in self.tree_techs.get_children():
            self.tree_techs.delete(r)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, cpf, telefone FROM technicians ORDER BY id DESC")
        for row in cur.fetchall():
            self.tree_techs.insert('', tk.END, values=row)
        conn.close()

    # ------------------ Ordens de Serviço ------------------
    def build_orders_tab(self):
        top = ttk.Frame(self.frame_orders, padding=8)
        top.pack(side=tk.TOP, fill=tk.X)

        left = ttk.Frame(top)
        left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        right = ttk.Frame(top)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        # Fields
        self.order_fields = {}
        labels = [
            ("Cliente ID", "cliente_id"),
            ("Tipo O.S.", "tipo_os"),
            ("Data Agendamento (YYYY-MM-DD HH:MM)", "data_agendamento"),
            ("Horário previsto", "horario_previsto"),
            ("Título/Relato", "titulo"),
            ("Descrição", "descricao"),
            ("Técnico ID", "tecnico_id"),
            ("Prioridade", "prioridade"),
            ("Canal de Origem", "canal_origem"),
            ("Equipamentos (seriais)", "equipamentos"),
            ("Checklist", "checklist"),
        ]
        for i, (lab, key) in enumerate(labels):
            ttk.Label(left, text=lab).grid(row=i, column=0, sticky=tk.W, pady=2)
            if key == 'descricao':
                e = tk.Text(left, height=4)
                e.grid(row=i, column=1, sticky=tk.EW, padx=4, pady=2)
            else:
                e = ttk.Entry(left)
                e.grid(row=i, column=1, sticky=tk.EW, padx=4, pady=2)
            self.order_fields[key] = e
        left.columnconfigure(1, weight=1)

        ttk.Button(right, text="Abrir O.S.", command=self.gui_abrir_os).pack(fill=tk.X, pady=4)
        ttk.Button(right, text="Atualizar status O.S.", command=self.gui_atualizar_status_prompt).pack(fill=tk.X, pady=4)
        ttk.Button(right, text="Exportar O.S. (CSV)", command=self.gui_export_orders).pack(fill=tk.X, pady=4)

        # treeview
        bottom = ttk.Frame(self.frame_orders, padding=8)
        bottom.pack(fill=tk.BOTH, expand=True)
        cols = ("id", "cliente", "tipo", "data_abertura", "prioridade", "status")
        self.tree_orders = ttk.Treeview(bottom, columns=cols, show="headings")
        for c in cols:
            self.tree_orders.heading(c, text=c.title())
            self.tree_orders.column(c, width=140)
        self.tree_orders.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.tree_orders.bind('<Double-1>', self.on_order_double)
        scrollbar = ttk.Scrollbar(bottom, orient=tk.VERTICAL, command=self.tree_orders.yview)
        self.tree_orders.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_orders()

        # adiciona logo nesta aba (sem remover nada)
        self.add_logo_to_frame(self.frame_orders)

    def gui_abrir_os(self):
        # coletar dados
        def get_val(key):
            w = self.order_fields[key]
            if isinstance(w, tk.Text):
                return w.get('1.0', tk.END).strip()
            return w.get().strip()

        cliente_id = get_val('cliente_id')
        tipo_os = get_val('tipo_os')
        titulo = get_val('titulo')
        descricao = get_val('descricao')
        if not cliente_id or not tipo_os or not titulo:
            messagebox.showwarning("Atenção", "Preencha Cliente ID, Tipo O.S. e Título (obrigatório).")
            return
        data_ag = get_val('data_agendamento')
        horario_prev = get_val('horario_previsto')
        endereco_exec = self.get_endereco_cliente(cliente_id)
        tecnico_id = get_val('tecnico_id')
        prioridade = get_val('prioridade') or 'Média'
        canal = get_val('canal_origem') or 'Telefone'
        equipamentos = get_val('equipamentos')
        checklist = get_val('checklist')

        conn = get_conn()
        cur = conn.cursor()
        data_ab = datetime.now().strftime(DATE_FMT)
        cur.execute(
            """INSERT INTO orders (
                cliente_id, tipo_os, data_abertura, data_agendamento, horario_previsto, endereco_execucao,
                titulo, descricao, tecnico_id, prioridade, canal_origem, equipamentos, status, checklist
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (cliente_id, tipo_os, data_ab, data_ag, horario_prev, endereco_exec, titulo, descricao,
             tecnico_id if tecnico_id else None, prioridade, canal, equipamentos, 'Aberta', checklist)
        )
        os_id = cur.lastrowid
        cur.execute("INSERT INTO history (order_id, timestamp, evento, responsavel, detalhes) VALUES (?,?,?,?,?)",
                    (os_id, datetime.now().strftime(DATE_FMT), 'Abertura', 'Sistema', f'O.S. aberta: {titulo}'))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", f"O.S. criada com número: {os_id}")
        self.refresh_orders()
        # limpar campos
        for w in self.order_fields.values():
            if isinstance(w, tk.Text):
                w.delete('1.0', tk.END)
            else:
                w.delete(0, tk.END)

    def get_endereco_cliente(self, cliente_id):
        try:
            cid = int(cliente_id)
        except Exception:
            return ''
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT rua, numero, bairro, cidade, estado FROM clients WHERE id = ?", (cid,))
        r = cur.fetchone()
        conn.close()
        if r:
            return ", ".join([p for p in r if p])
        return ''

    def refresh_orders(self):
        for r in self.tree_orders.get_children():
            self.tree_orders.delete(r)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT o.id, c.nome, o.tipo_os, o.data_abertura, o.prioridade, o.status FROM orders o LEFT JOIN clients c ON o.cliente_id = c.id ORDER BY o.id DESC LIMIT 300")
        for row in cur.fetchall():
            self.tree_orders.insert('', tk.END, values=row)
        conn.close()

    def on_order_double(self, event):
        sel = self.tree_orders.selection()
        if not sel:
            return
        item = self.tree_orders.item(sel[0])
        oid = item['values'][0]
        self.show_order_detail(oid)

    def show_order_detail(self, oid):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE id = ?", (oid,))
        row = cur.fetchone()
        cur.execute("SELECT timestamp, evento, responsavel, detalhes FROM history WHERE order_id = ? ORDER BY id", (oid,))
        hist = cur.fetchall()
        conn.close()
        cols = [d[0] for d in get_conn().cursor().execute("PRAGMA table_info(orders)").fetchall()]
        text = "\n".join([f"{cols[i]}: {row[i]}" for i in range(len(row))])
        if hist:
            text += "\n\n--- Histórico ---\n"
            text += "\n".join([f"{h[0]} | {h[1]} | {h[2]} | {h[3]}" for h in hist])
        detail_win = tk.Toplevel(self)
        detail_win.title(f"O.S. {oid}")
        txt = tk.Text(detail_win, wrap=tk.WORD)
        txt.insert(tk.END, text)
        txt.config(state=tk.DISABLED)
        txt.pack(fill=tk.BOTH, expand=True)

    def gui_atualizar_status_prompt(self):
        def do_update():
            oid = entry_oid.get().strip()
            novo = combo.get().strip()
            if not oid or not novo:
                messagebox.showwarning("Atenção", "Preencha número da O.S. e novo status.")
                return
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT id FROM orders WHERE id = ?", (oid,))
            if not cur.fetchone():
                messagebox.showerror("Erro", "O.S. não encontrada.")
                conn.close()
                return
            cur.execute("UPDATE orders SET status = ? WHERE id = ?", (novo, oid))
            cur.execute("INSERT INTO history (order_id, timestamp, evento, responsavel, detalhes) VALUES (?,?,?,?,?)",
                        (oid, datetime.now().strftime(DATE_FMT), f"Status alterado para {novo}", 'Operador', ''))
            if novo == 'Concluída':
                cur.execute("UPDATE orders SET data_encerramento = ? WHERE id = ?", (datetime.now().strftime(DATE_FMT), oid))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Status atualizado.")
            win.destroy()
            self.refresh_orders()

        win = tk.Toplevel(self)
        win.title("Atualizar status O.S.")
        ttk.Label(win, text="Número da O.S.").pack(padx=8, pady=4)
        entry_oid = ttk.Entry(win)
        entry_oid.pack(fill=tk.X, padx=8)
        ttk.Label(win, text="Novo status").pack(padx=8, pady=4)
        combo = ttk.Combobox(win, values=["Aberta", "Em andamento", "Pendente", "Concluída", "Cancelada"], state='readonly')
        combo.pack(fill=tk.X, padx=8)
        ttk.Button(win, text="Atualizar", command=do_update).pack(padx=8, pady=8)

    def gui_export_orders(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files','*.csv')], title='Salvar O.S. como')
        if not path:
            return
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders")
        rows = cur.fetchall()
        headers = [d[0] for d in cur.execute("PRAGMA table_info(orders)").fetchall()]
        conn.close()
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        messagebox.showinfo("Exportado", f"{len(rows)} O.S. exportadas para:\n{path}")

    # ------------------ Relatórios ------------------
    def build_reports_tab(self):
        f = ttk.Frame(self.frame_reports, padding=8)
        f.pack(fill=tk.BOTH, expand=True)
        ttk.Button(f, text="Relatório: quantidade de O.S. por status", command=self.report_os_by_status).pack(fill=tk.X, pady=4)
        ttk.Button(f, text="Relatório: desempenho por técnico", command=self.report_performance_by_tech).pack(fill=tk.X, pady=4)
        ttk.Button(f, text="Histórico de um cliente (por ID)", command=self.gui_historico_cliente_prompt).pack(fill=tk.X, pady=4)

        self.report_box = tk.Text(f, height=20)
        self.report_box.pack(fill=tk.BOTH, expand=True, pady=8)

        # adiciona logo nesta aba (sem remover nada)
        self.add_logo_to_frame(self.frame_reports)

    def report_os_by_status(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT status, COUNT(*) FROM orders GROUP BY status")
        rows = cur.fetchall()
        conn.close()
        text = "Relatório - O.S. por status:\n\n"
        for s, c in rows:
            text += f"{s}: {c}\n"
        self.report_box.delete('1.0', tk.END)
        self.report_box.insert(tk.END, text)

    def report_performance_by_tech(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT t.id, t.nome,
              COUNT(o.id) as total_os,
              AVG((julianday(o.data_encerramento) - julianday(o.data_abertura)) * 24) as horas_medias
            FROM technicians t
            LEFT JOIN orders o ON o.tecnico_id = t.id AND o.data_encerramento IS NOT NULL
            GROUP BY t.id
            ORDER BY total_os DESC
        """)
        rows = cur.fetchall()
        conn.close()
        text = "Relatório - desempenho por técnico:\n\n"
        text += "ID | Nome | Total O.S. concluídas | Horas médias (aprox)\n"
        for r in rows:
            text += f"{r[0]} | {r[1]} | {r[2]} | {round(r[3] or 0,2)}\n"
        self.report_box.delete('1.0', tk.END)
        self.report_box.insert(tk.END, text)

    def gui_historico_cliente_prompt(self):
        def do_show():
            cid = entry.get().strip()
            if not cid:
                messagebox.showwarning("Atenção", "Informe ID do cliente.")
                return
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT o.id, o.tipo_os, o.data_abertura, o.data_encerramento, o.status, o.titulo FROM orders o WHERE o.cliente_id = ? ORDER BY o.id DESC", (cid,))
            rows = cur.fetchall()
            conn.close()
            text = f"Histórico de atendimentos do cliente {cid}:\n\n"
            if not rows:
                text += "Nenhuma O.S. encontrada.\n"
            else:
                for r in rows:
                    text += f"Nº:{r[0]} | Tipo:{r[1]} | Aberta:{r[2]} | Encerrada:{r[3]} | Status:{r[4]} | Título:{r[5]}\n"
            self.report_box.delete('1.0', tk.END)
            self.report_box.insert(tk.END, text)
            win.destroy()

        win = tk.Toplevel(self)
        win.title("Histórico por cliente")
        ttk.Label(win, text="ID do cliente").pack(padx=8, pady=4)
        entry = ttk.Entry(win)
        entry.pack(fill=tk.X, padx=8)
        ttk.Button(win, text="Mostrar", command=do_show).pack(padx=8, pady=8)


if __name__ == '__main__':
    app = App()
    app.mainloop()
