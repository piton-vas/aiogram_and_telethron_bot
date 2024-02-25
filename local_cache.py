from os import getenv
from dotenv import load_dotenv
load_dotenv('.venv/.env')
env_max_cache_length = getenv('env_max_cache_length')




def memory_dict_add_new_cashe(user_chat_id, user_message_id, proxy_message_id):
    from loader import memory_msgs_ids_dict
    if len(memory_msgs_ids_dict) >= int(env_max_cache_length) : del memory_msgs_ids_dict[0] # если кэш заканчивается удаляем первого
    memory_msgs_ids_dict[proxy_message_id] = {'user_chat_id': user_chat_id,
                                     'user_message_id': user_message_id}
    print(memory_msgs_ids_dict)

def memory_dict_update_replay_message_id(proxy_message_id, replay_bot_message_id):
    from loader import memory_msgs_ids_dict
    raw_dict = memory_msgs_ids_dict[proxy_message_id]
    raw_dict['replay_bot_message_id'] = replay_bot_message_id
    print("memory_dict_update_replay_message_id")
    print(raw_dict)
    memory_msgs_ids_dict[proxy_message_id] = raw_dict

    if proxy_message_id in memory_msgs_ids_dict:
        memory_msgs_ids_dict[proxy_message_id]['replay_bot_message_id'] = replay_bot_message_id
        return memory_msgs_ids_dict
    else:
        return False



def memory_check_cache_replay_message_id(proxy_message_id):
    from loader import memory_msgs_ids_dict
    print("memory_check_cache_replay_message_id")
    print(memory_msgs_ids_dict)
    if proxy_message_id in memory_msgs_ids_dict:
        if 'replay_bot_message_id' not in memory_msgs_ids_dict[proxy_message_id]:
            replay_bot_message_id = None
        else:
            replay_bot_message_id = memory_msgs_ids_dict[proxy_message_id]['replay_bot_message_id']

        return {'user_chat_id':memory_msgs_ids_dict[proxy_message_id]['user_chat_id'],
                "user_message_id":memory_msgs_ids_dict[proxy_message_id]['user_message_id'],
                "replay_bot_message_id":replay_bot_message_id}
        print(memory_msgs_ids_dict)
    else:
        print(f"memory_check_cache_replay_message_id  not found proxy_message_id:{proxy_message_id}")
        return False




