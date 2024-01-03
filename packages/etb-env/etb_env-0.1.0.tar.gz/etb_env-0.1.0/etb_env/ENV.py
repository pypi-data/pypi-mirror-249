import os
from dotenv import load_dotenv

class Env:
    '''provides nice central access to grab ENV vals'''

    def __init__(self):
        load_dotenv()

    def get(self, vars: list[str]) -> dict:
        '''pass list of env values to get, returns key-value mapping of env val name : value'''
        var_dict = {}

        for entry in vars:
            value = os.environ.get(entry, False)
            assert value, f'ENV value {entry} not found'

            var_dict[entry] = value

        return var_dict
    
    def get_db_auth(self) -> dict:
        '''just for ease/standardization of accessing database auth'''
        
        db_params = ["USER", "PASSWORD", "HOST", "PORT", "DATABASE"]

        return self.get(db_params)