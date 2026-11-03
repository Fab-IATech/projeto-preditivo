from fastapi.testclient import TestClient

from app.main import app

VALIDO = {
    "mean_radius": 14.1, "mean_texture": 19.3, "mean_perimeter": 91.9,
    "mean_area": 654.9, "mean_smoothness": 0.096, "mean_compactness": 0.104,
    "mean_concavity": 0.089, "mean_concave_points": 0.049,
    "mean_symmetry": 0.181, "mean_fractal_dimension": 0.063,
}


def test_health():
    with TestClient(app) as c:
        r = c.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok", "modelo_carregado": True}


def test_predict_ok():
    with TestClient(app) as c:
        r = c.post("/predict", json=VALIDO)
        assert r.status_code == 200
        assert r.json()["classe"] in ("maligno", "benigno")


def test_predict_tipo_invalido_422():
    with TestClient(app) as c:
        assert c.post("/predict", json={**VALIDO, "mean_radius": "abc"}).status_code == 422


def test_predict_fora_do_limite_422():
    with TestClient(app) as c:
        assert c.post("/predict", json={**VALIDO, "mean_radius": -5}).status_code == 422


def test_predict_campo_ausente_422():
    with TestClient(app) as c:
        d = dict(VALIDO); d.pop("mean_area")
        assert c.post("/predict", json=d).status_code == 422


def test_predict_campo_extra_422():
    with TestClient(app) as c:
        assert c.post("/predict", json={**VALIDO, "foo": 1}).status_code == 422
