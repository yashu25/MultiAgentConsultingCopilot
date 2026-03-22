# MultiAgentConsultingCopilot
# 🎯 PitchReady AI

> Pre-pitch competitive intelligence for consultants & BD teams — powered by free LLMs

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)](https://streamlit.io)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Free_Models-green)](https://openrouter.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🤔 What is PitchReady AI?

Every consultant and BD professional knows the feeling — you have a big pitch tomorrow and you don't know who else is in the room, what objections are coming, or how to open strong.

**PitchReady AI** solves this. Enter your client name, deal context, and engagement type — four AI agents build your complete competitive brief in minutes.

---

## 🤖 The 4-Agent Pipeline
```
🔍 Landscape    →    📋 Battlecard    →    💬 Objection    →    🎯 Pitch
   Scanner            Builder              Handler             Sharpener
```

| Agent | What it does | Output |
|-------|-------------|--------|
| 🔍 **Landscape Scanner** | Researches the client, identifies likely competitors pitching for the same deal | Client intel, who's in the room, decision dynamics |
| 📋 **Battlecard Builder** | Builds a battlecard for each competitor | Their pitch, their weaknesses, how to beat them, landmine questions |
| 💬 **Objection Handler** | Prepares word-for-word responses to the 6 most likely objections | Exact language, hidden concerns, follow-up questions |
| 🎯 **Pitch Sharpener** | Crafts your opening, POV, closing move, and power questions | Killer opener, value story, pre-meeting checklist |

---

## ✨ What You Get

- **Client Intel** — key facts, strategic priorities, known pain points
- **Competitor Battlecards** — their pitch, weaknesses, and how to beat them
- **Landmine Questions** — questions that make the client doubt your competitors
- **Objection Playbook** — word-for-word responses to price, vendor, timeline objections
- **Killer Opening** — first 30 seconds of your pitch, client-specific
- **Unique POV** — the 1 insight only you can credibly say
- **Closing Strategy** — exactly what to ask for at the end of the meeting
- **5 Power Questions** — questions that position you as the smartest firm in the room
- **Downloadable Brief** — full `.md` file to share with your team

---

## 🆓 100% Free — No Paid APIs

Just one free API key from OpenRouter. No credit card ever.

Models used (auto-fallback if one is rate-limited):

| Model | Provider |
|-------|----------|
| `google/gemma-3-27b-it:free` | Google |
| `meta-llama/llama-3.3-70b-instruct:free` | Meta |
| `mistralai/mistral-7b-instruct:free` | Mistral |
| `qwen/qwen3-8b:free` | Alibaba |
| `microsoft/phi-3-mini-128k-instruct:free` | Microsoft |

---

## ⚡ Quick Start

### Step 1 — Get free API key (2 min)
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up — no credit card needed
3. API Keys → Create Key → Copy (`sk-or-v1-...`)

### Step 2 — Run locally
```bash
git clone https://github.com/yourusername/pitchready-ai.git
cd pitchready-ai
pip install streamlit requests
streamlit run app.py
```

### Step 3 — Deploy free on Streamlit Cloud
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → `app.py` → Deploy
4. Share the live link!

---

## 🚀 How to Use

1. Paste your **OpenRouter API key** in the sidebar
2. Enter **client name** and **industry**
3. Select **engagement type** (strategy, tech implementation, sales pitch, etc.)
4. Add **deal context** — the more detail, the sharper the brief
5. Click **Build My Pitch Brief**
6. Watch all 4 agents run in sequence
7. Download the complete brief as `.md`

---

## 💡 Example Use Cases

- **Management Consultant** — pitching a digital transformation to a bank, wants to know who else is pitching and how to position against them
- **SaaS Sales** — enterprise deal, needs battlecards against 3 known competitors
- **Startup BD** — pitching a partnership, wants to anticipate objections
- **Freelance Consultant** — new client pitch, needs to sound like they've done their homework

---

## 📁 Structure
```
pitchready-ai/
├── app.py              ← Main application (single file, no dependencies)
├── requirements.txt    ← streamlit, requests
└── README.md
```

**requirements.txt:**
```
streamlit>=1.35.0
requests>=2.31.0
```

---

## 🗺️ Roadmap

- [ ] Export to PDF / PowerPoint
- [ ] Save and compare briefs across deals
- [ ] Industry-specific prompt tuning
- [ ] Team sharing and collaboration

---

*Built with ❤️ · Free forever · No credit card needed*
