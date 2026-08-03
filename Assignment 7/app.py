"""
ScreenWise :: AI Wellbeing Dashboard
A Streamlit dashboard that visualizes screen time data and uses the
Gemini API to deliver a brutal-but-fair productivity coaching report.
"""

import os
import json
from datetime import datetime

import pandas as pd
import streamlit as st

# Load variables from a local .env file (harmless no-op if it doesn't exist,
# e.g. on Streamlit Community Cloud where secrets are injected differently).
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# google-genai is optional at import-time so the app doesn't crash
# if the dependency / API key isn't configured yet.
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="ScreenWise | AI Wellbeing Dashboard",
    page_icon="🧠",
    layout="wide",
)

# --------------------------------------------------------------------------
# Phase 1: Data Pipeline
# --------------------------------------------------------------------------
@st.cache_data
def load_data(path: str = "screentime.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Date"])
    return df


df = load_data()

# --------------------------------------------------------------------------
# Phase 2: Command Center UI — Sidebar Controls
# --------------------------------------------------------------------------
st.sidebar.title("⚙️ Control Panel")

available_dates = sorted(df["Date"].dt.date.unique())
selected_date = st.sidebar.selectbox(
    "Select a day to inspect",
    options=available_dates,
    index=len(available_dates) - 1,  # default to most recent day
    format_func=lambda d: d.strftime("%A, %b %d %Y"),
)

daily_goal_minutes = st.sidebar.slider(
    "Daily screen time goal (minutes)",
    min_value=30,
    max_value=480,
    value=180,
    step=15,
    help="How much total screen time you're aiming to stay under each day.",
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "ScreenWise reads `screentime.csv`, summarizes it, and asks Gemini to "
    "coach you like a no-nonsense friend who actually wants you to win."
)

# --------------------------------------------------------------------------
# Filtered data for the selected day
# --------------------------------------------------------------------------
day_df = df[df["Date"].dt.date == selected_date]

st.title("🧠 ScreenWise — AI Wellbeing Dashboard")
st.caption(f"Snapshot for **{selected_date.strftime('%A, %B %d, %Y')}**")

# --------------------------------------------------------------------------
# Phase 2: KPI Row
# --------------------------------------------------------------------------
total_minutes_today = int(day_df["Minutes_Used"].sum())

if not day_df.empty:
    most_used_app_row = day_df.groupby("App_Name")["Minutes_Used"].sum().idxmax()
    most_used_app_minutes = int(day_df.groupby("App_Name")["Minutes_Used"].sum().max())
else:
    most_used_app_row = "N/A"
    most_used_app_minutes = 0

delta_minutes = total_minutes_today - daily_goal_minutes

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Screen Time Today",
        value=f"{total_minutes_today} min",
    )

with col2:
    st.metric(
        label="Most Used App",
        value=most_used_app_row,
        delta=f"{most_used_app_minutes} min",
        delta_color="off",
    )

with col3:
    st.metric(
        label="Vs. Daily Goal",
        value=f"{daily_goal_minutes} min goal",
        delta=f"{delta_minutes:+d} min",
        delta_color="inverse",  # going over goal should read as "bad" (red)
    )

st.markdown("---")

# --------------------------------------------------------------------------
# Phase 2: Visualizations (14-day trend)
# --------------------------------------------------------------------------
st.subheader("📊 14-Day Screen Time Trend")

trend_col, cat_col = st.columns([2, 1])

with trend_col:
    daily_totals = (
        df.groupby(df["Date"].dt.date)["Minutes_Used"].sum().rename("Total Minutes")
    )
    st.bar_chart(daily_totals)

with cat_col:
    st.markdown("**Today's Category Breakdown**")
    if not day_df.empty:
        cat_totals = day_df.groupby("Category")["Minutes_Used"].sum().sort_values(
            ascending=False
        )
        st.bar_chart(cat_totals)
    else:
        st.info("No data recorded for this day.")

st.markdown("---")

# --------------------------------------------------------------------------
# Phase 3: The Data Bridge — aggregate + serialize for the AI
# --------------------------------------------------------------------------
def build_ai_context(day_df: pd.DataFrame, goal_minutes: int) -> str:
    """
    Aggregates the day's usage per category and converts it into a clean
    string that can be safely embedded into a prompt. AI models can't read
    raw DataFrames, so this is the bridge between pandas and the LLM.
    """
    if day_df.empty:
        return json.dumps({"note": "No screen time recorded for this day."})

    category_summary = (
        day_df.groupby("Category")["Minutes_Used"].sum().sort_values(ascending=False)
    )
    app_summary = (
        day_df.groupby("App_Name")["Minutes_Used"].sum().sort_values(ascending=False)
    )

    summary = {
        "date": str(selected_date),
        "total_minutes": int(day_df["Minutes_Used"].sum()),
        "daily_goal_minutes": goal_minutes,
        "minutes_over_or_under_goal": int(day_df["Minutes_Used"].sum()) - goal_minutes,
        "by_category_minutes": category_summary.to_dict(),
        "by_app_minutes": app_summary.to_dict(),
    }
    return json.dumps(summary, indent=2)


