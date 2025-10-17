from google import genai
from google.genai import types
from google.genai.errors import APIError

class assistant_bot:

    def __init__(self):

        self.api_key = self.read_key()
        self.client = None
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

    def conect_client(self):
        try:
            self.client = genai.Client(api_key=self.api_key) 
        except Exception as e:
            print("Erro ao inicializar o cliente. Verifique sua GEMINI_API_KEY.")


    def start_chat(self, history):
        try:
            config = types.GenerateContentConfig(
                system_instruction= self.SYSTEM_INSTRUCTION
            )
            self.chat = self.client.chats.create(
                model='gemini-2.5-flash', 
                config=config,
                history= history
            )
        except APIError as e:
            print(f"Erro na API ao iniciar o chat: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
