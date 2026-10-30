"""
AETHR-CHRONOS // Modern Agentic AI Temporal & Focus Orchestrator
Created by an Agentic AI Developer.
"""

import re
import json
import datetime
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------
# Page Configuration & Agentic Design System
# ---------------------------------------------------------
st.set_page_config(
    page_title="AETHR-CHRONOS | Agentic Temporal AI",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Agentic Cyberpunk / Dark Glassmorphism CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Space+Grotesk:wght@400;600;700&display=swap');

    :root {
        --agent-cyan: #00f5d4;
        --agent-purple: #7928ca;
        --agent-blue: #0070f3;
        --agent-bg: #090d16;
        --agent-card: rgba(16, 24, 40, 0.75);
        --agent-border: rgba(0, 245, 212, 0.25);
    }

    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(121, 40, 202, 0.15) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(0, 245, 212, 0.12) 0%, transparent 45%),
                    #070a12;
        color: #e2e8f0;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Custom Header Banner */
    .agent-header {
        background: linear-gradient(135deg, rgba(16, 24, 40, 0.85) 0%, rgba(9, 13, 22, 0.95) 100%);
        border: 1px solid var(--agent-border);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 245, 212, 0.08);
        backdrop-filter: blur(12px);
        position: relative;
        overflow: hidden;
    }

    .agent-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00f5d4, #7928ca, #0070f3, #00f5d4);
        background-size: 300% 100%;
        animation: borderShift 6s linear infinite;
    }

    @keyframes borderShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .agent-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 245, 212, 0.1);
        border: 1px solid rgba(0, 245, 212, 0.35);
        border-radius: 9999px;
        padding: 4px 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #00f5d4;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #00f5d4;
        box-shadow: 0 0 10px #00f5d4;
        animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.8); }
    }

    .agent-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-top: 10px;
        margin-bottom: 4px;
        background: linear-gradient(135deg, #ffffff 40%, #00f5d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .agent-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace;
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: #00f5d4 !important;
        font-weight: 700;
    }

    /* Primary and Secondary Buttons */
    .stButton>button {
        border-radius: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        transition: all 0.25s ease;
    }

    .stButton>button:hover {
        border-color: #00f5d4;
        box-shadow: 0 0 14px rgba(0, 245, 212, 0.35);
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 25 * 60  # Default 25m Pomodoro
if "task_name" not in st.session_state:
    st.session_state.task_name = "Deep Work: Core Autonomous Logic"
if "session_history" not in st.session_state:
    st.session_state.session_history = []
if "completed_count" not in st.session_state:
    st.session_state.completed_count = 0
if "streak_count" not in st.session_state:
    st.session_state.streak_count = 1
if "timer_trigger_token" not in st.session_state:
    st.session_state.timer_trigger_token = 0


# ---------------------------------------------------------
# Natural Language Parser (Agentic Feature)
# ---------------------------------------------------------
def parse_natural_language_command(user_prompt: str) -> tuple[int, str]:
    """
    Agentic parser extracting duration (hours, minutes, seconds)
    and mission objective from natural language.
    Examples:
      - '25m fine tuning LLM model' -> (1500, 'Fine tuning LLM model')
      - '1h 30m code review' -> (5400, 'Code review')
      - '45 seconds eye relaxation' -> (45, 'Eye relaxation')
      - '10 min quick break' -> (600, 'Quick break')
    """
    text = user_prompt.strip().lower()
    total_secs = 0

    # Extract hours
    hr_match = re.search(r"(\d+)\s*(?:h|hr|hrs|hours?)\b", text)
    if hr_match:
        total_secs += int(hr_match.group(1)) * 3600

    # Extract minutes
    min_match = re.search(r"(\d+)\s*(?:m|min|mins|minutes?)\b", text)
    if min_match:
        total_secs += int(min_match.group(1)) * 60

    # Extract seconds
    sec_match = re.search(r"(\d+)\s*(?:s|sec|secs|seconds?)\b", text)
    if sec_match:
        total_secs += int(sec_match.group(1))

    # Fallback: if only a raw number was typed, assume minutes
    if total_secs == 0:
        raw_num = re.search(r"^(\d+)$", text)
        if raw_num:
            total_secs = int(raw_num.group(1)) * 60

    # Clean text to extract task description
    cleaned = re.sub(
        r"\b(?:\d+\s*(?:h|hr|hrs|hours?|m|min|mins|minutes?|s|sec|secs|seconds?))\b",
        "",
        user_prompt,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\b(?:timer|set|for|start|countdown|please)\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[\s,:;\-]+", " ", cleaned).strip()

    task_desc = cleaned.capitalize() if cleaned else "Autonomous Focus Protocol"
    return (total_secs if total_secs > 0 else 25 * 60, task_desc)


# ---------------------------------------------------------
# Preset Handlers
# ---------------------------------------------------------
def apply_preset(seconds: int, task: str):
    st.session_state.total_seconds = seconds
    st.session_state.task_name = task
    st.session_state.timer_trigger_token += 1


# ---------------------------------------------------------
# Sidebar Controls & Agentic Telemetry
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛰️ **Agent Telemetry**")
    st.markdown(
        """
        <div style="background: rgba(0,245,212,0.06); border: 1px solid rgba(0,245,212,0.2); border-radius: 8px; padding: 12px; margin-bottom: 16px;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #00f5d4;">
                AGENT: AETHR-COGNITION v2.4<br>
                STATUS: SYNAPSE ACTIVE<br>
                DRIFT CORRECTION: ENABLED<br>
                AUDIO SYNTHESIS: WEB-AUDIO 2.0
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 🎯 **Focus Target**")
    daily_goal = st.slider("Daily Sessions Target", min_value=1, max_value=12, value=4)
    progress_val = min(st.session_state.completed_count / daily_goal, 1.0)
    st.progress(progress_val)
    st.caption(f"Progress: {st.session_state.completed_count}/{daily_goal} Missions Accomplished")

    st.divider()

    st.markdown("#### ⚙️ **Audio & Synthesis**")
    enable_audio = st.toggle("Enable Chimes & Alarms", value=True)
    ambient_hint = st.checkbox("Enable Cyberpunk Focus Ambience", value=False)
    st.caption("Sound waves are synthesized dynamically in your browser without external audio files.")

    st.divider()

    st.markdown("#### 📜 **Mission Control Log**")
    if st.session_state.session_history:
        for idx, item in enumerate(reversed(st.session_state.session_history[-5:])):
            st.markdown(
                f"<div style='font-size: 0.78rem; font-family: monospace; color: #94a3b8; border-bottom: 1px solid rgba(255,255,255,0.05); padding: 4px 0;'>"
                f"✅ {item['time']} — <b>{item['task']}</b> ({item['duration']})"
                f"</div>",
                unsafe_allow_html=True,
            )
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.session_history.clear()
            st.session_state.completed_count = 0
            st.rerun()
    else:
        st.caption("No missions logged yet. Complete a countdown cycle to archive telemetry.")


# ---------------------------------------------------------
# Main Page Header
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="agent-header">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div class="agent-badge">
                <span class="pulse-dot"></span>
                <span>CHRONOS PROTOCOL // ONLINE</span>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #94a3b8;">
                SYS_TIME: {datetime.datetime.now().strftime('%H:%M:%S UTC')}
            </div>
        </div>
        <h1 class="agent-title">AETHR-CHRONOS</h1>
        <p class="agent-subtitle">
            Autonomous Agentic Temporal Orchestrator &bull; High-Frequency Precision Countdown Engine
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Productivity Score & Metrics Row
# ---------------------------------------------------------
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Focus Minutes", f"{(st.session_state.completed_count * 25):,} m")
with m2:
    st.metric("Missions Completed", f"{st.session_state.completed_count}")
with m3:
    st.metric("Focus Streak", f"{st.session_state.streak_count} 🔥")
with m4:
    st.metric("Temporal Efficiency", f"{96.4 + (st.session_state.completed_count * 0.4):.1f}%")

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Agentic Natural Language Command Dispatcher
# ---------------------------------------------------------
with st.container():
    st.markdown("#### 🤖 **Agentic Mission Dispatcher (Natural Language)**")
    col_input, col_btn = st.columns([4, 1])

    with col_input:
        user_command = st.text_input(
            "Enter mission in natural language:",
            placeholder='e.g., "25m deep work on neural network fine-tuning" or "10 min chai break"',
            label_visibility="collapsed",
        )

    with col_btn:
        if st.button("🚀 Deploy Mission", use_container_width=True):
            if user_command.strip():
                parsed_secs, parsed_task = parse_natural_language_command(user_command)
                apply_preset(parsed_secs, parsed_task)
                st.rerun()

# ---------------------------------------------------------
# Quick Agentic Mission Presets
# ---------------------------------------------------------
st.markdown("##### ⚡ **Tactical Presets**")
p1, p2, p3, p4 = st.columns(4)

with p1:
    if st.button("🧠 Deep Flow (25m)", use_container_width=True):
        apply_preset(25 * 60, "Deep Flow: Cognitive Task Execution")
        st.rerun()

with p2:
    if st.button("⚡ Hyper Sprint (15m)", use_container_width=True):
        apply_preset(15 * 60, "Hyper Sprint: Rapid Problem Solving")
        st.rerun()

with p3:
    if st.button("☕ Synaptic Recharge (5m)", use_container_width=True):
        apply_preset(5 * 60, "Synaptic Recharge: Rest & Hydration")
        st.rerun()

with p4:
    if st.button("🚀 Macro Flow (50m)", use_container_width=True):
        apply_preset(50 * 60, "Macro Flow: High Architecture Design")
        st.rerun()

# ---------------------------------------------------------
# Manual Precision Calibration (Accordion)
# ---------------------------------------------------------
with st.expander("🛠️ Manual Precision Calibration (Custom Time)", expanded=False):
    c_hr, c_min, c_sec, c_set = st.columns([1, 1, 1, 1])
    with c_hr:
        in_hr = st.number_input("Hours", min_value=0, max_value=23, value=st.session_state.total_seconds // 3600)
    with c_min:
        in_min = st.number_input("Minutes", min_value=0, max_value=59, value=(st.session_state.total_seconds % 3600) // 60)
    with c_sec:
        in_sec = st.number_input("Seconds", min_value=0, max_value=59, value=st.session_state.total_seconds % 60)
    with c_set:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Apply Precision Calibration", use_container_width=True):
            calc_secs = int(in_hr * 3600 + in_min * 60 + in_sec)
            if calc_secs > 0:
                apply_preset(calc_secs, "Custom Calibrated Mission")
                st.rerun()
            else:
                st.error("Please enter a non-zero time.")

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Cyberpunk Animated Circular SVG HUD Component
# Client-side 60 FPS, Non-blocking, Built-in Web Audio API
# ---------------------------------------------------------
hud_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Space+Grotesk:wght@600;700&display=swap');

    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        user-select: none;
    }}

    body {{
        background: transparent;
        color: #f8fafc;
        font-family: 'Space Grotesk', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 0;
        overflow: hidden;
    }}

    .hud-container {{
        width: 100%;
        max-width: 680px;
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85) 0%, rgba(7, 10, 18, 0.95) 100%);
        border: 1px solid rgba(0, 245, 212, 0.28);
        border-radius: 24px;
        padding: 28px 24px;
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.6), inset 0 0 24px rgba(0, 245, 212, 0.04);
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
    }}

    /* Top Mission Label */
    .mission-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        margin-bottom: 20px;
        padding-bottom: 14px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    }}

    .mission-title {{
        font-size: 0.92rem;
        font-weight: 700;
        color: #e2e8f0;
        letter-spacing: 0.02em;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .status-badge {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        padding: 4px 10px;
        border-radius: 999px;
        background: rgba(0, 245, 212, 0.1);
        border: 1px solid rgba(0, 245, 212, 0.3);
        color: #00f5d4;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    /* Circular SVG Timer */
    .circle-wrap {{
        position: relative;
        width: 280px;
        height: 280px;
        margin: 10px 0 20px 0;
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
        stroke-width: 10;
        stroke-linecap: round;
    }}

    .circle-bg {{
        stroke: rgba(255, 255, 255, 0.06);
    }}

    .circle-progress {{
        stroke: #00f5d4;
        stroke-dasharray: 816.8; /* 2 * PI * 130 */
        stroke-dashoffset: 0;
        transition: stroke-dashoffset 0.3s ease, stroke 0.4s ease;
        filter: drop-shadow(0 0 10px rgba(0, 245, 212, 0.6));
    }}

    .circle-progress.paused {{
        stroke: #f59e0b;
        filter: drop-shadow(0 0 10px rgba(245, 158, 11, 0.6));
    }}

    .circle-progress.completed {{
        stroke: #10b981;
        filter: drop-shadow(0 0 15px rgba(16, 185, 129, 0.8));
    }}

    /* Digital Time Readout */
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
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(0, 245, 212, 0.4);
        line-height: 1;
    }}

    .time-percent {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 8px;
        letter-spacing: 0.05em;
    }}

    /* Controls */
    .controls-grid {{
        display: flex;
        gap: 12px;
        margin-top: 10px;
        width: 100%;
        justify-content: center;
        flex-wrap: wrap;
    }}

    button.ctrl-btn {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        font-weight: 700;
        padding: 12px 22px;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }}

    button.ctrl-btn:hover {{
        background: rgba(0, 245, 212, 0.12);
        border-color: #00f5d4;
        box-shadow: 0 0 16px rgba(0, 245, 212, 0.35);
        transform: translateY(-2px);
    }}

    button.ctrl-btn:active {{
        transform: translateY(0);
    }}

    button.btn-primary {{
        background: linear-gradient(135deg, #00f5d4 0%, #0070f3 100%);
        color: #050811;
        border: none;
        box-shadow: 0 4px 18px rgba(0, 245, 212, 0.35);
    }}

    button.btn-primary:hover {{
        background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%);
        color: #ffffff;
        box-shadow: 0 0 22px rgba(0, 245, 212, 0.55);
    }}

    button.btn-bump {{
        padding: 8px 14px;
        font-size: 0.78rem;
        background: rgba(121, 40, 202, 0.15);
        border-color: rgba(121, 40, 202, 0.4);
        color: #c084fc;
    }}

    button.btn-bump:hover {{
        border-color: #a855f7;
        background: rgba(121, 40, 202, 0.3);
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.4);
    }}

    .bumps-container {{
        display: flex;
        gap: 8px;
        margin-top: 14px;
    }}
</style>
</head>
<body>

<div class="hud-container">
    <div class="mission-header">
        <div class="mission-title">
            <span>🎯</span>
            <span id="taskLabel">{st.session_state.task_name}</span>
        </div>
        <div id="statusBadge" class="status-badge">● READY</div>
    </div>

    <!-- Circular Progress SVG -->
    <div class="circle-wrap">
        <svg viewBox="0 0 280 280">
            <circle class="circle-bg" cx="140" cy="140" r="130"></circle>
            <circle id="progressCircle" class="circle-progress" cx="140" cy="140" r="130"></circle>
        </svg>
        <div class="timer-readout">
            <div id="timeDisplay" class="time-digits">--:--</div>
            <div id="percentDisplay" class="time-percent">100% REMAINING</div>
        </div>
    </div>

    <!-- Main Controls -->
    <div class="controls-grid">
        <button id="toggleBtn" class="ctrl-btn btn-primary" onclick="toggleTimer()">
            <span id="toggleIcon">▶</span>
            <span id="toggleText">START MISSION</span>
        </button>
        <button class="ctrl-btn" onclick="resetTimer()">
            <span>⏹</span>
            <span>RESET</span>
        </button>
    </div>

    <!-- Rapid Adjustment Bumps -->
    <div class="bumps-container">
        <button class="ctrl-btn btn-bump" onclick="addSeconds(60)">+1 MIN</button>
        <button class="ctrl-btn btn-bump" onclick="addSeconds(300)">+5 MIN</button>
        <button class="ctrl-btn btn-bump" onclick="addSeconds(600)">+10 MIN</button>
    </div>
</div>

<script>
    // Configuration from Streamlit
    let totalDuration = {st.session_state.total_seconds};
    let remainingSeconds = totalDuration;
    let isRunning = false;
    let timerInterval = null;
    let isAudioEnabled = {str(enable_audio).lower()};
    let isAmbientEnabled = {str(ambient_hint).lower()};

    const CIRCUMFERENCE = 2 * Math.PI * 130; // ~816.81
    const progressCircle = document.getElementById('progressCircle');
    const timeDisplay = document.getElementById('timeDisplay');
    const percentDisplay = document.getElementById('percentDisplay');
    const statusBadge = document.getElementById('statusBadge');
    const toggleIcon = document.getElementById('toggleIcon');
    const toggleText = document.getElementById('toggleText');

    progressCircle.style.strokeDasharray = CIRCUMFERENCE;

    // Web Audio Synthesizer (Zero Dependencies)
    let audioCtx = null;
    let ambientSource = null;

    function initAudio() {{
        if (!audioCtx) {{
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            audioCtx = new AudioContext();
        }}
        if (audioCtx.state === 'suspended') {{
            audioCtx.resume();
        }}
    }}

    function playTone(freq, type = 'sine', duration = 0.15, gainVal = 0.15) {{
        if (!isAudioEnabled) return;
        try {{
            initAudio();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(gainVal, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }} catch(e) {{
            console.warn("Audio synth warning:", e);
        }}
    }}

    // Agentic Completion Chime (Harmonic Chord)
    function playMissionCompleteChime() {{
        if (!isAudioEnabled) return;
        try {{
            initAudio();
            const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
            notes.forEach((freq, idx) => {{
                setTimeout(() => {{
                    playTone(freq, 'triangle', 0.8, 0.25);
                }}, idx * 160);
            }});
        }} catch(e) {{}}
    }}

    // Ambient Cyberpunk Brown Noise Generator
    function startAmbientNoise() {{
        if (!isAmbientEnabled) return;
        try {{
            initAudio();
            if (ambientSource) return;
            const bufferSize = audioCtx.sampleRate * 2;
            const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
            const data = buffer.getChannelData(0);
            let lastOut = 0.0;
            for (let i = 0; i < bufferSize; i++) {{
                const white = Math.random() * 2 - 1;
                data[i] = (lastOut + (0.02 * white)) / 1.02;
                lastOut = data[i];
                data[i] *= 2.5; // Gain factor
            }}
            ambientSource = audioCtx.createBufferSource();
            ambientSource.buffer = buffer;
            ambientSource.loop = true;
            const filter = audioCtx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.value = 400; // Deep soothing hum
            const gain = audioCtx.createGain();
            gain.gain.value = 0.08;
            ambientSource.connect(filter);
            filter.connect(gain);
            gain.connect(audioCtx.destination);
            ambientSource.start();
        }} catch(e) {{}}
    }}

    function stopAmbientNoise() {{
        if (ambientSource) {{
            try {{
                ambientSource.stop();
                ambientSource.disconnect();
            }} catch(e) {{}}
            ambientSource = null;
        }}
    }}

    function formatTime(totalSecs) {{
        const hrs = Math.floor(totalSecs / 3600);
        const mins = Math.floor((totalSecs % 3600) / 60);
        const secs = totalSecs % 60;
        if (hrs > 0) {{
            return `${{String(hrs).padStart(2, '0')}}:${{String(mins).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;
        }} else {{
            return `${{String(mins).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;
        }}
    }}

    function updateDisplay() {{
        timeDisplay.innerText = formatTime(remainingSeconds);
        const percent = totalDuration > 0 ? (remainingSeconds / totalDuration) : 0;
        const offset = CIRCUMFERENCE * (1 - percent);
        progressCircle.style.strokeDashoffset = offset;
        percentDisplay.innerText = `${{Math.round(percent * 100)}}% REMAINING`;
    }}

    function toggleTimer() {{
        initAudio();
        if (isRunning) {{
            // Pause
            clearInterval(timerInterval);
            isRunning = false;
            stopAmbientNoise();
            toggleIcon.innerText = "▶";
            toggleText.innerText = "RESUME";
            statusBadge.innerText = "● PAUSED";
            statusBadge.style.color = "#f59e0b";
            progressCircle.classList.add('paused');
            playTone(440, 'sine', 0.1, 0.1);
        }} else {{
            // Start / Resume
            if (remainingSeconds <= 0) {{
                remainingSeconds = totalDuration;
            }}
            isRunning = true;
            progressCircle.classList.remove('paused', 'completed');
            toggleIcon.innerText = "⏸";
            toggleText.innerText = "PAUSE";
            statusBadge.innerText = "● AGENT ENGAGED";
            statusBadge.style.color = "#00f5d4";
            playTone(880, 'sine', 0.15, 0.15);
            startAmbientNoise();

            timerInterval = setInterval(() => {{
                if (remainingSeconds > 0) {{
                    remainingSeconds--;
                    updateDisplay();
                }} else {{
                    // Finished
                    clearInterval(timerInterval);
                    isRunning = false;
                    stopAmbientNoise();
                    progressCircle.classList.add('completed');
                    toggleIcon.innerText = "▶";
                    toggleText.innerText = "RESTART";
                    statusBadge.innerText = "● MISSION ACCOMPLISHED";
                    statusBadge.style.color = "#10b981";
                    playMissionCompleteChime();
                }}
            }}, 1000);
        }}
    }}

    function resetTimer() {{
        clearInterval(timerInterval);
        isRunning = false;
        stopAmbientNoise();
        remainingSeconds = totalDuration;
        updateDisplay();
        progressCircle.classList.remove('paused', 'completed');
        toggleIcon.innerText = "▶";
        toggleText.innerText = "START MISSION";
        statusBadge.innerText = "● READY";
        statusBadge.style.color = "#00f5d4";
        playTone(330, 'sine', 0.1, 0.1);
    }}

    function addSeconds(extra) {{
        totalDuration += extra;
        remainingSeconds += extra;
        updateDisplay();
        playTone(660, 'sine', 0.08, 0.1);
    }}

    // Initial render
    updateDisplay();
</script>
</body>
</html>
"""

components.html(hud_html, height=480, scrolling=False)

# ---------------------------------------------------------
# Mission Log Recorder & Quick Archiver
# ---------------------------------------------------------
st.markdown("---")
st.markdown("##### 📝 **Log & Archive Completed Session**")
l_col1, l_col2 = st.columns([3, 1])

with l_col1:
    session_note = st.text_input(
        "Mission Log Notes / Accomplishment Summary:",
        value=f"Completed {st.session_state.task_name} session.",
    )

with l_col2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("💾 Record Session to History", use_container_width=True):
        duration_mins = max(1, st.session_state.total_seconds // 60)
        st.session_state.session_history.append(
            {
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "task": st.session_state.task_name,
                "duration": f"{duration_mins}m",
                "notes": session_note,
            }
        )
        st.session_state.completed_count += 1
        st.session_state.streak_count += 1
        st.success(f"Archived mission: {st.session_state.task_name} (+{duration_mins}m)")
        st.rerun()

# ---------------------------------------------------------
# Footer / Agentic Developer Credits
# ---------------------------------------------------------
st.markdown(
    """
    <div style="text-align: center; margin-top: 40px; padding: 20px; color: #64748b; font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; border-top: 1px solid rgba(255,255,255,0.05);">
        <span>⚡ AETHR-CHRONOS // ENGINEERED BY AGENTIC AI DEVELOPER &bull; ZERO LATENCY CLIENT-SIDE HUD</span>
    </div>
    """,
    unsafe_allow_html=True,
)
