# 🤖 Projeto P — Assistente Pessoal com IA

Assistente pessoal com interface gráfica integrado à API do **Google Gemini**, com sistema de memória persistente em dois níveis: cache de respostas via **SQLite** e contexto do usuário via **JSON**.

---

## ✨ Como funciona

1. Você digita uma pergunta na interface
2. O sistema verifica se já respondeu essa pergunta antes (cache local)
3. Se sim, retorna a resposta salva sem gastar chamada de API
4. Se não, consulta o Gemini, retorna a resposta e salva localmente pra próxima vez
5. Informações pessoais (como seu nome) são salvas em JSON e lembradas entre sessões

---

## 🧠 Sistema de memória

O projeto usa dois mecanismos de memória diferentes:

| Tipo | Tecnologia | O que salva |
|---|---|---|
| Cache de respostas | SQLite | Perguntas e respostas anteriores |
| Contexto do usuário | JSON | Informações pessoais (nome, preferências) |

---

## 🛠️ Tecnologias utilizadas

| Biblioteca | Função |
|---|---|
| `Tkinter` | Interface gráfica (nativa do Python) |
| `google-generativeai` | Integração com a API do Gemini |
| `SQLite3` | Banco de dados local para cache (nativo do Python) |
| `JSON` | Persistência de contexto do usuário (nativo do Python) |

---

## ⚙️ Pré-requisitos

Você vai precisar de uma **API Key do Google Gemini** — é gratuita:
1. Acesse [aistudio.google.com](https://aistudio.google.com)
2. Crie uma chave de API
3. Configure como variável de ambiente no seu sistema:

```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="sua_chave_aqui"

# Linux/Mac
export GEMINI_API_KEY="sua_chave_aqui"
```

> ⚠️ Nunca coloque sua chave diretamente no código — o projeto já está configurado para buscá-la de forma segura no ambiente.

---

## 🚀 Rodando localmente

```bash
# Clone o repositório
git clone https://github.com/Sukodemarakuja/Projeto_P
cd Projeto_P

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o projeto
python main.py
```

---

## 📁 Estrutura do projeto

```
Projeto_P/
├── main.py                    # Código principal
├── requirements.txt           # Dependências
├── assistente.db              # Banco de dados SQLite (gerado automaticamente)
├── informacoes_usuario.json   # Contexto do usuário (gerado automaticamente)
└── README.md
```

---

## 💬 Comandos especiais

| O que digitar | O que acontece |
|---|---|
| `meu nome é João` | O assistente salva seu nome e lembra nas próximas sessões |
| `qual é o meu nome` | O assistente retorna o nome salvo |
| Qualquer outra pergunta | Consulta o cache local ou o Gemini |

---

## 📌 Próximas melhorias

- [ ] Suporte a múltiplos usuários com login simples
- [ ] Histórico de conversa visível na interface
- [ ] Comando para limpar o cache local
- [ ] Normalização das perguntas no cache (evitar duplicatas por maiúsculas/minúsculas)

---

*Projeto desenvolvido por [João Henrique (Suko)](https://suko-portifolio.onrender.com) · 2026*
