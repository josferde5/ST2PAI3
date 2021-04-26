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

        return cls._instances[cls]


class Config(metaclass=ConfigSingleton):
    pass
