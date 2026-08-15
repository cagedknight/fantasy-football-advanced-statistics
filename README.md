# Fantasy

Ranks the free agents in *your* fantasy football league by advanced stats, scored against
your league's actual rules rather than a generic consensus ranking.

A 12-team PPR superflex league and a 10-team standard league do not value the same player
the same way. Most public rankings pick one format and scale it. This computes value from
raw stat projections and your league's own scoring vector, then measures each player
against the replacement level implied by your roster settings.

> **Status:** early. The scaffold, tooling, and CI are in place; data ingest is next.
> See [Roadmap](#roadmap).

## Architecture

```
nflverse ─┐
Sleeper  ─┼─→ ingest ─→ identity resolution ─→ Postgres ─→ FastAPI ─→ React
CSV      ─┘                                                  ↑
                                                    league scoring rules
```

Nothing calls an external API on the request path. A scheduled job ingests into Postgres;
the API only ever reads local data. Player identity resolution — mapping a league's player
ids onto stat-feed ids — is the load-bearing piece, and gets a confidence score and a
manual review queue rather than silent best-effort matching.

## Quickstart

Requires [uv](https://docs.astral.sh/uv/) and Node 22+. Docker is optional until the
database lands in the next phase.

```bash
cp .env.example .env

# api → http://localhost:8000  (docs at /docs)
cd api && uv sync && uv run uvicorn fantasy.main:app --reload

# web → http://localhost:5173
cd web && npm install && npm run dev
```

The web app shows its API connection status on load, so a green line means the whole
stack is wired correctly.

With Docker, `docker compose -f infra/compose.yml up --build` brings up Postgres and the
API together.

## Layout

| Path | What lives here |
|---|---|
| `api/` | FastAPI service — routers, ingest jobs, scoring engine |
| `web/` | React + Vite + TypeScript frontend |
| `infra/` | Dockerfile and compose definition |
| `notebooks/` | Exploratory analysis; stat reliability work |
| `.github/workflows/` | CI |

## Design decisions

**Raw stat lines are stored; fantasy points never are.** Points are a function of a stat
line and a league's scoring vector. Persisting a points column would hardcode one scoring
format and make every other league wrong.

**Config comes entirely from the environment.** No host or port is hardcoded, so the same
container runs locally and in any deployment target without a code change.

**Stats are weighted by how quickly they stabilize.** Snap share and target share are
predictive within a few games; yards per carry and touchdown rate are mostly noise across
a whole season. Treating them as equally meaningful is the most common way these tools
give confidently bad advice. Constants are derived empirically in `notebooks/` rather
than guessed.

**Tests run against real Postgres, not SQLite.** SQLite accepts things Postgres rejects,
which converts test-suite passes into production failures.

**Migrations are backward compatible with the running release.** They apply before new
code goes live, so a migration that breaks the old version breaks the deploy.

## Roadmap

- [x] Scaffold, tooling, CI
- [ ] Data spike — confirm nflverse field coverage
- [ ] Schema and ingest (nflverse stats, Sleeper crosswalk)
- [ ] League import — Sleeper API and CSV fallback
- [ ] Scoring engine and VORP with flex coupling
- [ ] Frontend: league connect, free agent board
- [ ] Deploy
- [ ] Shrinkage model, role-change detection, roster simulation
- [ ] MLB support (schema is already multi-sport)
