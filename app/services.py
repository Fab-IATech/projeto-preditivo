"""Camada de serviço: carrega o modelo serializado e executa predições."""
from pathlib import Path

import joblib
import pandas as pd

from app.schemas import EntradaPredicao, SaidaPredicao

# Caminho relativo à raiz do projeto (sem caminhos absolutos da máquina)
CAMINHO_MODELO = Path(__file__).resolve().parent.parent / "models" / "modelo.joblib"

# Mesmos nomes de colunas usados no treino (ordem importa)
COLUNAS = list(EntradaPredicao.model_fields.keys())


class ModeloService:
    def __init__(self, caminho: Path = CAMINHO_MODELO):
        self.pipeline = joblib.load(caminho)

    def prever(self, dados: EntradaPredicao) -> SaidaPredicao:
        df = pd.DataFrame([dados.model_dump()], columns=COLUNAS)
        # No dataset original: classe 0 = maligno, 1 = benigno
        p_maligno = float(self.pipeline.predict_proba(df)[0][0])
        classe = "maligno" if p_maligno >= 0.5 else "benigno"
        return SaidaPredicao(classe=classe, probabilidade_maligno=round(p_maligno, 4))
