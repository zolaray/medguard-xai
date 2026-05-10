"""
╔══════════════════════════════════════════════════════════════╗
║         MedGuard-XAI  —  Clinical Risk Intelligence          ║
║         By Fatima Rayane  |  CS × Biomedical AI              ║
║         Demo version — pre-computed AI outputs               ║
╚══════════════════════════════════════════════════════════════╝

Run:  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# ══════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="MedGuard-XAI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ══════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html, body, .stApp {
    background-color: #0d1117 !important;
    font-family: 'IBM Plex Sans', sans-serif;
    color: #e6edf3;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d;
}
[data-testid="stSidebar"] * { color: #e6edf3 !important; }

.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.metric-card .label {
    font-size: 0.70rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 0.35rem;
    font-family: 'IBM Plex Mono', monospace;
}
.metric-card .value {
    font-size: 2.1rem;
    font-weight: 600;
    line-height: 1;
    font-family: 'IBM Plex Mono', monospace;
}
.metric-card .sub {
    font-size: 0.72rem;
    color: #8b949e;
    margin-top: 0.3rem;
}

.panel {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.panel-title {
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8b949e;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid #21262d;
    padding-bottom: 0.5rem;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.9rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.05em;
}
.badge-low      { background:#1a3a1a; color:#3fb950; border:1px solid #2d5a2d; }
.badge-moderate { background:#3a2e0a; color:#d29922; border:1px solid #5a460f; }
.badge-high     { background:#3a1a1a; color:#f85149; border:1px solid #5a2a2a; }
.badge-critical {
    background:#2d1010; color:#ff6b6b; border:1px solid #5a2020;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%,100% { box-shadow:0 0 0 0 rgba(248,81,73,.4); }
    50%      { box-shadow:0 0 0 6px rgba(248,81,73,0); }
}

.xai-box {
    background: #0d1f0d;
    border: 1px solid #2d5a2d;
    border-left: 4px solid #3fb950;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    font-size: 0.87rem;
    line-height: 1.75;
    color: #c3e6c3;
}

.flag-tag {
    display: inline-block;
    background: #3a1a1a;
    color: #f85149;
    border: 1px solid #5a2a2a;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.74rem;
    font-family: 'IBM Plex Mono', monospace;
    margin: 2px 2px 2px 0;
}

.status-dot {
    width:8px; height:8px; border-radius:50%;
    background:#3fb950; box-shadow:0 0 6px #3fb950;
    animation:pulse-dot 2s infinite;
    display:inline-block; margin-right:6px;
}
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:.4} }

.case-card {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: border-color .2s;
}
.case-card:hover { border-color: #58a6ff; }
.case-card.active { border-color: #58a6ff; background: #1a2332; }

.stButton > button {
    background: linear-gradient(135deg,#1a3a5c,#0d2240) !important;
    color: #58a6ff !important;
    border: 1px solid #58a6ff !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: .05em !important;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg,#1f4a7a,#112e55) !important;
    box-shadow: 0 0 12px rgba(88,166,255,.25) !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  PRE-COMPUTED DEMO DATA
#  These are real AI outputs — generated once,
#  saved here so the app works with zero API calls
# ══════════════════════════════════════════════

CASES = {
    "🫀 Diabetic Patient — Chest Pain": {
        "report": """PATIENT: Male, 58 years old
DATE: 2026-05-01 | CHIEF COMPLAINT: Chest pain and shortness of breath for 3 days

VITAL SIGNS:
BP: 158/96 mmHg  |  HR: 102 bpm  |  RR: 22/min  |  SpO2: 94%  |  Temp: 37.2°C

MEDICATIONS: Metformin 1000mg BD, Amlodipine 5mg OD

LAB RESULTS:
HbA1c: 9.8%  |  Fasting glucose: 287 mg/dL  |  Troponin I: 0.08 ng/mL (elevated)
BNP: 420 pg/mL (elevated)  |  Creatinine: 1.4 mg/dL  |  LDL: 142 mg/dL  |  WBC: 11.2

ECG: ST depression in leads V4-V6

