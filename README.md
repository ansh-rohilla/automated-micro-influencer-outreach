# Automated Micro-Influencer Outreach System

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Pipeline-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end automated system that discovers real micro-influencers, filters and classifies them based on predefined brand-fit criteria, enriches their profiles with contact context, generates AI/LLM-personalized collaboration outreach messages, and executes an idempotent sending and tracking workflow.

Built for the **EDXSO AI Engineer Intern – Assignment 1**.

---

## 📑 Project Workflow Overview

The overall system is designed as an end-to-end pipeline following this lifecycle:

```mermaid
flowchart LR
    A[Public Platforms / Marketplace] --> B[Influencer Discovery]
    B --> C[58+ Real Profiles]
    C --> D[Filtering & Classification]
    D --> E[Profile Enrichment]
    E --> F[AI Personalization]
    F --> G[Email Pitch + Instagram DM]
    G --> H[Sending Layer]
    H --> I[Outreach Tracker]
```

| Pipeline Component | Status | Description |
| :--- | :---: | :--- |
| **Influencer Discovery** | **COMPLETED** | Automated discovery of **58 real, verified Technology & AI creators** across Instagram, YouTube, and TikTok. |
| **Filtering & Classification** | **COMPLETED** | Automated criteria filtering (5k–100k followers, >2.0% ER, brand fit) with explicit pass/fail rationale. |
| **Profile Enrichment** | *Upcoming* | Extracting contact emails, content themes, bios, locations, and handles (strictly marking "Not Found" if unavailable). |
| **AI Personalization** | *Upcoming* | AI/LLM generation of email pitches (60–90 words) & Instagram DMs (15–30 words). |
| **Sending Layer** | *Upcoming* | Email sending (SMTP + Safe Simulation Mode) with duplicate prevention and manual Instagram DM workflow. |
| **Outreach Tracker & UI** | *Upcoming* | Real-time campaign tracking, audit logs, and interactive Streamlit review dashboard. |

---

## 🔍 Influencer Discovery (Technology & AI)

### 1. Methodology & Data Sources
- **Source**: Live public creator directories and verified UGC marketplace (Collabstr Tech & AI directory).
- **Target Category**: **Technology & AI** (including AI tools, SaaS, Cloud, Developer tools, and Tech Hardware).
- **Yield**: **58 unique, verified creators** (exceeding the requirement of at least 50).
- **Data Integrity**: **Zero fabricated data**. All names, usernames, follower tiers, locations, and bios reflect real creators.

### 2. Discovered Audience Breakdown
- **Total Discovered**: **58 creators**
- **By Tier**:
  - **Micro-Influencers (5,000 – 100,000 followers)**: `35 creators` *(Target cohort)*
  - **Macro-Influencers (> 100,000 followers)**: `17 creators`
  - **Nano-Influencers (< 5,000 followers)**: `6 creators`
- **By Primary Platform**:
  - **Instagram**: `26`
  - **TikTok**: `22`
  - **YouTube**: `9`
  - **X (Twitter)**: `1`

### 3. Discovered Data Schema
Saved in `data/raw/discovered_influencers.csv` with fields: `ID`, `Name`, `Username`, `Platform`, `Followers`, `Follower_Tier`, `Engagement_Rate`, `Niche`, `Content_Themes`, `Location`, `Profile_URL`, `Headline`, `Bio`, and `Discovery_Source`.

---

## 🎯 Filtering & Classification Engine

The filtering engine automatically evaluates discovered candidates against strict quantitative and qualitative criteria to identify genuine micro-influencers and compute brand-fit suitability.

### 1. Qualification Criteria
| Criterion | Rule / Threshold | Purpose |
| :--- | :--- | :--- |
| **Follower Range** | **5,000 – 100,000** | Strict micro-influencer threshold bounds |
| **Minimum Engagement Rate** | **$\ge$ 2.0%** | Ensures high audience responsiveness and ROI |
| **Allowed Platforms** | Instagram, TikTok, YouTube, X | Validates supported outreach channels |
| **Niche Relevance** | AI, Tech, SaaS, Dev Tools, Cloud, Cybersecurity | Matches target domain alignment |
| **Brand Safety** | Disqualifies spam, casino, adult, or toxic keywords | Enforces brand reputation protection |

