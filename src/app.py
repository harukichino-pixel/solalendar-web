import streamlit as st
import json
from tier1_engine import SolalendarTier1
from tier2_engine import SolalendarTier2
from tier3_engine import SolalendarTier3

# ---------------------------------------------------------
# UI Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="Solalendar v4.3 Full", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    .layer-box { padding: 15px; border-radius: 10px; background-color: #1E1E1E; border: 1px solid #333; margin-bottom: 10px; }
    .layer-title { font-size: 0.9em; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    .layer-value { font-size: 1.4em; font-weight: bold; color: #FFF; }
    .highlight { color: #00ADB5; }
    
    .vals-card { background: linear-gradient(135deg, #2C3E50 0%, #000000 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #F39C12; margin-bottom: 10px; }
    .vals-type { font-size: 2em; font-weight: bold; color: #F39C12; }
    
    /* Tier 3 Wisdom Card */
    .wisdom-card {
        background: linear-gradient(135deg, #4b1d52 0%, #0f0c29 100%);
        padding: 30px; border-radius: 15px; border: 1px solid #8e44ad;
        text-align: center; margin-top: 20px;
        box-shadow: 0 0 20px rgba(142, 68, 173, 0.4);
    }
    .wisdom-headline { font-size: 2.5em; font-weight: bold; background: -webkit-linear-gradient(#eee, #999); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; }
    .wisdom-text { font-size: 1.1em; line-height: 1.8; color: #E0E0E0; font-family: serif; font-style: italic; margin-bottom: 30px; }
    .wisdom-advice { background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; color: #00ADB5; font-weight: bold; display: inline-block; }
</style>
""", unsafe_allow_html=True)

st.title("🌌 Solalendar Core v4.3")
st.caption("Integrated Fate Architecture: Tier 1, 2 & 3")

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.header("🔑 System Access")
    api_key = st.text_input("OpenAI API Key", type="password")
    st.divider()
    st.header("📍 Tier 1 Coordinates")
    name = st.text_input("Name", "Haruki")
    c1, c2, c3 = st.columns(3)
    year = c1.number_input("Year", 1900, 2100, 1974)
    month = c2.number_input("Month", 1, 12, 11)
    day = c3.number_input("Day", 1, 31, 4)
    tc1, tc2 = st.columns(2)
    hour = tc1.number_input("Hour", 0, 23, 7)
    minute = tc2.number_input("Minute", 0, 59, 0)
    tier1_btn = st.button("Decode Tier 1 (PSC) 🚀", type="primary")

# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["🧬 Tier 1: Nature", "🔭 Tier 2: Observation", "💎 Tier 3: Wisdom"])

# --- TAB 1: Tier 1 (FIXED: All Layers 0-5 Restored) ---
with tab1:
    if tier1_btn:
        engine = SolalendarTier1(name, year, month, day, hour, minute)
        st.session_state['psc_data'] = engine.analyze()
        
    if 'psc_data' in st.session_state:
        d = st.session_state['psc_data']
        col_l, col_r = st.columns(2)
        
        with col_l:
            # Layer 0 (Restored)
            l0 = d['layer_0_kernel']
            st.markdown(f"<div class='layer-box'><div class='layer-title'>Layer 0: Kernel</div><div class='layer-value'>{l0['jdn']:.2f} JDN</div></div>", unsafe_allow_html=True)

            # Layer 1
            l1 = d['layer_1_bios']
            st.markdown(f"<div class='layer-box'><div class='layer-title'>Layer 1: BIOS</div><div class='layer-value'>LPN <span class='highlight'>{l1['lpn']}</span></div></div>", unsafe_allow_html=True)
            
            # Layer 2
            l2 = d['layer_2_infra']
            pin = l2['cycles'].get('pinnacle', {})
            pin_html = f"<div style='margin-top:5px; border-left:3px solid #00ADB5; padding-left:10px; font-size:0.8em'>{pin.get('current_stage','-')}</div>" if pin else ""
            st.markdown(f"<div class='layer-box'><div class='layer-title'>Layer 2: Infra</div><div class='layer-value'>{l2['cycles']['saturn_cycle']}</div>{pin_html}</div>", unsafe_allow_html=True)
            
        with col_r:
            # Layer 3
            l3 = d['layer_3_env']
            st.markdown(f"<div class='layer-box'><div class='layer-title'>Layer 3: Env</div><div class='layer-value'>{l3['sun_sign']}</div></div>", unsafe_allow_html=True)
            
            # Layer 4 (Restored)
            l4 = d['layer_4_runtime']
            st.markdown(f"<div class='layer-box'><div class='layer-title'>Layer 4: Runtime</div><div class='layer-value'>{l4['eastern_root']}</div><div style='font-size:0.8em; color:#AAA'>Moon: {l4['moon_sign']} / Tone: {l4['texture']}</div></div>", unsafe_allow_html=True)
            
            # Layer 5
            l5 = d['layer_5_skin']
            st.markdown(f"<div class='layer-box'><div class='layer-title'>Layer 5: Skin</div><div class='layer-value'>{l5['ascendant']}</div></div>", unsafe_allow_html=True)

# --- TAB 2: Tier 2 ---
with tab2:
    with st.expander("📝 Assessment Form", expanded=True):
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            q_curiosity = st.slider("知的好奇心", 1, 5, 3)
            q_confidence = st.slider("自信・自己効力感", 1, 5, 3)
            q_action = st.slider("行動力", 1, 5, 3)
            q_ryoshiki = st.checkbox("世間体・常識フィルター", value=True)
            q_driver = st.selectbox("原動力", ["Ideals (理想)", "Achievement (達成)", "Self-Expression (自己表現)"])
            driver_map = {"Ideals (理想)": "Ideals", "Achievement (達成)": "Achievement", "Self-Expression (自己表現)": "Self-Expression"}
        with col_q2:
            q_text = st.text_area("最近の出来事・心情 (200文字程度)", height=200)
            
        if st.button("Run Tier 2 Diagnostics 🧠"):
            t2_engine = SolalendarTier2(api_key)
            anchor = {"curiosity_score": q_curiosity, "confidence_score": q_confidence, "action_score": q_action, "social_norm_flag": q_ryoshiki, "primary_driver": driver_map[q_driver]}
            st.session_state['tier2_result'] = t2_engine.analyze(anchor, q_text)

    if 'tier2_result' in st.session_state:
        res = st.session_state['tier2_result']
        if "error" not in res:
            l6 = res.get("layer_6_behavior", {})
            l7 = res.get("layer_7_motivation", {})
            st.success(f"Diagnosed: {l7.get('vals_type')} / {l6.get('dominant_element')}")
            st.json(res)

# --- TAB 3: Tier 3 ---
with tab3:
    st.header("💎 The Integration")
    st.markdown("Tier 1（先天的運命）と Tier 2（後天的戦略）を統合し、構造的な解決策を提示します。")
    
    # 実行条件のチェック
    ready = ('psc_data' in st.session_state) and ('tier2_result' in st.session_state)
    
    if ready:
        if st.button("Generate Wisdom (Gap Analysis) ✨", type="primary"):
            with st.spinner("Consulting the System Administrator of Fate..."):
                t3_engine = SolalendarTier3(api_key)
                wisdom = t3_engine.integrate(st.session_state['psc_data'], st.session_state['tier2_result'])
                st.session_state['tier3_wisdom'] = wisdom
        
        if 'tier3_wisdom' in st.session_state:
            w = st.session_state['tier3_wisdom']
            if "error" in w:
                st.error(w['error'])
            else:
                gap = w['gap_analysis']
                msg = w['wisdom_message']
                
                # Gap Info
                st.info(f"Analysis: Tier 1 [{gap['tier1_element']}] vs Tier 2 [{gap['tier2_element']}] = {gap['relationship_type']} (Stress: {gap['stress_level']})")
                
                # Wisdom Card
                st.markdown(f"""
                <div class="wisdom-card">
                    <div class="wisdom-headline">{msg['headline']}</div>
                    <div class="wisdom-text">{msg['narrative']}</div>
                    <div class="wisdom-advice">💡 ACT: {msg['actionable_advice']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please complete Tier 1 and Tier 2 analysis first.")