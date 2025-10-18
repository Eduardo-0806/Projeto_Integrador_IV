import time
import random
import streamlit as st
from assistant_bot import assistant_bot
import google.generativeai as genai

st.set_page_config(
    page_title='Assistente Saúde Diagnóstico',
    page_icon=':stethoscope:'
)

st.title('Sistema De Diagnóstico Inicial 🩺')
st.caption('Chatbot feito com Gemini')

if 'historico' not in st.session_state:
    st.session_state.historico = []

bot = assistant_bot()
bot.create_model()
bot.start_chat(history=st.session_state.historico)

for mensagem in bot.chat.history:
    if mensagem.role == 'model':
        role = 'assistant'
    else:
        role = mensagem.role
    with st.chat_message(role):
        st.markdown(mensagem.parts[0].text)

prompt = st.chat_input('')
if prompt:
    prompt = prompt.replace('\n', ' \n')
    with st.chat_message('user'):
        st.markdown(prompt)
    with st.chat_message('assistant'):
        mensagem_placeholder = st.empty()
        mensagem_placeholder.markdown('Pensando...')
        try:
            resposta = ''
            for chunk in bot.chat.send_message(prompt, stream=True):
                contagem_palavras = 0
                n_aleatorio = random.randint(5, 10)
                for palavra in chunk.text:
                    resposta += palavra
                    contagem_palavras += 1
                    if contagem_palavras == n_aleatorio:
                        time.sleep(0.05)
                        mensagem_placeholder.markdown(resposta + '_')
                        contagem_palavras = 0
                        n_aleatorio = random.randint(5, 10)
            mensagem_placeholder.markdown(resposta)
        except genai.types.generation_types.BlockedPromptException as e:
            st.exception(e)
        except Exception as e:
            st.exception(e)
        st.session_state.historico = bot.chat.history