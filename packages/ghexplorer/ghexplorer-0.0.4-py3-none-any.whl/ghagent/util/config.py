import os

from .io import set_json_value, load_json_value
from .time import validate_time

GHAGENT_HOME = os.path.expanduser("~/.ghagent")
GHARCHIVE_DIR = os.path.join(GHAGENT_HOME, "gharchive")
CONFIG_FILE_PATH = os.path.join(GHAGENT_HOME, "config.json")
LANCEDB_DIR = GHAGENT_HOME
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

class ConfigValidationError(Exception):
    def __init__(self, message: str, status_code: int):
        """
        Error code:
          1001: config file path not existed
          1002: missing timewindow
          1003: missing GitHub API Token
        """
        super().__init__(message)
        self.status_code = status_code

def get_downloaded_gharchive_dates():
    start_date = None
    end_date = None
    files = os.listdir(GHARCHIVE_DIR)
    files.sort()
    if len(files) == 0:
        return start_date, end_date

def set_time_window(start_date: str, end_date: str):
    # sanity check
    if not validate_time(start_date):
        raise ValueError(f"Invalid start date: {start_date}")
    if not validate_time(end_date):
        raise ValueError(f"Invalid end date: {end_date}")
    
    set_json_value(CONFIG_FILE_PATH, "start_date", start_date)
    set_json_value(CONFIG_FILE_PATH, "end_date", end_date)

def set_github_token(token: str):
    set_json_value(CONFIG_FILE_PATH, "github_token", token)

def config_validation_check():
    """
    Various configuration setup and setting validation
    """
    # check config file exists
    if not os.path.exists(CONFIG_FILE_PATH):
        raise ConfigValidationError("Config file not found", 1001)
    
    # check time window is set
    if not load_json_value(CONFIG_FILE_PATH, "start_date", "") or not load_json_value(CONFIG_FILE_PATH, "end_date", ""):
        raise ConfigValidationError("Time window is not set", 1002)
    
    # check GitHub token is set
    if not load_json_value(CONFIG_FILE_PATH, "github_token", ""):
        raise ConfigValidationError("Github Access Token is not set", 1003)
