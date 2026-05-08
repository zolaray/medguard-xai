"""
MedGuard-XAI — Clinical Risk Intelligence Dashboard (DEMO MODE)
NO API KEY REQUIRED — Perfect for SMART Shenzhen submission
Live Demo: https://medguard-xai.streamlit.app
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="MedGuard-XAI", page_icon="🏥", layout="wide")

# ============================================================
# INITIALIZE SESSION STATE
# ============================================================
if "history" not in st.session_state:
    st.session_state.history = []
if "current" not in st.session_state:
    st.session_state.current = None

# ============================================================
# MOCK AI FUNCTIONS (No API Key Needed)
# ============================================================

def mock_extract_findings(report_text):
    """Simulate AI extraction using keyword matching"""
    report_lower = report_text.lower()
    
    # Extract age
    age_match = re.search(r'(\d+)\s*(?:years?|y/o)', report_lower)
    age = age_match.group(1) if age_match else "unknown"
    
    # Extract gender
    gender = "Male" if "male" in report_lower else "Female" if "female" in report_lower else "Unknown"
    
    # Chief complaint extract
    complaint_match = re.search(r'chief complaint:?([^\n]+)', report_lower)
    chief_complaint = complaint_match.group(1).strip() if complaint_match else "Not specified"
    
    # Diagnoses based on keywords
    diagnoses = []
    if "diabetes" in report_lower or "dm" in report_lower or "hba1c" in report_lower:
        diagnoses.append("Type 2 Diabetes Mellitus")
    if "hypertension" in report_lower or "htn" in report_lower or "bp" in report_lower:
        diagnoses.append("Hypertension")
    if "chest pain" in report_lower or "angina" in report_lower or "troponin" in report_lower:
        diagnoses.append("Possible Acute Coronary Syndrome")
    if "fever" in report_lower and "rash" in report_lower:
        diagnoses.append("Suspected Meningococcemia")
    if "pneumonia" in report_lower or "lung" in report_lower:
        diagnoses.append("Pneumonia")
    if "wbc" in report_lower and "elevated" in report_lower:
        diagnoses.append("Systemic Infection")
    
    # Medications
    medications = []
    med_keywords = ["metformin", "amlodipine", "lisinopril", "warfarin", "enoxaparin", 
                    "paracetamol", "ibuprofen", "aspirin", "atorvastatin"]
    for med in med_keywords:
        if med in report_lower:
            medications.append(med.title())
    
    # Vital signs
    vitals = {}
    bp_match = re.search(r'bp:?\s*(\d+)/(\d+)', report_lower)
    if bp_match:
        vitals["BP"] = f"{bp_match.group(1)}/{bp_match.group(2)}"
    hr_match = re.search(r'hr:?\s*(\d+)', report_lower)
    if hr_match:
        vitals["HR"] = hr_match.group(1)
    temp_match = re.search(r'temp:?\s*([\d.]+)', report_lower)
    if temp_match:
        vitals["Temperature"] = f"{temp_match.group(1)}°C"
    
    # Lab results
    labs = {}
    hba1c_match = re.search(r'hba1c:?\s*([\d.]+%?)', report_lower)
    if hba1c_match:
        labs["HbA1c"] = hba1c_match.group(1)
    glucose_match = re.search(r'glucose:?\s*(\d+)', report_lower)
    if glucose_match:
        labs["Glucose"] = f"{glucose_match.group(1)} mg/dL"
    troponin_match = re.search(r'troponin:?\s*([\d.]+)', report_lower)
    if troponin_match:
        labs["Troponin"] = f"{troponin_match.group(1)} ng/mL (elevated)"
    wbc_match = re.search(r'wbc:?\s*([\d.]+)', report_lower)
    if wbc_match:
        labs["WBC"] = f"{wbc_match.group(1)} x10^9/L"
    crp_match = re.search(r'crp:?\s*([\d.]+)', report_lower)
    if crp_match:
        labs["CRP"] = f"{crp_match.group(1)} mg/L"
    
    # Risk flags
    risk_flags = []
    if "chest pain" in report_lower and ("diabetes" in report_lower or "hypertension" in report_lower):
        risk_flags.append("Cardiac risk: Chest pain + metabolic syndrome")
    if "fever" in report_lower and "rash" in report_lower:
        risk_flags.append("Infectious risk: Fever with rash - urgent evaluation needed")
    if "neck stiffness" in report_lower or "photophobia" in report_lower:
        risk_flags.append("Neurological risk: Meningeal signs present")
    if "hypotension" in report_lower or ("bp" in report_lower and "95" in report_lower and "60" in report_lower):
        risk_flags.append("Hemodynamic risk: Hypotension suggestive of sepsis")
    if "inr" in report_lower and ("3." in report_lower or "high" in report_lower):
        risk_flags.append("Bleeding risk: Supratherapeutic INR")
    if "troponin" in report_lower and "elevated" in report_lower:
        risk_flags.append("Cardiac risk: Elevated troponin suggestive of myocardial injury")
    if "hba1c" in report_lower and "9" in report_lower:
        risk_flags.append("Metabolic risk: Poorly controlled diabetes")
    
    # Risk dimensions - FIXED LINE
    risk_dimensions = {
        "Cardiac": 70 if "chest pain" in report_lower or "troponin" in report_lower else 20,
        "Metabolic": 80 if "diabetes" in report_lower or "hba1c" in report_lower else 30,
        "Infection": 85 if ("fever" in report_lower or "rash" in report_lower or "wbc" in report_lower) else 15,
        "Medication": 60 if "warfarin" in report_lower or "inr" in report_lower else 10,
        "Neurological": 75 if "neck stiffness" in report_lower or "photophobia" in report_lower else 10,
    }
    
    # Determine report type
    if "lab" in report_lower:
        report_type = "lab_report"
    elif "discharge" in report_lower:
        report_type = "discharge_summary"
    elif "radiology" in report_lower or "xray" in report_lower or "ct" in report_lower:
        report_type = "radiology"
    else:
        report_type = "clinical_note"
    
    return {
        "patient_age": age,
        "patient_gender": gender,
        "chief_complaint": chief_complaint,
        "diagnoses": diagnoses,
        "medications": medications,
        "vital_signs": vitals,
        "lab_results": labs,
        "risk_flags": risk_flags,
        "risk_dimensions": risk_dimensions,
        "report_type": report_type,
    }

def mock_analyze_risk(findings):
    """Simulate risk analysis based on findings"""
    flags_count = len(findings.get("risk_flags", []))
    dims = findings.get("risk_dimensions", {})
    avg_risk = sum(dims.values()) / len(dims) if dims else 0
    
    risk_score = min(100, int(avg_risk * 0.7 + flags_count * 8))
    
    if risk_score >= 70:
        overall_risk = "HIGH"
    elif risk_score >= 40:
        overall_risk = "MODERATE"
    else:
        overall_risk = "LOW"
    
    findings_str = str(findings)
    if "fever" in findings_str and "rash" in findings_str:
        if "neck stiffness" in findings_str or "hypotension" in findings_str:
            overall_risk = "CRITICAL"
            risk_score = 94
    
    # Generate reasoning
    if findings.get("risk_dimensions", {}).get("Cardiac", 0) > 60:
        reasoning = "Patient presents with cardiac risk factors including elevated troponin and chest pain. Combined with metabolic syndrome, this suggests possible acute coronary syndrome."
    elif findings.get("risk_dimensions", {}).get("Infection", 0) > 70:
        reasoning = "High fever with rash and meningeal signs suggests possible meningococcal infection. Hypotension indicates hemodynamic compromise - this is a medical emergency."
    elif findings.get("risk_dimensions", {}).get("Neurological", 0) > 60:
        reasoning = "Neurological symptoms including neck stiffness and photophobia raise concern for meningitis. Requires immediate evaluation."
    elif findings.get("risk_dimensions", {}).get("Metabolic", 0) > 70:
        reasoning = "Poorly controlled diabetes (HbA1c >9%) with elevated glucose and multiple comorbidities increases risk of complications."
    else:
        reasoning = "Multiple risk factors identified requiring clinical correlation. Patient would benefit from comprehensive evaluation."
    
    primary_concerns = findings.get("risk_flags", [])[:3]
    if not primary_concerns:
        primary_concerns = ["Routine monitoring recommended"]
    
    recommended_actions = []
    risk_dims = findings.get("risk_dimensions", {})
    if risk_dims.get("Cardiac", 0) > 60:
        recommended_actions.append("Cardiology consult within 24 hours")
        recommended_actions.append("Serial troponin and ECG monitoring")
    if risk_dims.get("Infection", 0) > 70:
        recommended_actions.append("Immediate infectious disease evaluation")
        recommended_actions.append("Blood cultures and empiric antibiotics")
    if risk_dims.get("Neurological", 0) > 60:
        recommended_actions.append("Neurology consult urgently")
        recommended_actions.append("Lumbar puncture if no contraindication")
    if risk_dims.get("Metabolic", 0) > 70:
        recommended_actions.append("Endocrinology referral for diabetes management")
        recommended_actions.append("Diabetes education and medication adjustment")
    if not recommended_actions:
        recommended_actions.append("Follow up with primary care within 1-2 weeks")
        recommended_actions.append("Monitor symptoms and return if worsens")
    
    recommended_actions.append("This is a decision-support tool. Clinical judgment required.")
    
    return {
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "primary_concerns": primary_concerns,
        "reasoning": reasoning,
        "recommended_actions": recommended_actions,
        "confidence": "HIGH" if risk_score > 60 or risk_score < 20 else "MEDIUM",
    }

def mock_generate_explanation(report_text, findings, risk):
    """Generate a clinical explanation without API"""
    level = risk["overall_risk"]
    
    explanation = f"""