ai_context_str = build_ai_context(day_df, daily_goal_minutes)

# --------------------------------------------------------------------------
# Phase 3: The System Prompt
# --------------------------------------------------------------------------
COACH_PROMPT = f"""
You are "Coach OS" — a holistic life coach who is brutally honest but
fundamentally on the user's side. You have been handed one day's worth of
screen time data, broken down by category and by app.

DATA (JSON):
{ai_context_str}

Your job:
1. Diagnose the day in 1-2 blunt sentences. Do not just say "use your phone
   less" — that is a useless, lazy answer.
2. Identify the single category or app that ate the most time, and propose a
   SPECIFIC, physical, real-world replacement activity for that exact amount
   of time (e.g. "That 47 minutes of TikTok could have been a full workout,
   or half of a good chapter of a book, or a meal-prepped lunch for tomorrow").
3. Give one small, achievable action for tomorrow — not a vague resolution.
4. End with a short, honest verdict: was today a "green", "yellow", or "red"
   day relative to the stated goal?

Keep the whole response under 180 words. Use markdown. Do not be cruel, but
do not be a pushover either — be the friend who tells the truth because they
actually want the user to win.
"""

# --------------------------------------------------------------------------
# Phase 3: The Output — call Gemini and render
# --------------------------------------------------------------------------
st.subheader("🤖 Coach OS — Your AI Wellbeing Report")

api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

if st.button("Generate Today's Coaching Report", type="primary"):
    if not GENAI_AVAILABLE:
        st.error(
            "The `google-genai` package isn't installed. Run "
            "`pip install google-genai` and restart the app."
        )
    elif not api_key:
        st.error(
            "No `GEMINI_API_KEY` found in your environment. Add it to a "
            "`.env` file (and load it, e.g. with `python-dotenv`) or export "
            "it before launching Streamlit."
        )
    else:
        with st.spinner("Coach OS is reviewing your day..."):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=COACH_PROMPT,
                )
                report_text = response.text

                # Choose the widget based on how bad the day was
                if delta_minutes > 60:
                    st.error("🔴 Severe overage day")
                elif delta_minutes > 0:
                    st.warning("🟡 Slightly over goal")
                else:
                    st.success("🟢 On track!")

                st.markdown(report_text)

            except Exception as e:
                st.error(f"Gemini API call failed: {e}")
else:
    st.info(
        "Click the button above to generate your personalized coaching "
        "report for the selected day."
    )

st.markdown("---")

# --------------------------------------------------------------------------
# Phase 4: Innovation Deliverable — The "Shareable" Accountability Link
# --------------------------------------------------------------------------
st.subheader("🔗 Shareable Accountability Link")

query_params = st.query_params

if st.button("Generate my accountability link"):
    st.query_params["date"] = str(selected_date)
    st.query_params["total_minutes"] = str(total_minutes_today)
    st.query_params["goal_minutes"] = str(daily_goal_minutes)
    st.query_params["status"] = "over" if delta_minutes > 0 else "under"

if "total_minutes" in query_params:
    shared_date = query_params.get("date", str(selected_date))
    shared_total = query_params.get("total_minutes", "N/A")
    shared_goal = query_params.get("goal_minutes", "N/A")
    shared_status = query_params.get("status", "N/A")

    st.success(
        f"**Accountability snapshot for {shared_date}:** "
        f"{shared_total} min used vs. a {shared_goal} min goal "
        f"({shared_status} goal)."
    )
    st.caption(
        "Copy this page's URL from your browser's address bar and send it "
        "to your accountability partner — the stats above are embedded "
        "directly in the link's query parameters."
    )
else:
    st.caption(
        "Generate a link above, then copy the URL from your browser to "
        "share your stats with an accountability partner."
    )

st.markdown("---")
st.caption(
    f"ScreenWise · generated {datetime.now().strftime('%Y-%m-%d %H:%M')} · "
    "built for the MirAI School of Technology AI Builder Track"
)
