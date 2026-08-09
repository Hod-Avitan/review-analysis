# Review Intelligence Agent

## Overview

Review Intelligence Agent is a proof-of-concept application that analyzes app store reviews using AI and turns a large volume of user feedback into actionable product insights.
The goal of the tool is to help product teams understand what users are experiencing across multiple applications, identify recurring issues, detect release-related problems, discover feature requests, and prioritize reviews that require human attention.
Instead of manually reviewing feedback one review at a time, the system analyzes reviews, extracts structured information, groups similar issues into themes, and presents the results in a dashboard.

## Features

### AI Review Analysis

Each review is analyzed and enriched with:
- Category
- Theme
- Issue summary
- Sentiment
- Severity
- Suggested action
- Human reply recommendation

Example insights:
- Crash issues
- Performance problems
- Payment issues
- Account-related issues
- Feature requests

### Issue Clustering & Theme Detection

The application groups reviews describing similar problems into common themes.
For example:
- "App crashes on startup"
- "Game closes immediately after launch"
- "Crash after the latest update"
are grouped under a common theme such as: Crash
This helps identify recurring user problems instead of treating every review as a separate issue.

### Product Insights Dashboard

The dashboard provides portfolio-level views across multiple applications, including:
- Issues by application
- Issues by release version
- Issue trends over time
- Common themes
- Feature requests based on user feedback
- Reviews requiring human attention
- Suggested reply generation
These insights help teams identify where users are struggling and prioritize areas that require attention.

### Human-in-the-Loop Review Handling

Not every review should be handled automatically.
The system identifies reviews that may require personal attention, such as highly negative, sensitive, or critical cases.
Lower-risk reviews can move to the reply suggestion flow, while important cases remain under human review.

### Suggested Reply Generation

For lower-risk reviews, the system generates suggested replies based on app store review best practices.
The goal is to reduce manual effort while keeping responses professional, respectful, and appropriate for public store communication.

## Project Structure

```text
.
├── app.py                  # Streamlit application
├── review_agent.py         # AI review analysis logic
├── insights_agent.py       # Aggregation and insights generation
├── reply_agent.py          # AI reply suggestions
├── requirements.txt
└── sample_reviews.xlsx     # Example input dataset
```

## Technology Stack

- Python
- Streamlit
- OpenAI API
- Pandas
- OpenPyXL
- Plotly
- python-dotenv

## Running the Project

### 1. Clone the repository

```bash
git clone <repository-url>
```
### 2. Create a virtual environment

python -m venv venv

Activate:
Mac/Linux:
source venv/bin/activate

Windows:
venv\Scripts\activate

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:
OPENAI_API_KEY=api_key

### 5. Run the application

streamlit run app.py

## Input Format

The application accepts an Excel file containing app store reviews.
Required columns:

| Column | Description |
|---|---|
| app | Application name |
| country | Review country |
| date | Review date |
| version | Application version |
| rating | Review rating |
| language | Review language |
| review_text | Review content |

## Status

This project is a proof-of-concept implementation.