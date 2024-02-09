from env.config import openAI_TOKEN, neuro_Zakupki_asst_ID
from openai import OpenAI
client = OpenAI(
    api_key=openAI_TOKEN
)
my_assistant = client.beta.assistants.retrieve(neuro_Zakupki_asst_ID)
# print(my_assistant)
