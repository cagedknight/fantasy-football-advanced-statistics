# Build plan

A walkable checklist. Work top to bottom; each phase is one or more pull requests.

## Ownership

| Area | Owner |
|---|---|
| Scaffolding, CI/CD, Docker, deployment | Claude |
| Ingest plumbing, HTTP clients, retries, caching | Claude |
| API wiring, routers, serialization | Claude |
| Frontend | Claude |
| **Scoring engine, replacement level, VORP** | **Nathan** |
| **Shrinkage model, trend detection, valuation** | **Nathan** |
| **Stat reliability analysis** | **Nathan** |

For Nathan-owned work, Claude writes the type signatures and failing tests first. The
target is unambiguous and `pytest` tells you the moment you're done.

## The loop

1. Cut a branch — `feat/`, `fix/`, `docs/`, `spike/`
2. Implement, with tests
3. Run what CI runs:
   ```bash
   cd api && uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest -q
   cd web && npm run lint && npm run typecheck && npm run build
   ```
4. Push the branch, open a PR
5. CI runs; review the diff; merge
6. `git checkout main && git pull`, repeat

---

## Phase 0 — Scaffold ✅

- [x] Repo, monorepo layout, `.gitattributes`
- [x] FastAPI on Python 3.12 via uv; ruff, mypy strict, pytest
- [x] React 19 + Vite + TypeScript + TanStack Query
- [x] Dockerfile and compose for api + Postgres
- [x] CI: parallel `api` / `web` / `docker`
- [ ] **Nathan:** merge the CI badge PR
- [ ] **Nathan:** branch protection on `main` — checks `api`/`web`/`docker`, **approvals `0`**
- [ ] **Nathan:** `wsl --install`, reboot, install Docker Desktop

## Phase 1 — Data spike · `spike/data-sources`

Validates the assumption the whole NFL-first decision rests on. Cheap to falsify now,
expensive to discover in Phase 2.

- [ ] **Claude:** confirm Sleeper `/v1/players/nfl` carries `gsis_id`, `espn_id`, `yahoo_id`
- [ ] **Claude:** measure crosswalk coverage across fantasy-relevant players
- [ ] **Claude:** confirm nflverse has snap share, route participation, target share
- [ ] **Claude:** check historical depth — how many seasons for reliability work
- [ ] **Claude:** write `docs/data-sources.md` with findings

**Done when:** we know the crosswalk hit rate and which stats have usable history.
**If it fails:** reconsider MLB-first, or plan for name-based matching from the start.

## Phase 2 — Schema and ingest · `feat/schema`, `feat/ingest`

- [ ] **Claude:** Postgres via compose; SQLAlchemy 2.0 + Alembic wired
- [ ] **Claude:** migrations for `player`, `player_external_id`, `team`, `game`, stats
- [ ] **Claude:** ingest nflverse weekly stats — idempotent upserts
- [ ] **Claude:** ingest Sleeper player dictionary into `player_external_id`
- [ ] **Claude:** `ingest_run` audit table; CI runs tests against real Postgres
- [ ] **Nathan:** review the schema before it's merged — it constrains everything after

**Done when:** one command populates a database you can query.

## Phase 3 — League import · `feat/league-import`

- [ ] **Nathan:** provide your Sleeper league ID
- [ ] **Claude:** fetch league settings, rosters, users, free agent pool
- [ ] **Claude:** persist `league_scoring_rule` and `roster_slot` from league settings
- [ ] **Claude:** identity match with confidence score; unmatched go to a review queue
- [ ] **Claude:** CSV upload fallback
- [ ] **Claude:** handle team defenses and kickers — roster players with no stat-feed rows

**Done when:** your real league's free agents resolve to players with stats attached.

## Phase 4 — Scoring and VORP · `feat/scoring` — **Nathan writes this**

The first phase you own. This is the core product logic and the thing you'll be asked
about.

- [ ] **Claude:** type signatures and failing tests in `api/src/fantasy/scoring/`
- [ ] **Nathan:** `score_stat_line(stats, rules) -> float`
- [ ] **Nathan:** `replacement_rank(position, n_teams, roster_slots) -> int`
- [ ] **Nathan:** flex coupling — RB/WR/TE replacement levels are not independent
- [ ] **Nathan:** `vorp(player, league) -> float`
- [ ] **Claude:** expose it over the API once tests are green

**Done when:** your league's free agents come back ranked, and the ordering visibly
changes when you flip PPR off.

## Phase 5 — Frontend · `feat/web-league-board`

- [ ] **Claude:** generate the TypeScript client from OpenAPI; CI fails on drift
- [ ] **Claude:** league connect flow
- [ ] **Claude:** sortable free agent board with VORP
- [ ] **Claude:** player detail view
- [ ] **Claude:** one Playwright test — connect league, see rankings

**Done when:** it's demoable locally end to end.

## Phase 5b — Deploy · `chore/deploy`

Deliberately separate from Phase 5 so the demo milestone and the hosting milestone don't
collide.

- [ ] **Nathan:** sign up — Neon (Postgres, no card), Vercel (web, no card)
- [ ] **Nathan:** pick a backend host and check whether it wants a card
- [ ] **Claude:** `deploy.yml` — build, push to GHCR, migrate, deploy
- [ ] **Claude:** scheduled ingest workflow
- [ ] **Claude:** smoke test against production after each deploy
- [ ] **Nathan:** add the live URL to the top of the README

**Done when:** a stranger can click a link and use it.

## Phase 6 — The model · **Nathan writes this**

Where the project stops being CRUD. No deadline; the season is long.

- [ ] **Nathan:** split-half reliability analysis in `notebooks/`
- [ ] **Nathan:** commit derived stabilization constants as `api/src/fantasy/model/constants.yaml`
- [ ] **Nathan:** shrinkage estimator — `(observed + k * prior) / (n + k)`
- [ ] **Nathan:** EWMA on fast-stabilizing usage stats; changepoint detection on role
- [ ] **Nathan:** corroboration rule — a trend counts only if usage and efficiency agree
- [ ] **Nathan:** floor/ceiling from historical variance, age-adjusted priors
- [ ] **Nathan:** roster simulation — Δ expected wins from a swap

**Done when:** the tool tells you something the public rankings don't.

---

## Deferred

- MLB support — schema is already multi-sport; revisit in February
- Yahoo OAuth — token lifecycle, encrypted refresh tokens at rest
- ESPN — requires users to paste session cookies; security and UX cost is real
