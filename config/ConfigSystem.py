from configurator import Config
from voluptuous import Schema, All, Clamp
from loggingsystem.Logger import Logger
import json
import pathlib


class ConfigSystem:
    logger = Logger("Config")

    # Config file location
    __config_file_location = str(pathlib.Path(__file__).parent.absolute())+"/../rsc/config.json"

    # Schema to validate the config
    __schema = Schema({
        'counter': All(int, Clamp(0)),
        'text': str,
        'event': str,
        'useSmoker': bool
    })

    def __init__(self):
        # Loads the defaults
        self.__config = Config({
            'counter': 0,
            'text': 'Sie sind der %counter%, der auf %event% die Welt zerstoeren wollte.',
            'event': "der Makerfaire",
            'useSmoker': True
        })
        pass

    '''
    Initializes the config module,
    tries to load the config from it's config file
    '''

    def initialize(self):
        try:
            self.logger.debug("initialize", "Loading config from path '"+str(self.__config_file_location)+"'")

            # Tries to load the config
            self.try_add_custom(
                Config.from_path(self.__config_file_location, parser="json", optional=True)
            )
        except Exception as e:
            self.logger.error_with_exception("initialize", "Failed to load config file...", e)

    '''
    Takes in a raw object that should be a config, validates it and applies it to the current config
    :return whether or not the object was valid and got applied to the current config
    '''

    def try_add_custom(self, raw: object):
        try:
            # Tries to load the config
            custom_cfg = raw if isinstance(raw, Config) else Config(raw)

            # Tries to validate the config
            custom_cfg = self.__schema(custom_cfg.data)

            # Applies the config
            self.__config += custom_cfg
            return True
        except Exception as e:
            self.logger.error_with_exception("try_add_custom", "Failed to append config file...", e)
            return False

    '''
    Saves the current config to disk
    '''
    def save(self):
        # Saves the config file
        try:
            with open(self.__config_file_location, "w") as f:
                json.dump(self.__config.data, f)
        except Exception as e:
            self.logger.error_with_exception("save", "Failed to save file...", e)
            return False

    # Returns the config to get/edit data
    def get(self):
        return self.__config
