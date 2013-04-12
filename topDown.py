import logging
import config


def run():
    logging.info('Initialising')
    config = ConfigParser.ConfigParser()
    config.read('settings.conf')
    
    