HISTORY: Type 2 diabetes mellitus (10 years). No previous cardiac events.
Family history of coronary artery disease. BMI 31.2. Smoker (15 pack-years).""",

        "findings": {
            "patient_age": 58,
            "patient_gender": "Male",
            "chief_complaint": "Chest pain and shortness of breath for 3 days",
            "diagnoses": ["Type 2 Diabetes Mellitus", "Hypertension", "Suspected Acute Coronary Syndrome"],
            "medications": ["Metformin 1000mg BD", "Amlodipine 5mg OD"],
            "lab_results": {
                "HbA1c": "9.8% (high)",
                "Fasting Glucose": "287 mg/dL (high)",
                "Troponin I": "0.08 ng/mL (ELEVATED)",
                "BNP": "420 pg/mL (ELEVATED)",
                "Creatinine": "1.4 mg/dL (borderline)",
                "LDL": "142 mg/dL (high)",
                "WBC": "11.2 x10⁹/L (mildly elevated)",
            },
            "vital_signs": {
                "Blood Pressure": "158/96 mmHg (high)",
                "Heart Rate": "102 bpm (tachycardia)",
                "Respiratory Rate": "22/min (elevated)",
                "SpO2": "94% (low)",
                "Temperature": "37.2°C (normal)",
            },
            "risk_flags": [
                "Elevated Troponin I",
                "ST depression V4-V6",
                "Elevated BNP",
                "SpO2 94%",
                "Uncontrolled diabetes (HbA1c 9.8%)",
                "Tachycardia 102 bpm",
            ],
            "report_type": "clinical_note",
            "risk_dimensions": {
                "cardiac": 88,
                "metabolic": 82,
                "infection": 22,
                "medication": 35,
                "neurological": 10,
                "renal": 40,
            },
        },

        "risk": {
            "overall_risk": "HIGH",
            "risk_score": 87,
            "primary_concerns": [
                "Possible Non-ST Elevation Myocardial Infarction (NSTEMI)",
                "Severely uncontrolled Type 2 diabetes with end-organ implications",
                "Hypoxemia (SpO2 94%) with tachycardia suggesting cardiac compromise",
            ],
            "reasoning": "The combination of elevated Troponin I, ST depression in V4-V6, elevated BNP, and tachycardia in a 58-year-old diabetic patient with hypertension and active smoking history constitutes a high-risk cardiac presentation. Diabetes significantly increases the risk of silent or atypical MI presentations, making this constellation of findings particularly concerning.",
            "recommended_actions": [
                "Urgent cardiology consultation",
                "Serial Troponin measurements every 3-6 hours",
                "12-lead ECG immediately and continuous cardiac monitoring",
                "Supplemental oxygen to maintain SpO2 >95%",
                "Aspirin 300mg loading dose if not contraindicated",
                "NPO pending cardiac workup",
            ],
            "confidence": "HIGH",
            "time_sensitivity": "URGENT",
        },

        "explanation": """## Summary
This 58-year-old male with a 10-year history of poorly controlled Type 2 diabetes presents with a 3-day history of chest pain and shortness of breath — a high-risk constellation in a diabetic patient. The AI system has flagged this as a **HIGH risk** case with a score of 87/100, primarily driven by cardiac biomarker elevation and ECG changes.

## Key Findings & Why They Matter
- **Elevated Troponin I (0.08 ng/mL):** Troponin is released when heart muscle cells are damaged. Any elevation above normal range is treated as a cardiac emergency until proven otherwise — this is the AI's most significant flag.
- **ST depression in V4-V6:** This ECG pattern is a classic sign of myocardial ischemia — the heart muscle is not receiving enough oxygen. Combined with elevated Troponin, this suggests NSTEMI.
- **BNP 420 pg/mL:** Brain natriuretic peptide is a heart failure marker. Elevation here suggests the heart is under significant stress and working harder than normal.
- **SpO2 94% + HR 102 bpm:** Low oxygen saturation with tachycardia indicates the heart and lungs are compensating — an early sign of decompensation.
- **HbA1c 9.8%:** Chronically uncontrolled diabetes accelerates cardiovascular disease and masks typical chest pain symptoms.

## AI Reasoning Transparency
The system assigned HIGH risk (not CRITICAL) because Troponin elevation, while significant, is moderate rather than severely elevated, and the patient is hemodynamically borderline rather than in shock. The multi-dimensional radar shows cardiac (88) and metabolic (82) risk as co-dominant — the AI identified that diabetes is not background noise here, it is actively amplifying cardiac risk.

