import logging
import os
import sys

logger = logging.getLogger(__name__)

class Essentials:
    """main.Essentials
    
    Contains out-of-the-box default logger setups.
    """
    standard_level = 'DEBUG'

    def level_setter(level: str):
        """main.Essentials.level_setter
        
        Utility method to set the log level.
        """
        if level == 'DEBUG':
            logger.setLevel(logging.DEBUG)
        elif level == 'INFO':
            logger.setLevel(logging.INFO)
        elif level == 'WARNING':
            logger.setLevel(logging.WARNING)
        elif level == 'ERROR':
            logger.setLevel(logging.ERROR)
        elif level == 'CRITICAL':
            logger.setLevel(logging.CRITICAL)
        else:
            raise ValueError(f'Invalid log level: {level}')

    @classmethod
    def gen(cls, filename: str = 'entries.log', level: str = standard_level, in_current_folder: bool = True):
        """main.Essentials.gen
        
        Simple and generalized log setup.      
        
        By default, the log file name is 'entries.log,' and it's set to debug level.
        """
        LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
        
        cls.level_setter(level)
        
        file_path = filename
        if in_current_folder:
            calling_module = sys.modules['__main__'].__file__ if '__main__' in sys.modules else sys.argv[0]
            current_path = os.path.abspath(os.path.dirname(calling_module))
            file_path = os.path.join(current_path, filename)

        file_handler = logging.FileHandler(file_path)
        console_handler = logging.StreamHandler()

        file_handler.setLevel(logging.getLevelName(level))
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))     
        console_handler.setLevel(logging.getLevelName(level))
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)