import time
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
# routers
from .routers import token, user

app = FastAPI(title='Dex Service', docs_url='/api/docs', redoc_url=None, openapi_url='/api/openapi.json')

# middlewares section
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


app.include_router(token.router)
app.include_router(user.router)
