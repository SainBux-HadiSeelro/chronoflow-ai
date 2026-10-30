# ⏱️ AETHR-CHRONOS // Agentic AI Temporal Orchestrator

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42+-FF4B4B.svg)](https://streamlit.io)
[![Agentic AI](https://img.shields.io/badge/Design-Agentic%20AI%20HUD-00f5d4.svg)](#)
[![Zero Latency](https://img.shields.io/badge/Engine-Client--Side%2060FPS-7928ca.svg)](#)

> **AETHR-CHRONOS** is a next-generation countdown timer and focus orchestrator built with an **Agentic AI** philosophy. Designed for developers, researchers, and power users who need high-precision temporal control without UI freezing, thread-blocking, or bland aesthetics.

---

## ⚡ Key Highlights & Upgrades

### 🧠 1. Agentic Natural Language Mission Parser
No need to fiddle with multiple number inputs. Simply type what you want in plain text:
- `"25m deep work on neural network fine-tuning"`
- `"1h 30m architecture review"`
- `"45s eye relaxation"`
- `"10 min chai break"`

The AI parser extracts duration and context automatically and deploys the mission!

### 🔮 2. Sci-Fi Cyberpunk HUD (60 FPS Non-Blocking)
- **Fluid Circular SVG Progress Ring**: Real-time glow animations that dynamically adjust with the remaining percentage.
- **Zero-Freeze State Machine**: Resolves the classic Streamlit `time.sleep()` blocking bug. You can **Pause**, **Resume**, **Reset**, and instantly bump (**+1m**, **+5m**, **+10m**) without freezing your backend.

### 🎵 3. Zero-Dependency Web Audio Synthesis
- **Dynamic Harmonic Chimes**: Synthesizes multi-tone alert chords upon mission completion using the browser's Web Audio API.
- **Cyberpunk Brown Noise Ambience**: Optional ambient background sound generated directly via audio buffers to enhance deep focus without loading external MP3 files.

### 📊 4. Focus Telemetry & Mission Archiving
- Daily goal tracking and progress visualizers.
- Live streak counter and temporal efficiency metrics.
- Mission archive log to record completed sprints with custom notes.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
Ensure you have **Python 3.12+** installed on your system.

### 2. Install Dependencies
```bash
python -m pip install -e .
```
*(or simply install Streamlit directly: `python -m pip install "streamlit>=1.42.0"`)*

### 3. Launch the Application
Run the Streamlit app:
```bash
python -m streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 🎮 Tactical Presets

| Preset | Duration | Optimized For |
| :--- | :--- | :--- |
| **🧠 Deep Flow** | 25 Min | Core cognitive coding, model training, algorithm design |
| **⚡ Hyper Sprint** | 15 Min | Rapid debugging, quick reviews, hotfixes |
| **☕ Synaptic Recharge** | 5 Min | Mental cooldown, hydration, physical stretch |
| **🚀 Macro Flow** | 50 Min | High-level system architecture, prolonged deep work |

---

## 🏗️ Architecture

```
6_Countdown Timer Python Project/
├── app.py              # AETHR-CHRONOS Flagship Application (Streamlit + HUD)
├── pyproject.toml      # Dependency & package configuration
├── README.md           # Documentation & user guide
└── .gitignore          # Version control ignore rules
```

---

## 🛡️ License
MIT License. Crafted with precision by an **Agentic AI Developer**.