## Suggested Actions
- Urgent cardiology consultation within the hour
- Serial Troponin at 0h, 3h, 6h to track trajectory
- Continuous ECG monitoring
- Glycemic management alongside cardiac workup

## Confidence & Limitations
Confidence is HIGH given the convergence of multiple independent biomarkers. The AI cannot assess clinical appearance, pain severity, or family history nuance — these must be integrated by the treating physician.

*This is a decision-support tool only. Clinical judgment by a qualified physician is required.*""",
    },


    "🧒 Pediatric Fever — Critical Rash": {
        "report": """PATIENT: Female, 7 years old
DATE: 2026-04-28 | CHIEF COMPLAINT: High fever and rash for 2 days

VITAL SIGNS:
Temperature: 39.8°C  |  HR: 124 bpm  |  BP: 95/60 mmHg  |  RR: 26/min

LAB RESULTS:
WBC: 18.4 x10⁹/L (elevated)  |  CRP: 85 mg/L (elevated)
Platelets: 98 x10⁹/L (LOW)  |  Neutrophils: 82%
Blood culture: pending

CLINICAL NOTE: 2-day history of high fever, non-blanching petechial rash on lower limbs,
neck stiffness, photophobia. No recent travel. Vaccinations up to date.
Rapid deterioration over last 6 hours reported by parents.""",

        "findings": {
            "patient_age": 7,
            "patient_gender": "Female",
            "chief_complaint": "High fever and petechial rash for 2 days with rapid deterioration",
            "diagnoses": ["Suspected Bacterial Meningitis", "Possible Meningococcal Septicemia", "Thrombocytopenia"],
            "medications": [],
            "lab_results": {
                "WBC": "18.4 x10⁹/L (HIGH)",
                "CRP": "85 mg/L (HIGH)",
                "Platelets": "98 x10⁹/L (LOW)",
                "Neutrophils": "82% (elevated)",
                "Blood Culture": "Pending",
            },
            "vital_signs": {
                "Temperature": "39.8°C (high fever)",
                "Heart Rate": "124 bpm (tachycardia)",
                "Blood Pressure": "95/60 mmHg (hypotension)",
                "Respiratory Rate": "26/min (tachypnea)",
            },
            "risk_flags": [
                "Non-blanching petechial rash",
                "Neck stiffness + photophobia",
                "Thrombocytopenia (platelets 98)",
                "Hypotension in pediatric patient",
                "Rapid 6-hour deterioration",
                "High fever + neutrophilia",
            ],
            "report_type": "clinical_note",
            "risk_dimensions": {
                "cardiac": 55,
                "metabolic": 30,
                "infection": 97,
                "medication": 10,
                "neurological": 92,
                "renal": 25,
            },
        },

        "risk": {
            "overall_risk": "CRITICAL",
            "risk_score": 96,
            "primary_concerns": [
                "Bacterial meningitis / meningococcal disease — life-threatening",
                "Early septic shock — hypotension + tachycardia in a child",
                "Thrombocytopenia — risk of disseminated intravascular coagulation (DIC)",
            ],
            "reasoning": "A non-blanching petechial rash with fever, neck stiffness, and photophobia in a child is bacterial meningitis until proven otherwise — this is one of the most time-critical presentations in pediatric emergency medicine. The addition of hypotension (BP 95/60), tachycardia, thrombocytopenia, and rapid 6-hour deterioration elevates this to CRITICAL. Every hour of delay in antibiotic administration increases mortality risk significantly.",
            "recommended_actions": [
                "IMMEDIATE IV antibiotics — do not wait for lumbar puncture results",
                "Blood culture before antibiotics if feasible within 10 minutes",
                "IV access x2 + aggressive fluid resuscitation",
                "Pediatric ICU admission",
                "Lumbar puncture after stabilization only",
                "Notify parents and escalate to senior pediatrician immediately",
            ],
            "confidence": "HIGH",
            "time_sensitivity": "IMMEDIATE",
        },

        "explanation": """## Summary
This 7-year-old girl presents with a textbook **CRITICAL** emergency: non-blanching petechial rash, high fever, neck stiffness, and photophobia with rapid 6-hour deterioration. The AI has assigned the highest possible risk score (96/100). This is a time-critical case where minutes matter.

