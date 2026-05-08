"""
MedGuard-XAI — Clinical Risk Intelligence Dashboard (DEMO MODE)
NO API KEY REQUIRED — Perfect for SMART Shenzhen submission
Run: streamlit run dashboard_mock.py
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="MedGuard-XAI", page_icon="🏥", layout="wide")

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
    
    # Risk flags
    risk_flags = []
    if "chest pain" in report_lower and ("diabetes" in report_lower or "hypertension" in report_lower):
        risk_flags.append("Cardiac risk: Chest pain + metabolic syndrome")
    if "fever" in report_lower and "rash" in report_lower:
        risk_flags.append("Infectious risk: Fever with rash - urgent evaluation needed")
    if "inr" in report_lower and ("3." in report_lower or "high" in report_lower):
        risk_flags.append("Bleeding risk: Supratherapeutic INR")
    if "troponin" in report_lower and "elevated" in report_lower:
        risk_flags.append("Cardiac risk: Elevated troponin suggestive of myocardial injury")
    if "hba1c" in report_lower and "9" in report_lower:
        risk_flags.append("Metabolic risk: Poorly controlled diabetes")
    
    # Risk dimensions
    risk_dimensions = {
        "Cardiac": 70 if "chest pain" in report_lower or "troponin" in report_lower else 20,
        "Metabolic": 80 if "diabetes" in report_lower or "hba1c" in report_lower else 30,
        "Infection": 85 if "fever" in report_lower or "rash" in report_lower else 15,
        "Medication": 60 if "warfarin" in report_lower or "inr" in report_lower else 10,
        "Neurological": 50 if "stroke" in report_lower or "confusion" in report_lower else 10,
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
    # Calculate risk score based on flags and dimensions
    flags_count = len(findings.get("risk_flags", []))
    dims = findings.get("risk_dimensions", {})
    avg_risk = sum(dims.values()) / len(dims) if dims else 0
    
    risk_score = min(100, int(avg_risk * 0.7 + flags_count * 8))
    
    # Determine risk level
    if risk_score >= 70:
        overall_risk = "HIGH"
    elif risk_score >= 40:
        overall_risk = "MODERATE"
    else:
        overall_risk = "LOW"
    
    # Special cases for critical
    if "fever" in str(findings) and "rash" in str(findings):
        overall_risk = "CRITICAL"
        risk_score = 92
    
    # Generate reasoning
    reasoning = ""
    if "Cardiac" in dims and dims["Cardiac"] > 60:
        reasoning = "Patient presents with cardiac risk factors including elevated troponin and chest pain. Combined with metabolic syndrome, this suggests possible acute coronary syndrome."
    elif "Infection" in dims and dims["Infection"] > 70:
        reasoning = "High fever with rash and rapid deterioration suggests possible meningococcal infection. Neurological symptoms (neck stiffness, photophobia) increase urgency."
    elif "Metabolic" in dims and dims["Metabolic"] > 70:
        reasoning = "Poorly controlled diabetes (HbA1c >9%) with elevated glucose and multiple comorbidities increases risk of complications."
    else:
        reasoning = "Multiple risk factors identified requiring clinical correlation. Patient would benefit from comprehensive evaluation."
    
    # Primary concerns
    primary_concerns = findings.get("risk_flags", [])[:3]
    if not primary_concerns:
        primary_concerns = ["Routine monitoring recommended"]
    
    # Recommended actions
    recommended_actions = []
    if "Cardiac" in dims and dims["Cardiac"] > 60:
        recommended_actions.append("Cardiology consult within 24 hours")
        recommended_actions.append("Serial troponin and ECG monitoring")
    if "Infection" in dims and dims["Infection"] > 70:
        recommended_actions.append("Immediate infectious disease evaluation")
        recommended_actions.append("Blood cultures and empiric antibiotics")
    if "Metabolic" in dims and dims["Metabolic"] > 70:
        recommended_actions.append("Endocrinology referral for diabetes management")
        recommended_actions.append("Diabetes education and medication adjustment")
    if not recommended_actions:
        recommended_actions.append("Follow up with primary care within 1-2 weeks")
        recommended_actions.append("Monitor symptoms and return if worsens")
    
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
    for flag in findings.get('risk_flags', [])[:3]:
        explanation += f"- **{flag}** — This combination of findings requires prompt clinical attention.\n"
    
    explanation += f"""
