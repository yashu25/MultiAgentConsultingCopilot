import streamlit as st
import requests
import json

MODELS = [
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "qwen/qwen3-8b:free",
    "microsoft/phi-3-mini-128k-instruct:free",
]

def call_llm(api_key, prompt, placeholder=None, css_class="out", max_tokens=1400):
    for m in MODELS:
        full = ""
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://pitchready.streamlit.app",
                    "X-Title": "PitchReady AI"
                },
                json={
                    "model": m,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True,
                    "max_tokens": max_tokens
                },
                stream=True, timeout=90
            )
            if r.status_code in [429, 404]:
                continue
            if r.status_code != 200:
                raise Exception(f"API Error {r.status_code}: {r.text}")
            for line in r.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: ") and line != "data: [DONE]":
                        try:
                            delta = json.loads(line[6:])["choices"][0]["delta"].get("content", "")
                            if delta:
                                full += delta
                                if placeholder:
                                    placeholder.markdown(
                                        f'<div class="{css_class}">{full}▌</div>',
                                        unsafe_allow_html=True
                                    )
                        except: pass
            if placeholder:
                placeholder.markdown(f'<div class="{css_class}">{full}</div>', unsafe_allow_html=True)
            return full, m
        except Exception as e:
            if "429" in str(e) or "404" in str(e): continue
            raise e
    raise Exception("All models are rate-limited. Please wait 1-2 minutes and retry.")