## Key Findings & Why They Matter
- **Non-blanching petechial rash:** This is the single most alarming sign in this case. A rash that does not blanch (turn white) when pressed indicates bleeding under the skin — a hallmark of meningococcal disease, which can be fatal within hours.
- **Neck stiffness + photophobia:** These are the classic signs of meningeal irritation — the membranes around the brain are inflamed. In combination with fever and rash, bacterial meningitis must be the working diagnosis.
- **Thrombocytopenia (platelets 98):** Low platelets in this context suggest the body's clotting system is being consumed — a sign of early DIC (disseminated intravascular coagulation), a life-threatening complication of severe sepsis.
- **Hypotension (95/60 mmHg):** In a 7-year-old, this blood pressure indicates early septic shock. Children maintain BP longer than adults before crashing — this reading means decompensation is already beginning.
- **Rapid deterioration in 6 hours:** The trajectory matters as much as the values. A child worsening this fast is a red flag for aggressive bacterial infection.

## AI Reasoning Transparency
The AI assigned CRITICAL (not just HIGH) because of the convergence of: a pathognomonic rash pattern, two signs of CNS involvement, hemodynamic instability, thrombocytopenia suggesting DIC risk, and rapid trajectory. The radar chart shows infection (97) and neurological (92) risk as the dominant dimensions — this is a sepsis-meningitis dual threat.

## Suggested Actions
- IV antibiotics immediately — Ceftriaxone is standard first-line
- Do not delay treatment waiting for LP confirmation
- Aggressive fluid bolus for hypotension
- ICU escalation — this child needs intensive monitoring

## Confidence & Limitations
Confidence is HIGH. The clinical picture is highly consistent. The AI cannot assess rash morphology directly or the child's level of consciousness — the clinician's bedside assessment of these is essential.

*This is a decision-support tool only. Clinical judgment by a qualified physician is required.*""",
    },


    "🦴 Post-Op Elderly Patient — Bleeding Risk": {
        "report": """PATIENT: Female, 74 years old
POST-OPERATIVE DAY 2: Right hip replacement surgery

VITAL SIGNS:
BP: 102/68 mmHg  |  HR: 88 bpm  |  Temp: 38.1°C  |  SpO2: 96%

MEDICATIONS: Warfarin 5mg OD, Enoxaparin 40mg SC, Paracetamol 1g QID

LAB RESULTS:
INR: 3.8 (supratherapeutic)  |  Hemoglobin: 8.2 g/dL (low)
Creatinine: 1.9 mg/dL (elevated)  |  CRP: 112 mg/L (elevated)
D-Dimer: 2.8 mg/L (elevated)

