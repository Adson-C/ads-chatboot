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

# PAGINAS ====================
# tela de login
def pag_login():
    st.header('💬 Bem-vindo ao App AJG Msg 🎈', divider=True)
    tb1, tb2 = st.tabs(['Entrar', 'Cadastrar'])

    with tb1.form(key='login'):
        nome = st.text_input('Digite seu nome de usuario')
        senha = st.text_input('Digite sua senha', type='password')
        st.form_submit_button('Entrar')

    with tb2.form(key='cadastro'):
        nome = st.text_input('Cadastre um novo usuario')
        senha = st.text_input('Cadastre uma nova senha', type='password')
        if st.form_submit_button('Cadastrar'):
            _cadastrar_usuarios(nome, senha)
        
# Cadastro
def _cadastrar_usuarios(nome, senha):
    if salvar_novos_usuarios(nome, senha):
        st.success('Cadastrado com sucesso!')
        time.sleep(1)
        st.session_state['usuario_logado'] = nome.upper()
        mudar_pagina('chat')
        st.rerun()
    else:
        st.error('Usuário já existe!')
        
# Mudar tela chat
def mudar_pagina(nome_pagina):
     st.session_state['pagina_atual'] = nome_pagina
     
    
def pagina_chat():
    st.title('💬 App AJG')
    st.divider()

    usuario_logado = st.session_state['usuario_logado']
    conversando_com = 'Giselle'
    mensagens = ler_mensagen_armazenadas(usuario_logado, conversando_com)

    for mensagem in mensagens:
        nome_usuario = 'user' if mensagem['nome_usuario'] == usuario_logado else mensagem['nome_usuario'] 
        avatar = None if mensagem['nome_usuario'] == usuario_logado else '😏'
        chat = st.chat_message(nome_usuario, avatar=avatar)
        chat.markdown(mensagem['conteudo'])


    nova_mensagem = st.chat_input('Digite uma mensagem')
    if nova_mensagem:
        nova_dic_mensagem = {'nome_usuario': usuario_logado, 'conteudo': nova_mensagem}
        chat = st.chat_message('user')
        chat.markdown(nova_dic_mensagem['conteudo'])
        mensagens.append(nova_dic_mensagem)
        armazena_mensagens(usuario_logado, conversando_com, mensagens)
# Inicialização da aplicação 
def inicializa_aplicacao():
    if not 'pagina_atual' in st.session_state:
        mudar_pagina('login')
    if not 'usuario_logado' in st.session_state:
        st.session_state['usuario_logado'] = ''
        
def main():
    inicializa_aplicacao()

    if st.session_state['pagina_atual'] == 'login':
        pag_login()
    elif st.session_state['pagina_atual'] == 'chat':
        pagina_chat()

if __name__ == '__main__':
    main()
