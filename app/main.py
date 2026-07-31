"""TaxPilot web UI — FastAPI backend.

Run from the repository root:
    export ANTHROPIC_API_KEY=sk-ant-...   # required only for the chat
    uvicorn app.main:app --reload

Endpoints:
    GET  /                 chat UI
    POST /api/chat         question -> grounded answer with citations
    GET  /api/corpus       corpus catalogue (index.yaml)
    POST /api/upload       save a client file into clients/
    POST /api/analyze      run the CbCR structural check on an uploaded file
    GET  /api/status       API-key / corpus health
"""
import io
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

import yaml
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from app.context import system_prompt

REPO = Path(__file__).resolve().parent.parent
CLIENTS = REPO / "clients"
MODEL = os.environ.get("TAXPILOT_MODEL", "claude-sonnet-5")

app = FastAPI(title="TaxPilot")


class ChatRequest(BaseModel):
    messages: list  # [{"role": "user"|"assistant", "content": str}, ...]


@app.get("/")
def index():
    return FileResponse(REPO / "app" / "static" / "index.html")


@app.get("/api/status")
def status():
    return {
        "api_key_configured": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "model": MODEL,
        "corpus_documents": len(yaml.safe_load((REPO / "corpus" / "index.yaml").read_text(encoding="utf-8"))["documents"]),
    }


@app.get("/api/corpus")
def corpus():
    data = yaml.safe_load((REPO / "corpus" / "index.yaml").read_text(encoding="utf-8"))
    return {
        "documents": [
            {"id": d["id"], "title": d["title"], "verified": d.get("verified", False),
             "source": d.get("official_source", "")}
            for d in data["documents"]
        ],
        "secondary": [{"id": s["id"], "title": s["title"]} for s in data.get("secondary_sources", [])],
        "pending": [p["description"] for p in data.get("pending", [])],
    }


@app.post("/api/chat")
def chat(req: ChatRequest):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return JSONResponse(status_code=503, content={
            "error": "ANTHROPIC_API_KEY is not configured on the server. "
                     "Set it and restart to enable the chat."})
    import anthropic
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=[{"type": "text", "text": system_prompt(),
                 "cache_control": {"type": "ephemeral"}}],
        messages=req.messages,
    )
    return {"answer": "".join(b.text for b in response.content if b.type == "text")}


def _safe_name(name):
    return re.sub(r"[^A-Za-z0-9._ ()-]", "_", Path(name).name) or "upload.bin"


@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    dest = CLIENTS / _safe_name(file.filename)
    dest.write_bytes(await file.read())
    return {"saved_as": f"clients/{dest.name}"}


@app.post("/api/analyze")
def analyze(payload: dict):
    name = _safe_name(payload.get("filename", ""))
    fy = int(payload.get("fy", 2025))
    path = CLIENTS / name
    if not path.exists():
        return JSONResponse(status_code=404, content={"error": f"clients/{name} not found"})
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "analyze_cbcr_excel.py"), str(path), "--fy", str(fy)],
        capture_output=True, text=True, cwd=REPO, timeout=120,
    )
    return {"report": result.stdout or result.stderr}