CLINICAL NOTE: Recovering from right total hip arthroplasty. Reports increasing right leg
pain and swelling. Known atrial fibrillation, chronic kidney disease stage 3.
Wound site appears clean. Confused this morning per nursing notes.""",

        "findings": {
            "patient_age": 74,
            "patient_gender": "Female",
            "chief_complaint": "Post-op day 2 hip replacement — leg pain, swelling, and new confusion",
            "diagnoses": [
                "Post-operative right hip arthroplasty",
                "Atrial fibrillation",
                "Chronic kidney disease stage 3",
                "Supratherapeutic anticoagulation",
                "Suspected deep vein thrombosis",
            ],
            "medications": ["Warfarin 5mg OD", "Enoxaparin 40mg SC", "Paracetamol 1g QID"],
            "lab_results": {
                "INR": "3.8 (SUPRATHERAPEUTIC — target 2-3)",
                "Hemoglobin": "8.2 g/dL (LOW)",
                "Creatinine": "1.9 mg/dL (elevated — CKD3)",
                "CRP": "112 mg/L (elevated)",
                "D-Dimer": "2.8 mg/L (elevated)",
            },
            "vital_signs": {
                "Blood Pressure": "102/68 mmHg (low)",
                "Heart Rate": "88 bpm",
                "Temperature": "38.1°C (low-grade fever)",
                "SpO2": "96%",
            },
            "risk_flags": [
                "INR 3.8 — supratherapeutic anticoagulation",
                "Dual anticoagulation (Warfarin + Enoxaparin)",
                "New confusion post-op",
                "Elevated D-Dimer + leg swelling → DVT risk",
                "Anemia (Hb 8.2) — possible post-op bleed",
                "Low blood pressure",
            ],
            "report_type": "clinical_note",
            "risk_dimensions": {
                "cardiac": 52,
                "metabolic": 45,
                "infection": 55,
                "medication": 91,
                "neurological": 60,
                "renal": 68,
            },
        },

        "risk": {
            "overall_risk": "HIGH",
            "risk_score": 81,
            "primary_concerns": [
                "Supratherapeutic anticoagulation with dual agents — major bleeding risk",
                "New-onset confusion — possible intracranial bleed, PE, or delirium",
                "Elevated D-Dimer with leg symptoms — DVT/PE must be excluded",
            ],
            "reasoning": "This patient presents a dangerous paradox: she is simultaneously over-anticoagulated (INR 3.8, dual therapy) — increasing bleeding risk — while also showing signs that could indicate a new clot (elevated D-Dimer, leg pain/swelling, post-op state). New confusion in an elderly post-operative patient on supratherapeutic anticoagulation raises urgent concern for intracranial bleed. This complex picture requires immediate multidisciplinary assessment.",
            "recommended_actions": [
                "Hold Enoxaparin immediately — dual anticoagulation with supratherapeutic INR is high bleeding risk",
                "Urgent CT head to exclude intracranial bleed given new confusion",
                "Doppler ultrasound of right leg to assess for DVT",
                "Hematology and anticoagulation team review",
                "Vitamin K consideration if active bleeding suspected",
                "Repeat INR in 4-6 hours after holding anticoagulation",
            ],
            "confidence": "MEDIUM",
            "time_sensitivity": "URGENT",
        },

        "explanation": """## Summary
This 74-year-old woman on post-operative day 2 following hip replacement presents a complex and dangerous clinical picture. She is simultaneously at risk for both **major bleeding** (over-anticoagulated) and **new thrombosis** (elevated D-Dimer, leg symptoms). New confusion adds a neurological urgency. The AI has assigned HIGH risk (81/100) with the medication dimension as the dominant flag.

## Key Findings & Why They Matter
- **INR 3.8 on dual anticoagulation (Warfarin + Enoxaparin):** Her INR target is 2.0–3.0. At 3.8, she is already over-anticoagulated — adding Enoxaparin on top of this is a significant bleeding risk. This combination needs immediate review.
- **New confusion this morning:** In an elderly post-operative patient on over-anticoagulation, new confusion is a red flag for intracranial bleeding until proven otherwise. It could also be delirium, PE, or medication effect — but intracranial bleed must be excluded urgently.
- **D-Dimer 2.8 mg/L + right leg pain and swelling:** Post-hip surgery DVT is common. Elevated D-Dimer with leg symptoms requires imaging to rule out deep vein thrombosis or pulmonary embolism.
- **Hemoglobin 8.2 g/dL:** This is low, and in the post-op context may indicate ongoing or recent bleeding from the surgical site or elsewhere.
- **BP 102/68 + low-grade fever:** Hypotension with fever suggests either infection or early hypovolemia — both concerning in this frail post-operative patient.

## AI Reasoning Transparency
The AI assigned HIGH (not CRITICAL) because the patient is currently hemodynamically borderline rather than in collapse, and the confusion could have benign causes (delirium). However, the medication dimension (91/100) is the dominant risk driver — the dual anticoagulation situation is the most actionable and time-sensitive issue. The AI identified that this is a medical paradox case, which is why confidence is MEDIUM — the clinical picture has competing risks pulling in opposite directions.

## Suggested Actions
- CT head immediately for the confusion
- Hold Enoxaparin pending senior review
- Leg Doppler ultrasound
- Do not adjust Warfarin blindly — get expert anticoagulation guidance

## Confidence & Limitations
Confidence is MEDIUM because this case involves competing risks (bleed vs. clot) that require clinical judgment beyond pattern matching. The AI has identified the danger signals but cannot resolve the therapeutic paradox — a hematologist and the surgical team must be involved.

