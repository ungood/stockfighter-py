import configparser
import getpass
import keyring
import os

config_file_name = os.path.expanduser("~/.stockfighter.cfg")

config = configparser.ConfigParser()
config.read(config_file_name)

def get_instance_id(level_name):
    return config[level_name]['InstanceId']

def prompt_password(system, account, message):
    existing_password = keyring.get_password(system, account)
    if existing_password is None:
        prompt = message + ": "
    else:
        asterisks = "*" * len(existing_password)
        prompt = "{} [{}]: ".format(message, asterisks)
    
    new_password = getpass.getpass(prompt)
    if len(new_password) > 0:
        keyring.set_password(system, account, new_password)
        print(message + " set!")
        
def get_stockfighter_api_key():
    return keyring.get_password("stockfighter", "apikey")
    
def set_stockfighter_api_key():
    prompt_password("stockfighter", "apikey", "Stockfighter API Key")

