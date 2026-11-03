"""Rotas HTTP da API."""
import logging

from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import EntradaPredicao, SaidaPredicao, SaudeResposta

logger = logging.getLogger("api")
router = APIRouter()


def _servico(request: Request):
    servico = getattr(request.app.state, "modelo_service", None)
    if servico is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo não carregado na memória.",
        )
    return servico


@router.get("/health", response_model=SaudeResposta, tags=["monitoramento"])
def health(request: Request):
    """Verifica se a API está de pé e o modelo está na memória."""
    _servico(request)
    return SaudeResposta(status="ok", modelo_carregado=True)


@router.post("/predict", response_model=SaidaPredicao, tags=["inferência"])
def predict(dados: EntradaPredicao, request: Request):
    """Recebe as medidas e devolve a classe prevista.

    Dados inválidos são barrados pelo Pydantic com HTTP 422.
    """
    servico = _servico(request)
    try:
        return servico.prever(dados)
    except Exception:
        logger.exception("Falha na inferência")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao executar a predição.",
        )