*This is a decision-support tool only. Clinical judgment by a qualified physician is required.*""",
    },
}


# ══════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════
if "selected_case" not in st.session_state:
    st.session_state.selected_case = list(CASES.keys())[0]


# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════
def score_color(s):
    if s < 30:  return "#3fb950"
    if s < 60:  return "#d29922"
    if s < 80:  return "#f85149"
    return "#ff6b6b"

def risk_color(level):
    return {"LOW":"#3fb950","MODERATE":"#d29922","HIGH":"#f85149","CRITICAL":"#ff6b6b"}.get(level,"#8b949e")

def sens_color(s):
    return {"IMMEDIATE":"#ff6b6b","URGENT":"#d29922","ROUTINE":"#3fb950"}.get(s,"#8b949e")


# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
<div style='padding:.5rem 0 1rem'>
  <div style='font-family:IBM Plex Mono,monospace;font-size:1rem;font-weight:600;color:#58a6ff'>
    🏥 MedGuard-XAI
  </div>
  <div style='font-size:.71rem;color:#8b949e;margin-top:4px;font-family:IBM Plex Mono,monospace'>
    Clinical Risk Intelligence v1.0
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size:.74rem;color:#8b949e;font-family:IBM Plex Mono,monospace;margin-bottom:10px;text-transform:uppercase;letter-spacing:.08em'>Patient Cases</div>", unsafe_allow_html=True)

    for name, data in CASES.items():
        level  = data["risk"]["overall_risk"]
        score  = data["risk"]["risk_score"]
        color  = risk_color(level)
        active = "active" if name == st.session_state.selected_case else ""
        if st.button(f"{name}", key=f"btn_{name}"):
            st.session_state.selected_case = name
            st.rerun()
        # small risk pill under each button
        st.markdown(f"""
<div style='font-size:.7rem;font-family:IBM Plex Mono,monospace;color:{color};
            margin:-8px 0 8px 4px;'>
  {level} · {score}/100
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
<div style='font-size:.7rem;color:#8b949e;font-family:IBM Plex Mono,monospace;margin-bottom:6px'>
  HOW IT WORKS
</div>
<div style='font-size:.75rem;color:#6e7681;line-height:1.6'>
  MedGuard-XAI runs a 3-agent AI pipeline:<br><br>
  <span style='color:#58a6ff'>①</span> <b>Extractor</b> — reads clinical text → structured data<br><br>
  <span style='color:#58a6ff'>②</span> <b>Risk Analyzer</b> — scores 6 risk dimensions<br><br>
  <span style='color:#58a6ff'>③</span> <b>XAI Layer</b> — explains <i>why</i> in plain language
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size:.64rem;color:#484f58;font-family:IBM Plex Mono,monospace;text-align:center'>Research prototype · Not for clinical use<br>Fatima Rayane · CS × Biomedical AI</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  LOAD SELECTED CASE
# ══════════════════════════════════════════════
case     = CASES[st.session_state.selected_case]
findings = case["findings"]
risk     = case["risk"]
xai      = case["explanation"]
score    = risk["risk_score"]
level    = risk["overall_risk"]
sens     = risk["time_sensitivity"]
flags    = findings["risk_flags"]
conf     = risk["confidence"]


