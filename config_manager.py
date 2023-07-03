import json


class ConfigManager:
    def __init__(self, filename):
        self.filename = filename
        self._load_config()

    def _load_config(self):
        with open(self.filename, 'r') as f:
            config = json.load(f)

        self.bot_config = BotConfig(config['bot'])
        self.database_config = DatabaseConfig(config['database'])
        self.intents_config = IntentsConfig(config['intents'])
        self.authorized_users = [User(user) for user in config['authorized_users']]

    def is_debug_mode(self):
        if self.bot_config.debug or self.bot_config.debug == 'true' or self.bot_config.debug == 'True':
            return True
        elif not self.bot_config.debug or self.bot_config.debug == 'false' or self.bot_config.debug == 'False' or self.bot_config.debug == '':
            return False
        else:
            raise ValueError("Invalid debug value")


class BotConfig:
    def __init__(self, config):
        self.token = config['token']
        self.test_token = config['testToken']
        self.prefix = config['prefix']
        self.activity = config['activity']
        self.version = config['version']
        self.debug = config['debug']


class DatabaseConfig:
    def __init__(self, config):
        self.host = config['host']
        self.user = config['user']
        self.password = config['password']
        self.database = config['database']


class IntentsConfig:
    def __init__(self, config):
        self.all = config['all']
        self.members = config['members']
        self.presences = config['presences']
        self.message_content = config['message_content']


class User:
    def __init__(self, user):
        self.id = user['id']
        self.name = user['name']
