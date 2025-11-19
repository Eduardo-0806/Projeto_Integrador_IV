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

sintomas_categorizados = {
    "Gerais/Sistêmicos": [
        "Febre", 
        "Fadiga/Cansaço", 
        "Mal-estar geral", 
        "Perda de peso inexplicada",
        "Calafrios",
        "Sudorese noturna"
    ],
    "Digestivos": [
        "Azia/Queimação", 
        "Náusea", 
        "Vômito", 
        "Diarreia", 
        "Constipação", 
        "Dor abdominal", 
        "Inchaço/Distensão abdominal", 
        "Perda de apetite"
    ],
    "Respiratórios": [
        "Tosse seca", 
        "Tosse com catarro", 
        "Falta de ar (Dispneia)", 
        "Dor no peito ao respirar", 
        "Coriza/Nariz escorrendo", 
        "Congestão nasal",
        "Espirros",
        "Dor de garganta"
    ],
    "Neurológicos": [
        "Dor de cabeça (Cefaleia)", 
        "Tontura/Vertigem", 
        "Confusão mental", 
        "Sonolência excessiva", 
        "Formigamento (Parestesia)", 
        "Fraqueza muscular", 
        "Perda de consciência/Desmaio",
        "Alteração da visão"
    ],
    "Musculoesqueléticos": [
        "Dor nas articulações (Artralgia)", 
        "Dor muscular (Mialgia)", 
        "Rigidez articular", 
        "Inchaço nas articulações", 
        "Cãibras"
    ],
    "Dermatológicos": [
        "Erupção cutânea (Rash)", 
        "Coceira (Prurido)", 
        "Vermelhidão na pele", 
        "Urticária", 
        "Pele seca",
        "Lesões na pele"
    ],
    "Cardiovasculares": [
        "Palpitações", 
        "Dor no peito (Angina)", 
        "Edema (Inchaço) nas pernas", 
        "Cansaço fácil aos esforços"
    ],
    "Oftalmológicos/Otorrinolaringológicos": [
        "Dor de ouvido (Otalgia)",
        "Zumbido",
        "Olhos vermelhos",
        "Visão turva",
        "Sensibilidade à luz (Fotofobia)",
        "Perda de olfato ou paladar"
    ]
}

if "categoria_idx" not in st.session_state:
    st.session_state.categoria_idx = 0

if "sintomas_marcados" not in st.session_state:
    st.session_state.sintomas_marcados = {cat: [] for cat in sintomas_categorizados.keys()}

if "sintomas_escolhidos" not in st.session_state:
    st.session_state.sintomas_escolhidos = ""

if "diagnostico_inicial" not in st.session_state:
    st.session_state.diagnostico_inicial = False

def prev_category():
    st.session_state.categoria_idx = (st.session_state.categoria_idx - 1) % len(sintomas_categorizados)

def next_category():
    st.session_state.categoria_idx = (st.session_state.categoria_idx + 1) % len(sintomas_categorizados)


with st.sidebar:
    st.title("Lista de Sintomas")

    col_esq, col_nome, col_dir = st.columns([1, 4, 1])

    with col_esq:
        st.button("←", key="btn_prev", on_click=prev_category)
    with col_dir:
        st.button("→", key="btn_next", on_click=next_category)

    categoria_atual = list(sintomas_categorizados.keys())[st.session_state.categoria_idx]

    
    with col_nome:
        st.markdown(
            f"<div style='text-align:center; margin-top: 6px;'>"
            f"<strong>{categoria_atual}</strong><br>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.write("")

    sintomas_selecionados = st.session_state.sintomas_marcados.get(categoria_atual, [])
    novos_selecionados = []
    for sintoma in sintomas_categorizados[categoria_atual]:
        chave = f"{categoria_atual}__{sintoma}"
        if st.checkbox(sintoma, value=(sintoma in sintomas_selecionados), key=chave):
            novos_selecionados.append(sintoma)
    st.session_state.sintomas_marcados[categoria_atual] = novos_selecionados


    if st.button("Enviar", key="btn_enviar", use_container_width=True):
        todos = []
        for lista in st.session_state.sintomas_marcados.values():
            todos.extend(lista)
        if len(todos) < 3:
            st.error("Selecione pelo menos 3 sintomas para melhor precisão do diagnóstico")
        else:
            st.session_state.sintomas_escolhidos = todos
            st.success(f"Sintomas enviados: {', '.join(todos) if todos else 'Nenhum'}")



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


if st.session_state.sintomas_escolhidos:

    prompt = st.chat_input('')


    if (not st.session_state.diagnostico_inicial):
        prompt = bot.initial_diagnosis(st.session_state.sintomas_escolhidos)
        st.session_state.diagnostico_inicial = True
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