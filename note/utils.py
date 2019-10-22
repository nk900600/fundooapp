import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('fundoo.log', 'w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)