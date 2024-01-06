"""Configuration Manager Module"""
from configparser import ConfigParser


class AppConfig:
    """Configuration Manager. Take a configuration file path and parse it with the ConfigParser module"""
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.__config = ConfigParser()
        if len(self.__config.read(self.config_file_path)) == 0:
            raise ValueError(
                f'No se pudo cargar el archivo de configuración: {self.config_file_path}')

    def get(self, section, key):
        """Get a config key value, return None if section, key not exists"""
        try:
            value = self.__config[section][key]
        except KeyError:
            value = None
        return value

    def set(self, section, key, value):
        """Set a config key value, return False if not possible"""
        try:
            self.__config[section][key] = value
            if self.__config[section][key] == value:
                with open(self.config_file_path, 'w', encoding="utf-8") as configfile:
                    self.__config.write(configfile)
                    return True
            return False
        except KeyError:
            return False
