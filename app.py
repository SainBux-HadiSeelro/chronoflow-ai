"""
ChronoFlow-AI // Simple, Modern & Smart Countdown Timer with 24/7 Corner Chatbot
Designed for everyday users & power-focused professionals.
"""

import re
import datetime
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="ChronoFlow | Simple & Smart Countdown Timer",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Modern, Clean & Simple CSS Styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    /* Global Theme */
    .stApp {
        background: linear-gradient(180deg, #0b0f19 0%, #111827 100%);
        color: #f3f4f6;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Container Card */
    .main-card {
        background: rgba(31, 41, 55, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }

    /* Simple Header */
    .app-header {
        text-align: center;
        margin-top: 10px;
        margin-bottom: 24px;
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
        background: linear-gradient(135deg, #ffffff 40%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .app-tagline {
        color: #9ca3af;
        font-size: 1rem;
        margin: 0;
    }

    /* Buttons Styling */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 18px;
        transition: all 0.2s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.25);
    }

    /* Metrics Bar */
    div[data-testid="stMetric"] {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 12px 16px;
    }

    div[data-testid="stMetricValue"] {
        color: #818cf8 !important;
        font-weight: 700;
    }

    /* Floating Corner Chatbot Button (Bottom Right) */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        z-index: 999999 !important;
    }

    div[data-testid="stPopover"] > button {
        border-radius: 50px !important;
        padding: 14px 22px !important;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.5), 0 0 15px rgba(124, 58, 237, 0.4) !important;
        border: none !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 10px !important;
        transition: all 0.25s ease !important;
    }

    div[data-testid="stPopover"] > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 15px 30px -5px rgba(79, 70, 229, 0.7) !important;
    }

    /* Chat bubble styling */
    .stChatMessage {
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# State Management
# ---------------------------------------------------------
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 25 * 60  # Default 25m
if "task_name" not in st.session_state:
    st.session_state.task_name = "Study / Work Session"
if "completed_count" not in st.session_state:
    st.session_state.completed_count = 0
if "session_history" not in st.session_state:
    st.session_state.session_history = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Assalam o Alaikum! Main aapka 24/7 AI Assistant hoon.**\n\n"
                "Aap mujhse timer use karne, study schedule banane, ya sound ke baare me kuch bhi aasaan zubaan me pooch sakte hain!"
            ),
        }
    ]


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def parse_simple_time_text(text: str) -> tuple[int, str]:
    """Parse text like '25m study' or '10 min break'"""
    t = text.lower().strip()
    secs = 0
    h = re.search(r"(\d+)\s*(?:h|hr|hour|hours)", t)
    m = re.search(r"(\d+)\s*(?:m|min|minute|minutes)", t)
    s = re.search(r"(\d+)\s*(?:s|sec|second|seconds)", t)
    if h:
        secs += int(h.group(1)) * 3600
    if m:
        secs += int(m.group(1)) * 60
    if s:
        secs += int(s.group(1))

    if secs == 0:
        raw = re.search(r"^(\d+)$", t)
        if raw:
            secs = int(raw.group(1)) * 60

    cleaned = re.sub(r"\b(?:\d+\s*(?:h|hr|hours?|m|min|minutes?|s|sec|seconds?))\b", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b(?:timer|set|for|start|countdown|please)\b", "", cleaned, flags=re.IGNORECASE).strip()
    task = cleaned.capitalize() if cleaned else "Work / Study"
    return (secs if secs > 0 else 25 * 60, task)


def set_timer(seconds: int, task: str):
    st.session_state.total_seconds = seconds
    st.session_state.task_name = task


# ---------------------------------------------------------
# 24/7 Corner Chatbot Logic (Friendly & Simple)
# ---------------------------------------------------------
def get_corner_chat_reply(query: str) -> str:
    q = query.lower().strip()

    if any(k in q for k in ["salam", "hello", "hi", "hey", "kese", "kaise", "hal"]):
        return (
            "👋 **Walaikum Assalam!**\n\n"
            "Main theek hoon! Aap batayein main aapki timer ya study session me kya madad kar sakta hoon?\n\n"
            "- *'Timer kaise lagayein?'*\n"
            "- *'Study ke liye best time kitna hai?'*\n"
            "- *'Sound kyu nahi aa rahi?'*"
        )

    if any(k in q for k in ["sound", "audio", "awaaz", "alarm", "chime"]):
        return (
            "🔊 **Sound / Alarm ki Maloomat:**\n\n"
            "- Jab timer 00:00:00 par pohnchta hai to pyari si bell chime bajti hai.\n"
            "- **Tip:** Browser security ki wajah se page par kam az kam ek dafa **Start** button click hona zaroori hai taake browser sound allow kare."
        )

    if any(k in q for k in ["preset", "buttons", "modes", "study", "work", "pomodoro"]):
        return (
            "🎯 **Aasaan Timer Presets:**\n\n"
            "1. **Study / Work (25 min):** Har 25 minute baad 5 minute ka break lein (ise Pomodoro technique kehte hain).\n"
            "2. **Chai Break (5 min):** Paani peene aur fresh hone ke liye.\n"
            "3. **Long Break (15 min):** Kuch der araam karne ke liye.\n"
            "4. **Deep Focus (45 min):** Lamba kaam ya exam preparation ke liye."
        )

    if any(k in q for k in ["kaise", "how to", "use", "chale"]):
        return (
            "⏱️ **Timer Use Karna Bohot Aasaan Hai:**\n\n"
            "1. Screen par kisi bhi button par click karein (jaise *'Study (25 min)'*).\n"
            "2. **Green START** button dabayein, countdown shuru ho jayega!\n"
            "3. Kaam rokna ho to **PAUSE** dabayein, shuru se chalana ho to **RESET** dabayein."
        )

    return (
        f"🤖 **ChronoFlow Assistant:**\n\n"
        f"Aapne poocha: *\"{query}\"*\n\n"
        f"Aap timer ko screen par buttons ke zariye aasaani se control kar sakte hain. "
        f"Agar koi aur sawal ho to zaroor poochein, main 24/7 yahin mojood hoon!"
    )


# ---------------------------------------------------------
# App Header
# ---------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1 class="app-title">⏱️ ChronoFlow Timer</h1>
        <p class="app-tagline">Aasaan, Tez aur Khubsurat Countdown Timer</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Quick Stats (Clean & Friendly)
# ---------------------------------------------------------
s1, s2, s3 = st.columns(3)
with s1:
    st.metric("Total Focus Time", f"{(st.session_state.completed_count * 25)} mins")
with s2:
    st.metric("Missions Completed", f"{st.session_state.completed_count} ✅")
with s3:
    st.metric("Assistant Status", "Online 🟢")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1-Click Fast Presets (Aam bande ke liye bilkul simple)
# ---------------------------------------------------------
st.markdown("<h4 style='text-align: center; font-size: 1.1rem; color: #9ca3af;'>⚡ Quick Presets (1-Click me time set karein)</h4>", unsafe_allow_html=True)
p1, p2, p3, p4 = st.columns(4)

with p1:
    if st.button("💻 Study (25m)", use_container_width=True):
        set_timer(25 * 60, "Study / Work")
        st.rerun()

with p2:
    if st.button("☕ Chai Break (5m)", use_container_width=True):
        set_timer(5 * 60, "Chai Break")
        st.rerun()

with p3:
    if st.button("🌴 Rest (15m)", use_container_width=True):
        set_timer(15 * 60, "Rest & Refresh")
        st.rerun()

with p4:
    if st.button("🚀 Focus (45m)", use_container_width=True):
        set_timer(45 * 60, "Deep Focus")
        st.rerun()

# ---------------------------------------------------------
# Clean, Simple & Modern Circular Timer HUD
# ---------------------------------------------------------
hud_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=JetBrains+Mono:wght@700&display=swap');

    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        user-select: none;
    }}

    body {{
        background: transparent;
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 6px 0;
    }}

    .timer-card {{
        width: 100%;
        max-width: 540px;
        background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 26px 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }}

    .task-badge {{
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #a5b4fc;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 16px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}

    .circle-wrap {{
        position: relative;
        width: 250px;
        height: 250px;
        margin: 6px 0 16px 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    svg {{
        transform: rotate(-90deg);
        width: 100%;
        height: 100%;
    }}

    circle {{
        fill: none;
        stroke-width: 12;
        stroke-linecap: round;
    }}

    .circle-bg {{
        stroke: rgba(255, 255, 255, 0.08);
    }}

    .circle-progress {{
        stroke: #6366f1;
        stroke-dasharray: 722.5; /* 2 * PI * 115 */
        stroke-dashoffset: 0;
        transition: stroke-dashoffset 0.3s ease, stroke 0.3s ease;
        filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.5));
    }}

    .circle-progress.paused {{
        stroke: #f59e0b;
        filter: drop-shadow(0 0 10px rgba(245, 158, 11, 0.5));
    }}

    .circle-progress.completed {{
        stroke: #10b981;
        filter: drop-shadow(0 0 15px rgba(16, 185, 129, 0.7));
    }}

    .timer-readout {{
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}

    .time-digits {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.2rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
        line-height: 1;
    }}

    .status-text {{
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 600;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    .controls-row {{
        display: flex;
        gap: 12px;
        width: 100%;
        justify-content: center;
        margin-top: 10px;
        flex-wrap: wrap;
    }}

    button.btn-action {{
        padding: 12px 24px;
        border-radius: 14px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        cursor: pointer;
        border: none;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }}

    button.btn-start {{
        background: #10b981;
        color: #ffffff;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
    }}

    button.btn-start:hover {{
        background: #059669;
        transform: translateY(-2px);
    }}

    button.btn-pause {{
        background: #f59e0b;
        color: #ffffff;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.4);
    }}

    button.btn-pause:hover {{
        background: #d97706;
        transform: translateY(-2px);
    }}

    button.btn-reset {{
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #e2e8f0;
    }}

    button.btn-reset:hover {{
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }}

    .bumps-row {{
        display: flex;
        gap: 10px;
        margin-top: 14px;
    }}

    button.btn-bump {{
        padding: 8px 16px;
        border-radius: 10px;
        font-size: 0.82rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #c7d2fe;
        cursor: pointer;
        transition: all 0.2s ease;
    }}

    button.btn-bump:hover {{
        background: rgba(99, 102, 241, 0.3);
        transform: translateY(-1px);
    }}
</style>
</head>
<body>

<div class="timer-card">
    <div class="task-badge">
        <span>🎯</span>
        <span>{st.session_state.task_name}</span>
    </div>

    <div class="circle-wrap">
        <svg viewBox="0 0 250 250">
            <circle class="circle-bg" cx="125" cy="125" r="115"></circle>
            <circle id="progressCircle" class="circle-progress" cx="125" cy="125" r="115"></circle>
        </svg>
        <div class="timer-readout">
            <div id="timeDisplay" class="time-digits">--:--</div>
            <div id="statusLabel" class="status-text">READY</div>
        </div>
    </div>

    <div class="controls-row">
        <button id="toggleBtn" class="btn-action btn-start" onclick="toggleTimer()">
            <span id="btnIcon">▶</span>
            <span id="btnText">START</span>
        </button>
        <button class="btn-action btn-reset" onclick="resetTimer()">
            <span>🔄</span>
            <span>RESET</span>
        </button>
    </div>

    <div class="bumps-row">
        <button class="btn-bump" onclick="addSeconds(60)">+1 Min</button>
        <button class="btn-bump" onclick="addSeconds(300)">+5 Min</button>
        <button class="btn-bump" onclick="addSeconds(600)">+10 Min</button>
    </div>
</div>

<script>
    let totalDuration = {st.session_state.total_seconds};
    let remaining = totalDuration;
    let isRunning = false;
    let timerId = null;

    const CIRCLE_LENGTH = 2 * Math.PI * 115; // 722.56
    const circle = document.getElementById('progressCircle');
    const display = document.getElementById('timeDisplay');
    const statusLabel = document.getElementById('statusLabel');
    const toggleBtn = document.getElementById('toggleBtn');
    const btnIcon = document.getElementById('btnIcon');
    const btnText = document.getElementById('btnText');

    circle.style.strokeDasharray = CIRCLE_LENGTH;

    // Web Audio Bell Chime
    let audioCtx = null;
    function playChime() {{
        try {{
            if (!audioCtx) {{
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                audioCtx = new AudioContext();
            }}
            if (audioCtx.state === 'suspended') audioCtx.resume();

            const notes = [523.25, 659.25, 783.99, 1046.50]; // Sweet chord C-E-G-C
            notes.forEach((freq, idx) => {{
                setTimeout(() => {{
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                    gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.8);
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.8);
                }}, idx * 180);
            }});
        }} catch(e) {{}}
    }}

    function formatTime(secs) {{
        const h = Math.floor(secs / 3600);
        const m = Math.floor((secs % 3600) / 60);
        const s = secs % 60;
        if (h > 0) {{
            return `${{String(h).padStart(2, '0')}}:${{String(m).padStart(2, '0')}}:${{String(s).padStart(2, '0')}}`;
        }}
        return `${{String(m).padStart(2, '0')}}:${{String(s).padStart(2, '0')}}`;
    }}

    function update() {{
        display.innerText = formatTime(remaining);
        const ratio = totalDuration > 0 ? remaining / totalDuration : 0;
        circle.style.strokeDashoffset = CIRCLE_LENGTH * (1 - ratio);
    }}

    function toggleTimer() {{
        if (isRunning) {{
            // Pause
            clearInterval(timerId);
            isRunning = false;
            circle.classList.add('paused');
            toggleBtn.className = "btn-action btn-start";
            btnIcon.innerText = "▶";
            btnText.innerText = "RESUME";
            statusLabel.innerText = "PAUSED";
            statusLabel.style.color = "#f59e0b";
        }} else {{
            // Start
            if (remaining <= 0) remaining = totalDuration;
            isRunning = true;
            circle.classList.remove('paused', 'completed');
            toggleBtn.className = "btn-action btn-pause";
            btnIcon.innerText = "⏸";
            btnText.innerText = "PAUSE";
            statusLabel.innerText = "RUNNING";
            statusLabel.style.color = "#10b981";

            timerId = setInterval(() => {{
                if (remaining > 0) {{
                    remaining--;
                    update();
                }} else {{
                    clearInterval(timerId);
                    isRunning = false;
                    circle.classList.add('completed');
                    toggleBtn.className = "btn-action btn-start";
                    btnIcon.innerText = "▶";
                    btnText.innerText = "RESTART";
                    statusLabel.innerText = "TIME'S UP! ⏰";
                    statusLabel.style.color = "#10b981";
                    playChime();
                }}
            }}, 1000);
        }}
    }}

    function resetTimer() {{
        clearInterval(timerId);
        isRunning = false;
        remaining = totalDuration;
        circle.classList.remove('paused', 'completed');
        toggleBtn.className = "btn-action btn-start";
        btnIcon.innerText = "▶";
        btnText.innerText = "START";
        statusLabel.innerText = "READY";
        statusLabel.style.color = "#94a3b8";
        update();
    }}

    function addSeconds(sec) {{
        totalDuration += sec;
        remaining += sec;
        update();
    }}

    update();
</script>
</body>
</html>
"""

components.html(hud_html, height=440, scrolling=False)

# ---------------------------------------------------------
# Custom Time Input (Aam bande ke liye simple)
# ---------------------------------------------------------
with st.expander("🛠️ Custom Time Set Karein (Apni marzi ka waqt)", expanded=False):
    t_tab1, t_tab2 = st.tabs(["🔢 Number Input", "✍️ Likh Kar Set Karein"])

    with t_tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            inp_h = st.number_input("Ghante (Hours)", 0, 23, st.session_state.total_seconds // 3600)
        with c2:
            inp_m = st.number_input("Minutes", 0, 59, (st.session_state.total_seconds % 3600) // 60)
        with c3:
            inp_s = st.number_input("Seconds", 0, 59, st.session_state.total_seconds % 60)

        custom_name = st.text_input("Kaam ka naam (Task Name):", value="Custom Session")

        if st.button("Timer Apply Karein ⏱️", use_container_width=True):
            tot = int(inp_h * 3600 + inp_m * 60 + inp_s)
            if tot > 0:
                set_timer(tot, custom_name if custom_name else "Custom Session")
                st.rerun()
            else:
                st.warning("Please kam az kam 1 second select karein.")

    with t_tab2:
        nlp_text = st.text_input(
            "Jaise ke: '30m coding' ya '10 min break'",
            placeholder="e.g. 15m exercise",
        )
        if st.button("Set Text Timer 🚀", use_container_width=True):
            if nlp_text.strip():
                t_sec, t_lbl = parse_simple_time_text(nlp_text)
                set_timer(t_sec, t_lbl)
                st.rerun()

# ---------------------------------------------------------
# Completed Session Logger
# ---------------------------------------------------------
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
with st.container():
    col_l1, col_l2 = st.columns([3, 1])
    with col_l1:
        note = st.text_input("Session Notes (optional):", value=f"Completed {st.session_state.task_name}")
    with col_l2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Save Session ✅", use_container_width=True):
            st.session_state.completed_count += 1
            st.session_state.session_history.append(
                {
                    "time": datetime.datetime.now().strftime("%I:%M %p"),
                    "task": st.session_state.task_name,
                    "note": note,
                }
            )
            st.success("Session save ho gaya!")
            st.rerun()

# ---------------------------------------------------------
# FLOATING CORNER CHATBOT (Bottom Right Website-Style Widget)
# ---------------------------------------------------------
with st.popover("💬 Chat Support (24/7)", use_container_width=False):
    st.markdown(
        """
        <div style="border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; margin-bottom: 12px;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #818cf8; display: flex; align-items: center; gap: 8px;">
                <span>💬</span>
                <span>ChronoFlow Assistant</span>
                <span style="font-size: 0.72rem; background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 2px 8px; border-radius: 999px;">● Online</span>
            </div>
            <p style="font-size: 0.8rem; color: #94a3b8; margin: 2px 0 0 0;">
                Main aapka 24/7 live helper hoon. Kuch bhi poochein!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick Suggestion Chips
    c_chip1, c_chip2 = st.columns(2)
    with c_chip1:
        if st.button("⏱️ Timer kaise chalayein?", use_container_width=True):
            user_q = "Timer kaise chalayein?"
            st.session_state.chat_messages.append({"role": "user", "content": user_q})
            ans = get_corner_chat_reply(user_q)
            st.session_state.chat_messages.append({"role": "assistant", "content": ans})
            st.rerun()

    with c_chip2:
        if st.button("🧠 Study ke tips?", use_container_width=True):
            user_q = "Study ke tips?"
            st.session_state.chat_messages.append({"role": "user", "content": user_q})
            ans = get_corner_chat_reply(user_q)
            st.session_state.chat_messages.append({"role": "assistant", "content": ans})
            st.rerun()

    # Chat Messages Box
    with st.container(height=260):
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Chat Form Input
    with st.form("corner_chat_form", clear_on_submit=True):
        chat_col_in, chat_col_btn = st.columns([4, 1])
        with chat_col_in:
            user_input = st.text_input(
                "Message...",
                placeholder="Apna sawal yahan likhein...",
                label_visibility="collapsed",
            )
        with chat_col_btn:
            send_clicked = st.form_submit_button("Send 🚀")

        if send_clicked and user_input.strip():
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            reply = get_corner_chat_reply(user_input)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

# ---------------------------------------------------------
# Clean Minimal Footer
# ---------------------------------------------------------
st.markdown(
    """
    <div style="text-align: center; margin-top: 30px; padding: 16px; color: #6b7280; font-size: 0.82rem;">
        <span>ChronoFlow Timer &bull; Simple, Modern & Fast</span>
    </div>
    """,
    unsafe_allow_html=True,
)