## 📋 Summary

This patient presents with {findings.get('chief_complaint', 'a clinical condition')}. 
The AI has identified {len(findings.get('risk_flags', []))} risk flags and assigned a 
**{level}** risk level ({risk['risk_score']}/100).

## ⚠️ Key Findings & Why They Matter

"""
    for flag in findings.get('risk_flags', [])[:4]:
        explanation += f"- **{flag}**\n"
    
    explanation += f"""
## 🔍 AI Reasoning Transparency

{risk['reasoning']}

The risk assessment is based on:
- {len(findings.get('diagnoses', []))} active diagnoses identified
- {len(findings.get('medications', []))} medications detected
- {len(findings.get('lab_results', {}))} laboratory values analyzed
- {len(findings.get('vital_signs', {}))} vital signs reviewed

## 💊 Suggested Clinical Actions

"""
    for action in risk.get('recommended_actions', [])[:4]:
        explanation += f"- {action}\n"
    
    explanation += f"""
## ⚡ Confidence & Limitations

**Confidence Level:** {risk['confidence']}

*The AI's confidence is based on pattern matching against known clinical presentations. 
This analysis is limited to information explicitly mentioned in the report. 
Missing data (e.g., allergies, family history) would affect accuracy.*

---
*This is a decision-support tool only. Final clinical judgment required.*
"""
    return explanation

# ============================================================
# SAMPLE REPORTS
# ============================================================
SAMPLE_REPORTS = {
    "Diabetic Patient with Chest Pain": """
