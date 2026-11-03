"""Ponto de entrada da aplicação FastAPI."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import router
from app.services import ModeloService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: o modelo é carregado UMA vez, não a cada requisição
    app.state.modelo_service = ModeloService()
    yield
    # Shutdown: libera a referência
    app.state.modelo_service = None


app = FastAPI(
    title="API de Diagnóstico Preditivo (Breast Cancer Wisconsin)",
    description="Serve um pipeline scikit-learn serializado via FastAPI.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(router)