# ══════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════
st.markdown(f"""
<div style='display:flex;align-items:center;gap:1rem;padding:.4rem 0 1.4rem;
            border-bottom:1px solid #30363d;margin-bottom:1.5rem'>
  <div>
    <div style='font-family:IBM Plex Mono,monospace;font-size:1.4rem;font-weight:500'>
      MedGuard<span style='color:#58a6ff'>-XAI</span>
    </div>
    <div style='font-size:.76rem;color:#8b949e;font-family:IBM Plex Mono,monospace;margin-top:2px'>
      <span class='status-dot'></span>Clinical Risk Intelligence Dashboard · Explainable AI
    </div>
  </div>
  <div style='margin-left:auto;text-align:right'>
    <div style='font-size:.7rem;color:#8b949e;font-family:IBM Plex Mono,monospace'>Active Case</div>
    <div style='font-size:.85rem;color:#e6edf3;font-family:IBM Plex Mono,monospace'>{st.session_state.selected_case}</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  METRIC CARDS
# ══════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)

with c1:
    sc = score_color(score)
    st.markdown(f"""
<div class='metric-card'>
  <div class='label'>Risk Score</div>
  <div class='value' style='color:{sc}'>{score}</div>
  <div class='sub'>out of 100</div>
</div>""", unsafe_allow_html=True)

with c2:
    badge = f"badge-{level.lower()}"
    st.markdown(f"""
<div class='metric-card'>
  <div class='label'>Risk Level</div>
  <div style='margin:.45rem 0'><span class='badge {badge}'>{level}</span></div>
  <div class='sub'>{conf} confidence</div>
</div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
<div class='metric-card'>
  <div class='label'>Risk Flags</div>
  <div class='value' style='color:#f85149'>{len(flags)}</div>
  <div class='sub'>findings flagged</div>
</div>""", unsafe_allow_html=True)

with c4:
    sc2 = sens_color(sens)
    st.markdown(f"""
<div class='metric-card'>
  <div class='label'>Time Sensitivity</div>
  <div class='value' style='color:{sc2};font-size:1.15rem;padding-top:.3rem'>{sens}</div>
  <div class='sub'>{findings.get("report_type","").replace("_"," ")}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  GAUGE + RADAR
# ══════════════════════════════════════════════
col_g, col_r = st.columns(2)

with col_g:
    st.markdown("<div class='panel'><div class='panel-title'>⚡ Risk Score Gauge</div>", unsafe_allow_html=True)
    fig_g = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font":{"color":score_color(score),"size":46,"family":"IBM Plex Mono"}},
        gauge={
            "axis":{"range":[0,100],"tickcolor":"#8b949e","tickfont":{"color":"#8b949e","size":9}},
            "bar":{"color":score_color(score),"thickness":.25},
            "bgcolor":"#161b22","borderwidth":0,
            "steps":[
                {"range":[0,30],"color":"#0d2a0d"},
                {"range":[30,60],"color":"#2a1f0d"},
                {"range":[60,80],"color":"#2a0d0d"},
                {"range":[80,100],"color":"#1a0505"},
            ],
            "threshold":{"line":{"color":score_color(score),"width":3},"thickness":.8,"value":score},
        },
    ))
    fig_g.update_layout(paper_bgcolor="#161b22",plot_bgcolor="#161b22",
                        font_color="#e6edf3",height=210,
                        margin=dict(t=20,b=10,l=30,r=30))
    st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_r:
    st.markdown("<div class='panel'><div class='panel-title'>🕸️ Multi-Dimensional Risk Radar</div>", unsafe_allow_html=True)
    dims = findings["risk_dimensions"]
    cats = [k.capitalize() for k in dims]
    vals = list(dims.values())
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatterpolar(
        r=vals+[vals[0]], theta=cats+[cats[0]],
        fill="toself",
        fillcolor=f"rgba({','.join(str(int(score_color(score).lstrip('#')[i:i+2],16)) for i in (0,2,4))},.15)",
        line=dict(color=score_color(score),width=2),
        marker=dict(color=score_color(score),size=6),
    ))
    fig_r.update_layout(
        polar=dict(
            bgcolor="#0d1117",
            radialaxis=dict(range=[0,100],visible=True,color="#484f58",
                            gridcolor="#30363d",tickfont=dict(color="#484f58",size=9)),
            angularaxis=dict(color="#8b949e",gridcolor="#30363d",
                             tickfont=dict(color="#8b949e",size=11,family="IBM Plex Mono")),
        ),
        paper_bgcolor="#161b22",showlegend=False,
        height=210,margin=dict(t=20,b=20,l=40,r=40),
    )
    st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  FINDINGS TABLE + FLAGS
# ══════════════════════════════════════════════
col_t, col_f = st.columns([3, 2])

with col_t:
    st.markdown("<div class='panel'><div class='panel-title'>🧬 Extracted Clinical Findings</div>", unsafe_allow_html=True)
    rows = []
    rows.append({"Category":"Patient","Field":"Age / Gender",
                 "Value":f"{findings['patient_age']} / {findings['patient_gender']}"})
    rows.append({"Category":"Patient","Field":"Chief Complaint","Value":findings["chief_complaint"]})
    for dx in findings.get("diagnoses",[]):
        rows.append({"Category":"Diagnosis","Field":"Condition","Value":dx})
    for med in findings.get("medications",[]) or ["None listed"]:
        rows.append({"Category":"Medication","Field":"Drug","Value":med})
    for k,v in findings.get("vital_signs",{}).items():
        rows.append({"Category":"Vitals","Field":k,"Value":str(v)})
    for k,v in findings.get("lab_results",{}).items():
        rows.append({"Category":"Lab Result","Field":k,"Value":str(v)})

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, height=270,
        column_config={
            "Category":st.column_config.TextColumn(width="small"),
            "Field":st.column_config.TextColumn(width="medium"),
            "Value":st.column_config.TextColumn(width="large"),
        })
    st.markdown("</div>", unsafe_allow_html=True)

