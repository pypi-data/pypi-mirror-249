from .goldenset import *
from .goldenset import _get_entity_names_of_user, _entity_name
import logging

# The httpx logs are too verbose
logging.getLogger("httpx").setLevel(logging.CRITICAL)
