from os import getenv
from dotenv import load_dotenv
load_dotenv('.venv/.env')
env_max_cache_length = getenv('env_max_cache_length')

# Ключ массива proxy_message_id это номер сообщения от нашего бота к стороннему
def memory_dict_add_new_cashe(user_chat_id, user_message_id, proxy_message_id):
    from loader import memory_msgs_ids_dict
    if len(memory_msgs_ids_dict) >= int(env_max_cache_length) : del memory_msgs_ids_dict[0] # если кэш заканчивается удаляем первого
    memory_msgs_ids_dict[proxy_message_id] = {  'user_chat_id': user_chat_id,
                                                'user_message_id': user_message_id}

# Добавляем еще один айдишник replay_bot_message_id в кэш
def memory_dict_update_replay_message_id(proxy_message_id, replay_bot_message_id):
    from loader import memory_msgs_ids_dict
    raw_dict = memory_msgs_ids_dict[proxy_message_id]
    raw_dict['replay_bot_message_id'] = replay_bot_message_id
    memory_msgs_ids_dict[proxy_message_id] = raw_dict
    if proxy_message_id in memory_msgs_ids_dict:
        memory_msgs_ids_dict[proxy_message_id]['replay_bot_message_id'] = replay_bot_message_id
        return memory_msgs_ids_dict
    else:
        return False


# Проверяем наличия в кэше сообщения наших сообщений. replay_bot_message_id может быть, а может и не быть
def memory_check_cache_replay_message_id(proxy_message_id):
    from loader import memory_msgs_ids_dict
    if proxy_message_id in memory_msgs_ids_dict:
        user_chat_id = memory_msgs_ids_dict[proxy_message_id]['user_chat_id']
        user_message_id = memory_msgs_ids_dict[proxy_message_id]['user_message_id']
        if 'replay_bot_message_id' not in memory_msgs_ids_dict[proxy_message_id]:
            replay_bot_message_id = None
        else:
            replay_bot_message_id = memory_msgs_ids_dict[proxy_message_id]['replay_bot_message_id']

        return {'user_chat_id':user_chat_id,
                "user_message_id":user_message_id,
                "replay_bot_message_id":replay_bot_message_id}
    else:
        print(f"memory_check_cache_replay_message_id  not found proxy_message_id:{proxy_message_id}")
        return False




