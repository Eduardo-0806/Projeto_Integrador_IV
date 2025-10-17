import streamlit as st
from assistant_bot import assistant_bot
import random
from time import sleep 

def start_assistant(history):
    bot_ajuda = assistant_bot()
    bot_ajuda.conect_client()
    bot_ajuda.start_chat(history)

    return bot_ajuda

def app():
    st.header("Sistema de Diagnóstico Inicial", divider=True)

    if "historico" not in st.session_state:
        st.session_state.historico = []

    bot = start_assistant(st.session_state.historico)

    for mensagem in bot.chat.get_history():
        if mensagem.role == "model":
            role = "assistant"
        else:
            role = mensagem.role
        with st.chat_message(role):
            st.markdown(mensagem.parts[0].text)

    prompt = st.chat_input("Escreva sua duvida")
    if prompt:
        with st.chat_message('user'):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            mensagem_placeholder = st.empty()
            mensagem_placeholder.markdown("pensando")
            try:
                resposta = ''
                for chunk in bot.chat.send_message_stream(prompt):
                    contagem_palavras = 0
                    n_aleatorio = random.randint(5, 10)
                    for palavra in chunk.text:
                        resposta += palavra
                        contagem_palavras += 1
                        if contagem_palavras == n_aleatorio:
                            sleep(0.05)
                            mensagem_placeholder.markdown(resposta + '_')
                            contagem_palavras = 0
                            n_aleatorio = random.randint(5, 10)
                mensagem_placeholder.markdown(resposta)
            except Exception as e:
                print(f"Erro na geração da resposta: {e}")

app()