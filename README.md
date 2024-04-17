# 📊 fastapi-react-polls — live polls (React + FastAPI + MongoDB)

> Create polls with multiple options and vote with live tallies. **React** (Vite) + **FastAPI** + **MongoDB**, pytest/vitest harness.

![React](https://img.shields.io/badge/React-18-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![MongoDB](https://img.shields.io/badge/MongoDB-7-47A248)
![Tests](https://img.shields.io/badge/tests-pytest%20%2B%20vitest-brightgreen)

## ✨ Features
- Create a poll with 2–10 validated options; vote by option index.
- Atomic vote increments (`$inc`) and live totals/percentages.
- Backend tested with in-memory Mongo (`mongomock`).

## 🚀 Run
```bash
docker compose up --build
cd client && npm install && npm run dev
```

## ✅ Test
```bash
./run_harness.sh                 # pytest + vitest
```

## 🔌 API
`GET /api/polls` · `POST /api/polls` · `GET /api/polls/{id}` ·
`POST /api/polls/{id}/vote` · `DELETE /api/polls/{id}`

## 📝 License
MIT — see [LICENSE](LICENSE).
