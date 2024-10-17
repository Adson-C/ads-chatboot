from pathlib import Path
import pickle
import time

import streamlit as st
from unidecode import unidecode

from ultil import *

TEMPO_DE_RERUN = 3
# PAGINAS ====================
# tela de login
def pag_login():
    st.header('💬 Bem-vindo ao App AJG Msg 🎈', divider=True)
    tb1, tb2 = st.tabs(['Entrar', 'Cadastrar'])

    with tb1.form(key='login'):
        nome = st.text_input('Digite seu nome de usuario')
        senha = st.text_input('Digite sua senha', type='password')
        if st.form_submit_button('Entrar'):
            _login_usuarios(nome, senha)

    with tb2.form(key='cadastro'):
        nome = st.text_input('Cadastre um novo usuario')
        senha = st.text_input('Cadastre uma nova senha', type='password')
        if st.form_submit_button('Cadastrar'):
            _cadastrar_usuarios(nome, senha)
            
# Login usuarios
def _login_usuarios(nome, senha):
    if validar_senha(nome, senha):
        st.success('Login efetuado com sucesso!')
        time.sleep(1)
        st.session_state['usuario_logado'] = nome.upper()
        mudar_pagina('chat')
        st.rerun()
    else:
        st.error('Erro ao logar usuario!')
        
# Cadastro usuarios
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
    conversando_com = st.session_state['conversando_com']
    mensagens = ler_mensagen_armazenadas(usuario_logado, conversando_com)

    container = st.container()
    for mensagem in mensagens:
        nome_usuario = 'user' if mensagem['nome_usuario'] == usuario_logado else mensagem['nome_usuario'] 
        avatar = None if mensagem['nome_usuario'] == usuario_logado else '😏'
        chat = container.chat_message(nome_usuario, avatar=avatar)
        chat.markdown(mensagem['conteudo'])


    nova_mensagem = st.chat_input('Digite uma mensagem')
    if nova_mensagem:
        if nova_mensagem != st.session_state['ultima_conversa_enviada']:
            st.session_state['ultima_conversa_enviada'] = nova_mensagem
            nova_dic_mensagem = {'nome_usuario': usuario_logado, 'conteudo': nova_mensagem}
            chat = container.chat_message('user')
            chat.markdown(nova_dic_mensagem['conteudo'])
            mensagens.append(nova_dic_mensagem)
            armazena_mensagens(usuario_logado, conversando_com, mensagens)
# Inicialização da aplicação 
def inicializa_aplicacao():
    if not 'pagina_atual' in st.session_state:
        mudar_pagina('login')
    if not 'usuario_logado' in st.session_state:
        st.session_state['usuario_logado'] = ''
    if not 'conversando_com' in st.session_state:
        st.session_state['conversando_com'] = ''
    if not 'ultima_conversa_enviada' in st.session_state:
        st.session_state['ultima_conversa_enviada'] = ''    
# Pagina seleção conversa
def pagina_selecao_conversa(elemento):
    # conversas
    if not st.session_state['conversando_com'] == '':
        elemento.title(f'😏 Conversando com :green[{st.session_state["conversando_com"]}]')
        elemento.divider()
    usuarios = lista_usuarios()
    usuarios = [u for u in usuarios if u != st.session_state['usuario_logado']]
    conversando_com = elemento.selectbox('Selecione o usuário para conversar',
                                          usuarios)
    elemento.button('Iniciar conversa',
              on_click=selecionar_conversa,
              args=(conversando_com, ))
#  selecionar conversa
def selecionar_conversa(conversando_com):
    st.session_state['conversando_com'] = conversando_com
    st.success(f'Iniciando conversa com {conversando_com}')
    time.sleep(1)
    mudar_pagina('chat')
        
def main():
    inicializa_aplicacao()

    if st.session_state['pagina_atual'] == 'login':
        pag_login()
    elif st.session_state['pagina_atual'] == 'chat':
        if st.session_state['conversando_com'] == '':
            container = st.container()
            pagina_selecao_conversa(container)
        else:
            pagina_chat()
            container = st.sidebar.container()
            pagina_selecao_conversa(container)
            time.sleep(TEMPO_DE_RERUN)
            st.rerun()

if __name__ == '__main__':
    main()