st.set_page_config(page_title="PitchReady AI", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
.stApp { background: #FAFAF7; color: #141410; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3.5rem !important; max-width: 1280px !important; }

[data-testid="stSidebar"] { background: #141410 !important; }
[data-testid="stSidebar"] * { color: #e8e4d8 !important; }
[data-testid="stSidebar"] .stTextInput input { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.12) !important; color: #e8e4d8 !important; border-radius: 8px !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important; }
[data-testid="stSidebar"] .stSelectbox > div > div { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 8px !important; }
[data-testid="stSidebar"] label { color: rgba(255,255,255,0.4) !important; font-size: 0.65rem !important; text-transform: uppercase !important; letter-spacing: 1.2px !important; }
[data-testid="stSidebar"] a { color: #d4a843 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.06) !important; }

/* HEADER */
.eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; letter-spacing: 2.5px; text-transform: uppercase; color: #9a8c6e; margin-bottom: 14px; }
.hero-title { font-family: 'DM Serif Display', serif; font-size: 3rem; font-weight: 400; color: #141410; line-height: 1.1; margin-bottom: 12px; letter-spacing: -0.5px; }
.hero-title em { font-style: italic; color: #c4882a; }
.hero-sub { font-size: 1rem; color: #6b6650; font-weight: 300; line-height: 1.65; margin-bottom: 8px; max-width: 560px; }
.divider { border: none; border-top: 1px solid #e8e4d8; margin: 24px 0 32px; }

/* FORM */
.sec-label { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; color: #9a8c6e; margin-bottom: 16px; display: flex; align-items: center; gap: 10px; }
.sec-label::after { content: ''; flex: 1; height: 1px; background: #e8e4d8; }

.stTextArea textarea { background: white !important; border: 1.5px solid #e0dac8 !important; border-radius: 10px !important; color: #141410 !important; font-family: 'Outfit', sans-serif !important; font-size: 0.9rem !important; line-height: 1.7 !important; padding: 14px 16px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important; }
.stTextArea textarea:focus { border-color: #c4882a !important; box-shadow: 0 0 0 3px rgba(196,136,42,0.1) !important; }
.stTextArea textarea::placeholder { color: #b8b09a !important; }
.stSelectbox > div > div { background: white !important; border: 1.5px solid #e0dac8 !important; border-radius: 10px !important; color: #141410 !important; font-size: 0.88rem !important; }
.stTextInput input { background: white !important; border: 1.5px solid #e0dac8 !important; border-radius: 10px !important; color: #141410 !important; font-size: 0.88rem !important; }
label { font-size: 0.78rem !important; font-weight: 600 !important; color: #3a3520 !important; }

/* BUTTON */
.stButton > button { background: #141410 !important; color: #faf8f0 !important; border: none !important; border-radius: 10px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.92rem !important; font-weight: 600 !important; padding: 14px 28px !important; width: 100% !important; box-shadow: 0 4px 14px rgba(20,20,16,0.18) !important; transition: all 0.2s !important; letter-spacing: 0.2px !important; }
.stButton > button:hover { background: #2a2820 !important; transform: translateY(-1px) !important; }

/* AGENT STEPS */
.step-row { display: flex; align-items: center; gap: 6px; margin-bottom: 20px; flex-wrap: wrap; }
.step { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; padding: 5px 12px; border-radius: 100px; border: 1px solid #e0dac8; color: #9a8c6e; background: white; letter-spacing: 0.5px; }
.step.on { background: #141410; color: #faf8f0; border-color: #141410; }
.step-arrow { color: #c4882a; font-size: 0.8rem; }

.agent-label { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; padding: 2px 10px; border-radius: 100px; font-weight: 600; letter-spacing: 0.5px; display: inline-block; margin-right: 8px; }
.lbl-1 { background: #fef9ec; color: #92600e; border: 1px solid #f0d88a; }
.lbl-2 { background: #f0f7ff; color: #1a4a8a; border: 1px solid #b8d4f8; }
.lbl-3 { background: #f0fff8; color: #0a5c3a; border: 1px solid #90e0bc; }
.lbl-4 { background: #fff5f8; color: #8a1a3a; border: 1px solid #f8b8cc; }
.agent-title { font-family: 'DM Serif Display', serif; font-size: 1.05rem; color: #141410; }
.agent-row { display: flex; align-items: center; margin: 20px 0 10px; padding-bottom: 10px; border-bottom: 1px solid #eeead8; }

.out { background: white; border: 1px solid #e0dac8; border-radius: 14px; padding: 24px 28px; font-family: 'Outfit', sans-serif; font-size: 0.9rem; line-height: 1.85; color: #3a3520; box-shadow: 0 2px 16px rgba(0,0,0,0.05); margin-bottom: 8px; }
.out-1 { border-left: 3px solid #d4a843; }
.out-2 { border-left: 3px solid #4a90d4; }
.out-3 { border-left: 3px solid #3ab87a; }
.out-4 { border-left: 3px solid #d44a6a; }

.empty { background: white; border: 1.5px dashed #d8d0b8; border-radius: 14px; padding: 56px 40px; text-align: center; }
.empty-icon { font-size: 3rem; margin-bottom: 16px; }
.empty-title { font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: #6b6650; margin-bottom: 10px; }
.empty-sub { font-size: 0.85rem; color: #9a8c6e; line-height: 1.7; margin-bottom: 20px; }
.chip { display: inline-block; background: #f5f0e4; color: #6b5830; font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; padding: 4px 10px; border-radius: 6px; margin: 3px; }

.stDownloadButton > button { background: white !important; color: #3a3520 !important; border: 1.5px solid #e0dac8 !important; border-radius: 10px !important; font-size: 0.82rem !important; width: 100% !important; margin-top: 12px !important; box-shadow: none !important; }
.stDownloadButton > button:hover { border-color: #c4882a !important; color: #c4882a !important; }

.footer { margin-top: 56px; padding-top: 20px; border-top: 1px solid #e8e4d8; font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #b8b09a; letter-spacing: 0.3px; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding:28px 20px 22px;border-bottom:1px solid rgba(255,255,255,0.05);margin-bottom:18px;">
        <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:white;margin-bottom:4px;">PitchReady <span style="color:#d4a843;">AI</span></div>
        <div style="font-size:0.7rem;color:rgba(255,255,255,0.35);line-height:1.6;">Pre-pitch intelligence<br>for consultants & BD teams</div>
        <div style="background:rgba(212,168,67,0.15);border:1px solid rgba(212,168,67,0.25);color:#d4a843;font-family:'JetBrains Mono',monospace;font-size:0.58rem;padding:3px 10px;border-radius:100px;margin-top:12px;display:inline-block;letter-spacing:0.5px;">✦ FREE · 4-AGENT PIPELINE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style="font-size:0.7rem;color:rgba(255,255,255,0.35);line-height:1.7;padding:0 4px 14px;">
    Get free key → <a href="https://openrouter.ai" target="_blank">openrouter.ai</a><br>
    Sign up → API Keys → Create
    </div>""", unsafe_allow_html=True)

    api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-v1-...")
    st.divider()
    st.markdown("""<div style="font-size:0.68rem;color:rgba(255,255,255,0.25);line-height:1.9;padding:0 4px;">
    <b style="color:rgba(255,255,255,0.45);">4 agents run in sequence:</b><br>
    🔍  Landscape Scanner<br>
    📋  Battlecard Builder<br>
    💬  Objection Handler<br>
    🎯  Pitch Sharpener
    </div>""", unsafe_allow_html=True)

# ── HERO ──
st.markdown('<div class="eyebrow">✦ Pre-Pitch Intelligence · 4-Agent AI Pipeline · Free</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Walk into every pitch<br><em>fully prepared.</em></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Tell PitchReady about your client and deal context — 4 AI agents build your complete competitive brief in minutes.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.markdown('<div class="sec-label">Deal Context</div>', unsafe_allow_html=True)

    client_name = st.text_input("Client / Prospect Name", placeholder="e.g. Tata Consultancy, HDFC Bank, Byju's...")
    client_industry = st.selectbox("Client Industry", [
        "Banking & Financial Services", "Technology / SaaS", "E-Commerce / Retail",
        "Healthcare & Pharma", "Education", "Manufacturing & Industrial",
        "Media & Entertainment", "Telecom", "Real Estate", "Government / PSU", "Other"
    ])
    deal_type = st.selectbox("Type of Engagement", [
        "Strategy Consulting", "Digital Transformation",
        "Product / Technology Implementation", "Market Entry",
        "M&A / Due Diligence", "Cost Optimization",
        "Sales / BD Pitch", "Other"
    ])
    your_firm = st.text_input("Your Firm / Product", placeholder="e.g. Deloitte, McKinsey, your startup...")
    context = st.text_area(
        "Deal Context & What You Know",
        placeholder="e.g. HDFC is evaluating vendors for a core banking modernization. They're currently on TCS BaNCS. Budget is ~50Cr. Decision in Q3. Key stakeholder is CTO.",
        height=130
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    submit = st.button("Build My Pitch Brief →")

with col2:
    st.markdown('<div class="sec-label">Intelligence Brief</div>', unsafe_allow_html=True)

    if submit:
        if not api_key:
            st.error("⚠️ Add your OpenRouter API key in the sidebar — free at openrouter.ai")
        elif not client_name:
            st.error("⚠️ Please enter the client or prospect name.")
        else:
            full_report = f"# PitchReady Brief\n**Client:** {client_name} | **Industry:** {client_industry} | **Deal:** {deal_type}\n\n---\n\n"

            deal_ctx = f"""
Client: {client_name}
Industry: {client_industry}
Deal Type: {deal_type}
Our Firm/Product: {your_firm or 'Not specified'}
Context: {context or 'Not provided'}
"""

            # ══ AGENT 1: LANDSCAPE SCANNER ══
            st.markdown("""
            <div class="step-row">
                <div class="step on">🔍 Landscape</div>
                <div class="step-arrow">→</div>
                <div class="step">📋 Battlecard</div>
                <div class="step-arrow">→</div>
                <div class="step">💬 Objections</div>
                <div class="step-arrow">→</div>
                <div class="step">🎯 Pitch</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="agent-row"><span class="agent-label lbl-1">AGENT 1</span><span class="agent-title">🔍 Landscape Scanner</span></div>', unsafe_allow_html=True)

            p1 = st.empty()
            with st.spinner("Scanning competitive landscape..."):
                prompt1 = f"""You are a senior consultant preparing a pre-pitch intelligence brief.

Deal Context:
{deal_ctx}

Scan the competitive landscape for this deal:

## Client Intelligence
What is known about {client_name}? Key facts about their business, scale, recent news, strategic priorities, known pain points in {client_industry}.

## Who Else Is Pitching?
List the 3-4 most likely competitors who will also pitch for this {deal_type} engagement at {client_name}. For each:
- Company name & their positioning
- Why they're a threat
- Their typical pitch angle

## Current Vendor / Status Quo
What is {client_name} likely using today? What's the risk of them doing nothing (status quo)?

## Decision Dynamics
Typical decision-making process for this type of deal in {client_industry}. Who are the likely stakeholders and what do they care about?

Be specific and realistic."""

                out1, _ = call_llm(api_key, prompt1, p1, "out out-1", 1200)
                full_report += f"# AGENT 1: LANDSCAPE SCAN\n\n{out1}\n\n---\n\n"

            # ══ AGENT 2: BATTLECARD BUILDER ══
            st.markdown("""
            <div class="step-row" style="margin-top:12px;">
                <div class="step">🔍 Landscape</div>
                <div class="step-arrow">→</div>
                <div class="step on">📋 Battlecard</div>
                <div class="step-arrow">→</div>
                <div class="step">💬 Objections</div>
                <div class="step-arrow">→</div>
                <div class="step">🎯 Pitch</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="agent-row"><span class="agent-label lbl-2">AGENT 2</span><span class="agent-title">📋 Battlecard Builder</span></div>', unsafe_allow_html=True)

            p2 = st.empty()
            with st.spinner("Building competitive battlecards..."):
                prompt2 = f"""You are a competitive intelligence expert building sales battlecards.

Deal: {deal_type} for {client_name} ({client_industry})
Our firm: {your_firm or 'our firm'}

Competitors identified:
{out1[:800]}

Build a battlecard for each competitor:

## Battlecard: [Competitor Name]

**Their Pitch in 1 Line:** What they'll likely say to {client_name}

**Their 3 Strongest Claims:**
1.
2.
3.

**Their 3 Real Weaknesses:**
1.
2.
3.

**How We Beat Them:**
The 2-3 specific reasons {your_firm or 'we'} wins against them for THIS deal.

**The Landmine to Plant:**
One question to ask in the room that makes the client doubt this competitor.

Keep it sharp. No fluff. This is for use in the actual pitch meeting."""

                out2, _ = call_llm(api_key, prompt2, p2, "out out-2", 1200)
                full_report += f"# AGENT 2: BATTLECARDS\n\n{out2}\n\n---\n\n"

            # ══ AGENT 3: OBJECTION HANDLER ══
            st.markdown("""
            <div class="step-row" style="margin-top:12px;">
                <div class="step">🔍 Landscape</div>
                <div class="step-arrow">→</div>
                <div class="step">📋 Battlecard</div>
                <div class="step-arrow">→</div>
                <div class="step on">💬 Objections</div>
                <div class="step-arrow">→</div>
                <div class="step">🎯 Pitch</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="agent-row"><span class="agent-label lbl-3">AGENT 3</span><span class="agent-title">💬 Objection Handler</span></div>', unsafe_allow_html=True)

            p3 = st.empty()
            with st.spinner("Preparing objection responses..."):
                prompt3 = f"""You are a veteran dealmaker who has closed hundreds of {deal_type} deals in {client_industry}.

Our firm: {your_firm or 'our firm'}
Client: {client_name}

Prepare a complete objection handling guide for this pitch:

## The 6 Most Likely Objections

For each objection:

### Objection [N]: "[Exact words the client might say]"

**Why they're really saying this:** (the hidden concern)

**The Response:**
What to say — word for word. Keep it under 4 sentences. Confident, not defensive.

**The Follow-up Question:**
One question to ask after responding to take back control.

Cover these objection types:
1. Price / budget objection
2. "We're happy with our current vendor"
3. Competitor comparison ("Company X offered us...")
4. Timeline / implementation risk
5. Team / capability doubt
6. "We need to think about it"

Make responses feel natural and consultative, not salesy."""

                out3, _ = call_llm(api_key, prompt3, p3, "out out-3", 1200)
                full_report += f"# AGENT 3: OBJECTION HANDLER\n\n{out3}\n\n---\n\n"

            # ══ AGENT 4: PITCH SHARPENER ══
            st.markdown("""
            <div class="step-row" style="margin-top:12px;">
                <div class="step">🔍 Landscape</div>
                <div class="step-arrow">→</div>
                <div class="step">📋 Battlecard</div>
                <div class="step-arrow">→</div>
                <div class="step">💬 Objections</div>
                <div class="step-arrow">→</div>
                <div class="step on">🎯 Pitch</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="agent-row"><span class="agent-label lbl-4">AGENT 4</span><span class="agent-title">🎯 Pitch Sharpener</span></div>', unsafe_allow_html=True)

            p4 = st.empty()
            with st.spinner("Sharpening your pitch..."):
                prompt4 = f"""You are a pitch coach who has helped teams win $500M+ in deals.

Deal: {deal_type} for {client_name} ({client_industry})
Our firm: {your_firm or 'our firm'}
Context: {context or 'Not provided'}

Based on all the intelligence gathered, sharpen the pitch:

## The Killer Opening
First 30 seconds of the pitch. Hook them immediately. Reference something specific about {client_name}'s situation.

## Our Unique Point of View
The 1 insight about {client_industry} or this deal type that only {your_firm or 'we'} can credibly say. This is our differentiated perspective.

## The 3-Point Value Story
Three specific, quantified value claims tailored to {client_name}. No generic statements.

## The Moment of Choice
The slide or moment in the pitch where we make {client_name} feel the cost of NOT choosing us.

## Closing Move
How to close the room. What to ask for at the end of this meeting.

## The 5 Questions to Ask the Client
Strategic questions that position us as the smartest firm in the room and uncover buying signals.

## Pre-Meeting Checklist
5 things to do before walking into this pitch.

Make this feel like advice from a senior partner who has pitched {client_name} before."""

                out4, used_model = call_llm(api_key, prompt4, p4, "out out-4", 1400)
                full_report += f"# AGENT 4: PITCH SHARPENER\n\n{out4}"

            st.caption(f"✓ Brief ready · Powered by `{used_model}`")
            st.download_button(
                "⬇ Download Pitch Brief (.md)",
                data=full_report,
                file_name=f"pitchready_{client_name.lower().replace(' ','_')}.md",
                mime="text/markdown"
            )

    else:
        st.markdown("""
        <div class="empty">
            <div class="empty-icon">🎯</div>
            <div class="empty-title">Your pitch brief awaits.</div>
            <div class="empty-sub">Tell PitchReady who you're pitching and what the deal is.<br>Four agents will build your complete competitive brief.</div>
            <div>
                <span class="chip">Landscape Scan</span>
                <span class="chip">Competitor Battlecards</span>
                <span class="chip">Objection Playbook</span>
                <span class="chip">Pitch Opening</span>
                <span class="chip">Closing Strategy</span>
                <span class="chip">5 Power Questions</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="footer">PitchReady AI · Built with OpenRouter free models · Streamlit · 2025</div>', unsafe_allow_html=True)