PATIENT: Male, 58 years old
CHIEF COMPLAINT: Chest pain and shortness of breath for 3 days
VITALS: BP 158/96, HR 102, SpO2 94%, Temp 37.2°C
MEDICATIONS: Metformin, Amlodipine
LABS: HbA1c 9.8%, Troponin I 0.08 ng/mL (elevated), BNP 420 pg/mL, LDL 142
HISTORY: Type 2 diabetes, hypertension, smoker
NOTE: ECG shows ST depression.
""",
    "Pediatric Fever & Rash": """
PATIENT: Female, 7 years old
CHIEF COMPLAINT: High fever and rash for 2 days
VITALS: Temp 39.8°C, HR 124, BP 95/60
LABS: WBC 18.4 (elevated), CRP 85 mg/L (elevated), Platelets 98 (low)
NOTE: Non-blanching rash on lower limbs, neck stiffness, photophobia. Rapid deterioration.
""",
    "Post-Op Elderly Patient": """
PATIENT: Female, 74 years old
POST-OPERATIVE DAY 2: Right hip replacement
VITALS: BP 102/68, Temp 38.1°C, SpO2 96%
MEDICATIONS: Warfarin, Enoxaparin
LABS: INR 3.8 (supratherapeutic), Hemoglobin 8.2 g/dL, CRP 112 mg/L
NOTE: Increasing right leg pain and swelling. Confused this morning.
""",
}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("# 🏥 MedGuard-XAI")
    st.markdown("**DEMO MODE** — No API Key Required")
    st.caption("Mock AI for demonstration. Real version uses GPT-4o-mini.")
    st.markdown("---")
    
    sample = st.selectbox("Load Sample Report", list(SAMPLE_REPORTS.keys()))
    
    report = st.text_area("Clinical Report", value=SAMPLE_REPORTS[sample], height=300)
    
    if st.button("🔬 Analyze Report", type="primary", use_container_width=True):
        if not report.strip():
            st.error("Please enter a clinical report")
        else:
            with st.spinner("Analyzing (Mock AI)..."):
                findings = mock_extract_findings(report)
                risk = mock_analyze_risk(findings)
                explanation = mock_generate_explanation(report, findings, risk)
                st.session_state.current = {
                    "findings": findings,
                    "risk": risk,
                    "explanation": explanation,
                    "time": datetime.now().strftime("%H:%M")
                }
                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.insert(0, st.session_state.current)
                st.rerun()
    
    st.markdown("---")
    st.caption("⚠️ **Demo Mode** - Uses rule-based simulation. The production version uses OpenAI's GPT-4o-mini for real AI understanding.")

# ============================================================
# DISPLAY RESULTS
# ============================================================
st.markdown("# 🏥 MedGuard-XAI")
st.markdown("### Clinical Risk Intelligence Dashboard")

if "current" not in st.session_state or st.session_state.current is None:
    st.info("👈 Select a sample report or paste your own, then click **Analyze Report**")
    st.stop()

d = st.session_state.current
findings = d["findings"]
risk = d["risk"]
score = risk["risk_score"]
level = risk["overall_risk"]

risk_emoji = {"LOW": "🟢", "MODERATE": "🟡", "HIGH": "🔴", "CRITICAL": "🚨"}.get(level, "⚪")

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Risk Score", f"{score}/100")
with col2: st.metric("Risk Level", f"{risk_emoji} {level}")
with col3: st.metric("Risk Flags", len(findings.get("risk_flags", [])))
with col4: st.metric("Confidence", risk.get("confidence", "MEDIUM"))

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🧬 Extracted Findings")
    findings_data = []
    if findings.get("patient_age"): findings_data.append({"Field": "Age", "Value": findings["patient_age"]})
    if findings.get("patient_gender"): findings_data.append({"Field": "Gender", "Value": findings["patient_gender"]})
    if findings.get("chief_complaint"): findings_data.append({"Field": "Chief Complaint", "Value": findings["chief_complaint"][:80]})
    for dx in findings.get("diagnoses", []): findings_data.append({"Field": "Diagnosis", "Value": dx})
    for med in findings.get("medications", []): findings_data.append({"Field": "Medication", "Value": med})
    for lab, val in findings.get("lab_results", {}).items(): findings_data.append({"Field": f"Lab: {lab}", "Value": val})
    if findings_data:
        st.dataframe(pd.DataFrame(findings_data), use_container_width=True, hide_index=True)
    else:
        st.info("No structured findings extracted")

with col_right:
    st.markdown("### 🎯 Risk Radar Chart")
    dims = findings.get("risk_dimensions", {})
    if dims and any(dims.values()):
        fig = go.Figure(data=go.Scatterpolar(
            r=list(dims.values()), 
            theta=list(dims.keys()), 
            fill="toself",
            line=dict(color="#f85149" if level in ["HIGH", "CRITICAL"] else "#d29922" if level == "MODERATE" else "#3fb950", width=2)
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(range=[0, 100], tickfont=dict(size=10))),
            height=300,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Risk dimensions will appear after analysis")
    
    st.markdown("### ⚠️ Risk Flags")
    for flag in findings.get("risk_flags", [])[:3]:
        st.markdown(f"- 🚩 {flag}")

st.markdown("---")

st.markdown("### 💡 AI Clinical Explanation (XAI)")
st.markdown(d["explanation"])

st.markdown("---")
st.caption("""
⚠️ **Medical Disclaimer:** MedGuard-XAI is a research prototype and decision-support tool only. 
All outputs must be reviewed and validated by a licensed physician. 
Not for clinical use without human oversight.
""")
