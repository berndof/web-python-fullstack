from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Monta a pasta /dist para servir os arquivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="dist"), name="static")

# Configura o diretório de templates
templates = Jinja2Templates(directory="src")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "pages/home.html", {"request": request, "title": "Meu Projeto Frontend"}
    )
