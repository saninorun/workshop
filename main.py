import uvicorn
from fastapi import FastAPI
from workshop.api import router
from workshop.settings import settings


app = FastAPI()
app.include_router(router)

# @app.get('/')
# def root():
#     return {'message':'hello'}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        port=settings.server_port,
        host=settings.server_host,
        reload=True
    ) 