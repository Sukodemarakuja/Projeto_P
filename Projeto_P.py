import tkinter as tk
import sqlite3
import google.generativeai as genai
import json

# Configurar API Keys
GENAI_API_KEY = "AIzaSyC5_1X3X7e0i_XT7946bqx8DV5L3NKlegQ"
genai.configure(api_key=GENAI_API_KEY)

#CONFIGURANDO O SQLite (BASE DE DADOS DO P

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

#USANDO O GEMINI

def consultar_gemini(pergunta):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        resposta = model.generate_content(pergunta)
        return resposta.text.strip() if hasattr(resposta, 'text') else "Erro ao obter resposta do Gemini"
    except Exception as e:
        return f'Erro ao consultar Gemini: {e}'

# Funções para manipular o arquivo JSON
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

# Interface Tkinter
janela = tk.Tk()
janela.title("Projeto_P")

area_resposta = tk.Text(janela, height=10, width=50)
area_resposta.pack()

entrada_pergunta = tk.Entry(janela, width=40)
entrada_pergunta.pack()

botao_enviar = tk.Button(janela, text="Enviar")
botao_enviar.pack()


def enviar_pergunta():
    nome_usuario = "usuario_padrao" #Ou solicite o nome do usuario na primeira interação.
    pergunta = entrada_pergunta.get()

    if "meu nome é" in pergunta.lower():
        nome = pergunta.split("meu nome é")[-1].strip()
        informacoes_usuario[nome_usuario] = {"nome": nome}
        resposta = f"Olá, {nome}!"
    elif "qual é o meu nome" in pergunta.lower():
        nome = informacoes_usuario.get(nome_usuario, {}).get("nome")
        resposta = f"Seu nome é {nome}." if nome else "Desculpe, não sei seu nome."
    else:
        resposta = consultar_dados(nome_usuario, pergunta)
        if not resposta:
            resposta = consultar_gemini(pergunta)
            inserir_dados(nome_usuario, pergunta, resposta)

    area_resposta.insert(tk.END, f"Você: {pergunta}\n")
    area_resposta.insert(tk.END, f"Assistente: {resposta}\n")
    entrada_pergunta.delete(0, tk.END)
    salvar_informacoes_usuario(informacoes_usuario)

botao_enviar.config(command=enviar_pergunta)

janela.mainloop()