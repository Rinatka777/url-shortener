from app.core.config import get_settings

def _clear_cache():
    get_settings.cache_clear()

def test_defaults_when_no_env(monkeypatch):
    _clear_cache()
    monkeypatch.delenv("SERVICE_NAME", raising=False)
    monkeypatch.delenv("ENV", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    cfg = get_settings()
    assert cfg.service_name == "url-shortener"
    assert cfg.env == "dev"
    assert cfg.log_level == "INFO"

def test_env_overrides(monkeypatch):
    _clear_cache()
    monkeypatch.setenv("SERVICE_NAME", "my-app")
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    cfg = get_settings()
    assert cfg.service_name == "my-app"
    assert cfg.env == "test"
    assert cfg.log_level == "DEBUG"

def test_singleton_identity(monkeypatch):
    _clear_cache()
    monkeypatch.setenv("SERVICE_NAME", "one")
    a = get_settings()
    b = get_settings()
    assert a is b  # same object (cached)

def test_invalid_env_falls_back(monkeypatch):
    _clear_cache()
    monkeypatch.setenv("ENV", "staging")  # invalid
    cfg = get_settings()
    assert cfg.env == "dev"
