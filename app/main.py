from fastapi import Depends, FastAPI
from dotenv import load_dotenv
from app.middlewares.apikey_handle import get_api_key
from app.routes.task_routes import task_router
from app.routes.auth_routes import auth_router

app = FastAPI(title="Seek prueba tecnica API", version="1.0.0")
load_dotenv(override=True)

app.include_router(auth_router, prefix="/auth", tags=["authentication"], dependencies=[Depends(get_api_key)])
app.include_router(task_router, prefix="/tasks", tags=["tasks"], dependencies=[Depends(get_api_key)])