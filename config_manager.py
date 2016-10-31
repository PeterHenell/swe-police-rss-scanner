import configparser
import optparse
import logging


class Configuration:

    def __init__(self, config):
        self.config_dict = config

    # Allow access to the hidden dictionary in dictionary style config['key']
    def __getitem__(self, key):
        return self.config_dict[key]

    def get_int(self, key):
        return int(self.config_dict[key])


class ConfigManager:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('ConfigManager')
        handler = logging.StreamHandler()
        self.logger.addHandler(handler)

    @staticmethod
    def from_file(file_name):
        parser = optparse.OptionParser()

        parser.add_option('--config', dest='config', default=file_name)
        options, args = parser.parse_args()

        config = configparser.RawConfigParser()
        config.optionxform = str
        config.read(options.config)
        return ConfigManager(config)

    def get_config(self, key):
        return Configuration(dict(self.config.items(key)))

    def set_logging(self):
        logging_conf = self.get_config('logging')
        formatter = logging.Formatter('%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
        for h in self.logger.handlers:
            h.setFormatter(formatter)
        self.logger.setLevel(logging_conf['log_level'])


