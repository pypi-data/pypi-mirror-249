
import importlib.metadata 
import logging
postgresql_access_logger = logging.getLogger(__name__)

__version__ =  importlib.metadata.version('postgresql_access') 

