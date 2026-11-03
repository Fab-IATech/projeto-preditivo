"""Contrato de dados da API (Pydantic): entrada e saída do endpoint /predict."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EntradaPredicao(BaseModel):
    """Medidas médias extraídas de imagem de aspirado de massa mamária."""

    model_config = ConfigDict(
        extra="forbid",  # rejeita campos desconhecidos
        strict=True,     # rejeita tipos errados (ex.: "abc" no lugar de número)
        json_schema_extra={
            "example": {
                "mean_radius": 14.1,
                "mean_texture": 19.3,
                "mean_perimeter": 91.9,
                "mean_area": 654.9,
                "mean_smoothness": 0.096,
                "mean_compactness": 0.104,
                "mean_concavity": 0.089,
                "mean_concave_points": 0.049,
                "mean_symmetry": 0.181,
                "mean_fractal_dimension": 0.063,
            }
        },
    )

    mean_radius: float = Field(..., gt=0, le=50, description="Raio médio (> 0 e <= 50)")
    mean_texture: float = Field(..., gt=0, le=60, description="Textura média")
    mean_perimeter: float = Field(..., gt=0, le=300, description="Perímetro médio")
    mean_area: float = Field(..., gt=0, le=3000, description="Área média")
    mean_smoothness: float = Field(..., gt=0, lt=1, description="Suavidade média (0 a 1)")
    mean_compactness: float = Field(..., ge=0, lt=1, description="Compacidade média (0 a 1)")
    mean_concavity: float = Field(..., ge=0, lt=1, description="Concavidade média (0 a 1)")
    mean_concave_points: float = Field(..., ge=0, lt=1, description="Pontos côncavos médios (0 a 1)")
    mean_symmetry: float = Field(..., gt=0, lt=1, description="Simetria média (0 a 1)")
    mean_fractal_dimension: float = Field(..., gt=0, lt=1, description="Dimensão fractal média (0 a 1)")


class SaidaPredicao(BaseModel):
    """Resposta do endpoint /predict."""

    classe: Literal["maligno", "benigno"] = Field(..., description="Classe prevista")
    probabilidade_maligno: float = Field(..., ge=0, le=1, description="P(maligno)")


class SaudeResposta(BaseModel):
    status: Literal["ok"]
    modelo_carregado: bool
