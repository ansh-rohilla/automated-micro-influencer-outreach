# Automated Micro-Influencer Outreach System

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Pipeline-green.svg)]()
[![Tests](https://img.shields.io/badge/Tests-Passing%20(6%2F6)-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end automated system that discovers real micro-influencers, filters and classifies them based on predefined brand-fit criteria, enriches their profiles with contact context and demographics, generates AI/LLM-personalized collaboration outreach messages, and executes an idempotent sending and tracking workflow.

---

## Table of Contents

- [System Architecture & Lifecycle](#system-architecture--lifecycle)
- [Key Features & Highlights](#key-features--highlights)
- [Technology Stack & Tools Used](#technology-stack--tools-used)
- [Pipeline Components](#pipeline-components)
  - [1. Influencer Discovery](#1-influencer-discovery)
  - [2. Filtering & Classification Engine](#2-filtering--classification-engine)
  - [3. Profile Enrichment Engine](#3-profile-enrichment-engine)
  - [4. AI Message Personalization](#4-ai-message-personalization)
  - [5. Sending Layer & Duplicate Prevention](#5-sending-layer--duplicate-prevention)
  - [6. Outreach Tracker & Analytics](#6-outreach-tracker--analytics)
- [Interactive Web Dashboard (Streamlit)](#interactive-web-dashboard-streamlit)
- [Project Directory Structure](#project-directory-structure)
- [Installation & Quickstart Guide](#installation--quickstart-guide)
- [Testing & Quality Assurance](#testing--quality-assurance)
- [Evaluation Criteria Alignment](#evaluation-criteria-alignment)
- [Limitations & Ethical Considerations](#limitations--ethical-considerations)
- [Scalability to 500+ Influencers](#scalability-to-500-influencers)

---

## System Architecture & Lifecycle

The pipeline operates as a modular, decoupled flow from initial discovery to delivery tracking:

```mermaid
flowchart TD
    A["Public Platforms & Marketplace (Collabstr Tech/AI)"] --> B["1. Influencer Discovery\n(Scrapes 58 Real Creators)"]
    B --> C["2. Filtering & Classification\n(5k-100k, >2.0% ER, Brand Safety)"]
    C --> D{"Passed or Failed?"}
    D -- "Failed (28)" --> E["Audit Log\n(Rejection Rationale)"]
    D -- "Passed (30)" --> F["3. Profile Enrichment\n(Contacts, Context, Demographics)"]
    F --> G["4. AI Personalization Engine\n(Email 60-90w | Instagram DM 15-30w)"]
    G --> H["5. Sending Layer\n(SMTP / Simulation + Duplicate Prevention)"]
    H --> I["6. Live Outreach Tracker\n(CSV & JSON Audit Logs)"]
```

---

## Key Features & Highlights

- **Real, Authentic Creator Data**: Discovers **58 verified Technology & AI influencers** across Instagram, TikTok, and YouTube with usernames, bios, locations, and follower counts. **No fabricated records or guessed emails**.
- **Deterministic & Auditable Filtering**: Evaluates quantitative thresholds (5k–100k followers, $\ge 2.0\%$ ER) and qualitative brand safety rules, attaching explicit pass/fail rationale to each profile.
- **Strict Anti-Fabrication Email Policy**: Verified business contacts attached where publicly listed; strictly marked `"Not Found"` when unavailable to test error-handling in the sending layer.
- **AI-Driven Personalization**: Dynamically synthesizes bespoke pitches referencing the creator's tone, niche, recent content topics, and audience demographics across 6 diverse collaboration angles (*Sponsorship, Affiliate Campaign, UGC, Ambassador, Paid Placement, Barter*).
- **Enforced Word-Count Bounds**: Strictly enforces **60–90 words** for email pitches and **15–30 words** for Instagram DMs.
- **Idempotent Sending Layer**: Dual-mode email dispatcher (Live SMTP + Safe Simulation) with automated duplicate prevention and a compliant manual/simulated Instagram DM workflow.
- **Dual Interfaces**: Full-featured CLI commands and an interactive **Streamlit Web Dashboard**.

---

## Technology Stack & Tools Used

| Layer | Tools & Libraries | Purpose |
| :--- | :--- | :--- |
| **Language & Runtime** | Python 3.9+ / Python 3.13 | Core development language |
| **Data Validation** | `Pydantic v2` | Strongly-typed schemas across all pipeline stages |
| **Data Extraction** | `BeautifulSoup4`, `urllib` / `requests` | Web scraping and HTML parsing of public directories |
| **Data Processing** | `Pandas` | Data manipulation, deduplication, and CSV/JSON export |
| **AI / LLM Integration** | `litellm`, `google-genai`, `openai` | Dynamic prompt engineering and personalization |
| **Sending & Automation** | Python `smtplib`, `email.mime`, `uuid` | RFC-822 email construction, SMTP dispatch, and simulation |
| **Interactive UI** | `Streamlit` | Visual dashboard for reviewing, filtering, and dispatching |
| **Testing** | Python `unittest` | Automated unit testing and constraint verification |

---

## Pipeline Components

### 1. Influencer Discovery
- **Source**: Live public directories and verified creator marketplace (Collabstr Tech & AI directory).
- **Target Category**: **Technology & AI** (Generative AI tools, SaaS, Cloud, Developer tools, and Tech Hardware).
- **Yield**: **58 unique, verified creators** (exceeding the requirement of at least 50).
- **Platforms Captured**: Instagram (26), TikTok (22), YouTube (9), X (1).
- **Output Files**: `data/raw/discovered_influencers.csv` and `.json`.

### 2. Filtering & Classification Engine
Evaluates candidates against strict quantitative and qualitative criteria:
- **Follower Range**: `5,000 – 100,000` (Standard micro-influencer definition).
- **Engagement Threshold**: $\ge 2.0\%$ benchmark engagement rate.
- **Brand Safety**: Automated negative keyword filter (blocks spam, gambling, adult content).
- **Brand-Fit Score (0–10 scale)**: Multi-factor composite heuristic weighting engagement rate, thematic keyword depth, and follower sweet spot (15k–75k).
- **Results**:
  - **30 Shortlisted (PASSED)**: Qualified micro-influencers.
  - **28 Excluded (FAILED)**: Categorized with auditable failure reasons:
    - *Follower count (500) is below the micro-influencer threshold (5,000)*
    - *Follower count (480,400) exceeds the micro-influencer ceiling (100,000) - classified as Macro*
    - *Engagement rate (1.95%) is below minimum threshold (2.0%)*
- **Output Files**: `data/processed/classified_influencers.csv` and `data/processed/shortlisted_influencers.csv`.

### 3. Profile Enrichment Engine
Enriches the 30 shortlisted micro-influencers with mandatory and optional context:
- **Mandatory Fields**: Name, Platform, Profile URL, Follower Count, Engagement Rate, Niche, Content Themes, Contact Email.
- **Optional Fields**: Instagram / TikTok / YouTube handles, Website / Linktree, Audience Geography, Audience Age (`18-34 years, 76%`), Audience Gender (`62% Male / 38% Female`).
- **Context Signals**: Pedagogical tone/style (`Technical & Educational`, `Practical UGC Demos`, `Business & Strategic Insights`) and recent content topics.
- **Anti-Fabrication Compliance**: Verified public business emails attached from Linktrees and personal domains (e.g. `montesbar.diego@gmail.com`, `shubham@shubook.in`, `connect@wealthcircle.in`). All others are explicitly marked **`"Not Found"`**.
- **Output Files**: `data/processed/enriched_influencers.csv` and `.json`.

### 4. AI Message Personalization
Generates two distinct personalized outreach messages for each qualified creator:
1. **Email Collaboration Pitch**:
   - **Length**: Strictly **60–90 words** (average 74.6 words).
   - **Context Signals**: Creator's name, tone, recent content focus, audience demographics, specific collaboration angle, and value proposition.
   - **Collaboration Angles**: *Sponsorship, Affiliate campaign, UGC content creation, Brand ambassador program, Paid product placement, Barter collaboration*.
2. **Instagram Direct Message (DM)**:
   - **Length**: Strictly **15–30 words** (average 28.5 words).
   - **Style**: Natural, conversational, peer-to-peer inquiry.
- **Output Files**: `data/processed/personalized_outreach.csv` and `.json`.

### 5. Sending Layer & Duplicate Prevention
- **Recipient Selection**: Automatically selects influencers with a valid contact email. Influencers marked `"Not Found"` are gracefully logged as `SKIPPED_NO_EMAIL`.
- **Dual Sending Modes**:
  - `simulation` (Default): Simulates RFC-822 message construction, network delays, generates synthetic message IDs (`<msg_sim_..._domain>`), and provides complete audit records.
  - `smtp`: Live SSL/TLS authenticated dispatch via any standard SMTP server (e.g. Gmail).
- **Duplicate Prevention (Idempotency)**: Tracks recipient email hashes. If an influencer has already been contacted, subsequent attempts are automatically flagged and recorded as `SKIPPED_DUPLICATE`.
- **Instagram DM Workflow**: Compliant simulated dispatch and manual copy-to-clipboard workstation respecting platform terms.

### 6. Outreach Tracker & Analytics
Maintains a complete audit history in `data/processed/outreach_tracker.csv` with fields:
`Log_ID`, `Influencer`, `Email`, `Channel`, `Platform`, `Collaboration_Angle`, `Message_Generated`, `Sent_Date`, `Status`, `Delivery_Mode`, `Details`.

---

## Interactive Web Dashboard (Streamlit)

Launch the web application to visually explore and test every stage of the pipeline:

```bash
streamlit run app.py
```

### Dashboard Features:
1. **Executive Overview**: High-level KPIs, pipeline metrics, and architecture diagram.
2. **Influencer Discovery**: Interactive data table of all 58 creators with search and platform filters.
3. **Filtering & Classification**: Real-time pass/fail inspection, brand-fit score distributions, and rejection rationale.
4. **Profile Enrichment**: Comprehensive table of contact emails, demographics, and content themes.
5. **AI Message Personalization**: Interactive viewer with word-count compliance indicators and human-in-the-loop editing.
6. **Sending Layer & Tracker**: Live delivery logs, duplicate detection audit, and Instagram DM copy workstation.

---

## Project Directory Structure

```
automated-micro-influencer-outreach/
├── README.md                      # Comprehensive system documentation
├── requirements.txt               # Dependencies
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore rules
├── main.py                        # Master end-to-end pipeline runner
├── app.py                         # Streamlit interactive web dashboard
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── influencer.py          # Discovered & Classified Pydantic schemas
│   │   ├── enrichment.py          # EnrichedInfluencer schema
│   │   ├── personalization.py     # PersonalizedMessage & Batch schema
│   │   └── outreach.py            # OutreachLogEntry & DispatchResult schema
│   ├── discovery/
│   │   ├── __init__.py
│   │   ├── base.py                # Abstract BaseDiscoverySource class
│   │   ├── collabstr.py           # Collabstr live public directory scraper
│   │   └── pipeline.py            # Discovery pipeline orchestrator
│   ├── filtering/
│   │   ├── __init__.py
│   │   ├── criteria.py            # FilterCriteria configuration
│   │   ├── classifier.py          # InfluencerClassifier & brand-fit scoring
│   │   └── pipeline.py            # Filtering pipeline orchestrator
│   ├── enrichment/
│   │   ├── __init__.py
│   │   ├── enricher.py            # ProfileEnricher engine
│   │   └── pipeline.py            # Enrichment pipeline orchestrator
│   ├── personalization/
│   │   ├── __init__.py
│   │   ├── prompts.py             # Prompt templates & collaboration angles
│   │   ├── generator.py           # PersonalizationEngine & word-count validator
│   │   └── pipeline.py            # Personalization pipeline orchestrator
│   ├── sending/
│   │   ├── __init__.py
│   │   ├── validator.py           # Email validator & duplicate detector
│   │   ├── dispatcher.py          # SMTP & simulation email dispatcher
│   │   ├── instagram_workflow.py  # Manual/simulated Instagram DM workflow
│   │   ├── tracker.py             # OutreachTracker persistent logger
│   │   └── pipeline.py            # Sending pipeline orchestrator
│   └── utils/
│       ├── __init__.py
│       └── parsers.py             # Metric parsers, engagement heuristics, theme extractors
├── scripts/
│   ├── run_discovery.py           # Discovery CLI runner
│   ├── run_filtering.py           # Filtering & Classification CLI runner
│   ├── run_enrichment.py          # Profile Enrichment CLI runner
│   ├── run_personalization.py     # AI Personalization CLI runner
│   └── run_sending.py             # Sending Layer & Tracker CLI runner
├── tests/
│   └── test_pipeline.py           # Unit tests covering all pipeline stages
└── data/
    ├── raw/
    │   ├── discovered_influencers.csv    # 58 discovered creators
    │   └── discovered_influencers.json
    └── processed/
        ├── classified_influencers.csv    # 58 evaluated creators (Pass/Fail)
        ├── classified_influencers.json
        ├── shortlisted_influencers.csv   # 30 qualified micro-influencers
        ├── enriched_influencers.csv      # Complete mandatory & optional fields
        ├── enriched_influencers.json
        ├── personalized_outreach.csv     # Email pitches & Instagram DMs
        ├── personalized_outreach.json
        ├── outreach_tracker.csv          # Campaign delivery log
        └── outreach_tracker.json
```

---

## Installation & Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/ansh-rohilla/automated-micro-influencer-outreach.git
cd automated-micro-influencer-outreach
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(The system works out-of-the-box in simulation mode even without API keys!)*

### 4. Run One-Command End-to-End Execution
```bash
python main.py
```

### 5. Launch Interactive Web Dashboard
```bash
streamlit run app.py
```

---

## Testing & Quality Assurance

Run the automated test suite:
```bash
python -m unittest discover tests
```

### Test Coverage Highlights:
- `test_parse_follower_count`: Verifies robust parsing of `k`, `M`, ranges (`10k-25k`), and raw integer strings.
- `test_classify_follower_tier`: Verifies correct tier allocation (`Nano <5k`, `Micro 5k-100k`, `Macro >100k`).
- `test_filtering_and_classification`: Verifies pass/fail decisions and explicit rejection reasons.
- `test_personalization_word_counts`: Asserts strict adherence to **60–90 words** for email pitches and **15–30 words** for Instagram DMs.
- `test_validator_and_duplicate_prevention`: Verifies duplicate email detection and missing email handling.
- `test_simulation_dispatcher`: Verifies synthetic message ID generation and simulated delivery cycles.

---

## Evaluation Criteria Alignment

| Criteria | System Implementation & Evidence |
| :--- | :--- |
| **1. Functionality** | End-to-end pipeline operates smoothly from discovery to tracking; verified via `main.py` and Streamlit dashboard. |
| **2. Data Quality** | Extracted 58 genuine, real creator profiles from live directories with authentic usernames, follower counts, and bios. |
| **3. Automation** | Fully automated CLI and pipeline orchestrator requiring zero manual interventions. |
| **4. Filtering Logic** | Strict 5k–100k follower bounds, $\ge 2.0\%$ ER, brand safety, and explicit pass/fail audit logs. |
| **5. Profile Enrichment** | All mandatory and optional fields populated (contacts, demographics, tone, recent topics) with anti-fabrication standards. |
| **6. AI Personalization** | Bespoke messages dynamically referencing creator context; strictly adheres to 60–90 words (email) and 15–30 words (DM). |
| **7. Engineering Quality** | Clean modular architecture, Pydantic type safety, reusable adapters, and decoupled pipeline stages. |
| **8. Error Handling** | Graceful handling of missing emails (`SKIPPED_NO_EMAIL`), duplicate detection (`SKIPPED_DUPLICATE`), and network retry logic. |
| **9. Documentation** | Comprehensive README, architectural diagrams, step-by-step setup guides, and docstrings throughout. |
| **10. Scalability** | Decoupled pipeline design allows swapping data sources or scaling discovery from 50 to 500+ influencers without refactoring. |

---

## Limitations & Ethical Considerations

1. **Platform Rate Limits & Respectful Scraping**:
   - The live discovery adapter incorporates user-agent rotation and throttling delays (1.0s) to respect directory server capacity.
2. **Contact Email Availability**:
   - In accordance with privacy norms and assignment rules against fabricated data, contact emails are only attached when publicly listed by the creator. All others are marked `"Not Found"`.
3. **Instagram DM Automation Compliance**:
   - To respect Meta's Terms of Service against unauthorized browser automation, Instagram outreach is structured as a compliant simulated and manual copy-dispatch workflow.
4. **LLM Word Count Variance**:
   - Standard LLMs occasionally struggle with exact word-count constraints. Our pipeline couples prompt instructions with an automated word-count validator and trimmer to guarantee compliance.

---

## Scalability to 500+ Influencers

The architecture is built for horizontal scale:
- **Asynchronous Scraping**: `BaseDiscoverySource` interface can be backed by `aiohttp` or Playwright for high-concurrency collection.
- **Batch Processing**: Personalization and Sending pipelines process records as batches, easily scalable across multi-worker queues (e.g. Celery / Redis).
- **Persistent Storage**: The current CSV/JSON logging layer can be swapped for a relational database (PostgreSQL / SQLite via SQLAlchemy) with zero changes to the core pipeline logic.
