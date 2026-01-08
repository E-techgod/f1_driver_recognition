import importlib


def test_server_exposes_flask_app():
    server = importlib.import_module("server")
    assert hasattr(server, "app"), "server.py must expose `app = Flask(__name__)`"


def test_attendance_endpoint_works():
    server = importlib.import_module("server")
    client = server.app.test_client()

    payload = {"driver_name": "Max Verstappen"}
    resp = client.post("/attendance", json=payload)

    assert resp.status_code in (200, 201)
    assert resp.is_json
    assert resp.get_json().get("status") == "success"
