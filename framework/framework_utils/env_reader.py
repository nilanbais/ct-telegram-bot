
import os
import json
from abc import ABC

import dotenv

PROJECT_NAME = 'ct-telegram-bot'

def get_project_root(os_cwd: str) -> str:
    splitted_path = os_cwd.split('\\' or '/')
    # Direction -> 1 = somewhere in project, 0 = search rest of path
    project_name_in_path = False if all([x != PROJECT_NAME for x in splitted_path]) else True

    if project_name_in_path:

        index = len(splitted_path)
        keep_going = True
        while keep_going:
            if index < 0:
                print("index < 0")
                break

            build_path = os.path.sep.join(splitted_path[:index])
            if build_path.endswith(PROJECT_NAME):
                keep_going = False
                return build_path
            
            index -= 1
    else:
        # todo: functie schrijven voor wanneer dit gebeurt
        pass
         
def get_env_folder_path() -> str:
    project_root = get_project_root(os_cwd=os.getcwd())
    return os.path.join(project_root, 'env')



class VarReaderBase(ABC):

    def __init__(self, env_file: str) -> None:
        self.env_file:str = env_file
        self.project_root:str = get_env_folder_path()
    
    @property
    def _config(self) -> dict:
        return dotenv.dotenv_values(os.path.join(self.project_root, self.env_file))
            

    def get_value(self, variable_name: str) -> str:
        return self._config[variable_name]


class DBVarReader(VarReaderBase):
    def __init__(self) -> None:
        super().__init__(env_file='db.env')


class APIVarReader(VarReaderBase):
    def __init__(self) -> None:
        super().__init__(env_file='api.env')


class BotVarReader(VarReaderBase):
    def __init__(self) -> None:
        super().__init__(env_file='bot.env')

class TwitterVarReader(VarReaderBase):
    def __init__(self) -> None:
        super().__init__(env_file='twitter.env')



class EnvVarReader:

    def get_value(self, variable_name: str) -> str:
        reader_object:VarReaderBase = self._get_reader_object(variable_name)
        return reader_object.get_value(variable_name)

    def _get_reader_object(self, variable_name: str) -> VarReaderBase:
        var_prefix = variable_name.split("_")[0]
        match var_prefix.lower():
            case 'bot':
                return BotVarReader()
            case 'db':
                return DBVarReader()
            case 'api':
                return APIVarReader()
            case 'twitter':
                return TwitterVarReader()


USERS_COLLECTION = EnvVarReader().get_value('DB_USERS_COLLECTION')
CRYPTO_COLLECTION = EnvVarReader().get_value('DB_CRYPTO_COLLECTION')
RAPORTS_COLLECTION = EnvVarReader().get_value('DB_RAPORTS_COLLECTION')
