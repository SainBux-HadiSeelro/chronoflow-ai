"""
ChronoFlow-AI // Simple, Modern & High-Contrast Countdown Timer with 24/7 Corner Chatbot
Optimized for 100% visual clarity, readability, mobile responsiveness and ease of use.
"""

import re
import datetime
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="ChronoFlow | Simple Countdown Timer",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Global High-Contrast Styling & Mobile Responsiveness
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@700&display=swap');

    /* Global App Background & Base Typography */
    .stApp {
        background-color: #0b0f19 !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Force all text paragraphs, spans, labels to be crisp white / light */
    p, span, h1, h2, h3, h4, h5, h6, li {
        color: #f8fafc !important;
    }

    /* Main Container Mobile Optimization */
    .block-container {
        max-width: 680px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 1rem !important;
            padding-bottom: 6rem !important;
        }
    }

    /* App Header */
    .app-header {
        text-align: center;
        margin-top: 4px;
        margin-bottom: 16px;
    }

    .app-title {
        font-size: clamp(1.6rem, 5vw, 2.2rem) !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
        color: #ffffff !important;
    }

    .app-tagline {
        color: #94a3b8 !important;
        font-size: clamp(0.85rem, 2.6vw, 1.05rem) !important;
        font-weight: 500;
        margin: 0;
    }

    /* Widget Labels (Hours, Minutes, Task Name, Notes) */
    label, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
    }

    /* Input Boxes (Text input, Number input) - Solid Background with Crisp White Text */
    input, textarea, [data-baseweb="input"] input, [data-baseweb="base-input"] input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1.5px solid #475569 !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }

    input:focus, textarea:focus, [data-baseweb="input"]:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.3) !important;
    }

    input::placeholder, textarea::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }

    /* Number Input Stepper Buttons (+ / -) */
    button[data-testid="stNumberInputStepDown"], button[data-testid="stNumberInputStepUp"] {
        color: #ffffff !important;
        background-color: #334155 !important;
        border-color: #475569 !important;
    }

    /* Responsive Stats Metric Cards (Keeps them in 1 Row on Mobile) */
    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
    }

    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"] {
        min-width: 0 !important;
        flex: 1 1 0 !important;
    }

    div[data-testid="stMetric"] {
        background-color: #1e293b !important;
        border: 1.5px solid #334155 !important;
        border-radius: 12px !important;
        padding: 8px 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
        text-align: center !important;
    }

    div[data-testid="stMetricLabel"] p {
        color: #cbd5e1 !important;
        font-size: clamp(0.68rem, 2.2vw, 0.85rem) !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    div[data-testid="stMetricValue"] div {
        color: #38bdf8 !important;
        font-weight: 800 !important;
        font-size: clamp(1.05rem, 3.2vw, 1.35rem) !important;
    }

    /* Streamlit Standard Buttons (Presets & Action buttons) */
    .stButton > button {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1.5px solid #475569 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 9px 12px !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #4f46e5 !important;
        border-color: #6366f1 !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4) !important;
    }

    /* Quick Presets on Mobile: Clean 2x2 Grid instead of stacked rows */
    @media (max-width: 640px) {
        div[data-testid="stHorizontalBlock"]:has(.stButton) {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 8px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.stButton) > div[data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
        }
        .stButton > button {
            padding: 10px 8px !important;
            font-size: 0.85rem !important;
        }
    }

    /* Expander Container & Header */
    [data-testid="stExpander"] {
        background-color: #1e293b !important;
        border: 1.5px solid #334155 !important;
        border-radius: 16px !important;
        margin-top: 14px !important;
        overflow: hidden !important;
    }

    [data-testid="stExpander"] summary {
        background-color: #1e293b !important;
        padding: 12px 16px !important;
    }

    [data-testid="stExpander"] summary span, [data-testid="stExpander"] summary p {
        color: #f8fafc !important;
        font-weight: 700 !important;
        font-size: 0.96rem !important;
    }

    /* Tabs Inside Expander */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0f172a !important;
        padding: 4px !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 7px 12px !important;
        font-size: 0.88rem !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #4f46e5 !important;
        color: #ffffff !important;
    }

    /* Custom Number Input Columns side by side on Mobile */
    @media (max-width: 640px) {
        [data-testid="stExpander"] [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            gap: 6px !important;
        }
        [data-testid="stExpander"] [data-testid="stColumn"] {
            min-width: 0 !important;
            flex: 1 1 0 !important;
        }
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
    st.session_state.task_name = "Study / Work"
if "completed_count" not in st.session_state:
    st.session_state.completed_count = 0
if "session_history" not in st.session_state:
    st.session_state.session_history = []


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
# App Header (Responsive & Clean)
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
# Quick Stats (Clean, High Contrast & Always 1 Row on Mobile)
# ---------------------------------------------------------
s1, s2, s3 = st.columns(3)
with s1:
    st.metric("Total Focus Time", f"{(st.session_state.completed_count * 25)}m")
with s2:
    st.metric("Missions Done", f"{st.session_state.completed_count} ✅")
with s3:
    st.metric("Assistant Status", "Online 🟢")

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1-Click Fast Presets (Responsive 2x2 Grid on Mobile)
# ---------------------------------------------------------
st.markdown("<h4 style='text-align: center; font-size: 1.05rem; color: #f1f5f9; font-weight: 700; margin-bottom: 10px;'>⚡ Quick Presets (1-Click me set karein)</h4>", unsafe_allow_html=True)
p1, p2, p3, p4 = st.columns(4)

with p1:
    if st.button("💻 Study (25m)", use_container_width=True):
        set_timer(25 * 60, "Study / Work")
        st.rerun()

with p2:
    if st.button("☕ Chai (5m)", use_container_width=True):
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
# Clean, High-Contrast Circular Timer HUD + Pinned Corner Chatbot Launcher
# ---------------------------------------------------------
hud_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=JetBrains+Mono:wght@700&display=swap');

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        user-select: none;
    }

    body {
        background: transparent;
        color: #ffffff;
        font-family: 'Plus Jakarta Sans', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 4px 0;
    }

    .timer-card {
        width: 100%;
        max-width: 520px;
        background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #334155;
        border-radius: 24px;
        padding: 20px 14px;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.5);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .task-badge {
        background: rgba(99, 102, 241, 0.25);
        border: 1.5px solid #818cf8;
        color: #ffffff;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 0.92rem;
        font-weight: 700;
        margin-bottom: 12px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    .circle-wrap {
        position: relative;
        width: clamp(210px, 58vw, 250px);
        height: clamp(210px, 58vw, 250px);
        margin: 4px 0 14px 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    svg {
        transform: rotate(-90deg);
        width: 100%;
        height: 100%;
    }

    circle {
        fill: none;
        stroke-width: 13;
        stroke-linecap: round;
    }

    .circle-bg {
        stroke: #334155;
    }

    .circle-progress {
        stroke: #6366f1;
        stroke-dasharray: 753.9; /* 2 * PI * 120 */
        stroke-dashoffset: 0;
        transition: stroke-dashoffset 0.3s ease, stroke 0.3s ease;
        filter: drop-shadow(0 0 12px rgba(99, 102, 241, 0.6));
    }

    .circle-progress.paused {
        stroke: #f59e0b;
        filter: drop-shadow(0 0 12px rgba(245, 158, 11, 0.6));
    }

    .circle-progress.completed {
        stroke: #10b981;
        filter: drop-shadow(0 0 16px rgba(16, 185, 129, 0.8));
    }

    .timer-readout {
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .time-digits {
        font-family: 'JetBrains Mono', monospace;
        font-size: clamp(2.8rem, 8.5vw, 3.4rem);
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
        line-height: 1;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }

    .status-text {
        font-size: 0.85rem;
        color: #cbd5e1;
        font-weight: 700;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .controls-row {
        display: flex;
        gap: 12px;
        width: 100%;
        justify-content: center;
        margin-top: 8px;
        flex-wrap: wrap;
    }

    button.btn-action {
        padding: 12px 24px;
        border-radius: 12px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 0.95rem;
        cursor: pointer;
        border: none;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    button.btn-start {
        background: #10b981;
        color: #ffffff;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.45);
    }

    button.btn-start:hover {
        background: #059669;
        transform: translateY(-2px);
    }

    button.btn-pause {
        background: #f59e0b;
        color: #ffffff;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.45);
    }

    button.btn-pause:hover {
        background: #d97706;
        transform: translateY(-2px);
    }

    button.btn-reset {
        background: #334155;
        border: 1.5px solid #475569;
        color: #ffffff;
    }

    button.btn-reset:hover {
        background: #475569;
        transform: translateY(-2px);
    }

    .bumps-row {
        display: flex;
        gap: 8px;
        margin-top: 14px;
        flex-wrap: wrap;
        justify-content: center;
    }

    button.btn-bump {
        padding: 8px 14px;
        border-radius: 9px;
        font-size: 0.82rem;
        font-weight: 700;
        background: rgba(99, 102, 241, 0.25);
        border: 1.5px solid #818cf8;
        color: #ffffff;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    button.btn-bump:hover {
        background: rgba(99, 102, 241, 0.45);
        transform: translateY(-1px);
    }
</style>
</head>
<body>

<div class="timer-card">
    <div class="task-badge">
        <span>🎯</span>
        <span>__TASK_NAME__</span>
    </div>

    <div class="circle-wrap">
        <svg viewBox="0 0 260 260">
            <circle class="circle-bg" cx="130" cy="130" r="120"></circle>
            <circle id="progressCircle" class="circle-progress" cx="130" cy="130" r="120"></circle>
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
    let totalDuration = __TOTAL_SECONDS__;
    let remaining = totalDuration;
    let isRunning = false;
    let timerId = null;

    const CIRCLE_LENGTH = 2 * Math.PI * 120; // 753.98
    const circle = document.getElementById('progressCircle');
    const display = document.getElementById('timeDisplay');
    const statusLabel = document.getElementById('statusLabel');
    const toggleBtn = document.getElementById('toggleBtn');
    const btnIcon = document.getElementById('btnIcon');
    const btnText = document.getElementById('btnText');

    circle.style.strokeDasharray = CIRCLE_LENGTH;

    // Web Audio Bell Chime
    let audioCtx = null;
    function playChime() {
        try {
            if (!audioCtx) {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                audioCtx = new AudioContext();
            }
            if (audioCtx.state === 'suspended') audioCtx.resume();

            const notes = [523.25, 659.25, 783.99, 1046.50];
            notes.forEach((freq, idx) => {
                setTimeout(() => {
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
                }, idx * 180);
            });
        } catch(e) {}
    }

    function formatTime(secs) {
        const h = Math.floor(secs / 3600);
        const m = Math.floor((secs % 3600) / 60);
        const s = secs % 60;
        if (h > 0) {
            return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
        }
        return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }

    function update() {
        display.innerText = formatTime(remaining);
        const ratio = totalDuration > 0 ? remaining / totalDuration : 0;
        circle.style.strokeDashoffset = CIRCLE_LENGTH * (1 - ratio);
    }

    function toggleTimer() {
        if (isRunning) {
            // Pause
            clearInterval(timerId);
            isRunning = false;
            circle.classList.add('paused');
            toggleBtn.className = "btn-action btn-start";
            btnIcon.innerText = "▶";
            btnText.innerText = "RESUME";
            statusLabel.innerText = "PAUSED";
            statusLabel.style.color = "#f59e0b";
        } else {
            // Start
            if (remaining <= 0) remaining = totalDuration;
            isRunning = true;
            circle.classList.remove('paused', 'completed');
            toggleBtn.className = "btn-action btn-pause";
            btnIcon.innerText = "⏸";
            btnText.innerText = "PAUSE";
            statusLabel.innerText = "RUNNING";
            statusLabel.style.color = "#10b981";

            timerId = setInterval(() => {
                if (remaining > 0) {
                    remaining--;
                    update();
                } else {
                    clearInterval(timerId);
                    isRunning = false;
                    circle.classList.add('completed');
                    toggleBtn.className = "btn-action btn-start";
                    btnIcon.innerText = "▶";
                    btnText.innerText = "RESTART";
                    statusLabel.innerText = "TIME'S UP! ⏰";
                    statusLabel.style.color = "#10b981";
                    playChime();
                }
            }, 1000);
        }
    }

    function resetTimer() {
        clearInterval(timerId);
        isRunning = false;
        remaining = totalDuration;
        circle.classList.remove('paused', 'completed');
        toggleBtn.className = "btn-action btn-start";
        btnIcon.innerText = "▶";
        btnText.innerText = "START";
        statusLabel.innerText = "READY";
        statusLabel.style.color = "#cbd5e1";
        update();
    }

    function addSeconds(sec) {
        totalDuration += sec;
        remaining += sec;
        update();
    }

    update();

    // ========================================================
    // PINNED CORNER FLOATING CHATBOT ATTACHED TO SCREEN CORNER
    // ========================================================
    function setupCornerChatbot() {
        try {
            const pdoc = window.parent.document;
            if (!pdoc || !pdoc.body) return;

            // If already created, skip duplicate
            if (pdoc.getElementById('chronoflow-corner-chatbot')) return;

            const wrap = pdoc.createElement('div');
            wrap.id = 'chronoflow-corner-chatbot';

            wrap.innerHTML = `
            <style>
                #cf-chat-launcher {
                    position: fixed;
                    bottom: 22px;
                    right: 22px;
                    z-index: 2147483647;
                    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                    color: #ffffff;
                    border-radius: 50px;
                    padding: 12px 20px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    cursor: pointer;
                    box-shadow: 0 10px 28px rgba(79, 70, 229, 0.65), 0 0 16px rgba(124, 58, 237, 0.4);
                    border: 2px solid rgba(255, 255, 255, 0.25);
                    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
                    font-size: 0.96rem;
                    font-weight: 700;
                    transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s ease;
                    user-select: none;
                }

                #cf-chat-launcher:hover {
                    transform: translateY(-3px) scale(1.04);
                    box-shadow: 0 14px 35px rgba(79, 70, 229, 0.85);
                }

                .cf-online-indicator {
                    width: 9px;
                    height: 9px;
                    background-color: #10b981;
                    border-radius: 50%;
                    box-shadow: 0 0 8px #10b981;
                    display: inline-block;
                    animation: cfPulse 2s infinite;
                }

                @keyframes cfPulse {
                    0%, 100% { opacity: 1; transform: scale(1); }
                    50% { opacity: 0.6; transform: scale(1.2); }
                }

                #cf-chat-window {
                    position: fixed;
                    bottom: 84px;
                    right: 22px;
                    width: 380px;
                    max-height: 520px;
                    z-index: 2147483647;
                    background: #0f172a;
                    border: 2px solid #6366f1;
                    border-radius: 20px;
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
                    display: none;
                    flex-direction: column;
                    overflow: hidden;
                    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
                    color: #ffffff;
                    animation: cfSlideUp 0.25s ease forwards;
                }

                @keyframes cfSlideUp {
                    from { opacity: 0; transform: translateY(16px) scale(0.96); }
                    to { opacity: 1; transform: translateY(0) scale(1); }
                }

                .cf-chat-header {
                    padding: 13px 16px;
                    background: #1e293b;
                    border-bottom: 1.5px solid #334155;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .cf-header-title {
                    font-weight: 800;
                    font-size: 1.02rem;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    color: #ffffff;
                }

                .cf-header-badge {
                    font-size: 0.72rem;
                    background: rgba(16, 185, 129, 0.2);
                    border: 1px solid #10b981;
                    color: #10b981;
                    padding: 2px 7px;
                    border-radius: 999px;
                    font-weight: 700;
                }

                .cf-chat-close {
                    background: transparent;
                    border: none;
                    color: #94a3b8;
                    font-size: 1.25rem;
                    cursor: pointer;
                    padding: 4px 8px;
                    border-radius: 8px;
                    transition: all 0.2s;
                    line-height: 1;
                }

                .cf-chat-close:hover {
                    color: #ffffff;
                    background: #334155;
                }

                .cf-chat-chips {
                    display: flex;
                    gap: 6px;
                    padding: 8px 12px;
                    overflow-x: auto;
                    white-space: nowrap;
                    background: #0f172a;
                    border-bottom: 1px solid #1e293b;
                    scrollbar-width: thin;
                }

                .cf-chat-chip {
                    background: rgba(99, 102, 241, 0.18);
                    border: 1px solid #6366f1;
                    color: #e2e8f0;
                    font-size: 0.76rem;
                    font-weight: 700;
                    padding: 5px 11px;
                    border-radius: 50px;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    flex-shrink: 0;
                }

                .cf-chat-chip:hover {
                    background: #6366f1;
                    color: #ffffff;
                    transform: translateY(-1px);
                }

                .cf-chat-messages {
                    padding: 14px;
                    flex: 1;
                    overflow-y: auto;
                    max-height: 310px;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }

                .cf-msg {
                    max-width: 88%;
                    padding: 10px 14px;
                    border-radius: 14px;
                    font-size: 0.88rem;
                    line-height: 1.45;
                    word-break: break-word;
                }

                .cf-msg-bot {
                    align-self: flex-start;
                    background: #1e293b;
                    border: 1px solid #334155;
                    color: #f8fafc;
                    border-bottom-left-radius: 4px;
                }

                .cf-msg-user {
                    align-self: flex-end;
                    background: #4f46e5;
                    color: #ffffff;
                    border-bottom-right-radius: 4px;
                }

                .cf-chat-footer {
                    padding: 10px 14px;
                    background: #1e293b;
                    border-top: 1.5px solid #334155;
                    display: flex;
                    gap: 8px;
                }

                .cf-chat-input {
                    flex: 1;
                    background: #0f172a;
                    border: 1.5px solid #475569;
                    border-radius: 10px;
                    padding: 9px 12px;
                    color: #ffffff;
                    font-size: 0.88rem;
                    outline: none;
                    font-family: inherit;
                }

                .cf-chat-input:focus {
                    border-color: #818cf8;
                }

                .cf-chat-send {
                    background: #10b981;
                    color: #ffffff;
                    border: none;
                    border-radius: 10px;
                    padding: 9px 14px;
                    font-weight: 700;
                    font-size: 0.86rem;
                    cursor: pointer;
                    transition: background 0.2s;
                    font-family: inherit;
                }

                .cf-chat-send:hover {
                    background: #059669;
                }

                @media (max-width: 640px) {
                    #cf-chat-launcher {
                        bottom: 16px !important;
                        right: 16px !important;
                        width: 52px !important;
                        height: 52px !important;
                        padding: 0 !important;
                        border-radius: 50% !important;
                        justify-content: center !important;
                    }
                    .cf-launcher-text {
                        display: none !important;
                    }
                    .cf-online-indicator {
                        position: absolute !important;
                        top: 4px !important;
                        right: 4px !important;
                        width: 10px !important;
                        height: 10px !important;
                    }
                    #cf-chat-window {
                        bottom: 76px !important;
                        right: 12px !important;
                        left: 12px !important;
                        width: auto !important;
                        max-width: calc(100vw - 24px) !important;
                        max-height: 72vh !important;
                    }
                }
            </style>

            <div id="cf-chat-launcher" title="24/7 AI Assistant">
                <span style="font-size: 1.25rem;">💬</span>
                <span class="cf-launcher-text">AI Assistant</span>
                <span class="cf-online-indicator"></span>
            </div>

            <div id="cf-chat-window">
                <div class="cf-chat-header">
                    <div class="cf-header-title">
                        <span>🤖</span>
                        <span>ChronoFlow Assistant</span>
                        <span class="cf-header-badge">● 24/7 Live</span>
                    </div>
                    <button class="cf-chat-close" id="cf-close-btn" title="Band Karein">✕</button>
                </div>

                <div class="cf-chat-chips">
                    <div class="cf-chat-chip" data-q="Timer kaise chalayein?">⏱️ Timer Tips</div>
                    <div class="cf-chat-chip" data-q="Study schedule tips?">🧠 Study Tips</div>
                    <div class="cf-chat-chip" data-q="Pomodoro technique kya hai?">⚡ Pomodoro</div>
                    <div class="cf-chat-chip" data-q="Sound ya alarm ki maloomat?">🔊 Alarm Sound</div>
                </div>

                <div class="cf-chat-messages" id="cf-msgs">
                    <div class="cf-msg cf-msg-bot">
                        👋 <b>Assalam o Alaikum! Main aapka 24/7 AI Assistant hoon.</b><br><br>
                        Aap mujhse timer use karne, study schedule banane, ya kisi bhi feature ke baare me pooch sakte hain!
                    </div>
                </div>

                <div class="cf-chat-footer">
                    <input class="cf-chat-input" id="cf-input" placeholder="Apna sawal yahan likhein..." autocomplete="off" />
                    <button class="cf-chat-send" id="cf-send">Send 🚀</button>
                </div>
            </div>
            `;

            pdoc.body.appendChild(wrap);

            const launcher = pdoc.getElementById('cf-chat-launcher');
            const chatWin = pdoc.getElementById('cf-chat-window');
            const closeBtn = pdoc.getElementById('cf-close-btn');
            const inputField = pdoc.getElementById('cf-input');
            const sendBtn = pdoc.getElementById('cf-send');
            const msgsBox = pdoc.getElementById('cf-msgs');

            launcher.onclick = () => {
                if (chatWin.style.display === 'flex') {
                    chatWin.style.display = 'none';
                } else {
                    chatWin.style.display = 'flex';
                    setTimeout(() => inputField && inputField.focus(), 150);
                }
            };

            closeBtn.onclick = () => {
                chatWin.style.display = 'none';
            };

            function getReply(query) {
                const q = query.toLowerCase().trim();
                if (q.includes('salam') || q.includes('hello') || q.includes('hi') || q.includes('kese') || q.includes('kaise ho')) {
                    return "👋 <b>Walaikum Assalam!</b> Main bilkul theek hoon! Aap batayein aaj kaunsa study ya focus session start karna hai? 🎯";
                }
                if (q.includes('sound') || q.includes('audio') || q.includes('awaaz') || q.includes('alarm') || q.includes('bell')) {
                    return "🔊 <b>Sound Maloomat:</b> Countdown 0 par pohnchne par bell bajti hai.<br><b>Tip:</b> Browser security policy ke mutabiq pehle ek baar screen par START dabana zaroori hai.";
                }
                if (q.includes('preset') || q.includes('pomodoro') || q.includes('technique')) {
                    return "⚡ <b>Pomodoro Technique:</b> 25 minute parhai karein aur phir 5 minute Chai Break lein. Isse bina thakey lambe time tak focus barkarar rehta hai!";
                }
                if (q.includes('kaise') || q.includes('use') || q.includes('chale') || q.includes('start')) {
                    return "⏱️ <b>Timer Use Karna Aasaan Hai:</b><br>1. Koi sa preset chunein (jaise Study 25m).<br>2. Green <b>START</b> dabayein.<br>3. Rokne ke liye Pause aur shuru se lagane ke liye Reset dabayein!";
                }
                if (q.includes('study') || q.includes('schedule') || q.includes('tips') || q.includes('parh')) {
                    return "🧠 <b>Top Focus Tip:</b> Apne notifications mute karein, <b>'Deep Focus (45m)'</b> preset lagayein, aur ek target complete karein bina kisi distraction ke!";
                }
                return `🤖 <b>ChronoFlow Assistant:</b> Aapka sawal <i>"${query}"</i> note kar liya! Screen ke buttons se timer control karein ya koi aur sawal ho to poochein!`;
            }

            function addMsg(txt, isUser) {
                const el = pdoc.createElement('div');
                el.className = isUser ? 'cf-msg cf-msg-user' : 'cf-msg cf-msg-bot';
                el.innerHTML = txt;
                msgsBox.appendChild(el);
                msgsBox.scrollTop = msgsBox.scrollHeight;
            }

            function sendUserMsg() {
                const v = inputField.value.trim();
                if (!v) return;
                addMsg(v, true);
                inputField.value = '';
                setTimeout(() => {
                    const ans = getReply(v);
                    addMsg(ans, false);
                }, 280);
            }

            sendBtn.onclick = sendUserMsg;
            inputField.onkeydown = (e) => {
                if (e.key === 'Enter') sendUserMsg();
            };

            const chips = pdoc.querySelectorAll('.cf-chat-chip');
            chips.forEach(c => {
                c.onclick = () => {
                    const q = c.getAttribute('data-q');
                    addMsg(q, true);
                    setTimeout(() => {
                        const ans = getReply(q);
                        addMsg(ans, false);
                    }, 280);
                };
            });

        } catch(e) {
            console.error("Corner chatbot error:", e);
        }
    }

    // Run setup after slight delay to ensure parent document is ready
    setTimeout(setupCornerChatbot, 200);
</script>
</body>
</html>
"""

# Populate dynamic variables into template
hud_final = (
    hud_template
    .replace("__TASK_NAME__", st.session_state.task_name)
    .replace("__TOTAL_SECONDS__", str(st.session_state.total_seconds))
)

components.html(hud_final, height=440, scrolling=False)

# ---------------------------------------------------------
# Custom Time Input (High Contrast, Responsive)
# ---------------------------------------------------------
with st.expander("🛠️ Custom Time Set Karein (Apni marzi ka waqt)", expanded=False):
    t_tab1, t_tab2 = st.tabs(["🔢 Number Input", "✍️ Likh Kar Set Karein"])

    with t_tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            inp_h = st.number_input("Ghante", 0, 23, st.session_state.total_seconds // 3600)
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
# Completed Session Logger (Clear & Legible)
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
# Clean Minimal Footer
# ---------------------------------------------------------
st.markdown(
    """
    <div style="text-align: center; margin-top: 24px; padding: 14px; color: #94a3b8; font-size: 0.85rem; font-weight: 600;">
        <span>ChronoFlow Timer &bull; Simple, Modern & Fast</span>
    </div>
    """,
    unsafe_allow_html=True,
)
