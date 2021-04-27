from configparser import ConfigParser


class ConfigSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ConfigSingleton, cls).__call__(*args, **kwargs)

            config = ConfigParser()
            config.read('config.ini')

            c = config['CONFIG']

            cls.port = c.get('port', '7070')
            if cls.port == '':
                cls.port = '7070'
            cls.port = int(cls.port)

            cls.username = c.get('username', 'st2pai3')
            if cls.username == '':
                cls.username = 'st2pai3'

            cls.password = c.get('password', 'qwerty')
            if cls.password == '':
                cls.password = 'qwerty'

            cls.connections = c.get('connections', '300')
            if cls.connections == '':
                cls.connections = '300'
            cls.connections = int(cls.connections)

        return cls._instances[cls]


class Config(metaclass=ConfigSingleton):
    pass
