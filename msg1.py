import streamlit as st

# msg ficticia
MSG_FICT = [{'nome_usuario': 'Adson', 
            'conteudo': 'Olá Giselle'},
            {'nome_usuario': 'Giselle',
            'conteudo': 'Ola, Adson'},]

def pagina_chat():
    st.title('💬 App AJG')
    st.divider()

    if not 'mensagens' in st.session_state:
        st.session_state['mensagens'] = MSG_FICT

    mensagens = st.session_state['mensagens']
    usuario_logado = 'Adson'

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
        st.session_state['mensagens'] = mensagens

def main():
    pagina_chat()

if __name__ == '__main__':
    main()
