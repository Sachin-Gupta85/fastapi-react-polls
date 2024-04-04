"""Polls API — FastAPI + MongoDB.

Create a poll with 2+ options, vote by option index, read live tallies.

Endpoints:
    GET    /api/health
    GET    /api/polls
    POST   /api/polls                     {question, options: [str, ...]}
    GET    /api/polls/{id}                poll + totals
    POST   /api/polls/{id}/vote           {option: <index>}
    DELETE /api/polls/{id}
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from .db import get_db

app = FastAPI(title="Polls API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class PollIn(BaseModel):
    question: str = Field(min_length=1, max_length=300)
    options: List[str] = Field(min_length=2, max_length=10)

    @field_validator("options")
    @classmethod
    def _clean(cls, v: List[str]) -> List[str]:
        opts = [o.strip() for o in v if o.strip()]
        if len(opts) < 2:
            raise ValueError("at least 2 non-empty options are required")
        return opts


class Vote(BaseModel):
    option: int = Field(ge=0)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ser(doc: dict) -> dict:
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    doc["total_votes"] = sum(o["votes"] for o in doc["options"])
    return doc


def _oid(pid: str) -> ObjectId:
    try:
        return ObjectId(pid)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail="poll not found")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/polls")
def list_polls(db=Depends(get_db)):
    return [_ser(d) for d in db.polls.find().sort("created_at", -1)]


@app.post("/api/polls", status_code=201)
def create_poll(poll: PollIn, db=Depends(get_db)):
    doc = {
        "question": poll.question,
        "options": [{"text": t, "votes": 0} for t in poll.options],
        "created_at": _now(),
    }
    doc["_id"] = db.polls.insert_one(doc).inserted_id
    return _ser(doc)


@app.get("/api/polls/{pid}")
def get_poll(pid: str, db=Depends(get_db)):
    doc = db.polls.find_one({"_id": _oid(pid)})
    if not doc:
        raise HTTPException(status_code=404, detail="poll not found")
    return _ser(doc)


@app.post("/api/polls/{pid}/vote")
def vote(pid: str, v: Vote, db=Depends(get_db)):
    doc = db.polls.find_one({"_id": _oid(pid)})
    if not doc:
        raise HTTPException(status_code=404, detail="poll not found")
    if v.option >= len(doc["options"]):
        raise HTTPException(status_code=400, detail="option index out of range")
    doc = db.polls.find_one_and_update(
        {"_id": doc["_id"]},
        {"$inc": {f"options.{v.option}.votes": 1}},
        return_document=True,
    )
    return _ser(doc)


@app.delete("/api/polls/{pid}", status_code=204)
def delete_poll(pid: str, db=Depends(get_db)):
    if db.polls.delete_one({"_id": _oid(pid)}).deleted_count == 0:
        raise HTTPException(status_code=404, detail="poll not found")
    return None
