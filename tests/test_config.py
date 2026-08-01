from assistant import config


def test_default_daily_budget_cap(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "PREFS_FILE", tmp_path / "preferences.json")
    assert config.get_daily_budget_cap() == 50000


def test_set_and_get_daily_budget_cap(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "PREFS_FILE", tmp_path / "preferences.json")
    config.set_daily_budget_cap(100)
    assert config.get_daily_budget_cap() == 100


def test_default_provider(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "PREFS_FILE", tmp_path / "preferences.json")
    assert config.get_provider() == "groq"


def test_set_and_get_provider(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "PREFS_FILE", tmp_path / "preferences.json")
    config.set_provider("openrouter")
    assert config.get_provider() == "openrouter"


def test_set_provider_rejects_invalid_value(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "PREFS_FILE", tmp_path / "preferences.json")
    try:
        config.set_provider("not_a_real_provider")
        assert False, "expected a ValueError"
    except ValueError:
        pass