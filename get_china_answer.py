import os
from dotenv import load_dotenv
load_dotenv('.venv/.env')
openAI_TOKEN = os.getenv('db_hopenAI_TOKENost')
print(openAI_TOKEN)