import calendar
import datetime as dt
import importlib

import streamlit as st

st.set_page_config(
    page_title="Career Intelligence Platform",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Modules (each package must expose main(), as before)
# ---------------------------------------------------------------------------
MODULES = {
    "Dashboard": ("▦", None),
    "Career Recommendation": ("◎", "src.career_recommendation.recommend"),
    "DMIT Dashboard": ("◈", "src.dmit_dashboard.dashboard"),
    "Roadmap Generator": ("⌖", "src.roadmap_generator.generator"),
    "AI Chatbot": ("✦", "src.counsellor_chatbot.chatbot"),
    "Skill Intelligence": ("▤", "src.skill_intelligence.intelligence"),
}
TITLES = {
    "Dashboard": "Dashboard",
    "Career Recommendation": "AI Career Recommendation Engine",
    "DMIT Dashboard": "Interactive DMIT Dashboard",
    "Roadmap Generator": "Career Roadmap Generator",
    "AI Chatbot": "AI Counsellor Chatbot",
    "Skill Intelligence": "School/Corporate Skill Intelligence",
}

if "nav" not in st.session_state:
    st.session_state.nav = "Dashboard"


def go(name: str):
    st.session_state.nav = name


def h(s: str) -> str:
    """Collapse indented HTML so Markdown doesn't treat it as a code block."""
    return "".join(line.strip() for line in s.splitlines())


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
:root{
  --bg:#A9B4FF; --panel:#FFFFFF; --side:#EEF0FF; --line:#E8EAF4;
  --ink:#14141F; --muted:#8A8DA3; --green:#17C964; --purple:#7C5CF0; --yellow:#F5B800; --blue:#3B6CF6;
}
html, body, [class*="css"], .stApp { font-family:'Manrope', system-ui, sans-serif; color:var(--ink); }
.stApp { background: linear-gradient(160deg,#A9B4FF 0%,#C4CBFF 100%); }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"]{ visibility:hidden; height:0; }
header[data-testid="stHeader"]{ background:transparent; }
/* keep the "re-open sidebar" arrow visible (it used to vanish with the header) */
[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"]{
  visibility:visible !important; background:#fff; border-radius:10px; box-shadow:0 2px 8px rgba(20,20,31,.15);
}
[data-testid="stExpandSidebarButton"] *, [data-testid="stSidebarCollapsedControl"] *,
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] *{ color:#14141F !important; }

/* main white panel */
.block-container{
  background:var(--panel); border-radius:18px; margin:1.2rem auto; padding:1.4rem 1.8rem 2rem;
  max-width:1280px; box-shadow:0 20px 50px rgba(60,70,160,.25);
}
h1,h2,h3,h4{ font-family:'Manrope',sans-serif !important; color:var(--ink) !important; letter-spacing:-.02em; font-weight:800 !important; }

/* sidebar */
section[data-testid="stSidebar"]{ background:var(--side); border-right:1px solid var(--line); }
section[data-testid="stSidebar"] > div{ padding-top:.5rem; }
.brand{ font-weight:800; font-size:1.25rem; margin:.3rem 0 1.4rem; display:flex; gap:.5rem; align-items:center; }
.brand i{ font-style:normal; background:var(--ink); color:#fff; width:28px; height:28px; border-radius:8px; display:grid; place-items:center; font-size:.9rem; }
section[data-testid="stSidebar"] div[role="radiogroup"]{ gap:.15rem; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label{
  padding:.6rem .8rem; border-radius:10px; cursor:pointer; font-weight:600; border:1px solid transparent;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover{ background:rgba(255,255,255,.6); }
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked){ background:#fff; border-color:var(--line); }
section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child{ display:none; }
/* readable module content inside the white panel */
.block-container, .block-container p, .block-container li, .block-container label,
.block-container span, .block-container td, .block-container th,
.block-container [data-testid="stMarkdownContainer"],
.block-container [data-testid="stWidgetLabel"] p,
.block-container [data-testid="stCaptionContainer"],
.block-container [data-testid="stChatMessage"] p{
  color:#14141F;
}
.block-container [data-testid="stCaptionContainer"], .block-container small{ color:#5A5D75 !important; }
.block-container .stButton > button, .block-container .stButton > button p,
.block-container .stDownloadButton > button, .block-container .stDownloadButton > button p,
.block-container [data-testid="stFormSubmitButton"] > button, .block-container [data-testid="stFormSubmitButton"] > button p{ color:#FFFFFF !important; }
.block-container .st-key-ai-btn .stButton > button, .block-container .st-key-ai-btn .stButton > button p{ color:#14141F !important; }
.block-container .dark, .block-container .dark *{ color:#FFFFFF; }
.block-container .dark .job, .block-container .dark .job *{ color:#14141F; }
.block-container .dark .job small{ color:#8A8DA3; }
.block-container .cal td.s{ color:#FFFFFF; }
.block-container .up{ color:#0B8A42; }
.block-container .link{ color:#2F55D4; }
.block-container .sub{ color:#6B6E85; }

/* inputs, selects, text areas, chat box */
.block-container input, .block-container textarea,
.block-container [data-baseweb="select"] > div,
.block-container [data-baseweb="input"] > div,
.block-container [data-testid="stChatInput"] textarea{
  background:#F3F4FA !important; color:#14141F !important; border:1px solid #E8EAF4 !important; border-radius:12px;
}
.block-container ::placeholder{ color:#8A8DA3 !important; opacity:1; }
.block-container [data-testid="stChatMessage"]{ background:#F6F7FC; border:1px solid #E8EAF4; border-radius:14px; }
.block-container [data-testid="stAlert"] p{ color:inherit; }
.block-container [data-testid="stFileUploader"] section{ background:#F5F7FF; border:1.5px dashed #B7C0F5; color:#14141F; }
.block-container [data-testid="stFileUploader"] section *{ color:#14141F; }
.block-container [data-testid="stFileUploader"] button{ background:#14141F; color:#fff !important; }
.block-container [data-testid="stDataFrame"], .block-container [data-testid="stTable"]{ color:#14141F; }
.block-container .stTabs [data-baseweb="tab"] p{ color:#5A5D75; font-weight:700; }
.block-container .stTabs [aria-selected="true"] p{ color:#14141F; }

/* ---- visibility fixes: elements that inherited the theme's light text ---- */
.block-container h1, .block-container h2, .block-container h3,
.block-container h4, .block-container h5, .block-container h6,
.block-container [data-testid="stHeading"] *{ color:#14141F !important; }
/* st.metric: value / label were near-white */
.block-container [data-testid="stMetricValue"],
.block-container [data-testid="stMetricValue"] *{ color:#14141F !important; opacity:1 !important; font-weight:800; }
.block-container [data-testid="stMetricLabel"],
.block-container [data-testid="stMetricLabel"] *{ color:#5A5D75 !important; opacity:1 !important; font-weight:600; }
/* form controls & expanders */
.block-container [data-testid="stCheckbox"] *, .block-container [data-testid="stToggle"] *,
.block-container [data-testid="stRadio"] label *, .block-container [data-testid="stExpander"] summary *,
.block-container [data-testid="stSelectbox"] [data-baseweb="select"] div,
.block-container [data-testid="stNumberInput"] input{ color:#14141F; }
.block-container [data-testid="stSliderTickBarMin"], .block-container [data-testid="stSliderTickBarMax"]{ color:#5A5D75 !important; }
.block-container [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] *{ color:#14141F; }
.block-container .tag{ color:#6B4FD8; }
.block-container .cal th{ color:#5A5D75; }
.block-container .drop{ color:#2F55D4; }
/* dropdown menus render outside the white panel */
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li{ background:#fff !important; color:#14141F !important; }
div[data-baseweb="popover"] li:hover, div[data-baseweb="popover"] li[aria-selected="true"]{ background:#F3F4FA !important; }
/* chat input lives in the bottom bar, outside .block-container */
[data-testid="stBottom"] > div{ background:transparent !important; }
[data-testid="stChatInput"]{ background:#fff !important; border:1px solid #E8EAF4; border-radius:14px; }
[data-testid="stChatInput"] textarea{ color:#14141F !important; background:transparent !important; }
[data-testid="stChatInput"] textarea::placeholder{ color:#8A8DA3 !important; opacity:1; }

/* readable sidebar text (overrides Streamlit's theme colours) */
section[data-testid="stSidebar"] .brand,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label p,
section[data-testid="stSidebar"] label span,
section[data-testid="stSidebar"] label div,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{
  color:#14141F !important; opacity:1 !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label p{
  font-size:.98rem !important; font-weight:700 !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked){
  background:#14141F; box-shadow:0 4px 12px rgba(20,20,31,.25);
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p,
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) span,
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) div{
  color:#FFFFFF !important;
}
section[data-testid="stSidebar"] .upgrade b{ color:#14141F !important; }
section[data-testid="stSidebar"] .upgrade span{ color:#4A4D63 !important; }
.upgrade{
  margin-top:1.6rem; padding:1rem; border-radius:16px; text-align:center;
  background:linear-gradient(180deg,#E9ECFF,#D9DEFF); border:1px solid #fff;
}
.upgrade .gem{ font-size:2.4rem; }
.upgrade b{ display:block; font-size:1rem; margin:.3rem 0 .2rem; }
.upgrade span{ font-size:.78rem; color:var(--muted); }
.upgrade .badge{ display:inline-block; margin:.6rem 0; background:#FFE9A8; border-radius:99px; padding:.15rem .6rem; font-size:.75rem; font-weight:700; color:var(--ink); }

/* cards */
.card{ background:#fff; border:1px solid var(--line); border-radius:16px; padding:1rem 1.2rem; height:100%; }
.card .t{ font-weight:700; font-size:.9rem; }
.card .sub{ color:var(--muted); font-size:.78rem; }
.big{ font-size:3.6rem; font-weight:800; line-height:1; letter-spacing:-.04em; }
.up{ color:var(--green); font-size:.75rem; font-weight:700; }
.row{ display:flex; justify-content:space-between; align-items:flex-end; }
.bar{ height:7px; border-radius:99px; background:#EEF0F6; overflow:hidden; margin:.2rem 0 .7rem; }
.bar > div{ height:100%; border-radius:99px; }
.lbl{ display:flex; justify-content:space-between; font-size:.8rem; font-weight:600; }
.link{ color:var(--blue); font-size:.78rem; font-weight:700; }
.dark{ background:#111; color:#fff; border-radius:16px; padding:1rem 1.2rem; height:100%; }
.dark .job{ background:#fff; color:var(--ink); border-radius:12px; padding:.8rem; margin:.7rem 0; font-weight:700; font-size:.9rem; }
.dark .job small{ display:block; color:var(--muted); font-weight:600; margin-top:.2rem; }
.offer{ display:inline-block; border:1px solid var(--line); border-radius:99px; padding:.2rem .9rem; font-weight:700; font-size:.8rem; }
.drop{ border:1.5px dashed #B7C0F5; background:#F5F7FF; border-radius:12px; text-align:center; padding:1.4rem .5rem; font-size:.8rem; color:var(--blue); margin-top:.6rem; }
.sec{ display:flex; justify-content:space-between; margin:1.4rem 0 .6rem; font-weight:700; font-size:.9rem; }

/* recommendation tiles */
.tile{ border-radius:16px; padding:1rem 1.1rem; min-height:150px; }
.tile .em{ font-size:2.2rem; }
.tile b{ display:block; font-size:1.05rem; margin-top:.5rem; }
.tile span{ font-size:.8rem; color:#555770; }
.tag{ display:inline-block; font-size:.68rem; background:rgba(255,255,255,.7); border-radius:6px; padding:.1rem .45rem; margin:.5rem .3rem 0 0; color:#6B4FD8; }

/* calendar */
.cal{ border:1px solid var(--line); border-radius:16px; padding:.8rem; }
.cal .m{ font-weight:800; text-align:center; margin-bottom:.4rem; }
.cal table{ width:100%; border-collapse:separate; border-spacing:3px; text-align:center; font-size:.72rem; }
.cal th{ color:var(--muted); font-weight:600; }
.cal td{ height:26px; border-radius:50%; background:#F3F4FA; font-weight:600; }
.cal td.e{ background:transparent; }
.cal td.s{ background:var(--ink); color:#fff; }
.cal td.today{ outline:2px solid var(--ink); background:#fff; }

/* widgets */
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button{
  background:var(--ink); color:#fff; border:none; border-radius:99px; font-weight:700; padding:.45rem 1.1rem;
}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover{ background:#2B2B45; color:#fff; }
.stButton > button:disabled, .stDownloadButton > button:disabled{ opacity:.45; cursor:not-allowed; }
.stButton > button:focus-visible{ outline:3px solid var(--purple); }
div[data-testid="stTextInput"] input{ background:#F3F4FA; border:none; border-radius:99px; padding:.6rem 1rem; }
.st-key-ai-btn .stButton > button{ background:#fff; color:var(--ink); border:2px solid transparent;
  background-image:linear-gradient(#fff,#fff),linear-gradient(90deg,#17C964,#7C5CF0,#F5B800,#EF4F9B);
  background-origin:border-box; background-clip:padding-box,border-box; }
.st-key-ai-btn .stButton > button:hover{ color:var(--ink); }
[data-testid="stMetric"]{ background:#fff; border:1px solid var(--line); border-radius:12px; padding:.7rem 1rem; }
.stTabs [aria-selected="true"]{ color:var(--ink); }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="brand"><i>◆</i>Career Intelligence</div>', unsafe_allow_html=True)
    st.radio(
        "Navigate",
        list(MODULES.keys()),
        key="nav",
        format_func=lambda n: f"{MODULES[n][0]}   {n}",
        label_visibility="collapsed",
    )
    st.markdown(
        h(
            """
        <div class="upgrade"><div class="gem">💎</div>
        <b>Upgrade to Pro</b>
        <span>Unlock detailed reports and unlimited counselling chats.</span><br>
        <span class="badge">1 month free</span></div>
        """
        ),
        unsafe_allow_html=True,
    )

module = st.session_state.nav

# ---------------------------------------------------------------------------
# Top bar
# ---------------------------------------------------------------------------
c_search, c_ai, c_sp, c_user = st.columns([4, 1.4, 3, 0.6], vertical_alignment="center")
with c_search:
    st.text_input("Search", placeholder="🔍  Search", label_visibility="collapsed")
with c_ai:
    with st.container(key="ai-btn"):
        st.button("AI Assistant ✦", on_click=go, args=("AI Chatbot",), use_container_width=True)
with c_user:
    st.markdown(
        '<div style="text-align:right;font-size:1.6rem">🧑‍🎓</div>', unsafe_allow_html=True
    )
st.markdown('<hr style="border:none;border-top:1px solid #E8EAF4;margin:.6rem 0 1rem">', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Dashboard home (sample figures: replace with real data)
# ---------------------------------------------------------------------------
def calendar_html() -> str:
    today = dt.date.today()
    session_days = {7, 10, 17, 22, 24, 29}
    rows = ""
    for week in calendar.Calendar(firstweekday=0).monthdayscalendar(today.year, today.month):
        cells = ""
        for d in week:
            if d == 0:
                cells += '<td class="e"></td>'
            else:
                cls = "today" if d == today.day else ("s" if d in session_days else "")
                cells += f'<td class="{cls}">{d}</td>'
        rows += f"<tr>{cells}</tr>"
    head = "".join(f"<th>{x}</th>" for x in "MTWTFSS")
    return h(
        f"""<div class="cal"><div class="m">{today.strftime('%B %Y')}</div>
        <table><tr>{head}</tr>{rows}</table></div>"""
    )


def skill_bar(name: str, pct: int, color: str) -> str:
    return (
        f'<div class="lbl"><span>{name}</span><span>{pct}%</span></div>'
        f'<div class="bar"><div style="width:{pct}%;background:{color}"></div></div>'
    )


def dashboard():
    main_col, side_col = st.columns([3, 1.15], gap="large")

    with main_col:
        a, b = st.columns([1, 1.25], gap="medium")
        with a:
            st.markdown(
                h(
                    """
                <div class="card"><div class="t">Assessments taken</div>
                <div class="row"><div><div class="big">46</div>
                <div class="sub">Completed so far</div></div>
                <div><span class="up">▲ 7%</span>
                <svg width="110" height="50" viewBox="0 0 110 50"><polyline fill="none" stroke="#F59E0B" stroke-width="2.5"
                points="0,45 20,40 40,42 60,22 80,26 110,8"/></svg></div></div></div>
                """
                ),
                unsafe_allow_html=True,
            )
        with b:
            st.markdown(
                h(
                    f"""
                <div class="card"><div class="t">Skill tracker</div>
                <div class="row" style="align-items:center;gap:1.2rem">
                <div><div class="big" style="font-size:2.6rem">127h</div>
                <div class="sub">Time spent learning</div></div>
                <div style="flex:1">{skill_bar('Analytical',46,'#17C964')}{skill_bar('Creative',12,'#7C5CF0')}{skill_bar('Technical',27,'#F5B800')}</div>
                </div></div>
                """
                ),
                unsafe_allow_html=True,
            )

        st.write("")
        c1, c2, c3 = st.columns([1.1, 1.1, 1], gap="medium")
        with c1:
            st.markdown(
                h(
                    """
                <div class="dark"><div style="font-size:.8rem;opacity:.8">Career feed</div>
                <div class="job">Product Designer<small>Matched to your strengths</small></div>
                <div style="font-size:.75rem;opacity:.7">Open Career Recommendation to see more</div></div>
                """
                ),
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                h(
                    """
                <div class="card"><div class="t">Ask the counsellor</div>
                <p class="sub" style="margin:.5rem 0 .8rem">Talk through subject choices, colleges or career doubts with no stress.</p>
                <span class="offer">Chat anytime</span></div>
                """
                ),
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                h(
                    """
                <div class="card"><div class="t">Upload your CV</div>
                <div class="sub">We will review it and recommend next steps.</div>
                <div class="drop">📁<br>Drag &amp; drop a file here</div></div>
                """
                ),
                unsafe_allow_html=True,
            )

        st.markdown('<div class="sec"><span>Explore modules</span></div>', unsafe_allow_html=True)
        tiles = [
            ("Career Recommendation", "🎯", "Careers that fit your profile", "#F8D9F6", ["#aptitude", "#careers"]),
            ("Roadmap Generator", "🗺️", "Plan the steps to your goal", "#DDE2FF", ["#plan", "#goals"]),
            ("Skill Intelligence", "📊", "Skill trends for schools and teams", "#FBF3B8", ["#skills", "#insights"]),
        ]
        for col, (name, ic, desc, color, tags) in zip(st.columns(3, gap="medium"), tiles):
            with col:
                tag_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
                st.markdown(
                    h(
                        f"""<div class="tile" style="background:{color}"><div class="em">{ic}</div>
                        <b>{name}</b><span>{desc}</span><br>{tag_html}</div>"""
                    ),
                    unsafe_allow_html=True,
                )
                st.button("Open", key=f"open_{name}", on_click=go, args=(name,))

    with side_col:
        st.markdown(calendar_html(), unsafe_allow_html=True)
        st.markdown('<div class="sec"><span>Up next</span><span class="link">View all</span></div>', unsafe_allow_html=True)
        st.markdown(
            h(
                """
            <div class="card" style="background:#F6F7FC"><div style="font-size:1.6rem">🧬</div>
            <div class="t" style="font-size:1.05rem">DMIT report review</div>
            <div class="sub">Walk through your results with a counsellor</div>
            <div class="lbl" style="margin-top:.8rem"><span>Progress</span><span>62%</span></div>
            <div class="bar"><div style="width:62%;background:#17C964"></div></div></div>
            """
            ),
            unsafe_allow_html=True,
        )
        st.button("Open DMIT Dashboard", on_click=go, args=("DMIT Dashboard",), use_container_width=True)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if module == "Dashboard":
    dashboard()
else:
    st.markdown(f"## {TITLES[module]}")
    import_path = MODULES[module][1]
    try:
        importlib.import_module(import_path).main()
    except ModuleNotFoundError as err:
        st.error(f"Could not load **{module}**: `{err.name}` is missing.")
