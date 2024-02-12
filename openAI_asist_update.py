from env.config import openAI_TOKEN, neuro_Zakupki_asst_ID
from pprint import pprint, pp, PrettyPrinter
import asyncio
from openai import OpenAI, AsyncOpenAI
# import database

client = OpenAI(api_key=openAI_TOKEN)
client_async = AsyncOpenAI(api_key=openAI_TOKEN)



assistant_files = client.beta.assistants.files.list(
  assistant_id=neuro_Zakupki_asst_ID
)

print(assistant_files)
print(client.files.list())