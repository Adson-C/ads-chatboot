from pathlib import Path
import pickle
import time

import streamlit as st
from unidecode import unidecode

# GESTÃO DE ARQUIVOS ====================
PASTA_MENSAGENS = Path(__file__).parent / 'mensagens'
PASTA_MENSAGENS.mkdir(exist_ok=True)

PASTA_USUARIOS = Path(__file__).parent / 'usuarios'
PASTA_USUARIOS.mkdir(exist_ok=True)

# ler messagens armazenadas
def ler_mensagen_armazenadas(usuario, conversando_com):
    nome_arquivo = nome_arquivo_armazenado(usuario, conversando_com)
    if (PASTA_MENSAGENS / nome_arquivo).exists():
        with open(PASTA_MENSAGENS / nome_arquivo, 'rb') as f:
            return pickle.load(f)
    else:    
        return []

# salvar mensagens armazenadas
def armazena_mensagens(usuario, conversando_com, mensagens):
    nome_arquivo = nome_arquivo_armazenado(usuario, conversando_com)
    with open(PASTA_MENSAGENS / nome_arquivo, 'wb') as f:
        pickle.dump(mensagens, f)

# nome_arquivo_armazenado
def nome_arquivo_armazenado(usuario, conversando_com):
    nome_arquivo = [usuario, conversando_com]
    nome_arquivo.sort()
    nome_arquivo = [u.replace(' ', '_') for u in nome_arquivo]
    nome_arquivo = [unidecode(u) for u in nome_arquivo]
    return '&'.join(nome_arquivo).lower()
# Salvar novos usuarios
def salvar_novos_usuarios(nome, senha):
    nome_arquivo = unidecode(nome.replace(' ', '_').lower())
    if (PASTA_USUARIOS / nome_arquivo).exists():
        return False
    else:
        with open(PASTA_USUARIOS / nome_arquivo, 'wb') as f:
            pickle.dump({'nome_usuario': nome, 'senha': senha}, f)
        return True
    
# VALIDAR USUÁRIO SENHA
def validar_senha(nome, senha):
    nome_arquivo = unidecode(nome.replace(' ', '_').lower())
    if not (PASTA_USUARIOS / nome_arquivo).exists():
        return False
    else:
        with open(PASTA_USUARIOS / nome_arquivo, 'rb') as f:
            arquivo_senha = pickle.load(f)
        if arquivo_senha['senha'] == senha:
            return True
        else:
            return False
# RETORNAR LISTA USUARIOS 
def lista_usuarios():
    usuarios = list(PASTA_USUARIOS.glob("*"))
    usuarios = [u.stem.upper() for u in usuarios]
    return usuarios

