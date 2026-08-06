# Review Intelligence Agent

## Overview

Review Intelligence Agent is a proof-of-concept system designed to transform large volumes of app store reviews into actionable product insights.

The goal is to help product teams understand recurring user problems, identify release-related issues, prioritize critical reviews, and reduce manual review analysis.

The system uses AI-based review classification combined with aggregation and visualization layers to move from individual reviews to portfolio-level insights.

---

# Problem

Mobile apps receive hundreds or thousands of reviews across different apps, countries, languages, and versions.

Reading reviews one by one makes it difficult to identify:

- Recurring bugs
- Feature requests
- Release regressions
- Performance issues
- Payment/account problems
- Reviews requiring personal attention

The challenge is turning unstructured user feedback into structured product decisions.

---

# Solution

The system analyzes reviews through an AI-powered pipeline:

```
App Store Reviews
        |
        ↓
Review Classification Agent
        |
        ↓
Structured Review Data
        |
        ↓
Insights & Prioritization Dashboard
        |
        ↓
Human Escalation / Automated Reply Suggestions
```

---

# Features

## 1. Review Analysis Agent

Each review is analyzed and enriched with:

- Category
- Theme
- Issue summary
- Sentiment
- Severity
- Suggested action
- Human reply requirement

Example:

Input:

> "The game crashes every time I open it after the latest update"

Output:

```json
{
  "category": "Bug",
  "theme": "Crash",
  "issue_summary": "Crash occurs immediately after launching the app",
  "sentiment": "Negative",
  "severity": "Critical",
  "requires_human_reply": true,
  "suggested_action": "Investigate bug"
}
```

---

## 2. Theme Normalization

A key challenge in review analysis is that users describe the same problem differently.

Examples:

```
"App crashes on startup"
"Game closes immediately"
"Crash after update"
```

are grouped into:

```
Theme: Crash
```

This allows meaningful aggregation and prevents fragmented insights.

---

## 3. Product Insights Dashboard

The dashboard provides multiple levels of analysis:

### Review Level

Shows every review enriched with AI-generated analysis.

### Portfolio Level

Identifies the most common issues across all apps.

Example:

| Theme | Severity | Count |
|---|---|---|
| Crash | Critical | 25 |
| Performance | High | 18 |
| Login Issue | High | 12 |

---

### App Level

Compares issues across different applications.

Example:

| App | Theme | Count |
|---|---|---|
| Game A | Crash | 12 |
| Game B | Payment | 8 |

---

### Release Impact Analysis

Identifies issues associated with specific app versions.

Example:

| Version | Theme | Count |
|---|---|---|
| 5.8.0 | Crash | 15 |
| 5.8.0 | Performance | 10 |

This helps identify possible regressions after releases.

---

## 4. Human-in-the-loop Workflow

Not every review requires manual handling.

The system identifies reviews that need human attention:

Examples:

- 1-star reviews
- Account access issues
- Payment problems
- Lost progress
- Highly frustrated users

These reviews are separated into a dedicated queue.

---

## 5. Automated Reply Suggestions

For lower-risk reviews, the system generates suggested responses.

Examples:

- Positive feedback
- General comments
- Non-critical complaints

Critical cases remain under human review.

---

# Architecture

```
                 Excel Reviews Dataset
                         |
                         ↓
              Review Classification Agent
                         |
                         ↓
              Structured Review Dataset
                         |
        ---------------------------------
        |               |               |
        ↓               ↓               ↓
   App Insights   Release Analysis   Human Queue
        |
        ↓
 Automated Reply Suggestions
```

---

# Technology Stack

- Python
- Streamlit
- OpenAI API
- Pandas
- OpenPyXL
- dotenv

---

# Running the Project

## 1. Clone repository

```bash
git clone <repository-url>
```

## 2. Create virtual environment

```bash
python -m venv venv
```

Activate:

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure API Key

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

## 5. Run application

```bash
streamlit run app.py
```

---

# Input Dataset Format

The application expects an Excel file with the following columns:

| Column | Description |
|---|---|
| app | Application name |
| country | Review country |
| date | Review date |
| version | App version |
| rating | User rating |
| language | Review language |
| review_text | Review content |

---

# Production Considerations

This proof-of-concept uses uploaded Excel files for simplicity.

A production implementation could include:

## Data ingestion

Connect directly to:

- Google Play Reviews API
- App Store Connect API

for continuous review collection.

---

## Storage

Persist reviews and analysis results in:

- PostgreSQL
- BigQuery
- Data warehouse solution

---

## Processing

Move analysis into an asynchronous pipeline:

```
New Review
     |
     ↓
Queue
     |
     ↓
AI Processing Worker
     |
     ↓
Database
     |
     ↓
Dashboard
```

---

## Product Workflow Integration

Future extensions:

- Automatically create Jira tickets for confirmed bugs
- Notify responsible teams
- Track issue trends over releases
- Compare apps and markets

---

# Why this approach

The system focuses on reducing noise and helping product teams answer:

- What problems are users experiencing?
- Is a new release causing issues?
- Which problems impact the most users?
- Which reviews require immediate attention?

The objective is not only to analyze reviews, but to turn user feedback into actionable product decisions.