### 2. Brand-Fit Scoring Algorithm (0.0 to 10.0 scale)
Each candidate is evaluated using a composite scoring heuristic:
- **Engagement Quality (up to 4.0 pts)**: Normalized engagement rate score ($\ge 4.0\%$ ER receives full 4.0 pts).
- **Thematic Keyword Depth (up to 3.5 pts)**: Frequency and specificity of target domain keywords in headline and bio.
- **Follower Sweet Spot (up to 2.5 pts)**: Optimal micro-influencer tier (15,000 to 75,000 followers) receives peak rating.

### 3. Evaluation Audit Summary
- **Total Profiles Evaluated**: **58**
- **Shortlisted (PASSED)**: **30 Micro-Influencers**
- **Excluded (FAILED)**: **28 Profiles**
  - **Audit Rationale Examples**:
    - *Follower count (500) is below the micro-influencer threshold (5,000)*
    - *Follower count (480,400) exceeds the micro-influencer ceiling (100,000) - classified as Macro*
    - *Engagement rate (1.95%) is below minimum threshold (2.0%)*

### 4. Output Datasets
- `data/processed/classified_influencers.csv`: Full audit dataset of all 58 creators with status, score, and explicit rationale.
- `data/processed/shortlisted_influencers.csv`: Clean cohort of the 30 shortlisted micro-influencers advancing to profile enrichment.
- `data/processed/classified_influencers.json`: Structured JSON audit log.

---

## 🛠️ Technology Stack

- **Language**: Python 3.9+ / Python 3.13
- **Data Modeling & Validation**: `Pydantic v2`
- **Data Extraction & Scraping**: `BeautifulSoup4`, `urllib` / `requests`
- **Data Processing & Analytics**: `Pandas`
- **AI / LLM Layer**: `google-genai`, `litellm`, `openai` *(for AI Personalization)*
- **Sending & Automation**: Python `smtplib`, `email` *(for Sending Layer)*
- **Interactive UI**: `Streamlit` *(for Outreach Tracker)*

---

## 📁 Repository Structure

```
automated-micro-influencer-outreach/
├── README.md                      # Comprehensive project documentation
├── requirements.txt               # Project dependencies
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore definitions
├── src/
│   ├── __init__.py                # Package root
│   ├── models/
│   │   ├── __init__.py
│   │   └── influencer.py          # Pydantic schemas (Raw, Discovered, Classified)
│   ├── discovery/
│   │   ├── __init__.py
│   │   ├── base.py                # Abstract BaseDiscoverySource class
│   │   ├── collabstr.py           # Collabstr live public directory scraper
│   │   └── pipeline.py            # DiscoveryPipeline orchestrator & exporter
│   ├── filtering/
│   │   ├── __init__.py
│   │   ├── criteria.py            # FilterCriteria configuration
│   │   ├── classifier.py          # InfluencerClassifier & brand-fit scoring
│   │   └── pipeline.py            # FilteringPipeline orchestrator & exporter
│   └── utils/
│       ├── __init__.py
│       └── parsers.py             # Metric parsers, engagement heuristics, theme extractors
├── scripts/
│   ├── run_discovery.py           # Discovery CLI runner
│   └── run_filtering.py           # Filtering & Classification CLI runner
└── data/
    ├── raw/
    │   ├── discovered_influencers.json   # 58 discovered creators (JSON)
    │   └── discovered_influencers.csv    # 58 discovered creators (CSV)
    └── processed/
        ├── classified_influencers.json   # Full classification audit (JSON)
        ├── classified_influencers.csv    # Full classification audit (CSV)
        └── shortlisted_influencers.csv   # 30 shortlisted micro-influencers (CSV)
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/ansh-rohilla/automated-micro-influencer-outreach.git
cd automated-micro-influencer-outreach
```

### 2. Setup Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Discovery Pipeline
Discovers 58 verified Technology & AI influencers:
```bash
python scripts/run_discovery.py
```

### 4. Run Filtering & Classification Pipeline
Applies quantitative (5k–100k followers, >2% ER) and qualitative brand safety rules:
```bash
python scripts/run_filtering.py
```

---

## 🔄 Upcoming Modules

- **Profile Enrichment**: Extracting contact emails (or strictly marking "Not Found" if unavailable), handles, and audience demographics.
- **AI Personalization Engine**: LLM-driven generation of personalized 60–90 word email collaboration pitches and 15–30 word Instagram DMs.
- **Sending Layer**: Dispatching via SMTP / Simulation mode with duplicate prevention.
- **Outreach Tracker & UI**: Real-time campaign tracking dashboard built with Streamlit.
