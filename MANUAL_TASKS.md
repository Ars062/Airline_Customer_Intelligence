# MANUAL_TASKS.md

Tasks that genuinely require a human (credentials, GUI clicks, license acceptance).
Status values: PENDING / COMPLETED. Nothing below is marked COMPLETED unless actually done.

## Manual Task 1 — Dataiku DSS setup (per project spec: do NOT download automatically)

### Task
Install/configure Dataiku DSS (if desired) and build the documented visual workflow.

### Why
Requires license acceptance, account/server setup, and GUI interaction; must not be
fabricated. Project spec explicitly says not to attempt automatic download.

### Exact Steps
1. Obtain Dataiku DSS (Community/licensed edition) on a machine you control.
2. Create account/server as required by Dataiku's installer.
3. Create a new Dataiku project, e.g. `airline-customer-experience`.
4. Import `data/AirlineReviews.csv` (or `data/processed/airline_reviews_clean.csv` once built) as a dataset.
5. Build Flow: Raw Dataset → Prepare (cleaning) → Feature Engineering → NLP features
   → Train/Test split → Supervised ML (classification) → Prediction → Business output dataset.
6. Capture screenshots for `dataiku/` (flow view, preparation script, model report, prediction).

### Verification
Screenshots exist under `dataiku/` and `dataiku/README.md` describes datasets/recipes/models/metrics.

### Status
PENDING

## Manual Task 2 — Power BI dashboard build

### Task
Build the 4-page Power BI dashboard from `data/outputs/powerbi_customer_experience.csv` (to be created in Phase 7).

### Why
Power BI is a GUI product; dashboard authoring and screenshot capture cannot be automated here.

### Exact Steps
1. Open Power BI Desktop; Get Data → Text/CSV → load the Power BI output CSV (or SQLite).
2. Build pages: (1) Executive Overview, (2) Customer Experience, (3) NLP Intelligence, (4) Predictive Analytics.
3. Export screenshots to `dashboard/`.

### Verification
Screenshots present under `dashboard/` and measures match the prepared dataset.

### Status
PENDING

## Manual Task 3 — GitHub authentication / push

### Task
Authenticate to GitHub and push the local project to
`https://github.com/Ars062/Airline_Customer_Intelligence` (verified: repo exists, currently empty).

### Why
Requires human credentials/authorization. The `gh` CLI is not installed, so login + first push need you.

### Done automatically (2026-09-22)
- `git init`, branch `main`, local identity `Ars062 <arsiddique10762@gmail.com>`
- Remote `origin` set to `https://github.com/Ars062/Airline_Customer_Intelligence.git`
- `.gitignore` excludes the 117 MB raw CSV (over GitHub's 100 MB limit); audit outputs are committed
- Local commit `ecac2c5` — "Phase 1: dataset audit (129k rows x 22 cols) + project scaffold" (7 files, no secrets)

### Exact Steps (for you)
1. In a terminal inside `D:\Airline_Customer_Intelligence`, run: `git push -u origin main`
2. When prompted, sign in via the browser popup (Git Credential Manager) or with a
   Personal Access Token (GitHub → Settings → Developer settings → Tokens).
   Username: `Ars062`.
3. Refresh `https://github.com/Ars062/Airline_Customer_Intelligence` to verify files appear.

### Exact Steps
1. Create repo, `git init`, review `git status`/`git diff` for secrets.
2. Authenticate (`gh auth login` or equivalent) and push.

### Verification
Remote repo URL recorded; no secrets committed.

### Status
PENDING