## 🔍 AI Reasoning Transparency

> {risk['reasoning']}

The risk assessment is based on:
- Presence of {len(findings.get('diagnoses', []))} active diagnoses
- {len(findings.get('medications', []))} medications identified
- {len(findings.get('lab_results', {}))} laboratory values analyzed

## 💊 Suggested Clinical Actions

"""
    for action in risk.get('recommended_actions', [])[:3]:
        explanation += f"- {action}\n"
    
    explanation += f"""
## ⚡ Confidence & Limitations

**Confidence:** {risk['confidence']}

*The AI's confidence is based on pattern matching against known clinical presentations. 
This analysis is limited to information explicitly mentioned in the report. 
Missing data would affect accuracy.*

---
*This is a decision-support tool only. Clinical judgment required.*
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
    st.caption("Mock AI for demonstration. Real version uses GPT-4.")
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
                st.session_state.history.insert(0, st.session_state.current)
                st.rerun()
    
    st.markdown("---")
    st.caption("⚠️ **Demo Mode** - Uses rule-based simulation. The production version uses OpenAI's GPT-4o-mini for real AI understanding.")

# ============================================================
# DISPLAY RESULTS
# ============================================================
st.markdown("# 🏥 MedGuard-XAI")
st.markdown("### Clinical Risk Intelligence Dashboard")

if "current" not in st.session_state or not st.session_state.current:
    st.info("👈 Select a sample report or paste your own, then click **Analyze Report**")
    st.stop()

d = st.session_state.current
findings = d["findings"]
risk = d["risk"]
score = risk["risk_score"]
level = risk["overall_risk"]

risk_color = {"LOW": "🟢", "MODERATE": "🟡", "HIGH": "🔴", "CRITICAL": "🚨"}.get(level, "⚪")

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Risk Score", f"{score}/100")
with c2: st.metric("Risk Level", f"{risk_color} {level}")
with c3: st.metric("Risk Flags", len(findings.get("risk_flags", [])))
with c4: st.metric("Confidence", risk.get("confidence", "MEDIUM"))

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧬 Extracted Findings")
    findings_data = []
    if findings.get("patient_age"): findings_data.append({"Field": "Age", "Value": findings["patient_age"]})
    if findings.get("patient_gender"): findings_data.append({"Field": "Gender", "Value": findings["patient_gender"]})
    if findings.get("chief_complaint"): findings_data.append({"Field": "Chief Complaint", "Value": findings["chief_complaint"][:80]})
    for dx in findings.get("diagnoses", []): findings_data.append({"Field": "Diagnosis", "Value": dx})
    for med in findings.get("medications", []): findings_data.append({"Field": "Medication", "Value": med})
    if findings_data:
        st.dataframe(pd.DataFrame(findings_data), use_container_width=True, hide_index=True)

with col2:
    st.markdown("### 🎯 Risk Radar")
    dims = findings.get("risk_dimensions", {})
    if dims:
        fig = go.Figure(data=go.Scatterpolar(
            r=list(dims.values()), theta=list(dims.keys()), fill="toself",
            line=dict(color="#f85149" if level in ["HIGH", "CRITICAL"] else "#3fb950", width=2)
        ))
        fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100])), height=280, margin=dict(l=30, r=30))
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### 💡 Clinical Explanation")
st.markdown(d["explanation"])

st.markdown("---")
st.caption("⚠️ **Medical Disclaimer:** Decision-support tool only. Clinical judgment required.")
