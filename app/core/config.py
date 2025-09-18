import os
from functools import lru_cache
from typing import Any

_ALLOWED_ENVS = {"dev", "test", "prod"}

class Settings:
    def __init__(self, service_name: str, env: str, log_level: str) -> None:
        # Basic type coercion/validation (stay simple & defensive)
        if not isinstance(service_name, str) or not service_name:
            service_name = "url-shortener"

        if env not in _ALLOWED_ENVS:
            # fallback to default if invalid
            env = "dev"

        if not isinstance(log_level, str) or not log_level:
            log_level = "INFO"

        self.service_name = service_name
        self.env = env
        self.log_level = log_level

    def __repr__(self) -> str:
        return (
            f"Settings(service_name={self.service_name!r}, "
            f"env={self.env!r}, log_level={self.log_level!r})"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Settings):
            return NotImplemented
        return (
            self.service_name == other.service_name
            and self.env == other.env
            and self.log_level == other.log_level
        )

def _read_settings_from_env() -> Settings:
    service_name = os.getenv("SERVICE_NAME", "url-shortener")
    env = os.getenv("ENV", "dev")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    return Settings(service_name=service_name, env=env, log_level=log_level)

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return _read_settings_from_env()








