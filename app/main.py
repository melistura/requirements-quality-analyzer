from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.analyzer import analyze_requirements

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "results": None,
            "input_text": "",
        },
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, text: str = Form(...)):
    results = analyze_requirements(text)

    total_requirements = len(results)

    fr_count = sum(
        1 for r in results if r["type"] == "Functional Requirement"
    )
    nfr_count = sum(
        1 for r in results if r["type"] == "Non-Functional Requirement"
    )

    # Ortalama kalite puanı, her gereksinimin quality_score değerinden hesaplanır.
    average_score = 0
    if total_requirements > 0:
        average_score = round(
            sum(r.get("quality_score", 0) for r in results) / total_requirements
        )

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "results": results,
            "input_text": text,
            "total_requirements": total_requirements,
            "fr_count": fr_count,
            "nfr_count": nfr_count,
            "average_score": average_score,
        },
    )
