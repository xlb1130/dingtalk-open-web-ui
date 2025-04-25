import threading
import tomllib
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).resolve().parent.parent

PROJECT_ROOT = get_project_root()


class Config:
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._config = None
                    self._load_initial_config()
                    self._initialized = True

    @staticmethod
    def _get_config_path() -> Path:
        root = PROJECT_ROOT
        config_path = root / "config.toml"
        if config_path.exists():
            return config_path
        example_path = root / "config.example.toml"
        if example_path.exists():
            return example_path
        raise FileNotFoundError("No configuration file found in config directory")

    def _load_config(self) -> dict:
        config_path = self._get_config_path()
        with config_path.open("rb") as f:
            return tomllib.load(f)

    def _load_initial_config(self):
        raw_config = self._load_config()
        dingtalk = raw_config.get("dingtalk", {})
        
        self.dingtalk_client_id = dingtalk.get("dingtalk_client_id")
        self.dingtalk_client_secret = dingtalk.get("dingtalk_client_secret")
        self.dingtalk_template_card_id = dingtalk.get('dingtalk_template_card_id')
       
        open_web_ui = raw_config.get("open_web_ui", {})
        self.open_web_ui_api_key = open_web_ui.get("open_web_ui_api_key")
        self.open_web_ui_host = open_web_ui.get("open_web_ui_host")
        self.open_web_ui_api_timeout = open_web_ui.get("open_web_ui_api_timeout")
        self.open_web_ui_model_name = open_web_ui.get("open_web_ui_model_name")
        self.root_path = PROJECT_ROOT

config = Config()