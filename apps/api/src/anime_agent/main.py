"""Typed query API and bounded conversation over a pinned local snapshot."""
import sqlite3
from fastapi import FastAPI, Query as Parameter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from anime_agent.config import Settings
from anime_agent.conversation import build_agent
from anime_agent.history import Conflict, History, NotFound
from anime_agent.models import ActivateRequest, ConversationHistory, Filters, Query, Result, SavedTurn, TurnRequest
from anime_agent.queries import DatasetUnavailable, InvalidQuery, Repository


class Health(BaseModel):
    service: str
    status: str
    phase: int
    dataset_status: str
    conversation_status: str
    model_status: str
    mcp_status: str


def create_app(settings: Settings | None = None) -> FastAPI:
    app = FastAPI(title="Anime Data Agent", version="0.3.0")
    app.state.settings = settings or Settings.from_environment()
    app.state.repository = None
    app.state.agent = None
    app.state.history = None

    def repository():
        if app.state.repository is None:
            app.state.repository = Repository(app.state.settings.dataset_path)
        return app.state.repository

    def history():
        if app.state.history is None:
            app.state.history = History(app.state.settings.conversation_db)
        return app.state.history

    def agent():
        if app.state.agent is None:
            app.state.agent = build_agent(repository())
        return app.state.agent

    async def unavailable_handler(request, error):
        return JSONResponse(status_code=503, content={'detail': str(error)})

    async def invalid_handler(request, error):
        return JSONResponse(status_code=422, content={'detail': str(error)})

    async def conflict_handler(request, error):
        return JSONResponse(status_code=409, content={'detail': str(error)})

    async def not_found_handler(request, error):
        return JSONResponse(status_code=404, content={'detail': str(error)})

    async def storage_handler(request, error):
        return JSONResponse(status_code=503, content={'detail': 'El historial no está disponible; no se guardó un turno parcial.'})

    app.add_exception_handler(DatasetUnavailable, unavailable_handler)
    app.add_exception_handler(InvalidQuery, invalid_handler)
    app.add_exception_handler(Conflict, conflict_handler)
    app.add_exception_handler(NotFound, not_found_handler)
    app.add_exception_handler(sqlite3.Error, storage_handler)

    @app.get("/api/health", response_model=Health)
    async def health():
        try:
            repository()
            dataset_status = 'validated'
        except DatasetUnavailable:
            dataset_status = 'unavailable'
        return Health(
            service="anime-data-agent-api", status="ok", phase=5,
            dataset_status=dataset_status, conversation_status="bounded_rules",
            model_status="not_connected", mcp_status="not_implemented",
        )

    @app.get('/api/dataset')
    async def dataset():
        return repository().metadata()

    @app.post('/api/query', response_model=Result)
    async def query(body: Query):
        return repository().execute(body)

    @app.get('/api/anime/search', response_model=Result)
    async def search(title: str = Parameter(min_length=1, max_length=300), limit: int = Parameter(default=10, ge=1, le=100)):
        return repository().execute(Query(kind='search', filters=Filters(title=title), order_by='title', limit=limit))

    @app.get('/api/anime/{anime_id}', response_model=Result)
    async def detail(anime_id: int):
        if anime_id <= 0:
            raise InvalidQuery('El ID debe ser positivo.')
        if anime_id not in repository().by_id:
            raise NotFound('Anime no encontrado.')
        return repository().execute(Query(kind='detail', ids=[anime_id]))

    @app.post('/api/conversations', status_code=201, response_model=ConversationHistory)
    async def create_conversation():
        return history().create()

    @app.get('/api/conversations/{conversation_id}', response_model=ConversationHistory)
    async def get_conversation(conversation_id: str):
        return history().get(conversation_id)

    @app.post('/api/conversations/{conversation_id}/turns', response_model=SavedTurn)
    async def turn(conversation_id: str, body: TurnRequest):
        return history().append(conversation_id, body, agent())

    @app.post('/api/conversations/{conversation_id}/activate', response_model=ConversationHistory)
    async def activate(conversation_id: str, body: ActivateRequest):
        return history().activate(conversation_id, body)

    return app


app = create_app()