with col_f:
    st.markdown("<div class='panel'><div class='panel-title'>⚠️ Risk Flags & Actions</div>", unsafe_allow_html=True)
    flag_html = "".join(f"<span class='flag-tag'>⚑ {f}</span>" for f in flags)
    st.markdown(f"<div style='margin-bottom:.9rem'>{flag_html}</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:.73rem;color:#8b949e;font-family:IBM Plex Mono,monospace;margin:.5rem 0 .4rem;text-transform:uppercase;letter-spacing:.08em'>Primary Concerns</div>", unsafe_allow_html=True)
    for c in risk.get("primary_concerns",[]):
        st.markdown(f"<div style='font-size:.8rem;padding:3px 0;color:#c9d1d9;border-bottom:1px solid #21262d'>→ {c}</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:.73rem;color:#8b949e;font-family:IBM Plex Mono,monospace;margin:.7rem 0 .4rem;text-transform:uppercase;letter-spacing:.08em'>Recommended Actions</div>", unsafe_allow_html=True)
    for a in risk.get("recommended_actions",[]):
        st.markdown(f"<div style='font-size:.78rem;padding:2px 0;color:#79c0ff'>✦ {a}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  XAI EXPLANATION
# ══════════════════════════════════════════════
st.markdown("<div class='panel'><div class='panel-title'>💡 XAI — Plain Language Explanation for Clinician</div>", unsafe_allow_html=True)
st.markdown(f"<div class='xai-box'>{xai.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  BAR CHART
# ══════════════════════════════════════════════
st.markdown("<div class='panel'><div class='panel-title'>📊 Risk Breakdown by Dimension</div>", unsafe_allow_html=True)
dims = findings["risk_dimensions"]
fig_b = go.Figure(go.Bar(
    x=list(dims.values()), y=[k.capitalize() for k in dims], orientation="h",
    marker=dict(color=list(dims.values()),
                colorscale=[[0,"#1a3a1a"],[.3,"#3fb950"],[.6,"#d29922"],[.8,"#f85149"],[1,"#ff6b6b"]],
                cmin=0, cmax=100),
    text=[str(v) for v in dims.values()],
    textposition="outside",
    textfont=dict(color="#8b949e",family="IBM Plex Mono",size=11),
))
fig_b.update_layout(
    paper_bgcolor="#161b22", plot_bgcolor="#161b22",
    xaxis=dict(range=[0,115],gridcolor="#21262d",color="#484f58",tickfont=dict(color="#484f58")),
    yaxis=dict(color="#8b949e",tickfont=dict(color="#8b949e",family="IBM Plex Mono",size=12)),
    margin=dict(t=10,b=10,l=10,r=60), height=220, bargap=.35,
)
st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar":False})
st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  CLINICAL REPORT VIEWER
# ══════════════════════════════════════════════
with st.expander("📄 View Original Clinical Report"):
    st.markdown(f"""
<div style='background:#0d1117;border:1px solid #30363d;border-radius:8px;
            padding:1rem 1.2rem;font-family:IBM Plex Mono,monospace;
            font-size:.8rem;color:#8b949e;white-space:pre-wrap;line-height:1.7'>
{case["report"]}
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════
st.markdown("""
<div style='text-align:center;padding:1.5rem 0 .5rem;font-size:.69rem;
            color:#484f58;font-family:IBM Plex Mono,monospace;
            border-top:1px solid #21262d;margin-top:.5rem'>
  ⚕️ MedGuard-XAI is a research prototype and decision-support tool only.
  All outputs require validation by a licensed physician.<br>
  Built by Fatima Rayane · CS × Biomedical AI · SMART Shenzhen Application Demo
</div>
""", unsafe_allow_html=True)
