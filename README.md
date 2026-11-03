# API de Diagnóstico Preditivo — Breast Cancer Wisconsin

## 1. Nome e resumo do projeto
**Problema de negócio:** apoiar a triagem de tumores de mama, classificando-os como *maligno* ou *benigno* a partir de 10 medidas médias extraídas de imagens de aspirado por agulha fina.
**Solução:** um pipeline de Machine Learning (imputação + padronização + Random Forest) treinado offline, serializado com `joblib` e servido por uma **API REST FastAPI**, com validação estrita de dados via **Pydantic**.

> Projeto acadêmico (Módulo 2 – Projeto Avaliativo, Opção B). Não substitui diagnóstico médico.

## 2. Origem do modelo
**Opção B** — modelo treinado do zero em base pública: *Breast Cancer Wisconsin (Diagnostic)*, do **UCI Machine Learning Repository**, distribuída com o scikit-learn (`sklearn.datasets.load_breast_cancer`). 569 amostras; usamos as 10 features `mean_*`.
Resultados no conjunto de teste (20%, estratificado): acurácia ≈ 0,947 · F1 ≈ 0,958 · ROC-AUC ≈ 0,990.

## 3. Tecnologias utilizadas
Python 3.11 ou superior · FastAPI 0.159.1 · Uvicorn 0.54.0 · Pydantic 2.14.1 · scikit-learn 1.8.0 · pandas 3.0.2 · numpy 2.4.4 · joblib 1.5.3 · pytest 9.1.1 · httpx 0.28.1 · Jupyter Notebook

## 4. Instruções de instalação e execução
```bash
git clone <URL_DO_REPOSITORIO>
cd projeto-preditivo

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (opcional) re-treinar o modelo: executar todas as células de
# notebooks/treinamento.ipynb  -> gera models/modelo.joblib

uvicorn app.main:app --reload
```
A API sobe em `http://127.0.0.1:8000`. Testes: `pytest -q`.

## 5. Documentação da API
Swagger interativo: **http://127.0.0.1:8000/docs**

### `GET /health`
Resposta `200 OK`:
```json
{"status": "ok", "modelo_carregado": true}
```
(`503` se o modelo não estiver na memória.)

### `POST /predict`
Entrada:
```json
{
  "mean_radius": 14.1, "mean_texture": 19.3, "mean_perimeter": 91.9,
  "mean_area": 654.9, "mean_smoothness": 0.096, "mean_compactness": 0.104,
  "mean_concavity": 0.089, "mean_concave_points": 0.049,
  "mean_symmetry": 0.181, "mean_fractal_dimension": 0.063
}
```
Saída `200 OK`:
```json
{"classe": "benigno", "probabilidade_maligno": 0.295}
```
| Código | Quando |
|---|---|
| 200 | Predição realizada |
| 422 | Dado inválido: tipo errado, campo ausente/extra ou valor fora dos limites (`gt`, `ge`, `le`, `lt`) |
| 500 | Erro interno inesperado na inferência |

Exemplo:
```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" \
  -d '{"mean_radius":14.1,"mean_texture":19.3,"mean_perimeter":91.9,"mean_area":654.9,"mean_smoothness":0.096,"mean_compactness":0.104,"mean_concavity":0.089,"mean_concave_points":0.049,"mean_symmetry":0.181,"mean_fractal_dimension":0.063}'
```

## 6. Estrutura do projeto
```
projeto-preditivo/
├── app/
│   ├── main.py        # app + lifespan (carrega o modelo 1x)
│   ├── routers.py     # /health e /predict
│   ├── schemas.py     # contratos Pydantic (Field com restrições)
│   └── services.py    # carga do modelo e inferência
├── models/modelo.joblib
├── notebooks/treinamento.ipynb
├── tests/test_api.py
├── requirements.txt
└── README.md
```

## 7. Links das evidências
- Repositório GitHub: **(https://github.com/Fab-IATech/projeto-preditivo.)**
