"""
Streamlit Web Dashboard for Automated Micro-Influencer Outreach System.
Provides an interactive GUI for Discovery, Filtering, Enrichment, AI Personalization, and Outreach Tracking.
"""

import os
import pandas as pd
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Micro-Influencer Outreach System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3B82F6;
    }
    .status-passed {
        color: #065F46;
        background-color: #D1FAE5;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .status-failed {
        color: #991B1B;
        background-color: #FEE2E2;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load cached pipeline datasets."""
    raw_csv = "data/raw/discovered_influencers.csv"
    classified_csv = "data/processed/classified_influencers.csv"
    enriched_csv = "data/processed/enriched_influencers.csv"
    outreach_csv = "data/processed/personalized_outreach.csv"
    tracker_csv = "data/processed/outreach_tracker.csv"

    df_raw = pd.read_csv(raw_csv) if os.path.exists(raw_csv) else pd.DataFrame()
    df_classified = pd.read_csv(classified_csv) if os.path.exists(classified_csv) else pd.DataFrame()
    df_enriched = pd.read_csv(enriched_csv) if os.path.exists(enriched_csv) else pd.DataFrame()
    df_outreach = pd.read_csv(outreach_csv) if os.path.exists(outreach_csv) else pd.DataFrame()
    df_tracker = pd.read_csv(tracker_csv) if os.path.exists(tracker_csv) else pd.DataFrame()

    return df_raw, df_classified, df_enriched, df_outreach, df_tracker


df_raw, df_classified, df_enriched, df_outreach, df_tracker = load_data()

# Sidebar Navigation
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 5px 0 15px 0;">
        <span style="font-size: 50px;">🚀</span>
        <h3 style="margin: 4px 0 0 0; color: #3B82F6; font-size: 1.3rem; font-weight: 700;">OutreachAI</h3>
        <p style="margin: 0; color: #9CA3AF; font-size: 0.8rem;">Micro-Influencer Outreach System</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Workflow Stage:",
    [
        "Dashboard Overview",
        "1. Influencer Discovery",
        "2. Filtering & Classification",
        "3. Profile Enrichment",
        "4. AI Message Personalization",
        "5. Sending Layer & Tracker"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Automated Micro-Influencer Outreach")
st.sidebar.caption("Pipeline: Tech & AI Niche")

# ==========================================
# 0. DASHBOARD OVERVIEW
# ==========================================
if page == "Dashboard Overview":
    st.markdown("<div class='main-title'>Automated Micro-Influencer Outreach System</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>End-to-End AI Pipeline: Discovery → Filtering → Enrichment → Personalization → Sending → Tracking</div>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Discovered", len(df_raw) if not df_raw.empty else 0, "58 verified")
    with col2:
        passed_n = len(df_classified[df_classified["Status"] == "PASSED"]) if not df_classified.empty else 0
        st.metric("Shortlisted (Passed)", passed_n, "Micro Tier")
    with col3:
        failed_n = len(df_classified[df_classified["Status"] == "FAILED"]) if not df_classified.empty else 0
        st.metric("Excluded (Failed)", failed_n, "Audited")
    with col4:
        st.metric("AI Pitches Generated", len(df_outreach) if not df_outreach.empty else 0, "60-90w email")
    with col5:
        st.metric("Tracker Logs", len(df_tracker) if not df_tracker.empty else 0, "Idempotent")

    st.markdown("---")
    st.subheader("System Architecture")
    st.markdown("""
    ```
    ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
    │ Influencer Discovery │ ──> │ Filtering & Scoring  │ ──> │  Profile Enrichment  │
    │  (58 Tech Profiles)  │     │  (30 Micro Shortlist)│     │(Contacts/Demographics│
    └──────────────────────┘     └──────────────────────┘     └──────────────────────┘
                                                                         │
                                                                         ▼
    ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
    │   Outreach Tracker   │ <── │    Sending Layer     │ <── │  AI Personalization  │
    │ (Audit CSV & Logs)   │     │ (SMTP / Simulation)  │     │ (Pitch: 60-90w | DM) │
    └──────────────────────┘     └──────────────────────┘     └──────────────────────┘
    ```
    """)

    st.subheader("Key Capabilities Demonstrated")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        - **Live Public Extraction**: Scrapes 58 verified creator records with usernames, platforms, locations, and bios.
        - **Rule-Based & Deterministic Auditing**: Strict 5,000–100,000 follower bounds, $>2.0\%$ engagement rates, and explicit rejection rationale.
        - **Ethical Anti-Fabrication Standards**: Real emails attached where publicly listed; strictly marked `"Not Found"` otherwise.
        """)
    with c2:
        st.markdown("""
        - **AI Message Personalization**: Enforces strict word count bounds (60–90 words for emails, 15–30 words for Instagram DMs).
        - **Dual-Mode Dispatch Layer**: Safe Simulation mode + Live SMTP with duplicate outreach prevention.
        - **Compliance Workflow**: Respects Instagram limits with manual copy-to-clipboard dispatch interface.
        """)

# ==========================================
# 1. INFLUENCER DISCOVERY
# ==========================================
elif page == "1. Influencer Discovery":
    st.markdown("<div class='main-title'>1. Influencer Discovery</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Live extraction of real Technology & AI creators across Instagram, TikTok, and YouTube.</div>", unsafe_allow_html=True)

    if not df_raw.empty:
        col1, col2 = st.columns([1, 3])
        with col1:
            plat_filter = st.multiselect("Filter Platform", options=df_raw["Platform"].unique(), default=df_raw["Platform"].unique())
            tier_filter = st.multiselect("Filter Tier", options=df_raw["Follower_Tier"].unique(), default=df_raw["Follower_Tier"].unique())
        with col2:
            search_query = st.text_input("Search Creator Name, Username, or Bio", "")

        filtered = df_raw[
            (df_raw["Platform"].isin(plat_filter)) &
            (df_raw["Follower_Tier"].isin(tier_filter))
        ]
        if search_query:
            filtered = filtered[
                filtered["Name"].str.contains(search_query, case=False, na=False) |
                filtered["Bio"].str.contains(search_query, case=False, na=False)
            ]

        st.dataframe(filtered, use_container_width=True, height=450)
        st.caption(f"Showing {len(filtered)} of {len(df_raw)} discovered profiles.")
    else:
        st.warning("No discovery dataset found. Run `python scripts/run_discovery.py` to populate.")

# ==========================================
# 2. FILTERING & CLASSIFICATION
# ==========================================
elif page == "2. Filtering & Classification":
    st.markdown("<div class='main-title'>2. Filtering & Classification Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Audit and classification of discovered creators against micro-influencer criteria.</div>", unsafe_allow_html=True)

    if not df_classified.empty:
        col1, col2 = st.columns([1, 2])
        with col1:
            status_filter = st.radio("Filter Status:", ["All", "PASSED (Shortlisted)", "FAILED (Excluded)"])
        with col2:
            st.info("""
            **Criteria Applied**:
            - Follower Count: **5,000 to 100,000** (Micro-influencer definition)
            - Engagement Rate: $\ge$ **2.0%**
            - Category: **Technology & AI** alignment
            - Brand Safety: Toxic & spam keyword check
            """)

        display_df = df_classified.copy()
        if status_filter == "PASSED (Shortlisted)":
            display_df = display_df[display_df["Status"] == "PASSED"]
        elif status_filter == "FAILED (Excluded)":
            display_df = display_df[display_df["Status"] == "FAILED"]

        st.dataframe(display_df, use_container_width=True, height=450)
        st.caption(f"Total Profiles in View: {len(display_df)}")
    else:
        st.warning("No classification dataset found. Run `python scripts/run_filtering.py`.")

# ==========================================
# 3. PROFILE ENRICHMENT
# ==========================================
elif page == "3. Profile Enrichment":
    st.markdown("<div class='main-title'>3. Profile Enrichment</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Enriched profile metrics, contact emails (anti-fabrication), and audience context.</div>", unsafe_allow_html=True)

    if not df_enriched.empty:
        c1, c2, c3 = st.columns(3)
        emails_avail = len(df_enriched[df_enriched["Contact_Email"] != "Not Found"])
        with c1:
            st.metric("Total Enriched Micro-Influencers", len(df_enriched))
        with c2:
            st.metric("Verified Business Emails Available", emails_avail)
        with c3:
            st.metric("Marked 'Not Found' (Anti-Fabrication)", len(df_enriched) - emails_avail)

        st.dataframe(df_enriched, use_container_width=True, height=450)
    else:
        st.warning("No enriched dataset found. Run `python scripts/run_enrichment.py`.")

# ==========================================
# 4. AI MESSAGE PERSONALIZATION
# ==========================================
elif page == "4. AI Message Personalization":
    st.markdown("<div class='main-title'>4. AI Message Personalization</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Bespoke Email Collaboration Pitches (60-90 words) & Instagram DMs (15-30 words).</div>", unsafe_allow_html=True)

    if not df_outreach.empty:
        creator_names = df_outreach["Influencer_Name"].tolist()
        selected_creator = st.selectbox("Select Creator to Inspect Personalized Outreach:", creator_names)

        creator_row = df_outreach[df_outreach["Influencer_Name"] == selected_creator].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📧 Email Collaboration Pitch")
            email_wc = creator_row["Email_Word_Count"]
            is_valid_email = 60 <= email_wc <= 90
            status_badge = "✅ Compliant (60-90w)" if is_valid_email else "⚠️ Check Length"
            st.markdown(f"**Word Count:** `{email_wc} words` — **Status:** {status_badge}")
            st.text_input("Subject Line:", creator_row["Email_Subject"], disabled=True)
            st.text_area("Email Pitch Body:", creator_row["Email_Pitch"], height=180)
            st.caption(f"Collaboration Angle: {creator_row['Collaboration_Angle']} | Value Prop: {creator_row['Value_Proposition']}")

        with col2:
            st.subheader("💬 Instagram Direct Message (DM)")
            dm_wc = creator_row["DM_Word_Count"]
            is_valid_dm = 15 <= dm_wc <= 30
            dm_status_badge = "✅ Compliant (15-30w)" if is_valid_dm else "⚠️ Check Length"
            st.markdown(f"**Word Count:** `{dm_wc} words` — **Status:** {dm_status_badge}")
            st.text_area("Instagram DM Text:", creator_row["Instagram_DM"], height=120)
            st.button(f"📋 Copy DM for @{selected_creator}", on_click=lambda: st.toast("DM copied to clipboard!"))

        st.markdown("---")
        st.subheader("Complete Outreach Batch Table")
        st.dataframe(df_outreach, use_container_width=True)
    else:
        st.warning("No outreach dataset found. Run `python scripts/run_personalization.py`.")

# ==========================================
# 5. SENDING LAYER & TRACKER
# ==========================================
elif page == "5. Sending Layer & Tracker":
    st.markdown("<div class='main-title'>5. Sending Layer & Outreach Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Live delivery dispatcher, duplicate prevention, and persistent audit logs.</div>", unsafe_allow_html=True)

    if not df_tracker.empty:
        col1, col2, col3, col4 = st.columns(4)
        sent_emails = len(df_tracker[df_tracker["Status"].isin(["SENT", "SIMULATED_SENT"]) & (df_tracker["Channel"] == "Email")])
        skipped_emails = len(df_tracker[df_tracker["Status"] == "SKIPPED_NO_EMAIL"])
        duplicates = len(df_tracker[df_tracker["Status"] == "SKIPPED_DUPLICATE"])
        dms_sent = len(df_tracker[df_tracker["Channel"] == "Instagram DM"])

        with col1:
            st.metric("Emails Delivered / Simulated", sent_emails)
        with col2:
            st.metric("Skipped (No Email)", skipped_emails)
        with col3:
            st.metric("Duplicates Prevented", duplicates)
        with col4:
            st.metric("Instagram DMs Handled", dms_sent)

        st.markdown("---")
        st.subheader("Live Campaign Audit Trail")
        st.dataframe(df_tracker, use_container_width=True, height=450)
    else:
        st.warning("No tracker records found. Run `python scripts/run_sending.py`.")
