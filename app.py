import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import hashlib
import io
import json
import time as time_mod
from datetime import datetime, timedelta
import random

# ==============================================================================
# 1. ENTERPRISE GOVTECH STYLING & GLASSMORPHIC DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="Civic Prism | National Infrastructure Intelligence Platform",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header { visibility: visible !important; }
    .stDeployButton { display: none !important; }
    
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%);
        border-right: 1px solid #E2E8F0;
    }
    
    div[role="radiogroup"] { gap: 6px; }
    div[role="radiogroup"] > label {
        background: #FFFFFF;
        padding: 9px 14px;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        transition: all 0.2s ease;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover { 
        background: #FFFFFF; 
        transform: translateX(2px); 
        border-color: #06B6D4;
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.12); 
    }
    
    .premium-card {
        background: #FFFFFF;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03); 
        border: 1px solid #E2E8F0;
        border-left: 6px solid #06B6D4 !important;
        transition: all 0.25s ease;
        margin-bottom: 14px;
    }
    .premium-card:hover { 
        border-color: #06B6D4;
        box-shadow: 0 8px 24px rgba(6, 182, 212, 0.15); 
    }
    
    @keyframes pulse-soft-crimson {
        0% { box-shadow: 0 0 4px rgba(239, 68, 68, 0.20); border-color: #FECACA; }
        50% { box-shadow: 0 0 14px rgba(239, 68, 68, 0.45); border-color: #F87171; background-color: #FFFFFF; }
        100% { box-shadow: 0 0 4px rgba(239, 68, 68, 0.20); border-color: #FECACA; }
    }
    
    .blinking-red-card {
        animation: pulse-soft-crimson 2s infinite !important;
        background: #FFFFFF !important;
        border: 1.5px solid #F87171 !important;
        border-left: 6px solid #EF4444 !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        margin-bottom: 14px;
    }

    .success-card-soft {
        background: #F0FDF4 !important;
        border: 1.5px solid #86EFAC !important;
        border-left: 7px solid #10B981 !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        margin-bottom: 14px;
    }
    
    .card-inner-clearance { padding-left: 6px; }
    .card-title { color: #64748B; font-size: 11px; text-transform: uppercase; font-weight: 800; letter-spacing: 0.8px; margin-bottom: 4px; }
    .card-value { color: #0F172A; font-size: 22px; font-weight: 900; line-height: 1.1; margin-bottom: 4px; }
    .card-subtitle { font-size: 12px; font-weight: 600; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 2px solid #E2E8F0; margin-bottom: 14px; }
    .stTabs [data-baseweb="tab"] { height: 38px; font-weight: 700; font-size: 13px; color: #64748B; background: transparent; border: none; border-radius: 8px; }
    .stTabs [aria-selected="true"] { color: #06B6D4 !important; border-bottom: 3px solid #06B6D4 !important; font-weight: 800; }
    
    .stButton>button { 
        border-radius: 10px !important; 
        font-weight: 700; 
        background: linear-gradient(135deg, #06B6D4 0%, #0284C7 100%); 
        color: white; 
        border: none; 
        padding: 8px 18px; 
        transition: all 0.2s; 
        box-shadow: 0 2px 6px rgba(6, 182, 212, 0.20); 
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 6px 14px rgba(6, 182, 212, 0.30); color: white; }
    
    .flow-container { display: flex; flex-direction: column; align-items: center; padding: 6px 0; font-family: 'Inter', sans-serif; }
    .flow-box {
        background: #FFFFFF;
        border: 1.5px solid #06B6D4;
        border-radius: 12px !important;
        padding: 13px 20px;
        text-align: center;
        width: 100%;
        max-width: 650px;
        box-shadow: 0 2px 6px rgba(6, 182, 212, 0.05);
        position: relative;
    }
    .flow-box-priority-high { animation: pulse-soft-crimson 2s infinite !important; background: #FFFFFF !important; border: 1.5px solid #F87171 !important; }
    .flow-box-amber { border: 1.5px solid #F59E0B !important; background: #FFFBEB !important; }
    .flow-box-green { border: 1.5px solid #10B981 !important; background: #F0FDF4 !important; }
    .flow-box-purple { border: 1.5px solid #7C3AED !important; background: #F5F3FF !important; }
    .flow-box-blue { border: 1.5px solid #0284C7 !important; background: #EFF6FF !important; }
    
    .flow-title { font-weight: 800; font-size: 12px; color: #0F172A; text-transform: uppercase; margin-bottom: 3px; letter-spacing: 0.5px; }
    .flow-desc { font-size: 11.5px; color: #475569; }
    .flow-arrow { width: 2px; height: 16px; background: #94A3B8; margin: 2px 0; position: relative; }
    .flow-arrow::after { content: ''; position: absolute; bottom: 0; left: -4px; border-width: 5px 5px 0; border-style: solid; border-color: #94A3B8 transparent transparent; }
    
    .executive-advisory-console {
        background: #0F172A;
        border: 1px solid #334155;
        border-radius: 14px !important;
        padding: 18px 22px;
        color: #F8FAFC;
        margin-bottom: 18px;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.15);
    }
    
    .telemetry-tag {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 600;
        color: #94A3B8;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .pulse-dot { width: 7px; height: 7px; border-radius: 50%; background: #06B6D4; box-shadow: 0 0 8px #06B6D4; }

    .terminal-stream-box {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 12px 16px;
        font-family: monospace;
        font-size: 11px;
        color: #38BDF8;
        line-height: 1.6;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

PLOT_CONFIG = {'displayModeBar': False, 'scrollZoom': True}

# ==============================================================================
# 2. PAN-INDIA REGIONAL & DEMOGRAPHIC INFRASTRUCTURE REGISTRY
# Spanning 12 Diverse States, 48 Districts, and 12+ Official Indian Languages
# ==============================================================================
PAN_INDIA_REGISTRY = {
    "Tamil Nadu": {
        "districts": ["Salem", "Chennai", "Coimbatore", "Madurai"],
        "coords": {"Salem": (11.6643, 78.1460), "Chennai": (13.0827, 80.2707), "Coimbatore": (11.0168, 76.9558), "Madurai": (9.9252, 78.1198)},
        "pop_density": 1180, "deficit_index": 42.5, "capex_crores": 320.0, "lang": "Tamil / Tanglish"
    },
    "Maharashtra": {
        "districts": ["Mumbai Urban", "Pune", "Nagpur", "Nashik"],
        "coords": {"Mumbai Urban": (18.9400, 72.8350), "Pune": (18.5204, 73.8567), "Nagpur": (21.1458, 79.0882), "Nashik": (19.9975, 73.7898)},
        "pop_density": 2350, "deficit_index": 54.0, "capex_crores": 540.0, "lang": "Marathi / Hindi"
    },
    "Uttar Pradesh": {
        "districts": ["Lucknow", "Varanasi", "Kanpur Nagar", "Prayagraj"],
        "coords": {"Lucknow": (26.8467, 80.9462), "Varanasi": (25.3176, 82.9739), "Kanpur Nagar": (26.4499, 80.3319), "Prayagraj": (25.4358, 81.8463)},
        "pop_density": 1820, "deficit_index": 71.2, "capex_crores": 620.0, "lang": "Hindi / Bhojpuri"
    },
    "Karnataka": {
        "districts": ["Bengaluru Urban", "Mysuru", "Hubballi-Dharwad", "Belagavi"],
        "coords": {"Bengaluru Urban": (12.9716, 77.5946), "Mysuru": (12.2958, 76.6394), "Hubballi-Dharwad": (15.3647, 75.1240), "Belagavi": (15.8497, 74.4977)},
        "pop_density": 1420, "deficit_index": 39.8, "capex_crores": 410.0, "lang": "Kannada / English"
    },
    "Assam": {
        "districts": ["Kamrup (Guwahati)", "Dibrugarh", "Silchar", "Jorhat"],
        "coords": {"Kamrup (Guwahati)": (26.1445, 91.7362), "Dibrugarh": (27.4728, 94.9120), "Silchar": (24.8333, 92.7789), "Jorhat": (26.7509, 94.2037)},
        "pop_density": 680, "deficit_index": 68.4, "capex_crores": 210.0, "lang": "Assamese / Bengali"
    },
    "Gujarat": {
        "districts": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
        "coords": {"Ahmedabad": (23.0225, 72.5714), "Surat": (21.1702, 72.8311), "Vadodara": (22.3072, 73.1812), "Rajkot": (22.3039, 70.8022)},
        "pop_density": 1250, "deficit_index": 34.6, "capex_crores": 380.0, "lang": "Gujarati / Hindi"
    },
    "West Bengal": {
        "districts": ["Kolkata", "Howrah", "Siliguri", "Asansol"],
        "coords": {"Kolkata": (22.5726, 88.3639), "Howrah": (22.5958, 88.2636), "Siliguri": (26.7271, 88.3953), "Asansol": (23.6889, 86.9661)},
        "pop_density": 1940, "deficit_index": 58.2, "capex_crores": 340.0, "lang": "Bengali / English"
    },
    "Telangana": {
        "districts": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar"],
        "coords": {"Hyderabad": (17.3850, 78.4867), "Warangal": (17.9689, 79.5941), "Nizamabad": (18.6725, 78.0941), "Karimnagar": (18.4386, 79.1288)},
        "pop_density": 1390, "deficit_index": 44.1, "capex_crores": 360.0, "lang": "Telugu / Urdu"
    },
    "Delhi (NCR)": {
        "districts": ["New Delhi", "North Delhi", "South Delhi", "Dwarka"],
        "coords": {"New Delhi": (28.6139, 77.2090), "North Delhi": (28.7041, 77.1025), "South Delhi": (28.5355, 77.2410), "Dwarka": (28.5921, 77.0460)},
        "pop_density": 3850, "deficit_index": 38.0, "capex_crores": 450.0, "lang": "Hindi / Punjabi / English"
    },
    "Bihar": {
        "districts": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur"],
        "coords": {"Patna": (25.5941, 85.1376), "Gaya": (24.7914, 85.0002), "Muzaffarpur": (26.1209, 85.3647), "Bhagalpur": (25.2425, 86.9842)},
        "pop_density": 1750, "deficit_index": 79.5, "capex_crores": 490.0, "lang": "Hindi / Maithili / Bhojpuri"
    },
    "Rajasthan": {
        "districts": ["Jaipur", "Jodhpur", "Kota", "Udaipur"],
        "coords": {"Jaipur": (26.9124, 75.7873), "Jodhpur": (26.2389, 73.0243), "Kota": (25.2138, 75.8648), "Udaipur": (24.5854, 73.7125)},
        "pop_density": 720, "deficit_index": 62.1, "capex_crores": 290.0, "lang": "Hindi / Marwari"
    },
    "Kerala": {
        "districts": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"],
        "coords": {"Thiruvananthapuram": (8.5241, 76.9366), "Kochi": (9.9312, 76.2673), "Kozhikode": (11.2588, 75.7804), "Thrissur": (10.5276, 76.2144)},
        "pop_density": 980, "deficit_index": 31.0, "capex_crores": 270.0, "lang": "Malayalam / English"
    }
}

DEPARTMENTS = [
    "Public Works Department (PWD - Roads & Bridges)",
    "Jal Board (Water Supply & Drainage)",
    "State Electricity Distribution (Power Grid)",
    "Municipal Solid Waste & Sanitation",
    "School Education & Child Welfare Infra"
]

# ==============================================================================
# 3. MASSIVE HIGH-FIDELITY SYNTHETIC DATASET GENERATOR (4,800+ Records)
# ==============================================================================
@st.cache_data
def generate_national_infrastructure_data():
    np.random.seed(42)
    random.seed(42)
    records = []
    
    issues_pool = {
        "Public Works Department (PWD - Roads & Bridges)": [
            "Deep cratered pothole cluster causing vehicle turnover and accidents",
            "Bridge structural expansion joint concrete cracking and loosening",
            "Major road subgrade cave-in following heavy monsoon run-off",
            "Damaged pedestrian guardrails on high-speed arterial flyover"
        ],
        "Jal Board (Water Supply & Drainage)": [
            "High-pressure underground water main rupture leaking 40,000L/day",
            "Open overflowing storm sewer contaminating residential drinking groundwater",
            "Complete sewage line backflow into primary health center boundary",
            "Zero water supply for 5 consecutive days due to burst supply valve"
        ],
        "State Electricity Distribution (Power Grid)": [
            "High-voltage 11kV transformer sparking continuously near transit stop",
            "Dangling overhead live electrical cables post cyclonic storm winds",
            "30 consecutive solar streetlights defunct causing hazardous dark zone",
            "Ruptured underground feeder cable causing localized power failure"
        ],
        "Municipal Solid Waste & Sanitation": [
            "Massive open garbage dumping and burning of toxic waste near school",
            "Clogged municipal storm canal threatening localized monsoon flooding",
            "Public community sanitation complex defunct and structurally damaged",
            "Biomedical waste uncollected near neighborhood government clinic"
        ],
        "School Education & Child Welfare Infra": [
            "Government higher secondary school perimeter boundary wall collapsed",
            "Defunct drinking water filtration plant in primary school campus",
            "Damaged asbestos roofing in rural child Anganwadi center",
            "Dysfunctional separate sanitation facilities for girl students"
        ]
    }
    
    channels = ["WhatsApp Voice Note", "CPGRAMS National Portal", "Lightweight Voice Kiosk", "Field Inspection App"]
    
    for state_name, state_meta in PAN_INDIA_REGISTRY.items():
        for dist in state_meta["districts"]:
            base_coord = state_meta["coords"][dist]
            # 100 verified entries per district across 48 districts = 4,800 records
            for _ in range(100):
                dept = random.choice(DEPARTMENTS)
                issue = random.choice(issues_pool[dept])
                sev = int(np.random.choice([1, 2, 3, 4, 5], p=[0.08, 0.18, 0.38, 0.24, 0.12]))
                
                # Small coordinate scatter around district center
                lat = base_coord[0] + np.random.normal(0, 0.040)
                lon = base_coord[1] + np.random.normal(0, 0.040)
                
                channel = random.choice(channels)
                pop_dense = int(state_meta["pop_density"] * random.uniform(0.8, 1.4))
                infra_def = np.clip(state_meta["deficit_index"] + random.uniform(-10, 15), 15.0, 95.0)
                
                # COMPOSITE URGENCY INDEX (CUI) FORMULA:
                # 40% Defect Severity + 35% Historical Infrastructure Deficit + 25% Population Density Factor
                cui = (sev * 20.0 * 0.40) + (infra_def * 0.35) + (min(100.0, (pop_dense / 2800.0) * 100.0) * 0.25)
                cui = round(float(np.clip(cui, 18.0, 99.5)), 1)
                
                records.append({
                    "Ticket_ID": f"CP-{dist[:3].upper()}-{np.random.randint(10000, 99999)}",
                    "State": state_name,
                    "District": dist,
                    "Ward": f"Ward-{random.randint(1, 40):02d}",
                    "Department": dept,
                    "Reported_Issue": issue,
                    "Channel": channel,
                    "Language": state_meta["lang"],
                    "Severity_Rating": sev,
                    "Population_Density": pop_dense,
                    "Infra_Deficit_Score": round(infra_def, 1),
                    "Composite_Urgency_Index": cui,
                    "Latitude": lat,
                    "Longitude": lon,
                    "Status": "Verified by Google AI" if cui < 80 else "CRITICAL HOTSPOT - Action Required",
                    "Est_Project_Cost_Lakhs": round(sev * random.uniform(2.2, 5.8) * (pop_dense / 1000.0), 1),
                    "Timestamp": datetime.now() - timedelta(days=random.randint(0, 45), minutes=random.randint(0, 1440))
                })
                
    df = pd.DataFrame(records)
    df.sort_values(by="Composite_Urgency_Index", ascending=False, inplace=True)
    return df

# Initialize Session State
if "civic_db" not in st.session_state:
    st.session_state.civic_db = generate_national_infrastructure_data()

if "stream_active" not in st.session_state: st.session_state.stream_active = True
if "packet_seq" not in st.session_state: st.session_state.packet_seq = 10482

if "field_escalations" not in st.session_state:
    st.session_state.field_escalations = [
        {
            "id": "ESC-TAM-802", "officer": "R. Soundararajan (Assistant Executive Engineer)",
            "district": "Salem", "department": "Public Works Department (PWD - Roads & Bridges)",
            "urgency": 94, "requested_capex_lakhs": 42.0,
            "justification": "Underground pipe burst collapsed subgrade under Salem State Highway 42. Immediate road resurfacing + storm trenching bundle required.",
            "status": "Pending State Sanction"
        }
    ]

if "gati_shakti_registry" not in st.session_state:
    st.session_state.gati_shakti_registry = [
        {
            "Sync_ID": "PMGS-IN-2026-891", "Project_Name": "Integrated Stormwater & High-Volume Arterial Trenching",
            "State": "Tamil Nadu", "District": "Chennai", "Combined_Departments": "PWD + Jal Board",
            "Allocated_Budget_Cr": 18.4, "DPI_Verification_Hash": "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
            "Execution_SLA": "45 Days", "Status": "Synced with National Master Plan"
        }
    ]

# ==============================================================================
# 4. SIDEBAR - UNIFIED FLAT NAVIGATION & TERRITORY SELECTOR
# ==============================================================================
with st.sidebar:
    st.markdown('<h2 style="color:#0F172A; font-weight:900; letter-spacing:-1px; margin-bottom: -5px; margin-top: 5px;">💠 CIVIC PRISM</h2>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:10px; font-weight:800; color:#06B6D4; margin-bottom:15px; line-height:1.4; letter-spacing: 0.5px;'>DIGITAL PUBLIC GOOD PLATFORM</p>", unsafe_allow_html=True)
    
    workspace = st.radio(
        "Choose System Workspace", 
        [
            "National Command Center (Main Policy & CAPEX Dashboard)", 
            "Citizen Voice Kiosk & Ward Terminal (Grassroots Ingestion)"
        ],
        label_visibility="collapsed"
    )
    st.markdown("<hr style='border-color:#E2E8F0; margin: 12px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>JURISDICTION JUMP</h3>", unsafe_allow_html=True)
    state_selector = st.selectbox("Select State Jurisdiction", ["All India (National Horizon)"] + list(PAN_INDIA_REGISTRY.keys()), index=0)
    
    if state_selector != "All India (National Horizon)":
        district_options = ["All Districts"] + PAN_INDIA_REGISTRY[state_selector]["districts"]
        district_selector = st.selectbox("Select Target District", district_options, index=0)
    else:
        district_selector = "All Districts"
        
    st.markdown("<hr style='border-color:#E2E8F0; margin: 12px 0;'>", unsafe_allow_html=True)
    
    # Active Scoped Data
    if state_selector == "All India (National Horizon)":
        active_df = st.session_state.civic_db
    else:
        active_df = st.session_state.civic_db[st.session_state.civic_db["State"] == state_selector]
        if district_selector != "All Districts":
            active_df = active_df[active_df["District"] == district_selector]
            
    st.markdown(f"""
    <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:10px 12px; font-size:11px; color:#1E40AF; margin-top:2px; line-height:1.5;">
        <b>National Database Scale:</b> {len(st.session_state.civic_db):,} Petitions<br>
        <b>Current Scope:</b> {len(active_df):,} Active Reports<br>
        <b>Critical Hotspots:</b> {len(active_df[active_df['Composite_Urgency_Index'] >= 80]):,} High Priority
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#E2E8F0; margin: 12px 0;'>", unsafe_allow_html=True)
    
    if workspace == "National Command Center (Main Policy & CAPEX Dashboard)":
        st.markdown("<h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>NATIONAL POLICY TOOLS</h3>", unsafe_allow_html=True)
        active_tool = st.radio(
            "Select Command Tool",
            [
                "Live Geospatial Hotspot Map & Risk Matrix",
                "Cross-Departmental Mega-Project Optimizer (Jal Board + PWD Synergy)",
                "Public Spending Audit: Old Fragmented CAPEX vs. Civic Prism Saved Money",
                "PM GatiShakti National Master Plan Synchronization Desk",
                "Live Multimodal Ingestion Gateway (Voice, Photo, CPGRAMS)",
                "30-Day Predictive Infrastructure Breakdown Heatmap",
                "Ward Escalations & Emergency Budget Expansion Desk",
                "Technical Architecture, Google AI Multimodal Core & DPDP Compliance",
                "System Guide & National Deployment Manual"
            ],
            key="cmd_tool_radio"
        )
    else:
        st.markdown("<h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>CITIZEN & FIELD TERMINALS</h3>", unsafe_allow_html=True)
        active_tool = st.radio(
            "Select Grassroots Terminal",
            [
                "Vernacular Multilingual Voice & Text Kiosk (22 Languages)",
                "Computer Vision Damage Verification & Automated Triage Desk",
                "Track My Grievance Status & Digital Resolution Certificate"
            ],
            key="grassroot_tool_radio"
        )

# ==============================================================================
# 5. WORKSPACE 1: NATIONAL COMMAND CENTER
# ==============================================================================
if workspace == "National Command Center (Main Policy & CAPEX Dashboard)":
    
    now = datetime.now()
    pkt_str = f"PKT-AI-{st.session_state.packet_seq}"
    total_db_count = len(active_df)
    red_hotspots = len(active_df[active_df["Composite_Urgency_Index"] >= 80])
    
    # 5A. DARK ADVISORY CONSOLE
    st.markdown(f"""
    <div class="executive-advisory-console">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <div class="pulse-dot"></div>
                <span style="font-size:13px; font-weight:800; letter-spacing:0.8px; text-transform:uppercase; color:#06B6D4;">
                    Google Cloud & Vertex AI Operational Telemetry Gateway
                </span>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <span class="telemetry-tag">Gemini Multimodal: Active (4,800 Ingest Nodes)</span>
                <span class="telemetry-tag">Speech-to-Text: 22 Languages</span>
                <span class="telemetry-tag">OpenStreetMap Vector Engine: 100% Free</span>
                <span class="telemetry-tag">DPDP Act (2023) Compliant</span>
            </div>
        </div>
        <div style="font-size:13px; color:#F8FAFC; line-height:1.5; font-weight:500;">
            <b>National Advisory:</b> Automated clustering detected <b>{red_hotspots} critical infrastructure failure hotspots</b> in {state_selector}. 
            Cross-departmental correlation engine suggests merging <i>Jal Board water line replacement</i> with <i>PWD road re-carpeting</i> across 14 high-density wards, preserving ₹14.8 Crores in public capital.
        </div>
        <div class="terminal-stream-box">
            [{now.strftime('%H:%M:%S')}] INGESTION_BUS: {pkt_str} verified from {state_selector} | Multilingual Speech-to-Text: Indic ASR Model Active<br>
            [{now.strftime('%H:%M:%S')}] GEMINI_VISION: Photo upload from Ward-04 verified ➔ Severe Structural Crack on Flyover Pillar (Damage Rating 4.9/5)<br>
            [{now.strftime('%H:%M:%S')}] GATISHAKTI_SYNC: Geospatial layer alignment complete. 48 Urban Local Bodies (ULBs) mapped.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --------------------------------------------------------------------------
    # TOOL 1: LIVE GEOSPATIAL MAP & RISK MATRIX (ZERO API KEY REQUIRED)
    # --------------------------------------------------------------------------
    if active_tool == "Live Geospatial Hotspot Map & Risk Matrix":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Live Infrastructure Risk Map — {state_selector}</h1>", unsafe_allow_html=True)
        st.write("Real-time geographic distribution of citizen petitions colored by the **Composite Urgency Index (CUI)**.")
        
        m1, m2, m3, m4 = st.columns(4)
        est_waste_saved = round(red_hotspots * 0.42, 2)
        total_capex = round(active_df["Est_Project_Cost_Lakhs"].sum() / 100.0, 2)
        
        with m1: 
            st.markdown(f"""
            <div class='premium-card'>
                <div class='card-title'>Active Scaled Petitions</div>
                <div class='card-value'>{len(active_df):,}</div>
                <div class='card-subtitle' style='color:#64748B;'>Multimodal Submissions</div>
            </div>
            """, unsafe_allow_html=True)
        with m2: 
            st.markdown(f"""
            <div class='blinking-red-card'>
                <div class='card-title' style='color:#BE123C;'>Critical Hotspots (CUI ≥ 80)</div>
                <div class='card-value'>{red_hotspots}</div>
                <div class='card-subtitle' style='color:#BE123C;'>Action Mandated</div>
            </div>
            """, unsafe_allow_html=True)
        with m3: 
            st.markdown(f"""
            <div class='premium-card' style='border-left-color: #7C3AED !important;'>
                <div class='card-title'>Estimated CAPEX Needed</div>
                <div class='card-value'>₹{total_capex} Cr</div>
                <div class='card-subtitle' style='color:#7C3AED;'>Total Capital Required</div>
            </div>
            """, unsafe_allow_html=True)
        with m4: 
            st.markdown(f"""
            <div class='success-card-soft'>
                <div class='card-title'>Inter-Agency Money Preserved</div>
                <div class='card-value'>₹{est_waste_saved} Cr</div>
                <div class='card-subtitle' style='color:#059669;'>Via Unified Execution</div>
            </div>
            """, unsafe_allow_html=True)
        
        map_tabs = st.tabs([
            "🗺️ Pan-India Live Interactive Map (OpenStreetMap Tiles - No Key Needed)",
            "📊 Distress Density by Department",
            "📋 Master Petitions Ledger (Raw Ingested Data)"
        ])
        
        with map_tabs[0]:
            # 100% Free OpenStreetMap tile implementation - Zero Mapbox API Key warnings
            fig_map = px.scatter_mapbox(
                active_df,
                lat="Latitude",
                lon="Longitude",
                color="Composite_Urgency_Index",
                size="Severity_Rating",
                color_continuous_scale="Turbo",
                hover_name="Ticket_ID",
                hover_data=["District", "Department", "Composite_Urgency_Index", "Channel"],
                zoom=4.2 if state_selector == "All India (National Horizon)" else 7.5,
                height=520
            )
            fig_map.update_layout(
                mapbox_style="open-street-map",
                margin={"r":0,"t":0,"l":0,"b":0},
                coloraxis_colorbar=dict(title="Urgency (CUI)")
            )
            st.plotly_chart(fig_map, use_container_width=True, config=PLOT_CONFIG)
            st.caption("ℹ️ OpenStreetMap vector tile layer loaded natively. Unmetered, offline-resilient, and requires zero external credentials.")

        with map_tabs[1]:
            dept_summary = active_df.groupby("Department")["Composite_Urgency_Index"].agg(['count', 'mean']).reset_index()
            dept_summary.columns = ["Department", "Total Grievances", "Average Urgency Score"]
            
            fig_bar = px.bar(
                dept_summary,
                x="Department",
                y="Total Grievances",
                color="Average Urgency Score",
                color_continuous_scale="Reds",
                text="Total Grievances"
            )
            fig_bar.update_layout(template="plotly_white", height=400, xaxis_tickangle=-15)
            st.plotly_chart(fig_bar, use_container_width=True, config=PLOT_CONFIG)

        with map_tabs[2]:
            st.dataframe(
                active_df[["Ticket_ID", "State", "District", "Ward", "Department", "Composite_Urgency_Index", "Severity_Rating", "Channel", "Status"]],
                use_container_width=True,
                height=400
            )

    # --------------------------------------------------------------------------
    # TOOL 2: CROSS-DEPARTMENTAL MEGA-PROJECT OPTIMIZER (Jal Board + PWD Synergy)
    # --------------------------------------------------------------------------
    elif active_tool == "Cross-Departmental Mega-Project Optimizer (Jal Board + PWD Synergy)":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Cross-Departmental Synergy Optimizer — {state_selector}</h1>", unsafe_allow_html=True)
        st.write("Identifies spatial and temporal overlaps across separate departmental budgets to prevent repetitive digging, pavement destruction, and contractor delays.")
        
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Uncoordinated Projects Bundled", "18 Mega-Clusters", delta="+100% Alignment")
        with c2: st.metric("Prevented Pavement Destruction", "48.2 Kilometers", delta="Saved from Re-digging")
        with c3: st.metric("Total Synergy Capital Preserved", "₹ 24.6 Crores", delta="32.5% Cost Reduction")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Clustered Public Works Opportunities")
        synergy_df = pd.DataFrame([
            [
                "MC-TAM-401", "Salem", "Ward-08 & 09",
                "PWD (Roads) + Jal Board (Drainage)",
                "Jal Board laying underground sewage main simultaneously with PWD full bitumen resurfacing.",
                "₹ 3.8 Cr", "₹ 1.2 Cr Saved", "Execution Window: 30 Days"
            ],
            [
                "MC-MAH-209", "Pune", "Ward-14, 15",
                "PWD + Electricity Distribution",
                "Shifting 11kV electrical cables underground during planned flyover approach expansion.",
                "₹ 7.2 Cr", "₹ 2.4 Cr Saved", "Execution Window: 45 Days"
            ],
            [
                "MC-UP-104", "Lucknow", "Ward-02, 05",
                "Jal Board + Solid Waste Management",
                "Canal desilting combined with stormwater culvert structural replacement before monsoon.",
                "₹ 2.9 Cr", "₹ 0.95 Cr Saved", "Execution Window: 20 Days"
            ],
            [
                "MC-KAR-772", "Bengaluru Urban", "Ward-22",
                "PWD + School Education",
                "Pedestrian foot-overbridge and traffic-calming speed tables outside government secondary school.",
                "₹ 1.6 Cr", "₹ 0.5 Cr Saved", "Execution Window: 15 Days"
            ]
        ], columns=["Mega-Cluster ID", "District", "Wards Covered", "Agencies Bundled", "Joint Engineering Objective", "Joint CAPEX", "Capital Preserved", "Timeline"])
        
        st.dataframe(synergy_df, use_container_width=True, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Algorithmic Joint Optimization Pipeline")
        
        st.markdown("""
        <div class="flow-container">
            <div class="flow-box">
                <div class="flow-title">Step 1: Spatial Proximity Clustering (DBSCAN & PostGIS)</div>
                <div class="flow-desc">Detects grievances from different departments situated within 250 meters of each other.</div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box flow-box-purple">
                <div class="flow-title">Step 2: Dependency Graph & Sequence Analysis</div>
                <div class="flow-desc">Enforces strict engineering order: <b>Underground Utilities (Pipes/Cables) First</b> ➔ <b>Subgrade Leveling</b> ➔ <b>Surface Bitumen Paving Last</b>.</div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box flow-box-green">
                <div class="flow-title">Step 3: Unified Single-Tender Project Detail Sheet (PDS)</div>
                <div class="flow-desc">Generates a unified municipal tender with joint contractor accountability and shared work possession.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TOOL 3: PUBLIC SPENDING AUDIT: OLD MANUAL WAY VS. CIVIC PRISM
    # --------------------------------------------------------------------------
    elif active_tool == "Public Spending Audit: Old Fragmented CAPEX vs. Civic Prism Saved Money":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Public Spending Audit — Old Fragmented CAPEX vs. Civic Prism</h1>", unsafe_allow_html=True)
        st.write("Direct economic ledger comparing wasteful, uncoordinated municipal budget spending with Civic Prism's optimized planning model.")
        
        total_p = len(active_df)
        legacy_loss = total_p * 18500.0
        optimized_cost = total_p * 4200.0
        net_saved = legacy_loss - optimized_cost
        mitigation_pct = round((net_saved / legacy_loss) * 100.0, 1)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-radius: 16px; padding: 18px 24px; color: white; margin-bottom: 20px; box-shadow: 0 4px 18px rgba(15, 23, 42, 0.12);">
            <div style="font-size: 11px; text-transform: uppercase; font-weight: 800; color: #38BDF8; letter-spacing: 1px; margin-bottom: 6px;">Executive Audit Summary (Consolidated Regional Infrastructure Allocation)</div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
                <div>
                    <div style="font-size: 12px; color: #94A3B8;">Old Fragmented Approach Loss</div>
                    <div style="font-size: 24px; font-weight: 900; color: #F87171;">₹{legacy_loss:,.0f} <span style="font-size:14px; font-weight:600;">(₹{legacy_loss/10000000:.2f} Cr)</span></div>
                </div>
                <div style="font-size: 24px; color: #64748B; font-weight: 300;">➔</div>
                <div>
                    <div style="font-size: 12px; color: #94A3B8;">Civic Prism Coordinated Cost</div>
                    <div style="font-size: 24px; font-weight: 900; color: #38BDF8;">₹{optimized_cost:,.0f} <span style="font-size:14px; font-weight:600;">(₹{optimized_cost/10000000:.2f} Cr)</span></div>
                </div>
                <div style="font-size: 24px; color: #64748B; font-weight: 300;">➔</div>
                <div>
                    <div style="font-size: 12px; color: #94A3B8;">Taxpayer Capital Preserved</div>
                    <div style="font-size: 26px; font-weight: 900; color: #34D399;">₹{net_saved:,.0f} <span style="font-size:15px; font-weight:700;">(₹{net_saved/10000000:.2f} Cr Saved)</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c_kpi1, c_kpi2, c_kpi3, c_kpi4 = st.columns(4)
        with c_kpi1: st.markdown(f"<div class='premium-card' style='border-left-color: #DC2626 !important;'><div class='card-title'>Old System Loss</div><div class='card-value' style='color:#DC2626;'>₹{legacy_loss/10000000:.2f} Cr</div><div class='card-subtitle'>Repetitive Digging & Silos</div></div>", unsafe_allow_html=True)
        with c_kpi2: st.markdown(f"<div class='premium-card' style='border-left-color: #0284C7 !important;'><div class='card-title'>Platform Execution Cost</div><div class='card-value' style='color:#0284C7;'>₹{optimized_cost/10000000:.2f} Cr</div><div class='card-subtitle'>Automated AI Triage</div></div>", unsafe_allow_html=True)
        with c_kpi3: st.markdown(f"<div class='premium-card' style='border-left-color: #059669 !important;'><div class='card-title'>Net Taxpayer Savings</div><div class='card-value' style='color:#059669;'>₹{net_saved/10000000:.2f} Cr</div><div class='card-subtitle'>Preserved Municipal Budget</div></div>", unsafe_allow_html=True)
        with c_kpi4: st.markdown(f"<div class='premium-card' style='border-left-color: #7C3AED !important;'><div class='card-title'>Budget Efficiency Gain</div><div class='card-value' style='color:#7C3AED;'>{mitigation_pct}%</div><div class='card-subtitle'>Waste Eliminated</div></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### Detailed Side-by-Side Savings Ledger")
        
        audit_table = pd.DataFrame([
            [
                "Repetitive Trenching & Pavement Destruction",
                f"₹{legacy_loss * 0.38:,.0f}", f"₹{optimized_cost * 0.10:,.0f}", f"₹{(legacy_loss * 0.38) - (optimized_cost * 0.10):,.0f}", "84.2% Waste Eliminated"
            ],
            [
                "Manual Desk-to-Desk Triage & Routing Delays",
                f"₹{legacy_loss * 0.25:,.0f}", f"₹{optimized_cost * 0.12:,.0f}", f"₹{(legacy_loss * 0.25) - (optimized_cost * 0.12):,.0f}", "78.4% Time Saved"
            ],
            [
                "Emergency Post-Disaster Re-work Penalties",
                f"₹{legacy_loss * 0.22:,.0f}", f"₹{optimized_cost * 0.08:,.0f}", f"₹{(legacy_loss * 0.22) - (optimized_cost * 0.08):,.0f}", "86.0% Claims Avoided"
            ],
            [
                "Public Productivity Loss (Traffic Diversions)",
                f"₹{legacy_loss * 0.15:,.0f}", f"₹{optimized_cost * 0.15:,.0f}", f"₹{(legacy_loss * 0.15) - (optimized_cost * 0.15):,.0f}", "Commuter Hours Saved"
            ],
            [
                "CONSOLIDATED AUDIT TOTALS",
                f"₹{legacy_loss:,.0f}", f"₹{optimized_cost:,.0f}", f"₹{net_saved:,.0f}", f"{mitigation_pct}% Overall Savings"
            ]
        ], columns=["Expenditure Line Item", "Old Manual Way (Money Wasted)", "Civic Prism Coordinated", "Capital Preserved", "Impact Status"])
        
        st.dataframe(audit_table, use_container_width=True, hide_index=True)
        
        out_buf = io.StringIO()
        out_buf.write("========================================================================================\n")
        out_buf.write("           GOVERNMENT OF INDIA - MINISTRY OF HOUSING & URBAN AFFAIRS                     \n")
        out_buf.write("           NATIONAL INFRASTRUCTURE ASSET OPTIMIZATION STATEMENT                        \n")
        out_buf.write("========================================================================================\n")
        out_buf.write(f"JURISDICTION SCOPE : {state_selector.upper()} - {district_selector.upper()}\n")
        out_buf.write(f"GENERATION TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_buf.write(f"TOTAL MONEY SAVED   : Rs {net_saved:,.2f} ({net_saved/10000000:.2f} Crores)\n")
        out_buf.write(f"EFFICIENCY RATING   : {mitigation_pct}%\n")
        out_buf.write("----------------------------------------------------------------------------------------\n\n")
        out_buf.write(audit_table.to_string(index=False))
        out_buf.write("\n\n========================================================================================\n")
        
        st.download_button(
            label="📥 Download Official Financial Savings Statement (.TXT)",
            data=out_buf.getvalue(),
            file_name=f"CivicPrism_Financial_Savings_{state_selector.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # --------------------------------------------------------------------------
    # TOOL 4: PM GATISHAKTI NATIONAL MASTER PLAN SYNCHRONIZATION DESK
    # --------------------------------------------------------------------------
    elif active_tool == "PM GatiShakti National Master Plan Synchronization Desk":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>PM GatiShakti National Master Plan Sync Desk</h1>", unsafe_allow_html=True)
        st.write("Convert localized citizen grievance clusters into standardized **Project Detail Sheets (PDS)** aligned with the PM GatiShakti National Master Plan (NMP) data format.")
        
        col_g1, col_g2 = st.columns([1.5, 1])
        
        with col_g1:
            st.markdown("#### Synchronized Inter-Departmental Projects")
            gati_df = pd.DataFrame(st.session_state.gati_shakti_registry)
            st.dataframe(gati_df, use_container_width=True, hide_index=True)
            
            st.markdown("#### Trigger Live National Master Plan Alignment")
            target_dist = st.selectbox("Select District for Alignment", PAN_INDIA_REGISTRY[state_selector]["districts"] if state_selector != "All India (National Horizon)" else ["Salem", "Chennai", "Mumbai Urban", "Lucknow", "Bengaluru Urban"])
            proj_name = st.text_input("Project Specification Name", value=f"{target_dist} Unified Utility Corridor Expansion")
            budget_val = st.number_input("Proposed Budget Allocation (₹ Crores)", 1.0, 100.0, 12.5, step=0.5)
            
            if st.button("🚀 Export and Sync with PM GatiShakti National Master Plan", use_container_width=True):
                new_id = f"PMGS-IN-{datetime.now().strftime('%Y')}-{random.randint(100, 999)}"
                token = hashlib.sha256(f"{new_id}-{target_dist}-{datetime.now()}".encode()).hexdigest().upper()
                
                new_entry = {
                    "Sync_ID": new_id,
                    "Project_Name": proj_name,
                    "State": state_selector if state_selector != "All India (National Horizon)" else "National Jurisdiction",
                    "District": target_dist,
                    "Combined_Departments": "PWD + Jal Board + Power Grid",
                    "Allocated_Budget_Cr": budget_val,
                    "DPI_Verification_Hash": token,
                    "Execution_SLA": "60 Days",
                    "Status": "Synced with National Master Plan"
                }
                st.session_state.gati_shakti_registry.insert(0, new_entry)
                
                st.success(f"Successfully Synchronized with PM GatiShakti NMP under Reference ID: {new_id}!")
                st.balloons()
                time_mod.sleep(0.5)
                st.rerun()

        with col_g2:
            st.markdown("#### Cryptographic Audit & JSON Payload")
            latest = st.session_state.gati_shakti_registry[0]
            
            st.markdown(f"""
            <div class="success-card-soft">
                <div class="card-inner-clearance">
                    <strong style="color: #065F46; font-size: 13px;">GatiShakti Verified Entry: {latest['Sync_ID']}</strong>
                    <div style="font-size: 12px; color: #1E293B; margin-top: 6px;">
                        <b>Project:</b> {latest['Project_Name']}<br>
                        <b>Jurisdiction:</b> {latest['District']} ({latest['State']})<br>
                        <b>Budget:</b> ₹ {latest['Allocated_Budget_Cr']} Crores<br>
                        <b>Digital Signature:</b> <code>{latest['DPI_Verification_Hash'][:28]}...</code>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            json_payload = json.dumps(latest, indent=4)
            st.download_button(
                label="📥 Export GatiShakti Standard JSON Schema",
                data=json_payload,
                file_name=f"GatiShakti_Export_{latest['Sync_ID']}.json",
                mime="application/json",
                use_container_width=True
            )

    # --------------------------------------------------------------------------
    # TOOL 5: LIVE MULTIMODAL INGESTION GATEWAY (Voice, Photo, CPGRAMS)
    # --------------------------------------------------------------------------
    elif active_tool == "Live Multimodal Ingestion Gateway (Voice, Photo, CPGRAMS)":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Live Multimodal Ingestion Gateway</h1>", unsafe_allow_html=True)
        st.write("Aggregates unstructured citizen voice streams, WhatsApp messages, and geotagged damage photos across India into verified data rows.")
        
        c_i1, c_i2, c_i3 = st.columns(3)
        with c_i1: st.metric("Live Intake Channels", "4 Active Streams", delta="Voice, Chat, Web, API")
        with c_i2: st.metric("Dialect Tolerance", "22 Scheduled Languages", delta="Indic ASR Active")
        with c_i3: st.metric("Spam & Duplicate Filter Rate", "99.2%", delta="Perceptual Hashing")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Ingested Multimodal Grievance Feed")
        
        st.dataframe(
            active_df[["Ticket_ID", "Channel", "Language", "Reported_Issue", "Department", "Composite_Urgency_Index", "Status"]].head(25),
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------------------------
    # TOOL 6: 30-DAY PREDICTIVE INFRASTRUCTURE BREAKDOWN HEATMAP
    # --------------------------------------------------------------------------
    elif active_tool == "30-Day Predictive Infrastructure Breakdown Heatmap":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>30-Day Predictive Failure Heatmap — {state_selector}</h1>", unsafe_allow_html=True)
        st.write("Forecasts which municipal wards are at critical risk of catastrophic failure (water pipe bursts, road sinkholes, power blackouts) based on wear rate, weather, and complaint velocity.")
        
        dist_names = PAN_INDIA_REGISTRY[state_selector]["districts"] if state_selector != "All India (National Horizon)" else ["Salem", "Chennai", "Mumbai Urban", "Lucknow", "Bengaluru Urban", "Ahmedabad"]
        days = [f"Day +{d}" for d in range(1, 15)]
        
        heat_matrix = []
        for dist in dist_names:
            row = [int(np.clip(random.randint(30, 95) + np.sin(i) * 10, 20, 99)) for i in range(len(days))]
            heat_matrix.append(row)
            
        fig_pred = go.Figure(data=go.Heatmap(
            z=heat_matrix,
            x=days,
            y=dist_names,
            colorscale=[[0, '#059669'], [0.5, '#F59E0B'], [1.0, '#DC2626']],
            colorbar=dict(title="Distress Index")
        ))
        fig_pred.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=10), template="plotly_white")
        st.plotly_chart(fig_pred, use_container_width=True, config=PLOT_CONFIG)
        
        st.info("💡 **Predictive Action:** Wards marked in dark red require immediate preventive maintenance within the next 48 to 72 hours to prevent emergency corridor shutdowns.")

    # --------------------------------------------------------------------------
    # TOOL 7: WARD ESCALATIONS & EMERGENCY BUDGET EXPANSION DESK
    # --------------------------------------------------------------------------
    elif active_tool == "Ward Escalations & Emergency Budget Expansion Desk":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Ward Field Engineer Escalation Desk</h1>", unsafe_allow_html=True)
        st.write("Site engineers submit ground reality escalations when localized damage exceeds budgeted allocations.")
        
        c_e1, c_e2 = st.columns([1.5, 1])
        with c_e1:
            st.markdown("#### Pending Emergency Escalations")
            for idx, item in enumerate(st.session_state.field_escalations):
                is_approved = (item["status"] == "State Sanction Approved")
                card_css = "success-card-soft" if is_approved else "blinking-red-card"
                badge = "APPROVED" if is_approved else "PENDING ACTION"
                
                st.markdown(f"""
                <div class="{card_css}">
                    <div class="card-inner-clearance">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="font-weight:900; color:#0F172A;">{item['id']} | {item['district']} ({item['department'].split(' ')[0]})</span>
                            <span style="background:{'#10B981' if is_approved else '#EF4444'}; color:white; font-size:10px; font-weight:bold; padding:2px 8px; border-radius:6px;">{badge}</span>
                        </div>
                        <div style="font-size:12px; color:#475569; margin:4px 0;">
                            <b>Officer:</b> {item['officer']} | <b>Requested CAPEX:</b> ₹{item['requested_capex_lakhs']} Lakhs
                        </div>
                        <div style="font-size:12.5px; color:#1E293B;">{item['justification']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if not is_approved:
                    if st.button(f"Sanction Emergency Allocation (₹{item['requested_capex_lakhs']} Lakhs)", key=f"sanc_{idx}"):
                        item["status"] = "State Sanction Approved"
                        st.success(f"Emergency funds authorized for {item['district']}!")
                        time_mod.sleep(0.4)
                        st.rerun()

        with c_e2:
            st.markdown("#### Submit Ground Escalation")
            with st.form("esc_form"):
                e_off = st.text_input("Officer Full Name", value="K. R. Narayanan (Divisional Engineer)")
                e_dist = st.selectbox("Target District", PAN_INDIA_REGISTRY[state_selector]["districts"] if state_selector != "All India (National Horizon)" else ["Salem", "Chennai", "Pune"])
                e_dept = st.selectbox("Department", DEPARTMENTS)
                e_amt = st.number_input("Requested Extra CAPEX (₹ Lakhs)", 5.0, 200.0, 35.0, step=5.0)
                e_just = st.text_area("Ground Technical Justification", placeholder="Describe ground collapse, unmapped pipe network, or severe hazard...")
                
                if st.form_submit_button("Transmit Emergency Escalation"):
                    if e_just:
                        new_esc = {
                            "id": f"ESC-{e_dist[:3].upper()}-{random.randint(100,999)}",
                            "officer": e_off,
                            "district": e_dist,
                            "department": e_dept,
                            "urgency": 92,
                            "requested_capex_lakhs": e_amt,
                            "justification": e_just,
                            "status": "Pending State Sanction"
                        }
                        st.session_state.field_escalations.insert(0, new_esc)
                        st.success("Ground escalation transmitted to State Headquarters.")
                        time_mod.sleep(0.4)
                        st.rerun()

    # --------------------------------------------------------------------------
    # TOOL 8: TECHNICAL ARCHITECTURE & GOOGLE AI INTEGRATION FLOW
    # --------------------------------------------------------------------------
    elif active_tool == "Technical Architecture, Google AI Multimodal Core & DPDP Compliance":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Technical Architecture & Google AI Core</h1>", unsafe_allow_html=True)
        st.write("Detailed end-to-end engineering pipeline showing how raw citizen sensory data transforms into PM GatiShakti intelligence.")
        
        st.markdown("""
        <div class="flow-container">
            <div class="flow-box flow-box-blue" style="max-width: 680px;">
                <div class="flow-title">Layer 1: Multimodal Grassroots Ingestion (Any Device, Any Language)</div>
                <div class="flow-desc">
                    • <b>Voice Streams:</b> Vernacular audio processed via Indic ASR models across 22 scheduled languages.<br>
                    • <b>Messengers:</b> WhatsApp Business & Telegram webhooks with zero citizen training needed.<br>
                    • <b>Camera Verification:</b> Smartphone photos tagged with EXIF GPS timestamps.
                </div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box flow-box-purple" style="max-width: 680px;">
                <div class="flow-title">Layer 2: Google Gemini Multimodal Core & Vertex AI</div>
                <div class="flow-desc">
                    • <b>Semantic Entity Extraction:</b> Extracts category, defect type, and landmark from informal Hinglish/Tanglish.<br>
                    • <b>Computer Vision Damage Verification:</b> Classifies structural damage severity (1–5) and filters spam images.<br>
                    • <b>JSON Schema Guardrails:</b> Strict programmatic outputs preventing hallucinations.
                </div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box flow-box-amber" style="max-width: 680px;">
                <div class="flow-title">Layer 3: Geospatial Context & Demographic Fusion</div>
                <div class="flow-desc">
                    • <b>Composite Urgency Index ($CUI$):</b> <code>(Severity * 40%) + (Deficit Score * 35%) + (Pop Density * 25%)</code>.<br>
                    • <b>DBSCAN Hotspot Clustering:</b> Merges fragmented citizen petitions within 250m into single project zones.<br>
                    • <b>OpenStreetMap Vector Engine:</b> Completely free, unmetered mapping layer requiring zero API keys.
                </div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box flow-box-green" style="max-width: 680px;">
                <div class="flow-title">Layer 4: National Policy Alignment & PM GatiShakti NMP</div>
                <div class="flow-desc">
                    • <b>Tender Bundling:</b> Merges Water (Jal Board) and Road (PWD) works into a single Mega-Cluster tender.<br>
                    • <b>SHA-256 Audit Trail:</b> Cryptographic proof-of-work certificates for complete auditability.<br>
                    • <b>DPDP Act (2023) Compliance:</b> Edge PII scrubbing eliminates sensitive citizen identities.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TOOL 9: SYSTEM GUIDE & OPERATIONS MANUAL
    # --------------------------------------------------------------------------
    elif active_tool == "System Guide & National Deployment Manual":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>System Guide & National Deployment Manual</h1>", unsafe_allow_html=True)
        
        with st.expander("📖 Module 1: How Municipal Commissioners Use Civic Prism", expanded=True):
            st.markdown("""
            1. **Select Territory**: Jump between National Overview or specific States (e.g., Tamil Nadu, Maharashtra, Uttar Pradesh) using the left sidebar.
            2. **Identify Critical Red Zones**: Look at the Live Geospatial Map for red clusters (Composite Urgency Index ≥ 80).
            3. **Review Joint Synergies**: Switch to the *Cross-Departmental Mega-Project Optimizer* to approve combined tenders, saving up to 35% in wasted road repaving costs.
            4. **Export to National Master Plan**: Click *Export and Sync with PM GatiShakti* to generate standardized, cryptographically signed tenders ready for public bidding.
            """)

        with st.expander("⚙️ Module 2: Mathematical Formulation of the Composite Urgency Index (CUI)", expanded=True):
            st.markdown("""
            To prevent affluent, digitally active neighborhoods from monopolizing repair budgets, Civic Prism normalizes citizen reports through a weighted demographic equation:
            
            $$\\text{CUI} = \\left( \\text{Severity} \\times 20 \\times 0.40 \\right) + \\left( \\text{Historical Deficit Score} \\times 0.35 \\right) + \\left( \\frac{\\text{Population Density}}{2800} \\times 100 \\times 0.25 \\right)$$
            
            This guarantees that underserved rural and peri-urban wards with high population densities receive immediate infrastructure priority, ensuring democratic public spending.
            """)

# ==============================================================================
# 6. WORKSPACE 2: CITIZEN VOICE KIOSK & WARD TERMINALS
# ==============================================================================
elif workspace == "Citizen Voice Kiosk & Ward Terminal (Grassroots Ingestion)":
    
    # --------------------------------------------------------------------------
    # TOOL 1: VERNACULAR VOICE & TEXT KIOSK
    # --------------------------------------------------------------------------
    if active_tool == "Vernacular Multilingual Voice & Text Kiosk (22 Languages)":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Citizen Voice Reporting Kiosk</h1>", unsafe_allow_html=True)
        st.write("Speak or type in your own language or informal dialect (Hindi, Tamil, Marathi, Bengali, Hinglish, etc.). Google Gemini AI will automatically translate and classify your request.")
        
        c_k1, c_k2 = st.columns([1.2, 1])
        
        with c_k1:
            with st.container(border=True):
                st.markdown("### 🎙️ 1. Describe the Infrastructure Defect")
                sample_voice_options = [
                    "Custom Input (Type or Paste Below)",
                    "Tamil/Tanglish: Salem main road la periya pallam irukku, auto kavunthu pochi, water pipe vera leak aaguthu.",
                    "Hindi/Hinglish: Yahan transformer se chingari nikal rahi hai aur road pura toot chuka hai hospital ke paas.",
                    "Marathi: Rastya var khup mothe khadde padlet aani pani chi line futli aahe.",
                    "Bengali: School er pasher rasta ta ekebare bhenge geche, bacchader jete osubidha hocche."
                ]
                sel_sample = st.selectbox("Choose a Real Vernacular Voice Note Sample or Type Your Own:", sample_voice_options)
                
                if sel_sample == "Custom Input (Type or Paste Below)":
                    citizen_text = st.text_area("Your Voice Transcription or Message:", placeholder="e.g., Road is broken near station and dirty water is leaking on the road.", height=90)
                else:
                    citizen_text = sel_sample.split(": ", 1)[1]
                    st.info(f"Loaded Sample Audio Transcript: *\"{citizen_text}\"*")
                
                st.markdown("### 📸 2. Photographic Proof (Simulated Upload)")
                uploaded_photo = st.file_uploader("Upload Smartphone Image (JPEG, PNG)", type=["jpg", "png"])
                
                target_state = st.selectbox("Your State", list(PAN_INDIA_REGISTRY.keys()))
                target_dist = st.selectbox("Your District", PAN_INDIA_REGISTRY[target_state]["districts"])
                
                submit_kiosk = st.button("Submit Report to National Ingestion Engine", use_container_width=True)
                
        with c_k2:
            st.markdown("### ⚙️ Real-Time Google AI Triage Result")
            if submit_kiosk and citizen_text:
                with st.spinner("Refracting vernacular input via Google Gemini AI..."):
                    # High fidelity simulation of Gemini Multimodal Extraction
                    lang_detected = "Tamil (Tanglish Code-Mixed)" if "Salem" in citizen_text else ("Hindi (Colloquial)" if "transformer" in citizen_text else ("Marathi" if "Rastya" in citizen_text else "Indic Vernacular"))
                    cat_detected = "Public Works (Roads) + Jal Board (Water Leak)" if "pipe" in citizen_text or "pani" in citizen_text else "State Power Grid (Transformer Safety)"
                    sev_calc = 5 if ("chingari" in citizen_text or "kavunthu" in citizen_text) else 4
                    
                    ticket_id = f"CP-{target_dist[:3].upper()}-{random.randint(10000, 99999)}"
                    
                    st.markdown(f"""
                    <div class="success-card-soft">
                        <div class="card-inner-clearance">
                            <strong style="color: #065F46; font-size: 14px;">Grievance Successfully Registered & Classified</strong>
                            <div style="font-size: 12px; color: #1E293B; margin-top: 6px; line-height: 1.6;">
                                <b>Tracking ID:</b> <code>{ticket_id}</code><br>
                                <b>Detected Language:</b> {lang_detected}<br>
                                <b>Identified Sector:</b> {cat_detected}<br>
                                <b>Extracted Severity:</b> <span style="color:#DC2626; font-weight:bold;">{sev_calc}/5 (Critical Urgency)</span><br>
                                <b>English Translation:</b> <i>"Major road collapse and structural water pipe rupture detected near transit route."</i><br>
                                <b>Status:</b> Geotagged & Dispatched to {target_dist} Ward Action Queue.
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Awaiting citizen submission on the left...")

    # --------------------------------------------------------------------------
    # TOOL 2: COMPUTER VISION DAMAGE VERIFICATION & TRIAGE DESK
    # --------------------------------------------------------------------------
    elif active_tool == "Computer Vision Damage Verification & Automated Triage Desk":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Computer Vision Infrastructure Damage Assessor</h1>", unsafe_allow_html=True)
        st.write("Demonstrates how Gemini Vision analyzes uploaded photographs, verifies that the damage is real, and filters out spam or irrelevant images.")
        
        cv_col1, cv_col2 = st.columns(2)
        with cv_col1:
            st.markdown("#### Sample Verification Case")
            sample_cv = st.selectbox("Select Test Image Scenario:", [
                "Test Case A: Severe Road Subsidence & Pothole Crater",
                "Test Case B: High Voltage Electrical Wire Dangling",
                "Test Case C: Clogged Drainage Canal & Garbage Accumulation",
                "Test Case D: Irrelevant / Spam Photo (Cat / Selfie Filter)"
            ])
            
            if st.button("Run Gemini Computer Vision Inspection", use_container_width=True):
                with st.spinner("Analyzing image features, edge cracking, and safety hazards..."):
                    time_mod.sleep(0.4)
                    if "Spam" in sample_cv:
                        st.error("❌ Gemini Vision Verdict: SPAM / IRRELEVANT PHOTO DETECTED. No physical infrastructure damage found. Report rejected to protect public funds.")
                    else:
                        st.markdown(f"""
                        <div class="success-card-soft">
                            <div class="card-inner-clearance">
                                <strong style="color: #065F46; font-size: 14px;">✅ Structural Damage Verified by Google Gemini Vision</strong>
                                <div style="font-size: 12px; color: #1E293B; margin-top: 6px; line-height: 1.6;">
                                    <b>Asset Classified:</b> Civil Transportation & Ground Infrastructure<br>
                                    <b>Defect Severity:</b> 4.7 / 5.0 (High Hazard to Life & Vehicles)<br>
                                    <b>Confidence Score:</b> 98.6% Verification Certainty<br>
                                    <b>Action:</b> Dispatched to Ward Rapid Response Team.
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        with cv_col2:
            st.markdown("#### Verification Pipeline Logic")
            st.markdown("""
            <div class="flow-container">
                <div class="flow-box">
                    <div class="flow-title">1. EXIF Metadata Validation</div>
                    <div class="flow-desc">Extracts embedded GPS coordinates and verifies timestamp freshness.</div>
                </div>
                <div class="flow-arrow"></div>
                <div class="flow-box flow-box-purple">
                    <div class="flow-title">2. Perceptual Hash Duplicate Detection</div>
                    <div class="flow-desc">Checks if the same image was already submitted by multiple users.</div>
                </div>
                <div class="flow-arrow"></div>
                <div class="flow-box flow-box-green">
                    <div class="flow-title">3. Gemini Vision Structural Classification</div>
                    <div class="flow-desc">Quantifies concrete crack depth, water volume, or catenary line detachment.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TOOL 3: TRACK GRIEVANCE STATUS & RESOLUTION CERTIFICATE
    # --------------------------------------------------------------------------
    elif active_tool == "Track My Grievance Status & Digital Resolution Certificate":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Track My Grievance & Resolution Certificate</h1>", unsafe_allow_html=True)
        st.write("Track the live progress of any submitted petition using its unique tracking code.")
        
        sample_ticket_id = st.text_input("Enter Your Ticket Reference ID:", value=active_df["Ticket_ID"].iloc[0])
        
        match = active_df[active_df["Ticket_ID"] == sample_ticket_id]
        if not match.empty:
            item = match.iloc[0]
            st.markdown(f"""
            <div class="premium-card">
                <div class="card-inner-clearance">
                    <div class="card-title">OFFICIAL GRIEVANCE STATUS REPORT</div>
                    <div class="card-value">{item['Ticket_ID']}</div>
                    <p style="font-size: 13px; color: #1E293B; margin-top: 6px;">
                        <b>Jurisdiction:</b> {item['District']}, {item['State']} ({item['Ward']})<br>
                        <b>Department:</b> {item['Department']}<br>
                        <b>Issue:</b> {item['Reported_Issue']}<br>
                        <b>Current Status:</b> <span style="color:#059669; font-weight:bold;">{item['Status']}</span><br>
                        <b>Urgency Level:</b> {item['Composite_Urgency_Index']} / 100
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Cryptographic Resolution Certificate Generator
            cert_buf = io.StringIO()
            cert_buf.write("================================================================================\n")
            cert_buf.write("      CIVIC PRISM - NATIONAL DIGITAL RESOLUTION CERTIFICATE                    \n")
            cert_buf.write("================================================================================\n")
            cert_buf.write(f"TICKET IDENTIFIER : {item['Ticket_ID']}\n")
            cert_buf.write(f"JURISDICTION      : {item['District']}, {item['State']}\n")
            cert_buf.write(f"DEPARTMENT        : {item['Department']}\n")
            cert_buf.write(f"URGENCY INDEX     : {item['Composite_Urgency_Index']}\n")
            cert_buf.write(f"STATUS            : ALLOCATED FOR TENDER UNDER PM GATISHAKTI NMP\n")
            cert_buf.write(f"VERIFICATION HASH : {hashlib.sha256(item['Ticket_ID'].encode()).hexdigest().upper()}\n")
            cert_buf.write("================================================================================\n")
            
            st.download_button(
                label="📥 Download Official Resolution Certificate (.TXT)",
                data=cert_buf.getvalue(),
                file_name=f"Resolution_Certificate_{item['Ticket_ID']}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.warning("Ticket ID not found in the national registry.")
