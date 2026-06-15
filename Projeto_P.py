import tkinter as tk
import sqlite3
import google.generativeai as genai
import json
import os

# --- CONFIGURAÇÃO DE SEGURANÇA (API KEY) ---
# O código agora busca a chave de forma segura no sistema operacional.
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY", "SUA_API_KEY_AQUI")
genai.configure(api_key=GENAI_API_KEY)

# --- CONFIGURANDO O SQLite (BASE DE DADOS LOCAL) ---
def conectar():
    return sqlite3.connect("assistente.db")

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
                CREATE TABLE IF NOT EXISTS memoria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT,
                    chave TEXT,
                    valor TEXT)
            ''')
    conn.commit()
    conn.close()

# Inicializa o banco de dados local
criar_tabela()

def inserir_dados(usuario, chave, valor):
    conn = conectar()
    c = conn.cursor()
    c.execute('''
                INSERT INTO memoria (usuario, chave, valor) VALUES(?,?,?)
            ''', (usuario, chave, valor))
    conn.commit()
    conn.close()

def consultar_dados(usuario, chave):
    conn = conectar()
    c = conn.cursor()
    c.execute(''' SELECT valor FROM memoria WHERE usuario = ? AND chave = ?''', (usuario, chave))
    resultado = c.fetchone()
    conn.close()
    return resultado[0] if resultado else None

# --- INTEGRAÇÃO COM A API DO GEMINI ---
def consultar_gemini(pergunta):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        resposta = model.generate_content(pergunta)
        return resposta.text.strip() if hasattr(resposta, 'text') else "Erro ao obter resposta do Gemini"
    except Exception as e:
        return f'Erro ao consultar Gemini: {e}'

# --- MANIPULAÇÃO DE ARQUIVOS JSON ---
def salvar_informacoes_usuario(informacoes):
    with open("informacoes_usuario.json", "w") as arquivo:
        json.dump(informacoes, arquivo)

def carregar_informacoes_usuario():
    try:
        with open("informacoes_usuario.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

informacoes_usuario = carregar_informacoes_usuario()

# --- INTERFACE GRÁFICA (TKINTER) ---
janela = tk.Tk()
janela.title("AI Assistant - Local Memory Project")

area_resposta = tk.Text(janela, height=15, width=60)
area_resposta.pack(pady=10)

entrada_pergunta = tk.Entry(janela, width=50)
entrada_pergunta.pack(pady=5)

botao_enviar = tk.Button(janela, text="Enviar Question")
botao_enviar.pack(pady=5)

def enviar_pergunta():
    nome_usuario = "usuario_padrao" 
    pergunta = entrada_pergunta.get()

    if not pergunta.strip():
        return

    # Regra de contexto simples via JSON
    if "meu nome é" in pergunta.lower():
        nome = pergunta.split("meu nome é")[-1].strip()
        informacoes_usuario[nome_usuario] = {"nome": nome}
        resposta = f"Olá, {nome}!"
    elif "qual é o meu nome" in pergunta.lower():
        nome = informacoes_usuario.get(nome_usuario, {}).get("nome")
        resposta = f"Seu nome é {nome}." if nome else "Desculpe, ainda não sei o seu nome."
    else:
        # Sistema de Cache: Busca primeiro no banco de dados local (SQLite)
        resposta = consultar_dados(nome_usuario, pergunta)
        if not resposta:
            # Se não encontrar localmente, consome a API do Gemini e salva o resultado
            resposta = consultar_gemini(pergunta)
            inserir_dados(nome_usuario, pergunta, resposta)

    area_resposta.insert(tk.END, f"Você: {pergunta}\n")
    area_resposta.insert(tk.END, f"Assistente: {resposta}\n\n")
    area_resposta.insert(tk.END, "-"*40 + "\n")
    entrada_pergunta.delete(0, tk.END)
    salvar_informacoes_usuario(informacoes_usuario)

botao_enviar.config(command=enviar_pergunta)

janela.mainloop()
