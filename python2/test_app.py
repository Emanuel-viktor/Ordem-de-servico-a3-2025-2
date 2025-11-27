import os
import sqlite3
import pytest
from gui_gestao_com_excluir import get_conn, init_db, DB_FILE



#  FIXTURE DE BANCO LIMPO

@pytest.fixture
def clean_db():
    """Remove o banco antes de cada teste para garantir ambiente limpo."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()
    yield
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)



#  TESTE: BANCO CRIA TABELAS

def test_tables_exist(clean_db):
    conn = get_conn()
    cur = conn.cursor()

    tables = [t[0] for t in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    ]

    assert "clients" in tables
    assert "technicians" in tables
    assert "orders" in tables
    assert "history" in tables

    conn.close()



#  TESTE: INSERIR CLIENTE

def test_insert_client(clean_db):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO clients (
            nome, tipo_pessoa, documento, cep, rua, numero, bairro, cidade, estado,
            ponto_referencia, email, telefone_principal, telefone_secundario,
            nome_responsavel, cpf_responsavel, tel_responsavel, tel_zelador,
            observacoes, data_cadastro, status, modalidade_atendimento
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        "Cliente Teste", "Física", "12345678900", "00000-000", "Rua X", "10", "Centro",
        "Cidade Y", "SP", "Perto de algo", "email@test.com", "1111-1111",
        "2222-2222", "Resp Teste", "12345678900", "3333-3333", "4444-4444",
        "Nenhuma", "2025-01-01 10:00:00", "Ativo", "Normal"
    ))

    conn.commit()

    cur.execute("SELECT nome FROM clients WHERE nome='Cliente Teste'")
    result = cur.fetchone()

    assert result is not None
    assert result[0] == "Cliente Teste"

    conn.close()



#  TESTE: INSERIR TÉCNICO

def test_insert_technician(clean_db):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO technicians (nome, cpf, rg, telefone, email)
        VALUES (?, ?, ?, ?, ?)
    """, ("Tecnico Teste", "11111111111", "22222222", "9999-9999", "tec@test.com"))

    conn.commit()

    cur.execute("SELECT nome FROM technicians WHERE nome='Tecnico Teste'")
    result = cur.fetchone()

    assert result is not None
    assert result[0] == "Tecnico Teste"

    conn.close()



#  TESTE: INSERIR ORDEM

def test_insert_order(clean_db):
    conn = get_conn()
    cur = conn.cursor()

    # primeiro cria cliente e técnico
    cur.execute("INSERT INTO clients (nome, tipo_pessoa, documento, data_cadastro, status) VALUES (?,?,?,?,?)",
                ("Cliente", "Física", "123", "2025", "Ativo"))
    cur.execute("INSERT INTO technicians (nome) VALUES ('Tecnico')")

    cur.execute("""
        INSERT INTO orders (cliente_id, tipo_os, data_abertura, status)
        VALUES (?, ?, ?, ?)
    """, (1, "Instalação", "2025-01-01 10:00:00", "Aberta"))

    conn.commit()

    cur.execute("SELECT tipo_os FROM orders WHERE id = 1")
    result = cur.fetchone()

    assert result is not None
    assert result[0] == "Instalação"

    conn.close()
