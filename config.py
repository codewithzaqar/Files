import configparser
import os

def load_config():
    """Load configuration settings from config.ini"""
    config = configparser.ConfigParser()
    defaults = {
        'use_colors': 'true',
        'history_size': '10'
    }

    if not os.path.exists('config.ini'):
        config['Settings'] = defaults
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        config.read('config.ini')

    settings = {
        'use_colors': config.getboolean('Settings', 'use_colors', fallback=True),
        'history_size': config.getint('Settings', 'history_size', fallback=10)
    }
    return settings