from assistant import router, config


def test_chooses_online_provider_when_online(tmp_path, monkeypatch):
    monkeypatch.setattr(router, "is_online", lambda: True)
    monkeypatch.setattr(config, "PREFS_FILE", tmp_path / "preferences.json")

    from assistant.tokens import USAGE_FILE
    monkeypatch.setattr("assistant.tokens.USAGE_FILE", tmp_path / "usage.json")

    assert router.choose_mode() == "groq"


def test_falls_back_to_offline_when_no_internet(tmp_path, monkeypatch):
    monkeypatch.setattr(router, "is_online", lambda: False)
    monkeypatch.setattr(router, "is_ollama_running", lambda: True)
    monkeypatch.setattr(config, "PREFS_FILE", tmp_path / "preferences.json")
    monkeypatch.setattr("assistant.tokens.USAGE_FILE", tmp_path / "usage.json")

    assert router.choose_mode() == "offline"


def test_raises_when_no_internet_and_no_ollama(tmp_path, monkeypatch):
    monkeypatch.setattr(router, "is_online", lambda: False)
    monkeypatch.setattr(router, "is_ollama_running", lambda: False)
    monkeypatch.setattr(config, "PREFS_FILE", tmp_path / "preferences.json")
    monkeypatch.setattr("assistant.tokens.USAGE_FILE", tmp_path / "usage.json")

    try:
        router.choose_mode()
        assert False, "expected a RuntimeError"
    except RuntimeError:
        pass


def test_forces_offline_when_budget_exceeded(tmp_path, monkeypatch):
    monkeypatch.setattr(router, "is_online", lambda: True)
    monkeypatch.setattr(router, "is_ollama_running", lambda: True)
    monkeypatch.setattr(config, "PREFS_FILE", tmp_path / "preferences.json")
    monkeypatch.setattr("assistant.tokens.USAGE_FILE", tmp_path / "usage.json")

    config.set_daily_budget_cap(10)
    from assistant.tokens import record_usage
    record_usage(50)

    assert router.choose_mode() == "offline"