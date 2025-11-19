import google.generativeai as genai
from google.genai import types
from google.genai.errors import APIError

class assistant_bot:
    def __init__(self):

        self.api_key = self.read_key()
        self.model = None
        self.SYSTEM_INSTRUCTION = ("Você é um assistente informativo sobre saúde e doenças. "
    "Sua principal prioridade é fornecer respostas claras e objetivas "
    "com base em conhecimento geral de saúde. Você deve manter o contexto "
    "de mensagens anteriores para responder de forma coerente. "
    "VOCÊ DEVE SEMPRE incluir a seguinte frase no final da sua resposta: "
    "'⚠️ Lembre-se: Este projeto visa somente oferecer um diagnóstico prévio e de fácil acesso. Consulte um médico para diagnóstico preciso e tratamento correto.' ")
        self.chat = None

    def read_key(self):
        path = "api_key"
        with open(path) as f:
            return f.readline().strip("\n")

    def create_model(self):
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=self.SYSTEM_INSTRUCTION 
            )
        except Exception as e:
            print("Erro ao inicializar o cliente. Verifique sua GEMINI_API_KEY.")


    def start_chat(self, history=[]):

        try:
            self.chat = self.model.start_chat(
                history= history
            )
        except APIError as e:
            print(f"Erro na API ao iniciar o chat: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
    
    def initial_diagnosis(self, symptoms):
       
        symptoms_list = ""
        for x in range(0, len(symptoms)):
            if x == len(symptoms) - 1:
                symptoms_list += f"{symptoms[x]}."
            else:
                symptoms_list += f"{symptoms[x]}, "
        return f"Estou sentindo os seguintes sintomas: \n{symptoms_list} \n Com base nisso, faça um diagnóstico com a doença mais provável de apresentar esses sintomas, explique para mim de maneira breve qual a ligação dessa doença com os sintomas, causas e como tratar"