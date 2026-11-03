# Guia de entrega (não faz parte do código)

## Git — branches e commits sugeridos
```bash
git init && git branch -M main
git add .gitignore README.md requirements.txt && git commit -m "Adiciona README e requirements"
git checkout -b develop

git checkout -b feature/treino-modelo
git add notebooks models && git commit -m "Adiciona notebook de treino e modelo serializado"
git checkout develop && git merge feature/treino-modelo

git checkout -b feature/api-schemas
git add app/__init__.py app/schemas.py && git commit -m "Cria schemas Pydantic com validação de limites"
git checkout develop && git merge feature/api-schemas

git checkout -b feature/api-servico-rotas
git add app/services.py app/routers.py app/main.py && git commit -m "Implementa serviço, rotas e lifespan"
git checkout develop && git merge feature/api-servico-rotas

git checkout -b feature/testes
git add tests && git commit -m "Adiciona testes da API"
git checkout develop && git merge feature/testes

git checkout main && git merge develop
git remote add origin <URL> && git push -u origin main develop
```

## Roteiro do vídeo (máx. 10 min)
1. (1 min) Problema e objetivo; mostrar o rosto.
2. (2 min) Notebook: dados, pipeline, métricas, serialização.
3. (2 min) Estrutura modular da API e por que cada camada existe.
4. (1 min) Lifespan: modelo carregado uma vez na memória.
5. (1 min) Pydantic: Field, limites, extra="forbid"; mostrar 422 no /docs.
6. (1 min) Demo ao vivo: /health e /predict no Swagger.
7. (1 min) GitHub: branches e commits.
8. (1 min) Melhorias e limitações (ex.: usar todas as 30 features, calibração, Docker).
