# from config import openAI_TOKEN, neuro_Zakupki_asst_ID
from openai import OpenAI, AsyncOpenAI
import database

import os
from dotenv import load_dotenv
load_dotenv('.venv/.env')
env_openAI_token = os.getenv('env_openAI_token')
env_openAI_neuroZakupki_asst_ID = os.getenv('env_openAI_neuroZakupki_asst_ID')

client = OpenAI(api_key=env_openAI_token)
client_async = AsyncOpenAI(api_key=env_openAI_token)

# my_assistant = client.beta.assistants.retrieve(neuro_Zakupki_asst_ID)
# print(my_assistant)


def my_openAI_connection():
    pass

def create_new_tread(user_id):
    thread_id = client.beta.threads.create()
    database.add_thread_id_to_user(user_id, thread_id.id)

# def add_user_messege_to_thread(thread_id, user_message):
#     message = client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content=user_message
#     )

# Вот бы это асинхронно запустить или как правильно*?
# run = client.beta.threads.runs.create(
#  thread_id=thread.id,
#  assistant_id=assistant.id
# )

def add_user_messege_and_run(thread_id, message):

    add_message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=env_openAI_neuroZakupki_asst_ID
    )
    # print(run)


    while run.status !="completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        # print(run.status)
        # TODO: Добавить поэтапный ответ

    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    return messages.data[0].content[0].text.value

# openAI_run(testing_thread)

# Работает, но хз как поможет
# async def main() -> None:
#     chat_completion = await client_async.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Say this is a test",
#             }
#         ],
#         model="gpt-3.5-turbo",
#     )
#
# asyncio.run(main())

