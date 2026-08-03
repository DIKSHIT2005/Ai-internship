# ScreenWise: AI Wellbeing Dashboard 🧠

```
$ whoami
> a developer tired of doomscrolling

$ screenwise --status
> [ANALYZING] 14 days of screen time data...
> [WARNING]   social media category trending upward
> [OK]        coding hours holding steady
> [COACH]     "put the phone down. go touch grass. then come back and ship."
```

## > what is this

**ScreenWise** is a Streamlit wellbeing dashboard that turns raw screen-time
data into an actual coaching conversation. It ingests a CSV of daily app
usage, visualizes the trends, and hands a clean summary to Gemini, which
plays the role of a brutal-but-fair life coach — one that gives you real,
physical-world replacements instead of empty "touch grass" platitudes.

## > stack

```
$ cat stack.txt
streamlit      → UI / dashboard framework
pandas         → data wrangling
google-genai   → Gemini API client
python-dotenv  → local secret management
```

## > run it locally

```bash
$ git clone <your-repo-url>
$ cd screenwise
$ python -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt

$ cp .env.example .env
$ vim .env   # paste in your GEMINI_API_KEY

$ streamlit run app.py
```

## > features

```
[x] 14-day synthetic screen time dataset (screentime.csv)
[x] sidebar controls: day selector + daily goal slider
[x] KPI row: total time / most used app / delta vs. goal
[x] bar chart trends across categories and days
[x] Gemini-powered coaching report (category-aware, actionable)
[x] shareable accountability link via st.query_params
```

## > deployment

```
$ streamlit deploy app.py
> deployed → https://your-app.streamlit.app
```

Set `GEMINI_API_KEY` as a secret in Streamlit Community Cloud's
**Settings → Secrets** panel (do not commit `.env`).

## > file map

```
screenwise/
├── app.py              # the whole dashboard
├── screentime.csv      # 14-day synthetic dataset
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## > license

```
$ cat LICENSE
do whatever you want, just go outside sometimes
```
