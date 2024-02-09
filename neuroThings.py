from env.config import openAI_TOKEN, neuro_Zakupki_asst_ID
from openai import OpenAI
import database

client = OpenAI(
    api_key=openAI_TOKEN
)
# my_assistant = client.beta.assistants.retrieve(neuro_Zakupki_asst_ID)
# print(my_assistant)


def my_openAI_connection():
    pass

def create_new_tread(user_id):
    thread_id = client.beta.threads.create()
    database.add_thread_id_to_user(user_id, thread_id.id)
    # print(thread_id)

# create_new_tread(123)


# Вот бы это асинхронно запустить или как правильно*?
# run = client.beta.threads.runs.create(
#  thread_id=thread.id,
#  assistant_id=assistant.id
# )


