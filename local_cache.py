from os import getenv
from dotenv import load_dotenv
load_dotenv('.venv/.env')
env_max_cache_length = getenv('env_max_cache_length')

memory_dict = dict()


def memory_dict_add_new_cashe(user_chat_id, user_message_id, proxy_message_id):
    global memory_dict
    if len(memory_dict) >= int(env_max_cache_length) : del memory_dict[0] # если кэш заканчивается удаляем первого
    memory_dict[proxy_message_id] = {'user_chat_id': user_chat_id,
                                     'user_message_id': user_message_id}
    print(memory_dict)


def memory_check_cache_replay_message_id(reply_to_msg_id):
    global memory_dict
    if reply_to_msg_id in memory_dict:
        return {'user_chat_id':memory_dict[reply_to_msg_id]['user_chat_id'],
                "user_message_id":memory_dict[reply_to_msg_id]['user_message_id']}
    else:
        print(f"memory_check_cache_replay_message_id  not found reply_to_msg_id:{reply_to_msg_id}")
        return False





