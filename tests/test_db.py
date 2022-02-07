from app.db import drop_db, init_db


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('app.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


def test_upload_data_command(runner, monkeypatch):
    result = runner.invoke(args=['upload-data'])
    assert 'Data was successfully uploaded' in result.output

