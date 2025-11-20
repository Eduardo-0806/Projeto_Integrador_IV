import google.generativeai as genai
from google.genai import types
from google.genai.errors import APIError

class assistant_bot:
    """
    Classe Responsável Pela Criação de um Bot Assistente de Diagnóstico Baseado em Sintomas Informados. <br>
    Utiliza da API do Gemini

    :param api_key: A chave de acesso para a Api.
    :type api_key: str
    :param model: O modelo de chatbot.
    :type model: GenerativeModel
    :param SYSTEM_INSTRUCTION: Instruções para orientar o modelo.
    :type SYSTEM_INSTRUCTION: str
    :param chat: O chatbot em si.
    :type chat: chat  
    """
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
        """
        Método responsável por ler a chave para acessar a API do Gemini

        :return: A chave da API.
        :rtype: str
        """
        path = "api_key"
        with open(path) as f:
            return f.readline().strip("\n")

    def create_model(self):
        """
        Método responsável por criar o moddelo de chatbot

        :raises Exception: Se a chave da API for inválida.
        """

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=self.SYSTEM_INSTRUCTION 
            )
        except Exception as e:
            print("Erro ao inicializar o cliente. Verifique sua GEMINI_API_KEY.")


    def start_chat(self, history=[]):
        """
        Método responsável por iniciar o chat com um histórico

        :param history: O histórico que será utilizado pelo chat.
        :type history: list(str)
        :raises APIError: Se a API apresentar algum erro ao criar o chat.
        :raises Exception: Se outro erro ocorrer.
        """

        try:
            self.chat = self.model.start_chat(
                history= history
            )
        except APIError as e:
            print(f"Erro na API ao iniciar o chat: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
    
    def initial_diagnosis(self, symptoms):
        """
        Método responsável por contruir a mensagem inicial para solicitação do dianóstico baseado nos sintomas passados

        :param symptoms: A lista de sintomas passadas pelo usuário.
        :type symptoms: list(str)
        :return: A mensagem de solicitação de diagnóstico que será passado para o chat.
        :rtype: str
        """
        symptoms_list = ""
        for x in range(0, len(symptoms)):
            if x == len(symptoms) - 1:
                symptoms_list += f"{symptoms[x]}."
            else:
                symptoms_list += f"{symptoms[x]}, "
        return f"Estou sentindo os seguintes sintomas: \n{symptoms_list} \n Com base nisso, faça um diagnóstico com a doença mais provável de apresentar esses sintomas, explique para mim de maneira breve qual a ligação dessa doença com os sintomas, causas e como tratar"